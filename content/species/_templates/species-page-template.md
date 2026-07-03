---
id: species-page-template
type: species-page
title: Species Page Template
species_group: []
species: []
difficulty: beginner
audience:
  - traveler
  - student
  - citizen-scientist
  - researcher
status: draft
sources:
  - url: "https://example.org/replace-with-real-source"
    title: "Replace with real source"
    accessed: "2026-06-11"
review:
  science: required
  ethics: required
  editor: pending
outputs:
  website_path: /species/_templates/species-page-template
  github_path: content/species/_templates/species-page-template.md
  map_layer: false
media:
  registry_record: content/media/species-media-registry.yaml#replace-with-artifact-id
  render_contract: content/media/species-media-render-contract.yaml#replace-with-artifact-id
  public_explorer_record: content/media/species-media-public-explorer-manifest.yaml#replace-with-artifact-id
  primary:
    asset_id:
    path:
    source_url:
    creator:
    credit:
    license:
    rights_status: needs-review
    alt_text:
    qa_status: candidate
  embeds:
    - provider: source_card
      url: https://example.org/replace-with-official-or-partner-source
      rights_status: link-backed-source-card
      notes: Public fallback only; does not authorize image download, crop, social reuse, or hero-image reuse.
      domain: example.org
      source_type: source_to_classify
  render:
    strategy: verified_source_card_fallback
    public_visual_kind: source_card
    public_visual_public_use: true
    species_page_visual_slot: true
    species_page_hero_image_allowed: false
    candidate_thumbnail_allowed: false
    candidate_public_use: false
  review:
    primary_status: candidate
    curation_decision: pending
    checks_complete: 0
    checks_total: 9
    promotion_allowed_now: false
  supporting_assets: []
impact:
  claim: "Template — replace with the species page's impact claim."
  eligible_for_hypercert: false
contributors:
  - github: frankxai
license: CC-BY-4.0
---

# Species Page Template

> Copy this file to `content/species/<guild>/<species-slug>.md`, replace every section, and update the frontmatter. Conservation status **must** cite a recognized authority (IUCN Red List or equivalent). Science-sensitive content requires expert review (`review.science: required`); any observation guidance requires ethics review.

> Media note: add or update a matching record in `content/media/species-media-registry.yaml`, then run `python scripts/sync_species_page_media.py --write`. Public pages follow `content/media/species-media-render-contract.yaml` or `content/media/species-media-public-explorer-manifest.yaml`, so candidate image URLs stay review-only until approval. Generated art can be supporting context, but the primary species image must have image-level rights, creator credit, alt text, species-match basis, and ethics QA before approval.

## At a glance

Common name (*Scientific name*) — one or two sentences a beginner understands. State the species guild and where in the world it lives, at regional granularity.

| Field | Value | Source |
|---|---|---|
| Scientific name | *Genus species* | WoRMS / authority |
| Guild | cetaceans / pinnipeds / turtles / sharks-rays / reefs | — |
| IUCN status | e.g. Least Concern / Vulnerable / Endangered | IUCN Red List (cite) |
| Range | Regional description | cite |

## Identification

What it looks like; how to tell it apart from similar species. Plain language; define any jargon on first use.

## Ecology and behavior

Diet, habitat, life history — every factual claim cited to Tier 1–2 sources. Behavioral interpretation is cited to published research; no anthropomorphic claims as fact.

## Conservation status and threats

State IUCN status and main threats **with citations**. Do not invent population numbers or trends. If a figure cannot be sourced, mark the artifact `status: needs-sources` and remove the claim.

## How to observe responsibly

Link the reviewed observation guide or field mission for this species. Do **not** generate approach/interaction guidance here; reference the reviewed artifact. Never publish precise locations of sensitive aggregations.

## How you can help

Citizen-science platforms where sightings can be logged; reviewed missions; relevant partner organizations.

## Sources

- Replace with the full source list backing every factual claim above. Use stable URLs / DOIs and record access dates.
