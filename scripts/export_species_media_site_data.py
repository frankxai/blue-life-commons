#!/usr/bin/env python3
"""Export joined species/media data for a future visual explorer.

The output is intentionally publication-safe: candidate images are marked as
review-only, and no candidate is represented as approved primary media.

Usage:
  python scripts/export_species_media_site_data.py
"""
from __future__ import annotations

from collections import Counter
from datetime import date
import json
from pathlib import Path
import sys

import yaml

ROOT = Path(__file__).resolve().parent.parent
REGISTRY_PATH = ROOT / "content" / "media" / "species-media-registry.yaml"
SOURCE_ROUTING_PATH = ROOT / "content" / "media" / "species-media-source-routing.yaml"
RICH_EMBEDS_PATH = ROOT / "content" / "media" / "species-media-rich-embeds.yaml"
APPROVAL_QUEUE_PATH = ROOT / "content" / "media" / "species-media-approval-queue.yaml"
RENDER_CONTRACT_PATH = ROOT / "content" / "media" / "species-media-render-contract.yaml"
OUT_PATH = ROOT / "content" / "media" / "species-media-site-data.json"


def frontmatter(path: Path):
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return {}
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}
    return yaml.safe_load(parts[1]) or {}


def site_record(record, source_route=None, rich_embed_fallback=None, approval_record=None, render_contract=None):
    species_path = ROOT / record["species_page"]
    fm = frontmatter(species_path)
    primary = record.get("primary") or {}
    candidate = primary.get("candidate") or {}
    return {
        "artifact_id": record.get("artifact_id"),
        "species_page": record.get("species_page"),
        "website_path": (fm.get("outputs") or {}).get("website_path"),
        "taxon_group": record.get("taxon_group"),
        "common_name": record.get("common_name"),
        "scientific_name": record.get("scientific_name"),
        "species_slugs": record.get("species_slugs") or [],
        "media_status": record.get("media_status"),
        "primary_status": primary.get("status"),
        "approved": {
            "asset_id": primary.get("approved_asset_id"),
            "path": primary.get("approved_path"),
            "source_url": primary.get("source_url"),
            "original_media_url": primary.get("original_media_url"),
            "creator": primary.get("creator"),
            "credit": primary.get("credit"),
            "license": primary.get("license"),
            "license_url": primary.get("license_url"),
            "rights_status": primary.get("rights_status"),
            "alt_text": primary.get("alt_text"),
            "qa_status": primary.get("qa_status"),
            "approved_surfaces": primary.get("approved_surfaces") or [],
            "blocked_surfaces": primary.get("blocked_surfaces") or [],
            "reviewer": primary.get("reviewer"),
            "reviewed_on": primary.get("reviewed_on"),
        },
        "candidate": {
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
            "flags": candidate.get("flags") or [],
            "review_status": candidate.get("review_status"),
            "public_use": False,
        },
        "rich_embed": record.get("rich_embed") or {},
        "public_fallback": {
            "source_card": (rich_embed_fallback or {}).get("source_card") or {},
        },
        "curation": {
            "decision": (approval_record or {}).get("decision"),
            "reviewer": (approval_record or {}).get("reviewer"),
            "reviewed_on": (approval_record or {}).get("reviewed_on"),
            "checks_complete": sum(
                1 for value in ((approval_record or {}).get("checks") or {}).values() if value is True
            ),
            "checks_total": len(((approval_record or {}).get("checks") or {})),
        },
        "source_route": {
            "priority": (source_route or {}).get("priority"),
            "route": (source_route or {}).get("route"),
            "rationale": (source_route or {}).get("rationale"),
            "partner_refs": (source_route or {}).get("partner_refs") or [],
            "recommended_actions": (source_route or {}).get("recommended_actions") or [],
        },
        "source_candidates": record.get("source_candidates") or {},
        "supporting_assets": record.get("current_supporting_assets") or [],
        "render_contract": render_contract or {},
        "next_action": record.get("next_action"),
    }


