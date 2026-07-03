#!/usr/bin/env python3
"""Build a review pack from species media candidate caches.

This turns raw candidate metadata into a per-species review queue. It can also
stage the top candidate into ``content/media/species-media-registry.yaml`` as a
candidate primary image. Staging is not approval: the registry remains blocked
from public primary use until a reviewer fills the approved-primary fields.

Usage:
  python scripts/build_species_media_review_pack.py
  python scripts/build_species_media_review_pack.py --stage-registry-candidates
"""
from __future__ import annotations

import argparse
from collections import Counter
from datetime import date
from pathlib import Path
import re

import yaml

ROOT = Path(__file__).resolve().parent.parent
REGISTRY_PATH = ROOT / "content" / "media" / "species-media-registry.yaml"
CANDIDATE_DIR = ROOT / "content" / "media" / "candidates"
REVIEW_DIR = ROOT / "content" / "media" / "review-packs"

RIGHTS_SCORES = {
    "public-domain-or-cc0-candidate": 44,
    "cc-by-candidate": 38,
    "cc-by-sa-candidate": 32,
    "needs-review-no-derivatives": 2,
    "blocked-noncommercial": -50,
    "needs-review": 4,
}

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
]

DISTRESS_TERMS = [
    "dead",
    "injured",
    "stranded",
    "carcass",
    "entangled",
    "hook",
    "caught",
    "fishermen hit",
    "harvest",
]

CAPTIVITY_TERMS = ["aquarium", "zoo", "tank", "captive", "captivity"]

PROXIMITY_TERMS = [
    "diver",
    "swimmer",
    "surf",
    "wake",
    "close-up",
    "feeding",
    "petting",
]

SENSITIVITY_TERMS = ["nesting", "nest", "pup", "calf", "rookery", "haul-out", "haulout"]

INDIVIDUAL_OR_TAG_TERMS = ["tagged", "named", "individual", "patient", "rehab", "release"]

NON_PHOTO_TERMS = ["illustr", "drawing", "plate", "larousse", "sketch", "diagram", "painting"]


def load_yaml(path: Path):
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def latest_candidate_cache() -> Path:
    files = sorted(CANDIDATE_DIR.glob("wikimedia-species-media-candidates-*.yaml"))
    if not files:
        raise SystemExit("No Wikimedia candidate cache found. Run collect_wikimedia_species_media.py first.")
    return files[-1]


def text_blob(candidate):
    return " ".join(
        str(candidate.get(key) or "")
        for key in ["title", "creator", "credit", "source", "license", "usage_terms", "commons_file_page"]
    ).lower()


def candidate_flags(candidate):
    blob = text_blob(candidate)
    flags = []
    if any(term in blob for term in DISTRESS_TERMS):
        flags.append("distress_or_mortality_review")
    if any(term in blob for term in CAPTIVITY_TERMS):
        flags.append("captivity_or_facility_review")
    if any(term in blob for term in PROXIMITY_TERMS):
        flags.append("human_or_vehicle_proximity_review")
    if any(term in blob for term in SENSITIVITY_TERMS):
        flags.append("sensitive_life_stage_or_site_review")
    if any(term in blob for term in INDIVIDUAL_OR_TAG_TERMS):
        flags.append("individual_or_tagged_animal_review")
    if any(term in blob for term in NON_PHOTO_TERMS):
        flags.append("non_photo_or_historical_media_review")
    if not candidate.get("creator") and not candidate.get("credit"):
        flags.append("missing_creator_or_credit")
    if not candidate.get("license"):
        flags.append("missing_license")
    return flags


def score_candidate(candidate):
    rights_status = candidate.get("rights_status") or "needs-review"
    score = RIGHTS_SCORES.get(rights_status, 0)
    blob = text_blob(candidate)
    flags = candidate_flags(candidate)

    if any(term in blob for term in OFFICIAL_TERMS):
        score += 22
    if candidate.get("creator"):
        score += 6
    if candidate.get("credit"):
        score += 5
    if candidate.get("license"):
        score += 4
    if candidate.get("commons_file_page") and candidate.get("image_url"):
        score += 4
    if (candidate.get("width") or 0) >= 1200 and (candidate.get("height") or 0) >= 800:
        score += 4

    penalties = {
        "distress_or_mortality_review": 55,
        "captivity_or_facility_review": 48,
        "human_or_vehicle_proximity_review": 22,
        "sensitive_life_stage_or_site_review": 18,
        "individual_or_tagged_animal_review": 22,
        "non_photo_or_historical_media_review": 24,
        "missing_creator_or_credit": 10,
        "missing_license": 15,
    }
    for flag in flags:
        score -= penalties.get(flag, 0)
    return score, flags


