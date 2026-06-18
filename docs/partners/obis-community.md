# OBIS — Contributing Occurrence Data Back to the Community

| Field | Value |
|---|---|
| Partner | OBIS — Ocean Biodiversity Information System (obis.org) |
| Records | 130M+ occurrence records |
| Publishing Nodes | 160+ IPTs worldwide |
| OBIS Secretariat | Flanders Marine Institute (VLIZ), Belgium |
| Required Format | Darwin Core Archive |
| Data License Options | CC0 · CC-BY · CC-BY-NC |
| Contact | obis.org/contact |

OBIS is the global open-access repository for marine species occurrence data. With more than 130 million records contributed by 160+ publishing nodes worldwide, it is the authoritative aggregator for marine biodiversity observations. GBIF and OBIS are mirrored — a single Darwin Core Archive submission reaches both systems simultaneously. BLC reads from OBIS via the OIS connector; this guide covers the reciprocal path: contributing field mission observations back into the OBIS network so that BLC citizen science data reaches the global record.

---

## Integration Points

### OIS `obis` Connector (Read Path)

The OIS `obis` connector queries occurrence records to support species pages, range maps, and guardian briefings. The `source-verify` skill validates that OBIS occurrences referenced in species pages carry a valid `dataset_id`, ensuring that citations trace to a real published dataset rather than to OBIS as a generic aggregator. Species pages should cite specific OBIS dataset DOIs, not just "via OBIS."

### Contributing Field Mission Observations (Write Path)

Observations generated through BLC citizen science programmes should be contributed back to OBIS through the following process:

1. **Assign a Darwin Core dataset ID before the mission launches.** Pre-registration ensures provenance is intact from the first data record rather than assigned retrospectively. Contact an OBIS node to obtain a dataset identifier.

2. **Format data as Darwin Core Archive.** OBIS provides templates and guidance at [obis.org/contribute](https://obis.org/contribute). Required fields include `occurrenceID`, `scientificName`, `decimalLatitude`, `decimalLongitude`, `eventDate`, and `basisOfRecord`.

3. **Submit through an OBIS node.** Data goes through a national or thematic IPT (Integrated Publishing Toolkit) node. The OBIS Secretariat can direct contributors to the most appropriate node for their geography or taxonomic focus.

4. **Pass automated QC.** OBIS runs coordinate validation, taxonomy alignment to the World Register of Marine Species (WoRMS), and duplicate detection. The BLC `source-verify` skill checks outgoing datasets against the same criteria before submission to reduce rejection rates.

### License Requirements for Contributed Data

OBIS accepts datasets under three licenses only: **CC0**, **CC-BY**, or **CC-BY-NC**. BLC field missions use **CC0 for occurrence data**. This is a deliberate choice that maximises reuse by the research community and is consistent with the OBIS community norm. This license applies only to the raw occurrence data, not to the narrative content of the BLC artifact — the associated field mission briefing, methodology notes, and interpretive content remain under CC-BY-4.0.

### GBIF Mirroring

Because OBIS and GBIF are mirrored, a single Darwin Core Archive submission to an OBIS node automatically makes the data discoverable on [gbif.org](https://www.gbif.org). This double reach increases citation potential and ensures the data appears in the broadest possible downstream analyses.

---

## Attribution Standard

BLC species pages cite the specific OBIS dataset DOI rather than a generic OBIS reference:

```
Occurrence data: [Dataset Name], [Institution], via OBIS
DOI: [dataset-specific DOI]
```

This enables precise provenance tracing and ensures that data contributors receive accurate citation credit in downstream uses of the record.

---

*Built on SIP · Blue Life Commons (CC-BY-4.0)*
