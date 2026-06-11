---
id: dataset-card-template
type: dataset-card
title: Dataset Card Template
audience:
  - researcher
  - developer
status: draft
sources:
  - url: "https://example.org/replace-with-real-source"
    title: "Replace with real dataset/provider URL"
    accessed: "2026-06-11"
review:
  science: required
  ethics: not-applicable
  editor: pending
outputs:
  website_path: /research/_templates/dataset-card-template
  github_path: content/research/_templates/dataset-card-template.md
  map_layer: false
impact:
  claim: "Template — replace with the dataset card's impact claim."
  eligible_for_hypercert: false
contributors:
  - github: frankxai
license: CC-BY-4.0
---

# Dataset Card Template

> Copy this file to `content/research/<dataset-slug>.md`, replace every section, and update the frontmatter. A dataset card documents a real data source so others can use it correctly and lawfully. Verify every field against the provider's live documentation; record the access date. If you cannot determine the license, say so — do not guess.

## What it is

One paragraph: what the dataset/service provides and who operates it.

## Access

| Field | Value |
|---|---|
| Provider | Organization name |
| Docs / API URL | Stable URL (verified) |
| Base URL | Verified API base URL, or "no public API" |
| Auth | none / API key / registration required / OAuth |
| Rate limits | Documented limits, or "unspecified — be conservative" |
| Formats | JSON / CSV / NetCDF / etc. |

## License and reuse

State the **data license** and what consumers may do (redistribute, attribution-required, query-only, prohibited). This is the most important section; an unclear license blocks downstream use.

## Fields

The key fields a consumer will use, and what each means. Note units and coordinate reference systems where relevant.

## Limitations and ethics

Coverage gaps, known biases, update cadence, and any sensitive-data handling (e.g., coarsening precise locations of vulnerable populations before reuse).

## How it's used in the commons

Which species pages, region briefings, or Ocean Intelligence connectors rely on this dataset. Link the matching connector if one exists.

## Sources

- The provider's documentation and license page, with access dates.
