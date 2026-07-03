#!/usr/bin/env python3
"""Build source-routing and partner/reviewer packets for species media.

This script turns the media registry into practical review lanes:
official/public-domain fast track, open-license attribution review, ethics
replacement/manual review, rich-embed fallback, and partner/media-grant asks.

It does not approve media, download media, or claim that any candidate is safe
for public hero use.

Usage:
  python scripts/build_species_media_source_packets.py
"""
from __future__ import annotations

from collections import Counter, defaultdict
from datetime import date
from pathlib import Path
from urllib.parse import urlparse

import yaml

ROOT = Path(__file__).resolve().parent.parent
REGISTRY_PATH = ROOT / "content" / "media" / "species-media-registry.yaml"
ROUTING_PATH = ROOT / "content" / "media" / "species-media-source-routing.yaml"
REVIEW_DIR = ROOT / "content" / "media" / "review-packs"

OFFICIAL_TERMS = [
    "noaa",
    "nmfs",
    "national oceanic",
    "u.s. fish",
    "usfws",
    "fish and wildlife service",
    "national park service",
    "nps",
    "nasa",
    "federal government",
    "government employee",
    "smithsonian",
]

HIGH_RISK_FLAGS = {
    "distress_or_mortality_review",
    "captivity_or_facility_review",
    "individual_or_tagged_animal_review",
}

OPEN_RIGHTS = {
    "public-domain-or-cc0-candidate",
    "cc-by-candidate",
    "cc-by-sa-candidate",
}


def load_yaml(path: Path):
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def rel(path: Path):
    return path.relative_to(ROOT).as_posix()


def text_blob(*values):
    return " ".join(str(value or "") for value in values).lower()


def url_domain(url):
    if not url:
        return None
    parsed = urlparse(url)
    return parsed.netloc.lower().removeprefix("www.")


def source_ref_groups(record, source_profiles):
    refs = record.get("source_candidates") or {}
    all_refs = []
    for key in ["official_or_institutional_refs", "open_license_refs", "partner_refs"]:
        all_refs.extend(refs.get(key) or [])

    grouped = defaultdict(list)
    for ref in all_refs:
        profile = source_profiles.get(ref) or {}
        grouped[profile.get("type") or "unknown"].append(ref)
    return dict(sorted(grouped.items()))


def candidate_is_official(candidate, record, source_profiles):
    refs = source_ref_groups(record, source_profiles)
    blob = text_blob(
        candidate.get("creator"),
        candidate.get("credit"),
        candidate.get("source"),
        candidate.get("title"),
        candidate.get("commons_file_page"),
        (record.get("rich_embed") or {}).get("preferred_source_url"),
        " ".join(refs.get("official_institutional") or []),
    )
    return any(term in blob for term in OFFICIAL_TERMS)


def partner_refs(record, source_profiles):
    refs = record.get("source_candidates") or {}
    partners = []
    for ref in refs.get("partner_refs") or []:
        profile = source_profiles.get(ref) or {}
        if ref != "partner_media_grant_needed" or profile.get("type") == "partner_or_ngo":
            partners.append(ref)
    for ref in refs.get("official_or_institutional_refs") or []:
        profile = source_profiles.get(ref) or {}
        if profile.get("type") == "partner_or_ngo":
            partners.append(ref)
    return sorted(set(partners))


