#!/usr/bin/env python3
"""Build a reviewer-only species media approval workbench.

This joins the approval queue, dossiers, Commons API snapshots, acquisition
plan, outreach packets, public render boundary, and trace ledger into one
curator surface. It is intentionally reviewer-only because it includes
candidate file pages and direct image URLs.

Usage:
  python scripts/build_species_media_approval_workbench.py
"""
from __future__ import annotations

import argparse
from collections import Counter
from datetime import date
import html
from pathlib import Path
import re

import yaml

ROOT = Path(__file__).resolve().parent.parent
MEDIA_DIR = ROOT / "content" / "media"
REVIEW_PACK_DIR = MEDIA_DIR / "review-packs"

REGISTRY_PATH = MEDIA_DIR / "species-media-registry.yaml"
APPROVAL_QUEUE_PATH = MEDIA_DIR / "species-media-approval-queue.yaml"
APPROVAL_DOSSIERS_PATH = MEDIA_DIR / "species-media-approval-dossiers.yaml"
COMMONS_RIGHTS_SNAPSHOTS_PATH = MEDIA_DIR / "species-media-commons-rights-snapshots.yaml"
ACQUISITION_PLAN_PATH = MEDIA_DIR / "species-media-acquisition-plan.yaml"
PUBLIC_EXPLORER_PATH = MEDIA_DIR / "species-media-public-explorer-manifest.yaml"
TRACE_LEDGER_PATH = MEDIA_DIR / "species-media-trace-ledger.yaml"
OUTREACH_PACKETS_PATH = MEDIA_DIR / "species-media-outreach-packets.yaml"
WORKBENCH_MANIFEST_PATH = MEDIA_DIR / "species-media-approval-workbench.yaml"

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

WORKBENCH_STATUS_LABELS = {
    "promotion_ready": "Promotion ready",
    "ethics_first": "Ethics first",
    "snapshot_recheck": "Snapshot recheck",
    "official_rights_review": "Official rights",
    "open_public_domain_review": "Open public domain",
    "open_license_attribution_review": "Attribution review",
    "partner_outreach": "Partner outreach",
    "approval_queue_review": "Approval queue",
}


def load_yaml(path: Path):
    if not path.exists():
        return {}
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def rel(path: Path):
    return path.relative_to(ROOT).as_posix()


def by_id(payload):
    return {record.get("artifact_id"): record for record in payload.get("records") or []}


def esc(value):
    if value is None:
        return ""
    return html.escape(str(value), quote=True)


def slug(value):
    value = (value or "none").lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-") or "none"


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


def status_for(dossier_record, snapshot_record, acquisition_record, approval_record):
    if promotion_allowed(approval_record):
        return "promotion_ready"
    flags = sorted(
        set(
            ((dossier_record.get("candidate_evidence") or {}).get("flags") or [])
            + ((snapshot_record.get("ethics_location_evidence") or {}).get("api_text_flags") or [])
            + ((snapshot_record.get("ethics_location_evidence") or {}).get("registry_flags") or [])
        )
    )
    if flags or acquisition_record.get("acquisition_lane") == "ethics_first_candidate_review":
        return "ethics_first"
    if snapshot_record and snapshot_record.get("snapshot_status") != "fetched":
        return "snapshot_recheck"
    lane = acquisition_record.get("acquisition_lane")
    if lane == "official_public_domain_review":
        return "official_rights_review"
    if lane == "open_public_domain_review":
        return "open_public_domain_review"
    if lane == "open_license_attribution_review":
        return "open_license_attribution_review"
    if lane == "partner_or_ngo_media_grant":
        return "partner_outreach"
    return "approval_queue_review"


def approval_snippet(approval_record):
    template = approval_record.get("approved_primary_template") or {}
    snippet = {
        "decision": "approve_primary",
        "reviewer": "TODO-curator-github-handle",
        "reviewed_on": date.today().isoformat(),
        "checks": {key: True for key in APPROVAL_CHECKS},
        "approved_primary_template": {
            "approved_asset_id": template.get("approved_asset_id") or "TODO",
            "source_url": template.get("source_url") or "TODO",
            "original_media_url": template.get("original_media_url") or "TODO-if-different",
            "creator": template.get("creator") or "TODO",
            "credit": template.get("credit") or "TODO",
            "license": template.get("license") or "TODO",
            "license_url": template.get("license_url") or "TODO-if-applicable",
            "rights_status": template.get("rights_status") or "TODO-public-domain|cc0|cc-by|cc-by-sa|partner-grant",
            "alt_text": template.get("alt_text") or "TODO-plain-visible-content-only",
            "species_match_basis": template.get("species_match_basis") or "TODO-source-caption|taxon-page|partner-assertion|expert-review",
            "crop_guidance": template.get("crop_guidance") or "TODO-desktop-mobile-card-crop",
            "ethics_notes": template.get("ethics_notes") or "TODO-proximity-location-captivity-distress-check",
            "approved_surfaces": template.get("approved_surfaces") or ["species-page-primary", "visual-explorer-card"],
            "blocked_surfaces": template.get("blocked_surfaces") or [
                "social-crop-until-reviewed",
                "merchandise",
                "paid-ad-without-extra-rights-check",
            ],
        },
    }
    return yaml.safe_dump(snippet, sort_keys=False, allow_unicode=False, width=100).rstrip()


