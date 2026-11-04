# Blue Life Commons: brand and Guardian direction

Status: **design proposal; not an approved identity, deployed service, or publication authority**  
Owner: Frank Riemer · Independent design, science, ethics, and engineering review: pending  
Figma: https://www.figma.com/design/z2ERBniGazSBzElmpIEtZ8  
Scope: build on DESIGN.md, TASTE.md, STYLE.md, ETHICS.md and the existing visual-system and media contracts.

## Brand idea

**Knowledge for a living ocean.** Blue Life Commons is a source-linked public field library and contribution commons for ocean life. The institution should feel curious, welcoming, exact, and patient. The Commons carries knowledge; the Ocean Intelligence System supplies tooling; Starlight sustains work through separately described services. This proposal does not establish legal ownership, trademark rights, or a new organization.

### Voice

- State the source, observation date, review state, and uncertainty when they matter.
- Speak to a person with a real task: explore a record, inspect a source, contribute evidence, review a change.
- Use “satellite heat-stress signal” when describing that source; only say “observed bleaching” when supported by an appropriate observation.
- Prefer “review-gated” to claiming every record is reviewed. Say “no recent data” rather than “nothing happened.”
- No guilt-led campaigns, invented animal intention, or claims of perfect coverage.

Example: “NOAA reports elevated heat stress in this region. This is a satellite-derived signal, not a confirmed observation of coral bleaching. Source date: [date]; last checked: [date]; review: pending.”

## Visual exploration

Figma contains three editable mark sketches: Shared Current (recommended), Horizon, and Living Trace. The Shared Current carries the existing commons-current concept into a reduced one-color symbol. It is a sketch and must be compared against existing marks in `assets/brand/`, relevant neighboring marks, and actual small-size usage before any replacement. The AI-generated art direction plate is concept imagery only; its maps, specimen details and graphics must never be represented as research evidence.

The proposal uses a quiet field-library vocabulary: editorial serif, clear sans, a restrained ocean-and-paper palette, sourced imagery, and visible attribution. Figma colors and fonts are exploratory and do not supersede existing canonical website tokens or licensed typography. Before release: reconcile with actual CSS; verify font license; test contrast; define light/dark, one-color, responsive, social, print and 16/32px versions; obtain originality and legal review; export optically refined editable SVG masters; and document decision, provenance, review and rollback. Generated pixels are not a logo master.

Media follows `docs/visual-system/species-media-pipeline.md` and the existing render contract. Do not use generated species images as identification evidence or present synthetic maps as observations.

## Interfaces and responsibilities

| Actor | Responsibility |
|---|---|
| Community member, educator, or researcher | Ask questions, supply sources and corrections, set local needs |
| ChatGPT, Claude, or other client | Provide a conversational interface; display attribution and status from the connected tools |
| Marine MCP | Search and return bounded, source-carrying responses; enforce existing review gating |
| Place-scoped Guardian | Poll selected sources; normalize, deduplicate and flag candidate changes |
| Reviewer | Decide source fitness, scientific interpretation, ethics, rights, correction and publication |
| Commons repository | Version artifacts, provenance and review state through pull requests |
| Starlight / operators | Maintain reliability, incident response, access controls and transparent operating costs |

Existing repositories already contain MCP and contributor skills; reuse their contracts. ChatGPT availability, remote transport, OAuth and connector distribution require separate compatibility and security verification. The local Claude Code setup in the existing README is not evidence of a hosted, publicly connectable ChatGPT integration.

## Proposed first pilot: one reef, one signal

Start with an interested regional partner and one predefined, non-sensitive area. Consume one NOAA Coral Reef Watch heat-stress product on its actual publication cadence. Validate source format, permitted use, license/attribution, freshness, geography and outages with the partner before scheduling it. The design can later support additional regions and feeds; no global coverage is implied.

Suggested record envelope: `source_id`, `source_url`, `source_product_version`, `observed_or_product_time`, `retrieved_at`, `region_id`, `spatial_resolution`, `value`, `units_or_level`, `license_attribution`, `content_hash`, `processing_version`, `freshness_state`, `review_state`, `limitations`, `supersedes`. A changed source produces a candidate event; an unchanged, stale, unavailable, malformed, corrected or retracted source produces an explicit state, never a silently reused “current” result.

Flow: scheduler → bounded source adapter → validation + deduplication → evidence snapshot and manifest → reviewer queue → optional draft PR → human science/ethics/editor review → public artifact. The operator can disable the feed, quarantine records, replay a version and correct or retract published material. A source alert is not an emergency service. Sensitive locations are generalized under the existing ethics contract. Test source outage, stale data, duplicate events, changed product version and correction paths before any pilot.

A low-cost starting architecture is a scheduled Worker and a small database; add Queues or Workflows only when workload, retries or long-running review actually justify them. Avoid an always-running browser. Existing credit terms, source quotas, storage and provider costs need verification before deployment. n8n or Composio can orchestrate optional integrations, but neither is the source of truth or bypasses review; adopt only where it removes demonstrated integration work.

## User-facing workflows to prototype

1. **Ask the ocean:** “What is known about this species near the Azores?” → reviewed records, source links, age and gaps.
2. **Watch a place:** “Show the latest source signals for this reef.” → dated observations, source and uncertainty; no implied live coverage.
3. **Contribute a correction:** source suggestion → schema validation → draft PR → human review.
4. **Build a briefing:** compare vetted sources → cite each claim → flag disagreements → reviewer approves.
5. **Reuse in education:** compile reviewed material → attribution and license retained → corrections link.

## References

- NOAA Coral Reef Watch product description: https://coralreefwatch.noaa.gov/product/5km/index_5km_baa.php
- NOAA heat-stress products and aggregation caveat: https://coralreefwatch.noaa.gov/product/5km/
- GBIF guidance on occurrence data and sampling: https://techdocs.gbif.org/en/data-publishing/data-quality-recommendations
- Cloudflare scheduled triggers: https://developers.cloudflare.com/workers/configuration/cron-triggers/
- Cloudflare queues and workflows: https://developers.cloudflare.com/workers/best-practices/workers-best-practices/

## Acceptance and outstanding decisions

- [ ] Compare concepts against existing identity; choose direction and assign independent reviewer.
- [ ] Verify rights, typography, marks, actual palette, accessible contrast, and small-size proofs.
- [ ] Select a partner, geographic scope, approved source and human reviewer.
- [ ] Audit existing runtime and Cloudflare resources before implementing or deploying.
- [ ] Test source adapters, failures, freshness, corrections, welfare and review gates.
- [ ] Verify ChatGPT/Claude client integration and publication policy separately.
