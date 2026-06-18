# Guide for Oceanographers and Conservation Researchers

Blue Life Commons gives researchers a sourced, schema-validated synthesis layer on top of the major open ocean databases — so you can spend less time tracking down baseline data and more time on the work only your expertise can do.

---

## Data Access: Querying OIS Connectors

The Ocean Intelligence System exposes 11 live connectors via a REST gateway. All underlying APIs are open/free-tier — OIS normalizes their response formats, adds anomaly detection, and routes queries through the knowledge layer.

### Species Occurrence (OBIS / GBIF)

Query species occurrence data with geographic filtering:

```python
import requests

# Query species occurrence via OIS — OBIS connector
r = requests.get(
    "https://api.ocean-intelligence.org/v1/connectors/obis/occurrence",
    params={
        "scientificname": "Balaenoptera musculus",
        "area": "salish-sea"
    }
)
data = r.json()
# Returns: occurrences[], total_records, date_range, data_quality_score, source_doi

# Query via GBIF connector for cross-validation
r2 = requests.get(
    "https://api.ocean-intelligence.org/v1/connectors/gbif/occurrence",
    params={
        "species": "Balaenoptera musculus",
        "geometry": "POLYGON((-126 47,-122 47,-122 50,-126 50,-126 47))"
    }
)
```

### Ocean State (ERDDAP / Copernicus Marine)

```python
# Sea surface temperature anomaly — NOAA ERDDAP
r = requests.get(
    "https://api.ocean-intelligence.org/v1/connectors/erddap/sst",
    params={"region": "great-barrier-reef", "days": 30}
)

# Salinity and current data — Copernicus Marine
r = requests.get(
    "https://api.ocean-intelligence.org/v1/connectors/copernicus/oceanstate",
    params={"region": "monterey-bay", "variables": "temperature,salinity,oxygen"}
)
```

### Conservation Status (IUCN Red List)

```python
# Current IUCN assessment for a species
r = requests.get(
    "https://api.ocean-intelligence.org/v1/connectors/iucn/status",
    params={"species": "Phocoena sinus"}
)
# Returns: category, criteria, assessment_date, population_trend, threats[]
```

Full connector documentation: [ocean-intelligence-system/docs/connectors/](https://github.com/frankxai/ocean-intelligence-system/docs/connectors/)

---

## Setting Up Anomaly Alerts for Your Study Region

Guardian agents in OIS watch for significant signal deviations — bleaching alert tier changes, unusual occurrence gaps, fishing pressure spikes, oxygen level drops — and emit structured alert objects.

**Subscribe via webhook:**

```python
import requests

# Register a webhook for your study region
r = requests.post(
    "https://api.ocean-intelligence.org/v1/webhooks",
    headers={"Authorization": "Bearer YOUR_TOKEN"},
    json={
        "region": "salish-sea",
        "signals": ["sst_anomaly", "occurrence_gap", "bleaching_alert"],
        "threshold": "moderate",          # low | moderate | high | critical
        "callback_url": "https://your-lab-server.edu/ocean-alerts"
    }
)
webhook_id = r.json()["webhook_id"]
```

Alert payloads include signal type, magnitude, connector source, timestamp, and a link to the Guardian briefing that generated the alert. Appropriate for automated ingestion into lab monitoring pipelines.

---

## Contributing Species Pages and Research Summaries

BLC welcomes researcher contributions — new species pages, corrections to existing data, and literature synthesis summaries. All contributions are CC-BY-4.0 and permanently credited.

**Artifact submission workflow:**

1. **Install marine-agent-skills** (Claude Code): `npx skills add frankxai/marine-agent-skills`
2. **Scaffold a draft:** Run `/species-page` or `/field-mission` — the skill will prompt for species name, IUCN status, range, threats, and source citations, then generate a schema-valid YAML+Markdown artifact.
3. **Validate:** Run `/validate-artifact` — checks schema compliance, source tier requirements, and ethics flags.
4. **Open a PR:** Run `/open-artifact-pr` — pushes the artifact to a branch and opens a PR with the standard review checklist.
5. **Science review:** A science reviewer (researcher or vetted contributor) reviews within 7 days. Corrections go back as PR comments; no silent edits.

For research summaries (literature reviews, monitoring methodology assessments), use the Research Summary template at `.github/ISSUE_TEMPLATE/research-summary.md`.

---

## Literature Synthesis via Guardian Briefings

Each Guardian agent maintains a `knowledge_grounding` block that references all BLC artifacts relevant to its watch area. These can be used as pre-synthesized literature starting points.

Query a Guardian's knowledge index:

```python
r = requests.get(
    "https://api.ocean-intelligence.org/v1/guardians/salish-sea/knowledge",
    params={"topic": "prey-availability"}
)
# Returns: relevant_artifacts[], key_citations[], synthesis_note, last_updated
```

The synthesis note is a Guardian-generated paragraph summarizing the current knowledge state on the topic, grounded in Tier 1 sources. Treat it as a reviewed starting point, not a citable source — follow the `key_citations[]` back to primary literature.

---

## Direct Database Access

For full programmatic access to the underlying databases without OIS normalization:

| Database | Endpoint | Auth |
|----------|----------|------|
| OBIS | `https://api.obis.org/v3/` | None |
| GBIF | `https://api.gbif.org/v1/` | None |
| WoRMS | `https://www.marinespecies.org/rest/` | None |
| NOAA ERDDAP | `https://coastwatch.pfeg.noaa.gov/erddap/` | None |
| Argo | `https://argovis.colorado.edu/api/` | None |
| IUCN Red List | `https://apiv4.iucnredlist.org/api/v4/` | Free token required |
| iNaturalist | `https://api.inaturalist.org/v1/` | None (rate limits apply) |

Full verified source list: [`SOURCES.md`](../../SOURCES.md)
