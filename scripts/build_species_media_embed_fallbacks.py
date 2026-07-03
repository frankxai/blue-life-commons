#!/usr/bin/env python3
"""Build publication-safe rich source-card fallbacks for species media.

The source-card layer answers a different question than primary image
approval: what can the public site safely render when no image has passed
rights, species-match, crop, and ethics review?

The output never copies external media. A verified source card is a link-backed
fallback for species pages and the visual explorer, not permission to reuse an
image from the linked page.

Usage:
  python scripts/build_species_media_embed_fallbacks.py
"""
from __future__ import annotations

import argparse
from collections import Counter
from datetime import date
from pathlib import Path
from urllib.parse import urlparse

import yaml

ROOT = Path(__file__).resolve().parent.parent
REGISTRY_PATH = ROOT / "content" / "media" / "species-media-registry.yaml"
FALLBACK_PATH = ROOT / "content" / "media" / "species-media-rich-embeds.yaml"
REVIEW_DIR = ROOT / "content" / "media" / "review-packs"

OFFICIAL_DOMAINS = {
    "cdhc.noaa.gov": "official_institutional",
    "fisheries.noaa.gov": "official_institutional",
    "floridakeys.noaa.gov": "official_institutional",
    "fws.gov": "official_institutional",
    "maritime-forum.ec.europa.eu": "official_institutional",
    "nps.gov": "official_institutional",
}

SOURCE_DOMAIN_TYPES = {
    **OFFICIAL_DOMAINS,
    "floridamuseum.ufl.edu": "institutional",
    "iucn.org": "authority_source",
    "kew.org": "institutional",
    "mantatrust.org": "partner_or_ngo",
    "oceanicsociety.org": "partner_or_ngo",
}

STATUS_LABELS = {
    "verified_source_card": "Verified source card",
    "needs_browser_recheck": "Needs browser recheck",
    "needs_link_check": "Needs link check",
    "missing_source_url": "Missing source URL",
    "broken_or_blocked": "Broken or blocked",
}


def load_yaml(path: Path):
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def rel(path: Path):
    return path.relative_to(ROOT).as_posix()


def latest_link_check():
    files = sorted(REVIEW_DIR.glob("species-media-link-check-*.yaml"))
    return files[-1] if files else None


def domain_for(url):
    if not url:
        return None
    return urlparse(url).netloc.lower().removeprefix("www.")


def link_result_map(link_check_path):
    if not link_check_path or not Path(link_check_path).exists():
        return {}, None
    payload = load_yaml(Path(link_check_path))
    results = {}
    for item in payload.get("links") or []:
        if item.get("kind") != "rich_embed_source":
            continue
        results[(item.get("artifact_id"), item.get("url"))] = item
    return results, payload


def source_card_status(url, link_result):
    if not url:
        return "missing_source_url"
    if not link_result:
        return "needs_link_check"
    if link_result.get("ok"):
        return "verified_source_card"
    if link_result.get("status_code") in {403, 405, 429}:
        return "needs_browser_recheck"
    return "broken_or_blocked"


def reviewer_action(status):
    if status == "verified_source_card":
        return "Safe as a link-backed fallback; do not copy images from the page without image-level rights review."
    if status == "needs_browser_recheck":
        return "Open in a browser and confirm the source page works before using it as a public fallback."
    if status == "needs_link_check":
        return "Run scripts/verify_species_media_links.py before enabling this fallback."
    if status == "missing_source_url":
        return "Add an official, institutional, partner, or authority source URL."
    return "Replace the source URL or document why the verifier failure is a temporary network issue."


def card_record(record, link_results):
    rich_embed = record.get("rich_embed") or {}
    url = rich_embed.get("preferred_source_url")
    domain = domain_for(url)
    link_result = link_results.get((record.get("artifact_id"), url))
    status = source_card_status(url, link_result)
    source_type = SOURCE_DOMAIN_TYPES.get(domain, "source_to_classify")
    public_use = status == "verified_source_card"
    return {
        "artifact_id": record.get("artifact_id"),
        "species_page": record.get("species_page"),
        "common_name": record.get("common_name"),
        "scientific_name": record.get("scientific_name"),
        "taxon_group": record.get("taxon_group"),
        "source_card": {
            "embed_id": f"{record.get('artifact_id')}-source-card-001",
            "status": status,
            "status_label": STATUS_LABELS.get(status, status),
            "public_use": public_use,
            "copies_external_media": False,
            "use_role": "public fallback when approved primary image is absent",
            "source_url": url,
            "domain": domain,
            "source_type": source_type,
            "display_title": f"{record.get('common_name')} source card",
            "allowed_surfaces": [
                "species-page-source-card",
                "visual-explorer-source-inspector",
                "review-pack",
            ]
            if public_use
            else ["review-pack"],
            "blocked_surfaces": [
                "primary-image-download",
                "social-crop-as-image",
                "hero-image-reuse-without-image-level-license",
            ],
            "link_check": {
                "ok": bool((link_result or {}).get("ok")),
                "status_code": (link_result or {}).get("status_code"),
                "method": (link_result or {}).get("method"),
                "elapsed_ms": (link_result or {}).get("elapsed_ms"),
                "error": (link_result or {}).get("error"),
            },
            "reviewer_action": reviewer_action(status),
        },
    }


