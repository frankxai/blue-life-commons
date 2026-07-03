#!/usr/bin/env python3
"""Build a public-safe species visual explorer prototype.

This surface is intentionally different from the review board. It does not
emit candidate image URLs, Commons file pages, candidate titles, or thumbnails.
Public cards render only the current render contract: approved image, verified
source-card fallback, source-card recheck placeholder, or blocked placeholder.

Usage:
  python scripts/build_species_media_public_explorer.py
"""
from __future__ import annotations

import argparse
from collections import Counter
from datetime import date
import html
import json
from pathlib import Path
import re
from urllib.parse import urlparse

import yaml

ROOT = Path(__file__).resolve().parent.parent
SITE_DATA_PATH = ROOT / "content" / "media" / "species-media-site-data.json"
CURATION_WORKSPACE_PATH = ROOT / "content" / "media" / "species-media-curation-workspace.yaml"
ACQUISITION_PLAN_PATH = ROOT / "content" / "media" / "species-media-acquisition-plan.yaml"
OUT_DIR = ROOT / "content" / "media" / "public"
MANIFEST_PATH = ROOT / "content" / "media" / "species-media-public-explorer-manifest.yaml"


def esc(value):
    if value is None:
        return ""
    return html.escape(str(value), quote=True)


def slug(value):
    value = (value or "none").lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-") or "none"


def load_workspace():
    if not CURATION_WORKSPACE_PATH.exists():
        return {}
    payload = yaml.safe_load(CURATION_WORKSPACE_PATH.read_text(encoding="utf-8")) or {}
    return {record.get("artifact_id"): record for record in payload.get("records") or []}


def load_acquisition_plan():
    if not ACQUISITION_PLAN_PATH.exists():
        return {}
    payload = yaml.safe_load(ACQUISITION_PLAN_PATH.read_text(encoding="utf-8")) or {}
    return {record.get("artifact_id"): record for record in payload.get("records") or []}


def source_host(source_url):
    if not source_url:
        return None
    return urlparse(source_url).netloc.lower()


def public_acquisition(acquisition_record=None):
    acquisition_record = acquisition_record or {}
    source_strategy = acquisition_record.get("source_strategy") or {}
    current_visual = acquisition_record.get("current_visual") or {}
    approval_gap = acquisition_record.get("approval_gap") or {}
    next_actions = acquisition_record.get("next_actions") or []
    next_action = next_actions[1] if len(next_actions) > 1 else (next_actions[0] if next_actions else None)
    lane = acquisition_record.get("acquisition_lane")
    target_family = source_strategy.get("target_source_family")
    return {
        "lane": lane,
        "label": acquisition_record.get("acquisition_label") or lane,
        "priority": acquisition_record.get("priority"),
        "target_source_family": target_family,
        "target_source_family_label": source_strategy.get("target_source_family_label") or target_family,
        "google_images_role": source_strategy.get("google_images_role"),
        "partner_media_grant_needed": source_strategy.get("partner_media_grant_needed") is True,
        "outreach_targets": source_strategy.get("outreach_targets") or [],
        "approved_primary_needed": current_visual.get("hero_image_ready") is not True,
        "promotion_allowed_now": approval_gap.get("promotion_allowed_now") is True,
        "checks_complete": approval_gap.get("checks_complete") or 0,
        "checks_total": approval_gap.get("checks_total") or 0,
        "next_action": next_action,
    }


