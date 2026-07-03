#!/usr/bin/env python3
"""Collect Wikimedia Commons candidate media for species records.

This script does not approve, download, or publish images. It queries Wikimedia
Commons file metadata so reviewers can inspect license, creator, source, and
species match before promoting a candidate into the species media registry.

Usage:
  python scripts/collect_wikimedia_species_media.py --limit-species 3
  python scripts/collect_wikimedia_species_media.py --per-species 2 --out content/media/candidates/wikimedia-species-media-candidates-2026-07-03.yaml
"""
from __future__ import annotations

import argparse
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
API = "https://commons.wikimedia.org/w/api.php"
USER_AGENT = "BlueLifeCommonsMediaCuration/0.1 (https://github.com/frankxai/blue-life-commons)"


def strip_markup(value):
    if value is None:
        return None
    text = re.sub(r"<[^>]+>", "", str(value))
    return html.unescape(text).strip() or None


def ext_value(extmetadata, key):
    value = (extmetadata or {}).get(key, {}).get("value")
    return strip_markup(value)


def commons_query(params):
    query = urlencode(params)
    request = Request(f"{API}?{query}", headers={"User-Agent": USER_AGENT})
    with urlopen(request, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def query_species(scientific_name, per_species):
    if not scientific_name:
        return []
    data = commons_query(
        {
            "action": "query",
            "generator": "search",
            "gsrnamespace": "6",
            "gsrsearch": f'filetype:bitmap "{scientific_name}"',
            "gsrlimit": str(per_species),
            "prop": "imageinfo",
            "iiprop": "url|mime|size|extmetadata",
            "format": "json",
            "formatversion": "2",
        }
    )

    candidates = []
    for page in (data.get("query") or {}).get("pages") or []:
        info = (page.get("imageinfo") or [{}])[0]
        ext = info.get("extmetadata") or {}
        license_short = ext_value(ext, "LicenseShortName")
        license_url = ext_value(ext, "LicenseUrl")
        usage_terms = ext_value(ext, "UsageTerms")
        candidates.append(
            {
                "title": page.get("title"),
                "commons_file_page": info.get("descriptionurl"),
                "image_url": info.get("url"),
                "mime": info.get("mime"),
                "width": info.get("width"),
                "height": info.get("height"),
                "creator": ext_value(ext, "Artist"),
                "credit": ext_value(ext, "Credit"),
                "source": ext_value(ext, "ImageDescription") or ext_value(ext, "ObjectName"),
                "license": license_short,
                "license_url": license_url,
                "usage_terms": usage_terms,
                "rights_status": classify_rights(license_short, license_url, usage_terms),
                "review_status": "candidate_needs_species_rights_ethics_review",
            }
        )
    return candidates


def classify_rights(license_short, license_url, usage_terms):
    text = " ".join(str(v or "") for v in (license_short, license_url, usage_terms)).lower()
    if not text:
        return "needs-review"
    if "noncommercial" in text or "by-nc" in text or "cc-by-nc" in text:
        return "blocked-noncommercial"
    if "no derivatives" in text or "by-nd" in text:
        return "needs-review-no-derivatives"
    if "public domain" in text or "cc0" in text:
        return "public-domain-or-cc0-candidate"
    if "cc by-sa" in text or "by-sa" in text:
        return "cc-by-sa-candidate"
    if "cc by" in text or "by/4.0" in text or "by/3.0" in text:
        return "cc-by-candidate"
    return "needs-review"


def load_records():
    data = yaml.safe_load(REGISTRY_PATH.read_text(encoding="utf-8"))
    return data.get("records") or []


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--per-species", type=int, default=6, help="Candidate files to request per species")
    parser.add_argument("--limit-species", type=int, help="Only query the first N registry records")
    parser.add_argument("--sleep", type=float, default=0.2, help="Delay between API calls")
    parser.add_argument("--out", help="Optional YAML output path relative to repo root")
    args = parser.parse_args()

    records = load_records()
    if args.limit_species:
        records = records[: args.limit_species]

    output = {
        "source": "wikimedia_commons",
        "generated_at": date.today().isoformat(),
        "policy": "Candidate metadata only. Do not publish until species match, image-level rights, creator credit, alt text, and ethics QA are approved.",
        "queries": [],
    }

    for record in records:
        scientific_name = record.get("scientific_name")
        candidates = query_species(scientific_name, args.per_species)
        output["queries"].append(
            {
                "artifact_id": record.get("artifact_id"),
                "species_page": record.get("species_page"),
                "common_name": record.get("common_name"),
                "scientific_name": scientific_name,
                "query": f'filetype:bitmap "{scientific_name}"',
                "candidates": candidates,
            }
        )
        time.sleep(args.sleep)

    rendered = yaml.safe_dump(output, sort_keys=False, allow_unicode=False, width=120)
    if args.out:
        out_path = ROOT / args.out
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(rendered, encoding="utf-8")
        print(f"Wrote {out_path.relative_to(ROOT)}")
    else:
        print(rendered)


if __name__ == "__main__":
    main()