def asset_id_for(record, candidate):
    title = candidate.get("title") or "candidate"
    slug = record.get("slug") or record.get("artifact_id")
    normalized = re.sub(r"^file:", "", title, flags=re.IGNORECASE)
    normalized = re.sub(r"\.[a-z0-9]+$", "", normalized, flags=re.IGNORECASE)
    normalized = re.sub(r"[^a-z0-9]+", "-", normalized.lower()).strip("-")
    return f"{record.get('artifact_id')}-wikimedia-{normalized[:48]}"


def summarize_candidate(record, candidate):
    score, flags = score_candidate(candidate)
    return {
        "asset_id": asset_id_for(record, candidate),
        "score": score,
        "flags": flags,
        "title": candidate.get("title"),
        "commons_file_page": candidate.get("commons_file_page"),
        "image_url": candidate.get("image_url"),
        "creator": candidate.get("creator"),
        "credit": candidate.get("credit"),
        "license": candidate.get("license"),
        "license_url": candidate.get("license_url"),
        "rights_status": candidate.get("rights_status"),
        "source": candidate.get("source"),
        "review_status": "candidate_needs_species_rights_ethics_review",
    }


def choose_top(record, candidates):
    summaries = [summarize_candidate(record, c) for c in candidates]
    summaries.sort(key=lambda c: c["score"], reverse=True)
    return summaries[0] if summaries else None, summaries


def readiness(candidate):
    if candidate is None:
        return "needs_candidate_source"
    if any(
        flag in candidate["flags"]
        for flag in [
            "distress_or_mortality_review",
            "captivity_or_facility_review",
            "individual_or_tagged_animal_review",
        ]
    ):
        return "manual_review_high_risk"
    if candidate["rights_status"] == "public-domain-or-cc0-candidate" and candidate["score"] >= 60:
        return "fast_track_rights_ethics_review"
    if candidate["rights_status"] in {"cc-by-candidate", "cc-by-sa-candidate"}:
        return "attribution_and_ethics_review"
    return "manual_review"


def build_pack(registry, candidate_cache):
    records_by_id = {r["artifact_id"]: r for r in registry.get("records") or []}
    recommendations = []
    for query in candidate_cache.get("queries") or []:
        record = records_by_id.get(query.get("artifact_id"))
        if not record:
            continue
        top, ranked = choose_top(record, query.get("candidates") or [])
        recommendations.append(
            {
                "artifact_id": record["artifact_id"],
                "species_page": record["species_page"],
                "common_name": record.get("common_name"),
                "scientific_name": record.get("scientific_name"),
                "readiness": readiness(top),
                "top_candidate": top,
                "ranked_candidates": ranked,
                "review_checklist": [
                    "Open Commons file page and original source.",
                    "Confirm image-level license, creator, credit, and commercial-use compatibility.",
                    "Confirm species match from source caption, taxon page, partner assertion, or expert review.",
                    "Reject or demote imagery with distress, unsafe proximity, captivity glamour, or sensitive location leakage.",
                    "Write alt text and crop guidance before approval.",
                ],
            }
        )
    return recommendations


