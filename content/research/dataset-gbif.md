---
id: dataset-gbif
type: dataset-card
title: "Dataset Card: GBIF — Global Biodiversity Information Facility"
audience:
  - researcher
  - developer
status: draft
sources:
  - url: "https://techdocs.gbif.org/en/openapi/"
    title: "GBIF API Reference — Technical Documentation"
    accessed: "2026-06-11"
  - url: "https://www.gbif.org/terms"
    title: "GBIF — Terms of use"
    accessed: "2026-06-11"
  - url: "https://www.gbif.org/news/82812/licensing-milestone-for-data-access-in-gbiforg"
    title: "Licensing milestone for data access in GBIF.org"
    accessed: "2026-06-11"
review:
  science: required
  ethics: not-applicable
  editor: pending
outputs:
  website_path: /research/dataset-gbif
  github_path: content/research/dataset-gbif.md
  map_layer: false
impact:
  claim: "Documented the GBIF occurrence + taxonomy API as a reusable, license-aware data source for the commons."
  eligible_for_hypercert: true
contributors:
  - github: frankxai
license: CC-BY-4.0
---

# Dataset Card: GBIF — Global Biodiversity Information Facility

> Status: draft, awaiting maintainer review. Endpoint and license details checked against GBIF documentation on 2026-06-11. GBIF aggregates both marine and terrestrial records; filter to marine taxa for ocean use.

## What it is

GBIF is an international, government-funded open-data infrastructure providing access to hundreds of millions of biodiversity occurrence records plus a unified backbone taxonomy. For ocean work it complements OBIS: broader taxonomic scope, with marine records filterable by taxon.

## Access

| Field | Value |
|---|---|
| Provider | GBIF Secretariat |
| Docs | [GBIF API reference](https://techdocs.gbif.org/en/openapi/) |
| API base | `https://api.gbif.org/v1` |
| Example endpoints | `/occurrence/search`, `/species/match`, `/enumeration/basic/License` |
| Auth | **None for read/search.** A free registered GBIF account is required only for initiating downloads (asynchronous occurrence download API) and authenticated POST operations. |
| Formats | JSON (API); Darwin Core Archive for downloads |

## License and reuse

GBIF data is published under **CC0** or **CC-BY** (and some **CC-BY-NC**); more than 82% of records are CC0 or CC-BY, which require no more than appropriate attribution. Licenses are **per dataset** — carry each record's license and citation through to downstream use. See [GBIF terms of use](https://www.gbif.org/terms). When you use a GBIF download, cite the download DOI it issues.

## Fields

Records follow Darwin Core: accepted scientific name (matched to the GBIF backbone), decimal latitude/longitude, coordinate uncertainty, event date, dataset key, publishing organization, and license. The `/species/match` endpoint resolves names to the backbone taxonomy.

## Limitations and ethics

- Strong sampling bias by geography and taxon; presence-only (absence is not implied).
- GBIF flags some sensitive-species records with **obscured/generalized coordinates** — respect that generalization; never attempt to de-obscure.
- Coarsen sensitive marine-species coordinates to regional granularity before publishing (ETHICS.md).

## How it's used in the commons

This card records GBIF as a candidate source for occurrence and taxonomy work in the commons. Blue Life Commons does not currently publish a GBIF connector here. Treat an implementation as unavailable until its code, tests, provenance, license handling, and coordinate safeguards are publicly inspectable.

## Sources

- [GBIF API Reference — Technical Documentation](https://techdocs.gbif.org/en/openapi/) (accessed 2026-06-11)
- [GBIF — Terms of use](https://www.gbif.org/terms) (accessed 2026-06-11)
- [Licensing milestone for data access in GBIF.org](https://www.gbif.org/news/82812/licensing-milestone-for-data-access-in-gbiforg) (accessed 2026-06-11)
