#!/usr/bin/env python3
"""Build a species media trace ledger.

The trace ledger proves ownership across the media system:

- species page frontmatter
- central registry
- public render contract
- sanitized public explorer record
- source-card fallback
- approval queue / curation workspace
- review-only candidate snapshot

It intentionally omits direct candidate image URLs and Commons file-page URLs.

Usage:
  python scripts/build_species_media_trace_ledger.py
"""
from __future__ import annotations

from collections import Counter
from datetime import date
from pathlib import Path
import sys

import yaml

ROOT = Path(__file__).resolve().parent.parent
SITE_DATA_PATH = ROOT / "content" / "media" / "species-media-site-data.json"
PUBLIC_EXPLORER_PATH = ROOT / "content" / "media" / "species-media-public-explorer-manifest.yaml"
CURATION_WORKSPACE_PATH = ROOT / "content" / "media" / "species-media-curation-workspace.yaml"
TRACE_LEDGER_PATH = ROOT / "content" / "media" / "species-media-trace-ledger.yaml"
REVIEW_PACK_PATH = ROOT / "content" / "media" / "review-packs" / f"species-media-trace-ledger-{date.today().isoformat()}.md"

BANNED_PUBLIC_STRINGS = set()


def load_yaml(path: Path):
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def load_json(path: Path):
    import json

    return json.loads(path.read_text(encoding="utf-8"))


def frontmatter(path: Path):
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return {}
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}
    return yaml.safe_load(parts[1]) or {}


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


def page_media_status(record, page_fm, public_record):
    artifact_id = record.get("artifact_id")
    media = page_fm.get("media") or {}
    embed = (media.get("embeds") or [{}])[0]
    render = media.get("render") or {}
    public_visual = ((record.get("render_contract") or {}).get("public_visual") or {})
    return {
        "has_media_block": bool(media),
        "registry_pointer_ok": media.get("registry_record")
        == f"content/media/species-media-registry.yaml#{artifact_id}",
        "render_pointer_ok": media.get("render_contract")
        == f"content/media/species-media-render-contract.yaml#{artifact_id}",
        "public_explorer_pointer_ok": media.get("public_explorer_record")
        == f"content/media/species-media-public-explorer-manifest.yaml#{artifact_id}",
        "embed_url_matches_public_visual": embed.get("url") == public_visual.get("source_url"),
        "render_strategy_matches": render.get("strategy")
        == ((record.get("render_contract") or {}).get("render_strategy")),
        "candidate_hidden": render.get("candidate_public_use") is False
        and render.get("candidate_thumbnail_allowed") is False,
    }


