#!/usr/bin/env python3
"""Build a curator approval queue for staged species media candidates.

This creates a durable checklist per species so candidate media can be promoted
without losing source, rights, species-match, ethics, crop, alt-text, or credit
requirements. The queue is intentionally pending by default; this script does
not approve media or edit the canonical registry.

Usage:
  python scripts/build_species_media_approval_queue.py
"""
from __future__ import annotations

from collections import Counter
from datetime import date
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
REGISTRY_PATH = ROOT / "content" / "media" / "species-media-registry.yaml"
SOURCE_ROUTING_PATH = ROOT / "content" / "media" / "species-media-source-routing.yaml"
RICH_EMBEDS_PATH = ROOT / "content" / "media" / "species-media-rich-embeds.yaml"
APPROVAL_QUEUE_PATH = ROOT / "content" / "media" / "species-media-approval-queue.yaml"
REVIEW_DIR = ROOT / "content" / "media" / "review-packs"

CHECKLIST = {
    "image_level_rights_verified": "Image-level license or permission was checked at the source.",
    "creator_and_credit_verified": "Creator, photographer, institution, and credit line were captured exactly.",
    "commercial_and_derivative_use_checked": "Commercial, derivative, attribution, and share-alike obligations were checked.",
    "species_match_verified": "Species match is grounded in source caption, taxon page, partner assertion, or expert review.",
    "ethics_checked": "Depiction does not encourage unsafe proximity, feeding, touching, baiting, chasing, crowding, or captivity glamour.",
    "sensitive_location_checked": "Caption, crop, EXIF, and context do not expose precise sensitive animal or vulnerable habitat locations.",
    "crop_checked": "Desktop, mobile, and card crops keep the animal/habitat legible and avoid misleading context.",
    "alt_text_written": "Alt text describes the visual without unsupported behavioral or conservation claims.",
    "approved_surfaces_set": "Approved and blocked surfaces are recorded.",
}

DECISIONS = {
    "pending",
    "approve_primary",
    "reject_candidate",
    "replace_candidate",
    "use_source_card_only",
}


def load_yaml(path: Path):
    if not path.exists():
        return {}
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def rel(path: Path):
    return path.relative_to(ROOT).as_posix()


def by_artifact(path: Path):
    payload = load_yaml(path)
    return {record.get("artifact_id"): record for record in payload.get("records") or []}


def normalize_approved_rights(candidate_rights):
    return {
        "public-domain-or-cc0-candidate": None,
        "cc-by-candidate": "cc-by",
        "cc-by-sa-candidate": "cc-by-sa",
    }.get(candidate_rights)


def approval_record(record, source_route, fallback):
    primary = record.get("primary") or {}
    candidate = primary.get("candidate") or {}
    source_card = (fallback or {}).get("source_card") or {}
    route = source_route.get("route") if source_route else None
    priority = source_route.get("priority") if source_route else None
    candidate_asset_id = candidate.get("asset_id")
    suggested_rights = normalize_approved_rights(candidate.get("rights_status"))

    return {
        "artifact_id": record.get("artifact_id"),
        "species_page": record.get("species_page"),
        "common_name": record.get("common_name"),
        "scientific_name": record.get("scientific_name"),
        "taxon_group": record.get("taxon_group"),
        "priority": priority,
        "source_route": route,
        "decision": "pending",
        "reviewer": None,
        "reviewed_on": None,
        "candidate": {
            "asset_id": candidate_asset_id,
            "provider": candidate.get("provider"),
            "title": candidate.get("title"),
            "commons_file_page": candidate.get("commons_file_page"),
            "image_url": candidate.get("image_url"),
            "creator": candidate.get("creator"),
            "credit": candidate.get("credit"),
            "license": candidate.get("license"),
            "license_url": candidate.get("license_url"),
            "rights_status": candidate.get("rights_status"),
            "flags": candidate.get("flags") or [],
            "score": candidate.get("score"),
        },
        "source_card_fallback": {
            "status": source_card.get("status"),
            "public_use": source_card.get("public_use"),
            "source_url": source_card.get("source_url"),
            "domain": source_card.get("domain"),
        },
        "checks": {key: False for key in CHECKLIST},
        "approved_primary_template": {
            "approved_asset_id": candidate_asset_id,
            "approved_path": None,
            "source_url": candidate.get("commons_file_page"),
            "original_media_url": candidate.get("image_url"),
            "creator": candidate.get("creator"),
            "credit": candidate.get("credit"),
            "license": candidate.get("license"),
            "license_url": candidate.get("license_url"),
            "rights_status": suggested_rights,
            "alt_text": None,
            "species_match_basis": None,
            "crop_guidance": None,
            "ethics_notes": None,
            "approved_surfaces": [
                "species-page-primary",
                "visual-explorer-card",
                "education-deck",
            ],
            "blocked_surfaces": [
                "social-crop-until-reviewed",
                "merchandise",
                "paid-ad-without-extra-rights-check",
            ],
        },
        "promotion_rule": (
            "Only change decision to approve_primary after every check is true, reviewer/reviewed_on are set, "
            "and approved_primary_template fields are complete."
        ),
    }


