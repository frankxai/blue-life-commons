---
id: dataset-worms
type: dataset-card
title: "Dataset Card: WoRMS — World Register of Marine Species"
audience:
  - researcher
  - developer
status: draft
sources:
  - url: "https://www.marinespecies.org/rest/"
    title: "WoRMS REST API documentation"
    accessed: "2026-06-11"
  - url: "https://www.marinespecies.org/aphia.php?p=webservice"
    title: "WoRMS web services overview"
    accessed: "2026-06-11"
review:
  science: required
  ethics: not-applicable
  editor: pending
outputs:
  website_path: /research/dataset-worms
  github_path: content/research/dataset-worms.md
  map_layer: false
impact:
  claim: "Documented the WoRMS taxonomy REST API as the commons' accepted-name authority."
  eligible_for_hypercert: true
contributors:
  - github: frankxai
license: CC-BY-4.0
---

# Dataset Card: WoRMS — World Register of Marine Species

> Status: draft, awaiting maintainer review. REST docs and no-auth read confirmed against WoRMS documentation on 2026-06-11; confirm the precise license/citation terms before relying on them.

## What it is

WoRMS is the authoritative register of marine species names, maintained by a global community of taxonomic editors. It is the backbone that OBIS reconciles its taxonomy against, so a name resolved in WoRMS is the name that aligns occurrence data across sources. The underlying database is Aphia.

## Access

| Field | Value |
|---|---|
| Provider | World Register of Marine Species (WoRMS) |
| Docs | [REST API](https://www.marinespecies.org/rest/), [web services overview](https://www.marinespecies.org/aphia.php?p=webservice) |
| API base | `https://www.marinespecies.org/rest` |
| Key endpoints | `AphiaRecordsByName/{name}`, `AphiaIDByName/{name}`, `AphiaClassificationByAphiaID/{id}` |
| Auth | None documented for read access |
| Formats | JSON |

## License and reuse

WoRMS content is generally made available under **CC-BY 4.0**, with a required citation format. Confirm the current terms and cite WoRMS per their requested format on any reuse. Any future connector must record the exact license string before it can be marked verified.

## Fields

`AphiaID` (the stable WoRMS taxon id), `scientificname`, `authority`, `status` (accepted/unaccepted), `rank`, `valid_name` (the accepted name if the queried name is a synonym), and a kingdom→genus classification. The WoRMS API may return `null` for no match; a future connector must preserve that as an explicit empty result.

## Limitations and ethics

- Taxonomy only — no occurrence or location data, so no coordinate-precision ethics apply.
- Names and statuses change as taxonomy is revised; treat a resolution as "as of" its access date.

## How it's used in the commons

This card records WoRMS as a candidate authority for accepted-name checks in species pages and future guardian work. Blue Life Commons does not currently publish a WoRMS connector here. Treat an implementation as unavailable until its code, tests, provenance, license handling, and empty-result behavior are publicly inspectable.

## Sources

- [WoRMS REST API documentation](https://www.marinespecies.org/rest/) (accessed 2026-06-11)
- [WoRMS web services overview](https://www.marinespecies.org/aphia.php?p=webservice) (accessed 2026-06-11)
