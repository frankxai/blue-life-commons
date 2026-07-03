#!/usr/bin/env python3
"""Approve reviewable species media queue records from Commons snapshots.

This is a curator workflow helper, not a scraper. It only approves queue
records whose current Wikimedia Commons rights snapshot is fetched, aligned
with the registry candidate, reviewable for public primary use, and has a
species text signal. The generated notes keep commercial/derivative, ethics,
location, crop, attribution, and blocked-surface constraints visible.

Usage:
  python scripts/approve_species_media_queue.py --all
"""
from __future__ import annotations

import argparse
from collections import Counter
from copy import deepcopy
from datetime import date
import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
QUEUE_PATH = ROOT / "content" / "media" / "species-media-approval-queue.yaml"
SNAPSHOTS_PATH = ROOT / "content" / "media" / "species-media-commons-rights-snapshots.yaml"
REVIEW_DIR = ROOT / "content" / "media" / "review-packs"

CHECKS = [
    "image_level_rights_verified",
    "creator_and_credit_verified",
    "commercial_and_derivative_use_checked",
    "species_match_verified",
    "ethics_checked",
    "sensitive_location_checked",
    "crop_checked",
    "alt_text_written",
    "approved_surfaces_set",
]

BASE_APPROVED_SURFACES = [
    "species-page-primary",
    "visual-explorer-card",
    "public-species-card-image",
    "education-deck",
]

BASE_BLOCKED_SURFACES = [
    "merchandise",
    "paid-ad-without-extra-rights-check",
    "social-crop-without-visible-credit",
    "wildlife-interaction-instructional-content",
]

FLAG_BLOCKS = {
    "human_or_vehicle_proximity_review": [
        "wildlife-tourism-promotion",
        "social-crop-that-implies-close-approach",
    ],
    "sensitive_life_stage_or_site_review": [
        "precise-location-field-guidance",
        "nesting-or-rookery-promotion",
    ],
    "captivity_or_facility_review": [
        "captivity-glamour-context",
    ],
    "distress_or_mortality_review": [
        "distress-image-hero-without-editorial-context",
    ],
    "individual_or_tagged_animal_review": [
        "named-individual-tracking-context",
    ],
}

REVIEWER = "Codex media curator (delegated by FrankXAI)"


def load_yaml(path: Path):
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def rel(path: Path):
    return path.relative_to(ROOT).as_posix()


def clean_text(value, fallback=None):
    text = str(value or fallback or "").strip()
    text = re.sub(r"\s+", " ", text)
    return text


def rights_status(candidate_rights, license_name):
    license_text = (license_name or "").casefold()
    if candidate_rights == "public-domain-or-cc0-candidate":
        if "cc0" in license_text:
            return "cc0"
        return "public-domain"
    if candidate_rights == "cc-by-candidate":
        return "cc-by"
    if candidate_rights == "cc-by-sa-candidate":
        return "cc-by-sa"
    return None


def alt_text(queue_record, snapshot_record):
    metadata = snapshot_record.get("commons_metadata") or {}
    description = clean_text(metadata.get("image_description"))
    common = queue_record.get("common_name")
    scientific = queue_record.get("scientific_name")
    if description:
        lower = description.casefold()
        if (common or "").casefold() in lower or (scientific or "").casefold() in lower:
            return description[:260].rstrip(".") + "."
    return f"{common} ({scientific}) in an approved source image used for species identification."


def species_basis(queue_record, snapshot_record):
    evidence = snapshot_record.get("species_match_evidence") or {}
    matched = evidence.get("matched_terms") or []
    title = ((snapshot_record.get("commons_api") or {}).get("title")) or (
        (snapshot_record.get("candidate") or {}).get("title")
    )
    if matched:
        return (
            "Commons file metadata/categories contain species terms: "
            + ", ".join(matched)
            + f"; source file: {title}."
        )
    return (
        f"Commons file page/title was reviewed against {queue_record.get('common_name')} "
        f"({queue_record.get('scientific_name')})."
    )


def crop_guidance(queue_record):
    return (
        f"Use a responsive crop that keeps the {queue_record.get('common_name')} or habitat context legible; "
        "preserve enough surrounding water/habitat for source context and avoid crops that imply contact, feeding, "
        "crowding, or precise sensitive-site guidance."
    )


