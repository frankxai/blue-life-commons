#!/usr/bin/env python3
"""Build the public render contract for species media.

The contract answers the site question directly: what may a public species
surface render today? Candidate photos remain review-only and are never a
public visual, even when they are visible in reviewer tooling.

Usage:
  python scripts/build_species_media_render_contract.py
"""
from __future__ import annotations

from collections import Counter
from datetime import date
from pathlib import Path
from urllib.parse import quote, unquote, urlparse

import yaml

ROOT = Path(__file__).resolve().parent.parent
SITE_DATA_PATH = ROOT / "content" / "media" / "species-media-site-data.json"
RENDER_CONTRACT_PATH = ROOT / "content" / "media" / "species-media-render-contract.yaml"
REVIEW_DIR = ROOT / "content" / "media" / "review-packs"


def load_site_data():
    import json

    return json.loads(SITE_DATA_PATH.read_text(encoding="utf-8"))


def rel(path: Path):
    return path.relative_to(ROOT).as_posix()


def source_host(source_url):
    if not source_url:
        return None
    return urlparse(source_url).netloc.lower()


def commons_public_media_url(source_url, original_media_url=None, width=900):
    if not source_url:
        return original_media_url
    parsed = urlparse(source_url)
    marker = "/wiki/File:"
    if parsed.netloc.lower() == "commons.wikimedia.org" and marker in parsed.path:
        filename = unquote(parsed.path.split(marker, 1)[1])
        return f"https://commons.wikimedia.org/wiki/Special:FilePath/{quote(filename)}?width={width}"
    return original_media_url


def candidate_snapshot(record):
    candidate = record.get("candidate") or {}
    return {
        "asset_id": candidate.get("asset_id"),
        "provider": candidate.get("provider"),
        "title": candidate.get("title"),
        "commons_file_page": candidate.get("commons_file_page"),
        "image_url": candidate.get("image_url"),
        "creator": candidate.get("creator"),
        "credit": candidate.get("credit"),
        "license": candidate.get("license"),
        "rights_status": candidate.get("rights_status"),
        "flags": candidate.get("flags") or [],
        "review_status": candidate.get("review_status"),
        "public_use": False,
        "blocked_surfaces": [
            "species-page-hero",
            "public-species-card-image",
            "social-crop",
            "downloaded-primary-asset",
        ],
    }


def public_placeholder(kind, title, action, source_card=None):
    source_card = source_card or {}
    return {
        "kind": kind,
        "public_use": False,
        "display_title": title,
        "source_url": source_card.get("source_url"),
        "domain": source_card.get("domain"),
        "status": source_card.get("status"),
        "reviewer_action": action,
    }


def render_record(record):
    approved = record.get("approved") or {}
    candidate = record.get("candidate") or {}
    source_card = ((record.get("public_fallback") or {}).get("source_card") or {})
    primary_status = record.get("primary_status")
    source_card_status = source_card.get("status")
    source_card_public = source_card.get("public_use") is True
    approved_ready = (
        primary_status == "approved"
        and bool(approved.get("asset_id"))
        and approved.get("qa_status") == "approved"
    )

    blocked_reasons = []
    if candidate.get("asset_id"):
        blocked_reasons.append("candidate media is review-only until curator approval")

    if approved_ready:
        strategy = "approved_primary_image"
        public_visual = {
            "kind": "image",
            "public_use": True,
            "asset_id": approved.get("asset_id"),
            "path": approved.get("path"),
            "source_url": approved.get("source_url"),
            "public_media_url": approved.get("path")
            or commons_public_media_url(approved.get("source_url"), approved.get("original_media_url")),
            "original_media_url": approved.get("original_media_url"),
            "domain": source_host(approved.get("source_url")),
            "creator": approved.get("creator"),
            "credit": approved.get("credit"),
            "license": approved.get("license"),
            "license_url": approved.get("license_url"),
            "rights_status": approved.get("rights_status"),
            "qa_status": approved.get("qa_status"),
            "alt_text": approved.get("alt_text"),
            "approved_surfaces": approved.get("approved_surfaces") or [],
            "blocked_surfaces": approved.get("blocked_surfaces") or [],
            "use_role": "approved species primary visual",
            "copies_external_media": False,
        }
        hero_image_allowed = True
    elif source_card_status == "verified_source_card" and source_card_public:
        strategy = "verified_source_card_fallback"
        public_visual = {
            "kind": "source_card",
            "public_use": True,
            "embed_id": source_card.get("embed_id"),
            "source_url": source_card.get("source_url"),
            "domain": source_card.get("domain"),
            "source_type": source_card.get("source_type"),
            "display_title": source_card.get("display_title"),
            "use_role": "link-backed public fallback when approved primary image is absent",
            "copies_external_media": False,
        }
        hero_image_allowed = False
        blocked_reasons.append("verified source card does not grant image download, crop, or hero-image reuse")
    elif source_card_status == "needs_browser_recheck":
        strategy = "source_card_recheck_placeholder"
        public_visual = public_placeholder(
            "source_card_placeholder",
            "Source card pending browser recheck",
            source_card.get("reviewer_action"),
            source_card,
        )
        hero_image_allowed = False
        blocked_reasons.append("source card must be opened in browser before public fallback use")
    elif candidate.get("asset_id"):
        strategy = "review_only_candidate_placeholder"
        public_visual = public_placeholder(
            "placeholder",
            "Media pending rights, species-match, crop, and ethics review",
            "Use reviewer board only until approval or source-card fallback is available.",
            source_card,
        )
        hero_image_allowed = False
    else:
        strategy = "blocked_no_public_visual"
        public_visual = public_placeholder(
            "placeholder",
            "No public visual available",
            "Add an official, partner, public-domain, open-license, or verified source-card fallback.",
            source_card,
        )
        hero_image_allowed = False
        blocked_reasons.append("no approved image, verified source card, or review-only candidate is available")

    species_slot = public_visual["kind"] in {"image", "source_card", "source_card_placeholder", "placeholder"}
    return {
        "artifact_id": record.get("artifact_id"),
        "species_page": record.get("species_page"),
        "common_name": record.get("common_name"),
        "scientific_name": record.get("scientific_name"),
        "taxon_group": record.get("taxon_group"),
        "render_strategy": strategy,
        "public_visual": public_visual,
        "surface_rules": {
            "species_page_visual_slot": species_slot,
            "visual_explorer_card_slot": True,
            "species_page_hero_image_allowed": hero_image_allowed,
            "social_crop_allowed": hero_image_allowed,
            "candidate_thumbnail_allowed": False,
        },
        "candidate_public_use": False,
        "review_only_candidate": candidate_snapshot(record),
        "blocked_public_use_reasons": blocked_reasons,
        "implementation_note": (
            "Render public_visual for public pages. Candidate URLs are for reviewer tooling only and "
            "must not be used as public species identity media."
        ),
    }