def first_action(actions):
    actions = actions or []
    if len(actions) > 1:
        return actions[1]
    return actions[0] if actions else "Complete reviewer checks before promotion."


def build_record(
    registry_record,
    approval_record,
    dossier_record,
    snapshot_record,
    acquisition_record,
    public_record,
    trace_record,
    outreach_record,
):
    artifact_id = registry_record.get("artifact_id")
    approval_record = approval_record or {}
    dossier_record = dossier_record or {}
    snapshot_record = snapshot_record or {}
    acquisition_record = acquisition_record or {}
    public_record = public_record or {}
    trace_record = trace_record or {}
    outreach_record = outreach_record or {}

    candidate = (
        dossier_record.get("candidate_evidence")
        or approval_record.get("candidate")
        or ((registry_record.get("primary") or {}).get("candidate") or {})
    )
    snapshot_candidate = snapshot_record.get("candidate") or {}
    checks = approval_record.get("checks") or {}
    approved = approval_record.get("approved_primary_template") or {}
    missing_checks = [key for key in APPROVAL_CHECKS if checks.get(key) is not True]
    missing_fields = [key for key in REQUIRED_APPROVED_FIELDS if not approved.get(key)]
    snapshot_rights = snapshot_record.get("rights_evidence") or {}
    species_evidence = snapshot_record.get("species_match_evidence") or {}
    ethics = snapshot_record.get("ethics_location_evidence") or {}
    public_visual = (public_record.get("public_visual") or {})
    public_surface_rules = public_record.get("surface_rules") or {}
    source_card = (
        dossier_record.get("current_public_fallback")
        or approval_record.get("source_card_fallback")
        or public_record.get("source_card")
        or {}
    )
    acquisition_strategy = acquisition_record.get("source_strategy") or {}
    current_visual = acquisition_record.get("current_visual") or {}
    outreach_permission = outreach_record.get("permission_request") or {}
    flags = sorted(
        set(
            (candidate.get("flags") or [])
            + (ethics.get("api_text_flags") or [])
            + (ethics.get("registry_flags") or [])
        )
    )
    status = status_for(dossier_record, snapshot_record, acquisition_record, approval_record)

    return {
        "artifact_id": artifact_id,
        "ownership_key": f"{artifact_id}|{registry_record.get('species_page')}",
        "species_page": registry_record.get("species_page"),
        "website_path": registry_record.get("website_path") or public_record.get("website_path"),
        "common_name": registry_record.get("common_name"),
        "scientific_name": registry_record.get("scientific_name"),
        "taxon_group": registry_record.get("taxon_group"),
        "workbench_status": status,
        "workbench_label": WORKBENCH_STATUS_LABELS[status],
        "priority": acquisition_record.get("priority") or dossier_record.get("priority") or "P2",
        "candidate_media": {
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
            "score": candidate.get("score"),
            "flags": flags,
            "public_use": False,
            "reviewer_only": True,
        },
        "commons_snapshot": {
            "snapshot_status": snapshot_record.get("snapshot_status"),
            "asset_id": snapshot_candidate.get("asset_id"),
            "api_rights_status": snapshot_rights.get("api_rights_status"),
            "registry_rights_status": snapshot_rights.get("registry_rights_status"),
            "reviewable_for_public_primary": snapshot_rights.get("reviewable_for_public_primary") is True,
            "license_metadata_present": snapshot_rights.get("license_metadata_present") is True,
            "creator_metadata_present": snapshot_rights.get("creator_metadata_present") is True,
            "credit_or_source_metadata_present": snapshot_rights.get("credit_or_source_metadata_present") is True,
            "alignment": snapshot_record.get("registry_alignment") or {},
            "species_text_signal": species_evidence.get("automated_text_signal") is True,
            "matched_terms": species_evidence.get("matched_terms") or [],
            "api_text_flags": ethics.get("api_text_flags") or [],
            "registry_flags": ethics.get("registry_flags") or [],
            "suggested_next_checks": (snapshot_record.get("approval_support") or {}).get("suggested_next_checks") or [],
            "snapshot_is_not_approval": True,
        },
        "approval_gate": {
            "decision": approval_record.get("decision"),
            "reviewer": approval_record.get("reviewer"),
            "reviewed_on": approval_record.get("reviewed_on"),
            "checks_complete": checked_count(checks),
            "checks_total": len(APPROVAL_CHECKS),
            "missing_checks": missing_checks,
            "missing_approved_primary_fields": missing_fields,
            "promotion_allowed_now": promotion_allowed(approval_record),
            "required_evidence": dossier_record.get("required_evidence") or [],
            "approval_yaml_snippet": approval_snippet(approval_record),
        },
        "public_boundary": {
            "current_visual_kind": public_visual.get("kind") or current_visual.get("public_visual_kind"),
            "render_strategy": public_visual.get("render_strategy") or current_visual.get("render_strategy"),
            "public_source_url": public_visual.get("source_url") or current_visual.get("public_source_url"),
            "public_source_domain": public_visual.get("domain") or current_visual.get("public_source_domain"),
            "public_source_type": public_visual.get("source_type") or current_visual.get("public_source_type"),
            "source_card_status": source_card.get("status") or current_visual.get("source_card_status"),
            "source_card_public_use": source_card.get("public_use") is True or current_visual.get("public_use") is True,
            "source_card_does_not_authorize_image_copy": True,
            "species_page_hero_image_allowed": public_surface_rules.get("species_page_hero_image_allowed") is True
            or current_visual.get("hero_image_ready") is True,
            "candidate_thumbnail_allowed": public_surface_rules.get("candidate_thumbnail_allowed") is True,
            "candidate_public_use": False,
        },
        "acquisition": {
            "lane": acquisition_record.get("acquisition_lane"),
            "label": acquisition_record.get("acquisition_label"),
            "target_source_family": acquisition_strategy.get("target_source_family"),
            "target_source_family_label": acquisition_strategy.get("target_source_family_label"),
            "google_images_role": acquisition_strategy.get("google_images_role"),
            "partner_media_grant_needed": acquisition_strategy.get("partner_media_grant_needed") is True,
            "outreach_targets": acquisition_strategy.get("outreach_targets") or [],
            "next_actions": acquisition_record.get("next_actions") or [],
        },
        "outreach": {
            "request_type": outreach_record.get("request_type"),
            "request_label": outreach_record.get("request_label"),
            "outreach_status": outreach_record.get("outreach_status"),
            "target": (outreach_record.get("permission_request") or {}).get("target")
            or ", ".join(acquisition_strategy.get("outreach_targets") or []),
            "source_card_fallback_until_approved": outreach_permission.get("source_card_fallback_until_approved") is True,
            "written_permission_required_before_reuse": outreach_permission.get("written_permission_required_before_reuse") is True,
            "required_permission_fields": outreach_permission.get("required_permission_fields") or [],
        },
        "trace": {
            "trace_state": trace_record.get("trace_state"),
            "trace_issues": trace_record.get("trace_issues") or [],
            "integrity_checks": trace_record.get("integrity_checks") or {},
        },
        "reviewer_actions": {
            "primary_next_action": first_action(acquisition_record.get("next_actions") or []),
            "review_sequence": dossier_record.get("review_sequence") or [],
            "dry_run_command": f"python scripts/promote_species_media.py --artifact-id {artifact_id}",
            "apply_command_after_clean_dry_run": f"python scripts/promote_species_media.py --artifact-id {artifact_id} --apply",
            "open_approval_queue_record": f"{rel(APPROVAL_QUEUE_PATH)}#{artifact_id}",
            "open_dossier_record": f"{rel(APPROVAL_DOSSIERS_PATH)}#{artifact_id}",
            "open_commons_snapshot_record": f"{rel(COMMONS_RIGHTS_SNAPSHOTS_PATH)}#{artifact_id}",
            "open_trace_record": f"{rel(TRACE_LEDGER_PATH)}#{artifact_id}",
        },
        "safety_controls": {
            "reviewer_only": True,
            "contains_review_candidate_urls": True,
            "not_public_site_input": True,
            "candidate_public_use": False,
            "source_card_no_copy_or_crop": True,
            "approved_primary_required_for_hero_image": True,
            "human_review_required_for_rights_species_ethics_crop_alt_text": True,
        },
    }


