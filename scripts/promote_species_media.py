#!/usr/bin/env python3
"""Promote approved species media queue records into the canonical registry.

This script is deliberately conservative. It only promotes records from
``content/media/species-media-approval-queue.yaml`` when a curator has already
set ``decision: approve_primary``, completed every required check, and filled
the approved-primary metadata.

By default it runs as a dry run and writes a reviewer report. Use ``--apply`` to
write changes to ``content/media/species-media-registry.yaml``.

Usage:
  python scripts/promote_species_media.py --all
  python scripts/promote_species_media.py --artifact-id species-blue-whale
  python scripts/promote_species_media.py --artifact-id species-blue-whale --apply
"""
from __future__ import annotations

import argparse
from collections import Counter
from copy import deepcopy
from datetime import date
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
REGISTRY_PATH = ROOT / "content" / "media" / "species-media-registry.yaml"
APPROVAL_QUEUE_PATH = ROOT / "content" / "media" / "species-media-approval-queue.yaml"
REVIEW_DIR = ROOT / "content" / "media" / "review-packs"

APPROVAL_CHECKS = {
    "image_level_rights_verified",
    "creator_and_credit_verified",
    "commercial_and_derivative_use_checked",
    "species_match_verified",
    "ethics_checked",
    "sensitive_location_checked",
    "crop_checked",
    "alt_text_written",
    "approved_surfaces_set",
}

ALLOWED_APPROVED_RIGHTS = {
    "owned",
    "licensed",
    "public-domain",
    "cc0",
    "cc-by",
    "cc-by-sa",
    "partner-grant",
}

REQUIRED_APPROVED_FIELDS = [
    "approved_asset_id",
    "source_url",
    "creator",
    "credit",
    "license",
    "rights_status",
    "alt_text",
    "species_match_basis",
    "crop_guidance",
    "ethics_notes",
    "approved_surfaces",
    "blocked_surfaces",
]


def load_yaml(path: Path):
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def rel(path: Path):
    return path.relative_to(ROOT).as_posix()


def selected_records(queue_records, artifact_id, all_records):
    if artifact_id and all_records:
        raise SystemExit("Use either --artifact-id or --all, not both.")
    if artifact_id:
        selected = [record for record in queue_records if record.get("artifact_id") == artifact_id]
        if not selected:
            raise SystemExit(f"No approval queue record found for {artifact_id!r}.")
        return selected
    if all_records:
        return queue_records
    raise SystemExit("Specify --artifact-id <id> or --all.")


def record_blockers(queue_record, registry_record):
    blockers = []
    if not registry_record:
        blockers.append("missing registry record")
        return blockers

    if queue_record.get("species_page") != registry_record.get("species_page"):
        blockers.append("queue species_page does not match registry")

    decision = queue_record.get("decision")
    if decision != "approve_primary":
        blockers.append(f"decision is {decision!r}, not 'approve_primary'")

    checks = queue_record.get("checks") or {}
    for key in sorted(APPROVAL_CHECKS):
        if checks.get(key) is not True:
            blockers.append(f"check not true: {key}")

    if not queue_record.get("reviewer"):
        blockers.append("missing reviewer")
    if not queue_record.get("reviewed_on"):
        blockers.append("missing reviewed_on")

    approved = queue_record.get("approved_primary_template") or {}
    for key in REQUIRED_APPROVED_FIELDS:
        if not approved.get(key):
            blockers.append(f"missing approved_primary_template.{key}")

    rights_status = approved.get("rights_status")
    if rights_status and rights_status not in ALLOWED_APPROVED_RIGHTS:
        blockers.append(f"invalid approved rights_status: {rights_status!r}")

    registry_primary = registry_record.get("primary") or {}
    registry_candidate = registry_primary.get("candidate") or registry_primary.get("approved_from_candidate") or {}
    queue_candidate = queue_record.get("candidate") or {}
    if queue_candidate.get("asset_id") != registry_candidate.get("asset_id"):
        blockers.append("queue candidate asset_id does not match registry candidate")

    approved_path = approved.get("approved_path")
    if approved_path and not (ROOT / approved_path).exists():
        blockers.append(f"approved_path does not exist: {approved_path}")

    return blockers


def approved_primary_from_queue(queue_record):
    candidate = queue_record.get("candidate") or {}
    approved = deepcopy(queue_record.get("approved_primary_template") or {})
    primary = {
        "status": "approved",
        "approved_asset_id": approved.get("approved_asset_id"),
        "approved_path": approved.get("approved_path"),
        "rights_status": approved.get("rights_status"),
        "qa_status": "approved",
        "source_url": approved.get("source_url"),
        "original_media_url": approved.get("original_media_url"),
        "creator": approved.get("creator"),
        "credit": approved.get("credit"),
        "license": approved.get("license"),
        "license_url": approved.get("license_url"),
        "alt_text": approved.get("alt_text"),
        "species_match_basis": approved.get("species_match_basis"),
        "crop_guidance": approved.get("crop_guidance"),
        "ethics_notes": approved.get("ethics_notes"),
        "approved_surfaces": approved.get("approved_surfaces") or [],
        "blocked_surfaces": approved.get("blocked_surfaces") or [],
        "reviewer": queue_record.get("reviewer"),
        "reviewed_on": queue_record.get("reviewed_on"),
        "approved_from_candidate": candidate,
    }
    return primary