def public_record(record, workspace_record=None, acquisition_record=None):
    render_contract = record.get("render_contract") or {}
    public_visual = render_contract.get("public_visual") or {}
    source_card = ((record.get("public_fallback") or {}).get("source_card") or {})
    surface_rules = render_contract.get("surface_rules") or {}
    source_url = public_visual.get("source_url") if public_visual.get("public_use") is True else None
    source_domain = public_visual.get("domain") or source_card.get("domain") or source_host(source_url)
    source_type = public_visual.get("source_type") or source_card.get("source_type")
    curation = record.get("curation") or {}
    source_route = record.get("source_route") or {}
    workspace_record = workspace_record or {}
    approval_state = workspace_record.get("approval_state") or {}
    blockers = workspace_record.get("blockers") or []
    public_use = public_visual.get("public_use") is True
    hero_allowed = surface_rules.get("species_page_hero_image_allowed") is True
    kind = public_visual.get("kind") or "placeholder"

    if kind == "source_card" and public_use:
        surface_note = "Verified source card fallback ready"
    elif kind == "source_card_placeholder":
        surface_note = "Source card recheck required"
    elif kind == "image" and public_use and hero_allowed:
        surface_note = "Approved primary image ready"
    else:
        surface_note = "Public visual pending"

    return {
        "artifact_id": record.get("artifact_id"),
        "species_page": record.get("species_page"),
        "website_path": record.get("website_path"),
        "taxon_group": record.get("taxon_group"),
        "common_name": record.get("common_name"),
        "scientific_name": record.get("scientific_name"),
        "media_status": record.get("media_status"),
        "primary_status": record.get("primary_status"),
        "public_visual": {
            "kind": kind,
            "public_use": public_use,
            "render_strategy": render_contract.get("render_strategy"),
            "source_url": source_url,
            "public_media_url": public_visual.get("public_media_url") if public_use and kind == "image" else None,
            "domain": source_domain,
            "source_type": source_type,
            "display_title": public_visual.get("display_title") or source_card.get("display_title"),
            "creator": public_visual.get("creator"),
            "credit": public_visual.get("credit"),
            "license": public_visual.get("license"),
            "license_url": public_visual.get("license_url"),
            "alt_text": public_visual.get("alt_text"),
            "copies_external_media": public_visual.get("copies_external_media") is True,
            "surface_note": surface_note,
        },
        "surface_rules": {
            "species_page_visual_slot": surface_rules.get("species_page_visual_slot") is True,
            "visual_explorer_card_slot": surface_rules.get("visual_explorer_card_slot") is True,
            "species_page_hero_image_allowed": hero_allowed,
            "candidate_thumbnail_allowed": surface_rules.get("candidate_thumbnail_allowed") is True,
        },
        "candidate_review": {
            "candidate_public_use": False,
            "candidate_hidden_from_public_manifest": True,
            "candidate_review_state": "review_only_until_curator_approval",
        },
        "source_card": {
            "status": source_card.get("status"),
            "public_use": source_card.get("public_use") is True,
            "domain": source_card.get("domain"),
            "source_type": source_card.get("source_type"),
        },
        "source_route": {
            "route": source_route.get("route"),
            "priority": source_route.get("priority"),
        },
        "curation": {
            "decision": curation.get("decision"),
            "checks_complete": curation.get("checks_complete") or 0,
            "checks_total": curation.get("checks_total") or 0,
            "recommended_batch": workspace_record.get("recommended_batch"),
            "batch_label": workspace_record.get("batch_label"),
            "workstream": workspace_record.get("workstream"),
            "promotion_allowed_now": approval_state.get("promotion_allowed_now") is True,
            "blocker_count": len(blockers),
        },
        "acquisition": public_acquisition(acquisition_record),
        "supporting_assets_count": len(record.get("supporting_assets") or []),
    }


def manifest(payload):
    workspace_by_id = load_workspace()
    acquisition_by_id = load_acquisition_plan()
    records = [
        public_record(
            record,
            workspace_by_id.get(record.get("artifact_id")),
            acquisition_by_id.get(record.get("artifact_id")),
        )
        for record in payload.get("records") or []
    ]
    visual_kinds = Counter((record["public_visual"] or {}).get("kind") or "placeholder" for record in records)
    render_strategies = Counter(
        (record["public_visual"] or {}).get("render_strategy") or "none" for record in records
    )
    groups = Counter(record.get("taxon_group") or "ungrouped" for record in records)
    source_statuses = Counter((record.get("source_card") or {}).get("status") or "none" for record in records)
    curation_batches = Counter((record.get("curation") or {}).get("recommended_batch") or "none" for record in records)
    acquisition_lanes = Counter((record.get("acquisition") or {}).get("lane") or "none" for record in records)
    target_families = Counter(
        (record.get("acquisition") or {}).get("target_source_family") or "none" for record in records
    )
    priorities = Counter((record.get("acquisition") or {}).get("priority") or "none" for record in records)
    source_domains = Counter((record["public_visual"] or {}).get("domain") or "none" for record in records)
    source_types = Counter((record["public_visual"] or {}).get("source_type") or "none" for record in records)
    hero_ready = sum(
        1 for record in records if (record.get("surface_rules") or {}).get("species_page_hero_image_allowed") is True
    )
    public_ready = sum(
        1 for record in records if (record.get("public_visual") or {}).get("public_use") is True
    )
    candidates_blocked = sum(
        1
        for record in records
        if (record.get("candidate_review") or {}).get("candidate_public_use") is False
    )
    approved_primary_needed = sum(
        1 for record in records if (record.get("acquisition") or {}).get("approved_primary_needed") is True
    )
    return {
        "version": date.today().isoformat(),
        "generated_at": date.today().isoformat(),
        "source_data": SITE_DATA_PATH.relative_to(ROOT).as_posix(),
        "acquisition_plan": ACQUISITION_PLAN_PATH.relative_to(ROOT).as_posix(),
        "policy": {
            "public_manifest_omits_candidate_urls": True,
            "public_manifest_omits_candidate_file_pages": True,
            "candidate_public_use": False,
            "approved_primary_required_for_hero_image": True,
            "source_card_does_not_authorize_image_copy": True,
            "google_images_discovery_only": True,
            "partner_grants_require_written_permission": True,
        },
        "summary": {
            "species_records": len(records),
            "public_visual_ready": public_ready,
            "hero_image_ready": hero_ready,
            "approved_primary_needed": approved_primary_needed,
            "candidate_public_use_blocked": candidates_blocked,
            "visual_kind_counts": dict(sorted(visual_kinds.items())),
            "render_strategy_counts": dict(sorted(render_strategies.items())),
            "taxon_group_counts": dict(sorted(groups.items())),
            "source_card_status_counts": dict(sorted(source_statuses.items())),
            "curation_batch_counts": dict(sorted(curation_batches.items())),
            "acquisition_lane_counts": dict(sorted(acquisition_lanes.items())),
            "target_source_family_counts": dict(sorted(target_families.items())),
            "priority_counts": dict(sorted(priorities.items())),
            "source_domain_counts": dict(sorted(source_domains.items())),
            "source_type_counts": dict(sorted(source_types.items())),
        },
        "records": records,
    }