def main():
    registry = yaml.safe_load(REGISTRY_PATH.read_text(encoding="utf-8")) or {}
    source_routing = {}
    if SOURCE_ROUTING_PATH.exists():
        source_routing_payload = yaml.safe_load(SOURCE_ROUTING_PATH.read_text(encoding="utf-8")) or {}
        source_routing = {
            record.get("artifact_id"): record for record in source_routing_payload.get("records") or []
        }
    rich_embed_fallbacks = {}
    if RICH_EMBEDS_PATH.exists():
        rich_embed_payload = yaml.safe_load(RICH_EMBEDS_PATH.read_text(encoding="utf-8")) or {}
        rich_embed_fallbacks = {
            record.get("artifact_id"): record for record in rich_embed_payload.get("records") or []
        }
    approval_queue = {}
    if APPROVAL_QUEUE_PATH.exists():
        approval_payload = yaml.safe_load(APPROVAL_QUEUE_PATH.read_text(encoding="utf-8")) or {}
        approval_queue = {
            record.get("artifact_id"): record for record in approval_payload.get("records") or []
        }
    render_contract = {}
    if RENDER_CONTRACT_PATH.exists():
        render_contract_payload = yaml.safe_load(RENDER_CONTRACT_PATH.read_text(encoding="utf-8")) or {}
        render_contract = {
            record.get("artifact_id"): record for record in render_contract_payload.get("records") or []
        }
    records = [
        site_record(
            record,
            source_routing.get(record.get("artifact_id")),
            rich_embed_fallbacks.get(record.get("artifact_id")),
            approval_queue.get(record.get("artifact_id")),
            render_contract.get(record.get("artifact_id")),
        )
        for record in registry.get("records") or []
    ]
    missing_pages = [record["species_page"] for record in records if not (ROOT / record["species_page"]).exists()]
    if missing_pages:
        for path in missing_pages:
            print(f"ERROR missing species page: {path}", file=sys.stderr)
        return 1

    status_counts = Counter(record["primary_status"] for record in records)
    group_counts = Counter(record["taxon_group"] for record in records)
    rights_counts = Counter((record["candidate"] or {}).get("rights_status") or "none" for record in records)
    route_counts = Counter((record.get("source_route") or {}).get("route") or "none" for record in records)
    fallback_counts = Counter(
        ((record.get("public_fallback") or {}).get("source_card") or {}).get("status") or "none"
        for record in records
    )
    curation_counts = Counter((record.get("curation") or {}).get("decision") or "none" for record in records)
    render_strategy_counts = Counter(
        ((record.get("render_contract") or {}).get("render_strategy")) or "none" for record in records
    )
    public_visual_ready = sum(
        1
        for record in records
        if (((record.get("render_contract") or {}).get("public_visual") or {}).get("public_use") is True)
    )
    hero_image_ready = sum(
        1
        for record in records
        if (((record.get("render_contract") or {}).get("surface_rules") or {}).get("species_page_hero_image_allowed")
        is True)
    )
    flagged = [record["artifact_id"] for record in records if (record["candidate"] or {}).get("flags")]

    payload = {
        "version": date.today().isoformat(),
        "generated_at": date.today().isoformat(),
        "policy": {
            "candidate_public_use": False,
            "approved_primary_required_for_public_species_hero": True,
            "generated_supporting_assets_are_not_official_media": True,
            "public_site_must_follow_render_contract": True,
        },
        "summary": {
            "species_records": len(records),
            "primary_status_counts": dict(sorted(status_counts.items())),
            "taxon_group_counts": dict(sorted(group_counts.items())),
            "candidate_rights_counts": dict(sorted(rights_counts.items())),
            "source_route_counts": dict(sorted(route_counts.items())),
            "public_fallback_counts": dict(sorted(fallback_counts.items())),
            "curation_decision_counts": dict(sorted(curation_counts.items())),
            "render_strategy_counts": dict(sorted(render_strategy_counts.items())),
            "public_visual_ready": public_visual_ready,
            "hero_image_ready": hero_image_ready,
            "candidate_records_with_flags": flagged,
        },
        "records": records,
    }
    OUT_PATH.write_text(json.dumps(payload, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    print(f"Wrote {OUT_PATH.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
