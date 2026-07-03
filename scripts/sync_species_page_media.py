#!/usr/bin/env python3
"""Sync species-page frontmatter with the central species media contracts.

The central registry remains the source of truth. This script writes compact,
public-safe pointers into each species page so static site generators can find
the registry record, render contract, public source-card fallback, and current
approval state without reading review-only candidate image fields.

Usage:
  python scripts/sync_species_page_media.py --check
  python scripts/sync_species_page_media.py --write
"""
from __future__ import annotations

import argparse
from pathlib import Path
import sys

import yaml

ROOT = Path(__file__).resolve().parent.parent
SITE_DATA_PATH = ROOT / "content" / "media" / "species-media-site-data.json"
PUBLIC_EXPLORER_PATH = ROOT / "content" / "media" / "species-media-public-explorer-manifest.yaml"


def load_yaml(path: Path):
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def load_json(path: Path):
    import json

    return json.loads(path.read_text(encoding="utf-8"))


def split_frontmatter(path: Path):
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        raise ValueError(f"{path} has no YAML frontmatter")
    parts = text.split("---", 2)
    if len(parts) < 3:
        raise ValueError(f"{path} has incomplete YAML frontmatter")
    frontmatter = yaml.safe_load(parts[1]) or {}
    body = parts[2].lstrip("\r\n")
    return frontmatter, body


def dump_page(frontmatter, body):
    yaml_text = yaml.safe_dump(frontmatter, sort_keys=False, allow_unicode=False, width=1000)
    return f"---\n{yaml_text}---\n\n{body}"


def expected_media(site_record, public_record):
    artifact_id = site_record["artifact_id"]
    render = site_record.get("render_contract") or {}
    public_visual = (render.get("public_visual") or {}).copy()
    surface_rules = render.get("surface_rules") or {}
    source_card = ((site_record.get("public_fallback") or {}).get("source_card") or {})
    curation = site_record.get("curation") or {}
    supporting_assets = site_record.get("supporting_assets") or []
    approved = site_record.get("approved") or {}
    primary_status = site_record.get("primary_status")
    approved_ready = primary_status == "approved" and bool(approved.get("asset_id"))

    if approved_ready:
        primary = {
            "asset_id": approved.get("asset_id"),
            "path": approved.get("path"),
            "source_url": public_visual.get("source_url"),
            "public_media_url": public_visual.get("public_media_url"),
            "original_media_url": approved.get("original_media_url"),
            "creator": approved.get("creator"),
            "credit": approved.get("credit"),
            "license": approved.get("license"),
            "license_url": approved.get("license_url"),
            "rights_status": approved.get("rights_status"),
            "alt_text": approved.get("alt_text"),
            "qa_status": approved.get("qa_status") or "approved",
        }
    else:
        primary = {
            "asset_id": None,
            "path": None,
            "source_url": None,
            "creator": None,
            "credit": None,
            "license": None,
            "rights_status": "needs-review",
            "alt_text": None,
            "qa_status": "candidate",
        }

    if approved_ready:
        embed = {
            "provider": "approved_primary_source",
            "url": public_visual.get("source_url"),
            "rights_status": approved.get("rights_status"),
            "notes": "Approved primary media source; render public_media_url with stored attribution and blocked-surface rules.",
        }
        if public_visual.get("domain"):
            embed["domain"] = public_visual.get("domain")
        if public_visual.get("license"):
            embed["license"] = public_visual.get("license")
    else:
        embed = {
            "provider": "source_card",
            "url": public_visual.get("source_url"),
            "rights_status": "link-backed-source-card",
            "notes": (
                "Public fallback only; does not authorize image download, crop, "
                "social reuse, or hero-image reuse."
            ),
        }
        if source_card.get("domain"):
            embed["domain"] = source_card.get("domain")
        if source_card.get("source_type"):
            embed["source_type"] = source_card.get("source_type")

    return {
        "registry_record": f"content/media/species-media-registry.yaml#{artifact_id}",
        "render_contract": f"content/media/species-media-render-contract.yaml#{artifact_id}",
        "public_explorer_record": f"content/media/species-media-public-explorer-manifest.yaml#{artifact_id}",
        "primary": primary,
        "embeds": [embed],
        "render": {
            "strategy": render.get("render_strategy"),
            "public_visual_kind": public_visual.get("kind"),
            "public_visual_public_use": public_visual.get("public_use") is True,
            "species_page_visual_slot": surface_rules.get("species_page_visual_slot") is True,
            "species_page_hero_image_allowed": surface_rules.get("species_page_hero_image_allowed") is True,
            "candidate_thumbnail_allowed": surface_rules.get("candidate_thumbnail_allowed") is True,
            "candidate_public_use": render.get("candidate_public_use") is True,
        },
        "review": {
            "primary_status": primary_status,
            "curation_decision": curation.get("decision"),
            "checks_complete": curation.get("checks_complete") or 0,
            "checks_total": curation.get("checks_total") or 0,
            "promotion_allowed_now": (public_record.get("curation") or {}).get("promotion_allowed_now") is True,
        },
        "supporting_assets": supporting_assets,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true", help="Fail if any species page is out of sync.")
    mode.add_argument("--write", action="store_true", help="Update species-page frontmatter in place.")
    args = parser.parse_args()

    site_data = load_json(SITE_DATA_PATH)
    public_data = load_yaml(PUBLIC_EXPLORER_PATH)
    public_by_id = {record.get("artifact_id"): record for record in public_data.get("records") or []}

    changed = []
    errors = []
    for site_record in site_data.get("records") or []:
        artifact_id = site_record.get("artifact_id")
        public_record = public_by_id.get(artifact_id)
        if not public_record:
            errors.append(f"{artifact_id}: missing public explorer record")
            continue
        page_path = ROOT / site_record["species_page"]
        frontmatter, body = split_frontmatter(page_path)
        expected = expected_media(site_record, public_record)
        if frontmatter.get("media") != expected:
            changed.append(site_record["species_page"])
            if args.write:
                frontmatter["media"] = expected
                page_path.write_text(dump_page(frontmatter, body), encoding="utf-8")

    for error in errors:
        print(f"ERROR {error}")
    if changed:
        action = "Updated" if args.write else "Out of sync"
        for path in changed:
            print(f"{action}: {path}")
    else:
        print("Species page media frontmatter is in sync.")

    if errors:
        return 1
    if changed and args.check:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
