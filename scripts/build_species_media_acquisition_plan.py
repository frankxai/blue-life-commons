#!/usr/bin/env python3
"""Build a public-safe acquisition plan for species primary media.

The acquisition plan answers the operational question after source-card
fallbacks are in place: what does each species need next to get an approved
primary image?

It intentionally omits review-only candidate URLs and Commons file pages. Use
the curation workspace and approval queue for restricted reviewer links.

Usage:
  python scripts/build_species_media_acquisition_plan.py
"""
from __future__ import annotations

from collections import Counter
from datetime import date
from pathlib import Path
from urllib.parse import urlparse

import yaml

ROOT = Path(__file__).resolve().parent.parent
REGISTRY_PATH = ROOT / "content" / "media" / "species-media-registry.yaml"
SOURCE_ROUTING_PATH = ROOT / "content" / "media" / "species-media-source-routing.yaml"
RICH_EMBEDS_PATH = ROOT / "content" / "media" / "species-media-rich-embeds.yaml"
APPROVAL_QUEUE_PATH = ROOT / "content" / "media" / "species-media-approval-queue.yaml"
RENDER_CONTRACT_PATH = ROOT / "content" / "media" / "species-media-render-contract.yaml"
CURATION_WORKSPACE_PATH = ROOT / "content" / "media" / "species-media-curation-workspace.yaml"
TRACE_LEDGER_PATH = ROOT / "content" / "media" / "species-media-trace-ledger.yaml"
ACQUISITION_PLAN_PATH = ROOT / "content" / "media" / "species-media-acquisition-plan.yaml"
REVIEW_PACK_PATH = (
    ROOT
    / "content"
    / "media"
    / "review-packs"
    / f"species-media-acquisition-plan-{date.today().isoformat()}.md"
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

LANE_LABELS = {
    "primary_approved_maintenance": "Primary approved; maintain rights and attribution",
    "promotion_apply_ready": "Curator approved; run promotion tool",
    "ethics_first_candidate_review": "Ethics-first candidate review",
    "official_public_domain_review": "Official/public-domain image-level review",
    "open_public_domain_review": "Open public-domain image-level review",
    "open_license_attribution_review": "Open-license attribution review",
    "partner_or_ngo_media_grant": "Partner/NGO media grant or replacement",
}

SOURCE_FAMILY_LABELS = {
    "official_institutional": "Official or institutional",
    "partner_or_ngo": "Partner or NGO",
    "open_license_candidate": "Open-license candidate",
    "authority_source": "Authority source card",
    "institutional": "Institutional source card",
}


def load_yaml(path: Path):
    if not path.exists():
        return {}
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def rel(path: Path):
    return path.relative_to(ROOT).as_posix()


def by_id(payload):
    return {record.get("artifact_id"): record for record in payload.get("records") or []}


def host(url):
    if not url:
        return None
    return urlparse(url).netloc.lower().removeprefix("www.")


def checked_count(checks):
    return sum(1 for key in APPROVAL_CHECKS if checks.get(key) is True)


def is_promotable(approval_record):
    if not approval_record or approval_record.get("decision") != "approve_primary":
        return False
    checks = approval_record.get("checks") or {}
    if any(checks.get(key) is not True for key in APPROVAL_CHECKS):
        return False
    if not approval_record.get("reviewer") or not approval_record.get("reviewed_on"):
        return False
    approved = approval_record.get("approved_primary_template") or {}
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
    return all(approved.get(key) for key in required)


def source_refs(registry_record):
    refs = registry_record.get("source_candidates") or {}
    return {
        "official_or_institutional": refs.get("official_or_institutional_refs") or [],
        "open_license": refs.get("open_license_refs") or [],
        "partner": refs.get("partner_refs") or [],
    }


def target_source_family(route, source_type):
    if route == "official_public_domain_fast_track":
        return "official_institutional"
    if route == "open_license_attribution_review":
        return "open_license_candidate"
    if route == "open_public_domain_review":
        return "open_license_candidate"
    if route and route.startswith("ethics"):
        return "official_institutional"
    if source_type in SOURCE_FAMILY_LABELS:
        return source_type
    return "partner_or_ngo"


def acquisition_lane(registry_record, routing_record, approval_record, workspace_record, render_record):
    primary = registry_record.get("primary") or {}
    surface_rules = (render_record.get("surface_rules") or {}) if render_record else {}
    route = routing_record.get("route") if routing_record else None
    workspace_batch = workspace_record.get("recommended_batch") if workspace_record else None
    flags = ((workspace_record.get("candidate") or {}).get("flags") or []) if workspace_record else []

    if primary.get("status") == "approved" or surface_rules.get("species_page_hero_image_allowed") is True:
        return "primary_approved_maintenance"
    if is_promotable(approval_record):
        return "promotion_apply_ready"
    if flags or route in {"ethics_note_review", "ethics_replacement_or_manual_review"}:
        return "ethics_first_candidate_review"
    if route == "official_public_domain_fast_track" or workspace_batch == "03_official_public_domain_fast_track":
        return "official_public_domain_review"
    if route == "open_public_domain_review" or workspace_batch == "04_open_public_domain_review":
        return "open_public_domain_review"
    if route == "open_license_attribution_review" or workspace_batch == "05_open_license_attribution":
        return "open_license_attribution_review"
    return "partner_or_ngo_media_grant"


def next_actions(lane, record):
    source_domain = (record.get("current_visual") or {}).get("public_source_domain") or "the source publisher"
    partner_targets = (record.get("source_strategy") or {}).get("outreach_targets") or []
    target_text = ", ".join(partner_targets) if partner_targets else source_domain
    actions = ["Keep rendering the verified source card publicly until a primary image is approved."]

    if lane == "primary_approved_maintenance":
        actions.extend(
            [
                "Recheck attribution, license, crop, and alt text during scheduled content reviews.",
                "Keep blocked surfaces current if license terms or partner terms change.",
            ]
        )
    elif lane == "promotion_apply_ready":
        actions.extend(
            [
                f"Run python scripts/promote_species_media.py --artifact-id {record['artifact_id']}",
                f"Run python scripts/promote_species_media.py --artifact-id {record['artifact_id']} --apply after the dry run is clean.",
            ]
        )
    elif lane == "ethics_first_candidate_review":
        actions.extend(
            [
                "Open the curation workspace review record and inspect the candidate depiction before rights work.",
                "Reject or replace the candidate if it implies unsafe proximity, handling, captivity glamour, distress, or sensitive-location exposure.",
                "If acceptable, finish the full approval queue checklist with reviewer and date.",
            ]
        )
    elif lane == "official_public_domain_review":
        actions.extend(
            [
                "Confirm the image-level source says the creator is official or institutional, not a third-party credit.",
                "Confirm public-domain or CC0-style rights at image level and capture exact credit text.",
                "Write species-match basis, alt text, crop guidance, ethics notes, approved surfaces, and blocked surfaces in the approval queue.",
            ]
        )
    elif lane == "open_public_domain_review":
        actions.extend(
            [
                "Confirm original source, public-domain or CC0 status, and species caption before approval.",
                "Replace the candidate if original source confidence is weak or the depiction is ethically unsuitable.",
                "Complete crop, alt text, species-match, credit, and surface metadata before promotion.",
            ]
        )
    elif lane == "open_license_attribution_review":
        actions.extend(
            [
                "Capture exact creator, credit, license URL, modification rules, and share-alike obligations.",
                "Confirm commercial, derivative, educational, social, and grant-report surface compatibility.",
                "Block paid ads, merchandise, and social crops unless the license and reviewer explicitly allow them.",
            ]
        )
    else:
        actions.extend(
            [
                f"Send a written media grant or replacement-source ask to {target_text}.",
                "Request image-level license terms, required credit, allowed surfaces, embargoes, revocation terms, and welfare/location constraints.",
                "Use the source card only if permission is not granted.",
            ]
        )

    if lane != "partner_or_ngo_media_grant" and partner_targets:
        actions.append(f"Run partner outreach in parallel for stronger or owned media from {target_text}.")
    return actions


def build_record(registry_record, routing_record, rich_record, approval_record, render_record, workspace_record, trace_record):
    artifact_id = registry_record.get("artifact_id")
    routing_record = routing_record or {}
    rich_record = rich_record or {}
    approval_record = approval_record or {}
    render_record = render_record or {}
    workspace_record = workspace_record or {}
    trace_record = trace_record or {}

    public_visual = render_record.get("public_visual") or {}
    surface_rules = render_record.get("surface_rules") or {}
    source_card = rich_record.get("source_card") or {}
    candidate = ((registry_record.get("primary") or {}).get("candidate") or {})
    workspace_candidate = workspace_record.get("candidate") or {}
    checks = approval_record.get("checks") or {}
    route = routing_record.get("route")
    source_type = public_visual.get("source_type") or source_card.get("source_type")
    lane = acquisition_lane(registry_record, routing_record, approval_record, workspace_record, render_record)
    source_family = target_source_family(route, source_type)
    website_path = (
        registry_record.get("website_path")
        or workspace_record.get("website_path")
        or trace_record.get("website_path")
    )
    refs = source_refs(registry_record)
    partner_refs = [
        ref for ref in refs["partner"] if ref != "partner_media_grant_needed"
    ]
    source_domain = public_visual.get("domain") or source_card.get("domain") or host(public_visual.get("source_url"))
    outreach_targets = sorted(set(partner_refs + ([source_domain] if source_domain else [])))

    record = {
        "artifact_id": artifact_id,
        "ownership_key": f"{artifact_id}|{registry_record.get('species_page')}",
        "species_page": registry_record.get("species_page"),
        "website_path": website_path,
        "common_name": registry_record.get("common_name"),
        "scientific_name": registry_record.get("scientific_name"),
        "taxon_group": registry_record.get("taxon_group"),
        "desired_outcome": "approved_primary_image",
        "asset_tier_target": "Tier A real species media",
        "acquisition_lane": lane,
        "acquisition_label": LANE_LABELS[lane],
        "priority": routing_record.get("priority") or workspace_record.get("priority") or "P2",
        "current_visual": {
            "render_strategy": render_record.get("render_strategy"),
            "public_visual_kind": public_visual.get("kind"),
            "public_use": public_visual.get("public_use") is True,
            "public_source_url": public_visual.get("source_url"),
            "public_source_domain": source_domain,
            "public_source_type": source_type,
            "hero_image_ready": surface_rules.get("species_page_hero_image_allowed") is True,
            "source_card_status": source_card.get("status"),
            "source_card_copies_external_media": source_card.get("copies_external_media") is True,
        },
        "source_strategy": {
            "target_source_family": source_family,
            "target_source_family_label": SOURCE_FAMILY_LABELS.get(source_family, source_family),
            "google_images_role": "discovery_only",
            "source_refs": refs,
            "partner_media_grant_needed": "partner_media_grant_needed" in refs["partner"],
            "outreach_targets": outreach_targets,
            "preferred_source_card_url": public_visual.get("source_url") or source_card.get("source_url"),
        },
        "candidate_snapshot": {
            "asset_id": candidate.get("asset_id") or workspace_candidate.get("asset_id"),
            "provider": candidate.get("provider") or workspace_candidate.get("provider"),
            "rights_status": candidate.get("rights_status") or workspace_candidate.get("rights_status"),
            "license": candidate.get("license") or workspace_candidate.get("license"),
            "review_status": candidate.get("review_status") or "candidate_needs_species_rights_ethics_review",
            "flags": candidate.get("flags") or workspace_candidate.get("flags") or [],
            "public_use": False,
            "direct_urls_omitted": True,
        },
        "approval_gap": {
            "decision": approval_record.get("decision"),
            "reviewer": approval_record.get("reviewer"),
            "reviewed_on": approval_record.get("reviewed_on"),
            "checks_complete": checked_count(checks),
            "checks_total": len(APPROVAL_CHECKS),
            "missing_checks": [key for key in APPROVAL_CHECKS if checks.get(key) is not True],
            "promotion_allowed_now": is_promotable(approval_record),
        },
        "safety_controls": {
            "candidate_public_use": False,
            "candidate_thumbnail_allowed": surface_rules.get("candidate_thumbnail_allowed") is True,
            "approved_primary_required_for_hero_image": True,
            "source_card_does_not_authorize_image_copy": True,
            "direct_candidate_urls_omitted": True,
            "trace_record_present": bool(trace_record),
            "trace_issues": trace_record.get("trace_issues") or [],
        },
        "handoff": {
            "approval_queue_record": f"{rel(APPROVAL_QUEUE_PATH)}#{artifact_id}",
            "curation_workspace_record": f"{rel(CURATION_WORKSPACE_PATH)}#{artifact_id}",
            "trace_ledger_record": f"{rel(TRACE_LEDGER_PATH)}#{artifact_id}",
        },
    }
    record["next_actions"] = next_actions(lane, record)
    return record


def build_plan():
    registry = load_yaml(REGISTRY_PATH)
    routing = load_yaml(SOURCE_ROUTING_PATH)
    rich = load_yaml(RICH_EMBEDS_PATH)
    approval = load_yaml(APPROVAL_QUEUE_PATH)
    render = load_yaml(RENDER_CONTRACT_PATH)
    workspace = load_yaml(CURATION_WORKSPACE_PATH)
    trace = load_yaml(TRACE_LEDGER_PATH)

    routing_by_id = by_id(routing)
    rich_by_id = by_id(rich)
    approval_by_id = by_id(approval)
    render_by_id = by_id(render)
    workspace_by_id = by_id(workspace)
    trace_by_id = by_id(trace)

    records = [
        build_record(
            registry_record,
            routing_by_id.get(registry_record.get("artifact_id")),
            rich_by_id.get(registry_record.get("artifact_id")),
            approval_by_id.get(registry_record.get("artifact_id")),
            render_by_id.get(registry_record.get("artifact_id")),
            workspace_by_id.get(registry_record.get("artifact_id")),
            trace_by_id.get(registry_record.get("artifact_id")),
        )
        for registry_record in registry.get("records") or []
    ]
    lanes = Counter(record["acquisition_lane"] for record in records)
    families = Counter((record.get("source_strategy") or {}).get("target_source_family") for record in records)
    priorities = Counter(record.get("priority") or "none" for record in records)
    source_domains = Counter(
        (record.get("current_visual") or {}).get("public_source_domain") or "none" for record in records
    )
    public_ready = sum(1 for record in records if (record.get("current_visual") or {}).get("public_use") is True)
    hero_ready = sum(1 for record in records if (record.get("current_visual") or {}).get("hero_image_ready") is True)
    candidates_blocked = sum(
        1
        for record in records
        if (record.get("safety_controls") or {}).get("candidate_public_use") is False
    )
    promotion_ready = [
        record["artifact_id"]
        for record in records
        if (record.get("approval_gap") or {}).get("promotion_allowed_now") is True
    ]
    flagged = [
        record["artifact_id"]
        for record in records
        if (record.get("candidate_snapshot") or {}).get("flags")
    ]

    return {
        "version": date.today().isoformat(),
        "generated_at": date.today().isoformat(),
        "sources": {
            "registry": rel(REGISTRY_PATH),
            "source_routing": rel(SOURCE_ROUTING_PATH),
            "rich_embeds": rel(RICH_EMBEDS_PATH),
            "approval_queue": rel(APPROVAL_QUEUE_PATH),
            "render_contract": rel(RENDER_CONTRACT_PATH),
            "curation_workspace": rel(CURATION_WORKSPACE_PATH),
            "trace_ledger": rel(TRACE_LEDGER_PATH),
        },
        "policy": {
            "acquisition_plan_is_not_approval": True,
            "public_safe": True,
            "candidate_direct_urls_omitted": True,
            "candidate_public_use": False,
            "approved_primary_required_for_hero_image": True,
            "source_card_does_not_authorize_image_copy": True,
            "google_images_discovery_only": True,
            "partner_grants_require_written_permission": True,
        },
        "summary": {
            "species_records": len(records),
            "public_visual_ready": public_ready,
            "hero_image_ready": hero_ready,
            "approved_primary_needed": len(records) - hero_ready,
            "candidate_public_use_blocked": candidates_blocked,
            "promotion_ready_count": len(promotion_ready),
            "promotion_ready_artifact_ids": promotion_ready,
            "candidate_records_with_flags": flagged,
            "acquisition_lane_counts": dict(sorted(lanes.items())),
            "target_source_family_counts": dict(sorted(families.items())),
            "priority_counts": dict(sorted(priorities.items())),
            "public_source_domain_counts": dict(sorted(source_domains.items())),
        },
        "records": records,
    }


def markdown(payload):
    summary = payload.get("summary") or {}
    lines = [
        "# Species Media Acquisition Plan",
        "",
        f"Generated: {payload.get('generated_at')}",
        "",
        "This public-safe plan says what each species needs next to move from a verified source card to an approved primary image. It omits review-only candidate URLs; use the approval queue and curation workspace for restricted candidate links.",
        "",
        "## Summary",
        "",
        f"- Species records: {summary.get('species_records')}",
        f"- Public visual slots ready: {summary.get('public_visual_ready')}",
        f"- Hero images ready: {summary.get('hero_image_ready')}",
        f"- Approved primary images still needed: {summary.get('approved_primary_needed')}",
        f"- Promotion-ready records: {summary.get('promotion_ready_count')}",
        f"- Candidate public-use blocked: {summary.get('candidate_public_use_blocked')}",
        "",
        "## Lane Counts",
        "",
    ]
    for lane, count in (summary.get("acquisition_lane_counts") or {}).items():
        lines.append(f"- `{lane}`: {count}")
    lines.extend(
        [
            "",
            "## Board",
            "",
            "| Species | Current public visual | Acquisition lane | Approval gap | Next action |",
            "|---|---|---|---|---|",
        ]
    )
    for record in payload.get("records") or []:
        visual = record.get("current_visual") or {}
        gap = record.get("approval_gap") or {}
        source = visual.get("public_source_url")
        domain = visual.get("public_source_domain") or "source pending"
        current = f"[{domain}]({source})" if source else domain
        current += f"<br>`{visual.get('render_strategy')}`"
        lane = f"`{record.get('acquisition_lane')}`<br>{record.get('source_strategy', {}).get('target_source_family_label')}"
        approval = f"{gap.get('checks_complete')}/{gap.get('checks_total')} checks<br>promotion: `{str(gap.get('promotion_allowed_now')).lower()}`"
        action = (record.get("next_actions") or ["-"])[1 if len(record.get("next_actions") or []) > 1 else 0]
        lines.append(
            "| "
            + " | ".join(
                [
                    f"{record.get('common_name')}<br>`{record.get('artifact_id')}`",
                    current,
                    lane,
                    approval,
                    action,
                ]
            )
            + " |"
        )
    lines.extend(["", "## Per-Species Actions", ""])
    for record in payload.get("records") or []:
        lines.append(f"### {record.get('common_name')} ({record.get('scientific_name')})")
        lines.append("")
        lines.append(f"- Artifact: `{record.get('artifact_id')}`")
        lines.append(f"- Lane: `{record.get('acquisition_lane')}`")
        lines.append(f"- Target source family: `{record.get('source_strategy', {}).get('target_source_family')}`")
        source = record.get("current_visual", {}).get("public_source_url")
        if source:
            lines.append(f"- Current public source card: {source}")
        flags = record.get("candidate_snapshot", {}).get("flags") or []
        if flags:
            lines.append("- Candidate flags: " + ", ".join(f"`{flag}`" for flag in flags))
        lines.append("- Next actions:")
        for action in record.get("next_actions") or []:
            lines.append(f"  - {action}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def main():
    payload = build_plan()
    ACQUISITION_PLAN_PATH.write_text(
        yaml.safe_dump(payload, sort_keys=False, allow_unicode=False, width=120),
        encoding="utf-8",
    )
    REVIEW_PACK_PATH.parent.mkdir(parents=True, exist_ok=True)
    REVIEW_PACK_PATH.write_text(markdown(payload), encoding="utf-8")
    print(f"Wrote {rel(ACQUISITION_PLAN_PATH)}")
    print(f"Wrote {rel(REVIEW_PACK_PATH)}")
    print(
        "Species media acquisition plan: "
        f"{payload['summary']['species_records']} records, "
        f"{payload['summary']['approved_primary_needed']} primary images still needed."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
