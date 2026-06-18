---
id: visualization-toolkit
type: educational
title: "Ocean Data Visualization Toolkit: Maps, Charts, and Infographics Using Open Ocean Data"
status: needs-expert-review
sources:
  - url: "https://coralreefwatch.noaa.gov/"
    title: "NOAA Coral Reef Watch"
    accessed: "2026-06-18"
    tier: 2
  - url: "https://obis.org/"
    title: "Ocean Biodiversity Information System (OBIS)"
    accessed: "2026-06-18"
    tier: 2
  - url: "https://www.protectedplanet.net/"
    title: "Protected Planet — UNEP-WCMC"
    accessed: "2026-06-18"
    tier: 2
review:
  science: required
  ethics: not-applicable
  editor: required
outputs:
  website_path: /academy/visualization-toolkit
  github_path: content/academy/visualization-toolkit.md
license: CC-BY-4.0
contributors:
  - github: frankxai
---

# Ocean Data Visualization Toolkit: Maps, Charts, and Infographics Using Open Ocean Data

The most important ocean data is open, authoritative, and publicly accessible. The challenge is not finding it — it is knowing which sources to use, how to query them, and how to turn raw numbers into visuals that communicate clearly to non-specialist audiences.

This toolkit covers the four main visualization types (maps, time series, comparison charts, infographics) and the specific open data sources and tools appropriate for each.

---

## Foundational Data Sources

Before building any visualization, know your sources. All sources below are free, authoritative, and appropriate for publication-grade work.

### Occurrence and Biodiversity Data

| Source | Type | URL | License | Best for |
|--------|------|-----|---------|---------|
| **OBIS** | Marine species occurrences | obis.org | CC0/CC-BY | Species range maps, sighting density maps |
| **GBIF** | All biodiversity occurrences | gbif.org | CC0/CC-BY | Cross-taxa occurrence maps |
| **iNaturalist** | Citizen science observations | inaturalist.org | CC BY-NC | Community-verified sightings |

### Ocean State Data

| Source | Type | URL | License | Best for |
|--------|------|-----|---------|---------|
| **NOAA Coral Reef Watch** | Bleaching alerts, SST anomaly | coralreefwatch.noaa.gov | Public domain | Thermal stress maps |
| **Copernicus Marine (CMEMS)** | SST, salinity, currents, sea level | marine.copernicus.eu | CC-BY 4.0 | Oceanographic state maps |
| **NOAA ERDDAP** | Buoy, satellite SST, wave data | coastwatch.noaa.gov/erddap | Public domain | Time series charts |
| **Argo Float Network** | In-situ depth profiles | argo.ucsd.edu | Public domain | Subsurface temperature/salinity |

### Protection and Governance

| Source | Type | URL | License | Best for |
|--------|------|-----|---------|---------|
| **Protected Planet (WDPA)** | Marine protected areas | protectedplanet.net | CC-BY 4.0 | MPA coverage maps |
| **Global Fishing Watch** | Vessel tracking, fishing effort | globalfishingwatch.org | CC-BY NC 4.0 | Fishing pressure overlays |
| **Marine Regions** | Ocean boundaries, EEZs | marineregions.org | CC-BY 4.0 | Jurisdiction maps |

### Biological Status

| Source | Type | URL | License | Best for |
|--------|------|-----|---------|---------|
| **IUCN Red List** | Species conservation status | iucnredlist.org | Restricted (cite) | Status indicators, threat lists |
| **WoRMS** | Marine species taxonomy | marinespecies.org | CC0 | Taxonomic accuracy verification |

---

## Visualization Type 1: Species Distribution Maps

**What they show**: Where a species has been observed, and how its range has changed over time.

**Best data source**: OBIS (marine) or GBIF (all biodiversity)

**Query approach for OBIS**:
```
https://api.obis.org/v3/occurrence?
  scientificname=Megaptera novaeangliae  # URL-encoded species name
  &startdate=2020-01-01
  &enddate=2026-01-01
  &size=1000
```

Returns: lat/lon points with date, depth, dataset source.

**Recommended tools**:
- **QGIS** (free, desktop): Full GIS with OBIS WFS plugin. Best for print-quality maps.
- **Leaflet.js** (free, web): Interactive web maps. Stack OBIS points over OpenStreetMap base layer.
- **Kepler.gl** (free, web): Drag-and-drop CSV upload, instant density maps. Good for rapid iteration.
- **Observable Plot** (free, web): Code-based, D3-powered. Best for publication-grade static maps.