def build_record(record, public_record, workspace_record):
    artifact_id = record.get("artifact_id")
    species_path = ROOT / record.get("species_page")
    page_fm = frontmatter(species_path)
    candidate = record.get("candidate") or {}
    public_visual = ((record.get("render_contract") or {}).get("public_visual") or {})
    surface_rules = ((record.get("render_contract") or {}).get("surface_rules") or {})
    source_card = ((record.get("public_fallback") or {}).get("source_card") or {})
    curation = record.get("curation") or {}
    source_route = record.get("source_route") or {}
    workspace_record = workspace_record or {}
    approval_state = workspace_record.get("approval_state") or {}
    page_status = page_media_status(record, page_fm, public_record)

    media_strings = collect_strings(page_fm.get("media") or {})
    public_strings = collect_strings(public_record)
    candidate_urls = [candidate.get("image_url"), candidate.get("commons_file_page")]
    leaks = []
    for url in candidate_urls:
        if url and (url in media_strings or url in public_strings):
            leaks.append(url)
    for text in media_strings | public_strings:
        for banned in BANNED_PUBLIC_STRINGS:
            if banned in text:
                leaks.append(banned)

    integrity_checks = {
        **page_status,
        "species_page_exists": species_path.exists(),
        "artifact_id_matches_page": page_fm.get("id") == artifact_id,
        "website_path_matches_page": ((page_fm.get("outputs") or {}).get("website_path"))
        == record.get("website_path"),
        "public_visual_matches_manifest": (public_record.get("public_visual") or {}).get("source_url")
        == public_visual.get("source_url"),
        "source_card_verified": source_card.get("status") == "verified_source_card"
        and source_card.get("public_use") is True,
        "candidate_public_use_blocked": (not candidate.get("asset_id") or candidate.get("public_use") is False)
        and (record.get("render_contract") or {}).get("candidate_public_use") is False,
        "hero_image_rule_matches_status": surface_rules.get("species_page_hero_image_allowed")
        is (record.get("primary_status") == "approved"),
        "no_public_candidate_url_leak": not leaks,
    }

    trace_state = (
        "primary_image_ready"
        if surface_rules.get("species_page_hero_image_allowed") is True
        else "source_card_ready_candidate_pending"
    )

    return {
        "artifact_id": artifact_id,
        "ownership_key": f"{artifact_id}|{record.get('species_page')}",
        "species_page": record.get("species_page"),
        "website_path": record.get("website_path"),
        "taxon_group": record.get("taxon_group"),
        "common_name": record.get("common_name"),
        "scientific_name": record.get("scientific_name"),
        "species_slugs": record.get("species_slugs") or [],
        "trace_state": trace_state,
        "public_visual": {
            "kind": public_visual.get("kind"),
            "source_url": public_visual.get("source_url"),
            "domain": public_visual.get("domain"),
            "source_type": public_visual.get("source_type"),
            "render_strategy": (record.get("render_contract") or {}).get("render_strategy"),
            "public_use": public_visual.get("public_use") is True,
            "hero_image_allowed": surface_rules.get("species_page_hero_image_allowed") is True,
            "candidate_thumbnail_allowed": surface_rules.get("candidate_thumbnail_allowed") is True,
        },
        "candidate_review": {
            "asset_id": candidate.get("asset_id"),
            "provider": candidate.get("provider"),
            "rights_status": candidate.get("rights_status"),
            "license": candidate.get("license"),
            "review_status": candidate.get("review_status"),
            "flags": candidate.get("flags") or [],
            "public_use": False,
            "direct_urls_omitted": True,
        },
        "source_route": {
            "route": source_route.get("route"),
            "priority": source_route.get("priority"),
            "partner_refs": source_route.get("partner_refs") or [],
        },
        "curation": {
            "decision": curation.get("decision"),
            "checks_complete": curation.get("checks_complete") or 0,
            "checks_total": curation.get("checks_total") or 0,
            "recommended_batch": workspace_record.get("recommended_batch"),
            "batch_label": workspace_record.get("batch_label"),
            "workstream": workspace_record.get("workstream"),
            "promotion_allowed_now": approval_state.get("promotion_allowed_now") is True,
        },
        "page_media": {
            "registry_record": (page_fm.get("media") or {}).get("registry_record"),
            "render_contract": (page_fm.get("media") or {}).get("render_contract"),
            "public_explorer_record": (page_fm.get("media") or {}).get("public_explorer_record"),
        },
        "integrity_checks": integrity_checks,
        "trace_issues": [key for key, ok in integrity_checks.items() if ok is not True],
    }


def build_ledger():
    site_data = load_json(SITE_DATA_PATH)
    public_data = load_yaml(PUBLIC_EXPLORER_PATH)
    workspace = load_yaml(CURATION_WORKSPACE_PATH)
    public_by_id = {record.get("artifact_id"): record for record in public_data.get("records") or []}
    workspace_by_id = {record.get("artifact_id"): record for record in workspace.get("records") or []}

    records = []
    errors = []
    for record in site_data.get("records") or []:
        artifact_id = record.get("artifact_id")
        public_record = public_by_id.get(artifact_id)
        if not public_record:
            errors.append(f"{artifact_id}: missing public explorer record")
            continue
        trace = build_record(record, public_record, workspace_by_id.get(artifact_id))
        if trace["trace_issues"]:
            errors.append(f"{artifact_id}: " + ", ".join(trace["trace_issues"]))
        records.append(trace)

    trace_states = Counter(record.get("trace_state") for record in records)
    batches = Counter((record.get("curation") or {}).get("recommended_batch") or "none" for record in records)
    source_domains = Counter((record.get("public_visual") or {}).get("domain") or "none" for record in records)
    source_routes = Counter((record.get("source_route") or {}).get("route") or "none" for record in records)
    candidates_flagged = [
        record["artifact_id"]
        for record in records
        if (record.get("candidate_review") or {}).get("flags")
    ]
    payload = {
        "version": date.today().isoformat(),
        "generated_at": date.today().isoformat(),
        "policy": {
            "ledger_omits_candidate_direct_urls": True,
            "candidate_public_use": False,
            "public_render_source": "content/media/species-media-render-contract.yaml",
            "public_explorer_source": "content/media/species-media-public-explorer-manifest.yaml",
            "species_page_media_synced_by": "scripts/sync_species_page_media.py",
        },
        "summary": {
            "species_records": len(records),
            "trace_issue_count": len(errors),
            "trace_state_counts": dict(sorted(trace_states.items())),
            "curation_batch_counts": dict(sorted(batches.items())),
            "source_domain_counts": dict(sorted(source_domains.items())),
            "source_route_counts": dict(sorted(source_routes.items())),
            "candidate_records_with_flags": candidates_flagged,
            "public_visual_ready": sum(
                1 for record in records if (record.get("public_visual") or {}).get("public_use") is True
            ),
            "hero_image_ready": sum(
                1 for record in records if (record.get("public_visual") or {}).get("hero_image_allowed") is True
            ),
            "candidate_public_use_blocked": sum(
                1
                for record in records
                if (record.get("integrity_checks") or {}).get("candidate_public_use_blocked") is True
            ),
        },
        "records": records,
    }
    return payload, errors