def pill(text, variant="neutral"):
    return f'<span class="pill pill-{esc(variant)}">{esc(text or "none")}</span>'


def source_link(record):
    public_visual = record.get("public_visual") or {}
    source_url = public_visual.get("source_url")
    if not source_url:
        return ""
    return (
        f'<a class="source-link" href="{esc(source_url)}" target="_blank" '
        f'rel="noreferrer">Open source</a>'
    )


def source_plate(record):
    public_visual = record.get("public_visual") or {}
    kind = public_visual.get("kind")
    ready = public_visual.get("public_use") is True
    media_url = public_visual.get("public_media_url")
    domain = public_visual.get("domain") or "source pending"
    source_type = public_visual.get("source_type") or "unverified"
    note = public_visual.get("surface_note") or "Public visual pending"
    state = "ready" if ready else "pending"
    visual_label = "Source card" if kind == "source_card" else "Placeholder"
    if kind == "image":
        visual_label = "Approved image"
    if kind == "image" and ready and media_url:
        attribution = " / ".join(
            part
            for part in [
                public_visual.get("creator"),
                public_visual.get("license"),
            ]
            if part
        )
        return f"""
      <figure class="image-plate image-plate-{esc(state)}">
        <img src="{esc(media_url)}" alt="{esc(public_visual.get("alt_text") or record.get("common_name"))}" loading="lazy">
        <figcaption>
          <span>{esc(visual_label)}</span>
          <strong>{esc(domain)}</strong>
          <small>{esc(attribution or source_type.replace("_", " "))}</small>
        </figcaption>
      </figure>
    """
    return f"""
      <div class="source-plate source-plate-{esc(state)}">
        <div class="source-mark" aria-hidden="true">{esc((record.get("common_name") or "?")[:1])}</div>
        <div class="source-copy">
          <p class="source-kicker">{esc(visual_label)}</p>
          <p class="source-domain">{esc(domain)}</p>
          <p class="source-type">{esc(source_type.replace("_", " "))}</p>
        </div>
        <p class="source-note">{esc(note)}</p>
      </div>
    """


