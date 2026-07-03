#!/usr/bin/env python3
"""Build reviewer-only approval dossiers for species media candidates.

The approval queue stores the source of truth for curator decisions. These
dossiers are the working packet around that queue: the candidate evidence,
missing proof, acquisition lane, public fallback, trace pointers, and promotion
commands for each animal.

This artifact is intentionally reviewer-only because it includes candidate file
pages and direct image URLs. Public pages must continue to use the sanitized
public explorer manifest.

Usage:
  python scripts/build_species_media_approval_dossiers.py
"""
from __future__ import annotations

from collections import Counter
from datetime import date
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
REGISTRY_PATH = ROOT / "content" / "media" / "species-media-registry.yaml"
APPROVAL_QUEUE_PATH = ROOT / "content" / "media" / "species-media-approval-queue.yaml"
CURATION_WORKSPACE_PATH = ROOT / "content" / "media" / "species-media-curation-workspace.yaml"
ACQUISITION_PLAN_PATH = ROOT / "content" / "media" / "species-media-acquisition-plan.yaml"
PUBLIC_EXPLORER_PATH = ROOT / "content" / "media" / "species-media-public-explorer-manifest.yaml"
TRACE_LEDGER_PATH = ROOT / "content" / "media" / "species-media-trace-ledger.yaml"
APPROVAL_DOSSIERS_PATH = ROOT / "content" / "media" / "species-media-approval-dossiers.yaml"
REVIEW_PACK_PATH = (
    ROOT
    / "content"
    / "media"
    / "review-packs"
    / f"species-media-approval-dossiers-{date.today().isoformat()}.md"
)

