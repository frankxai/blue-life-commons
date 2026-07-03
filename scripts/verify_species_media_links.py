#!/usr/bin/env python3
"""Verify external links used by the species media registry.

This checks rich source embeds and Commons file pages by default. Direct
candidate image URLs can be checked with ``--include-image-urls``, but they are
excluded from the default run to avoid high-volume upload.wikimedia.org checks.
It is designed as a reviewer report, not a brittle CI gate. Use
``--fail-on-broken`` only when network conditions are stable enough.

Usage:
  python scripts/verify_species_media_links.py
  python scripts/verify_species_media_links.py --fail-on-broken
"""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import date
from pathlib import Path
import time
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen

import yaml

ROOT = Path(__file__).resolve().parent.parent
REGISTRY_PATH = ROOT / "content" / "media" / "species-media-registry.yaml"
REVIEW_DIR = ROOT / "content" / "media" / "review-packs"

USER_AGENT = "BlueLifeCommonsMediaLinkVerifier/1.0 (+https://github.com/frankxai/blue-life-commons)"


def rel(path: Path):
    return path.relative_to(ROOT).as_posix()


def media_links(record, include_image_urls=False):
    rich_embed = record.get("rich_embed") or {}
    candidate = ((record.get("primary") or {}).get("candidate") or {})
    links = []
    if rich_embed.get("preferred_source_url"):
        links.append(
            {
                "kind": "rich_embed_source",
                "url": rich_embed["preferred_source_url"],
            }
        )
    if candidate.get("commons_file_page"):
        links.append(
            {
                "kind": "candidate_file_page",
                "url": candidate["commons_file_page"],
            }
        )
    if include_image_urls and candidate.get("image_url"):
        links.append(
            {
                "kind": "candidate_image_url",
                "url": candidate["image_url"],
            }
        )
    return links


def check_url(item, timeout):
    url = item["url"]
    started = time.perf_counter()
    result = {
        **item,
        "domain": urlparse(url).netloc.lower().removeprefix("www."),
        "ok": False,
        "status_code": None,
        "method": None,
        "elapsed_ms": None,
        "error": None,
    }

    for method in ["HEAD", "GET"]:
        request = Request(url, headers={"User-Agent": USER_AGENT}, method=method)
        try:
            with urlopen(request, timeout=timeout) as response:
                result["status_code"] = response.status
                result["method"] = method
                result["ok"] = 200 <= response.status < 400
                break
        except HTTPError as error:
            result["status_code"] = error.code
            result["method"] = method
            result["ok"] = 200 <= error.code < 400
            result["error"] = str(error)
            if method == "HEAD" and error.code in {403, 405, 429, 500, 501, 503}:
                continue
            break
        except URLError as error:
            result["method"] = method
            result["error"] = str(error.reason)
            if method == "HEAD":
                continue
            break
        except Exception as error:  # noqa: BLE001 - report verifier failures without hiding the URL.
            result["method"] = method
            result["error"] = str(error)
            if method == "HEAD":
                continue
            break

    result["elapsed_ms"] = round((time.perf_counter() - started) * 1000)
    return result


def render_markdown(payload):
    summary = payload["summary"]
    lines = [
        "# Species Media Link Check",
        "",
        f"Generated: {payload['generated_at']}",
        "",
        "This report verifies source URLs used for review. A failed or blocked URL is not an approval decision; it is a reviewer follow-up.",
        "",
        "## Summary",
        "",
        f"- Species records: {summary['species_records']}",
        f"- Links checked: {summary['links_checked']}",
        f"- Reachable: {summary['reachable']}",
        f"- Broken or blocked: {summary['broken_or_blocked']}",
        "",
        "## Broken Or Blocked",
        "",
    ]

    broken = [item for item in payload["links"] if not item.get("ok")]
    if broken:
        lines.extend(["| Species | Kind | Status | Domain | URL |", "|---|---|---:|---|---|"])
        for item in broken:
            status = item.get("status_code") or item.get("error") or "unknown"
            lines.append(
                f"| {item['common_name']} | `{item['kind']}` | {status} | {item.get('domain') or '-'} | {item['url']} |"
            )
    else:
        lines.append("No broken or blocked links detected in this run.")

    lines.extend(["", "## All Links", "", "| Species | Kind | Status | Domain | URL |", "|---|---|---:|---|---|"])
    for item in payload["links"]:
        status = item.get("status_code") if item.get("status_code") is not None else item.get("error") or "unknown"
        marker = "ok" if item.get("ok") else "review"
        lines.append(
            f"| {item['common_name']} | `{item['kind']}` | {marker}:{status} | {item.get('domain') or '-'} | {item['url']} |"
        )
    return "\n".join(lines).rstrip() + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--timeout", type=float, default=12.0, help="Per-request timeout in seconds.")
    parser.add_argument("--workers", type=int, default=6, help="Parallel link checks.")
    parser.add_argument(
        "--include-image-urls",
        action="store_true",
        help="Also verify direct candidate image URLs. This can trigger Wikimedia rate limits.",
    )
    parser.add_argument("--fail-on-broken", action="store_true", help="Exit 1 if any link is broken or blocked.")
    args = parser.parse_args()

    registry = yaml.safe_load(REGISTRY_PATH.read_text(encoding="utf-8")) or {}
    checks = []
    for record in registry.get("records") or []:
        for link in media_links(record, include_image_urls=args.include_image_urls):
            checks.append(
                {
                    "artifact_id": record.get("artifact_id"),
                    "species_page": record.get("species_page"),
                    "common_name": record.get("common_name"),
                    "scientific_name": record.get("scientific_name"),
                    **link,
                }
            )

    results = []
    with ThreadPoolExecutor(max_workers=max(1, args.workers)) as pool:
        futures = [pool.submit(check_url, item, args.timeout) for item in checks]
        for future in as_completed(futures):
            results.append(future.result())

    results.sort(key=lambda item: (item["artifact_id"], item["kind"], item["url"]))
    reachable = sum(1 for item in results if item.get("ok"))
    broken = len(results) - reachable
    payload = {
        "version": date.today().isoformat(),
        "generated_at": date.today().isoformat(),
        "source_registry": rel(REGISTRY_PATH),
        "policy": {
            "link_check_is_not_media_approval": True,
            "candidate_public_use": False,
            "direct_image_urls_checked": args.include_image_urls,
            "network_failures_require_recheck_before_rejection": True,
        },
        "summary": {
            "species_records": len(registry.get("records") or []),
            "links_checked": len(results),
            "reachable": reachable,
            "broken_or_blocked": broken,
        },
        "links": results,
    }

    REVIEW_DIR.mkdir(parents=True, exist_ok=True)
    stamp = date.today().isoformat()
    yaml_path = REVIEW_DIR / f"species-media-link-check-{stamp}.yaml"
    md_path = REVIEW_DIR / f"species-media-link-check-{stamp}.md"
    yaml_path.write_text(yaml.safe_dump(payload, sort_keys=False, allow_unicode=False), encoding="utf-8")
    md_path.write_text(render_markdown(payload), encoding="utf-8")

    print(f"Wrote {rel(yaml_path)}")
    print(f"Wrote {rel(md_path)}")
    print(f"Species media links: {len(results)} checked, {reachable} reachable, {broken} broken/blocked.")
    return 1 if args.fail_on_broken and broken else 0


if __name__ == "__main__":
    raise SystemExit(main())