def build_queue():
    registry = load_yaml(REGISTRY_PATH)
    routes = by_artifact(SOURCE_ROUTING_PATH)
    fallbacks = by_artifact(RICH_EMBEDS_PATH)
    records = [
        approval_record(record, routes.get(record.get("artifact_id")) or {}, fallbacks.get(record.get("artifact_id")))
        for record in registry.get("records") or []
    ]
    decision_counts = Counter(record["decision"] for record in records)
    route_counts = Counter(record.get("source_route") or "none" for record in records)
    priority_counts = Counter(record.get("priority") or "none" for record in records)
    flagged = [record["artifact_id"] for record in records if record["candidate"].get("flags")]
    return {
        "version": date.today().isoformat(),
        "generated_at": date.today().isoformat(),
        "source_registry": rel(REGISTRY_PATH),
        "source_routing": rel(SOURCE_ROUTING_PATH) if SOURCE_ROUTING_PATH.exists() else None,
        "source_cards": rel(RICH_EMBEDS_PATH) if RICH_EMBEDS_PATH.exists() else None,
        "policy": {
            "queue_is_not_approval": True,
            "candidate_public_use": False,
            "approval_requires_all_checks_true": True,
            "source_card_fallback_does_not_grant_image_reuse": True,
        },
        "checklist_definitions": CHECKLIST,
        "allowed_decisions": sorted(DECISIONS),
        "summary": {
            "species_records": len(records),
            "decision_counts": dict(sorted(decision_counts.items())),
            "source_route_counts": dict(sorted(route_counts.items())),
            "priority_counts": dict(sorted(priority_counts.items())),
            "flagged_candidate_records": flagged,
        },
        "records": records,
    }


def render_markdown(payload):
    summary = payload["summary"]
    lines = [
        "# Species Media Approval Queue",
        "",
        f"Generated: {payload['generated_at']}",
        "",
        "This queue is a curator worksheet. It does not approve images. Promotion to primary media requires every check to be true plus complete reviewer, date, credit, alt text, crop, species-match, rights, and surface fields.",
        "",
        "## Summary",
        "",
        f"- Species records: {summary['species_records']}",
        "- Decisions: " + ", ".join(f"{k}={v}" for k, v in summary["decision_counts"].items()),
        "- Source routes: " + ", ".join(f"{k}={v}" for k, v in summary["source_route_counts"].items()),
        "- Priorities: " + ", ".join(f"{k}={v}" for k, v in summary["priority_counts"].items()),
        f"- Flagged candidates: {len(summary['flagged_candidate_records'])}",
        "",
        "## Queue Board",
        "",
        "| Priority | Species | Decision | Route | Candidate rights | Source card | Flags |",
        "|---|---|---|---|---|---|---|",
    ]
    for record in payload["records"]:
        flags = ", ".join(record["candidate"].get("flags") or []) or "-"
        source_card = record["source_card_fallback"].get("status") or "-"
        rights = record["candidate"].get("rights_status") or "-"
        lines.append(
            f"| {record.get('priority') or '-'} | {record['common_name']} | `{record['decision']}` | `{record.get('source_route') or '-'}` | `{rights}` | `{source_card}` | {flags} |"
        )

    lines.extend(["", "## Required Approval Checks", ""])
    for key, description in payload["checklist_definitions"].items():
        lines.append(f"- `{key}`: {description}")

    lines.extend(["", "## Per-Species Approval Cards", ""])
    for record in payload["records"]:
        candidate = record["candidate"]
        template = record["approved_primary_template"]
        lines.extend(
            [
                f"### {record['common_name']} (*{record['scientific_name']}*)",
                "",
                f"- Artifact id: `{record['artifact_id']}`",
                f"- Species page: `{record['species_page']}`",
                f"- Decision: `{record['decision']}`",
                f"- Route: `{record.get('source_route') or '-'}`",
                f"- Candidate: {candidate.get('title') or 'None'}",
                f"- Candidate file: {candidate.get('commons_file_page') or 'None'}",
                f"- Candidate image: {candidate.get('image_url') or 'None'}",
                f"- Candidate rights: `{candidate.get('rights_status') or 'none'}`",
                f"- Source-card fallback: `{record['source_card_fallback'].get('status') or 'none'}` ({record['source_card_fallback'].get('source_url') or 'no URL'})",
                f"- Suggested approved rights: `{template.get('rights_status') or 'fill manually'}`",
                "",
                "Checks:",
            ]
        )
        for key in CHECKLIST:
            lines.append(f"- [ ] `{key}`")
        lines.extend(
            [
                "",
                "Fields to complete before approval:",
                "- `reviewer`",
                "- `reviewed_on`",
                "- `approved_primary_template.alt_text`",
                "- `approved_primary_template.species_match_basis`",
                "- `approved_primary_template.crop_guidance`",
                "- `approved_primary_template.ethics_notes`",
                "- `approved_primary_template.rights_status` when the suggested value is blank or too broad",
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def main():
    payload = build_queue()
    APPROVAL_QUEUE_PATH.parent.mkdir(parents=True, exist_ok=True)
    REVIEW_DIR.mkdir(parents=True, exist_ok=True)
    md_path = REVIEW_DIR / f"species-media-approval-queue-{date.today().isoformat()}.md"
    APPROVAL_QUEUE_PATH.write_text(
        yaml.safe_dump(payload, sort_keys=False, allow_unicode=False, width=120),
        encoding="utf-8",
    )
    md_path.write_text(render_markdown(payload), encoding="utf-8")
    print(f"Wrote {rel(APPROVAL_QUEUE_PATH)}")
    print(f"Wrote {rel(md_path)}")
    print(
        "Species media approval queue: "
        f"{payload['summary']['species_records']} records, "
        f"{payload['summary']['decision_counts'].get('pending', 0)} pending decisions."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
