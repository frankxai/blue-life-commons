#!/usr/bin/env python3
"""Build reviewer-only Wikimedia Commons rights snapshots.

The registry stores staged candidate media. This script refreshes file-level
metadata from the Commons API for those candidates so reviewers can compare the
registry against source metadata before approving or rejecting a primary image.

It does not approve media, download images, or make candidate URLs public.

Usage:
  python scripts/build_species_media_commons_rights_snapshots.py
"""
from __future__ import annotations

from collections import Counter
from datetime import date
import html
import json
from pathlib import Path
import re
import time
from urllib.parse import urlencode
from urllib.request import Request, urlopen

import yaml

ROOT = Path(__file__).resolve().parent.parent
REGISTRY_PATH = ROOT / "content" / "media" / "species-media-registry.yaml"
APPROVAL_QUEUE_PATH = ROOT / "content" / "media" / "species-media-approval-queue.yaml"
COMMONS_SNAPSHOTS_PATH = ROOT / "content" / "media" / "species-media-commons-rights-snapshots.yaml"
REVIEW_PACK_PATH = (
    ROOT
    / "content"
    / "media"
    / "review-packs"
    / f"species-media-commons-rights-snapshots-{date.today().isoformat()}.md"
)

API = "https://commons.wikimedia.org/w/api.php"
USER_AGENT = "BlueLifeCommonsMediaCuration/0.2 (https://github.com/frankxai/blue-life-commons)"

DISTRESS_TERMS = [
    "dead",
    "injured",
    "stranded",
    "carcass",
    "entangled",
    "hook",
    "caught",
    "harvest",
]

CAPTIVITY_TERMS = ["aquarium", "zoo", "tank", "captive", "captivity"]
PROXIMITY_TERMS = ["diver", "swimmer", "surf", "wake", "feeding", "petting", "boat", "ship", "vessel"]
SENSITIVITY_TERMS = ["nesting", "nest", "pup", "calf", "rookery", "haul-out", "haulout"]
INDIVIDUAL_OR_TAG_TERMS = ["tagged", "named", "individual", "patient", "rehab", "release"]


def strip_markup(value):
    if value is None:
        return None
    text = re.sub(r"<[^>]+>", "", str(value))
    return html.unescape(text).strip() or None


def normalize_text(value):
    return re.sub(r"\s+", " ", strip_markup(value) or "").strip()


def text_equal(left, right):
    return normalize_text(left).casefold() == normalize_text(right).casefold()


def ext_value(extmetadata, key):
    value = (extmetadata or {}).get(key, {}).get("value")
    return strip_markup(value)


def load_yaml(path: Path):
    if not path.exists():
        return {}
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def rel(path: Path):
    return path.relative_to(ROOT).as_posix()