APPROVAL_CHECKS = [
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

CHECK_EVIDENCE = {
    "image_level_rights_verified": "Capture the image-level license or written permission from the candidate source, not just the hosting page.",
    "creator_and_credit_verified": "Copy the exact creator, institution, and credit line required by the source.",
    "commercial_and_derivative_use_checked": "Record commercial, derivative, attribution, and share-alike compatibility for every intended surface.",
    "species_match_verified": "Ground the species match in the source caption, taxon page, partner assertion, or expert review note.",
    "ethics_checked": "Check the depiction for unsafe proximity, handling, baiting, crowding, captivity glamour, distress, or misleading context.",
    "sensitive_location_checked": "Confirm caption, crop, EXIF-derived text, and surrounding context do not expose precise sensitive locations.",
    "crop_checked": "Inspect desktop hero, mobile crop, and card crop for legibility and non-misleading context.",
    "alt_text_written": "Write plain alt text for the visible content without unsupported behavior or conservation claims.",
    "approved_surfaces_set": "Keep approved and blocked surfaces explicit before promotion.",
}


def load_yaml(path: Path):
    if not path.exists():
        return {}
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def rel(path: Path):
    return path.relative_to(ROOT).as_posix()


def by_id(payload):
    return {record.get("artifact_id"): record for record in payload.get("records") or []}


def checked_count(checks):
    return sum(1 for key in APPROVAL_CHECKS if checks.get(key) is True)


def promotion_allowed(approval_record):
    if not approval_record or approval_record.get("decision") != "approve_primary":
        return False
    checks = approval_record.get("checks") or {}
    if any(checks.get(key) is not True for key in APPROVAL_CHECKS):
        return False
    if not approval_record.get("reviewer") or not approval_record.get("reviewed_on"):
        return False
    approved = approval_record.get("approved_primary_template") or {}
    return all(approved.get(key) for key in REQUIRED_APPROVED_FIELDS)


def dossier_status(approval_record, acquisition_record):
    if promotion_allowed(approval_record):
        return "promotion_ready"
    lane = acquisition_record.get("acquisition_lane")
    if lane == "ethics_first_candidate_review":
        return "ethics_first_review"
    if lane == "official_public_domain_review":
        return "official_rights_review"
    if lane == "open_public_domain_review":
        return "open_public_domain_review"
    if lane == "open_license_attribution_review":
        return "open_license_attribution_review"
    if lane == "partner_or_ngo_media_grant":
        return "partner_or_replacement_needed"
    return "approval_queue_review"


def review_sequence(status):
    base = ["Open the candidate file page and current public source card side by side."]
    if status == "ethics_first_review":
        base.extend(
            [
                "Inspect welfare, proximity, captivity, and sensitive-location context before rights work.",
                "Reject or replace the candidate if the depiction is ethically unsuitable.",
            ]
        )
    elif status == "official_rights_review":
        base.extend(
            [
                "Confirm the candidate creator or credit is official/institutional at image level.",
                "Confirm the public-domain or CC0 basis and exact required credit text.",
            ]
        )
    elif status == "open_public_domain_review":
        base.extend(
            [
                "Confirm original source confidence and public-domain or CC0 status at image level.",
                "Replace the candidate if provenance confidence is weak.",
            ]
        )
    elif status == "open_license_attribution_review":
        base.extend(
            [
                "Capture exact creator, credit, license URL, modification rules, and share-alike obligations.",
                "Block paid ads, merchandise, and social crops unless the reviewer explicitly approves those surfaces.",
            ]
        )
    elif status == "partner_or_replacement_needed":
        base.extend(
            [
                "Send a written media-grant or replacement-source ask before attempting promotion.",
                "Use the verified source card publicly until permission or a stronger candidate exists.",
            ]
        )
    base.extend(
        [
            "Fill every missing approval queue check and approved-primary field.",
            "Run the dry-run promotion command before applying registry changes.",
        ]
    )
    return base


def missing_template_fields(template):
    return [key for key in REQUIRED_APPROVED_FIELDS if not template.get(key)]


def build_record(registry_record, approval_record, curation_record, acquisition_record, public_record, trace_record):
    artifact_id = registry_record.get("artifact_id")
    approval_record = approval_record or {}
    curation_record = curation_record or {}
    acquisition_record = acquisition_record or {}
    public_record = public_record or {}
    trace_record = trace_record or {}
    candidate = approval_record.get("candidate") or {}
    template = approval_record.get("approved_primary_template") or {}
    checks = approval_record.get("checks") or {}
    status = dossier_status(approval_record, acquisition_record)
    missing_checks = [key for key in APPROVAL_CHECKS if checks.get(key) is not True]
    missing_fields = missing_template_fields(template)
    acquisition_strategy = acquisition_record.get("source_strategy") or {}
    public_visual = public_record.get("public_visual") or {}
    source_card = approval_record.get("source_card_fallback") or {}
    flags = candidate.get("flags") or []

    return {
        "artifact_id": artifact_id,
        "ownership_key": f"{artifact_id}|{registry_record.get('species_page')}",
        "species_page": registry_record.get("species_page"),
        "website_path": registry_record.get("website_path") or public_record.get("website_path"),
        "common_name": registry_record.get("common_name"),
        "scientific_name": registry_record.get("scientific_name"),
        "taxon_group": registry_record.get("taxon_group"),
        "priority": approval_record.get("priority") or acquisition_record.get("priority"),
        "dossier_status": status,
        "decision": approval_record.get("decision"),
        "reviewer": approval_record.get("reviewer"),
        "reviewed_on": approval_record.get("reviewed_on"),
        "approval_gap": {
            "checks_complete": checked_count(checks),
            "checks_total": len(APPROVAL_CHECKS),
            "missing_checks": missing_checks,
            "missing_approved_primary_fields": missing_fields,
            "promotion_allowed_now": promotion_allowed(approval_record),
        },
        "candidate_evidence": {
            "asset_id": candidate.get("asset_id"),
            "provider": candidate.get("provider"),
            "title": candidate.get("title"),
            "commons_file_page": candidate.get("commons_file_page"),
            "image_url": candidate.get("image_url"),
            "creator": candidate.get("creator"),
            "credit": candidate.get("credit"),
            "license": candidate.get("license"),
            "license_url": candidate.get("license_url"),
            "rights_status": candidate.get("rights_status"),
            "flags": flags,
            "score": candidate.get("score"),
            "public_use": False,
            "reviewer_only": True,
        },
        "current_public_fallback": {
            "status": source_card.get("status"),
            "public_use": source_card.get("public_use") is True,
            "source_url": source_card.get("source_url") or public_visual.get("source_url"),
            "domain": source_card.get("domain") or public_visual.get("domain"),
            "render_strategy": public_visual.get("render_strategy"),
            "source_card_does_not_authorize_image_copy": True,
        },
        "acquisition": {
            "lane": acquisition_record.get("acquisition_lane"),
            "label": acquisition_record.get("acquisition_label"),
            "target_source_family": acquisition_strategy.get("target_source_family"),
            "target_source_family_label": acquisition_strategy.get("target_source_family_label"),
            "partner_media_grant_needed": acquisition_strategy.get("partner_media_grant_needed") is True,
            "outreach_targets": acquisition_strategy.get("outreach_targets") or [],
        },
        "curation": {
            "recommended_batch": curation_record.get("recommended_batch"),
            "batch_label": curation_record.get("batch_label"),
            "workstream": curation_record.get("workstream"),
            "blockers": curation_record.get("blockers") or [],
            "next_curator_action": curation_record.get("next_curator_action"),
        },
        "required_evidence": [
            {"check": key, "needed": CHECK_EVIDENCE[key]} for key in missing_checks
        ],
        "approved_primary_template": {
            "approved_asset_id": template.get("approved_asset_id"),
            "source_url": template.get("source_url"),
            "original_media_url": template.get("original_media_url"),
            "creator": template.get("creator"),
            "credit": template.get("credit"),
            "license": template.get("license"),
            "license_url": template.get("license_url"),
            "rights_status": template.get("rights_status"),
            "approved_surfaces": template.get("approved_surfaces") or [],
            "blocked_surfaces": template.get("blocked_surfaces") or [],
        },
        "safety_controls": {
            "candidate_public_use": False,
            "candidate_links_reviewer_only": True,
            "source_card_no_copy_or_crop": True,
            "approved_primary_required_for_hero_image": True,
            "ethics_first": bool(flags) or status == "ethics_first_review",
            "trace_record_present": bool(trace_record),
        },
        "handoff": {
            "approval_queue_record": f"{rel(APPROVAL_QUEUE_PATH)}#{artifact_id}",
            "curation_workspace_record": f"{rel(CURATION_WORKSPACE_PATH)}#{artifact_id}",
            "acquisition_plan_record": f"{rel(ACQUISITION_PLAN_PATH)}#{artifact_id}",
            "public_explorer_record": f"{rel(PUBLIC_EXPLORER_PATH)}#{artifact_id}",
            "trace_ledger_record": f"{rel(TRACE_LEDGER_PATH)}#{artifact_id}",
            "dry_run_command": f"python scripts/promote_species_media.py --artifact-id {artifact_id}",
            "apply_command_after_clean_dry_run": f"python scripts/promote_species_media.py --artifact-id {artifact_id} --apply",
        },
        "review_sequence": review_sequence(status),
    }


def build_dossiers():
    registry = load_yaml(REGISTRY_PATH)
    approval = load_yaml(APPROVAL_QUEUE_PATH)
    curation = load_yaml(CURATION_WORKSPACE_PATH)
    acquisition = load_yaml(ACQUISITION_PLAN_PATH)
    public = load_yaml(PUBLIC_EXPLORER_PATH)
    trace = load_yaml(TRACE_LEDGER_PATH)

    approval_by_id = by_id(approval)
    curation_by_id = by_id(curation)
    acquisition_by_id = by_id(acquisition)
    public_by_id = by_id(public)
    trace_by_id = by_id(trace)

    records = [
        build_record(
            registry_record,
            approval_by_id.get(registry_record.get("artifact_id")),
            curation_by_id.get(registry_record.get("artifact_id")),
            acquisition_by_id.get(registry_record.get("artifact_id")),
            public_by_id.get(registry_record.get("artifact_id")),
            trace_by_id.get(registry_record.get("artifact_id")),
        )
        for registry_record in registry.get("records") or []
    ]

    statuses = Counter(record.get("dossier_status") or "none" for record in records)
    lanes = Counter((record.get("acquisition") or {}).get("lane") or "none" for record in records)
    priorities = Counter(record.get("priority") or "none" for record in records)
    missing_checks = Counter(
        check
        for record in records
        for check in ((record.get("approval_gap") or {}).get("missing_checks") or [])
    )
    missing_fields = Counter(
        field
        for record in records
        for field in ((record.get("approval_gap") or {}).get("missing_approved_primary_fields") or [])
    )
    flagged = [
        record["artifact_id"]
        for record in records
        if (record.get("candidate_evidence") or {}).get("flags")
    ]
    promotion_ready = [
        record["artifact_id"]
        for record in records
        if (record.get("approval_gap") or {}).get("promotion_allowed_now") is True
    ]

    return {
        "version": date.today().isoformat(),
        "generated_at": date.today().isoformat(),
        "sources": {
            "registry": rel(REGISTRY_PATH),
            "approval_queue": rel(APPROVAL_QUEUE_PATH),
            "curation_workspace": rel(CURATION_WORKSPACE_PATH),
            "acquisition_plan": rel(ACQUISITION_PLAN_PATH),
            "public_explorer": rel(PUBLIC_EXPLORER_PATH),
            "trace_ledger": rel(TRACE_LEDGER_PATH),
        },
        "policy": {
            "reviewer_only": True,
            "contains_review_candidate_urls": True,
            "not_public_site_input": True,
            "candidate_public_use": False,
            "source_card_does_not_authorize_image_copy": True,
            "promotion_requires_approval_queue": True,
            "dry_run_before_apply": True,
        },
        "summary": {
            "species_records": len(records),
            "promotion_ready_count": len(promotion_ready),
            "promotion_ready_artifact_ids": promotion_ready,
            "flagged_candidate_records": flagged,
            "dossier_status_counts": dict(sorted(statuses.items())),
            "acquisition_lane_counts": dict(sorted(lanes.items())),
            "priority_counts": dict(sorted(priorities.items())),
            "missing_check_counts": dict(sorted(missing_checks.items())),
            "missing_approved_primary_field_counts": dict(sorted(missing_fields.items())),
        },
        "records": records,
    }


def markdown(payload):
    summary = payload.get("summary") or {}
    lines = [
        "# Species Media Approval Dossiers",
        "",
        f"Generated: {payload.get('generated_at')}",
        "",
        "Reviewer-only packet for turning staged species media candidates into approved primary images. This file may include candidate file pages and direct image URLs; do not use it as a public website data source.",
        "",
        "## Summary",
        "",
        f"- Species records: {summary.get('species_records')}",
        f"- Promotion-ready records: {summary.get('promotion_ready_count')}",
        f"- Flagged candidates: {len(summary.get('flagged_candidate_records') or [])}",
        "",
        "## Dossier Status Counts",
        "",
    ]
    for status, count in (summary.get("dossier_status_counts") or {}).items():
        lines.append(f"- `{status}`: {count}")
    lines.extend(["", "## Missing Evidence Counts", ""])
    for check, count in (summary.get("missing_check_counts") or {}).items():
        lines.append(f"- `{check}`: {count}")
    lines.extend(
        [
            "",
            "## Approval Board",
            "",
            "| Species | Status | Candidate | Missing proof | Promotion |",
            "|---|---|---|---|---|",
        ]
    )
    for record in payload.get("records") or []:
        candidate = record.get("candidate_evidence") or {}
        gap = record.get("approval_gap") or {}
        candidate_link = candidate.get("commons_file_page")
        candidate_label = candidate.get("title") or candidate.get("asset_id") or "-"
        candidate_cell = f"[{candidate_label}]({candidate_link})" if candidate_link else candidate_label
        missing = f"{len(gap.get('missing_checks') or [])} checks, {len(gap.get('missing_approved_primary_fields') or [])} fields"
        promotion = "`ready`" if gap.get("promotion_allowed_now") else "`blocked`"
        lines.append(
            "| "
            + " | ".join(
                [
                    f"{record.get('common_name')}<br>`{record.get('artifact_id')}`",
                    f"`{record.get('dossier_status')}`<br>{record.get('acquisition', {}).get('label') or '-'}",
                    candidate_cell,
                    missing,
                    promotion,
                ]
            )
            + " |"
        )
    lines.extend(["", "## Per-Species Dossiers", ""])
    for record in payload.get("records") or []:
        candidate = record.get("candidate_evidence") or {}
        fallback = record.get("current_public_fallback") or {}
        gap = record.get("approval_gap") or {}
        curation = record.get("curation") or {}
        handoff = record.get("handoff") or {}
        lines.extend(
            [
                f"### {record.get('common_name')} (*{record.get('scientific_name')}*)",
                "",
                f"- Artifact: `{record.get('artifact_id')}`",
                f"- Species page: `{record.get('species_page')}`",
                f"- Dossier status: `{record.get('dossier_status')}`",
                f"- Acquisition lane: `{record.get('acquisition', {}).get('lane')}`",
                f"- Curation batch: `{curation.get('recommended_batch')}`",
                f"- Candidate file: {candidate.get('commons_file_page') or '-'}",
                f"- Candidate image: {candidate.get('image_url') or '-'}",
                f"- Candidate rights: `{candidate.get('rights_status') or 'none'}`",
                f"- Candidate flags: {', '.join(candidate.get('flags') or []) or '-'}",
                f"- Public fallback: `{fallback.get('status') or 'none'}` ({fallback.get('source_url') or '-'})",
                f"- Missing checks: {len(gap.get('missing_checks') or [])}/{gap.get('checks_total')}",
                f"- Missing approved-primary fields: {', '.join(gap.get('missing_approved_primary_fields') or []) or '-'}",
                "",
                "Review sequence:",
            ]
        )
        for action in record.get("review_sequence") or []:
            lines.append(f"- {action}")
        lines.extend(
            [
                "",
                "Promotion commands:",
                f"- Dry run: `{handoff.get('dry_run_command')}`",
                f"- Apply after clean dry run: `{handoff.get('apply_command_after_clean_dry_run')}`",
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def main():
    payload = build_dossiers()
    APPROVAL_DOSSIERS_PATH.parent.mkdir(parents=True, exist_ok=True)
    REVIEW_PACK_PATH.parent.mkdir(parents=True, exist_ok=True)
    APPROVAL_DOSSIERS_PATH.write_text(
        yaml.safe_dump(payload, sort_keys=False, allow_unicode=False, width=120),
        encoding="utf-8",
    )
    REVIEW_PACK_PATH.write_text(markdown(payload), encoding="utf-8")
    print(f"Wrote {rel(APPROVAL_DOSSIERS_PATH)}")
    print(f"Wrote {rel(REVIEW_PACK_PATH)}")
    print(
        "Species media approval dossiers: "
        f"{payload['summary']['species_records']} records, "
        f"{payload['summary']['promotion_ready_count']} promotion-ready."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