def apply_promotion(registry_record, queue_record):
    registry_record["media_status"] = "approved_primary"
    registry_record["primary"] = approved_primary_from_queue(queue_record)
    registry_record["next_action"] = (
        f"Primary media approved for {registry_record.get('common_name')}. "
        "Keep source, rights, crop, alt text, and ethics metadata current during future reviews."
    )


def build_report(results, applied):
    counts = Counter(result["status"] for result in results)
    lines = [
        "# Species Media Promotion Report",
        "",
        f"Generated: {date.today().isoformat()}",
        f"Mode: {'apply' if applied else 'dry-run'}",
        "",
        "This report records which approval-queue records can be promoted into the canonical species media registry.",
        "",
        "## Summary",
        "",
        f"- Records checked: {len(results)}",
        "- Statuses: " + ", ".join(f"{key}={value}" for key, value in sorted(counts.items())),
        "",
        "## Results",
        "",
        "| Species | Artifact id | Status | Notes |",
        "|---|---|---|---|",
    ]
    for result in results:
        notes = "; ".join(result.get("blockers") or []) or result.get("notes") or "-"
        lines.append(
            f"| {result.get('common_name') or '-'} | `{result['artifact_id']}` | `{result['status']}` | {notes} |"
        )
    return "\n".join(lines).rstrip() + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--artifact-id", help="Promote/check a single approval queue record.")
    parser.add_argument("--all", action="store_true", help="Promote/check every approval queue record.")
    parser.add_argument("--apply", action="store_true", help="Write approved promotions to the registry.")
    parser.add_argument("--registry", type=Path, default=REGISTRY_PATH)
    parser.add_argument("--approval-queue", type=Path, default=APPROVAL_QUEUE_PATH)
    args = parser.parse_args()

    registry_path = args.registry if args.registry.is_absolute() else ROOT / args.registry
    queue_path = args.approval_queue if args.approval_queue.is_absolute() else ROOT / args.approval_queue
    registry = load_yaml(registry_path)
    queue = load_yaml(queue_path)
    registry_by_id = {record.get("artifact_id"): record for record in registry.get("records") or []}
    queue_records = selected_records(queue.get("records") or [], args.artifact_id, args.all)

    results = []
    for queue_record in queue_records:
        artifact_id = queue_record.get("artifact_id")
        registry_record = registry_by_id.get(artifact_id)
        blockers = record_blockers(queue_record, registry_record)
        if blockers:
            results.append(
                {
                    "artifact_id": artifact_id,
                    "common_name": queue_record.get("common_name"),
                    "status": "blocked",
                    "blockers": blockers,
                }
            )
            continue

        if args.apply:
            apply_promotion(registry_record, queue_record)
            status = "promoted"
            notes = "registry updated"
        else:
            status = "promotable"
            notes = "dry-run only; use --apply to update registry"
        results.append(
            {
                "artifact_id": artifact_id,
                "common_name": queue_record.get("common_name"),
                "status": status,
                "notes": notes,
            }
        )

    REVIEW_DIR.mkdir(parents=True, exist_ok=True)
    stamp = date.today().isoformat()
    yaml_path = REVIEW_DIR / f"species-media-promotion-report-{stamp}.yaml"
    md_path = REVIEW_DIR / f"species-media-promotion-report-{stamp}.md"
    payload = {
        "version": stamp,
        "generated_at": stamp,
        "mode": "apply" if args.apply else "dry-run",
        "source_registry": rel(registry_path),
        "source_approval_queue": rel(queue_path),
        "policy": {
            "promotion_requires_curator_approval": True,
            "dry_run_by_default": True,
            "approved_primary_images_must_pass_registry_validator": True,
        },
        "summary": {
            "records_checked": len(results),
            "status_counts": dict(sorted(Counter(result["status"] for result in results).items())),
        },
        "results": results,
    }
    yaml_path.write_text(yaml.safe_dump(payload, sort_keys=False, allow_unicode=False, width=120), encoding="utf-8")
    md_path.write_text(build_report(results, args.apply), encoding="utf-8")

    if args.apply:
        registry["updated"] = stamp
        registry_path.write_text(yaml.safe_dump(registry, sort_keys=False, allow_unicode=False, width=120), encoding="utf-8")

    counts = payload["summary"]["status_counts"]
    print(f"Wrote {rel(yaml_path)}")
    print(f"Wrote {rel(md_path)}")
    print(
        "Species media promotion: "
        + ", ".join(f"{key}={value}" for key, value in sorted(counts.items()))
    )
    return 1 if any(result["status"] == "blocked" for result in results) and args.apply else 0


if __name__ == "__main__":
    raise SystemExit(main())