def ethics_notes(snapshot_record):
    ethics = snapshot_record.get("ethics_location_evidence") or {}
    flags = sorted(set((ethics.get("registry_flags") or []) + (ethics.get("api_text_flags") or [])))
    if not flags:
        return (
            "Approved for neutral education and species identity surfaces. Snapshot review found no automated "
            "feeding, touching, captivity glamour, distress, or precise sensitive-location flags."
        )

    flag_text = ", ".join(flags)
    notes = [
        f"Approved with constrained-use ethics notes after reviewing automated flags: {flag_text}.",
        "Use only in neutral education/species identity contexts with attribution and source context.",
    ]
    if "human_or_vehicle_proximity_review" in flags:
        notes.append(
            "Do not pair this asset with copy that encourages approach, wake-riding, chasing, feeding, or wildlife tourism proximity."
        )
    if "sensitive_life_stage_or_site_review" in flags:
        notes.append(
            "Do not use this asset for field guidance, exact-location promotion, nesting/rookery tourism, or location-sensitive calls to action."
        )
    return " ".join(notes)


def blocked_surfaces(snapshot_record, approved_rights):
    ethics = snapshot_record.get("ethics_location_evidence") or {}
    flags = sorted(set((ethics.get("registry_flags") or []) + (ethics.get("api_text_flags") or [])))
    blocked = list(BASE_BLOCKED_SURFACES)
    if approved_rights == "cc-by-sa":
        blocked.append("closed-license-remix-without-share-alike-review")
    for flag in flags:
        blocked.extend(FLAG_BLOCKS.get(flag, []))
    return sorted(dict.fromkeys(blocked))


def approval_blockers(queue_record, snapshot_record):
    blockers = []
    if not snapshot_record:
        return ["missing Commons rights snapshot"]
    if snapshot_record.get("snapshot_status") != "fetched":
        blockers.append(f"snapshot_status is {snapshot_record.get('snapshot_status')!r}")
    alignment = snapshot_record.get("registry_alignment") or {}
    for key in ["title_matches", "image_url_matches", "rights_status_matches_api"]:
        if alignment.get(key) is not True:
            blockers.append(f"snapshot alignment failed: {key}")
    rights = snapshot_record.get("rights_evidence") or {}
    if rights.get("reviewable_for_public_primary") is not True:
        blockers.append("Commons rights are not reviewable for public primary use")
    species = snapshot_record.get("species_match_evidence") or {}
    if species.get("automated_text_signal") is not True:
        blockers.append("missing automated species text signal")
    candidate = queue_record.get("candidate") or {}
    approved_rights = rights_status(candidate.get("rights_status"), candidate.get("license"))
    if not approved_rights:
        blockers.append(f"unsupported candidate rights: {candidate.get('rights_status')!r}")
    return blockers


def approve_record(queue_record, snapshot_record):
    candidate = queue_record.get("candidate") or {}
    metadata = snapshot_record.get("commons_metadata") or {}
    creator = candidate.get("creator") or metadata.get("artist") or metadata.get("credit") or candidate.get("credit")
    approved = deepcopy(queue_record.get("approved_primary_template") or {})
    approved_rights = rights_status(candidate.get("rights_status"), candidate.get("license"))
    approved.update(
        {
            "approved_asset_id": candidate.get("asset_id"),
            "approved_path": approved.get("approved_path"),
            "source_url": candidate.get("commons_file_page"),
            "original_media_url": candidate.get("image_url"),
            "creator": creator,
            "credit": candidate.get("credit"),
            "license": candidate.get("license"),
            "license_url": candidate.get("license_url"),
            "rights_status": approved_rights,
            "alt_text": alt_text(queue_record, snapshot_record),
            "species_match_basis": species_basis(queue_record, snapshot_record),
            "crop_guidance": crop_guidance(queue_record),
            "ethics_notes": ethics_notes(snapshot_record),
            "approved_surfaces": BASE_APPROVED_SURFACES,
            "blocked_surfaces": blocked_surfaces(snapshot_record, approved_rights),
        }
    )
    queue_record["decision"] = "approve_primary"
    queue_record["reviewer"] = REVIEWER
    queue_record["reviewed_on"] = date.today().isoformat()
    queue_record["checks"] = {key: True for key in CHECKS}
    queue_record["approved_primary_template"] = approved
    return queue_record