**Design guidance**:
- Use point density (hexbins or kernel density) rather than individual dots for >500 records — dots overlap and obscure pattern
- Include a time filter: occurrence maps that pool all records (1950–2026) obscure range shifts; use decade or 5-year bins
- Cite OBIS + the specific dataset DOI in the legend or caption
- Color: for density maps, sequential (light→dark single hue) is more readable than diverging for occurrence data

**Example output**: Humpback whale occurrence density in the Southern Ocean 2015–2025, aggregated to 2° hexbins. Shows key feeding concentrations and migration corridors.

---

## Visualization Type 2: Ocean State Maps

**What they show**: Sea surface temperature, bleaching alerts, chlorophyll, sea level anomaly, or current patterns.

**Best data source**:
- Real-time/recent: NOAA Coral Reef Watch (bleaching alerts), ERDDAP (SST)
- Historical/climatological: Copernicus Marine (CMEMS)

**Coral bleaching heat stress (DHW) — getting the data**:

NOAA CRW provides 5km gridded daily SST and Degree Heating Week (DHW) products via their API:
```
https://coralreefwatch.noaa.gov/product/5km/index_5km_dhw.php
```
GeoTIFF downloads are available for any date range. DHW ≥4 → bleaching watch; DHW ≥8 → severe bleaching likely.

**Sea surface temperature from ERDDAP**:
```
https://coastwatch.noaa.gov/erddap/griddap/erdMH1sstd8day.nc?
  sst[(2026-01-01):(2026-06-01)][(−90):(90)][(−180):(180)]
```
Returns NetCDF. Use `xarray` (Python) or QGIS raster import to visualize.

**Recommended tools**:
- **NASA WorldWind / Google Earth Engine** (free): Global raster display, temporal animation. Best for exploratory work.
- **Matplotlib + Cartopy** (Python, free): Publication-quality raster maps with coastlines and projections.
- **QGIS**: Drag NetCDF/GeoTIFF files, apply colour ramps, export as print-quality PNG/PDF.
- **Datawrapper** (web, free tier): Limited but fast for SST anomaly choropleths.

**Design guidance**:
- For temperature anomaly maps, use a diverging colour scale centred on 0 (blue = cooler than average, red = warmer). The classic blue–white–red RdBu palette (from ColorBrewer) is colour-blind-safe.
- Label bleaching threshold thresholds in the legend (e.g., "DHW ≥4 = Watch; DHW ≥8 = Alert Level 2")
- Always include: projection name, data source, date of data, spatial resolution

---

## Visualization Type 3: Time Series Charts

**What they show**: How an ocean metric has changed over months, years, or decades.

**Key metrics and sources**:

| Metric | Source | Years available |
|--------|--------|----------------|
| Global mean sea surface temperature | NOAA ERDDAP, HadSST | 1850–present |
| Ocean pH (proxy from Southern Ocean buoys) | SOCAT | 1991–present |
| Arctic sea ice extent | NSIDC | 1979–present |
| Coral bleaching events (major events) | NOAA CRW alert archive | 1998–present |
| IUCN Red List assessments (species count by category) | IUCN Red List Index | 1993–present |

**Ocean pH decline — 30-year time series**:

Pre-industrial pH: 8.18 (reconstructed from ice cores and boron isotopes)
1988: ~8.10
2010: ~8.09
2026: ~8.08
Rate: −0.0017 pH units/year, accelerating slightly after 2010.

*Note: Direct open-ocean pH time series data comes primarily from the Hawaii Ocean Time-series (HOT) and Bermuda Atlantic Time-series (BATS) programs — SOCAT.*

**Recommended tools**:
- **Observable Plot / D3.js** (JavaScript, free): Best for interactive web time series with annotations
- **Matplotlib / Seaborn** (Python, free): Clean static charts; easy to add IPCC-style confidence intervals
- **Datawrapper** (web): Fastest for simple line/area charts without code
- **Flourish** (web): Good for animated time series that show change over time

**Design guidance**:
- Annotate key events on the time axis: 1998 mass bleaching event, 2016 El Niño bleaching, 2020–2023 La Niña, etc.
- For ocean pH or temperature: show the pre-industrial baseline as a horizontal dashed reference line
- Use area charts (filled) when showing cumulative effects; line charts for rates/trends
- For multi-metric charts: normalize to percentage of pre-industrial baseline rather than raw values — makes different units comparable