def build_payload():
    registry = load_yaml(REGISTRY_PATH)
    approval = load_yaml(APPROVAL_QUEUE_PATH)
    dossiers = load_yaml(APPROVAL_DOSSIERS_PATH)
    snapshots = load_yaml(COMMONS_RIGHTS_SNAPSHOTS_PATH)
    acquisition = load_yaml(ACQUISITION_PLAN_PATH)
    public = load_yaml(PUBLIC_EXPLORER_PATH)
    trace = load_yaml(TRACE_LEDGER_PATH)
    outreach = load_yaml(OUTREACH_PACKETS_PATH)

    approval_by_id = by_id(approval)
    dossier_by_id = by_id(dossiers)
    snapshot_by_id = by_id(snapshots)
    acquisition_by_id = by_id(acquisition)
    public_by_id = by_id(public)
    trace_by_id = by_id(trace)
    outreach_by_id = by_id(outreach)

    records = [
        build_record(
            registry_record,
            approval_by_id.get(registry_record.get("artifact_id")),
            dossier_by_id.get(registry_record.get("artifact_id")),
            snapshot_by_id.get(registry_record.get("artifact_id")),
            acquisition_by_id.get(registry_record.get("artifact_id")),
            public_by_id.get(registry_record.get("artifact_id")),
            trace_by_id.get(registry_record.get("artifact_id")),
            outreach_by_id.get(registry_record.get("artifact_id")),
        )
        for registry_record in registry.get("records") or []
    ]

    statuses = Counter(record.get("workbench_status") or "none" for record in records)
    lanes = Counter((record.get("acquisition") or {}).get("lane") or "none" for record in records)
    rights = Counter((record.get("candidate_media") or {}).get("rights_status") or "none" for record in records)
    api_rights = Counter((record.get("commons_snapshot") or {}).get("api_rights_status") or "none" for record in records)
    domains = Counter((record.get("public_boundary") or {}).get("public_source_domain") or "none" for record in records)
    targets = Counter(
        target
        for record in records
        for target in ((record.get("acquisition") or {}).get("outreach_targets") or ["source-to-confirm"])
    )
    missing_checks = Counter(
        check
        for record in records
        for check in ((record.get("approval_gate") or {}).get("missing_checks") or [])
    )
    missing_fields = Counter(
        field
        for record in records
        for field in ((record.get("approval_gate") or {}).get("missing_approved_primary_fields") or [])
    )
    flagged = [
        record["artifact_id"]
        for record in records
        if (record.get("candidate_media") or {}).get("flags")
    ]
    promotion_ready = [
        record["artifact_id"]
        for record in records
        if (record.get("approval_gate") or {}).get("promotion_allowed_now") is True
    ]
    public_ready = sum(
        1 for record in records if (record.get("public_boundary") or {}).get("source_card_public_use") is True
    )
    hero_ready = sum(
        1
        for record in records
        if (record.get("public_boundary") or {}).get("species_page_hero_image_allowed") is True
    )
    snapshots_fetched = sum(
        1
        for record in records
        if (record.get("commons_snapshot") or {}).get("snapshot_status") == "fetched"
    )

    return {
        "version": date.today().isoformat(),
        "generated_at": date.today().isoformat(),
        "sources": {
            "registry": rel(REGISTRY_PATH),
            "approval_queue": rel(APPROVAL_QUEUE_PATH),
            "approval_dossiers": rel(APPROVAL_DOSSIERS_PATH),
            "commons_rights_snapshots": rel(COMMONS_RIGHTS_SNAPSHOTS_PATH),
            "acquisition_plan": rel(ACQUISITION_PLAN_PATH),
            "public_explorer": rel(PUBLIC_EXPLORER_PATH),
            "trace_ledger": rel(TRACE_LEDGER_PATH),
            "outreach_packets": rel(OUTREACH_PACKETS_PATH),
        },
        "policy": {
            "reviewer_only": True,
            "contains_review_candidate_urls": True,
            "not_public_site_input": True,
            "candidate_public_use": False,
            "public_site_must_use_render_contract": True,
            "source_card_does_not_authorize_image_copy": True,
            "promotion_requires_approval_queue": True,
            "human_review_required_for_rights_species_ethics_crop_alt_text": True,
            "google_images_discovery_only": True,
            "partner_grants_require_written_permission": True,
            "no_bulk_download_or_scraping": True,
        },
        "summary": {
            "species_records": len(records),
            "public_visual_ready": public_ready,
            "hero_image_ready": hero_ready,
            "approved_primary_needed": len(records) - hero_ready,
            "candidate_public_use_blocked": len(records),
            "commons_snapshots_fetched": snapshots_fetched,
            "promotion_ready_count": len(promotion_ready),
            "promotion_ready_artifact_ids": promotion_ready,
            "flagged_candidate_records": flagged,
            "workbench_status_counts": dict(sorted(statuses.items())),
            "acquisition_lane_counts": dict(sorted(lanes.items())),
            "candidate_rights_status_counts": dict(sorted(rights.items())),
            "api_rights_status_counts": dict(sorted(api_rights.items())),
            "public_source_domain_counts": dict(sorted(domains.items())),
            "outreach_target_counts": dict(sorted(targets.items())),
            "missing_check_counts": dict(sorted(missing_checks.items())),
            "missing_approved_primary_field_counts": dict(sorted(missing_fields.items())),
        },
        "records": records,
    }