def commons_query(params):
    query = urlencode(params)
    request = Request(f"{API}?{query}", headers={"User-Agent": USER_AGENT})
    with urlopen(request, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def query_file(title):
    return commons_query(
        {
            "action": "query",
            "titles": title,
            "prop": "imageinfo|categories",
            "iiprop": "url|mime|size|sha1|timestamp|user|extmetadata",
            "cllimit": "max",
            "format": "json",
            "formatversion": "2",
        }
    )


def classify_rights(license_short, license_url, usage_terms):
    text = " ".join(str(v or "") for v in (license_short, license_url, usage_terms)).lower()
    if not text:
        return "needs-review"
    if "noncommercial" in text or "by-nc" in text or "cc-by-nc" in text:
        return "blocked-noncommercial"
    if "no derivatives" in text or "by-nd" in text:
        return "needs-review-no-derivatives"
    if "public domain" in text or "cc0" in text or "pd-" in text:
        return "public-domain-or-cc0-candidate"
    if "cc by-sa" in text or "by-sa" in text:
        return "cc-by-sa-candidate"
    if "cc by" in text or "by/4.0" in text or "by/3.0" in text:
        return "cc-by-candidate"
    return "needs-review"


def evidence_blob(*values):
    return " ".join(str(value or "") for value in values).lower()


def ethics_flags(blob):
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
    return sorted(set(flags))


def species_terms(registry_record):
    terms = [
        registry_record.get("common_name"),
        registry_record.get("scientific_name"),
        registry_record.get("slug"),
    ]
    terms.extend(registry_record.get("species_slugs") or [])
    return sorted({term.lower().replace("-", " ") for term in terms if term})


def build_record(registry_record, approval_record, sleep_seconds):
    artifact_id = registry_record.get("artifact_id")
    primary = registry_record.get("primary") or {}
    candidate = primary.get("candidate") or primary.get("approved_from_candidate") or {}
    title = candidate.get("title")
    base = {
        "artifact_id": artifact_id,
        "ownership_key": f"{artifact_id}|{registry_record.get('species_page')}",
        "species_page": registry_record.get("species_page"),
        "common_name": registry_record.get("common_name"),
        "scientific_name": registry_record.get("scientific_name"),
        "candidate": {
            "asset_id": candidate.get("asset_id"),
            "provider": candidate.get("provider"),
            "title": title,
            "commons_file_page": candidate.get("commons_file_page"),
            "image_url": candidate.get("image_url"),
            "registry_rights_status": candidate.get("rights_status"),
            "public_use": False,
            "reviewer_only": True,
        },
        "snapshot_status": "skipped",
        "snapshot_errors": [],
    }
    if candidate.get("provider") != "wikimedia_commons" or not title:
        base["snapshot_errors"].append("candidate is not a Wikimedia Commons file candidate")
        return base

    try:
        data = query_file(title)
        time.sleep(sleep_seconds)
    except Exception as exc:  # pragma: no cover - network failure path
        base["snapshot_status"] = "error"
        base["snapshot_errors"].append(f"commons API request failed: {exc}")
        return base

    pages = (data.get("query") or {}).get("pages") or []
    if not pages or pages[0].get("missing"):
        base["snapshot_status"] = "missing"
        base["snapshot_errors"].append("Commons API did not return a current file page")
        return base

    page = pages[0]
    info = (page.get("imageinfo") or [{}])[0]
    ext = info.get("extmetadata") or {}
    categories = [item.get("title") for item in page.get("categories") or [] if item.get("title")]
    license_short = ext_value(ext, "LicenseShortName")
    license_url = ext_value(ext, "LicenseUrl")
    usage_terms = ext_value(ext, "UsageTerms")
    api_rights = classify_rights(license_short, license_url, usage_terms)
    description = ext_value(ext, "ImageDescription")
    object_name = ext_value(ext, "ObjectName")
    artist = ext_value(ext, "Artist")
    credit = ext_value(ext, "Credit")
    source = ext_value(ext, "Source")
    permission = ext_value(ext, "Permission")
    attribution_required = ext_value(ext, "AttributionRequired")
    restrictions = ext_value(ext, "Restrictions")
    combined = evidence_blob(title, description, object_name, artist, credit, source, " ".join(categories))
    terms = species_terms(registry_record)
    matched_terms = [term for term in terms if term in combined]
    automated_flags = ethics_flags(combined)
    registry_flags = candidate.get("flags") or []
    checks = (approval_record or {}).get("checks") or {}

    base.update(
        {
            "snapshot_status": "fetched",
            "commons_api": {
                "endpoint": API,
                "title": page.get("title"),
                "pageid": page.get("pageid"),
                "descriptionurl": info.get("descriptionurl"),
                "direct_image_url": info.get("url"),
                "mime": info.get("mime"),
                "width": info.get("width"),
                "height": info.get("height"),
                "sha1": info.get("sha1"),
                "timestamp": info.get("timestamp"),
                "uploader": info.get("user"),
                "categories": categories[:80],
            },
            "commons_metadata": {
                "artist": artist,
                "credit": credit,
                "source": source,
                "object_name": object_name,
                "image_description": description,
                "license_short_name": license_short,
                "license_url": license_url,
                "usage_terms": usage_terms,
                "permission": permission,
                "attribution_required": attribution_required,
                "restrictions": restrictions,
            },
            "registry_alignment": {
                "asset_id_matches": bool(candidate.get("asset_id")),
                "title_matches": page.get("title") == title,
                "commons_file_page_matches": info.get("descriptionurl") == candidate.get("commons_file_page"),
                "image_url_matches": info.get("url") == candidate.get("image_url"),
                "creator_matches_api_artist": text_equal(candidate.get("creator"), artist),
                "credit_matches_api_credit_or_source": text_equal(candidate.get("credit"), credit)
                or text_equal(candidate.get("credit"), source),
                "rights_status_matches_api": candidate.get("rights_status") == api_rights,
            },
            "rights_evidence": {
                "api_rights_status": api_rights,
                "registry_rights_status": candidate.get("rights_status"),
                "license_metadata_present": bool(license_short or license_url or usage_terms),
                "creator_metadata_present": bool(artist),
                "credit_or_source_metadata_present": bool(credit or source),
                "permission_metadata_present": bool(permission),
                "reviewable_for_public_primary": api_rights
                in {
                    "public-domain-or-cc0-candidate",
                    "cc-by-candidate",
                    "cc-by-sa-candidate",
                },
                "commercial_and_derivative_use_requires_human_review": True,
            },
            "species_match_evidence": {
                "automated_text_signal": bool(matched_terms),
                "matched_terms": matched_terms,
                "species_match_requires_human_review": True,
            },
            "ethics_location_evidence": {
                "registry_flags": registry_flags,
                "api_text_flags": automated_flags,
                "ethics_requires_human_review": True,
                "sensitive_location_requires_human_review": True,
            },
            "approval_support": {
                "approval_queue_decision": (approval_record or {}).get("decision"),
                "checks_complete": sum(1 for value in checks.values() if value is True),
                "checks_total": len(checks),
                "suggested_next_checks": [
                    key
                    for key in [
                        "image_level_rights_verified",
                        "creator_and_credit_verified",
                        "commercial_and_derivative_use_checked",
                        "species_match_verified",
                        "ethics_checked",
                        "sensitive_location_checked",
                    ]
                    if checks.get(key) is not True
                ],
                "snapshot_is_not_approval": True,
            },
        }
    )
    return base


def build_payload(sleep_seconds):
    registry = load_yaml(REGISTRY_PATH)
    approval = load_yaml(APPROVAL_QUEUE_PATH)
    approval_by_id = {record.get("artifact_id"): record for record in approval.get("records") or []}
    records = [
        build_record(
            registry_record,
            approval_by_id.get(registry_record.get("artifact_id")),
            sleep_seconds,
        )
        for registry_record in registry.get("records") or []
    ]
    statuses = Counter(record.get("snapshot_status") for record in records)
    rights = Counter((record.get("rights_evidence") or {}).get("api_rights_status") or "none" for record in records)
    registry_rights = Counter((record.get("candidate") or {}).get("registry_rights_status") or "none" for record in records)
    matched = sum(1 for record in records if (record.get("species_match_evidence") or {}).get("automated_text_signal"))
    fetched = [record for record in records if record.get("snapshot_status") == "fetched"]
    rights_mismatches = [
        record["artifact_id"]
        for record in fetched
        if not (record.get("registry_alignment") or {}).get("rights_status_matches_api")
    ]
    url_mismatches = [
        record["artifact_id"]
        for record in fetched
        if not (record.get("registry_alignment") or {}).get("image_url_matches")
    ]
    flagged = [
        record["artifact_id"]
        for record in fetched
        if (record.get("ethics_location_evidence") or {}).get("api_text_flags")
        or (record.get("ethics_location_evidence") or {}).get("registry_flags")
    ]
    reviewable = sum(
        1
        for record in fetched
        if (record.get("rights_evidence") or {}).get("reviewable_for_public_primary") is True
    )
    return {
        "version": date.today().isoformat(),
        "generated_at": date.today().isoformat(),
        "sources": {
            "registry": rel(REGISTRY_PATH),
            "approval_queue": rel(APPROVAL_QUEUE_PATH),
            "commons_api": API,
        },
        "policy": {
            "reviewer_only": True,
            "contains_review_candidate_urls": True,
            "not_public_site_input": True,
            "candidate_public_use": False,
            "api_metadata_is_not_approval": True,
            "human_review_required_for_rights_species_ethics_crop": True,
            "no_download_performed": True,
        },
        "summary": {
            "species_records": len(records),
            "snapshot_status_counts": dict(sorted(statuses.items())),
            "api_rights_status_counts": dict(sorted(rights.items())),
            "registry_rights_status_counts": dict(sorted(registry_rights.items())),
            "reviewable_rights_snapshot_count": reviewable,
            "automated_species_text_signal_count": matched,
            "rights_mismatch_artifact_ids": rights_mismatches,
            "image_url_mismatch_artifact_ids": url_mismatches,
            "records_with_ethics_or_location_flags": flagged,
        },
        "records": records,
    }


def markdown(payload):
    summary = payload.get("summary") or {}
    lines = [
        "# Species Media Commons Rights Snapshots",
        "",
        f"Generated: {payload.get('generated_at')}",
        "",
        "Reviewer-only Commons API metadata for staged species media candidates. These snapshots support review, but they do not approve media, download images, or make candidate URLs safe for public species pages.",
        "",
        "## Summary",
        "",
        f"- Species records: {summary.get('species_records')}",
        "- Snapshot status: "
        + ", ".join(f"`{key}`={value}" for key, value in (summary.get("snapshot_status_counts") or {}).items()),
        "- API rights: "
        + ", ".join(f"`{key}`={value}" for key, value in (summary.get("api_rights_status_counts") or {}).items()),
        f"- Reviewable rights snapshots: {summary.get('reviewable_rights_snapshot_count')}",
        f"- Automated species text signals: {summary.get('automated_species_text_signal_count')}",
        f"- Rights mismatches: {len(summary.get('rights_mismatch_artifact_ids') or [])}",
        f"- Image URL mismatches: {len(summary.get('image_url_mismatch_artifact_ids') or [])}",
        f"- Records with ethics/location flags: {len(summary.get('records_with_ethics_or_location_flags') or [])}",
        "",
        "## Snapshot Board",
        "",
        "| Species | Status | API rights | Registry match | Species signal | Flags | Commons |",
        "|---|---|---|---|---|---|---|",
    ]
    for record in payload.get("records") or []:
        candidate = record.get("candidate") or {}
        rights = record.get("rights_evidence") or {}
        alignment = record.get("registry_alignment") or {}
        species = record.get("species_match_evidence") or {}
        ethics = record.get("ethics_location_evidence") or {}
        flags = ", ".join((ethics.get("api_text_flags") or []) + (ethics.get("registry_flags") or [])) or "-"
        match_bits = []
        for key in ["title_matches", "image_url_matches", "rights_status_matches_api"]:
            if key in alignment:
                match_bits.append(f"{key.replace('_matches', '')}={str(alignment.get(key)).lower()}")
        link = candidate.get("commons_file_page")
        link_cell = f"[file]({link})" if link else "-"
        lines.append(
            "| "
            + " | ".join(
                [
                    f"{record.get('common_name')}<br>`{record.get('artifact_id')}`",
                    f"`{record.get('snapshot_status')}`",
                    f"`{rights.get('api_rights_status') or 'none'}`",
                    "<br>".join(match_bits) or "-",
                    ", ".join(species.get("matched_terms") or []) or "-",
                    flags,
                    link_cell,
                ]
            )
            + " |"
        )
    lines.extend(["", "## Per-Species Review Notes", ""])
    for record in payload.get("records") or []:
        candidate = record.get("candidate") or {}
        metadata = record.get("commons_metadata") or {}
        rights = record.get("rights_evidence") or {}
        species = record.get("species_match_evidence") or {}
        approval = record.get("approval_support") or {}
        lines.extend(
            [
                f"### {record.get('common_name')} (*{record.get('scientific_name')}*)",
                "",
                f"- Artifact: `{record.get('artifact_id')}`",
                f"- Candidate: {candidate.get('commons_file_page') or '-'}",
                f"- Snapshot status: `{record.get('snapshot_status')}`",
                f"- API rights status: `{rights.get('api_rights_status') or 'none'}`",
                f"- Commons license: {metadata.get('license_short_name') or '-'} ({metadata.get('license_url') or 'no URL'})",
                f"- Commons artist: {metadata.get('artist') or '-'}",
                f"- Commons credit/source: {metadata.get('credit') or metadata.get('source') or '-'}",
                f"- Species text signal: {', '.join(species.get('matched_terms') or []) or '-'}",
                f"- Approval queue checks: {approval.get('checks_complete')}/{approval.get('checks_total')}",
                "- Required next step: human reviewer must confirm rights, species match, ethics/location safety, crop, alt text, and approved surfaces before promotion.",
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def main():
    payload = build_payload(sleep_seconds=0.15)
    COMMONS_SNAPSHOTS_PATH.parent.mkdir(parents=True, exist_ok=True)
    REVIEW_PACK_PATH.parent.mkdir(parents=True, exist_ok=True)
    COMMONS_SNAPSHOTS_PATH.write_text(
        yaml.safe_dump(payload, sort_keys=False, allow_unicode=False, width=120),
        encoding="utf-8",
    )
    REVIEW_PACK_PATH.write_text(markdown(payload), encoding="utf-8")
    print(f"Wrote {rel(COMMONS_SNAPSHOTS_PATH)}")
    print(f"Wrote {rel(REVIEW_PACK_PATH)}")
    print(
        "Species media Commons rights snapshots: "
        f"{payload['summary']['species_records']} records, "
        f"{payload['summary']['snapshot_status_counts'].get('fetched', 0)} fetched."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