def render_markdown(payload):
    summary = payload["summary"]
    lines = [
        "# Species Media Render Contract",
        "",
        f"Generated: {payload['generated_at']}",
        "",
        "This contract tells public site surfaces what they may render right now. It separates approved images, verified source-card fallbacks, and non-public placeholders from review-only candidate photos.",
        "",
        "## Summary",
        "",
        f"- Species records: {summary['species_records']}",
        "- Render strategies: " + ", ".join(f"{k}={v}" for k, v in summary["render_strategy_counts"].items()),
        f"- Public visual ready: {summary['public_visual_ready']}",
        f"- Hero image ready: {summary['hero_image_ready']}",
        f"- Source-card fallback ready: {summary['source_card_ready']}",
        f"- Needs browser recheck: {summary['needs_browser_recheck']}",
        f"- Candidate public use blocked: {summary['candidate_public_use_blocked']}",
        "",
        "## Public Render Board",
        "",
        "| Species | Strategy | Public visual | Hero image | Source | Candidate public use | Next action |",
        "|---|---|---|---|---|---|---|",
    ]
    for record in payload["records"]:
        public_visual = record["public_visual"]
        source = public_visual.get("source_url") or public_visual.get("path") or "-"
        if source and source != "-" and str(source).startswith("http"):
            source = f"[source]({source})"
        hero = "yes" if record["surface_rules"].get("species_page_hero_image_allowed") else "no"
        candidate_public = "yes" if record.get("candidate_public_use") else "no"
        action = "; ".join(record.get("blocked_public_use_reasons") or []) or "approved primary image can render"
        lines.append(
            f"| {record['common_name']} | `{record['render_strategy']}` | `{public_visual['kind']}` | {hero} | {source} | {candidate_public} | {action} |"
        )
    return "\n".join(lines).rstrip() + "\n"


def build_contract():
    site_data = load_site_data()
    records = [render_record(record) for record in site_data.get("records") or []]
    strategy_counts = Counter(record["render_strategy"] for record in records)
    public_visual_ready = sum(1 for record in records if record["public_visual"].get("public_use") is True)
    hero_image_ready = sum(
        1 for record in records if record["surface_rules"].get("species_page_hero_image_allowed") is True
    )
    source_card_ready = sum(1 for record in records if record["render_strategy"] == "verified_source_card_fallback")
    needs_browser_recheck = sum(1 for record in records if record["render_strategy"] == "source_card_recheck_placeholder")
    candidate_public_use_blocked = sum(1 for record in records if record.get("candidate_public_use") is False)
    return {
        "version": date.today().isoformat(),
        "generated_at": date.today().isoformat(),
        "source_site_data": rel(SITE_DATA_PATH),
        "policy": {
            "candidate_public_use": False,
            "public_site_must_render_public_visual_only": True,
            "source_card_fallback_does_not_grant_image_reuse": True,
            "approved_primary_required_for_hero_image": True,
        },
        "summary": {
            "species_records": len(records),
            "render_strategy_counts": dict(sorted(strategy_counts.items())),
            "public_visual_ready": public_visual_ready,
            "hero_image_ready": hero_image_ready,
            "source_card_ready": source_card_ready,
            "needs_browser_recheck": needs_browser_recheck,
            "candidate_public_use_blocked": candidate_public_use_blocked,
        },
        "records": records,
    }


def main():
    payload = build_contract()
    RENDER_CONTRACT_PATH.write_text(
        yaml.safe_dump(payload, sort_keys=False, allow_unicode=False), encoding="utf-8"
    )
    REVIEW_DIR.mkdir(parents=True, exist_ok=True)
    markdown_path = REVIEW_DIR / f"species-media-render-contract-{date.today().isoformat()}.md"
    markdown_path.write_text(render_markdown(payload), encoding="utf-8")
    print(f"Wrote {rel(RENDER_CONTRACT_PATH)}")
    print(f"Wrote {rel(markdown_path)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