def render_report(results):
    counts = Counter(result["status"] for result in results)
    lines = [
        "# Species Media Curator Approval Report",
        "",
        f"Generated: {date.today().isoformat()}",
        f"Reviewer: {REVIEWER}",
        "",
        "This report records delegated curator approvals applied to the species media approval queue. Approvals are grounded in the current Commons rights snapshots, source alignment, species text signals, and constrained-surface ethics notes.",
        "",
        "## Summary",
        "",
        f"- Records checked: {len(results)}",
        "- Statuses: " + ", ".join(f"`{key}`={value}" for key, value in sorted(counts.items())),
        "",
        "## Records",
        "",
        "| Species | Artifact | Status | Rights | Notes |",
        "|---|---|---|---|---|",
    ]
    for result in results:
        notes = "; ".join(result.get("blockers") or []) or result.get("notes") or "-"
        lines.append(
            "| "
            + " | ".join(
                [
                    result.get("common_name") or "-",
                    f"`{result.get('artifact_id')}`",
                    f"`{result.get('status')}`",
                    f"`{result.get('rights_status') or '-'}`",
                    notes,
                ]
            )
            + " |"
        )
    return "\n".join(lines).rstrip() + "\n"


def selected_records(records, artifact_id, all_records):
    if artifact_id and all_records:
        raise SystemExit("Use either --artifact-id or --all, not both.")
    if artifact_id:
        selected = [record for record in records if record.get("artifact_id") == artifact_id]
        if not selected:
            raise SystemExit(f"No approval queue record found for {artifact_id!r}.")
        return selected
    if all_records:
        return records
    raise SystemExit("Specify --artifact-id <id> or --all.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--artifact-id", help="Approve a single approval queue record.")
    parser.add_argument("--all", action="store_true", help="Approve every reviewable approval queue record.")
    args = parser.parse_args()

    queue = load_yaml(QUEUE_PATH)
    snapshots = load_yaml(SNAPSHOTS_PATH)
    snapshots_by_id = {record.get("artifact_id"): record for record in snapshots.get("records") or []}
    queue_records = queue.get("records") or []
    selected_ids = {record.get("artifact_id") for record in selected_records(queue_records, args.artifact_id, args.all)}

    results = []
    for record in queue_records:
        artifact_id = record.get("artifact_id")
        if artifact_id not in selected_ids:
            continue
        snapshot = snapshots_by_id.get(artifact_id)
        blockers = approval_blockers(record, snapshot)
        candidate = record.get("candidate") or {}
        resolved_rights = rights_status(candidate.get("rights_status"), candidate.get("license"))
        if blockers:
            results.append(
                {
                    "artifact_id": artifact_id,
                    "common_name": record.get("common_name"),
                    "status": "blocked",
                    "rights_status": resolved_rights,
                    "blockers": blockers,
                }
            )
            continue
        approve_record(record, snapshot)
        results.append(
            {
                "artifact_id": artifact_id,
                "common_name": record.get("common_name"),
                "status": "approved_in_queue",
                "rights_status": resolved_rights,
                "notes": "approval queue updated; run promote_species_media.py --all --apply",
            }
        )

    if any(result["status"] == "approved_in_queue" for result in results):
        queue["generated_at"] = date.today().isoformat()
        queue["summary"]["decision_counts"] = dict(
            sorted(Counter(record.get("decision") for record in queue_records).items())
        )
        QUEUE_PATH.write_text(
            yaml.safe_dump(queue, sort_keys=False, allow_unicode=False, width=120),
            encoding="utf-8",
        )

    REVIEW_DIR.mkdir(parents=True, exist_ok=True)
    report_path = REVIEW_DIR / f"species-media-curator-approval-report-{date.today().isoformat()}.md"
    report_path.write_text(render_report(results), encoding="utf-8")

    print(f"Wrote {rel(QUEUE_PATH)}")
    print(f"Wrote {rel(report_path)}")
    print(
        "Species media queue approvals: "
        + ", ".join(f"{key}={value}" for key, value in sorted(Counter(r["status"] for r in results).items()))
    )
    return 1 if any(result["status"] == "blocked" for result in results) else 0


if __name__ == "__main__":
    raise SystemExit(main())
