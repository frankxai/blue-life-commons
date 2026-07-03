#!/usr/bin/env python3
"""Build a curator workspace for moving species media toward approval.

This is the action layer above the registry, source routing, source-card
fallbacks, approval queue, and render contract. It does not approve images.
It ranks the work, exposes blockers, and gives curators the exact next move
for each species.

Usage:
  python scripts/build_species_media_curation_workspace.py
"""
from __future__ import annotations

from collections import Counter, defaultdict
from datetime import date
import json
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
SITE_DATA_PATH = ROOT / "content" / "media" / "species-media-site-data.json"
APPROVAL_QUEUE_PATH = ROOT / "content" / "media" / "species-media-approval-queue.yaml"
WORKSPACE_PATH = ROOT / "content" / "media" / "species-media-curation-workspace.yaml"
REVIEW_DIR = ROOT / "content" / "media" / "review-packs"

CHECK_ORDER = [
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

BATCH_LABELS = {
    "01_source_card_recheck": "Browser recheck",
    "02_ethics_flag_review": "Ethics flag review",
    "03_official_public_domain_fast_track": "Official/public-domain fast track",
    "04_open_public_domain_review": "Open public-domain review",
    "05_open_license_attribution": "Open-license attribution review",
    "06_partner_grant_or_new_candidate": "Partner grant or replacement candidate",
}

BATCH_ACTIONS = {
    "01_source_card_recheck": [
        "Open the source-card URL in a browser.",
        "If the page is reachable, rerun scripts/verify_species_media_links.py and rebuild rich embeds.",
        "Continue candidate review only after the public fallback state is no longer blocked.",
    ],
    "02_ethics_flag_review": [
        "Inspect the candidate crop first, before rights work.",
        "Reject, replace, or document why the automated proximity/welfare flag is acceptable.",
        "If acceptable, continue through the full approval checklist.",
    ],
    "03_official_public_domain_fast_track": [
        "Confirm the candidate creator/credit is truly official or institutional.",
        "Confirm image-level public-domain or CC0-style rights on the source page.",
        "Write alt text, crop guidance, species-match basis, ethics notes, and reviewer/date.",
    ],
    "04_open_public_domain_review": [
        "Confirm public-domain/CC0 rights at the image level.",
        "Check original source and species match; replace if source confidence is weak.",
        "Complete crop, alt text, ethics, and surface metadata before promotion.",
    ],
    "05_open_license_attribution": [
        "Capture exact creator, credit line, license URL, attribution, and share-alike obligations.",
        "Confirm commercial, derivative, and surface compatibility.",
        "Block paid ads, merchandise, or social crops unless the license/surface review allows them.",
    ],
    "06_partner_grant_or_new_candidate": [
        "Use the source-card fallback while seeking a written media grant.",
        "Send partner/institution/photographer request with species, surface, credit, and embargo terms.",
        "Replace the candidate if no permission or open-license route is available.",
    ],
}


def rel(path: Path):
    return path.relative_to(ROOT).as_posix()


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def load_yaml(path: Path):
    if not path.exists():
        return {}
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def by_artifact(payload):
    return {record.get("artifact_id"): record for record in payload.get("records") or []}


def recommended_batch(record):
    flags = (record.get("candidate") or {}).get("flags") or []
    route = (record.get("source_route") or {}).get("route")
    render_strategy = (record.get("render_contract") or {}).get("render_strategy")
    rights = (record.get("candidate") or {}).get("rights_status")

    if render_strategy == "source_card_recheck_placeholder":
        return "01_source_card_recheck"
    if flags:
        return "02_ethics_flag_review"
    if route == "official_public_domain_fast_track":
        return "03_official_public_domain_fast_track"
    if route == "open_public_domain_review" or rights == "public-domain-or-cc0-candidate":
        return "04_open_public_domain_review"
    if route == "open_license_attribution_review":
        return "05_open_license_attribution"
    return "06_partner_grant_or_new_candidate"


def workstream_for(batch):
    return {
        "01_source_card_recheck": "public_fallback_recheck",
        "02_ethics_flag_review": "ethics_first",
        "03_official_public_domain_fast_track": "primary_image_review",
        "04_open_public_domain_review": "primary_image_review",
        "05_open_license_attribution": "primary_image_review",
        "06_partner_grant_or_new_candidate": "partner_or_replacement",
    }[batch]


def missing_checks(approval_record):
    checks = (approval_record or {}).get("checks") or {}
    return [key for key in CHECK_ORDER if checks.get(key) is not True]


def promotion_allowed(approval_record):
    if not approval_record or approval_record.get("decision") != "approve_primary":
        return False
    if missing_checks(approval_record):
        return False
    if not approval_record.get("reviewer") or not approval_record.get("reviewed_on"):
        return False
    template = approval_record.get("approved_primary_template") or {}
    required = [
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
    return all(template.get(key) for key in required)


def blockers(record, approval_record):
    candidate = record.get("candidate") or {}
    source_route = record.get("source_route") or {}
    render_contract = record.get("render_contract") or {}
    render_strategy = render_contract.get("render_strategy")
    result = []

    if (record.get("primary_status") or "") != "approved":
        result.append("no approved primary image")
    if (record.get("curation") or {}).get("decision") != "approve_primary":
        result.append("curator decision pending")
    missing = missing_checks(approval_record)
    if missing:
        result.append(f"{len(missing)} approval checks incomplete")
    if candidate.get("flags"):
        result.append("candidate has automated review flags: " + ", ".join(candidate.get("flags")))
    if source_route.get("route") == "official_public_domain_fast_track":
        result.append("confirm official/institutional creator is not a third-party credit")
    if source_route.get("route") == "open_license_attribution_review":
        result.append("capture exact attribution and share-alike obligations")
    if render_strategy == "source_card_recheck_placeholder":
        result.append("source-card fallback needs browser recheck")
    if not candidate.get("asset_id"):
        result.append("no candidate asset id")
    return result


def next_action(batch, record):
    if batch == "01_source_card_recheck":
        card = ((record.get("public_fallback") or {}).get("source_card") or {})
        return f"Open source-card URL in browser and re-run link verification: {card.get('source_url')}"
    if batch == "02_ethics_flag_review":
        return "Inspect candidate depiction first; reject/replace if proximity or welfare context is unsafe."
    if batch == "03_official_public_domain_fast_track":
        return "Review official/public-domain candidate fields, write alt/crop/species-match notes, then set approval queue checks."
    if batch == "04_open_public_domain_review":
        return "Confirm original source and public-domain/CC0 rights before filling approval queue checks."
    if batch == "05_open_license_attribution":
        return "Capture exact attribution/license obligations before any public-use approval."
    return "Use source-card fallback while requesting written grant or finding a replacement candidate."


def workspace_record(record, approval_record):
    batch = recommended_batch(record)
    render_contract = record.get("render_contract") or {}
    source_card = ((record.get("public_fallback") or {}).get("source_card") or {})
    candidate = record.get("candidate") or {}
    source_route = record.get("source_route") or {}
    missing = missing_checks(approval_record)
    return {
        "artifact_id": record.get("artifact_id"),
        "species_page": record.get("species_page"),
        "website_path": record.get("website_path"),
        "common_name": record.get("common_name"),
        "scientific_name": record.get("scientific_name"),
        "taxon_group": record.get("taxon_group"),
        "recommended_batch": batch,
        "batch_label": BATCH_LABELS[batch],
        "workstream": workstream_for(batch),
        "priority": source_route.get("priority") or "none",
        "source_route": source_route.get("route") or "none",
        "render_strategy": render_contract.get("render_strategy") or "none",
        "public_visual": {
            "kind": (render_contract.get("public_visual") or {}).get("kind"),
            "public_use": (render_contract.get("public_visual") or {}).get("public_use") is True,
            "source_url": (render_contract.get("public_visual") or {}).get("source_url"),
            "hero_image_allowed": ((render_contract.get("surface_rules") or {}).get("species_page_hero_image_allowed"))
            is True,
        },
        "source_card_fallback": {
            "status": source_card.get("status"),
            "public_use": source_card.get("public_use") is True,
            "source_url": source_card.get("source_url"),
            "domain": source_card.get("domain"),
        },
        "candidate": {
            "asset_id": candidate.get("asset_id"),
            "title": candidate.get("title"),
            "commons_file_page": candidate.get("commons_file_page"),
            "image_url": candidate.get("image_url"),
            "creator": candidate.get("creator"),
            "credit": candidate.get("credit"),
            "license": candidate.get("license"),
            "license_url": candidate.get("license_url"),
            "rights_status": candidate.get("rights_status"),
            "flags": candidate.get("flags") or [],
            "public_use": False,
        },
        "approval_state": {
            "decision": (approval_record or {}).get("decision"),
            "reviewer": (approval_record or {}).get("reviewer"),
            "reviewed_on": (approval_record or {}).get("reviewed_on"),
            "checks_complete": len(CHECK_ORDER) - len(missing),
            "checks_total": len(CHECK_ORDER),
            "missing_checks": missing,
            "promotion_allowed_now": promotion_allowed(approval_record),
        },
        "blockers": blockers(record, approval_record),
        "next_curator_action": next_action(batch, record),
        "commands_after_approval_queue_edit": [
            f"python scripts/promote_species_media.py --artifact-id {record.get('artifact_id')}",
            f"python scripts/promote_species_media.py --artifact-id {record.get('artifact_id')} --apply",
            "python scripts/validate_species_media.py",
            "python scripts/export_species_media_site_data.py",
            "python scripts/build_species_media_render_contract.py",
            "python scripts/export_species_media_site_data.py",
            "python scripts/build_species_media_visual_board.py",
        ],
    }


def build_workspace():
    site_data = load_json(SITE_DATA_PATH)
    approval_queue = by_artifact(load_yaml(APPROVAL_QUEUE_PATH))
    records = [
        workspace_record(record, approval_queue.get(record.get("artifact_id")))
        for record in site_data.get("records") or []
    ]
    batch_counts = Counter(record["recommended_batch"] for record in records)
    workstream_counts = Counter(record["workstream"] for record in records)
    route_counts = Counter(record["source_route"] for record in records)
    promotion_ready = [record["artifact_id"] for record in records if record["approval_state"]["promotion_allowed_now"]]
    public_fallback_blocked = [
        record["artifact_id"]
        for record in records
        if record["recommended_batch"] == "01_source_card_recheck"
    ]
    flagged = [record["artifact_id"] for record in records if record["candidate"]["flags"]]
    partner_refs = defaultdict(list)
    for record in site_data.get("records") or []:
        for ref in (record.get("source_route") or {}).get("partner_refs") or []:
            partner_refs[ref].append(record.get("artifact_id"))

    return {
        "version": date.today().isoformat(),
        "generated_at": date.today().isoformat(),
        "sources": {
            "site_data": rel(SITE_DATA_PATH),
            "approval_queue": rel(APPROVAL_QUEUE_PATH),
        },
        "policy": {
            "workspace_is_not_approval": True,
            "candidate_public_use": False,
            "promotion_requires_approval_queue_checks": True,
            "do_not_bypass_ethics_or_rights_review": True,
        },
        "batch_actions": BATCH_ACTIONS,
        "summary": {
            "species_records": len(records),
            "batch_counts": dict(sorted(batch_counts.items())),
            "workstream_counts": dict(sorted(workstream_counts.items())),
            "source_route_counts": dict(sorted(route_counts.items())),
            "promotion_ready_count": len(promotion_ready),
            "promotion_ready_artifact_ids": promotion_ready,
            "public_fallback_blocked_artifact_ids": public_fallback_blocked,
            "flagged_candidate_artifact_ids": flagged,
            "partner_ref_counts": {key: len(value) for key, value in sorted(partner_refs.items())},
        },
        "records": records,
    }


def md_link(label, url):
    return f"[{label}]({url})" if url else "-"


def render_markdown(payload):
    summary = payload["summary"]
    lines = [
        "# Species Media Curation Workspace",
        "",
        f"Generated: {payload['generated_at']}",
        "",
        "This workspace is the operating view for turning review-only candidates into approved primary species media. It is not an approval record; the approval queue remains the source of truth for curator decisions and checks.",
        "",
        "## Summary",
        "",
        f"- Species records: {summary['species_records']}",
        f"- Promotion-ready now: {summary['promotion_ready_count']}",
        "- Batches: " + ", ".join(f"{key}={value}" for key, value in summary["batch_counts"].items()),
        "- Workstreams: " + ", ".join(f"{key}={value}" for key, value in summary["workstream_counts"].items()),
        f"- Source-card browser rechecks: {len(summary['public_fallback_blocked_artifact_ids'])}",
        f"- Flagged candidates: {len(summary['flagged_candidate_artifact_ids'])}",
        "",
        "## Batch Actions",
        "",
        "| Batch | Count | Label | First action |",
        "|---|---:|---|---|",
    ]
    for batch, label in BATCH_LABELS.items():
        count = summary["batch_counts"].get(batch, 0)
        first_action = (payload["batch_actions"].get(batch) or ["-"])[0]
        lines.append(f"| `{batch}` | {count} | {label} | {first_action} |")

    lines.extend(
        [
            "",
            "## Curator Worklist",
            "",
            "| Batch | Species | Route | Render | Candidate rights | Source / file | Checks | Blockers |",
            "|---|---|---|---|---|---|---|---|",
        ]
    )
    for record in payload["records"]:
        candidate = record["candidate"]
        source = candidate.get("commons_file_page") or candidate.get("image_url")
        checks = f"{record['approval_state']['checks_complete']}/{record['approval_state']['checks_total']}"
        blockers_text = "<br>".join(record["blockers"]) if record["blockers"] else "-"
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{record['recommended_batch']}`",
                    record["common_name"],
                    f"`{record['source_route']}`",
                    f"`{record['render_strategy']}`",
                    f"`{candidate.get('rights_status') or '-'}`",
                    md_link("file", source),
                    checks,
                    blockers_text,
                ]
            )
            + " |"
        )

    lines.extend(["", "## Per-Species Next Actions", ""])
    for record in payload["records"]:
        candidate = record["candidate"]
        fallback = record["source_card_fallback"]
        lines.extend(
            [
                f"### {record['common_name']}",
                "",
                f"- Batch: `{record['recommended_batch']}` ({record['batch_label']})",
                f"- Candidate: {candidate.get('title') or '-'}",
                f"- Candidate file: {md_link('Commons/file page', candidate.get('commons_file_page'))}",
                f"- Public fallback: `{fallback.get('status')}` {md_link('source card', fallback.get('source_url'))}",
                f"- Checks: {record['approval_state']['checks_complete']}/{record['approval_state']['checks_total']}",
                f"- Promotion allowed now: `{str(record['approval_state']['promotion_allowed_now']).lower()}`",
                f"- Next action: {record['next_curator_action']}",
                "",
            ]
        )

    lines.extend(
        [
            "## Promotion Commands",
            "",
            "After a curator edits `content/media/species-media-approval-queue.yaml` with `decision: approve_primary`, reviewer/date, all checks true, and complete approved-primary metadata, run:",
            "",
            "```bash",
            "python scripts/promote_species_media.py --artifact-id <artifact_id>",
            "python scripts/promote_species_media.py --artifact-id <artifact_id> --apply",
            "python scripts/validate_species_media.py",
            "python scripts/export_species_media_site_data.py",
            "python scripts/build_species_media_render_contract.py",
            "python scripts/export_species_media_site_data.py",
            "python scripts/build_species_media_visual_board.py",
            "```",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


def main():
    payload = build_workspace()
    WORKSPACE_PATH.write_text(
        yaml.safe_dump(payload, sort_keys=False, allow_unicode=False), encoding="utf-8"
    )
    REVIEW_DIR.mkdir(parents=True, exist_ok=True)
    markdown_path = REVIEW_DIR / f"species-media-curation-workspace-{date.today().isoformat()}.md"
    markdown_path.write_text(render_markdown(payload), encoding="utf-8")
    print(f"Wrote {rel(WORKSPACE_PATH)}")
    print(f"Wrote {rel(markdown_path)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