def markdown(payload):
    summary = payload.get("summary") or {}
    lines = [
        "# Species Media Trace Ledger",
        "",
        f"Generated: {payload.get('generated_at')}",
        "",
        "## Summary",
        "",
        f"- Species records: {summary.get('species_records')}",
        f"- Public visuals ready: {summary.get('public_visual_ready')}",
        f"- Hero images ready: {summary.get('hero_image_ready')}",
        f"- Candidate public-use blocked: {summary.get('candidate_public_use_blocked')}",
        f"- Trace issues: {summary.get('trace_issue_count')}",
        "",
        "## Records",
        "",
        "| Species | Public visual | Candidate | Curation | Integrity |",
        "|---|---|---|---|---|",
    ]
    for record in payload.get("records") or []:
        public = record.get("public_visual") or {}
        candidate = record.get("candidate_review") or {}
        curation = record.get("curation") or {}
        integrity = "pass" if not record.get("trace_issues") else ", ".join(record.get("trace_issues"))
        public_cell = (
            f"`{public.get('render_strategy')}`<br>"
            f"[{public.get('domain')}]({public.get('source_url')})<br>"
            f"hero allowed: `{str(public.get('hero_image_allowed')).lower()}`"
        )
        candidate_cell = (
            f"`{candidate.get('asset_id')}`<br>"
            f"{candidate.get('rights_status')}<br>"
            f"direct URLs omitted: `{str(candidate.get('direct_urls_omitted')).lower()}`"
        )
        curation_cell = (
            f"{curation.get('checks_complete')}/{curation.get('checks_total')} checks<br>"
            f"`{curation.get('recommended_batch')}`<br>"
            f"promotion: `{str(curation.get('promotion_allowed_now')).lower()}`"
        )
        lines.append(
            "| "
            + " | ".join(
                [
                    f"{record.get('common_name')}<br>`{record.get('artifact_id')}`",
                    public_cell,
                    candidate_cell,
                    curation_cell,
                    integrity,
                ]
            )
            + " |"
        )
    lines.append("")
    return "\n".join(lines)


def main():
    payload, errors = build_ledger()
    TRACE_LEDGER_PATH.write_text(
        yaml.safe_dump(payload, sort_keys=False, allow_unicode=False),
        encoding="utf-8",
    )
    REVIEW_PACK_PATH.parent.mkdir(parents=True, exist_ok=True)
    REVIEW_PACK_PATH.write_text(markdown(payload), encoding="utf-8")
    print(f"Wrote {TRACE_LEDGER_PATH.relative_to(ROOT)}")
    print(f"Wrote {REVIEW_PACK_PATH.relative_to(ROOT)}")
    if errors:
        for error in errors:
            print(f"ERROR {error}", file=sys.stderr)
        return 1
    print(
        "Species media trace ledger: "
        f"{payload['summary']['species_records']} records, "
        f"{payload['summary']['trace_issue_count']} trace issues."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
