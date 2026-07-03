#!/usr/bin/env python3
"""Validate the species media registry against the current species corpus.

This check is intentionally about coverage and provenance readiness, not about
requiring every species to already have an approved image. A species may pass
with ``primary.status: needed`` as long as it is tracked, has source candidates,
and cannot be silently dropped from the media queue.

Usage: python scripts/validate_species_media.py
"""
from collections import Counter
from pathlib import Path
import sys

import yaml

ROOT = Path(__file__).resolve().parent.parent
REGISTRY_PATH = ROOT / "content" / "media" / "species-media-registry.yaml"
SOURCE_ROUTING_PATH = ROOT / "content" / "media" / "species-media-source-routing.yaml"
RICH_EMBEDS_PATH = ROOT / "content" / "media" / "species-media-rich-embeds.yaml"
APPROVAL_QUEUE_PATH = ROOT / "content" / "media" / "species-media-approval-queue.yaml"
RENDER_CONTRACT_PATH = ROOT / "content" / "media" / "species-media-render-contract.yaml"
CURATION_WORKSPACE_PATH = ROOT / "content" / "media" / "species-media-curation-workspace.yaml"
PUBLIC_EXPLORER_MANIFEST_PATH = ROOT / "content" / "media" / "species-media-public-explorer-manifest.yaml"
TRACE_LEDGER_PATH = ROOT / "content" / "media" / "species-media-trace-ledger.yaml"
ACQUISITION_PLAN_PATH = ROOT / "content" / "media" / "species-media-acquisition-plan.yaml"
APPROVAL_DOSSIERS_PATH = ROOT / "content" / "media" / "species-media-approval-dossiers.yaml"
OUTREACH_PACKETS_PATH = ROOT / "content" / "media" / "species-media-outreach-packets.yaml"
COMMONS_RIGHTS_SNAPSHOTS_PATH = ROOT / "content" / "media" / "species-media-commons-rights-snapshots.yaml"
APPROVAL_WORKBENCH_PATH = ROOT / "content" / "media" / "species-media-approval-workbench.yaml"
SPECIES_ROOT = ROOT / "content" / "species"

MEDIA_STATUSES = {
    "needs_primary_official_media",
    "primary_candidate_review",
    "approved_primary",
    "rich_embed_only",
    "blocked_rights",
}

PRIMARY_STATUSES = {"needed", "candidate", "approved", "rich_embed_only", "blocked"}