def card(record):
    public_visual = record.get("public_visual") or {}
    source_card = record.get("source_card") or {}
    route = record.get("source_route") or {}
    curation = record.get("curation") or {}
    acquisition = record.get("acquisition") or {}
    surface_rules = record.get("surface_rules") or {}
    group = record.get("taxon_group") or "ungrouped"
    visual_kind = public_visual.get("kind") or "placeholder"
    render_strategy = public_visual.get("render_strategy") or "none"
    source_status = source_card.get("status") or "none"
    curation_batch = curation.get("recommended_batch") or "none"
    acquisition_lane = acquisition.get("lane") or "none"
    acquisition_label = acquisition.get("label") or acquisition_lane
    target_family = acquisition.get("target_source_family") or "none"
    target_family_label = acquisition.get("target_source_family_label") or target_family
    next_action = acquisition.get("next_action") or "Keep source card visible while primary media is reviewed."
    outreach_targets = ", ".join(acquisition.get("outreach_targets") or []) or "source publisher"
    source_type = public_visual.get("source_type") or "none"
    source_domain = public_visual.get("domain") or "none"
    public_ready = public_visual.get("public_use") is True
    hero_allowed = surface_rules.get("species_page_hero_image_allowed") is True
    curation_label = (
        "Primary approved; maintain attribution"
        if hero_allowed
        else (curation.get("batch_label") or curation_batch).replace("_", " ")
    )
    search_blob = " ".join(
        str(value or "")
        for value in [
            record.get("artifact_id"),
            record.get("common_name"),
            record.get("scientific_name"),
            record.get("species_page"),
            record.get("website_path"),
            group,
            visual_kind,
            render_strategy,
            source_status,
            source_type,
            source_domain,
            route.get("route"),
            route.get("priority"),
            curation_batch,
            curation.get("batch_label"),
            curation.get("workstream"),
            acquisition_lane,
            acquisition_label,
            acquisition.get("priority"),
            target_family,
            target_family_label,
            next_action,
            outreach_targets,
            public_visual.get("surface_note"),
        ]
    ).lower()
    return f"""
    <article class="species-card group-{esc(slug(group))}" data-search="{esc(search_blob)}" data-group="{esc(group)}" data-kind="{esc(visual_kind)}" data-render="{esc(render_strategy)}" data-source-status="{esc(source_status)}" data-source-type="{esc(source_type)}" data-domain="{esc(source_domain)}" data-batch="{esc(curation_batch)}" data-acquisition="{esc(acquisition_lane)}" data-family="{esc(target_family)}" data-ready="{str(public_ready).lower()}">
      {source_plate(record)}
      <div class="card-body">
        <div class="pill-row">
          {pill(group)}
          {pill("public ready" if public_ready else "recheck", "ready" if public_ready else "pending")}
          {pill(visual_kind.replace("_", " "), "kind")}
          {pill(render_strategy.replace("_", " "), "render")}
          {pill((acquisition.get("priority") or "priority pending"), "priority")}
        </div>
        <h2>{esc(record.get("common_name"))}</h2>
        <p class="scientific">{esc(record.get("scientific_name"))}</p>
        <dl class="meta-grid">
          <div><dt>Source</dt><dd>{esc(source_domain)}</dd></div>
          <div><dt>Source type</dt><dd>{esc(source_type.replace("_", " "))}</dd></div>
          <div><dt>Source card</dt><dd>{esc(source_status.replace("_", " "))}</dd></div>
          <div><dt>Primary image</dt><dd>{esc("approved" if hero_allowed else "pending approval")}</dd></div>
          <div><dt>Curation lane</dt><dd>{esc(curation_label)}</dd></div>
          <div><dt>Approval checks</dt><dd>{esc(curation.get("checks_complete", 0))}/{esc(curation.get("checks_total", 0))}</dd></div>
          <div><dt>Route</dt><dd>{esc((route.get("route") or "none").replace("_", " "))}</dd></div>
          <div><dt>Species path</dt><dd>{esc(record.get("website_path") or record.get("species_page"))}</dd></div>
          <div><dt>Acquisition</dt><dd>{esc(acquisition_label.replace("_", " "))}</dd></div>
          <div><dt>Target</dt><dd>{esc(target_family_label.replace("_", " "))}</dd></div>
          <div><dt>Outreach</dt><dd>{esc(outreach_targets)}</dd></div>
          <div><dt>Next action</dt><dd>{esc(next_action)}</dd></div>
        </dl>
        <div class="surface-row">
          {pill("candidate hidden", "blocked")}
          {pill("no copy/crop rights from source card", "blocked")}
          {pill("hero locked" if not hero_allowed else "hero ready", "pending" if not hero_allowed else "ready")}
          {pill("partner grant needed" if acquisition.get("partner_media_grant_needed") else "image-level review", "acquisition")}
        </div>
        <div class="links">{source_link(record)}</div>
      </div>
    </article>
    """


def option(value, label):
    return f'<option value="{esc(value)}">{esc(label)}</option>'