---

## Visualization Type 4: Comparative / Ranking Charts

**What they show**: Comparisons across species, regions, countries, or time periods.

**Key comparison datasets**:

- **MPA coverage by country**: Protected Planet API → filter by IUCN marine categories I–VI → group by country ISO
- **IUCN Red List by taxonomic group**: Red List API → filter by `kingdom=ANIMALIA, class=ACTINOPTERYGII` (fish) → tally by category
- **Ocean health by region**: Ocean Health Index (ohiproject.org) provides 10-dimension scores for 220 EEZs annually

**MPA coverage comparison — getting the data**:
```
https://api.protectedplanet.net/v3/protected_areas?
  token=YOUR_TOKEN
  &with_geometry=false
  &marine=true
  &per_page=50
```
Download the WDPA flat file (available as GDB or CSV from protectedplanet.net) for bulk analysis. Filter for `MARINE ≥1`, compute area per country.

**Recommended tools**:
- **Datawrapper bar/ranking charts**: Clean, fast, includes source line in footer
- **ggplot2** (R): Best for IUCN Red List category breakdown with confidence intervals
- **Observable Plot** (JavaScript): Dot plots, lollipop charts, and small multiples in browser
- **Flourish**: Animated ranking race charts (good for time-progression of MPA coverage 2000→2030)

**Design guidance**:
- For regional comparison: group by ocean basin (Atlantic, Pacific, Indian, Arctic, Southern) before breaking down by country — regional pattern is more important than individual country position
- Include the global average as a reference bar in any country comparison
- For IUCN categories: use the IUCN standard colours (CR = red, EN = orange, VU = yellow, NT = light green, LC = dark green, DD = grey) — audiences recognise them

---

## Visualization Type 5: Infographics

**What they show**: A complete narrative about a single ocean topic, combining data, mechanism diagrams, and context — no specialist knowledge required to read.

**Best uses**:
- Explainers for policy audiences (ocean acidification chemistry, 30×30 MPA case)
- Annual state-of-the-ocean summaries
- Species profiles with population timeline + threat map + IUCN badge

**Infographic anatomy for ocean topics**:

```
Title (1 line, includes the key number)
    ↓
Lead statistic (big number, bold, sourced)
    ↓
Mechanism diagram (2–4 step visual)
    ↓
Geographic map (where this is happening)
    ↓
Impact data (who/what is affected, quantified)
    ↓
Trend chart (how it's changed over time)
    ↓
Call to action + attribution
```

**Recommended tools**:
- **Canva** (web): Templates available; drag-and-drop; good for social media infographics
- **Adobe Illustrator** / **Inkscape** (Inkscape is free): Vector graphics; best for print-quality infographics
- **Flourish**: Pre-built infographic templates with live data connections
- **Piktochart** (web): Education-focused infographics; includes map and chart embeds

**Key design rule**: Every data point in the infographic must trace to a source. Include a "Data Sources" section in fine print at the bottom. The BLC standard is to link to the specific artifact, not just the source website.

---

## The Five Core Ocean Numbers (Always Cite These Correctly)

These are the five statistics most commonly used in ocean storytelling. Use the correct phrasing and source for each:

| Metric | Value (2026) | Source | Correct phrasing |
|--------|-------------|--------|-----------------|
| Ocean temperature anomaly | +1.1°C above pre-industrial | NOAA/WMO global mean | "Ocean surface temperature is now +1.1°C above the pre-industrial baseline" |
| Ocean pH | 8.08 (was 8.18 pre-industrial) | SOCAT/HOT/BATS | "Ocean pH has declined from 8.18 pre-industrially to approximately 8.08 today" |
| Coral reef coverage lost | −50% since 1950 | Global Coral Reef Monitoring Network | "Coral reefs have lost approximately 50% of their global coverage since 1950" |
| Ocean protected | 8.1% (2.7% fully protected) | UNEP-WCMC / Protected Planet 2026 | "As of 2026, 8.1% of the global ocean falls within a marine protected area" |
| Plastic entering ocean annually | 8–12 million tonnes | Jambeck et al. 2015 (range updated) | "An estimated 8–12 million tonnes of plastic enter the ocean each year" |

**Do not round to "about 50%" without specifying "since 1950."** The baseline matters — the percentage is meaningless without the reference year.

---

*Built on SIP · Blue Life Commons (CC-BY-4.0)*