def pill(text, variant="neutral"):
    return f'<span class="pill pill-{esc(variant)}">{esc(text or "none")}</span>'


def link_button(label, href):
    if not href:
        return ""
    return f'<a class="button-link" href="{esc(href)}" target="_blank" rel="noreferrer">{esc(label)}</a>'


def option(value, label):
    return f'<option value="{esc(value)}">{esc(label)}</option>'


def progress_bar(done, total):
    total = total or 0
    percent = 0 if not total else int((done / total) * 100)
    return (
        f'<div class="progress" aria-label="{esc(done)}/{esc(total)} checks complete">'
        f'<span style="width:{percent}%"></span></div>'
    )


def card(record):
    candidate = record.get("candidate_media") or {}
    snapshot = record.get("commons_snapshot") or {}
    approval = record.get("approval_gate") or {}
    boundary = record.get("public_boundary") or {}
    acquisition = record.get("acquisition") or {}
    outreach = record.get("outreach") or {}
    trace = record.get("trace") or {}
    actions = record.get("reviewer_actions") or {}
    flags = candidate.get("flags") or []
    status = record.get("workbench_status") or "none"
    group = record.get("taxon_group") or "ungrouped"
    lane = acquisition.get("lane") or "none"
    rights = candidate.get("rights_status") or "none"
    api_rights = snapshot.get("api_rights_status") or "none"
    domain = boundary.get("public_source_domain") or "none"
    source_type = boundary.get("public_source_type") or "none"
    image_src = candidate.get("image_url")
    image_alt = f"Review candidate for {record.get('common_name') or record.get('artifact_id')}"
    missing_checks = approval.get("missing_checks") or []
    missing_fields = approval.get("missing_approved_primary_fields") or []
    search_blob = " ".join(
        str(value or "")
        for value in [
            record.get("artifact_id"),
            record.get("common_name"),
            record.get("scientific_name"),
            record.get("species_page"),
            status,
            group,
            lane,
            rights,
            api_rights,
            domain,
            source_type,
            candidate.get("title"),
            candidate.get("creator"),
            candidate.get("credit"),
            outreach.get("request_type"),
            outreach.get("request_label"),
            " ".join(flags),
            " ".join(snapshot.get("matched_terms") or []),
        ]
    ).lower()
    flag_html = "".join(pill(flag.replace("_", " "), "flag") for flag in flags) or pill("no automated flags", "ok")
    image_html = (
        f'<img src="{esc(image_src)}" alt="{esc(image_alt)}" loading="lazy" decoding="async">'
        if image_src
        else '<div class="empty-image">No candidate image</div>'
    )
    snippet = approval.get("approval_yaml_snippet") or ""
    source_card_link = link_button("Source card", boundary.get("public_source_url"))
    return f"""
    <article class="species-card group-{esc(slug(group))}" data-search="{esc(search_blob)}" data-status="{esc(status)}" data-group="{esc(group)}" data-lane="{esc(lane)}" data-rights="{esc(rights)}" data-api-rights="{esc(api_rights)}" data-domain="{esc(domain)}" data-flagged="{str(bool(flags)).lower()}">
      <figure class="media-frame">
        {image_html}
      </figure>
      <div class="card-body">
        <div class="pill-row">
          {pill(record.get("workbench_label"), "status")}
          {pill(group)}
          {pill(record.get("priority"), "priority")}
          {pill(rights, "rights")}
          {pill(api_rights, "api")}
          {pill(lane.replace("_", " "), "lane")}
        </div>
        <h2>{esc(record.get("common_name"))}</h2>
        <p class="scientific">{esc(record.get("scientific_name"))}</p>
        <div class="flag-row">{flag_html}</div>
        <dl class="meta-grid">
          <div><dt>Candidate</dt><dd>{esc(candidate.get("title"))}</dd></div>
          <div><dt>Creator</dt><dd>{esc(candidate.get("creator"))}</dd></div>
          <div><dt>License</dt><dd>{esc(candidate.get("license"))}</dd></div>
          <div><dt>Commons snapshot</dt><dd>{esc(snapshot.get("snapshot_status"))}</dd></div>
          <div><dt>Species signal</dt><dd>{esc(", ".join(snapshot.get("matched_terms") or []) or "none")}</dd></div>
          <div><dt>Source card</dt><dd>{esc(domain)} / {esc(boundary.get("source_card_status"))}</dd></div>
          <div><dt>Outreach</dt><dd>{esc(outreach.get("request_type"))}</dd></div>
          <div><dt>Trace</dt><dd>{esc(trace.get("trace_state"))}</dd></div>
        </dl>
        <section class="gate-block">
          <div class="gate-head">
            <strong>Approval gate</strong>
            <span>{esc(approval.get("checks_complete", 0))}/{esc(approval.get("checks_total", 0))} checks</span>
          </div>
          {progress_bar(approval.get("checks_complete", 0), approval.get("checks_total", 0))}
          <p>{esc(len(missing_checks))} checks and {esc(len(missing_fields))} approved-primary fields still missing.</p>
        </section>
        <section class="boundary-block">
          {pill("candidate hidden from public", "blocked")}
          {pill("source card no copy/crop", "blocked")}
          {pill("hero locked until approval", "blocked")}
        </section>
        <p class="next-action">{esc(actions.get("primary_next_action"))}</p>
        <details>
          <summary>Approval YAML starter</summary>
          <pre>{esc(snippet)}</pre>
        </details>
        <div class="links">
          {link_button("Candidate file", candidate.get("commons_file_page"))}
          {link_button("Direct image", candidate.get("image_url"))}
          {source_card_link}
        </div>
        <p class="command"><code>{esc(actions.get("dry_run_command"))}</code></p>
      </div>
    </article>
    """