def render_markdown(pack, source_path):
    counts = Counter(item["readiness"] for item in pack)
    rights = Counter((item.get("top_candidate") or {}).get("rights_status") or "none" for item in pack)
    lines = [
        f"# Species Media Review Pack - {date.today().isoformat()}",
        "",
        "> Review-only. These candidates are not approved primary species media until a reviewer completes rights, species-match, ethics, alt-text, and crop checks.",
        "",
        f"Source cache: `{source_path.relative_to(ROOT).as_posix()}`",
        "",
        "## Summary",
        "",
        f"- Species records: {len(pack)}",
        f"- Readiness: {', '.join(f'{k}={v}' for k, v in sorted(counts.items()))}",
        f"- Rights status: {', '.join(f'{k}={v}' for k, v in sorted(rights.items()))}",
        "",
        "## Top Candidate Queue",
        "",
        "| Species | Readiness | Candidate | Rights | Flags | Commons |",
        "|---|---|---|---|---|---|",
    ]
    for item in pack:
        candidate = item.get("top_candidate") or {}
        flags = ", ".join(candidate.get("flags") or []) or "none"
        title = (candidate.get("title") or "none").replace("|", "\\|")
        common = item["common_name"].replace("|", "\\|")
        commons = candidate.get("commons_file_page") or ""
        link = f"[file]({commons})" if commons else ""
        lines.append(
            f"| {common} | `{item['readiness']}` | {title} | `{candidate.get('rights_status') or ''}` | {flags} | {link} |"
        )

    lines.extend(["", "## Per-Species Review Cards", ""])
    for item in pack:
        candidate = item.get("top_candidate") or {}
        lines.extend(
            [
                f"### {item['common_name']} (*{item['scientific_name']}*)",
                "",
                f"- Species page: `{item['species_page']}`",
                f"- Readiness: `{item['readiness']}`",
                f"- Top candidate: {candidate.get('title') or 'None'}",
                f"- Commons file: {candidate.get('commons_file_page') or 'None'}",
                f"- Image URL: {candidate.get('image_url') or 'None'}",
                f"- Creator: {candidate.get('creator') or 'Unknown'}",
                f"- Credit: {candidate.get('credit') or 'Unknown'}",
                f"- License: {candidate.get('license') or 'Unknown'}",
                f"- Rights status: `{candidate.get('rights_status') or 'none'}`",
                f"- Flags: {', '.join(candidate.get('flags') or []) or 'none'}",
                "",
                "Review checklist:",
            ]
        )
        for check in item["review_checklist"]:
            lines.append(f"- [ ] {check}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def stage_registry(registry, pack):
    by_id = {item["artifact_id"]: item for item in pack}
    for record in registry.get("records") or []:
        item = by_id.get(record.get("artifact_id"))
        candidate = (item or {}).get("top_candidate")
        if not candidate:
            continue
        primary = record.setdefault("primary", {})
        primary["status"] = "candidate"
        primary["approved_asset_id"] = None
        primary["approved_path"] = None
        primary["rights_status"] = None
        primary["qa_status"] = "candidate_review"
        primary["candidate"] = {
            "asset_id": candidate["asset_id"],
            "provider": "wikimedia_commons",
            "title": candidate.get("title"),
            "commons_file_page": candidate.get("commons_file_page"),
            "image_url": candidate.get("image_url"),
            "creator": candidate.get("creator"),
            "credit": candidate.get("credit"),
            "license": candidate.get("license"),
            "license_url": candidate.get("license_url"),
            "rights_status": candidate.get("rights_status"),
            "score": candidate.get("score"),
            "flags": candidate.get("flags") or [],
            "review_status": "candidate_needs_species_rights_ethics_review",
        }
        record["media_status"] = "primary_candidate_review"
        record["next_action"] = (
            f"Review staged Wikimedia Commons candidate for {record.get('common_name')}: "
            "confirm image-level rights, species match, ethics/location safety, alt text, and crop before approval."
        )
    registry["updated"] = date.today().isoformat()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--registry", default=REGISTRY_PATH)
    parser.add_argument("--candidates", default=None)
    parser.add_argument("--out-md", default=None)
    parser.add_argument("--out-yaml", default=None)
    parser.add_argument("--stage-registry-candidates", action="store_true")
    args = parser.parse_args()

    registry_path = Path(args.registry)
    candidate_path = Path(args.candidates) if args.candidates else latest_candidate_cache()
    out_md = Path(args.out_md) if args.out_md else REVIEW_DIR / f"species-media-review-pack-{date.today().isoformat()}.md"
    out_yaml = Path(args.out_yaml) if args.out_yaml else REVIEW_DIR / f"species-media-review-pack-{date.today().isoformat()}.yaml"

    registry = load_yaml(registry_path)
    candidate_cache = load_yaml(candidate_path)
    pack = build_pack(registry, candidate_cache)

    REVIEW_DIR.mkdir(parents=True, exist_ok=True)
    out_yaml.write_text(
        yaml.safe_dump(
            {
                "generated_at": date.today().isoformat(),
                "source_cache": candidate_path.relative_to(ROOT).as_posix(),
                "policy": "Review-only candidate pack. Do not publish as primary media until approval fields are completed in the registry.",
                "recommendations": pack,
            },
            sort_keys=False,
            allow_unicode=False,
            width=120,
        ),
        encoding="utf-8",
    )
    out_md.write_text(render_markdown(pack, candidate_path), encoding="utf-8")

    if args.stage_registry_candidates:
        stage_registry(registry, pack)
        registry_path.write_text(yaml.safe_dump(registry, sort_keys=False, allow_unicode=False, width=120), encoding="utf-8")

    print(f"Wrote {out_md.relative_to(ROOT)}")
    print(f"Wrote {out_yaml.relative_to(ROOT)}")
    if args.stage_registry_candidates:
        print(f"Staged candidates in {registry_path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