def route_record(record, source_profiles):
    primary = record.get("primary") or {}
    candidate = primary.get("candidate") or {}
    rights_status = candidate.get("rights_status") or "none"
    flags = candidate.get("flags") or []
    rich_embed = record.get("rich_embed") or {}
    rich_url = rich_embed.get("preferred_source_url")
    rich_domain = url_domain(rich_url)
    official_candidate = candidate_is_official(candidate, record, source_profiles)
    partners = partner_refs(record, source_profiles)

    if flags and any(flag in HIGH_RISK_FLAGS for flag in flags):
        route = "ethics_replacement_or_manual_review"
        priority = "P0"
        rationale = "Automated review found high-risk welfare, captivity, distress, or individual/tagged-animal flags."
    elif flags:
        route = "ethics_note_review"
        priority = "P1"
        rationale = "Candidate has automated review flags that may still be approvable after source and crop review."
    elif official_candidate and rights_status == "public-domain-or-cc0-candidate":
        route = "official_public_domain_fast_track"
        priority = "P1"
        rationale = "Candidate appears official/institutional and public-domain/CC0-style, pending image-level review."
    elif rights_status == "public-domain-or-cc0-candidate":
        route = "open_public_domain_review"
        priority = "P1"
        rationale = "Candidate has public-domain/CC0-style rights metadata but still needs source and species review."
    elif rights_status in {"cc-by-candidate", "cc-by-sa-candidate"}:
        route = "open_license_attribution_review"
        priority = "P2"
        rationale = "Candidate may be reusable with attribution/share-alike obligations after review."
    elif primary.get("status") == "rich_embed_only" or (not candidate and rich_url):
        route = "rich_embed_only_until_grant"
        priority = "P2"
        rationale = "Use a source card until image reuse rights or a partner grant exists."
    else:
        route = "partner_grant_or_new_candidate_needed"
        priority = "P2"
        rationale = "No low-friction approvable candidate is ready; pursue a partner grant or new source."

    actions = [
        "Open the original source page and candidate file page.",
        "Confirm image-level rights, creator, credit line, and allowed surfaces.",
        "Confirm species match from caption, taxon page, partner assertion, or expert reviewer note.",
        "Reject or replace media with unsafe proximity, distress, captivity glamour, exact sensitive locations, or individual-animal risk.",
        "Write alt text, crop guidance, approved surfaces, blocked surfaces, and reviewer/date before approval.",
    ]
    if route.startswith("official"):
        actions.insert(1, "Confirm that the credited creator is actually an official/institutional source, not a third-party credit.")
    if route.startswith("open_license"):
        actions.insert(1, "Capture exact attribution text and any share-alike or modification obligations.")
    if route.startswith("ethics"):
        actions.insert(0, "Review this before other candidates; either demote it or document why the flag is acceptable.")
    if partners:
        actions.append("If reuse is unclear, request a written media grant from the listed partner/NGO or institution.")

    return {
        "artifact_id": record.get("artifact_id"),
        "species_page": record.get("species_page"),
        "common_name": record.get("common_name"),
        "scientific_name": record.get("scientific_name"),
        "taxon_group": record.get("taxon_group"),
        "priority": priority,
        "route": route,
        "rationale": rationale,
        "rich_embed_url": rich_url,
        "rich_embed_domain": rich_domain,
        "source_ref_groups": source_ref_groups(record, source_profiles),
        "partner_refs": partners,
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
            "rights_status": rights_status,
            "flags": flags,
            "score": candidate.get("score"),
            "official_institutional_signal": official_candidate,
            "public_use": False,
        },
        "recommended_actions": actions,
    }


