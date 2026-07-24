---
id: dataset-inaturalist
type: dataset-card
title: "Dataset Card: iNaturalist — Citizen-Science Observations API"
audience:
  - researcher
  - developer
  - citizen-scientist
status: draft
sources:
  - url: "https://www.inaturalist.org/pages/api+reference"
    title: "iNaturalist — API Reference"
    accessed: "2026-06-11"
  - url: "https://www.inaturalist.org/pages/api+recommended+practices"
    title: "iNaturalist — API Recommended Practices"
    accessed: "2026-06-11"
review:
  science: required
  ethics: required
  editor: pending
outputs:
  website_path: /research/dataset-inaturalist
  github_path: content/research/dataset-inaturalist.md
  map_layer: false
impact:
  claim: "Documented the iNaturalist observations API with its rate limits and obscured-coordinate handling for ethical commons use."
  eligible_for_hypercert: true
contributors:
  - github: frankxai
license: CC-BY-4.0
---

# Dataset Card: iNaturalist — Citizen-Science Observations API

> Status: draft, awaiting maintainer review. Endpoint, rate-limit, and coordinate-handling details checked against iNaturalist documentation on 2026-06-11. This source carries elevated ethics requirements because of sensitive-taxa coordinate handling.

## What it is

iNaturalist is a global citizen-science platform where people record species observations with photos and community identifications. It is a rich source of recent, geographically broad occurrence data — and a place the public can be invited to contribute, making it the natural companion to field missions and observation guides.

## Access

| Field | Value |
|---|---|
| Provider | iNaturalist (a joint initiative; observations contributed by the public) |
| Docs | [API reference](https://www.inaturalist.org/pages/api+reference), [recommended practices](https://www.inaturalist.org/pages/api+recommended+practices) |
| API base | `https://api.inaturalist.org/v1` (the faster v1 API with consistent response formats) |
| Auth | None for public reads. OAuth required for writes and to access one's own private/obscured coordinates. |
| Rate limits | Aim for ~1 request/second and **≤60 requests/minute** (hard cap ~100/min), and **≤10,000 requests/day**. Excess returns HTTP 429. Cache aggressively. |
| Formats | JSON |

## License and reuse

Licensing is **per observation** — each observer chooses (e.g. CC0, CC-BY, CC-BY-NC) or no license (all rights reserved). **Filter by license** and honor it per record; never assume a blanket license. Many records are CC-BY-NC, which restricts commercial reuse.

## Fields

Observation id, taxon (with community ID), observed-on date, geoprivacy/coordinate fields, place, quality grade (use `research`-grade for data work), photos, and license.

## Limitations and ethics

- **Obscured coordinates are load-bearing.** iNaturalist automatically obscures locations for taxa flagged sensitive (e.g. many threatened species). The public API returns generalized coordinates for these; precise coordinates require the observer's own authenticated access. **Never attempt to de-obscure, infer, or republish precise locations of obscured taxa.** This is both an iNaturalist rule and a Blue Life Commons ETHICS.md rule.
- Identification quality varies; prefer `research`-grade and treat IDs as community consensus, not authority.
- Effort bias toward populated, accessible, photogenic places.

## How it's used in the commons

This card records iNaturalist as a candidate source for future occurrence work and carefully reviewed citizen-science guidance. Blue Life Commons does not currently publish an iNaturalist connector here. Treat an implementation as unavailable until its code, tests, provenance, license handling, and sensitivity safeguards are publicly inspectable.

## Sources

- [iNaturalist — API Reference](https://www.inaturalist.org/pages/api+reference) (accessed 2026-06-11)
- [iNaturalist — API Recommended Practices](https://www.inaturalist.org/pages/api+recommended+practices) (accessed 2026-06-11)
