#!/usr/bin/env python3
"""Build a local visual board for staged species media candidates.

The board is a reviewer aid, not a publication surface. It embeds candidate
thumbnails from their source URLs and keeps every candidate marked review-only.

Usage:
  python scripts/build_species_media_visual_board.py
"""
from __future__ import annotations

import argparse
from collections import Counter
from datetime import date
import html
import json
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent.parent
SITE_DATA_PATH = ROOT / "content" / "media" / "species-media-site-data.json"
OUT_DIR = ROOT / "content" / "media" / "review-packs"


def esc(value):
    if value is None:
        return ""
    return html.escape(str(value), quote=True)


def thumbnail_url(candidate):
    title = candidate.get("title") or ""
    if title.lower().startswith("file:"):
        return f"https://commons.wikimedia.org/wiki/Special:Redirect/file/{quote(title[5:])}?width=760"
    return candidate.get("image_url") or ""


def pill(text, variant="neutral"):
    return f'<span class="pill pill-{esc(variant)}">{esc(text)}</span>'


def link_button(label, href):
    if not href:
        return ""
    return f'<a class="button-link" href="{esc(href)}" target="_blank" rel="noreferrer">{esc(label)}</a>'


def card(record):
    candidate = record.get("candidate") or {}
    rich_embed = record.get("rich_embed") or {}
    source_card = ((record.get("public_fallback") or {}).get("source_card") or {})
    curation = record.get("curation") or {}
    source_route = record.get("source_route") or {}
    render_contract = record.get("render_contract") or {}
    flags = candidate.get("flags") or []
    rights_status = candidate.get("rights_status") or "none"
    group = record.get("taxon_group") or "ungrouped"
    status = record.get("primary_status") or "unknown"
    route = source_route.get("route") or "none"
    priority = source_route.get("priority") or "none"
    fallback_status = source_card.get("status") or "none"
    curation_decision = curation.get("decision") or "none"
    render_strategy = render_contract.get("render_strategy") or "none"
    public_visual = render_contract.get("public_visual") or {}
    hero_allowed = ((render_contract.get("surface_rules") or {}).get("species_page_hero_image_allowed")) is True
    image_src = thumbnail_url(candidate)
    image_alt = f"Candidate media for {record.get('common_name') or record.get('artifact_id')}"
    search_blob = " ".join(
        str(value or "")
        for value in [
            record.get("artifact_id"),
            record.get("common_name"),
            record.get("scientific_name"),
            record.get("species_page"),
            candidate.get("title"),
            candidate.get("creator"),
            candidate.get("credit"),
            rights_status,
            route,
            priority,
            fallback_status,
            curation_decision,
            render_strategy,
            public_visual.get("kind"),
            source_card.get("domain"),
            source_card.get("source_type"),
            source_route.get("rationale"),
            " ".join(source_route.get("partner_refs") or []),
            " ".join(flags),
        ]
    ).lower()
    flag_html = "".join(pill(flag.replace("_", " "), "flag") for flag in flags) or pill("no automated flags", "ok")
    image_html = (
        f'<img src="{esc(image_src)}" alt="{esc(image_alt)}" loading="lazy" decoding="async">'
        if image_src
        else '<div class="empty-image">No image candidate</div>'
    )
    return f"""
    <article class="species-card" data-search="{esc(search_blob)}" data-group="{esc(group)}" data-status="{esc(status)}" data-rights="{esc(rights_status)}" data-route="{esc(route)}" data-fallback="{esc(fallback_status)}" data-curation="{esc(curation_decision)}" data-render="{esc(render_strategy)}" data-flagged="{str(bool(flags)).lower()}">
      <figure class="media-frame">
        {image_html}
      </figure>
      <div class="card-body">
        <div class="pill-row">
          {pill(group)}
          {pill(status, "status")}
          {pill(rights_status, "rights")}
          {pill(priority, "priority")}
          {pill(fallback_status.replace("_", " "), "fallback")}
          {pill(curation_decision.replace("_", " "), "curation")}
          {pill(render_strategy.replace("_", " "), "render")}
        </div>
        <h2>{esc(record.get("common_name"))}</h2>
        <p class="scientific">{esc(record.get("scientific_name"))}</p>
        <dl class="meta-grid">
          <div><dt>Candidate</dt><dd>{esc(candidate.get("title"))}</dd></div>
          <div><dt>Creator</dt><dd>{esc(candidate.get("creator"))}</dd></div>
          <div><dt>License</dt><dd>{esc(candidate.get("license"))}</dd></div>
          <div><dt>Route</dt><dd>{esc(route.replace("_", " "))}</dd></div>
          <div><dt>Public fallback</dt><dd>{esc(fallback_status.replace("_", " "))}</dd></div>
          <div><dt>Source card</dt><dd>{esc(source_card.get("domain"))}</dd></div>
          <div><dt>Curation</dt><dd>{esc(curation_decision)} ({esc(curation.get("checks_complete", 0))}/{esc(curation.get("checks_total", 0))})</dd></div>
          <div><dt>Render</dt><dd>{esc(render_strategy.replace("_", " "))}</dd></div>
          <div><dt>Hero allowed</dt><dd>{esc("yes" if hero_allowed else "no")}</dd></div>
          <div><dt>Review</dt><dd>{esc(candidate.get("review_status"))}</dd></div>
        </dl>
        <div class="flag-row">{flag_html}</div>
        <p class="next-action">{esc(record.get("next_action"))}</p>
        <div class="links">
          {link_button("Commons", candidate.get("commons_file_page"))}
          {link_button("Image", candidate.get("image_url"))}
          {link_button("Official", rich_embed.get("preferred_source_url"))}
        </div>
      </div>
    </article>
    """