CANDIDATE_RIGHTS = {
    "public-domain-or-cc0-candidate",
    "cc-by-candidate",
    "cc-by-sa-candidate",
    "needs-review-no-derivatives",
    "blocked-noncommercial",
    "needs-review",
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

SOURCE_CARD_STATUSES = {
    "verified_source_card",
    "needs_browser_recheck",
    "needs_link_check",
    "missing_source_url",
    "broken_or_blocked",
}

APPROVAL_DECISIONS = {
    "pending",
    "approve_primary",
    "reject_candidate",
    "replace_candidate",
    "use_source_card_only",
}

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

RENDER_STRATEGIES = {
    "approved_primary_image",
    "verified_source_card_fallback",
    "source_card_recheck_placeholder",
    "review_only_candidate_placeholder",
    "blocked_no_public_visual",
}

PUBLIC_VISUAL_KINDS = {
    "image",
    "source_card",
    "source_card_placeholder",
    "placeholder",
}

CURATION_BATCHES = {
    "01_source_card_recheck",
    "02_ethics_flag_review",
    "03_official_public_domain_fast_track",
    "04_open_public_domain_review",
    "05_open_license_attribution",
    "06_partner_grant_or_new_candidate",
}

CURATION_WORKSTREAMS = {
    "public_fallback_recheck",
    "ethics_first",
    "primary_image_review",
    "partner_or_replacement",
}

PUBLIC_EXPLORER_BANNED_STRINGS = set()

PUBLIC_EXPLORER_BANNED_KEYS = {
    "commons_file_page",
    "image_url",
    "candidate_title",
}

TRACE_LEDGER_BANNED_KEYS = PUBLIC_EXPLORER_BANNED_KEYS | {
    "direct_image_url",
    "candidate_image_url",
}

ACQUISITION_LANES = {
    "primary_approved_maintenance",
    "promotion_apply_ready",
    "ethics_first_candidate_review",
    "official_public_domain_review",
    "open_public_domain_review",
    "open_license_attribution_review",
    "partner_or_ngo_media_grant",
}

ACQUISITION_TARGET_SOURCE_FAMILIES = {
    "official_institutional",
    "partner_or_ngo",
    "open_license_candidate",
    "authority_source",
    "institutional",
}

ACQUISITION_PLAN_BANNED_KEYS = TRACE_LEDGER_BANNED_KEYS | {
    "candidate_direct_url",
    "candidate_file_page",
}

APPROVAL_DOSSIER_STATUSES = {
    "promotion_ready",
    "ethics_first_review",
    "official_rights_review",
    "open_public_domain_review",
    "open_license_attribution_review",
    "partner_or_replacement_needed",
    "approval_queue_review",
}

APPROVAL_DOSSIER_REQUIRED_FIELDS = {
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
}

OUTREACH_REQUEST_TYPES = {
    "request_ethically_safe_alternative_or_context",
    "confirm_official_public_domain_terms",
    "confirm_public_domain_terms",
    "confirm_open_license_attribution_terms",
    "request_media_grant_or_replacement",
    "no_outreach_promotion_ready",
    "rights_maintenance_recheck",
}

OUTREACH_STATUSES = {"draft", "sent", "responded", "granted", "declined", "blocked"}

OUTREACH_BANNED_KEYS = TRACE_LEDGER_BANNED_KEYS | {
    "candidate_direct_url",
    "candidate_file_page",
    "commons_file_page",
    "image_url",
}

COMMONS_SNAPSHOT_STATUSES = {"fetched", "missing", "skipped", "error"}

APPROVAL_WORKBENCH_STATUSES = {
    "promotion_ready",
    "ethics_first",
    "snapshot_recheck",
    "official_rights_review",
    "open_public_domain_review",
    "open_license_attribution_review",
    "partner_outreach",
    "approval_queue_review",
}


def frontmatter(path: Path):
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return None
    parts = text.split("---", 2)
    if len(parts) < 3:
        return None
    return yaml.safe_load(parts[1])


def species_pages():
    pages = {}
    for path in sorted(SPECIES_ROOT.rglob("*.md")):
        if "_templates" in path.parts or path.name.upper() == "README.md":
            continue
        fm = frontmatter(path)
        if not fm or fm.get("type") != "species-page":
            continue
        rel = path.relative_to(ROOT).as_posix()
        pages[rel] = fm
    return pages


def validate_approved_primary(record):
    errors = []
    primary = record.get("primary") or {}
    if primary.get("status") != "approved":
        return errors

    required = [
        "approved_asset_id",
        "rights_status",
        "source_url",
        "creator",
        "credit",
        "license",
        "alt_text",
        "species_match_basis",
    ]
    for key in required:
        if not primary.get(key):
            errors.append(f"approved primary missing {key}")

    if primary.get("rights_status") not in ALLOWED_APPROVED_RIGHTS:
        errors.append(
            "approved primary rights_status must be one of "
            + ", ".join(sorted(ALLOWED_APPROVED_RIGHTS))
        )

    if primary.get("qa_status") != "approved":
        errors.append("approved primary must set qa_status: approved")

    approved_path = primary.get("approved_path")
    if approved_path and not (ROOT / approved_path).exists():
        errors.append(f"approved_path does not exist: {approved_path}")

    return errors


def validate_candidate_primary(record):
    errors = []
    primary = record.get("primary") or {}
    if primary.get("status") != "candidate":
        return errors

    candidate = primary.get("candidate") or {}
    required = ["asset_id", "provider", "title", "commons_file_page", "image_url", "rights_status", "review_status"]
    for key in required:
        if not candidate.get(key):
            errors.append(f"candidate primary missing {key}")

    if candidate.get("rights_status") not in CANDIDATE_RIGHTS:
        errors.append(f"candidate primary has invalid rights_status {candidate.get('rights_status')!r}")

    if candidate.get("review_status") != "candidate_needs_species_rights_ethics_review":
        errors.append("candidate primary must remain review-only until approved")

    if primary.get("qa_status") != "candidate_review":
        errors.append("candidate primary must set qa_status: candidate_review")

    return errors


def validate_source_card(record):
    errors = []
    card = record.get("source_card") or {}
    status = card.get("status")
    if status not in SOURCE_CARD_STATUSES:
        errors.append(f"invalid source_card.status {status!r}")
        return errors

    if not card.get("embed_id"):
        errors.append("source card missing embed_id")
    if not card.get("source_url") and status != "missing_source_url":
        errors.append("source card missing source_url")
    if card.get("copies_external_media") is not False:
        errors.append("source card must set copies_external_media: false")
    if status == "verified_source_card":
        if card.get("public_use") is not True:
            errors.append("verified source card must set public_use: true")
        if not card.get("domain"):
            errors.append("verified source card missing domain")
        if not card.get("allowed_surfaces"):
            errors.append("verified source card missing allowed_surfaces")
    elif card.get("public_use") is True:
        errors.append("unverified source card must not set public_use: true")
    if not card.get("blocked_surfaces"):
        errors.append("source card missing blocked_surfaces")
    if not card.get("reviewer_action"):
        errors.append("source card missing reviewer_action")
    return errors


def validate_approval_queue_record(record, registry_by_id):
    errors = []
    artifact_id = record.get("artifact_id")
    registry_record = registry_by_id.get(artifact_id)
    if not registry_record:
        errors.append("approval queue record has no matching registry record")
        return errors
    if record.get("species_page") != registry_record.get("species_page"):
        errors.append("approval queue species_page does not match registry")
    decision = record.get("decision")
    if decision not in APPROVAL_DECISIONS:
        errors.append(f"invalid approval decision {decision!r}")
    candidate = record.get("candidate") or {}
    registry_candidate = registry_candidate_lineage(registry_record)
    if candidate.get("asset_id") != registry_candidate.get("asset_id"):
        errors.append("approval queue candidate asset_id does not match registry candidate")
    checks = record.get("checks") or {}
    for key in APPROVAL_CHECKS:
        if key not in checks:
            errors.append(f"approval queue missing check {key}")
        elif not isinstance(checks.get(key), bool):
            errors.append(f"approval queue check {key} must be boolean")
    unknown_checks = sorted(set(checks) - APPROVAL_CHECKS)
    for key in unknown_checks:
        errors.append(f"approval queue has unknown check {key}")

    if decision == "approve_primary":
        missing_true = [key for key in APPROVAL_CHECKS if checks.get(key) is not True]
        for key in missing_true:
            errors.append(f"approve_primary decision requires {key}: true")
        if not record.get("reviewer"):
            errors.append("approve_primary decision missing reviewer")
        if not record.get("reviewed_on"):
            errors.append("approve_primary decision missing reviewed_on")
        approved = record.get("approved_primary_template") or {}
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
        for key in required:
            if not approved.get(key):
                errors.append(f"approve_primary decision missing approved_primary_template.{key}")
        if approved.get("rights_status") not in ALLOWED_APPROVED_RIGHTS:
            errors.append("approve_primary decision has invalid approved rights_status")
    return errors


def approval_record_is_promotable(record):
    if not record or record.get("decision") != "approve_primary":
        return False
    checks = record.get("checks") or {}
    if any(checks.get(key) is not True for key in APPROVAL_CHECKS):
        return False
    if not record.get("reviewer") or not record.get("reviewed_on"):
        return False
    approved = record.get("approved_primary_template") or {}
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
    if any(not approved.get(key) for key in required):
        return False
    return approved.get("rights_status") in ALLOWED_APPROVED_RIGHTS


def collect_strings(value):
    if isinstance(value, str):
        return {value}
    if isinstance(value, dict):
        found = set()
        for item in value.values():
            found.update(collect_strings(item))
        return found
    if isinstance(value, list):
        found = set()
        for item in value:
            found.update(collect_strings(item))
        return found
    return set()


def collect_keys(value):
    if isinstance(value, dict):
        found = set(value)
        for item in value.values():
            found.update(collect_keys(item))
        return found
    if isinstance(value, list):
        found = set()
        for item in value:
            found.update(collect_keys(item))
        return found
    return set()


def registry_candidate_lineage(registry_record):
    primary = registry_record.get("primary") or {}
    return primary.get("candidate") or primary.get("approved_from_candidate") or {}


def validate_render_contract_record(record, registry_by_id, rich_by_id):
    errors = []
    artifact_id = record.get("artifact_id")
    registry_record = registry_by_id.get(artifact_id)
    if not registry_record:
        errors.append("render contract record has no matching registry record")
        return errors
    if record.get("species_page") != registry_record.get("species_page"):
        errors.append("render contract species_page does not match registry")

    strategy = record.get("render_strategy")
    if strategy not in RENDER_STRATEGIES:
        errors.append(f"invalid render_strategy {strategy!r}")

    public_visual = record.get("public_visual") or {}
    visual_kind = public_visual.get("kind")
    if visual_kind not in PUBLIC_VISUAL_KINDS:
        errors.append(f"invalid public_visual.kind {visual_kind!r}")

    surface_rules = record.get("surface_rules") or {}
    hero_allowed = surface_rules.get("species_page_hero_image_allowed")
    if surface_rules.get("candidate_thumbnail_allowed") is not False:
        errors.append("candidate_thumbnail_allowed must be false")
    if record.get("candidate_public_use") is not False:
        errors.append("candidate_public_use must be false")

    review_candidate = record.get("review_only_candidate") or {}
    if review_candidate.get("public_use") is not False:
        errors.append("review_only_candidate.public_use must be false")
    registry_candidate = ((registry_record.get("primary") or {}).get("candidate") or {})
    if registry_candidate.get("asset_id") and review_candidate.get("asset_id") != registry_candidate.get("asset_id"):
        errors.append("review_only_candidate asset_id does not match registry candidate")

    primary = registry_record.get("primary") or {}
    source_card = (rich_by_id.get(artifact_id) or {}).get("source_card") or {}

    if strategy != "approved_primary_image" and hero_allowed is True:
        errors.append("only approved_primary_image may allow a species-page hero image")

    if strategy == "approved_primary_image":
        if primary.get("status") != "approved":
            errors.append("approved_primary_image requires registry primary.status: approved")
        if public_visual.get("kind") != "image":
            errors.append("approved_primary_image requires public_visual.kind: image")
        if public_visual.get("public_use") is not True:
            errors.append("approved_primary_image requires public_visual.public_use: true")
        if public_visual.get("asset_id") != primary.get("approved_asset_id"):
            errors.append("approved primary asset_id does not match registry")
        if public_visual.get("source_url") != primary.get("source_url"):
            errors.append("approved primary source_url does not match registry")
        if not public_visual.get("public_media_url"):
            errors.append("approved primary image must expose public_media_url")
        if not public_visual.get("alt_text"):
            errors.append("approved primary image must expose alt_text")
        if hero_allowed is not True:
            errors.append("approved_primary_image must allow species-page hero image")
    elif strategy == "verified_source_card_fallback":
        if public_visual.get("kind") != "source_card":
            errors.append("verified_source_card_fallback requires public_visual.kind: source_card")
        if public_visual.get("public_use") is not True:
            errors.append("verified_source_card_fallback requires public_visual.public_use: true")
        if hero_allowed is not False:
            errors.append("verified source-card fallback must not allow hero image reuse")
        if not public_visual.get("source_url"):
            errors.append("verified source-card fallback missing source_url")
        if not public_visual.get("domain"):
            errors.append("verified source-card fallback missing domain")
        if source_card.get("status") != "verified_source_card":
            errors.append("verified source-card fallback does not match rich embed status")
        if source_card.get("public_use") is not True:
            errors.append("verified source-card fallback rich embed public_use must be true")
        if source_card.get("source_url") != public_visual.get("source_url"):
            errors.append("verified source-card fallback source_url does not match rich embed")
    elif strategy == "source_card_recheck_placeholder":
        if public_visual.get("kind") != "source_card_placeholder":
            errors.append("source_card_recheck_placeholder requires public_visual.kind: source_card_placeholder")
        if public_visual.get("public_use") is not False:
            errors.append("source_card_recheck_placeholder must not be public_use")
        if source_card.get("status") != "needs_browser_recheck":
            errors.append("source_card_recheck_placeholder does not match rich embed status")
    elif strategy == "review_only_candidate_placeholder":
        if public_visual.get("kind") != "placeholder":
            errors.append("review_only_candidate_placeholder requires public_visual.kind: placeholder")
        if public_visual.get("public_use") is not False:
            errors.append("review_only_candidate_placeholder must not be public_use")
    elif strategy == "blocked_no_public_visual":
        if public_visual.get("public_use") is not False:
            errors.append("blocked_no_public_visual must not be public_use")

    public_visual_strings = collect_strings(public_visual)
    for key in ["image_url", "commons_file_page"]:
        candidate_url = registry_candidate.get(key)
        if candidate_url and candidate_url in public_visual_strings:
            errors.append(f"public_visual contains review-only candidate {key}")

    return errors


def public_acquisition_next_action(acquisition_record):
    next_actions = acquisition_record.get("next_actions") or []
    if len(next_actions) > 1:
        return next_actions[1]
    if next_actions:
        return next_actions[0]
    return None


def validate_public_explorer_record(record, registry_by_id, render_by_id, acquisition_by_id=None):
    errors = []
    artifact_id = record.get("artifact_id")
    registry_record = registry_by_id.get(artifact_id)
    render_record = render_by_id.get(artifact_id)
    acquisition_record = (acquisition_by_id or {}).get(artifact_id)
    if not registry_record:
        errors.append("public explorer record has no matching registry record")
        return errors
    if not render_record:
        errors.append("public explorer record has no matching render contract record")
        return errors
    if record.get("species_page") != registry_record.get("species_page"):
        errors.append("public explorer species_page does not match registry")

    public_visual = record.get("public_visual") or {}
    render_visual = render_record.get("public_visual") or {}
    surface_rules = record.get("surface_rules") or {}
    render_rules = render_record.get("surface_rules") or {}

    if public_visual.get("kind") not in PUBLIC_VISUAL_KINDS:
        errors.append(f"invalid public explorer visual kind {public_visual.get('kind')!r}")
    if public_visual.get("kind") != render_visual.get("kind"):
        errors.append("public explorer visual kind does not match render contract")
    if public_visual.get("public_use") is not (render_visual.get("public_use") is True):
        errors.append("public explorer public_use does not match render contract")
    if public_visual.get("render_strategy") != render_record.get("render_strategy"):
        errors.append("public explorer render strategy does not match render contract")
    if public_visual.get("copies_external_media") is True:
        errors.append("public explorer must not copy external source-card media")

    if render_visual.get("public_use") is True:
        if render_visual.get("source_url") and public_visual.get("source_url") != render_visual.get("source_url"):
            errors.append("public explorer source_url does not match public render contract")
    elif public_visual.get("source_url"):
        errors.append("public explorer must omit source_url when public_visual.public_use is false")

    if surface_rules.get("candidate_thumbnail_allowed") is not False:
        errors.append("public explorer must set candidate_thumbnail_allowed: false")
    if surface_rules.get("species_page_hero_image_allowed") is not (
        render_rules.get("species_page_hero_image_allowed") is True
    ):
        errors.append("public explorer hero-image rule does not match render contract")
    if surface_rules.get("visual_explorer_card_slot") is not True:
        errors.append("public explorer visual_explorer_card_slot must be true")

    candidate_review = record.get("candidate_review") or {}
    if candidate_review.get("candidate_public_use") is not False:
        errors.append("public explorer candidate_public_use must be false")
    if candidate_review.get("candidate_hidden_from_public_manifest") is not True:
        errors.append("public explorer must mark candidates hidden from public manifest")

    primary_status = (registry_record.get("primary") or {}).get("status")
    if surface_rules.get("species_page_hero_image_allowed") is True and primary_status != "approved":
        errors.append("public explorer may only allow hero images for approved primary media")

    if acquisition_by_id is not None:
        if not acquisition_record:
            errors.append("public explorer record has no matching acquisition plan record")
        else:
            acquisition = record.get("acquisition") or {}
            source_strategy = acquisition_record.get("source_strategy") or {}
            current_visual = acquisition_record.get("current_visual") or {}
            approval_gap = acquisition_record.get("approval_gap") or {}
            expected_target_family = source_strategy.get("target_source_family")
            if not acquisition:
                errors.append("public explorer record missing acquisition block")
            if acquisition.get("lane") != acquisition_record.get("acquisition_lane"):
                errors.append("public explorer acquisition.lane does not match acquisition plan")
            if acquisition.get("label") != acquisition_record.get("acquisition_label"):
                errors.append("public explorer acquisition.label does not match acquisition plan")
            if acquisition.get("priority") != acquisition_record.get("priority"):
                errors.append("public explorer acquisition.priority does not match acquisition plan")
            if acquisition.get("target_source_family") != expected_target_family:
                errors.append("public explorer acquisition.target_source_family does not match acquisition plan")
            if acquisition.get("target_source_family_label") != source_strategy.get("target_source_family_label"):
                errors.append("public explorer acquisition target label does not match acquisition plan")
            if acquisition.get("google_images_role") != "discovery_only":
                errors.append("public explorer acquisition.google_images_role must be discovery_only")
            if acquisition.get("partner_media_grant_needed") is not (
                source_strategy.get("partner_media_grant_needed") is True
            ):
                errors.append("public explorer acquisition.partner_media_grant_needed does not match acquisition plan")
            if sorted(acquisition.get("outreach_targets") or []) != sorted(source_strategy.get("outreach_targets") or []):
                errors.append("public explorer acquisition.outreach_targets does not match acquisition plan")
            if acquisition.get("approved_primary_needed") is not (
                current_visual.get("hero_image_ready") is not True
            ):
                errors.append("public explorer acquisition.approved_primary_needed does not match acquisition plan")
            if acquisition.get("promotion_allowed_now") is not (
                approval_gap.get("promotion_allowed_now") is True
            ):
                errors.append("public explorer acquisition.promotion_allowed_now does not match acquisition plan")
            if acquisition.get("checks_complete") != (approval_gap.get("checks_complete") or 0):
                errors.append("public explorer acquisition.checks_complete does not match acquisition plan")
            if acquisition.get("checks_total") != (approval_gap.get("checks_total") or 0):
                errors.append("public explorer acquisition.checks_total does not match acquisition plan")
            if acquisition.get("next_action") != public_acquisition_next_action(acquisition_record):
                errors.append("public explorer acquisition.next_action does not match acquisition plan")

    registry_candidate = ((registry_record.get("primary") or {}).get("candidate") or {})
    public_strings = collect_strings(record)
    for key in ["image_url", "commons_file_page"]:
        candidate_url = registry_candidate.get(key)
        if candidate_url and candidate_url in public_strings:
            errors.append(f"public explorer contains review-only candidate {key}")
    for public_string in public_strings:
        for banned in PUBLIC_EXPLORER_BANNED_STRINGS:
            if banned in public_string:
                errors.append(f"public explorer contains banned public string {banned!r}")

    return errors


def validate_species_page_media(registry_record, page_fm, render_by_id, public_by_id):
    errors = []
    artifact_id = registry_record.get("artifact_id")
    media = page_fm.get("media") or {}
    render_record = render_by_id.get(artifact_id)
    public_record = public_by_id.get(artifact_id)
    if not media:
        errors.append("species page missing media frontmatter block")
        return errors
    if not render_record:
        errors.append("species page media cannot be checked without render contract record")
        return errors
    if not public_record:
        errors.append("species page media cannot be checked without public explorer record")
        return errors

    expected_registry = f"content/media/species-media-registry.yaml#{artifact_id}"
    expected_render = f"content/media/species-media-render-contract.yaml#{artifact_id}"
    expected_public = f"content/media/species-media-public-explorer-manifest.yaml#{artifact_id}"
    if media.get("registry_record") != expected_registry:
        errors.append("media.registry_record does not point to this artifact")
    if media.get("render_contract") != expected_render:
        errors.append("media.render_contract does not point to this artifact")
    if media.get("public_explorer_record") != expected_public:
        errors.append("media.public_explorer_record does not point to this artifact")

    render_media = media.get("render") or {}
    surface_rules = render_record.get("surface_rules") or {}
    public_visual = render_record.get("public_visual") or {}
    if render_media.get("strategy") != render_record.get("render_strategy"):
        errors.append("media.render.strategy does not match render contract")
    if render_media.get("public_visual_kind") != public_visual.get("kind"):
        errors.append("media.render.public_visual_kind does not match render contract")
    if render_media.get("public_visual_public_use") is not (public_visual.get("public_use") is True):
        errors.append("media.render.public_visual_public_use does not match render contract")
    if render_media.get("species_page_visual_slot") is not (
        surface_rules.get("species_page_visual_slot") is True
    ):
        errors.append("media.render.species_page_visual_slot does not match render contract")
    if render_media.get("species_page_hero_image_allowed") is not (
        surface_rules.get("species_page_hero_image_allowed") is True
    ):
        errors.append("media.render.species_page_hero_image_allowed does not match render contract")
    if render_media.get("candidate_thumbnail_allowed") is not False:
        errors.append("media.render.candidate_thumbnail_allowed must be false")
    if render_media.get("candidate_public_use") is not False:
        errors.append("media.render.candidate_public_use must be false")

    primary = media.get("primary") or {}
    registry_primary = registry_record.get("primary") or {}
    if render_record.get("render_strategy") == "approved_primary_image":
        if primary.get("asset_id") != public_visual.get("asset_id"):
            errors.append("media.primary.asset_id does not match approved public visual")
        if primary.get("source_url") != public_visual.get("source_url"):
            errors.append("media.primary.source_url does not match approved public visual")
        if primary.get("public_media_url") != public_visual.get("public_media_url"):
            errors.append("media.primary.public_media_url does not match approved public visual")
        for key in ["creator", "credit", "license", "alt_text"]:
            if not primary.get(key):
                errors.append(f"approved media.primary.{key} is required")
        if primary.get("qa_status") != "approved":
            errors.append("approved media.primary must set qa_status: approved")
    else:
        for key in ["asset_id", "path", "source_url", "creator", "credit", "license", "alt_text"]:
            if primary.get(key) is not None:
                errors.append(f"media.primary.{key} must remain null until primary image approval")
        if primary.get("rights_status") != "needs-review":
            errors.append("unapproved media.primary.rights_status must be needs-review")
        if primary.get("qa_status") != "candidate":
            errors.append("unapproved media.primary.qa_status must be candidate")
    if (media.get("review") or {}).get("primary_status") != registry_primary.get("status"):
        errors.append("media.review.primary_status does not match registry primary.status")

    if public_visual.get("kind") == "source_card":
        embeds = media.get("embeds") or []
        if len(embeds) != 1:
            errors.append("source-card media must have exactly one public embed")
        else:
            embed = embeds[0]
            if embed.get("provider") != "source_card":
                errors.append("media embed provider must be source_card")
            if embed.get("url") != public_visual.get("source_url"):
                errors.append("media embed url does not match render contract source_url")
            if embed.get("rights_status") != "link-backed-source-card":
                errors.append("media embed rights_status must be link-backed-source-card")
            if embed.get("domain") != public_visual.get("domain"):
                errors.append("media embed domain does not match render contract")
            if embed.get("source_type") != public_visual.get("source_type"):
                errors.append("media embed source_type does not match render contract")

    media_strings = collect_strings(media)
    registry_candidate = ((registry_record.get("primary") or {}).get("candidate") or {})
    for key in ["image_url", "commons_file_page"]:
        candidate_url = registry_candidate.get(key)
        if candidate_url and candidate_url in media_strings:
            errors.append(f"media frontmatter contains review-only candidate {key}")
    for media_string in media_strings:
        for banned in PUBLIC_EXPLORER_BANNED_STRINGS:
            if banned in media_string:
                errors.append(f"media frontmatter contains banned public string {banned!r}")

    return errors


def validate_trace_ledger_record(record, registry_by_id, render_by_id, public_by_id):
    errors = []
    artifact_id = record.get("artifact_id")
    registry_record = registry_by_id.get(artifact_id)
    render_record = render_by_id.get(artifact_id)
    public_record = public_by_id.get(artifact_id)
    if not registry_record:
        errors.append("trace ledger record has no matching registry record")
        return errors
    if not render_record:
        errors.append("trace ledger record has no matching render contract record")
        return errors
    if not public_record:
        errors.append("trace ledger record has no matching public explorer record")
        return errors

    expected_ownership = f"{artifact_id}|{registry_record.get('species_page')}"
    if record.get("ownership_key") != expected_ownership:
        errors.append("trace ledger ownership_key does not match registry")
    if record.get("species_page") != registry_record.get("species_page"):
        errors.append("trace ledger species_page does not match registry")
    public_visual = record.get("public_visual") or {}
    render_visual = render_record.get("public_visual") or {}
    if public_visual.get("source_url") != render_visual.get("source_url"):
        errors.append("trace ledger public visual source_url does not match render contract")
    if public_visual.get("render_strategy") != render_record.get("render_strategy"):
        errors.append("trace ledger render_strategy does not match render contract")
    if public_visual.get("public_use") is not (render_visual.get("public_use") is True):
        errors.append("trace ledger public_use does not match render contract")
    if public_visual.get("hero_image_allowed") is not (
        ((render_record.get("surface_rules") or {}).get("species_page_hero_image_allowed")) is True
    ):
        errors.append("trace ledger hero_image_allowed does not match render contract")
    if public_visual.get("candidate_thumbnail_allowed") is not False:
        errors.append("trace ledger candidate_thumbnail_allowed must be false")

    candidate = record.get("candidate_review") or {}
    registry_candidate = ((registry_record.get("primary") or {}).get("candidate") or {})
    if candidate.get("asset_id") != registry_candidate.get("asset_id"):
        errors.append("trace ledger candidate asset_id does not match registry candidate")
    if candidate.get("public_use") is not False:
        errors.append("trace ledger candidate public_use must be false")
    if candidate.get("direct_urls_omitted") is not True:
        errors.append("trace ledger must mark candidate direct URLs omitted")

    integrity_checks = record.get("integrity_checks") or {}
    failed_checks = [key for key, value in integrity_checks.items() if value is not True]
    for key in failed_checks:
        errors.append(f"trace ledger integrity check failed: {key}")
    if record.get("trace_issues"):
        errors.append("trace ledger trace_issues must be empty")

    trace_keys = collect_keys(record)
    for key in sorted(TRACE_LEDGER_BANNED_KEYS & trace_keys):
        errors.append(f"trace ledger contains banned key {key!r}")
    trace_strings = collect_strings(record)
    for key in ["image_url", "commons_file_page"]:
        candidate_url = registry_candidate.get(key)
        if candidate_url and candidate_url in trace_strings:
            errors.append(f"trace ledger contains review-only candidate {key}")
    for trace_string in trace_strings:
        for banned in PUBLIC_EXPLORER_BANNED_STRINGS:
            if banned in trace_string:
                errors.append(f"trace ledger contains banned public string {banned!r}")

    return errors


def validate_acquisition_plan_record(record, registry_by_id, render_by_id, approval_by_id, trace_by_id):
    errors = []
    artifact_id = record.get("artifact_id")
    registry_record = registry_by_id.get(artifact_id)
    render_record = render_by_id.get(artifact_id)
    approval_record = approval_by_id.get(artifact_id)
    trace_record = trace_by_id.get(artifact_id)
    if not registry_record:
        errors.append("acquisition plan record has no matching registry record")
        return errors
    if not render_record:
        errors.append("acquisition plan record has no matching render contract record")
        return errors
    if not approval_record:
        errors.append("acquisition plan record has no matching approval queue record")
        return errors

    expected_ownership = f"{artifact_id}|{registry_record.get('species_page')}"
    if record.get("ownership_key") != expected_ownership:
        errors.append("acquisition plan ownership_key does not match registry")
    if record.get("species_page") != registry_record.get("species_page"):
        errors.append("acquisition plan species_page does not match registry")
    if record.get("desired_outcome") != "approved_primary_image":
        errors.append("acquisition plan desired_outcome must be approved_primary_image")
    if record.get("acquisition_lane") not in ACQUISITION_LANES:
        errors.append(f"invalid acquisition_lane {record.get('acquisition_lane')!r}")
    if not record.get("next_actions"):
        errors.append("acquisition plan record missing next_actions")

    current_visual = record.get("current_visual") or {}
    render_visual = render_record.get("public_visual") or {}
    render_rules = render_record.get("surface_rules") or {}
    if current_visual.get("render_strategy") != render_record.get("render_strategy"):
        errors.append("acquisition current_visual.render_strategy does not match render contract")
    if current_visual.get("public_visual_kind") != render_visual.get("kind"):
        errors.append("acquisition current_visual.public_visual_kind does not match render contract")
    if current_visual.get("public_use") is not (render_visual.get("public_use") is True):
        errors.append("acquisition current_visual.public_use does not match render contract")
    if current_visual.get("public_source_url") != render_visual.get("source_url"):
        errors.append("acquisition current_visual.public_source_url does not match render contract")
    if current_visual.get("hero_image_ready") is not (
        render_rules.get("species_page_hero_image_allowed") is True
    ):
        errors.append("acquisition current_visual.hero_image_ready does not match render contract")
    if current_visual.get("source_card_copies_external_media") is True:
        errors.append("acquisition source card must not copy external media")

    source_strategy = record.get("source_strategy") or {}
    if source_strategy.get("google_images_role") != "discovery_only":
        errors.append("acquisition source_strategy.google_images_role must be discovery_only")
    if source_strategy.get("target_source_family") not in ACQUISITION_TARGET_SOURCE_FAMILIES:
        errors.append("acquisition source_strategy has invalid target_source_family")
    if not isinstance(source_strategy.get("partner_media_grant_needed"), bool):
        errors.append("acquisition source_strategy.partner_media_grant_needed must be boolean")

    candidate = record.get("candidate_snapshot") or {}
    registry_candidate = ((registry_record.get("primary") or {}).get("candidate") or {})
    if candidate.get("asset_id") != registry_candidate.get("asset_id"):
        errors.append("acquisition candidate asset_id does not match registry candidate")
    if candidate.get("public_use") is not False:
        errors.append("acquisition candidate public_use must be false")
    if candidate.get("direct_urls_omitted") is not True:
        errors.append("acquisition candidate must mark direct URLs omitted")

    checks = approval_record.get("checks") or {}
    approval_gap = record.get("approval_gap") or {}
    expected_complete = sum(1 for key in APPROVAL_CHECKS if checks.get(key) is True)
    expected_missing = sorted(key for key in APPROVAL_CHECKS if checks.get(key) is not True)
    if approval_gap.get("decision") != approval_record.get("decision"):
        errors.append("acquisition approval_gap.decision does not match approval queue")
    if approval_gap.get("checks_complete") != expected_complete:
        errors.append("acquisition approval_gap.checks_complete does not match approval queue")
    if approval_gap.get("checks_total") != len(APPROVAL_CHECKS):
        errors.append("acquisition approval_gap.checks_total must match approval checklist")
    if sorted(approval_gap.get("missing_checks") or []) != expected_missing:
        errors.append("acquisition approval_gap.missing_checks does not match approval queue")
    if approval_gap.get("promotion_allowed_now") is not approval_record_is_promotable(approval_record):
        errors.append("acquisition approval_gap.promotion_allowed_now does not match approval queue")

    safety = record.get("safety_controls") or {}
    if safety.get("candidate_public_use") is not False:
        errors.append("acquisition safety_controls.candidate_public_use must be false")
    if safety.get("candidate_thumbnail_allowed") is not False:
        errors.append("acquisition safety_controls.candidate_thumbnail_allowed must be false")
    if safety.get("approved_primary_required_for_hero_image") is not True:
        errors.append("acquisition must require approved primary before hero image")
    if safety.get("source_card_does_not_authorize_image_copy") is not True:
        errors.append("acquisition must mark source card as not authorizing image copy")
    if safety.get("direct_candidate_urls_omitted") is not True:
        errors.append("acquisition must mark direct candidate URLs omitted")
    if trace_record and safety.get("trace_record_present") is not True:
        errors.append("acquisition trace_record_present must be true when trace ledger exists")
    if safety.get("trace_issues"):
        errors.append("acquisition safety_controls.trace_issues must be empty")

    acquisition_keys = collect_keys(record)
    for key in sorted(ACQUISITION_PLAN_BANNED_KEYS & acquisition_keys):
        errors.append(f"acquisition plan contains banned key {key!r}")
    acquisition_strings = collect_strings(record)
    for key in ["image_url", "commons_file_page"]:
        candidate_url = registry_candidate.get(key)
        if candidate_url and candidate_url in acquisition_strings:
            errors.append(f"acquisition plan contains review-only candidate {key}")
    for acquisition_string in acquisition_strings:
        for banned in PUBLIC_EXPLORER_BANNED_STRINGS:
            if banned in acquisition_string:
                errors.append(f"acquisition plan contains banned public string {banned!r}")

    return errors


def validate_approval_dossier_record(
    record,
    registry_by_id,
    approval_by_id,
    acquisition_by_id,
    public_by_id,
    trace_by_id,
    workspace_by_id,
):
    errors = []
    artifact_id = record.get("artifact_id")
    registry_record = registry_by_id.get(artifact_id)
    approval_record = approval_by_id.get(artifact_id)
    acquisition_record = acquisition_by_id.get(artifact_id)
    public_record = public_by_id.get(artifact_id)
    trace_record = trace_by_id.get(artifact_id)
    workspace_record = workspace_by_id.get(artifact_id)
    if not registry_record:
        errors.append("approval dossier record has no matching registry record")
        return errors
    if not approval_record:
        errors.append("approval dossier record has no matching approval queue record")
        return errors
    if not acquisition_record:
        errors.append("approval dossier record has no matching acquisition plan record")
        return errors

    expected_ownership = f"{artifact_id}|{registry_record.get('species_page')}"
    if record.get("ownership_key") != expected_ownership:
        errors.append("approval dossier ownership_key does not match registry")
    if record.get("species_page") != registry_record.get("species_page"):
        errors.append("approval dossier species_page does not match registry")
    if record.get("dossier_status") not in APPROVAL_DOSSIER_STATUSES:
        errors.append(f"invalid approval dossier status {record.get('dossier_status')!r}")
    if record.get("decision") != approval_record.get("decision"):
        errors.append("approval dossier decision does not match approval queue")

    candidate = record.get("candidate_evidence") or {}
    queue_candidate = approval_record.get("candidate") or {}
    registry_candidate = registry_candidate_lineage(registry_record)
    for key in [
        "asset_id",
        "provider",
        "title",
        "commons_file_page",
        "image_url",
        "creator",
        "credit",
        "license",
        "license_url",
        "rights_status",
    ]:
        if candidate.get(key) != queue_candidate.get(key):
            errors.append(f"approval dossier candidate_evidence.{key} does not match approval queue")
    if candidate.get("asset_id") != registry_candidate.get("asset_id"):
        errors.append("approval dossier candidate asset_id does not match registry candidate")
    if candidate.get("public_use") is not False:
        errors.append("approval dossier candidate public_use must be false")
    if candidate.get("reviewer_only") is not True:
        errors.append("approval dossier candidate reviewer_only must be true")

    checks = approval_record.get("checks") or {}
    gap = record.get("approval_gap") or {}
    expected_missing_checks = sorted(key for key in APPROVAL_CHECKS if checks.get(key) is not True)
    approved = approval_record.get("approved_primary_template") or {}
    expected_missing_fields = sorted(
        key for key in APPROVAL_DOSSIER_REQUIRED_FIELDS if not approved.get(key)
    )
    if gap.get("checks_complete") != sum(1 for key in APPROVAL_CHECKS if checks.get(key) is True):
        errors.append("approval dossier checks_complete does not match approval queue")
    if gap.get("checks_total") != len(APPROVAL_CHECKS):
        errors.append("approval dossier checks_total must match approval checklist")
    if sorted(gap.get("missing_checks") or []) != expected_missing_checks:
        errors.append("approval dossier missing_checks does not match approval queue")
    if sorted(gap.get("missing_approved_primary_fields") or []) != expected_missing_fields:
        errors.append("approval dossier missing approved-primary fields do not match approval queue")
    if gap.get("promotion_allowed_now") is not approval_record_is_promotable(approval_record):
        errors.append("approval dossier promotion_allowed_now does not match approval queue")

    required_evidence_checks = sorted(
        item.get("check") for item in (record.get("required_evidence") or [])
    )
    if required_evidence_checks != expected_missing_checks:
        errors.append("approval dossier required_evidence does not match missing checks")

    fallback = record.get("current_public_fallback") or {}
    queue_fallback = approval_record.get("source_card_fallback") or {}
    public_visual = (public_record.get("public_visual") or {}) if public_record else {}
    if fallback.get("status") != queue_fallback.get("status"):
        errors.append("approval dossier public fallback status does not match approval queue")
    if fallback.get("source_url") != (queue_fallback.get("source_url") or public_visual.get("source_url")):
        errors.append("approval dossier public fallback source_url does not match queue/public explorer")
    if fallback.get("public_use") is not (queue_fallback.get("public_use") is True):
        errors.append("approval dossier public fallback public_use does not match approval queue")
    if fallback.get("source_card_does_not_authorize_image_copy") is not True:
        errors.append("approval dossier must mark source card as not authorizing image copy")

    acquisition = record.get("acquisition") or {}
    source_strategy = acquisition_record.get("source_strategy") or {}
    if acquisition.get("lane") != acquisition_record.get("acquisition_lane"):
        errors.append("approval dossier acquisition lane does not match acquisition plan")
    if acquisition.get("label") != acquisition_record.get("acquisition_label"):
        errors.append("approval dossier acquisition label does not match acquisition plan")
    if acquisition.get("target_source_family") != source_strategy.get("target_source_family"):
        errors.append("approval dossier acquisition target family does not match acquisition plan")
    if sorted(acquisition.get("outreach_targets") or []) != sorted(source_strategy.get("outreach_targets") or []):
        errors.append("approval dossier outreach targets do not match acquisition plan")

    if workspace_record:
        curation = record.get("curation") or {}
        for key in ["recommended_batch", "batch_label", "workstream", "next_curator_action"]:
            if curation.get(key) != workspace_record.get(key):
                errors.append(f"approval dossier curation.{key} does not match curation workspace")

    template = record.get("approved_primary_template") or {}
    for key in [
        "approved_asset_id",
        "source_url",
        "original_media_url",
        "creator",
        "credit",
        "license",
        "license_url",
        "rights_status",
    ]:
        if template.get(key) != approved.get(key):
            errors.append(f"approval dossier approved_primary_template.{key} does not match approval queue")

    safety = record.get("safety_controls") or {}
    if safety.get("candidate_public_use") is not False:
        errors.append("approval dossier safety_controls.candidate_public_use must be false")
    if safety.get("candidate_links_reviewer_only") is not True:
        errors.append("approval dossier safety_controls.candidate_links_reviewer_only must be true")
    if safety.get("source_card_no_copy_or_crop") is not True:
        errors.append("approval dossier safety_controls.source_card_no_copy_or_crop must be true")
    if safety.get("approved_primary_required_for_hero_image") is not True:
        errors.append("approval dossier must require approved primary before hero image")
    if trace_record and safety.get("trace_record_present") is not True:
        errors.append("approval dossier trace_record_present must be true when trace ledger exists")

    handoff = record.get("handoff") or {}
    expected_pointers = {
        "approval_queue_record": f"content/media/species-media-approval-queue.yaml#{artifact_id}",
        "curation_workspace_record": f"content/media/species-media-curation-workspace.yaml#{artifact_id}",
        "acquisition_plan_record": f"content/media/species-media-acquisition-plan.yaml#{artifact_id}",
        "public_explorer_record": f"content/media/species-media-public-explorer-manifest.yaml#{artifact_id}",
        "trace_ledger_record": f"content/media/species-media-trace-ledger.yaml#{artifact_id}",
        "dry_run_command": f"python scripts/promote_species_media.py --artifact-id {artifact_id}",
        "apply_command_after_clean_dry_run": f"python scripts/promote_species_media.py --artifact-id {artifact_id} --apply",
    }
    for key, expected in expected_pointers.items():
        if handoff.get(key) != expected:
            errors.append(f"approval dossier handoff.{key} does not match expected value")

    if not record.get("review_sequence"):
        errors.append("approval dossier missing review_sequence")

    return errors


def expected_outreach_targets(acquisition_record):
    source_strategy = acquisition_record.get("source_strategy") or {}
    current_visual = acquisition_record.get("current_visual") or {}
    targets = [
        item
        for item in source_strategy.get("outreach_targets") or []
        if item and item != "partner_media_grant_needed"
    ]
    source_domain = current_visual.get("public_source_domain")
    if source_domain:
        targets.append(source_domain)
    return sorted(set(targets)) or ["source-to-confirm"]


def validate_outreach_record(record, registry_by_id, acquisition_by_id, public_by_id, approval_by_id):
    errors = []
    artifact_id = record.get("artifact_id")
    registry_record = registry_by_id.get(artifact_id)
    acquisition_record = acquisition_by_id.get(artifact_id)
    public_record = public_by_id.get(artifact_id)
    approval_record = approval_by_id.get(artifact_id)
    if not registry_record:
        errors.append("outreach record has no matching registry record")
        return errors
    if not acquisition_record:
        errors.append("outreach record has no matching acquisition plan record")
        return errors

    expected_ownership = f"{artifact_id}|{registry_record.get('species_page')}"
    if record.get("ownership_key") != expected_ownership:
        errors.append("outreach ownership_key does not match registry")
    if record.get("species_page") != registry_record.get("species_page"):
        errors.append("outreach species_page does not match registry")
    if record.get("request_type") not in OUTREACH_REQUEST_TYPES:
        errors.append(f"invalid outreach request_type {record.get('request_type')!r}")
    if record.get("outreach_status") not in OUTREACH_STATUSES:
        errors.append(f"invalid outreach_status {record.get('outreach_status')!r}")
    if not record.get("request_label"):
        errors.append("outreach record missing request_label")

    acquisition = record.get("acquisition") or {}
    source_strategy = acquisition_record.get("source_strategy") or {}
    if acquisition.get("lane") != acquisition_record.get("acquisition_lane"):
        errors.append("outreach acquisition.lane does not match acquisition plan")
    if acquisition.get("label") != acquisition_record.get("acquisition_label"):
        errors.append("outreach acquisition.label does not match acquisition plan")
    if acquisition.get("target_source_family") != source_strategy.get("target_source_family"):
        errors.append("outreach acquisition.target_source_family does not match acquisition plan")
    if acquisition.get("target_source_family_label") != source_strategy.get("target_source_family_label"):
        errors.append("outreach acquisition target label does not match acquisition plan")
    if acquisition.get("google_images_role") != "discovery_only":
        errors.append("outreach acquisition.google_images_role must be discovery_only")
    if acquisition.get("partner_media_grant_needed") is not (
        source_strategy.get("partner_media_grant_needed") is True
    ):
        errors.append("outreach acquisition.partner_media_grant_needed does not match acquisition plan")
    if sorted(acquisition.get("outreach_targets") or []) != expected_outreach_targets(acquisition_record):
        errors.append("outreach acquisition.outreach_targets does not match acquisition plan")

    current_source = record.get("current_public_source") or {}
    acquisition_visual = acquisition_record.get("current_visual") or {}
    if current_source.get("kind") != acquisition_visual.get("public_visual_kind"):
        errors.append("outreach current source kind does not match acquisition plan")
    if current_source.get("source_url") != acquisition_visual.get("public_source_url"):
        errors.append("outreach current source URL does not match acquisition plan")
    if current_source.get("domain") != acquisition_visual.get("public_source_domain"):
        errors.append("outreach current source domain does not match acquisition plan")
    if current_source.get("source_type") != acquisition_visual.get("public_source_type"):
        errors.append("outreach current source type does not match acquisition plan")
    if current_source.get("public_use") is not (acquisition_visual.get("public_use") is True):
        errors.append("outreach current source public_use does not match acquisition plan")
    if current_source.get("source_card_does_not_authorize_image_copy") is not True:
        errors.append("outreach must mark source card as not authorizing image copy")

    approval_gap = record.get("approval_gap") or {}
    acquisition_gap = acquisition_record.get("approval_gap") or {}
    if approval_gap.get("decision") != acquisition_gap.get("decision"):
        errors.append("outreach approval_gap.decision does not match acquisition plan")
    if approval_gap.get("checks_complete") != (acquisition_gap.get("checks_complete") or 0):
        errors.append("outreach approval_gap.checks_complete does not match acquisition plan")
    if approval_gap.get("checks_total") != (acquisition_gap.get("checks_total") or 0):
        errors.append("outreach approval_gap.checks_total does not match acquisition plan")
    if approval_gap.get("promotion_allowed_now") is not (
        acquisition_gap.get("promotion_allowed_now") is True
    ):
        errors.append("outreach approval_gap.promotion_allowed_now does not match acquisition plan")
    if approval_record and approval_gap.get("promotion_allowed_now") is not approval_record_is_promotable(approval_record):
        errors.append("outreach promotion_allowed_now does not match approval queue")

    permission = record.get("permission_request") or {}
    if permission.get("source_card_fallback_until_approved") is not True:
        errors.append("outreach permission request must keep source-card fallback until approved")
    if permission.get("candidate_direct_urls_omitted") is not True:
        errors.append("outreach permission request must omit candidate direct URLs")
    if permission.get("candidate_public_use") is not False:
        errors.append("outreach permission request candidate_public_use must be false")
    if permission.get("written_permission_required_before_reuse") is not True:
        errors.append("outreach permission request must require written permission before reuse")
    for key in ["requested_surfaces", "blocked_until_written_permission", "required_permission_fields"]:
        if not permission.get(key):
            errors.append(f"outreach permission request missing {key}")

    template = record.get("message_template") or {}
    if not template.get("subject"):
        errors.append("outreach message template missing subject")
    if not template.get("body_lines"):
        errors.append("outreach message template missing body_lines")

    handoff = record.get("handoff") or {}
    expected_pointers = {
        "approval_queue_record": f"content/media/species-media-approval-queue.yaml#{artifact_id}",
        "acquisition_plan_record": f"content/media/species-media-acquisition-plan.yaml#{artifact_id}",
        "public_explorer_record": f"content/media/species-media-public-explorer-manifest.yaml#{artifact_id}",
    }
    for key, expected in expected_pointers.items():
        if handoff.get(key) != expected:
            errors.append(f"outreach handoff.{key} does not match expected value")
    if public_record and handoff.get("public_explorer_record") != f"content/media/species-media-public-explorer-manifest.yaml#{artifact_id}":
        errors.append("outreach public explorer pointer is invalid")
    if not handoff.get("after_permission_next_step"):
        errors.append("outreach handoff missing after_permission_next_step")

    outreach_keys = collect_keys(record)
    for key in sorted(OUTREACH_BANNED_KEYS & outreach_keys):
        errors.append(f"outreach packet contains banned key {key!r}")
    outreach_strings = collect_strings(record)
    registry_candidate = ((registry_record.get("primary") or {}).get("candidate") or {})
    for key in ["image_url", "commons_file_page"]:
        candidate_url = registry_candidate.get(key)
        if candidate_url and candidate_url in outreach_strings:
            errors.append(f"outreach packet contains review-only candidate {key}")
    for outreach_string in outreach_strings:
        for banned in PUBLIC_EXPLORER_BANNED_STRINGS:
            if banned in outreach_string:
                errors.append(f"outreach packet contains banned public string {banned!r}")

    return errors


def validate_commons_snapshot_record(record, registry_by_id, approval_by_id):
    errors = []
    artifact_id = record.get("artifact_id")
    registry_record = registry_by_id.get(artifact_id)
    approval_record = approval_by_id.get(artifact_id)
    if not registry_record:
        errors.append("Commons rights snapshot record has no matching registry record")
        return errors
    if not approval_record:
        errors.append("Commons rights snapshot record has no matching approval queue record")
        return errors

    expected_ownership = f"{artifact_id}|{registry_record.get('species_page')}"
    if record.get("ownership_key") != expected_ownership:
        errors.append("Commons rights snapshot ownership_key does not match registry")
    if record.get("species_page") != registry_record.get("species_page"):
        errors.append("Commons rights snapshot species_page does not match registry")
    if record.get("snapshot_status") not in COMMONS_SNAPSHOT_STATUSES:
        errors.append(f"invalid Commons rights snapshot status {record.get('snapshot_status')!r}")

    registry_candidate = registry_candidate_lineage(registry_record)
    candidate = record.get("candidate") or {}
    for key in ["asset_id", "provider", "title", "commons_file_page", "image_url"]:
        if candidate.get(key) != registry_candidate.get(key):
            errors.append(f"Commons rights snapshot candidate.{key} does not match registry candidate")
    if candidate.get("registry_rights_status") != registry_candidate.get("rights_status"):
        errors.append("Commons rights snapshot registry_rights_status does not match registry candidate")
    if candidate.get("public_use") is not False:
        errors.append("Commons rights snapshot candidate.public_use must be false")
    if candidate.get("reviewer_only") is not True:
        errors.append("Commons rights snapshot candidate.reviewer_only must be true")

    if record.get("snapshot_status") == "fetched":
        api = record.get("commons_api") or {}
        if api.get("title") != registry_candidate.get("title"):
            errors.append("Commons API title does not match registry candidate")
        if api.get("descriptionurl") != registry_candidate.get("commons_file_page"):
            errors.append("Commons API descriptionurl does not match registry candidate")
        if api.get("direct_image_url") != registry_candidate.get("image_url"):
            errors.append("Commons API direct_image_url does not match registry candidate")
        for key in ["mime", "width", "height", "sha1", "timestamp"]:
            if not api.get(key):
                errors.append(f"Commons API snapshot missing {key}")

        alignment = record.get("registry_alignment") or {}
        expected_alignment = {
            "asset_id_matches": bool(registry_candidate.get("asset_id")),
            "title_matches": api.get("title") == registry_candidate.get("title"),
            "commons_file_page_matches": api.get("descriptionurl") == registry_candidate.get("commons_file_page"),
            "image_url_matches": api.get("direct_image_url") == registry_candidate.get("image_url"),
        }
        for key, expected in expected_alignment.items():
            if alignment.get(key) is not expected:
                errors.append(f"Commons rights snapshot registry_alignment.{key} is incorrect")

        rights = record.get("rights_evidence") or {}
        if rights.get("api_rights_status") not in CANDIDATE_RIGHTS:
            errors.append("Commons rights snapshot has invalid api_rights_status")
        if rights.get("registry_rights_status") != registry_candidate.get("rights_status"):
            errors.append("Commons rights snapshot rights.registry_rights_status does not match registry")
        if alignment.get("rights_status_matches_api") is not (
            rights.get("api_rights_status") == registry_candidate.get("rights_status")
        ):
            errors.append("Commons rights snapshot rights_status_matches_api is incorrect")
        for key in [
            "license_metadata_present",
            "creator_metadata_present",
            "credit_or_source_metadata_present",
            "reviewable_for_public_primary",
            "commercial_and_derivative_use_requires_human_review",
        ]:
            if not isinstance(rights.get(key), bool):
                errors.append(f"Commons rights snapshot rights_evidence.{key} must be boolean")

        species = record.get("species_match_evidence") or {}
        if not isinstance(species.get("automated_text_signal"), bool):
            errors.append("Commons rights snapshot species automated_text_signal must be boolean")
        if species.get("species_match_requires_human_review") is not True:
            errors.append("Commons rights snapshot must require human species-match review")

        ethics = record.get("ethics_location_evidence") or {}
        if sorted(ethics.get("registry_flags") or []) != sorted(registry_candidate.get("flags") or []):
            errors.append("Commons rights snapshot registry flags do not match registry candidate")
        if ethics.get("ethics_requires_human_review") is not True:
            errors.append("Commons rights snapshot must require human ethics review")
        if ethics.get("sensitive_location_requires_human_review") is not True:
            errors.append("Commons rights snapshot must require human sensitive-location review")

        approval = record.get("approval_support") or {}
        checks = approval_record.get("checks") or {}
        if approval.get("approval_queue_decision") != approval_record.get("decision"):
            errors.append("Commons rights snapshot approval decision does not match approval queue")
        if approval.get("checks_complete") != sum(1 for value in checks.values() if value is True):
            errors.append("Commons rights snapshot checks_complete does not match approval queue")
        if approval.get("checks_total") != len(checks):
            errors.append("Commons rights snapshot checks_total does not match approval queue")
        if approval.get("snapshot_is_not_approval") is not True:
            errors.append("Commons rights snapshot must mark snapshot_is_not_approval true")
    else:
        if not record.get("snapshot_errors"):
            errors.append("non-fetched Commons rights snapshot must include snapshot_errors")

    return errors


def expected_workbench_status(dossier_record, snapshot_record, acquisition_record, approval_record):
    if approval_record_is_promotable(approval_record):
        return "promotion_ready"
    dossier_record = dossier_record or {}
    snapshot_record = snapshot_record or {}
    acquisition_record = acquisition_record or {}
    candidate_flags = (dossier_record.get("candidate_evidence") or {}).get("flags") or []
    ethics = snapshot_record.get("ethics_location_evidence") or {}
    flags = set(candidate_flags + (ethics.get("api_text_flags") or []) + (ethics.get("registry_flags") or []))
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


def validate_approval_workbench_record(
    record,
    registry_by_id,
    approval_by_id,
    dossier_by_id,
    snapshot_by_id,
    acquisition_by_id,
    public_by_id,
    trace_by_id,
    outreach_by_id,
):
    errors = []
    artifact_id = record.get("artifact_id")
    registry_record = registry_by_id.get(artifact_id)
    approval_record = approval_by_id.get(artifact_id)
    dossier_record = dossier_by_id.get(artifact_id)
    snapshot_record = snapshot_by_id.get(artifact_id)
    acquisition_record = acquisition_by_id.get(artifact_id)
    public_record = public_by_id.get(artifact_id)
    trace_record = trace_by_id.get(artifact_id)
    outreach_record = outreach_by_id.get(artifact_id)
    if not registry_record:
        errors.append("approval workbench record has no matching registry record")
        return errors
    if not approval_record:
        errors.append("approval workbench record has no matching approval queue record")
        return errors
    if not dossier_record:
        errors.append("approval workbench record has no matching approval dossier record")
        return errors
    if not snapshot_record:
        errors.append("approval workbench record has no matching Commons snapshot record")
        return errors
    if not acquisition_record:
        errors.append("approval workbench record has no matching acquisition plan record")
        return errors
    if not public_record:
        errors.append("approval workbench record has no matching public explorer record")
        return errors

    expected_ownership = f"{artifact_id}|{registry_record.get('species_page')}"
    if record.get("ownership_key") != expected_ownership:
        errors.append("approval workbench ownership_key does not match registry")
    if record.get("species_page") != registry_record.get("species_page"):
        errors.append("approval workbench species_page does not match registry")
    if record.get("workbench_status") not in APPROVAL_WORKBENCH_STATUSES:
        errors.append(f"invalid approval workbench status {record.get('workbench_status')!r}")
    expected_status = expected_workbench_status(
        dossier_record,
        snapshot_record,
        acquisition_record,
        approval_record,
    )
    if record.get("workbench_status") != expected_status:
        errors.append("approval workbench status does not match source evidence")

    candidate = record.get("candidate_media") or {}
    queue_candidate = approval_record.get("candidate") or {}
    registry_candidate = registry_candidate_lineage(registry_record)
    dossier_candidate = dossier_record.get("candidate_evidence") or {}
    for key in [
        "asset_id",
        "provider",
        "title",
        "commons_file_page",
        "image_url",
        "creator",
        "credit",
        "license",
        "license_url",
        "rights_status",
    ]:
        if candidate.get(key) != queue_candidate.get(key):
            errors.append(f"approval workbench candidate_media.{key} does not match approval queue")
    if candidate.get("asset_id") != registry_candidate.get("asset_id"):
        errors.append("approval workbench candidate asset_id does not match registry")
    expected_flags = sorted(
        set(
            (dossier_candidate.get("flags") or [])
            + ((snapshot_record.get("ethics_location_evidence") or {}).get("api_text_flags") or [])
            + ((snapshot_record.get("ethics_location_evidence") or {}).get("registry_flags") or [])
        )
    )
    if sorted(candidate.get("flags") or []) != expected_flags:
        errors.append("approval workbench candidate flags do not match dossier plus Commons flags")
    if candidate.get("public_use") is not False:
        errors.append("approval workbench candidate public_use must be false")
    if candidate.get("reviewer_only") is not True:
        errors.append("approval workbench candidate reviewer_only must be true")

    snapshot = record.get("commons_snapshot") or {}
    snapshot_candidate = snapshot_record.get("candidate") or {}
    snapshot_rights = snapshot_record.get("rights_evidence") or {}
    snapshot_species = snapshot_record.get("species_match_evidence") or {}
    snapshot_ethics = snapshot_record.get("ethics_location_evidence") or {}
    if snapshot.get("snapshot_status") != snapshot_record.get("snapshot_status"):
        errors.append("approval workbench Commons snapshot_status does not match snapshots")
    if snapshot.get("asset_id") != snapshot_candidate.get("asset_id"):
        errors.append("approval workbench Commons snapshot asset_id does not match snapshots")
    if snapshot.get("api_rights_status") != snapshot_rights.get("api_rights_status"):
        errors.append("approval workbench API rights status does not match snapshots")
    if snapshot.get("registry_rights_status") != snapshot_rights.get("registry_rights_status"):
        errors.append("approval workbench registry rights status does not match snapshots")
    if snapshot.get("reviewable_for_public_primary") is not (
        snapshot_rights.get("reviewable_for_public_primary") is True
    ):
        errors.append("approval workbench reviewable_for_public_primary does not match snapshots")
    if snapshot.get("alignment") != (snapshot_record.get("registry_alignment") or {}):
        errors.append("approval workbench Commons alignment does not match snapshots")
    if snapshot.get("species_text_signal") is not (snapshot_species.get("automated_text_signal") is True):
        errors.append("approval workbench species text signal does not match snapshots")
    if sorted(snapshot.get("matched_terms") or []) != sorted(snapshot_species.get("matched_terms") or []):
        errors.append("approval workbench matched_terms do not match snapshots")
    if sorted(snapshot.get("api_text_flags") or []) != sorted(snapshot_ethics.get("api_text_flags") or []):
        errors.append("approval workbench api_text_flags do not match snapshots")
    if sorted(snapshot.get("registry_flags") or []) != sorted(snapshot_ethics.get("registry_flags") or []):
        errors.append("approval workbench registry_flags do not match snapshots")
    if snapshot.get("snapshot_is_not_approval") is not True:
        errors.append("approval workbench must mark snapshot_is_not_approval true")

    approval = record.get("approval_gate") or {}
    checks = approval_record.get("checks") or {}
    expected_missing_checks = sorted(key for key in APPROVAL_CHECKS if checks.get(key) is not True)
    approved = approval_record.get("approved_primary_template") or {}
    expected_missing_fields = sorted(
        key for key in APPROVAL_DOSSIER_REQUIRED_FIELDS if not approved.get(key)
    )
    if approval.get("decision") != approval_record.get("decision"):
        errors.append("approval workbench decision does not match approval queue")
    if approval.get("reviewer") != approval_record.get("reviewer"):
        errors.append("approval workbench reviewer does not match approval queue")
    if approval.get("reviewed_on") != approval_record.get("reviewed_on"):
        errors.append("approval workbench reviewed_on does not match approval queue")
    if approval.get("checks_complete") != sum(1 for key in APPROVAL_CHECKS if checks.get(key) is True):
        errors.append("approval workbench checks_complete does not match approval queue")
    if approval.get("checks_total") != len(APPROVAL_CHECKS):
        errors.append("approval workbench checks_total must match approval checklist")
    if sorted(approval.get("missing_checks") or []) != expected_missing_checks:
        errors.append("approval workbench missing_checks do not match approval queue")
    if sorted(approval.get("missing_approved_primary_fields") or []) != expected_missing_fields:
        errors.append("approval workbench missing approved-primary fields do not match approval queue")
    if approval.get("promotion_allowed_now") is not approval_record_is_promotable(approval_record):
        errors.append("approval workbench promotion_allowed_now does not match approval queue")
    if "approved_primary_template:" not in (approval.get("approval_yaml_snippet") or ""):
        errors.append("approval workbench missing approval YAML starter")

    required_evidence_checks = sorted(
        item.get("check") for item in (approval.get("required_evidence") or [])
    )
    if required_evidence_checks != expected_missing_checks:
        errors.append("approval workbench required_evidence does not match missing checks")

    boundary = record.get("public_boundary") or {}
    public_visual = public_record.get("public_visual") or {}
    public_rules = public_record.get("surface_rules") or {}
    acquisition_visual = acquisition_record.get("current_visual") or {}
    if boundary.get("current_visual_kind") != (public_visual.get("kind") or acquisition_visual.get("public_visual_kind")):
        errors.append("approval workbench public visual kind does not match public explorer/acquisition")
    if boundary.get("render_strategy") != (public_visual.get("render_strategy") or acquisition_visual.get("render_strategy")):
        errors.append("approval workbench render_strategy does not match public explorer/acquisition")
    if boundary.get("public_source_url") != (public_visual.get("source_url") or acquisition_visual.get("public_source_url")):
        errors.append("approval workbench public source URL does not match public explorer/acquisition")
    if boundary.get("public_source_domain") != (public_visual.get("domain") or acquisition_visual.get("public_source_domain")):
        errors.append("approval workbench public source domain does not match public explorer/acquisition")
    if boundary.get("source_card_does_not_authorize_image_copy") is not True:
        errors.append("approval workbench must mark source cards as no-copy/no-crop")
    expected_hero_allowed = (
        public_rules.get("species_page_hero_image_allowed") is True
        or acquisition_visual.get("hero_image_ready") is True
    )
    if boundary.get("species_page_hero_image_allowed") is not expected_hero_allowed:
        errors.append("approval workbench hero-image boundary does not match public explorer/acquisition")
    if boundary.get("candidate_thumbnail_allowed") is not (public_rules.get("candidate_thumbnail_allowed") is True):
        errors.append("approval workbench candidate thumbnail boundary does not match public explorer")
    if boundary.get("candidate_public_use") is not False:
        errors.append("approval workbench candidate_public_use must be false")

    acquisition = record.get("acquisition") or {}
    source_strategy = acquisition_record.get("source_strategy") or {}
    if acquisition.get("lane") != acquisition_record.get("acquisition_lane"):
        errors.append("approval workbench acquisition lane does not match acquisition plan")
    if acquisition.get("label") != acquisition_record.get("acquisition_label"):
        errors.append("approval workbench acquisition label does not match acquisition plan")
    if acquisition.get("target_source_family") != source_strategy.get("target_source_family"):
        errors.append("approval workbench target source family does not match acquisition plan")
    if acquisition.get("google_images_role") != "discovery_only":
        errors.append("approval workbench Google Images role must be discovery_only")
    if acquisition.get("partner_media_grant_needed") is not (
        source_strategy.get("partner_media_grant_needed") is True
    ):
        errors.append("approval workbench partner media grant flag does not match acquisition plan")
    if sorted(acquisition.get("outreach_targets") or []) != sorted(source_strategy.get("outreach_targets") or []):
        errors.append("approval workbench outreach targets do not match acquisition plan")

    outreach = record.get("outreach") or {}
    if outreach_record:
        if outreach.get("request_type") != outreach_record.get("request_type"):
            errors.append("approval workbench outreach request_type does not match outreach packet")
        if outreach.get("request_label") != outreach_record.get("request_label"):
            errors.append("approval workbench outreach request_label does not match outreach packet")
        if outreach.get("outreach_status") != outreach_record.get("outreach_status"):
            errors.append("approval workbench outreach_status does not match outreach packet")
        permission = outreach_record.get("permission_request") or {}
        if outreach.get("source_card_fallback_until_approved") is not (
            permission.get("source_card_fallback_until_approved") is True
        ):
            errors.append("approval workbench outreach source-card fallback flag does not match outreach packet")
        if outreach.get("written_permission_required_before_reuse") is not (
            permission.get("written_permission_required_before_reuse") is True
        ):
            errors.append("approval workbench written permission flag does not match outreach packet")

    trace = record.get("trace") or {}
    if trace_record:
        if trace.get("trace_state") != trace_record.get("trace_state"):
            errors.append("approval workbench trace_state does not match trace ledger")
        if trace.get("trace_issues") != (trace_record.get("trace_issues") or []):
            errors.append("approval workbench trace_issues do not match trace ledger")

    actions = record.get("reviewer_actions") or {}
    expected_pointers = {
        "dry_run_command": f"python scripts/promote_species_media.py --artifact-id {artifact_id}",
        "apply_command_after_clean_dry_run": f"python scripts/promote_species_media.py --artifact-id {artifact_id} --apply",
        "open_approval_queue_record": f"content/media/species-media-approval-queue.yaml#{artifact_id}",
        "open_dossier_record": f"content/media/species-media-approval-dossiers.yaml#{artifact_id}",
        "open_commons_snapshot_record": f"content/media/species-media-commons-rights-snapshots.yaml#{artifact_id}",
        "open_trace_record": f"content/media/species-media-trace-ledger.yaml#{artifact_id}",
    }
    for key, expected in expected_pointers.items():
        if actions.get(key) != expected:
            errors.append(f"approval workbench reviewer_actions.{key} does not match expected value")
    if not actions.get("primary_next_action"):
        errors.append("approval workbench missing primary_next_action")

    safety = record.get("safety_controls") or {}
    if safety.get("reviewer_only") is not True:
        errors.append("approval workbench safety_controls.reviewer_only must be true")
    if safety.get("contains_review_candidate_urls") is not True:
        errors.append("approval workbench safety_controls.contains_review_candidate_urls must be true")
    if safety.get("not_public_site_input") is not True:
        errors.append("approval workbench safety_controls.not_public_site_input must be true")
    if safety.get("candidate_public_use") is not False:
        errors.append("approval workbench safety_controls.candidate_public_use must be false")
    if safety.get("source_card_no_copy_or_crop") is not True:
        errors.append("approval workbench safety_controls.source_card_no_copy_or_crop must be true")
    if safety.get("approved_primary_required_for_hero_image") is not True:
        errors.append("approval workbench must require approved primary before hero image")
    if safety.get("human_review_required_for_rights_species_ethics_crop_alt_text") is not True:
        errors.append("approval workbench must require human review for rights/species/ethics/crop/alt text")

    return errors


def validate_curation_workspace_record(record, registry_by_id, approval_by_id):
    errors = []
    artifact_id = record.get("artifact_id")
    registry_record = registry_by_id.get(artifact_id)
    if not registry_record:
        errors.append("curation workspace record has no matching registry record")
        return errors
    if record.get("species_page") != registry_record.get("species_page"):
        errors.append("curation workspace species_page does not match registry")

    batch = record.get("recommended_batch")
    if batch not in CURATION_BATCHES:
        errors.append(f"invalid recommended_batch {batch!r}")
    if record.get("workstream") not in CURATION_WORKSTREAMS:
        errors.append(f"invalid workstream {record.get('workstream')!r}")

    candidate = record.get("candidate") or {}
    registry_candidate = ((registry_record.get("primary") or {}).get("candidate") or {})
    if candidate.get("asset_id") != registry_candidate.get("asset_id"):
        errors.append("curation workspace candidate asset_id does not match registry candidate")
    if candidate.get("public_use") is not False:
        errors.append("curation workspace candidate.public_use must be false")

    approval_state = record.get("approval_state") or {}
    promotion_allowed = approval_state.get("promotion_allowed_now")
    if not isinstance(promotion_allowed, bool):
        errors.append("approval_state.promotion_allowed_now must be boolean")
    expected_promotion_allowed = approval_record_is_promotable(approval_by_id.get(artifact_id))
    if promotion_allowed is not expected_promotion_allowed:
        errors.append("approval_state.promotion_allowed_now does not match approval queue")

    public_visual = record.get("public_visual") or {}
    public_visual_strings = collect_strings(public_visual)
    for key in ["image_url", "commons_file_page"]:
        candidate_url = registry_candidate.get(key)
        if candidate_url and candidate_url in public_visual_strings:
            errors.append(f"curation public_visual contains review-only candidate {key}")

    source_route = record.get("source_route")
    flags = candidate.get("flags") or []
    source_card = record.get("source_card_fallback") or {}
    rights = candidate.get("rights_status")
    if batch == "01_source_card_recheck" and source_card.get("status") != "needs_browser_recheck":
        errors.append("source-card recheck batch requires source_card_fallback.status: needs_browser_recheck")
    if batch == "02_ethics_flag_review" and not flags:
        errors.append("ethics flag batch requires candidate flags")
    if batch == "03_official_public_domain_fast_track" and source_route != "official_public_domain_fast_track":
        errors.append("official/public-domain fast-track batch requires matching source_route")
    if batch == "04_open_public_domain_review" and source_route != "open_public_domain_review" and rights != "public-domain-or-cc0-candidate":
        errors.append("open public-domain batch requires open public-domain route or public-domain candidate rights")
    if batch == "05_open_license_attribution" and source_route != "open_license_attribution_review":
        errors.append("open-license attribution batch requires matching source_route")

    if not record.get("blockers"):
        errors.append("curation workspace record missing blockers")
    if not record.get("next_curator_action"):
        errors.append("curation workspace record missing next_curator_action")
    return errors


def main():
    if not REGISTRY_PATH.exists():
        print(f"ERROR missing registry: {REGISTRY_PATH.relative_to(ROOT)}")
        return 1

    pages = species_pages()
    registry = yaml.safe_load(REGISTRY_PATH.read_text(encoding="utf-8")) or {}
    records = registry.get("records") or []
    registry_by_id = {record.get("artifact_id"): record for record in records}
    source_profiles = registry.get("source_profiles") or {}

    errors = []
    warnings = []
    seen_paths = set()
    seen_ids = set()

    for i, record in enumerate(records, start=1):
        label = record.get("artifact_id") or f"record {i}"
        path = record.get("species_page")
        artifact_id = record.get("artifact_id")

        if not path:
            errors.append(f"{label}: missing species_page")
            continue
        if path in seen_paths:
            errors.append(f"{label}: duplicate species_page {path}")
        seen_paths.add(path)

        if not artifact_id:
            errors.append(f"{path}: missing artifact_id")
        elif artifact_id in seen_ids:
            errors.append(f"{path}: duplicate artifact_id {artifact_id}")
        seen_ids.add(artifact_id)

        if path not in pages:
            errors.append(f"{label}: registry path is not a current species page: {path}")
            continue

        page_id = pages[path].get("id")
        if page_id != artifact_id:
            errors.append(f"{path}: artifact_id {artifact_id!r} does not match page id {page_id!r}")

        if record.get("media_status") not in MEDIA_STATUSES:
            errors.append(f"{path}: invalid media_status {record.get('media_status')!r}")

        primary = record.get("primary") or {}
        if primary.get("status") not in PRIMARY_STATUSES:
            errors.append(f"{path}: invalid primary.status {primary.get('status')!r}")

        candidates = record.get("source_candidates") or {}
        for ref_group in ["official_or_institutional_refs", "open_license_refs", "partner_refs"]:
            for ref in candidates.get(ref_group) or []:
                if ref not in source_profiles:
                    errors.append(f"{path}: source ref {ref!r} in {ref_group} is not defined in source_profiles")
        if not candidates.get("open_license_refs"):
            errors.append(f"{path}: missing open_license_refs")
        if not candidates.get("official_or_institutional_refs") and not candidates.get("partner_refs"):
            warnings.append(f"{path}: no official/institutional or partner refs listed")

        rich_embed = record.get("rich_embed") or {}
        if rich_embed.get("status") == "candidate" and not rich_embed.get("preferred_source_url"):
            warnings.append(f"{path}: rich_embed candidate has no preferred_source_url")

        for asset in record.get("current_supporting_assets") or []:
            asset_path = asset.get("path")
            if asset_path and not (ROOT / asset_path).exists():
                errors.append(f"{path}: supporting asset does not exist: {asset_path}")
            if asset.get("role", "").startswith("generated") and not asset.get("use_limitations"):
                errors.append(f"{path}: generated supporting asset missing use_limitations")

        for primary_error in validate_approved_primary(record):
            errors.append(f"{path}: {primary_error}")
        for candidate_error in validate_candidate_primary(record):
            errors.append(f"{path}: {candidate_error}")

    missing = sorted(set(pages) - seen_paths)
    for path in missing:
        errors.append(f"missing species media registry record for {path}")

    extras = sorted(seen_paths - set(pages))
    for path in extras:
        errors.append(f"stale species media registry record for {path}")

    if SOURCE_ROUTING_PATH.exists():
        source_routing = yaml.safe_load(SOURCE_ROUTING_PATH.read_text(encoding="utf-8")) or {}
        routed_ids = {record.get("artifact_id") for record in source_routing.get("records") or []}
        registry_ids = {record.get("artifact_id") for record in records}
        for artifact_id in sorted(registry_ids - routed_ids):
            errors.append(f"source routing missing artifact_id {artifact_id}")
        for artifact_id in sorted(routed_ids - registry_ids):
            errors.append(f"source routing has stale artifact_id {artifact_id}")

    if RICH_EMBEDS_PATH.exists():
        rich_embeds = yaml.safe_load(RICH_EMBEDS_PATH.read_text(encoding="utf-8")) or {}
        rich_records = rich_embeds.get("records") or []
        rich_records_by_id = {record.get("artifact_id"): record for record in rich_records}
        rich_ids = {record.get("artifact_id") for record in rich_records}
        registry_ids = {record.get("artifact_id") for record in records}
        for artifact_id in sorted(registry_ids - rich_ids):
            errors.append(f"rich embed fallback missing artifact_id {artifact_id}")
        for artifact_id in sorted(rich_ids - registry_ids):
            errors.append(f"rich embed fallback has stale artifact_id {artifact_id}")
        pages_by_id = {record.get("artifact_id"): record.get("species_page") for record in records}
        for record in rich_records:
            label = record.get("artifact_id") or "rich embed record"
            if pages_by_id.get(record.get("artifact_id")) != record.get("species_page"):
                errors.append(f"{label}: rich embed species_page does not match registry")
            for source_card_error in validate_source_card(record):
                errors.append(f"{label}: {source_card_error}")

    approval_records_by_id = {}
    if APPROVAL_QUEUE_PATH.exists():
        approval_queue = yaml.safe_load(APPROVAL_QUEUE_PATH.read_text(encoding="utf-8")) or {}
        approval_records = approval_queue.get("records") or []
        approval_records_by_id = {record.get("artifact_id"): record for record in approval_records}
        approval_ids = {record.get("artifact_id") for record in approval_records}
        registry_ids = set(registry_by_id)
        for artifact_id in sorted(registry_ids - approval_ids):
            errors.append(f"approval queue missing artifact_id {artifact_id}")
        for artifact_id in sorted(approval_ids - registry_ids):
            errors.append(f"approval queue has stale artifact_id {artifact_id}")
        for record in approval_records:
            label = record.get("artifact_id") or "approval queue record"
            for approval_error in validate_approval_queue_record(record, registry_by_id):
                errors.append(f"{label}: {approval_error}")

    render_records_by_id = {}
    if RENDER_CONTRACT_PATH.exists():
        render_contract = yaml.safe_load(RENDER_CONTRACT_PATH.read_text(encoding="utf-8")) or {}
        render_records = render_contract.get("records") or []
        render_records_by_id = {record.get("artifact_id"): record for record in render_records}
        render_ids = {record.get("artifact_id") for record in render_records}
        registry_ids = set(registry_by_id)
        rich_records_by_id = {}
        if RICH_EMBEDS_PATH.exists():
            rich_payload = yaml.safe_load(RICH_EMBEDS_PATH.read_text(encoding="utf-8")) or {}
            rich_records_by_id = {
                record.get("artifact_id"): record for record in rich_payload.get("records") or []
            }
        for artifact_id in sorted(registry_ids - render_ids):
            errors.append(f"render contract missing artifact_id {artifact_id}")
        for artifact_id in sorted(render_ids - registry_ids):
            errors.append(f"render contract has stale artifact_id {artifact_id}")
        for record in render_records:
            label = record.get("artifact_id") or "render contract record"
            for render_error in validate_render_contract_record(record, registry_by_id, rich_records_by_id):
                errors.append(f"{label}: {render_error}")

    workspace_records_by_id = {}
    if CURATION_WORKSPACE_PATH.exists():
        workspace = yaml.safe_load(CURATION_WORKSPACE_PATH.read_text(encoding="utf-8")) or {}
        policy = workspace.get("policy") or {}
        if policy.get("workspace_is_not_approval") is not True:
            errors.append("curation workspace policy.workspace_is_not_approval must be true")
        if policy.get("candidate_public_use") is not False:
            errors.append("curation workspace policy.candidate_public_use must be false")
        workspace_records = workspace.get("records") or []
        workspace_records_by_id = {record.get("artifact_id"): record for record in workspace_records}
        workspace_ids = {record.get("artifact_id") for record in workspace_records}
        registry_ids = set(registry_by_id)
        for artifact_id in sorted(registry_ids - workspace_ids):
            errors.append(f"curation workspace missing artifact_id {artifact_id}")
        for artifact_id in sorted(workspace_ids - registry_ids):
            errors.append(f"curation workspace has stale artifact_id {artifact_id}")
        for record in workspace_records:
            label = record.get("artifact_id") or "curation workspace record"
            for workspace_error in validate_curation_workspace_record(record, registry_by_id, approval_records_by_id):
                errors.append(f"{label}: {workspace_error}")

    acquisition_plan_payload = {}
    acquisition_records_by_id = {}
    if ACQUISITION_PLAN_PATH.exists():
        acquisition_plan_payload = yaml.safe_load(ACQUISITION_PLAN_PATH.read_text(encoding="utf-8")) or {}
        acquisition_records_by_id = {
            record.get("artifact_id"): record for record in acquisition_plan_payload.get("records") or []
        }

    public_records_by_id = {}
    if PUBLIC_EXPLORER_MANIFEST_PATH.exists():
        public_manifest = yaml.safe_load(PUBLIC_EXPLORER_MANIFEST_PATH.read_text(encoding="utf-8")) or {}
        policy = public_manifest.get("policy") or {}
        if policy.get("public_manifest_omits_candidate_urls") is not True:
            errors.append("public explorer policy.public_manifest_omits_candidate_urls must be true")
        if policy.get("public_manifest_omits_candidate_file_pages") is not True:
            errors.append("public explorer policy.public_manifest_omits_candidate_file_pages must be true")
        if policy.get("candidate_public_use") is not False:
            errors.append("public explorer policy.candidate_public_use must be false")
        if policy.get("source_card_does_not_authorize_image_copy") is not True:
            errors.append("public explorer policy.source_card_does_not_authorize_image_copy must be true")
        if policy.get("google_images_discovery_only") is not True:
            errors.append("public explorer policy.google_images_discovery_only must be true")
        if policy.get("partner_grants_require_written_permission") is not True:
            errors.append("public explorer policy.partner_grants_require_written_permission must be true")

        public_records = public_manifest.get("records") or []
        public_records_by_id = {record.get("artifact_id"): record for record in public_records}
        public_ids = {record.get("artifact_id") for record in public_records}
        registry_ids = set(registry_by_id)
        for artifact_id in sorted(registry_ids - public_ids):
            errors.append(f"public explorer missing artifact_id {artifact_id}")
        for artifact_id in sorted(public_ids - registry_ids):
            errors.append(f"public explorer has stale artifact_id {artifact_id}")

        summary = public_manifest.get("summary") or {}
        if summary.get("species_records") != len(public_records):
            errors.append("public explorer summary.species_records does not match record count")
        if summary.get("species_records") != len(records):
            errors.append("public explorer summary.species_records does not match registry count")
        if summary.get("candidate_public_use_blocked") != len(records):
            errors.append("public explorer must report every candidate as blocked from public use")
        expected_public_ready = sum(
            1
            for record in render_records_by_id.values()
            if ((record.get("public_visual") or {}).get("public_use") is True)
        )
        expected_hero_ready = sum(
            1
            for record in render_records_by_id.values()
            if ((record.get("surface_rules") or {}).get("species_page_hero_image_allowed") is True)
        )
        if summary.get("public_visual_ready") != expected_public_ready:
            errors.append("public explorer summary.public_visual_ready does not match render contract")
        if summary.get("hero_image_ready") != expected_hero_ready:
            errors.append("public explorer summary.hero_image_ready does not match render contract")
        if acquisition_records_by_id:
            expected_approved_primary_needed = sum(
                1
                for record in acquisition_records_by_id.values()
                if ((record.get("current_visual") or {}).get("hero_image_ready") is not True)
            )
            expected_lanes = Counter(
                record.get("acquisition_lane") or "none" for record in acquisition_records_by_id.values()
            )
            expected_families = Counter(
                (record.get("source_strategy") or {}).get("target_source_family") or "none"
                for record in acquisition_records_by_id.values()
            )
            expected_priorities = Counter(
                record.get("priority") or "none" for record in acquisition_records_by_id.values()
            )
            if summary.get("approved_primary_needed") != expected_approved_primary_needed:
                errors.append("public explorer summary.approved_primary_needed does not match acquisition plan")
            if summary.get("acquisition_lane_counts") != dict(sorted(expected_lanes.items())):
                errors.append("public explorer summary.acquisition_lane_counts does not match acquisition plan")
            if summary.get("target_source_family_counts") != dict(sorted(expected_families.items())):
                errors.append("public explorer summary.target_source_family_counts does not match acquisition plan")
            if summary.get("priority_counts") != dict(sorted(expected_priorities.items())):
                errors.append("public explorer summary.priority_counts does not match acquisition plan")

        public_keys = collect_keys(public_manifest)
        for key in sorted(PUBLIC_EXPLORER_BANNED_KEYS & public_keys):
            errors.append(f"public explorer manifest contains banned key {key!r}")
        for public_string in collect_strings(public_manifest):
            for banned in PUBLIC_EXPLORER_BANNED_STRINGS:
                if banned in public_string:
                    errors.append(f"public explorer manifest contains banned public string {banned!r}")

        for record in public_records:
            label = record.get("artifact_id") or "public explorer record"
            for explorer_error in validate_public_explorer_record(
                record,
                registry_by_id,
                render_records_by_id,
                acquisition_records_by_id if ACQUISITION_PLAN_PATH.exists() else None,
            ):
                errors.append(f"{label}: {explorer_error}")

    if RENDER_CONTRACT_PATH.exists() and PUBLIC_EXPLORER_MANIFEST_PATH.exists():
        for record in records:
            artifact_id = record.get("artifact_id")
            path = record.get("species_page")
            page_fm = pages.get(path) or {}
            for media_error in validate_species_page_media(
                record,
                page_fm,
                render_records_by_id,
                public_records_by_id,
            ):
                errors.append(f"{artifact_id}: {media_error}")

    trace_records_by_id = {}
    if TRACE_LEDGER_PATH.exists():
        trace_ledger = yaml.safe_load(TRACE_LEDGER_PATH.read_text(encoding="utf-8")) or {}
        policy = trace_ledger.get("policy") or {}
        if policy.get("ledger_omits_candidate_direct_urls") is not True:
            errors.append("trace ledger policy.ledger_omits_candidate_direct_urls must be true")
        if policy.get("candidate_public_use") is not False:
            errors.append("trace ledger policy.candidate_public_use must be false")

        trace_records = trace_ledger.get("records") or []
        trace_records_by_id = {record.get("artifact_id"): record for record in trace_records}
        trace_ids = {record.get("artifact_id") for record in trace_records}
        registry_ids = set(registry_by_id)
        for artifact_id in sorted(registry_ids - trace_ids):
            errors.append(f"trace ledger missing artifact_id {artifact_id}")
        for artifact_id in sorted(trace_ids - registry_ids):
            errors.append(f"trace ledger has stale artifact_id {artifact_id}")

        summary = trace_ledger.get("summary") or {}
        if summary.get("species_records") != len(trace_records):
            errors.append("trace ledger summary.species_records does not match record count")
        if summary.get("species_records") != len(records):
            errors.append("trace ledger summary.species_records does not match registry count")
        if summary.get("trace_issue_count") != 0:
            errors.append("trace ledger summary.trace_issue_count must be 0")
        expected_public_ready = sum(
            1
            for record in render_records_by_id.values()
            if ((record.get("public_visual") or {}).get("public_use") is True)
        )
        expected_hero_ready = sum(
            1
            for record in render_records_by_id.values()
            if ((record.get("surface_rules") or {}).get("species_page_hero_image_allowed") is True)
        )
        if summary.get("public_visual_ready") != expected_public_ready:
            errors.append("trace ledger summary.public_visual_ready does not match render contract")
        if summary.get("hero_image_ready") != expected_hero_ready:
            errors.append("trace ledger summary.hero_image_ready does not match render contract")
        if summary.get("candidate_public_use_blocked") != len(records):
            errors.append("trace ledger must report every candidate as blocked from public use")

        trace_keys = collect_keys(trace_ledger)
        for key in sorted(TRACE_LEDGER_BANNED_KEYS & trace_keys):
            errors.append(f"trace ledger contains banned key {key!r}")
        for trace_string in collect_strings(trace_ledger):
            for banned in PUBLIC_EXPLORER_BANNED_STRINGS:
                if banned in trace_string:
                    errors.append(f"trace ledger contains banned public string {banned!r}")

        for record in trace_records:
            label = record.get("artifact_id") or "trace ledger record"
            for trace_error in validate_trace_ledger_record(
                record,
                registry_by_id,
                render_records_by_id,
                public_records_by_id,
            ):
                errors.append(f"{label}: {trace_error}")

    if ACQUISITION_PLAN_PATH.exists():
        acquisition_plan = acquisition_plan_payload
        policy = acquisition_plan.get("policy") or {}
        if policy.get("acquisition_plan_is_not_approval") is not True:
            errors.append("acquisition plan policy.acquisition_plan_is_not_approval must be true")
        if policy.get("public_safe") is not True:
            errors.append("acquisition plan policy.public_safe must be true")
        if policy.get("candidate_direct_urls_omitted") is not True:
            errors.append("acquisition plan policy.candidate_direct_urls_omitted must be true")
        if policy.get("candidate_public_use") is not False:
            errors.append("acquisition plan policy.candidate_public_use must be false")
        if policy.get("approved_primary_required_for_hero_image") is not True:
            errors.append("acquisition plan must require approved primary before hero image")
        if policy.get("source_card_does_not_authorize_image_copy") is not True:
            errors.append("acquisition plan must mark source cards as no-copy/no-crop")
        if policy.get("google_images_discovery_only") is not True:
            errors.append("acquisition plan policy.google_images_discovery_only must be true")
        if policy.get("partner_grants_require_written_permission") is not True:
            errors.append("acquisition plan policy.partner_grants_require_written_permission must be true")

        acquisition_records = acquisition_plan.get("records") or []
        acquisition_ids = {record.get("artifact_id") for record in acquisition_records}
        registry_ids = set(registry_by_id)
        for artifact_id in sorted(registry_ids - acquisition_ids):
            errors.append(f"acquisition plan missing artifact_id {artifact_id}")
        for artifact_id in sorted(acquisition_ids - registry_ids):
            errors.append(f"acquisition plan has stale artifact_id {artifact_id}")

        summary = acquisition_plan.get("summary") or {}
        if summary.get("species_records") != len(acquisition_records):
            errors.append("acquisition plan summary.species_records does not match record count")
        if summary.get("species_records") != len(records):
            errors.append("acquisition plan summary.species_records does not match registry count")
        expected_public_ready = sum(
            1
            for record in render_records_by_id.values()
            if ((record.get("public_visual") or {}).get("public_use") is True)
        )
        expected_hero_ready = sum(
            1
            for record in render_records_by_id.values()
            if ((record.get("surface_rules") or {}).get("species_page_hero_image_allowed") is True)
        )
        if summary.get("public_visual_ready") != expected_public_ready:
            errors.append("acquisition plan summary.public_visual_ready does not match render contract")
        if summary.get("hero_image_ready") != expected_hero_ready:
            errors.append("acquisition plan summary.hero_image_ready does not match render contract")
        if summary.get("approved_primary_needed") != len(records) - expected_hero_ready:
            errors.append("acquisition plan summary.approved_primary_needed does not match render contract")
        if summary.get("candidate_public_use_blocked") != len(records):
            errors.append("acquisition plan must report every candidate as blocked from public use")
        expected_promotion_ready = sorted(
            artifact_id
            for artifact_id, record in approval_records_by_id.items()
            if approval_record_is_promotable(record)
        )
        if sorted(summary.get("promotion_ready_artifact_ids") or []) != expected_promotion_ready:
            errors.append("acquisition plan promotion_ready_artifact_ids do not match approval queue")
        if summary.get("promotion_ready_count") != len(expected_promotion_ready):
            errors.append("acquisition plan promotion_ready_count does not match approval queue")

        acquisition_keys = collect_keys(acquisition_plan)
        for key in sorted(ACQUISITION_PLAN_BANNED_KEYS & acquisition_keys):
            errors.append(f"acquisition plan contains banned key {key!r}")
        for acquisition_string in collect_strings(acquisition_plan):
            for banned in PUBLIC_EXPLORER_BANNED_STRINGS:
                if banned in acquisition_string:
                    errors.append(f"acquisition plan contains banned public string {banned!r}")

        for record in acquisition_records:
            label = record.get("artifact_id") or "acquisition plan record"
            for acquisition_error in validate_acquisition_plan_record(
                record,
                registry_by_id,
                render_records_by_id,
                approval_records_by_id,
                trace_records_by_id,
            ):
                errors.append(f"{label}: {acquisition_error}")

    dossier_records_by_id = {}
    if APPROVAL_DOSSIERS_PATH.exists():
        dossiers = yaml.safe_load(APPROVAL_DOSSIERS_PATH.read_text(encoding="utf-8")) or {}
        policy = dossiers.get("policy") or {}
        if policy.get("reviewer_only") is not True:
            errors.append("approval dossiers policy.reviewer_only must be true")
        if policy.get("contains_review_candidate_urls") is not True:
            errors.append("approval dossiers policy.contains_review_candidate_urls must be true")
        if policy.get("not_public_site_input") is not True:
            errors.append("approval dossiers policy.not_public_site_input must be true")
        if policy.get("candidate_public_use") is not False:
            errors.append("approval dossiers policy.candidate_public_use must be false")
        if policy.get("source_card_does_not_authorize_image_copy") is not True:
            errors.append("approval dossiers must mark source cards as no-copy/no-crop")
        if policy.get("promotion_requires_approval_queue") is not True:
            errors.append("approval dossiers policy.promotion_requires_approval_queue must be true")
        if policy.get("dry_run_before_apply") is not True:
            errors.append("approval dossiers policy.dry_run_before_apply must be true")

        dossier_records = dossiers.get("records") or []
        dossier_records_by_id = {record.get("artifact_id"): record for record in dossier_records}
        dossier_ids = {record.get("artifact_id") for record in dossier_records}
        registry_ids = set(registry_by_id)
        for artifact_id in sorted(registry_ids - dossier_ids):
            errors.append(f"approval dossiers missing artifact_id {artifact_id}")
        for artifact_id in sorted(dossier_ids - registry_ids):
            errors.append(f"approval dossiers has stale artifact_id {artifact_id}")

        summary = dossiers.get("summary") or {}
        if summary.get("species_records") != len(dossier_records):
            errors.append("approval dossiers summary.species_records does not match record count")
        if summary.get("species_records") != len(records):
            errors.append("approval dossiers summary.species_records does not match registry count")
        expected_promotion_ready = sorted(
            artifact_id
            for artifact_id, record in approval_records_by_id.items()
            if approval_record_is_promotable(record)
        )
        if sorted(summary.get("promotion_ready_artifact_ids") or []) != expected_promotion_ready:
            errors.append("approval dossiers promotion_ready_artifact_ids do not match approval queue")
        if summary.get("promotion_ready_count") != len(expected_promotion_ready):
            errors.append("approval dossiers promotion_ready_count does not match approval queue")
        expected_statuses = Counter(
            record.get("dossier_status") or "none" for record in dossier_records
        )
        expected_lanes = Counter(
            (record.get("acquisition") or {}).get("lane") or "none" for record in dossier_records
        )
        expected_priorities = Counter(record.get("priority") or "none" for record in dossier_records)
        expected_missing_checks = Counter(
            check
            for record in dossier_records
            for check in ((record.get("approval_gap") or {}).get("missing_checks") or [])
        )
        expected_missing_fields = Counter(
            field
            for record in dossier_records
            for field in ((record.get("approval_gap") or {}).get("missing_approved_primary_fields") or [])
        )
        if summary.get("dossier_status_counts") != dict(sorted(expected_statuses.items())):
            errors.append("approval dossiers summary.dossier_status_counts does not match records")
        if summary.get("acquisition_lane_counts") != dict(sorted(expected_lanes.items())):
            errors.append("approval dossiers summary.acquisition_lane_counts does not match records")
        if summary.get("priority_counts") != dict(sorted(expected_priorities.items())):
            errors.append("approval dossiers summary.priority_counts does not match records")
        if summary.get("missing_check_counts") != dict(sorted(expected_missing_checks.items())):
            errors.append("approval dossiers summary.missing_check_counts does not match records")
        if summary.get("missing_approved_primary_field_counts") != dict(sorted(expected_missing_fields.items())):
            errors.append("approval dossiers summary.missing_approved_primary_field_counts does not match records")
        expected_flagged = sorted(
            artifact_id
            for artifact_id, record in dossier_records_by_id.items()
            if (record.get("candidate_evidence") or {}).get("flags")
        )
        if sorted(summary.get("flagged_candidate_records") or []) != expected_flagged:
            errors.append("approval dossiers flagged_candidate_records do not match records")

        for record in dossier_records:
            label = record.get("artifact_id") or "approval dossier record"
            for dossier_error in validate_approval_dossier_record(
                record,
                registry_by_id,
                approval_records_by_id,
                acquisition_records_by_id,
                public_records_by_id,
                trace_records_by_id,
                workspace_records_by_id,
            ):
                errors.append(f"{label}: {dossier_error}")

    outreach_records_by_id = {}
    if OUTREACH_PACKETS_PATH.exists():
        outreach = yaml.safe_load(OUTREACH_PACKETS_PATH.read_text(encoding="utf-8")) or {}
        policy = outreach.get("policy") or {}
        if policy.get("outreach_is_not_approval") is not True:
            errors.append("outreach packets policy.outreach_is_not_approval must be true")
        if policy.get("public_safe") is not True:
            errors.append("outreach packets policy.public_safe must be true")
        if policy.get("candidate_direct_urls_omitted") is not True:
            errors.append("outreach packets policy.candidate_direct_urls_omitted must be true")
        if policy.get("candidate_public_use") is not False:
            errors.append("outreach packets policy.candidate_public_use must be false")
        if policy.get("source_card_does_not_authorize_image_copy") is not True:
            errors.append("outreach packets must mark source cards as no-copy/no-crop")
        if policy.get("google_images_discovery_only") is not True:
            errors.append("outreach packets policy.google_images_discovery_only must be true")
        if policy.get("written_permission_required_before_reuse") is not True:
            errors.append("outreach packets policy.written_permission_required_before_reuse must be true")
        if policy.get("do_not_infer_private_contact_details") is not True:
            errors.append("outreach packets policy.do_not_infer_private_contact_details must be true")
        if policy.get("no_scraping_or_bulk_download") is not True:
            errors.append("outreach packets policy.no_scraping_or_bulk_download must be true")

        outreach_records = outreach.get("records") or []
        outreach_records_by_id = {record.get("artifact_id"): record for record in outreach_records}
        outreach_ids = {record.get("artifact_id") for record in outreach_records}
        registry_ids = set(registry_by_id)
        for artifact_id in sorted(registry_ids - outreach_ids):
            errors.append(f"outreach packets missing artifact_id {artifact_id}")
        for artifact_id in sorted(outreach_ids - registry_ids):
            errors.append(f"outreach packets has stale artifact_id {artifact_id}")

        target_packets = outreach.get("target_packets") or []
        summary = outreach.get("summary") or {}
        if summary.get("species_records") != len(outreach_records):
            errors.append("outreach packets summary.species_records does not match record count")
        if summary.get("species_records") != len(records):
            errors.append("outreach packets summary.species_records does not match registry count")
        if summary.get("outreach_target_count") != len(target_packets):
            errors.append("outreach packets summary.outreach_target_count does not match target packet count")
        expected_request_total = sum(packet.get("request_count") or 0 for packet in target_packets)
        if summary.get("outreach_request_count") != expected_request_total:
            errors.append("outreach packets summary.outreach_request_count does not match target packets")
        expected_needed = sum(
            1
            for record in outreach_records
            if ((record.get("approval_gap") or {}).get("promotion_allowed_now") is not True)
        )
        if summary.get("approved_primary_needed") != expected_needed:
            errors.append("outreach packets approved_primary_needed does not match records")
        expected_requests = Counter(record.get("request_type") or "none" for record in outreach_records)
        expected_statuses = Counter(record.get("outreach_status") or "none" for record in outreach_records)
        expected_lanes = Counter((record.get("acquisition") or {}).get("lane") or "none" for record in outreach_records)
        expected_families = Counter(
            (record.get("acquisition") or {}).get("target_source_family") or "none"
            for record in outreach_records
        )
        expected_priorities = Counter(record.get("priority") or "none" for record in outreach_records)
        expected_domains = Counter(
            (record.get("current_public_source") or {}).get("domain") or "none" for record in outreach_records
        )
        if summary.get("request_type_counts") != dict(sorted(expected_requests.items())):
            errors.append("outreach packets request_type_counts do not match records")
        if summary.get("outreach_status_counts") != dict(sorted(expected_statuses.items())):
            errors.append("outreach packets outreach_status_counts do not match records")
        if summary.get("acquisition_lane_counts") != dict(sorted(expected_lanes.items())):
            errors.append("outreach packets acquisition_lane_counts do not match records")
        if summary.get("target_source_family_counts") != dict(sorted(expected_families.items())):
            errors.append("outreach packets target_source_family_counts do not match records")
        if summary.get("priority_counts") != dict(sorted(expected_priorities.items())):
            errors.append("outreach packets priority_counts do not match records")
        if summary.get("source_domain_counts") != dict(sorted(expected_domains.items())):
            errors.append("outreach packets source_domain_counts do not match records")

        for packet in target_packets:
            packet_target = packet.get("target")
            packet_records = [
                record
                for record in outreach_records
                if packet_target in ((record.get("acquisition") or {}).get("outreach_targets") or [])
            ]
            if not packet.get("target_id"):
                errors.append("outreach target packet missing target_id")
            if packet.get("status") not in OUTREACH_STATUSES:
                errors.append(f"outreach target packet has invalid status {packet.get('status')!r}")
            if packet.get("request_count") != len(packet_records):
                errors.append(f"outreach target packet {packet_target!r} request_count does not match records")
            if sorted(packet.get("species_artifact_ids") or []) != sorted(
                record.get("artifact_id") for record in packet_records
            ):
                errors.append(f"outreach target packet {packet_target!r} species ids do not match records")
            if not packet.get("permission_fields"):
                errors.append(f"outreach target packet {packet_target!r} missing permission_fields")
            if not packet.get("preferred_contact_route"):
                errors.append(f"outreach target packet {packet_target!r} missing preferred_contact_route")

        outreach_keys = collect_keys(outreach)
        for key in sorted(OUTREACH_BANNED_KEYS & outreach_keys):
            errors.append(f"outreach packets contain banned key {key!r}")
        for outreach_string in collect_strings(outreach):
            for banned in PUBLIC_EXPLORER_BANNED_STRINGS:
                if banned in outreach_string:
                    errors.append(f"outreach packets contain banned public string {banned!r}")

        for record in outreach_records:
            label = record.get("artifact_id") or "outreach record"
            for outreach_error in validate_outreach_record(
                record,
                registry_by_id,
                acquisition_records_by_id,
                public_records_by_id,
                approval_records_by_id,
            ):
                errors.append(f"{label}: {outreach_error}")

    snapshot_records_by_id = {}
    if COMMONS_RIGHTS_SNAPSHOTS_PATH.exists():
        snapshots = yaml.safe_load(COMMONS_RIGHTS_SNAPSHOTS_PATH.read_text(encoding="utf-8")) or {}
        policy = snapshots.get("policy") or {}
        if policy.get("reviewer_only") is not True:
            errors.append("Commons rights snapshots policy.reviewer_only must be true")
        if policy.get("contains_review_candidate_urls") is not True:
            errors.append("Commons rights snapshots policy.contains_review_candidate_urls must be true")
        if policy.get("not_public_site_input") is not True:
            errors.append("Commons rights snapshots policy.not_public_site_input must be true")
        if policy.get("candidate_public_use") is not False:
            errors.append("Commons rights snapshots policy.candidate_public_use must be false")
        if policy.get("api_metadata_is_not_approval") is not True:
            errors.append("Commons rights snapshots policy.api_metadata_is_not_approval must be true")
        if policy.get("human_review_required_for_rights_species_ethics_crop") is not True:
            errors.append("Commons rights snapshots must require human rights/species/ethics/crop review")
        if policy.get("no_download_performed") is not True:
            errors.append("Commons rights snapshots policy.no_download_performed must be true")

        snapshot_records = snapshots.get("records") or []
        snapshot_records_by_id = {record.get("artifact_id"): record for record in snapshot_records}
        snapshot_ids = {record.get("artifact_id") for record in snapshot_records}
        registry_ids = set(registry_by_id)
        for artifact_id in sorted(registry_ids - snapshot_ids):
            errors.append(f"Commons rights snapshots missing artifact_id {artifact_id}")
        for artifact_id in sorted(snapshot_ids - registry_ids):
            errors.append(f"Commons rights snapshots has stale artifact_id {artifact_id}")

        summary = snapshots.get("summary") or {}
        if summary.get("species_records") != len(snapshot_records):
            errors.append("Commons rights snapshots summary.species_records does not match record count")
        if summary.get("species_records") != len(records):
            errors.append("Commons rights snapshots summary.species_records does not match registry count")
        expected_statuses = Counter(record.get("snapshot_status") or "none" for record in snapshot_records)
        expected_api_rights = Counter(
            (record.get("rights_evidence") or {}).get("api_rights_status") or "none"
            for record in snapshot_records
        )
        expected_registry_rights = Counter(
            (record.get("candidate") or {}).get("registry_rights_status") or "none"
            for record in snapshot_records
        )
        expected_reviewable = sum(
            1
            for record in snapshot_records
            if (record.get("rights_evidence") or {}).get("reviewable_for_public_primary") is True
        )
        expected_species_signals = sum(
            1
            for record in snapshot_records
            if (record.get("species_match_evidence") or {}).get("automated_text_signal") is True
        )
        expected_rights_mismatch = sorted(
            artifact_id
            for artifact_id, record in snapshot_records_by_id.items()
            if record.get("snapshot_status") == "fetched"
            and not ((record.get("registry_alignment") or {}).get("rights_status_matches_api") is True)
        )
        expected_url_mismatch = sorted(
            artifact_id
            for artifact_id, record in snapshot_records_by_id.items()
            if record.get("snapshot_status") == "fetched"
            and not ((record.get("registry_alignment") or {}).get("image_url_matches") is True)
        )
        expected_flagged = sorted(
            artifact_id
            for artifact_id, record in snapshot_records_by_id.items()
            if (record.get("snapshot_status") == "fetched")
            and (
                (record.get("ethics_location_evidence") or {}).get("api_text_flags")
                or (record.get("ethics_location_evidence") or {}).get("registry_flags")
            )
        )
        if summary.get("snapshot_status_counts") != dict(sorted(expected_statuses.items())):
            errors.append("Commons rights snapshots summary.snapshot_status_counts does not match records")
        if summary.get("api_rights_status_counts") != dict(sorted(expected_api_rights.items())):
            errors.append("Commons rights snapshots summary.api_rights_status_counts does not match records")
        if summary.get("registry_rights_status_counts") != dict(sorted(expected_registry_rights.items())):
            errors.append("Commons rights snapshots summary.registry_rights_status_counts does not match records")
        if summary.get("reviewable_rights_snapshot_count") != expected_reviewable:
            errors.append("Commons rights snapshots reviewable count does not match records")
        if summary.get("automated_species_text_signal_count") != expected_species_signals:
            errors.append("Commons rights snapshots species signal count does not match records")
        if sorted(summary.get("rights_mismatch_artifact_ids") or []) != expected_rights_mismatch:
            errors.append("Commons rights snapshots rights_mismatch_artifact_ids do not match records")
        if sorted(summary.get("image_url_mismatch_artifact_ids") or []) != expected_url_mismatch:
            errors.append("Commons rights snapshots image_url_mismatch_artifact_ids do not match records")
        if sorted(summary.get("records_with_ethics_or_location_flags") or []) != expected_flagged:
            errors.append("Commons rights snapshots records_with_ethics_or_location_flags do not match records")

        for record in snapshot_records:
            label = record.get("artifact_id") or "Commons rights snapshot record"
            for snapshot_error in validate_commons_snapshot_record(
                record,
                registry_by_id,
                approval_records_by_id,
            ):
                errors.append(f"{label}: {snapshot_error}")

    if APPROVAL_WORKBENCH_PATH.exists():
        workbench = yaml.safe_load(APPROVAL_WORKBENCH_PATH.read_text(encoding="utf-8")) or {}
        policy = workbench.get("policy") or {}
        if policy.get("reviewer_only") is not True:
            errors.append("approval workbench policy.reviewer_only must be true")
        if policy.get("contains_review_candidate_urls") is not True:
            errors.append("approval workbench policy.contains_review_candidate_urls must be true")
        if policy.get("not_public_site_input") is not True:
            errors.append("approval workbench policy.not_public_site_input must be true")
        if policy.get("candidate_public_use") is not False:
            errors.append("approval workbench policy.candidate_public_use must be false")
        if policy.get("public_site_must_use_render_contract") is not True:
            errors.append("approval workbench policy.public_site_must_use_render_contract must be true")
        if policy.get("source_card_does_not_authorize_image_copy") is not True:
            errors.append("approval workbench policy.source_card_does_not_authorize_image_copy must be true")
        if policy.get("promotion_requires_approval_queue") is not True:
            errors.append("approval workbench policy.promotion_requires_approval_queue must be true")
        if policy.get("human_review_required_for_rights_species_ethics_crop_alt_text") is not True:
            errors.append("approval workbench must require human review for rights/species/ethics/crop/alt text")
        if policy.get("google_images_discovery_only") is not True:
            errors.append("approval workbench policy.google_images_discovery_only must be true")
        if policy.get("partner_grants_require_written_permission") is not True:
            errors.append("approval workbench policy.partner_grants_require_written_permission must be true")
        if policy.get("no_bulk_download_or_scraping") is not True:
            errors.append("approval workbench policy.no_bulk_download_or_scraping must be true")

        workbench_records = workbench.get("records") or []
        workbench_records_by_id = {record.get("artifact_id"): record for record in workbench_records}
        workbench_ids = {record.get("artifact_id") for record in workbench_records}
        registry_ids = set(registry_by_id)
        for artifact_id in sorted(registry_ids - workbench_ids):
            errors.append(f"approval workbench missing artifact_id {artifact_id}")
        for artifact_id in sorted(workbench_ids - registry_ids):
            errors.append(f"approval workbench has stale artifact_id {artifact_id}")

        summary = workbench.get("summary") or {}
        if summary.get("species_records") != len(workbench_records):
            errors.append("approval workbench summary.species_records does not match record count")
        if summary.get("species_records") != len(records):
            errors.append("approval workbench summary.species_records does not match registry count")
        if summary.get("candidate_public_use_blocked") != len(workbench_records):
            errors.append("approval workbench must report every candidate as blocked from public use")

        expected_public_ready = sum(
            1
            for record in workbench_records
            if (record.get("public_boundary") or {}).get("source_card_public_use") is True
        )
        expected_hero_ready = sum(
            1
            for record in workbench_records
            if (record.get("public_boundary") or {}).get("species_page_hero_image_allowed") is True
        )
        expected_snapshots_fetched = sum(
            1
            for record in workbench_records
            if (record.get("commons_snapshot") or {}).get("snapshot_status") == "fetched"
        )
        expected_promotion_ready = sorted(
            artifact_id
            for artifact_id, record in workbench_records_by_id.items()
            if (record.get("approval_gate") or {}).get("promotion_allowed_now") is True
        )
        expected_flagged = sorted(
            artifact_id
            for artifact_id, record in workbench_records_by_id.items()
            if (record.get("candidate_media") or {}).get("flags")
        )
        expected_statuses = Counter(record.get("workbench_status") or "none" for record in workbench_records)
        expected_lanes = Counter(
            (record.get("acquisition") or {}).get("lane") or "none" for record in workbench_records
        )
        expected_candidate_rights = Counter(
            (record.get("candidate_media") or {}).get("rights_status") or "none"
            for record in workbench_records
        )
        expected_api_rights = Counter(
            (record.get("commons_snapshot") or {}).get("api_rights_status") or "none"
            for record in workbench_records
        )
        expected_domains = Counter(
            (record.get("public_boundary") or {}).get("public_source_domain") or "none"
            for record in workbench_records
        )
        expected_targets = Counter(
            target
            for record in workbench_records
            for target in ((record.get("acquisition") or {}).get("outreach_targets") or ["source-to-confirm"])
        )
        expected_missing_checks = Counter(
            check
            for record in workbench_records
            for check in ((record.get("approval_gate") or {}).get("missing_checks") or [])
        )
        expected_missing_fields = Counter(
            field
            for record in workbench_records
            for field in ((record.get("approval_gate") or {}).get("missing_approved_primary_fields") or [])
        )

        if summary.get("public_visual_ready") != expected_public_ready:
            errors.append("approval workbench summary.public_visual_ready does not match records")
        if summary.get("hero_image_ready") != expected_hero_ready:
            errors.append("approval workbench summary.hero_image_ready does not match records")
        if summary.get("approved_primary_needed") != len(workbench_records) - expected_hero_ready:
            errors.append("approval workbench summary.approved_primary_needed does not match records")
        if summary.get("commons_snapshots_fetched") != expected_snapshots_fetched:
            errors.append("approval workbench summary.commons_snapshots_fetched does not match records")
        if sorted(summary.get("promotion_ready_artifact_ids") or []) != expected_promotion_ready:
            errors.append("approval workbench promotion_ready_artifact_ids do not match records")
        if summary.get("promotion_ready_count") != len(expected_promotion_ready):
            errors.append("approval workbench promotion_ready_count does not match records")
        if sorted(summary.get("flagged_candidate_records") or []) != expected_flagged:
            errors.append("approval workbench flagged_candidate_records do not match records")
        if summary.get("workbench_status_counts") != dict(sorted(expected_statuses.items())):
            errors.append("approval workbench workbench_status_counts do not match records")
        if summary.get("acquisition_lane_counts") != dict(sorted(expected_lanes.items())):
            errors.append("approval workbench acquisition_lane_counts do not match records")
        if summary.get("candidate_rights_status_counts") != dict(sorted(expected_candidate_rights.items())):
            errors.append("approval workbench candidate_rights_status_counts do not match records")
        if summary.get("api_rights_status_counts") != dict(sorted(expected_api_rights.items())):
            errors.append("approval workbench api_rights_status_counts do not match records")
        if summary.get("public_source_domain_counts") != dict(sorted(expected_domains.items())):
            errors.append("approval workbench public_source_domain_counts do not match records")
        if summary.get("outreach_target_counts") != dict(sorted(expected_targets.items())):
            errors.append("approval workbench outreach_target_counts do not match records")
        if summary.get("missing_check_counts") != dict(sorted(expected_missing_checks.items())):
            errors.append("approval workbench missing_check_counts do not match records")
        if summary.get("missing_approved_primary_field_counts") != dict(sorted(expected_missing_fields.items())):
            errors.append("approval workbench missing approved-primary field counts do not match records")

        for record in workbench_records:
            label = record.get("artifact_id") or "approval workbench record"
            for workbench_error in validate_approval_workbench_record(
                record,
                registry_by_id,
                approval_records_by_id,
                dossier_records_by_id,
                snapshot_records_by_id,
                acquisition_records_by_id,
                public_records_by_id,
                trace_records_by_id,
                outreach_records_by_id,
            ):
                errors.append(f"{label}: {workbench_error}")

    approved = sum(1 for r in records if (r.get("primary") or {}).get("status") == "approved")
    needed = sum(1 for r in records if (r.get("primary") or {}).get("status") == "needed")
    candidates = sum(1 for r in records if (r.get("primary") or {}).get("status") == "candidate")

    for warning in warnings:
        print(f"WARN  {warning}")
    for error in errors:
        print(f"ERROR {error}")

    print(
        f"\nSpecies media registry: {len(records)} record(s), "
        f"{approved} approved primary, {candidates} candidate, {needed} needed."
    )
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
