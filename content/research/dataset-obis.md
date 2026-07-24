---
id: dataset-obis
type: dataset-card
title: "Dataset Card: OBIS — Ocean Biodiversity Information System"
audience:
  - researcher
  - developer
status: draft
sources:
  - url: "https://obis.org/data/access/"
    title: "OBIS — Data access"
    accessed: "2026-06-11"
  - url: "https://manual.obis.org/access.html"
    title: "The OBIS manual — Data access"
    accessed: "2026-06-11"
  - url: "https://registry.opendata.aws/obis/"
    title: "OBIS species occurrence data — Registry of Open Data on AWS"
    accessed: "2026-06-11"
  - url: "https://www.ioc.unesco.org/en/obis"
    title: "OBIS — Intergovernmental Oceanographic Commission (IOC-UNESCO)"
    accessed: "2026-06-11"
review:
  science: required
  ethics: not-applicable
  editor: pending
outputs:
  website_path: /research/dataset-obis
  github_path: content/research/dataset-obis.md
  map_layer: false
impact:
  claim: "Documented the OBIS occurrence API as a reusable, license-aware data source for the commons."
  eligible_for_hypercert: true
contributors:
  - github: frankxai
license: CC-BY-4.0
---

# Dataset Card: OBIS — Ocean Biodiversity Information System

> Status: draft, awaiting maintainer review. Endpoint and license details below were checked against OBIS documentation on 2026-06-11. Confirm the current API base path and per-dataset licenses before relying on them in production.

## What it is

OBIS (the Ocean Biodiversity Information System) is a global, open-access platform run under IOC-UNESCO that integrates, quality-controls, and serves marine species occurrence records — over 100 million records of roughly 160,000 marine species, contributed by thousands of datasets worldwide. Taxonomy is reconciled against the World Register of Marine Species (WoRMS).

## Access

| Field | Value |
|---|---|
| Provider | OBIS / IOC-UNESCO |
| Docs | [OBIS data access](https://obis.org/data/access/), [OBIS manual](https://manual.obis.org/access.html) |
| API base | `https://api.obis.org` (the Mapper and the R package are built on this API; the `occurrence` endpoint is the primary entry) |
| Auth | None documented for read access |
| Formats | JSON (API); full exports via the OBIS export tooling and the AWS Open Data mirror |
| Bulk mirror | OBIS occurrence data is also on the [AWS Registry of Open Data](https://registry.opendata.aws/obis/) |

## License and reuse

OBIS aggregates datasets under **mixed licenses** — individual datasets may be **CC0, CC-BY, or CC-BY-NC**. Each OBIS export includes a list of the licenses of the underlying datasets, and **users must cite and comply with each dataset's license**. Do not assume a single license for OBIS as a whole; carry per-dataset license through to any downstream use.

## Fields

OBIS records follow the Darwin Core standard and add 68 fields from the OBIS QC pipeline, including WoRMS-reconciled taxonomy. Core fields a consumer will use: accepted scientific name, decimal latitude/longitude, event date, dataset id, and the dataset's license.

## Limitations and ethics

- Occurrence data has spatial and taxonomic sampling bias (effort is uneven across regions and taxa).
- Coordinates can be precise. **Coarsen occurrence coordinates of sensitive or exploited species to regional granularity before publishing** (Blue Life Commons ETHICS.md); do not surface exact aggregation or nesting locations.
- Records reflect what has been reported, not true absence.

## How it's used in the commons

This card records OBIS as a candidate occurrence source for species pages, region briefings, and future guardian work. Blue Life Commons does not currently publish an OBIS connector here. Treat an implementation as unavailable until its code, tests, provenance, license handling, and coordinate safeguards are publicly inspectable.

## Sources

- [OBIS — Data access](https://obis.org/data/access/) (accessed 2026-06-11)
- [The OBIS manual — Data access](https://manual.obis.org/access.html) (accessed 2026-06-11)
- [OBIS on the AWS Registry of Open Data](https://registry.opendata.aws/obis/) (accessed 2026-06-11)
- [OBIS — IOC-UNESCO](https://www.ioc.unesco.org/en/obis) (accessed 2026-06-11)
