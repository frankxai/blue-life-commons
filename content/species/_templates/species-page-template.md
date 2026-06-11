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
impact:
  claim: "Template — replace with the species page's impact claim."
  eligible_for_hypercert: false
contributors:
  - github: frankxai
license: CC-BY-4.0
---

# Species Page Template

> Copy this file to `content/species/<guild>/<species-slug>.md`, replace every section, and update the frontmatter. Conservation status **must** cite a recognized authority (IUCN Red List or equivalent). Science-sensitive content requires expert review (`review.science: required`); any observation guidance requires ethics review.

## At a glance

Common name (*Scientific name*) — one or two sentences a beginner understands. State the species guild and where in the world it lives, at regional granularity.

| Field | Value | Source |
|---|---|---|
| Scientific name | *Genus species* | WoRMS / authority |
| Guild | cetacean / pinniped / turtle / shark-ray / reef | — |
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