def render_markdown(payload):
    summary = payload["summary"]
    lines = [
        "# Species Media Rich Embed Fallbacks",
        "",
        f"Generated: {payload['generated_at']}",
        "",
        "These source cards are publication-safe fallbacks for species records without approved primary images. They link to official, institutional, partner, or authority pages and do not copy external images.",
        "",
        "## Summary",
        "",
        f"- Species records: {summary['species_records']}",
        f"- Public fallback ready: {summary['public_fallback_ready']}",
        f"- Needs browser recheck: {summary['needs_browser_recheck']}",
        f"- Needs link check: {summary['needs_link_check']}",
        f"- Broken or blocked: {summary['broken_or_blocked']}",
        "",
        "## Reviewer Follow-Up",
        "",
    ]

    follow_up = [
        record
        for record in payload["records"]
        if record["source_card"]["status"] != "verified_source_card"
    ]
    if follow_up:
        lines.extend(["| Species | Status | Source | Action |", "|---|---|---|---|"])
        for record in follow_up:
            card = record["source_card"]
            lines.append(
                f"| {record['common_name']} | `{card['status']}` | {card.get('source_url') or '-'} | {card['reviewer_action']} |"
            )
    else:
        lines.append("No source-card fallback follow-up detected.")

    lines.extend(
        [
            "",
            "## Source Card Board",
            "",
            "| Species | Status | Source type | Domain | Public use | Source |",
            "|---|---|---|---|---|---|",
        ]
    )
    for record in payload["records"]:
        card = record["source_card"]
        public_use = "yes" if card["public_use"] else "no"
        source = card.get("source_url") or ""
        link = f"[source]({source})" if source else "-"
        lines.append(
            f"| {record['common_name']} | `{card['status']}` | `{card['source_type']}` | {card.get('domain') or '-'} | {public_use} | {link} |"
        )
    return "\n".join(lines).rstrip() + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--registry", type=Path, default=REGISTRY_PATH)
    parser.add_argument("--link-check", type=Path, default=None)
    parser.add_argument("--out", type=Path, default=FALLBACK_PATH)
    parser.add_argument(
        "--out-md",
        type=Path,
        default=REVIEW_DIR / f"species-media-rich-embed-fallbacks-{date.today().isoformat()}.md",
    )
    args = parser.parse_args()

    registry_path = args.registry if args.registry.is_absolute() else ROOT / args.registry
    link_check_path = args.link_check if args.link_check else latest_link_check()
    if link_check_path and not link_check_path.is_absolute():
        link_check_path = ROOT / link_check_path
    output_path = args.out if args.out.is_absolute() else ROOT / args.out
    output_md = args.out_md if args.out_md.is_absolute() else ROOT / args.out_md

    registry = load_yaml(registry_path)
    link_results, link_payload = link_result_map(link_check_path)
    records = [card_record(record, link_results) for record in registry.get("records") or []]
    status_counts = Counter(record["source_card"]["status"] for record in records)
    domain_counts = Counter(record["source_card"].get("domain") or "none" for record in records)
    source_type_counts = Counter(record["source_card"].get("source_type") or "none" for record in records)

    payload = {
        "version": date.today().isoformat(),
        "generated_at": date.today().isoformat(),
        "source_registry": rel(registry_path),
        "source_link_check": rel(link_check_path) if link_check_path else None,
        "policy": {
            "source_cards_copy_external_media": False,
            "source_card_public_use_does_not_grant_image_reuse": True,
            "approved_primary_image_still_required_for_species_hero": True,
            "google_images_discovery_only": True,
        },
        "summary": {
            "species_records": len(records),
            "public_fallback_ready": status_counts.get("verified_source_card", 0),
            "needs_browser_recheck": status_counts.get("needs_browser_recheck", 0),
            "needs_link_check": status_counts.get("needs_link_check", 0),
            "broken_or_blocked": status_counts.get("broken_or_blocked", 0),
            "missing_source_url": status_counts.get("missing_source_url", 0),
            "status_counts": dict(sorted(status_counts.items())),
            "domain_counts": dict(sorted(domain_counts.items())),
            "source_type_counts": dict(sorted(source_type_counts.items())),
        },
        "link_check_summary": (link_payload or {}).get("summary") or {},
        "records": records,
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_md.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(yaml.safe_dump(payload, sort_keys=False, allow_unicode=False, width=120), encoding="utf-8")
    output_md.write_text(render_markdown(payload), encoding="utf-8")

    print(f"Wrote {rel(output_path)}")
    print(f"Wrote {rel(output_md)}")
    print(
        "Species media source cards: "
        f"{len(records)} records, {payload['summary']['public_fallback_ready']} public fallback ready, "
        f"{payload['summary']['needs_browser_recheck']} need browser recheck."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
