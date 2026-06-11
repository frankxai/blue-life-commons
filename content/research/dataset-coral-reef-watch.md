---
id: dataset-coral-reef-watch
type: dataset-card
title: "Dataset Card: NOAA Coral Reef Watch — 5km Bleaching Heat-Stress Products"
species_group:
  - reefs
audience:
  - researcher
  - developer
status: draft
sources:
  - url: "https://coralreefwatch.noaa.gov/product/5km/"
    title: "NOAA Coral Reef Watch — Daily 5km Satellite Coral Bleaching Heat Stress Products (v3.1)"
    accessed: "2026-06-11"
  - url: "https://coastwatch.noaa.gov/erddap/info/noaacrwbaa7dDaily/index.html"
    title: "ERDDAP — NOAA CRW Daily Global 5km Bleaching Alert Area 7-day Max Composite"
    accessed: "2026-06-11"
  - url: "https://coralreefwatch.noaa.gov/product/5km/index_5km_dhw.php"
    title: "NOAA Coral Reef Watch — Degree Heating Week Product (v3.1)"
    accessed: "2026-06-11"
review:
  science: required
  ethics: not-applicable
  editor: pending
outputs:
  website_path: /research/dataset-coral-reef-watch
  github_path: content/research/dataset-coral-reef-watch.md
  map_layer: false
impact:
  claim: "Documented NOAA Coral Reef Watch 5km bleaching heat-stress products as the reef-guardian alert source."
  eligible_for_hypercert: true
contributors:
  - github: frankxai
license: CC-BY-4.0
---

# Dataset Card: NOAA Coral Reef Watch — 5km Bleaching Heat-Stress Products

> Status: draft, awaiting maintainer review. Products, access paths, and public-domain status checked against NOAA Coral Reef Watch documentation on 2026-06-11. This is the spine of the Reef Guardian.

## What it is

NOAA Coral Reef Watch (CRW) operates satellite-based monitoring of coral-reef thermal stress. Its daily global **5km (v3.1)** product suite turns sea surface temperature into the earliest legible warning of bleaching risk. These are the signals a reef guardian watches.

## Products

| Product | What it means |
|---|---|
| Sea Surface Temperature (SST) & SST Anomaly | Current temperature and departure from normal |
| Coral Bleaching HotSpot | Where SST exceeds the local bleaching threshold |
| Degree Heating Week (DHW) | **Accumulated** heat stress over the prior 12 weeks — the key bleaching-risk metric |
| Bleaching Alert Area (BAA, 7-day max) | Categorical alert level (No Stress → Watch → Warning → Alert Level 1/2…) derived from DHW |
| SST Trend, Regional Virtual Stations | Longer-term trend; per-reef time series |

Time series extend back to 1985 for most products.

## Access

| Field | Value |
|---|---|
| Provider | NOAA / NESDIS / STAR Coral Reef Watch |
| Docs | [CRW 5km products](https://coralreefwatch.noaa.gov/product/5km/) |
| Formats | NetCDF4 |
| Delivery | FTP, HTTP, THREDDS, and **ERDDAP** servers (e.g. dataset `noaacrwbaa7dDaily` on coastwatch.noaa.gov/erddap; `NOAA_DHW` on coastwatch.pfeg.noaa.gov/erddap) |
| Auth | None — free download and use |

## License and reuse

NOAA Coral Reef Watch products are **U.S. Government works in the public domain** and freely accessible for research and management. Attribution to NOAA Coral Reef Watch is expected as good practice.

## Fields

Gridded (5km) values per product: latitude, longitude, time, and the product variable (e.g. `CRW_BAA`, `CRW_DHW`, `CRW_SST`). The BAA categorical levels are the values a guardian translates into plain-language alerts.

## Limitations and ethics

- A **single warm week is not a bleaching event.** DHW measures *accumulated* stress; report alert levels exactly as CRW defines them and never invent a forecast beyond the product.
- Satellite SST has limitations in shallow, turbid, or nearshore reef environments; treat 5km grid cells as regional, not site-precise.
- No wildlife-location sensitivity (environmental grid), so ethics review is not applicable to the dataset itself — but a reef guardian's *outputs* still follow ETHICS.md.

## How it's used in the commons

The `alert` and `ocean-state` source for Reef Guardians (Ocean Intelligence System), and the evidence base for reef region briefings. Connector spec: `integrations/coral-reef-watch.md`.

## Sources

- [NOAA Coral Reef Watch — Daily 5km Heat Stress Products (v3.1)](https://coralreefwatch.noaa.gov/product/5km/) (accessed 2026-06-11)
- [ERDDAP — NOAA CRW Bleaching Alert Area 7-day Max](https://coastwatch.noaa.gov/erddap/info/noaacrwbaa7dDaily/index.html) (accessed 2026-06-11)
- [NOAA Coral Reef Watch — Degree Heating Week Product](https://coralreefwatch.noaa.gov/product/5km/index_5km_dhw.php) (accessed 2026-06-11)