def html_page(payload):
    records = payload.get("records") or []
    summary = payload.get("summary") or {}
    groups = Counter(record.get("taxon_group") or "ungrouped" for record in records)
    kinds = Counter((record.get("public_visual") or {}).get("kind") or "placeholder" for record in records)
    renders = Counter((record.get("public_visual") or {}).get("render_strategy") or "none" for record in records)
    statuses = Counter((record.get("source_card") or {}).get("status") or "none" for record in records)
    source_types = Counter((record.get("public_visual") or {}).get("source_type") or "none" for record in records)
    domains = Counter((record.get("public_visual") or {}).get("domain") or "none" for record in records)
    batches = Counter((record.get("curation") or {}).get("recommended_batch") or "none" for record in records)
    acquisitions = Counter((record.get("acquisition") or {}).get("lane") or "none" for record in records)
    families = Counter((record.get("acquisition") or {}).get("target_source_family") or "none" for record in records)
    group_options = "".join(option(value, f"{value} ({count})") for value, count in sorted(groups.items()))
    kind_options = "".join(option(value, f"{value.replace('_', ' ')} ({count})") for value, count in sorted(kinds.items()))
    render_options = "".join(option(value, f"{value.replace('_', ' ')} ({count})") for value, count in sorted(renders.items()))
    status_options = "".join(option(value, f"{value.replace('_', ' ')} ({count})") for value, count in sorted(statuses.items()))
    type_options = "".join(option(value, f"{value.replace('_', ' ')} ({count})") for value, count in sorted(source_types.items()))
    domain_options = "".join(option(value, f"{value} ({count})") for value, count in sorted(domains.items()))
    batch_options = "".join(option(value, f"{value.replace('_', ' ')} ({count})") for value, count in sorted(batches.items()))
    acquisition_options = "".join(
        option(value, f"{value.replace('_', ' ')} ({count})") for value, count in sorted(acquisitions.items())
    )
    family_options = "".join(
        option(value, f"{value.replace('_', ' ')} ({count})") for value, count in sorted(families.items())
    )
    cards = "\n".join(card(record) for record in records)
    generated_at = payload.get("generated_at") or date.today().isoformat()
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Blue Life Commons Public Species Visual Explorer</title>
  <style>
    :root {{
      color-scheme: light;
      --ink: #102126;
      --muted: #5c6d70;
      --paper: #f7f7f1;
      --panel: #ffffff;
      --line: #d6ddd9;
      --line-strong: #9fb3ae;
      --sea: #0e6f70;
      --kelp: #466f33;
      --clay: #a6533d;
      --sun: #b07a16;
      --deep: #18445a;
      --violet: #65507c;
      --shadow: 0 16px 44px rgba(16, 33, 38, 0.11);
    }}
    * {{ box-sizing: border-box; }}
    html {{ scroll-behavior: smooth; }}
    body {{
      margin: 0;
      background:
        linear-gradient(180deg, rgba(255,255,255,0.72), rgba(247,247,241,0.92)),
        repeating-linear-gradient(90deg, rgba(16,33,38,0.035) 0 1px, transparent 1px 96px);
      color: var(--ink);
      font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      line-height: 1.5;
    }}
    main {{
      width: min(1480px, calc(100% - 48px));
      margin: 0 auto;
      padding: 28px 0 40px;
    }}
    header {{
      display: grid;
      grid-template-columns: minmax(0, 1fr) minmax(280px, 420px);
      gap: 28px;
      align-items: end;
      min-height: 232px;
      border-bottom: 1px solid var(--line);
    }}
    .eyebrow {{
      margin: 0 0 10px;
      color: var(--sea);
      font-weight: 800;
      font-size: 0.78rem;
      letter-spacing: 0;
      text-transform: uppercase;
    }}
    h1 {{
      margin: 0;
      max-width: 850px;
      font-size: 3.1rem;
      line-height: 1.02;
      letter-spacing: 0;
    }}
    .subtitle {{
      max-width: 820px;
      margin: 14px 0 0;
      color: var(--muted);
      font-size: 1.04rem;
    }}
    .contract-panel {{
      border: 1px solid var(--line);
      border-radius: 8px;
      background: rgba(255,255,255,0.84);
      padding: 16px;
      box-shadow: 0 10px 28px rgba(16,33,38,0.07);
    }}
    .contract-panel h2 {{
      margin: 0 0 10px;
      font-size: 1rem;
      letter-spacing: 0;
    }}
    .contract-list {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 8px;
      margin: 0;
    }}
    .contract-list div {{
      border-top: 1px solid var(--line);
      padding-top: 8px;
      min-width: 0;
    }}
    .contract-list dt {{
      color: var(--muted);
      font-size: 0.75rem;
      text-transform: uppercase;
      letter-spacing: 0;
    }}
    .contract-list dd {{
      margin: 3px 0 0;
      font-size: 1.16rem;
      font-weight: 780;
    }}
    .summary-grid {{
      display: grid;
      grid-template-columns: repeat(6, minmax(0, 1fr));
      gap: 12px;
      margin: 20px 0;
    }}
    .summary-item {{
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 13px 15px;
      min-width: 0;
      box-shadow: 0 8px 24px rgba(16,33,38,0.06);
    }}
    .summary-item span {{
      display: block;
      color: var(--muted);
      font-size: 0.76rem;
      font-weight: 760;
      text-transform: uppercase;
      letter-spacing: 0;
    }}
    .summary-item strong {{
      display: block;
      margin-top: 4px;
      font-size: 1.85rem;
      line-height: 1.08;
    }}
    .toolbar {{
      position: sticky;
      top: 0;
      z-index: 5;
      display: grid;
      grid-template-columns: minmax(200px, 1.25fr) repeat(9, minmax(104px, 0.65fr)) minmax(88px, auto);
      gap: 9px;
      align-items: center;
      padding: 13px 0;
      background: rgba(247,247,241,0.91);
      backdrop-filter: blur(12px);
    }}
    input, select {{
      width: 100%;
      min-height: 42px;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: var(--panel);
      color: var(--ink);
      padding: 0 11px;
      font: inherit;
    }}
    label.checkbox {{
      display: inline-flex;
      min-height: 42px;
      align-items: center;
      gap: 7px;
      color: var(--muted);
      white-space: nowrap;
      font-weight: 680;
    }}
    .count {{
      margin: 0 0 14px;
      color: var(--muted);
      font-size: 0.94rem;
    }}
    .board {{
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 16px;
    }}
    .species-card {{
      overflow: hidden;
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 8px;
      box-shadow: var(--shadow);
      min-width: 0;
    }}
    .species-card::before {{
      content: "";
      display: block;
      height: 5px;
      background: var(--sea);
    }}
    .group-pinnipeds::before {{ background: var(--clay); }}
    .group-turtles::before {{ background: var(--kelp); }}
    .group-sharks-rays::before {{ background: var(--deep); }}
    .group-reefs::before {{ background: var(--sun); }}
    .group-sirenians::before {{ background: var(--violet); }}
    .source-plate {{
      min-height: 170px;
      display: grid;
      grid-template-columns: 72px minmax(0, 1fr);
      grid-template-rows: 1fr auto;
      gap: 14px;
      padding: 18px;
      background:
        linear-gradient(135deg, rgba(14,111,112,0.12), rgba(255,255,255,0.88) 44%, rgba(176,122,22,0.12)),
        var(--panel);
      border-bottom: 1px solid var(--line);
    }}
    .source-plate-pending {{
      background:
        linear-gradient(135deg, rgba(166,83,61,0.13), rgba(255,255,255,0.9) 46%, rgba(92,109,112,0.11)),
        var(--panel);
    }}
    .image-plate {{
      position: relative;
      min-height: 230px;
      margin: 0;
      overflow: hidden;
      background: #e7eee9;
      border-bottom: 1px solid var(--line);
    }}
    .image-plate img {{
      display: block;
      width: 100%;
      height: 260px;
      object-fit: contain;
      object-position: center;
      background: #dfe8e4;
    }}
    .image-plate figcaption {{
      position: absolute;
      left: 12px;
      right: 12px;
      bottom: 12px;
      display: grid;
      gap: 2px;
      max-width: calc(100% - 24px);
      padding: 9px 10px;
      border: 1px solid rgba(255,255,255,0.35);
      border-radius: 8px;
      background: rgba(16, 33, 38, 0.72);
      color: #fff;
      backdrop-filter: blur(8px);
    }}
    .image-plate figcaption span {{
      font-size: 0.7rem;
      font-weight: 820;
      text-transform: uppercase;
      letter-spacing: 0;
      color: rgba(255,255,255,0.78);
    }}
    .image-plate figcaption strong,
    .image-plate figcaption small {{
      overflow-wrap: anywhere;
    }}
    .image-plate figcaption strong {{
      font-size: 0.92rem;
      line-height: 1.12;
    }}
    .image-plate figcaption small {{
      color: rgba(255,255,255,0.76);
      font-size: 0.72rem;
      line-height: 1.15;
    }}
    .source-mark {{
      width: 72px;
      height: 72px;
      display: grid;
      place-items: center;
      border: 1px solid var(--line-strong);
      border-radius: 8px;
      color: var(--deep);
      background: rgba(255,255,255,0.76);
      font-size: 2rem;
      font-weight: 820;
    }}
    .source-copy {{ min-width: 0; }}
    .source-kicker {{
      margin: 2px 0 5px;
      color: var(--sea);
      font-size: 0.78rem;
      font-weight: 820;
      text-transform: uppercase;
      letter-spacing: 0;
    }}
    .source-domain {{
      margin: 0;
      font-size: 1.23rem;
      line-height: 1.15;
      font-weight: 820;
      overflow-wrap: anywhere;
    }}
    .source-type {{
      margin: 6px 0 0;
      color: var(--muted);
      font-size: 0.92rem;
      overflow-wrap: anywhere;
    }}
    .source-note {{
      grid-column: 1 / -1;
      margin: 0;
      color: var(--muted);
      font-size: 0.94rem;
    }}
    .card-body {{ padding: 16px; }}
    .pill-row, .surface-row, .links {{
      display: flex;
      flex-wrap: wrap;
      gap: 7px;
      align-items: center;
    }}
    .pill {{
      display: inline-flex;
      align-items: center;
      min-height: 24px;
      max-width: 100%;
      padding: 3px 8px;
      border: 1px solid var(--line);
      border-radius: 999px;
      background: #f3f6f3;
      color: var(--muted);
      font-size: 0.72rem;
      font-weight: 740;
      text-transform: uppercase;
      letter-spacing: 0;
      overflow-wrap: anywhere;
    }}
    .pill-ready {{ border-color: #a7c9bd; color: var(--sea); background: #eef8f3; }}
    .pill-pending {{ border-color: #e2c1b6; color: var(--clay); background: #fff1ec; }}
    .pill-kind {{ border-color: #c7d5da; color: var(--deep); background: #eef6f8; }}
    .pill-render {{ border-color: #d9c69d; color: #76520d; background: #fff8e8; }}
    .pill-blocked {{ border-color: #d8d4c9; color: #59666a; background: #f7f4ee; }}
    .pill-priority {{ border-color: #beb4d2; color: var(--violet); background: #f4f0fa; }}
    .pill-acquisition {{ border-color: #b9cda9; color: var(--kelp); background: #f1f8ee; }}
    h2 {{
      margin: 13px 0 0;
      font-size: 1.22rem;
      line-height: 1.16;
      letter-spacing: 0;
    }}
    .scientific {{
      margin: 3px 0 14px;
      color: var(--muted);
      font-style: italic;
    }}
    .meta-grid {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 10px 12px;
      margin: 0;
    }}
    dt {{
      color: var(--muted);
      font-size: 0.72rem;
      font-weight: 760;
      text-transform: uppercase;
      letter-spacing: 0;
    }}
    dd {{
      margin: 2px 0 0;
      overflow-wrap: anywhere;
      font-size: 0.91rem;
    }}
    .surface-row {{ margin-top: 14px; }}
    .links {{ margin-top: 14px; min-height: 36px; }}
    .source-link {{
      display: inline-flex;
      align-items: center;
      min-height: 36px;
      padding: 0 12px;
      border: 1px solid var(--line);
      border-radius: 8px;
      color: var(--ink);
      background: #fbfcfa;
      text-decoration: none;
      font-weight: 760;
      font-size: 0.9rem;
    }}
    .source-link:hover, .source-link:focus {{
      border-color: var(--sea);
      color: var(--sea);
      outline: none;
    }}
    .hidden {{ display: none; }}
    @media (prefers-reduced-motion: reduce) {{
      html {{ scroll-behavior: auto; }}
    }}
    @media (max-width: 1240px) {{
      .toolbar {{ grid-template-columns: minmax(220px, 1fr) minmax(150px, 0.6fr) minmax(150px, 0.6fr); }}
      .summary-grid {{ grid-template-columns: repeat(3, minmax(0, 1fr)); }}
      .board {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }}
    }}
    @media (max-width: 760px) {{
      main {{ width: min(100% - 32px, 640px); padding-top: 18px; }}
      header, .board, .meta-grid {{ grid-template-columns: 1fr; }}
      header {{ min-height: auto; padding-bottom: 16px; gap: 18px; }}
      h1 {{ font-size: 2rem; }}
      .subtitle {{ font-size: 0.98rem; }}
      .summary-grid {{ grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 8px; }}
      .summary-item {{ padding: 10px; }}
      .summary-item span {{ font-size: 0.68rem; }}
      .summary-item strong {{ font-size: 1.45rem; }}
      .toolbar {{ position: static; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 8px; }}
      .toolbar input {{ grid-column: 1 / -1; }}
      .contract-list {{ grid-template-columns: 1fr 1fr; }}
      .source-plate {{ grid-template-columns: 58px minmax(0, 1fr); min-height: 154px; padding: 15px; }}
      .source-mark {{ width: 58px; height: 58px; font-size: 1.55rem; }}
    }}
    @media (max-width: 430px) {{
      main {{ width: min(100% - 24px, 390px); }}
      h1 {{ font-size: 1.88rem; }}
      .summary-grid {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }}
    }}
  </style>
</head>
<body>
  <main data-public-explorer="true">
    <header>
      <div>
        <p class="eyebrow">Blue Life Commons media contract</p>
        <h1>Public Species Visual Explorer</h1>
      <p class="subtitle">Every species now has an approved primary image with source, credit, license, alt text, and blocked-surface rules. Candidate evidence stays hidden from public routes.</p>
      </div>
      <section class="contract-panel" aria-label="Publication contract">
        <h2>Render Boundary</h2>
        <dl class="contract-list">
          <div><dt>Generated</dt><dd>{esc(generated_at)}</dd></div>
          <div><dt>Candidate URLs</dt><dd>omitted</dd></div>
          <div><dt>Approved Images</dt><dd>{esc(summary.get("hero_image_ready", 0))}</dd></div>
          <div><dt>Primary needed</dt><dd>{esc(summary.get("approved_primary_needed", 0))}</dd></div>
        </dl>
      </section>
    </header>
    <section class="summary-grid" aria-label="Summary">
      <div class="summary-item"><span>Species</span><strong>{esc(summary.get("species_records", len(records)))}</strong></div>
      <div class="summary-item"><span>Public Visuals</span><strong>{esc(summary.get("public_visual_ready", 0))}</strong></div>
      <div class="summary-item"><span>Hero Ready</span><strong>{esc(summary.get("hero_image_ready", 0))}</strong></div>
      <div class="summary-item"><span>Primary Needed</span><strong>{esc(summary.get("approved_primary_needed", 0))}</strong></div>
      <div class="summary-item"><span>Candidate Blocked</span><strong>{esc(summary.get("candidate_public_use_blocked", 0))}</strong></div>
      <div class="summary-item"><span>Acquisition Lanes</span><strong>{esc(len(summary.get("acquisition_lane_counts") or {}))}</strong></div>
    </section>
    <section class="toolbar" aria-label="Filters">
      <input id="search" type="search" placeholder="Search species/lane">
      <select id="group"><option value="">All groups</option>{group_options}</select>
      <select id="kind"><option value="">All visuals</option>{kind_options}</select>
      <select id="render"><option value="">All render</option>{render_options}</select>
      <select id="sourceStatus"><option value="">All cards</option>{status_options}</select>
      <select id="sourceType"><option value="">All types</option>{type_options}</select>
      <select id="domain"><option value="">All domains</option>{domain_options}</select>
      <select id="batch"><option value="">Curation</option>{batch_options}</select>
      <select id="acquisition"><option value="">Acquisition</option>{acquisition_options}</select>
      <select id="family"><option value="">Targets</option>{family_options}</select>
      <label class="checkbox"><input id="readyOnly" type="checkbox"> Ready only</label>
    </section>
    <p class="count"><span id="visible-count">{esc(len(records))}</span> shown</p>
    <section class="board" id="board">
      {cards}
    </section>
  </main>
  <script>
    const cards = Array.from(document.querySelectorAll(".species-card"));
    const search = document.getElementById("search");
    const group = document.getElementById("group");
    const kind = document.getElementById("kind");
    const render = document.getElementById("render");
    const sourceStatus = document.getElementById("sourceStatus");
    const sourceType = document.getElementById("sourceType");
    const domain = document.getElementById("domain");
    const batch = document.getElementById("batch");
    const acquisition = document.getElementById("acquisition");
    const family = document.getElementById("family");
    const readyOnly = document.getElementById("readyOnly");
    const count = document.getElementById("visible-count");

    function applyFilters() {{
      const query = search.value.trim().toLowerCase();
      let visible = 0;
      for (const card of cards) {{
        const show =
          (!query || card.dataset.search.includes(query)) &&
          (!group.value || card.dataset.group === group.value) &&
          (!kind.value || card.dataset.kind === kind.value) &&
          (!render.value || card.dataset.render === render.value) &&
          (!sourceStatus.value || card.dataset.sourceStatus === sourceStatus.value) &&
          (!sourceType.value || card.dataset.sourceType === sourceType.value) &&
          (!domain.value || card.dataset.domain === domain.value) &&
          (!batch.value || card.dataset.batch === batch.value) &&
          (!acquisition.value || card.dataset.acquisition === acquisition.value) &&
          (!family.value || card.dataset.family === family.value) &&
          (!readyOnly.checked || card.dataset.ready === "true");
        card.classList.toggle("hidden", !show);
        if (show) visible += 1;
      }}
      count.textContent = visible.toString();
    }}

    for (const control of [search, group, kind, render, sourceStatus, sourceType, domain, batch, acquisition, family, readyOnly]) {{
      control.addEventListener("input", applyFilters);
      control.addEventListener("change", applyFilters);
    }}
  </script>
</body>
</html>
"""


def write_outputs(manifest_payload, html_path):
    MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    MANIFEST_PATH.write_text(
        yaml.safe_dump(manifest_payload, sort_keys=False, allow_unicode=False),
        encoding="utf-8",
    )
    html_path.write_text(html_page(manifest_payload), encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--out",
        type=Path,
        default=OUT_DIR / f"species-visual-explorer-{date.today().isoformat()}.html",
        help="Output HTML path.",
    )
    args = parser.parse_args()
    payload = json.loads(SITE_DATA_PATH.read_text(encoding="utf-8"))
    html_path = args.out if args.out.is_absolute() else ROOT / args.out
    manifest_payload = manifest(payload)
    write_outputs(manifest_payload, html_path)
    print(f"Wrote {MANIFEST_PATH.relative_to(ROOT)}")
    print(f"Wrote {html_path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
