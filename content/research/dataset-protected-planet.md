---
id: dataset-protected-planet
type: dataset-card
title: "Dataset Card: Protected Planet — World Database on Protected Areas (WDPA)"
audience:
  - researcher
  - developer
status: draft
sources:
  - url: "https://api.protectedplanet.net/documentation/v3"
    title: "Protected Planet API v3 documentation"
    accessed: "2026-06-11"
  - url: "https://www.protectedplanet.net/en/legal"
    title: "Protected Planet — Terms and Conditions"
    accessed: "2026-06-11"
review:
  science: required
  ethics: not-applicable
  editor: pending
outputs:
  website_path: /research/dataset-protected-planet
  github_path: content/research/dataset-protected-planet.md
  map_layer: false
impact:
  claim: "Documented the Protected Planet (WDPA) API and its query-only terms for the commons."
  eligible_for_hypercert: true
contributors:
  - github: frankxai
license: CC-BY-4.0
---

# Dataset Card: Protected Planet — World Database on Protected Areas (WDPA)

> Status: draft, awaiting maintainer review. Base URL, token auth, and WDPA terms confirmed against Protected Planet documentation on 2026-06-11. The license is restrictive — read the "License and reuse" section carefully.

## What it is

Protected Planet is the public interface to the World Database on Protected Areas (WDPA), maintained by UNEP-WCMC with IUCN. It is the authoritative global dataset of marine and terrestrial protected areas — boundaries, designations, IUCN management categories, and governance — used to answer "what protection applies here?"

## Access

| Field | Value |
|---|---|
| Provider | UNEP-WCMC & IUCN |
| Docs | [API v3 documentation](https://api.protectedplanet.net/documentation/v3) |
| API base | `https://api.protectedplanet.net/v3` |
| Key endpoint | `/protected_areas` (search; also by WDPA id) |
| Auth | **Free API token required** (request form at api.protectedplanet.net/request), passed as the `token` query param |
| Formats | JSON (and GeoJSON geometry) |

## License and reuse

This is the most important section. WDPA terms are **restrictive**:

- **Query-only.** Do **not** redistribute the raw WDPA database.
- A **specific citation is mandatory** on any publication or analysis: *UNEP-WCMC and IUCN (year) Protected Planet: The World Database on Protected Areas (WDPA)*.
- Commercial use and redistribution have additional conditions — read [the terms](https://www.protectedplanet.net/en/legal) before any reuse.

Treat WDPA as reference-for-analysis with attribution, not as open data to mirror.

## Fields

`wdpa_id` (stable id), `name`, `designation`, `iucn_category`, `marine` flag, and `countries`. Geometry is available as GeoJSON; the commons does not republish boundaries beyond what the terms allow.

## Limitations and ethics

- Coverage and currency vary by country; "as of" the access date.
- Protected-area boundaries are published by design, so no wildlife-location coarsening applies — but the redistribution terms above do.

## How it's used in the commons

This card records Protected Planet as a candidate source for protected-area context in region briefings and future guardian work. Blue Life Commons does not currently publish a Protected Planet connector here. Treat an implementation as unavailable until its code, tests, provenance, license handling, and redistribution controls are publicly inspectable.

## Sources

- [Protected Planet API v3 documentation](https://api.protectedplanet.net/documentation/v3) (accessed 2026-06-11)
- [Protected Planet — Terms and Conditions](https://www.protectedplanet.net/en/legal) (accessed 2026-06-11)
