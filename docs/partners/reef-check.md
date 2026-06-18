# Reef Check — Coral Monitoring Data Integration

| Field | Value |
|---|---|
| Partner | Reef Check (reefcheck.org) |
| Survey Scope | 17,700+ survey transects · 40+ countries |
| Methodology | Reef Check Methodology (EcoDiver + Master Reef Check Diver protocols) |
| OBIS Dataset DOI | [10.15468/kzovne](https://doi.org/10.15468/kzovne) |
| Data Submission | EzReef (online database at reefcheck.org) |
| Contact | reefcheck.org/contact |

Reef Check is the largest standardised coral reef monitoring programme in the world. Since 1996, its trained EcoDivers and Master Reef Check Divers have surveyed reefs using a consistent transect methodology that produces comparable data across geographies and time. This standardisation makes Reef Check data a reliable baseline for BLC species pages, field mission design, and OIS ground-truth validation.

---

## Integration Points

### BLC Species Pages

Reef Check surveys produce OBIS-compliant output, meaning their dataset is published to the Ocean Biodiversity Information System and is queryable via the BLC `obis` connector. BLC species pages for taxa that appear in Reef Check transects should link to the Reef Check dataset on OBIS using the canonical DOI: `10.15468/kzovne`. This ensures provenance is traceable to the original survey record rather than an intermediate aggregator.

### Field Mission Design (`/field-mission` artifacts)

The Master Reef Check Diver certification is the recognised standard for BLC field missions that involve coral transect work. Authors writing `/field-mission` artifacts for coral reef sites should:

1. Note whether the site has existing Reef Check survey history (queryable via OBIS)
2. Specify whether the mission follows Reef Check Methodology for transect layout and indicator species
3. Record findings in EzReef if the mission coordinator holds a Master Reef Check Diver certification, enabling contribution back to the global dataset

### OIS Coral Reef Watch Connector Pairing

The OIS `coral-reef-watch` connector provides NOAA thermal stress data (Degree Heating Weeks, bleaching alerts) at the regional level. Reef Check survey results provide ground-truth confirmation of whether thermal events translated into actual bleaching and mortality at specific sites. The OIS–Reef Check pairing is the satellite-plus-ground-truth stack: OIS sees the heat anomaly; Reef Check surveys document the ecological outcome. When both data streams are available for a region, guardian briefings should present them together.

### For Guardians

GBR Guardian and other reef-region guardians in OIS cross-reference Reef Check survey sites when records are available through OBIS. Guardian briefings that cite thermal stress events benefit from including the nearest Reef Check survey timestamp and coral cover percentage, which contextualises the satellite signal with observed reef condition.

---

## Data Contribution Path

Reef Check accepts data contributions through their [EzReef online database](https://www.reefcheck.org/tropical-program/submit-your-data/). Submissions require a trained EcoDiver or Master Reef Check Diver to ensure data quality. BLC citizen science programmes that train participants to Reef Check standards can contribute directly, with data appearing in subsequent OBIS dataset releases.

---

## Attribution Standard

BLC content that draws on Reef Check methodology or data cites both the organisation and the specific dataset:

```
Coral monitoring methodology: Reef Check (reefcheck.org)
Survey data: Reef Check via OBIS, DOI: 10.15468/kzovne
```

---

*Built on SIP · Blue Life Commons (CC-BY-4.0)*