def render_routing_markdown(payload):
    lines = [
        "# Species Media Source Routing",
        "",
        f"Generated: {payload['generated_at']}",
        "",
        "This packet converts the registry into practical review lanes. It does not approve images.",
        "",
        "## Summary",
        "",
    ]
    summary = payload["summary"]
    lines.append(f"- Species records: {summary['species_records']}")
    lines.append("- Routes: " + ", ".join(f"{k}={v}" for k, v in summary["route_counts"].items()))
    lines.append("- Priorities: " + ", ".join(f"{k}={v}" for k, v in summary["priority_counts"].items()))
    lines.append(f"- Partner/grant candidates: {summary['partner_grant_candidate_count']}")
    lines.append("")
    lines.extend(
        [
            "## Route Board",
            "",
            "| Priority | Species | Route | Candidate rights | Flags | Rich source |",
            "|---|---|---|---|---|---|",
        ]
    )
    for record in payload["records"]:
        candidate = record["candidate"]
        flags = ", ".join(candidate.get("flags") or []) or "-"
        rich = record.get("rich_embed_domain") or "-"
        rights = candidate.get("rights_status") or "-"
        lines.append(
            f"| {record['priority']} | {record['common_name']} | `{record['route']}` | `{rights}` | {flags} | {rich} |"
        )

    lines.extend(["", "## Per-Species Actions", ""])
    for record in payload["records"]:
        lines.append(f"### {record['common_name']} ({record['scientific_name']})")
        lines.append("")
        lines.append(f"- Route: `{record['route']}`")
        lines.append(f"- Priority: `{record['priority']}`")
        lines.append(f"- Rationale: {record['rationale']}")
        if record.get("rich_embed_url"):
            lines.append(f"- Rich source: {record['rich_embed_url']}")
        candidate = record["candidate"]
        if candidate.get("commons_file_page"):
            lines.append(f"- Candidate: {candidate.get('title')} - {candidate.get('commons_file_page')}")
        if record.get("partner_refs"):
            lines.append("- Partner/source refs: " + ", ".join(f"`{ref}`" for ref in record["partner_refs"]))
        lines.append("- Actions:")
        for action in record["recommended_actions"]:
            lines.append(f"  - {action}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def render_partner_queue(payload):
    grouped = defaultdict(list)
    for record in payload["records"]:
        route = record["route"]
        if record.get("partner_refs") or route in {
            "partner_grant_or_new_candidate_needed",
            "rich_embed_only_until_grant",
            "ethics_replacement_or_manual_review",
            "ethics_note_review",
        }:
            domain = record.get("rich_embed_domain") or "source-to-confirm"
            grouped[domain].append(record)

    lines = [
        "# Species Partner And Grant Queue",
        "",
        f"Generated: {payload['generated_at']}",
        "",
        "Use this packet for NGO, partner, institution, or photographer outreach when reuse rights are unclear or a stronger official image is preferred.",
        "",
        "## Grant Template Fields",
        "",
        "- Species and artifact id",
        "- Exact media requested or source page URL",
        "- Approved surfaces: species page, visual explorer, education deck, social crop, grant report",
        "- Required credit line and license wording",
        "- Any blocked surfaces, embargoes, or revocation terms",
        "- Welfare/location constraints and whether metadata/EXIF should be stripped",
        "- Contact, date, and written permission record",
        "",
    ]

    for domain, records in sorted(grouped.items()):
        lines.append(f"## {domain}")
        lines.append("")
        for record in sorted(records, key=lambda item: (item["priority"], item["common_name"])):
            candidate = record["candidate"]
            lines.append(f"### {record['common_name']} ({record['artifact_id']})")
            lines.append("")
            lines.append(f"- Route: `{record['route']}`")
            lines.append(f"- Priority: `{record['priority']}`")
            if record.get("rich_embed_url"):
                lines.append(f"- Source page: {record['rich_embed_url']}")
            if candidate.get("commons_file_page"):
                lines.append(f"- Current candidate: {candidate.get('commons_file_page')}")
            if candidate.get("flags"):
                lines.append("- Automated flags: " + ", ".join(f"`{flag}`" for flag in candidate["flags"]))
            if record.get("partner_refs"):
                lines.append("- Registry refs: " + ", ".join(f"`{ref}`" for ref in record["partner_refs"]))
            lines.append("- Ask: written permission or alternative official media with image-level license, credit, and welfare/location constraints.")
            lines.append("")

    if not grouped:
        lines.append("No partner/grant queue items.")
    return "\n".join(lines).rstrip() + "\n"


def main():
    registry = load_yaml(REGISTRY_PATH)
    source_profiles = registry.get("source_profiles") or {}
    records = [route_record(record, source_profiles) for record in registry.get("records") or []]
    route_counts = Counter(record["route"] for record in records)
    priority_counts = Counter(record["priority"] for record in records)
    partner_count = sum(1 for record in records if record.get("partner_refs") or record["route"].startswith("partner"))

    payload = {
        "version": date.today().isoformat(),
        "generated_at": date.today().isoformat(),
        "source_registry": rel(REGISTRY_PATH),
        "policy": {
            "candidate_public_use": False,
            "routing_is_not_approval": True,
            "google_images_discovery_only": True,
            "partner_grants_require_written_permission": True,
        },
        "summary": {
            "species_records": len(records),
            "route_counts": dict(sorted(route_counts.items())),
            "priority_counts": dict(sorted(priority_counts.items())),
            "partner_grant_candidate_count": partner_count,
        },
        "records": records,
    }

    ROUTING_PATH.write_text(yaml.safe_dump(payload, sort_keys=False, allow_unicode=False), encoding="utf-8")
    REVIEW_DIR.mkdir(parents=True, exist_ok=True)
    stamp = date.today().isoformat()
    routing_md = REVIEW_DIR / f"species-media-source-routing-{stamp}.md"
    partner_md = REVIEW_DIR / f"species-media-grant-queue-{stamp}.md"
    routing_md.write_text(render_routing_markdown(payload), encoding="utf-8")
    partner_md.write_text(render_partner_queue(payload), encoding="utf-8")

    print(f"Wrote {rel(ROUTING_PATH)}")
    print(f"Wrote {rel(routing_md)}")
    print(f"Wrote {rel(partner_md)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