def html_page(payload):
    records = payload.get("records") or []
    summary = payload.get("summary") or {}
    groups = Counter(record.get("taxon_group") or "ungrouped" for record in records)
    statuses = Counter(record.get("workbench_status") or "none" for record in records)
    lanes = Counter((record.get("acquisition") or {}).get("lane") or "none" for record in records)
    rights = Counter((record.get("candidate_media") or {}).get("rights_status") or "none" for record in records)
    api_rights = Counter((record.get("commons_snapshot") or {}).get("api_rights_status") or "none" for record in records)
    domains = Counter((record.get("public_boundary") or {}).get("public_source_domain") or "none" for record in records)
    group_options = "".join(option(value, f"{value} ({count})") for value, count in sorted(groups.items()))
    status_options = "".join(option(value, f"{value.replace('_', ' ')} ({count})") for value, count in sorted(statuses.items()))
    lane_options = "".join(option(value, f"{value.replace('_', ' ')} ({count})") for value, count in sorted(lanes.items()))
    rights_options = "".join(option(value, f"{value.replace('_', ' ')} ({count})") for value, count in sorted(rights.items()))
    api_options = "".join(option(value, f"{value.replace('_', ' ')} ({count})") for value, count in sorted(api_rights.items()))
    domain_options = "".join(option(value, f"{value} ({count})") for value, count in sorted(domains.items()))
    cards = "\n".join(card(record) for record in records)
    generated_at = payload.get("generated_at") or date.today().isoformat()
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Blue Life Commons Species Media Approval Workbench</title>
  <style>
    :root {{
      color-scheme: light;
      --ink: #0f2226;
      --muted: #5a6a6d;
      --paper: #f6f7f1;
      --panel: #ffffff;
      --line: #d8dfd9;
      --sea: #0f766e;
      --blue: #286f94;
      --gold: #a96f13;
      --clay: #a5533f;
      --violet: #65507c;
      --green: #496f34;
      --shadow: 0 18px 46px rgba(15, 34, 38, 0.12);
    }}
    * {{ box-sizing: border-box; }}
    html {{ scroll-behavior: smooth; }}
    body {{
      margin: 0;
      background:
        linear-gradient(180deg, rgba(255,255,255,0.82), rgba(246,247,241,0.96)),
        repeating-linear-gradient(90deg, rgba(15,34,38,0.035) 0 1px, transparent 1px 112px);
      color: var(--ink);
      font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      line-height: 1.5;
    }}
    main {{ width: min(1500px, calc(100% - 48px)); margin: 0 auto; padding: 28px 0 42px; }}
    header {{
      min-height: 246px;
      display: grid;
      grid-template-columns: minmax(0, 1fr) minmax(280px, 430px);
      align-items: end;
      gap: 28px;
      border-bottom: 1px solid var(--line);
    }}
    .eyebrow {{
      margin: 0 0 10px;
      color: var(--sea);
      font-size: 0.78rem;
      font-weight: 850;
      text-transform: uppercase;
      letter-spacing: 0;
    }}
    h1 {{ margin: 0; max-width: 900px; font-size: 3.25rem; line-height: 1.02; letter-spacing: 0; }}
    .subtitle {{ max-width: 820px; margin: 14px 0 0; color: var(--muted); font-size: 1.04rem; }}
    .contract-panel {{
      border: 1px solid var(--line);
      border-radius: 8px;
      background: rgba(255,255,255,0.88);
      padding: 16px;
      box-shadow: 0 10px 26px rgba(15,34,38,0.07);
    }}
    .contract-panel h2 {{ margin: 0 0 10px; font-size: 1rem; letter-spacing: 0; }}
    .contract-list {{ display: grid; grid-template-columns: 1fr 1fr; gap: 8px; margin: 0; }}
    .contract-list div {{ border-top: 1px solid var(--line); padding-top: 8px; min-width: 0; }}
    dt {{ color: var(--muted); font-size: 0.72rem; font-weight: 760; text-transform: uppercase; letter-spacing: 0; }}
    dd {{ margin: 2px 0 0; overflow-wrap: anywhere; }}
    .contract-list dd {{ font-size: 1.12rem; font-weight: 800; }}
    .summary-grid {{
      display: grid;
      grid-template-columns: repeat(6, minmax(0, 1fr));
      gap: 12px;
      margin: 20px 0;
    }}
    .summary-item {{
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 13px 15px;
      box-shadow: 0 8px 24px rgba(15,34,38,0.06);
    }}
    .summary-item span {{ display: block; color: var(--muted); font-size: 0.74rem; font-weight: 780; text-transform: uppercase; letter-spacing: 0; }}
    .summary-item strong {{ display: block; margin-top: 4px; font-size: 1.78rem; line-height: 1.1; }}
    .toolbar {{
      position: sticky;
      top: 0;
      z-index: 5;
      display: grid;
      grid-template-columns: minmax(220px, 1.45fr) repeat(6, minmax(128px, 0.7fr)) auto;
      gap: 9px;
      align-items: center;
      padding: 13px 0;
      background: rgba(246,247,241,0.92);
      backdrop-filter: blur(12px);
    }}
    input, select {{
      width: 100%;
      min-height: 42px;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: var(--panel);
      color: var(--ink);
      padding: 0 11px;
      font: inherit;
    }}
    label.checkbox {{ min-height: 42px; display: inline-flex; gap: 7px; align-items: center; color: var(--muted); white-space: nowrap; font-weight: 700; }}
    .count {{ margin: 0 0 14px; color: var(--muted); font-size: 0.94rem; }}
    .board {{ display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 16px; }}
    .species-card {{
      display: grid;
      grid-template-columns: minmax(250px, 0.84fr) minmax(0, 1fr);
      min-width: 0;
      overflow: hidden;
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 8px;
      box-shadow: var(--shadow);
    }}
    .species-card::before {{ content: ""; display: block; grid-column: 1 / -1; height: 5px; background: var(--sea); }}
    .group-pinnipeds::before {{ background: var(--clay); }}
    .group-turtles::before {{ background: var(--green); }}
    .group-sharks-rays::before {{ background: var(--blue); }}
    .group-reefs::before {{ background: var(--gold); }}
    .group-sirenians::before {{ background: var(--violet); }}
    .media-frame {{ margin: 0; min-height: 100%; background: #dfe8e6; border-right: 1px solid var(--line); }}
    .media-frame img {{ width: 100%; height: 100%; min-height: 480px; display: block; object-fit: cover; }}
    .empty-image {{ height: 100%; min-height: 480px; display: grid; place-items: center; color: var(--muted); font-weight: 800; }}
    .card-body {{ padding: 16px; min-width: 0; }}
    .pill-row, .flag-row, .boundary-block, .links {{ display: flex; flex-wrap: wrap; gap: 7px; align-items: center; }}
    .pill {{
      display: inline-flex;
      align-items: center;
      min-height: 24px;
      max-width: 100%;
      padding: 3px 8px;
      border: 1px solid var(--line);
      border-radius: 999px;
      background: #f4f6f3;
      color: var(--muted);
      font-size: 0.71rem;
      font-weight: 780;
      text-transform: uppercase;
      letter-spacing: 0;
      overflow-wrap: anywhere;
    }}
    .pill-status {{ border-color: #b8c7cf; color: var(--blue); background: #eef6f8; }}
    .pill-priority {{ border-color: #d9c69d; color: #78530c; background: #fff8e8; }}
    .pill-rights, .pill-api {{ border-color: #abd1c5; color: var(--sea); background: #eef8f4; }}
    .pill-lane {{ border-color: #c5bad8; color: var(--violet); background: #f4f0fa; }}
    .pill-ok {{ border-color: #b8d2bd; color: var(--green); background: #f1f8ee; }}
    .pill-flag {{ border-color: #ebc894; color: var(--gold); background: #fff7e4; }}
    .pill-blocked {{ border-color: #d7d2c7; color: #5b6668; background: #f7f4ee; }}
    h2 {{ margin: 13px 0 0; font-size: 1.28rem; line-height: 1.15; letter-spacing: 0; }}
    .scientific {{ margin: 3px 0 12px; color: var(--muted); font-style: italic; }}
    .flag-row {{ margin-bottom: 14px; }}
    .meta-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 10px 12px; margin: 0; }}
    .gate-block {{ margin-top: 14px; padding: 12px; border: 1px solid var(--line); border-radius: 8px; background: #fbfcfa; }}
    .gate-head {{ display: flex; justify-content: space-between; gap: 12px; color: var(--ink); font-size: 0.92rem; }}
    .progress {{ height: 8px; margin: 9px 0; border-radius: 999px; background: #e5ebe6; overflow: hidden; }}
    .progress span {{ display: block; height: 100%; background: var(--sea); }}
    .gate-block p, .next-action {{ margin: 0; color: var(--muted); font-size: 0.9rem; }}
    .boundary-block {{ margin-top: 12px; }}
    .next-action {{ min-height: 3.9em; margin-top: 12px; }}
    details {{ margin-top: 12px; }}
    summary {{ cursor: pointer; font-weight: 780; color: var(--ink); }}
    pre {{
      overflow-x: auto;
      max-height: 260px;
      margin: 10px 0 0;
      padding: 12px;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: #07161a;
      color: #d8f4ef;
      font-size: 0.78rem;
      line-height: 1.45;
    }}
    .links {{ margin-top: 14px; }}
    .button-link {{
      display: inline-flex;
      align-items: center;
      min-height: 34px;
      padding: 0 11px;
      border: 1px solid var(--line);
      border-radius: 8px;
      color: var(--ink);
      background: #fbfcfa;
      text-decoration: none;
      font-weight: 760;
      font-size: 0.88rem;
    }}
    .button-link:hover, .button-link:focus {{ border-color: var(--sea); color: var(--sea); outline: none; }}
    .command {{ margin: 12px 0 0; color: var(--muted); font-size: 0.82rem; overflow-wrap: anywhere; }}
    code {{ font-family: "Geist Mono", ui-monospace, SFMono-Regular, Consolas, monospace; }}
    .hidden {{ display: none; }}
    @media (prefers-reduced-motion: reduce) {{ html {{ scroll-behavior: auto; }} }}
    @media (max-width: 1260px) {{
      .board, header {{ grid-template-columns: 1fr; }}
      .species-card {{ grid-template-columns: minmax(220px, 0.7fr) minmax(0, 1fr); }}
      .summary-grid {{ grid-template-columns: repeat(3, minmax(0, 1fr)); }}
      .toolbar {{ grid-template-columns: minmax(220px, 1fr) repeat(2, minmax(150px, 0.6fr)); }}
    }}
    @media (max-width: 760px) {{
      main {{ width: min(100% - 32px, 640px); padding-top: 18px; }}
      h1 {{ font-size: 2rem; }}
      .summary-grid {{ grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 8px; }}
      .toolbar {{ position: static; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 8px; }}
      .toolbar input {{ grid-column: 1 / -1; }}
      .species-card, .meta-grid {{ grid-template-columns: 1fr; }}
      .media-frame {{ border-right: 0; border-bottom: 1px solid var(--line); }}
      .media-frame img, .empty-image {{ min-height: 260px; aspect-ratio: 16 / 10; }}
      .contract-list {{ grid-template-columns: 1fr 1fr; }}
    }}
  </style>
</head>
<body>
  <main data-approval-workbench="reviewer-only">
    <header>
      <div>
        <p class="eyebrow">Reviewer-only media control surface</p>
        <h1>Species Media Approval Workbench</h1>
        <p class="subtitle">Candidate photos, Commons rights evidence, source cards, outreach state, trace ownership, and promotion blockers in one place. This page is not a public site input.</p>
      </div>
      <section class="contract-panel" aria-label="Workbench contract">
        <h2>Boundary</h2>
        <dl class="contract-list">
          <div><dt>Generated</dt><dd>{esc(generated_at)}</dd></div>
          <div><dt>Species</dt><dd>{esc(summary.get("species_records", len(records)))}</dd></div>
          <div><dt>Candidate URLs</dt><dd>reviewer only</dd></div>
          <div><dt>Approved heroes</dt><dd>{esc(summary.get("hero_image_ready", 0))}</dd></div>
        </dl>
      </section>
    </header>
    <section class="summary-grid" aria-label="Summary">
      <div class="summary-item"><span>Species</span><strong>{esc(summary.get("species_records", len(records)))}</strong></div>
      <div class="summary-item"><span>Snapshots</span><strong>{esc(summary.get("commons_snapshots_fetched", 0))}</strong></div>
      <div class="summary-item"><span>Public Cards</span><strong>{esc(summary.get("public_visual_ready", 0))}</strong></div>
      <div class="summary-item"><span>Primary Needed</span><strong>{esc(summary.get("approved_primary_needed", 0))}</strong></div>
      <div class="summary-item"><span>Flagged</span><strong>{esc(len(summary.get("flagged_candidate_records") or []))}</strong></div>
      <div class="summary-item"><span>Promotion Ready</span><strong>{esc(summary.get("promotion_ready_count", 0))}</strong></div>
    </section>
    <section class="toolbar" aria-label="Filters">
      <input id="search" type="search" placeholder="Search species, source, creator, rights">
      <select id="status"><option value="">All statuses</option>{status_options}</select>
      <select id="group"><option value="">All groups</option>{group_options}</select>
      <select id="lane"><option value="">All lanes</option>{lane_options}</select>
      <select id="rights"><option value="">Candidate rights</option>{rights_options}</select>
      <select id="apiRights"><option value="">API rights</option>{api_options}</select>
      <select id="domain"><option value="">Source domains</option>{domain_options}</select>
      <label class="checkbox"><input id="flagged" type="checkbox"> Flagged only</label>
    </section>
    <p class="count"><span id="visible-count">{esc(len(records))}</span> shown</p>
    <section class="board" id="board">
      {cards}
    </section>
  </main>
  <script>
    const cards = Array.from(document.querySelectorAll(".species-card"));
    const search = document.getElementById("search");
    const status = document.getElementById("status");
    const group = document.getElementById("group");
    const lane = document.getElementById("lane");
    const rights = document.getElementById("rights");
    const apiRights = document.getElementById("apiRights");
    const domain = document.getElementById("domain");
    const flagged = document.getElementById("flagged");
    const count = document.getElementById("visible-count");

    function applyFilters() {{
      const query = search.value.trim().toLowerCase();
      let visible = 0;
      for (const card of cards) {{
        const show =
          (!query || card.dataset.search.includes(query)) &&
          (!status.value || card.dataset.status === status.value) &&
          (!group.value || card.dataset.group === group.value) &&
          (!lane.value || card.dataset.lane === lane.value) &&
          (!rights.value || card.dataset.rights === rights.value) &&
          (!apiRights.value || card.dataset.apiRights === apiRights.value) &&
          (!domain.value || card.dataset.domain === domain.value) &&
          (!flagged.checked || card.dataset.flagged === "true");
        card.classList.toggle("hidden", !show);
        if (show) visible += 1;
      }}
      count.textContent = visible.toString();
    }}

    for (const control of [search, status, group, lane, rights, apiRights, domain, flagged]) {{
      control.addEventListener("input", applyFilters);
      control.addEventListener("change", applyFilters);
    }}
  </script>
</body>
</html>
"""


def write_outputs(payload, html_path):
    MEDIA_DIR.mkdir(parents=True, exist_ok=True)
    REVIEW_PACK_DIR.mkdir(parents=True, exist_ok=True)
    WORKBENCH_MANIFEST_PATH.write_text(
        yaml.safe_dump(payload, sort_keys=False, allow_unicode=False, width=120),
        encoding="utf-8",
    )
    html_path.write_text(html_page(payload), encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--out",
        type=Path,
        default=REVIEW_PACK_DIR / f"species-media-approval-workbench-{date.today().isoformat()}.html",
        help="Output HTML path.",
    )
    args = parser.parse_args()
    html_path = args.out if args.out.is_absolute() else ROOT / args.out
    payload = build_payload()
    write_outputs(payload, html_path)
    print(f"Wrote {rel(WORKBENCH_MANIFEST_PATH)}")
    print(f"Wrote {rel(html_path)}")
    print(
        "Species media approval workbench: "
        f"{payload['summary']['species_records']} records, "
        f"{len(payload['summary']['flagged_candidate_records'])} flagged, "
        f"{payload['summary']['promotion_ready_count']} promotion-ready."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