def option(value, label):
    return f'<option value="{esc(value)}">{esc(label)}</option>'


def render(payload):
    records = payload.get("records") or []
    summary = payload.get("summary") or {}
    group_counts = Counter(record.get("taxon_group") or "ungrouped" for record in records)
    rights_counts = Counter((record.get("candidate") or {}).get("rights_status") or "none" for record in records)
    status_counts = Counter(record.get("primary_status") or "unknown" for record in records)
    route_counts = Counter((record.get("source_route") or {}).get("route") or "none" for record in records)
    fallback_counts = Counter(
        ((record.get("public_fallback") or {}).get("source_card") or {}).get("status") or "none"
        for record in records
    )
    curation_counts = Counter((record.get("curation") or {}).get("decision") or "none" for record in records)
    render_counts = Counter((record.get("render_contract") or {}).get("render_strategy") or "none" for record in records)
    public_visual_ready = sum(
        1
        for record in records
        if (((record.get("render_contract") or {}).get("public_visual") or {}).get("public_use") is True)
    )
    flagged_count = sum(1 for record in records if (record.get("candidate") or {}).get("flags"))
    groups = "".join(option(group, f"{group} ({count})") for group, count in sorted(group_counts.items()))
    rights = "".join(option(right, f"{right} ({count})") for right, count in sorted(rights_counts.items()))
    statuses = "".join(option(status, f"{status} ({count})") for status, count in sorted(status_counts.items()))
    routes = "".join(option(route, f"{route.replace('_', ' ')} ({count})") for route, count in sorted(route_counts.items()))
    fallbacks = "".join(
        option(status, f"{status.replace('_', ' ')} ({count})") for status, count in sorted(fallback_counts.items())
    )
    curations = "".join(
        option(decision, f"{decision.replace('_', ' ')} ({count})") for decision, count in sorted(curation_counts.items())
    )
    renders = "".join(
        option(strategy, f"{strategy.replace('_', ' ')} ({count})") for strategy, count in sorted(render_counts.items())
    )
    cards = "\n".join(card(record) for record in records)
    generated_at = payload.get("generated_at") or date.today().isoformat()
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Blue Life Commons Species Media Board</title>
  <style>
    :root {{
      color-scheme: light;
      --ink: #132126;
      --muted: #5a6970;
      --paper: #f7f8f5;
      --panel: #ffffff;
      --line: #d8ded9;
      --teal: #0f766e;
      --coral: #b4533f;
      --amber: #9a6700;
      --sky: #1d5f8f;
      --shadow: 0 16px 48px rgba(19, 33, 38, 0.12);
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      background: var(--paper);
      color: var(--ink);
      font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      line-height: 1.5;
    }}
    main {{ max-width: 1480px; margin: 0 auto; padding: 28px; }}
    header {{
      display: grid;
      grid-template-columns: minmax(0, 1fr) auto;
      gap: 24px;
      align-items: end;
      padding: 18px 0 24px;
      border-bottom: 1px solid var(--line);
    }}
    h1 {{ margin: 0; font-size: clamp(1.8rem, 3vw, 3.2rem); line-height: 1.02; letter-spacing: 0; }}
    .subtitle {{ max-width: 820px; margin: 12px 0 0; color: var(--muted); font-size: 1rem; }}
    .generated {{ color: var(--muted); font-size: 0.9rem; text-align: right; }}
    .summary-grid {{
      display: grid;
      grid-template-columns: repeat(6, minmax(0, 1fr));
      gap: 12px;
      margin: 22px 0;
    }}
    .summary-item {{
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 14px 16px;
      box-shadow: 0 8px 28px rgba(19, 33, 38, 0.06);
    }}
    .summary-item span {{ color: var(--muted); display: block; font-size: 0.78rem; text-transform: uppercase; letter-spacing: 0.08em; }}
    .summary-item strong {{ display: block; font-size: 1.8rem; line-height: 1.1; margin-top: 5px; }}
    .toolbar {{
      position: sticky;
      top: 0;
      z-index: 5;
      display: grid;
      grid-template-columns: minmax(220px, 1.6fr) repeat(7, minmax(140px, 0.7fr)) auto;
      gap: 10px;
      align-items: center;
      padding: 14px 0;
      background: color-mix(in srgb, var(--paper) 92%, transparent);
      backdrop-filter: blur(12px);
    }}
    input, select {{
      width: 100%;
      min-height: 42px;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: var(--panel);
      color: var(--ink);
      padding: 0 12px;
      font: inherit;
    }}
    label.checkbox {{
      min-height: 42px;
      display: inline-flex;
      align-items: center;
      gap: 8px;
      white-space: nowrap;
      color: var(--muted);
    }}
    .count {{ color: var(--muted); font-size: 0.9rem; margin: 0 0 14px; }}
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
    .media-frame {{
      margin: 0;
      aspect-ratio: 16 / 10;
      background: #dde7e6;
      border-bottom: 1px solid var(--line);
    }}
    .media-frame img {{
      width: 100%;
      height: 100%;
      display: block;
      object-fit: cover;
    }}
    .empty-image {{
      height: 100%;
      display: grid;
      place-items: center;
      color: var(--muted);
      font-weight: 650;
    }}
    .card-body {{ padding: 16px; }}
    .pill-row, .flag-row, .links {{ display: flex; flex-wrap: wrap; gap: 7px; align-items: center; }}
    .pill {{
      display: inline-flex;
      align-items: center;
      min-height: 24px;
      padding: 3px 8px;
      border: 1px solid var(--line);
      border-radius: 999px;
      background: #f2f5f2;
      color: var(--muted);
      font-size: 0.73rem;
      font-weight: 680;
      text-transform: uppercase;
      letter-spacing: 0.06em;
      max-width: 100%;
    }}
    .pill-status {{ border-color: #b8c8cd; color: var(--sky); background: #eef5f8; }}
    .pill-rights {{ border-color: #bfd9cf; color: var(--teal); background: #eef8f4; }}
    .pill-priority {{ border-color: #e2cfa0; color: #7a4f00; background: #fff9ea; }}
    .pill-fallback {{ border-color: #bad0de; color: #155a74; background: #edf7fb; }}
    .pill-curation {{ border-color: #dac3e8; color: #68418a; background: #f7effb; }}
    .pill-render {{ border-color: #c5c6aa; color: #56601d; background: #fafbe9; }}
    .pill-ok {{ border-color: #b9d6c5; color: var(--teal); background: #eff8f1; }}
    .pill-flag {{ border-color: #efd39b; color: var(--amber); background: #fff7e3; }}
    h2 {{ margin: 12px 0 0; font-size: 1.16rem; line-height: 1.18; letter-spacing: 0; }}
    .scientific {{ margin: 2px 0 14px; color: var(--muted); font-style: italic; }}
    .meta-grid {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 10px 12px;
      margin: 0;
    }}
    dt {{ color: var(--muted); font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.08em; }}
    dd {{ margin: 2px 0 0; overflow-wrap: anywhere; font-size: 0.9rem; }}
    .flag-row {{ margin-top: 14px; }}
    .next-action {{ min-height: 4.5em; margin: 14px 0; color: var(--muted); font-size: 0.92rem; }}
    .button-link {{
      display: inline-flex;
      align-items: center;
      min-height: 34px;
      padding: 0 11px;
      border: 1px solid var(--line);
      border-radius: 8px;
      color: var(--ink);
      background: #fbfcfa;
      text-decoration: none;
      font-weight: 700;
      font-size: 0.88rem;
    }}
    .button-link:hover {{ border-color: var(--teal); color: var(--teal); }}
    .hidden {{ display: none; }}
    @media (max-width: 1180px) {{
      .board {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }}
      .toolbar {{ grid-template-columns: minmax(220px, 1fr) minmax(150px, 0.6fr) minmax(150px, 0.6fr); }}
    }}
    @media (max-width: 740px) {{
      main {{ padding: 18px; }}
      header {{ grid-template-columns: 1fr; }}
      .generated {{ text-align: left; }}
      .summary-grid, .board, .toolbar, .meta-grid {{ grid-template-columns: 1fr; }}
      .toolbar {{ position: static; }}
      .next-action {{ min-height: auto; }}
    }}
  </style>
</head>
<body>
  <main>
    <header>
      <div>
        <h1>Species Media Board</h1>
        <p class="subtitle">Review-only candidate imagery and official-source links for Blue Life Commons species records. Candidate media is not approved for public hero use.</p>
      </div>
      <p class="generated">Generated {esc(generated_at)}</p>
    </header>
    <section class="summary-grid" aria-label="Summary">
      <div class="summary-item"><span>Species</span><strong>{esc(summary.get("species_records", len(records)))}</strong></div>
      <div class="summary-item"><span>Candidate Primary</span><strong>{esc(status_counts.get("candidate", 0))}</strong></div>
      <div class="summary-item"><span>Approved Primary</span><strong>{esc(status_counts.get("approved", 0))}</strong></div>
      <div class="summary-item"><span>Source Cards Ready</span><strong>{esc(fallback_counts.get("verified_source_card", 0))}</strong></div>
      <div class="summary-item"><span>Public Visuals</span><strong>{esc(public_visual_ready)}</strong></div>
      <div class="summary-item"><span>Flagged</span><strong>{esc(flagged_count)}</strong></div>
    </section>
    <section class="toolbar" aria-label="Filters">
      <input id="search" type="search" placeholder="Search species, source, rights, creator">
      <select id="group"><option value="">All groups</option>{groups}</select>
      <select id="status"><option value="">All statuses</option>{statuses}</select>
      <select id="rights"><option value="">All rights</option>{rights}</select>
      <select id="route"><option value="">All routes</option>{routes}</select>
      <select id="fallback"><option value="">All source cards</option>{fallbacks}</select>
      <select id="curation"><option value="">All curation</option>{curations}</select>
      <select id="render"><option value="">All render strategies</option>{renders}</select>
      <label class="checkbox"><input id="flagged" type="checkbox"> Flagged only</label>
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
    const status = document.getElementById("status");
    const rights = document.getElementById("rights");
    const route = document.getElementById("route");
    const fallback = document.getElementById("fallback");
    const curation = document.getElementById("curation");
    const render = document.getElementById("render");
    const flagged = document.getElementById("flagged");
    const count = document.getElementById("visible-count");

    function applyFilters() {{
      const query = search.value.trim().toLowerCase();
      let visible = 0;
      for (const card of cards) {{
        const matchesText = !query || card.dataset.search.includes(query);
        const matchesGroup = !group.value || card.dataset.group === group.value;
        const matchesStatus = !status.value || card.dataset.status === status.value;
        const matchesRights = !rights.value || card.dataset.rights === rights.value;
        const matchesRoute = !route.value || card.dataset.route === route.value;
        const matchesFallback = !fallback.value || card.dataset.fallback === fallback.value;
        const matchesCuration = !curation.value || card.dataset.curation === curation.value;
        const matchesRender = !render.value || card.dataset.render === render.value;
        const matchesFlag = !flagged.checked || card.dataset.flagged === "true";
        const show = matchesText && matchesGroup && matchesStatus && matchesRights && matchesRoute && matchesFallback && matchesCuration && matchesRender && matchesFlag;
        card.classList.toggle("hidden", !show);
        if (show) visible += 1;
      }}
      count.textContent = visible.toString();
    }}

    for (const control of [search, group, status, rights, route, fallback, curation, render, flagged]) {{
      control.addEventListener("input", applyFilters);
      control.addEventListener("change", applyFilters);
    }}
  </script>
</body>
</html>
"""


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--out",
        type=Path,
        default=OUT_DIR / f"species-media-visual-board-{date.today().isoformat()}.html",
        help="Output HTML path.",
    )
    args = parser.parse_args()
    payload = json.loads(SITE_DATA_PATH.read_text(encoding="utf-8"))
    output = args.out if args.out.is_absolute() else ROOT / args.out
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render(payload), encoding="utf-8")
    print(f"Wrote {output.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
