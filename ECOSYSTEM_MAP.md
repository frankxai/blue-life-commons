# Ocean Intelligence Ecosystem Map

Four repositories form a vertically integrated ocean intelligence stack — from raw knowledge through live intelligence to end-user applications. Each layer is independently useful; together they form a closed loop from ocean science to human action.

---

## Layer 1: Knowledge Commons

**[blue-life-commons](https://github.com/frankxai/blue-life-commons)** *(this repo)*

- **License:** CC-BY-4.0
- **What's here:** 58+ knowledge artifacts — species pages, region briefings, sustainable practices, ocean wisdom library, welfare assessments, dataset cards, partner profiles, field mission protocols, research summaries
- **Governance:** `ETHICS.md` (non-negotiable) · `SOURCES.md` (Tier 1–3 sourcing) · `schema/artifact-schema.yaml` (machine-validated schema)
- **Who uses it:** NGOs (advocacy, grant evidence) · researchers (synthesis starting point) · creators (story material) · all Guardian agents (knowledge grounding)

This layer stays open and CC-BY-4.0 permanently. It is never paywalled, never commercialized directly.

---

## Layer 2: Intelligence Layer

**[ocean-intelligence-system](https://github.com/frankxai/ocean-intelligence-system)**

- **License:** MIT (code)
- **What's here:** 11 real-time data connectors, Guardian agent framework, REST gateway, dashboard
- **Connectors:**

| Connector | Signal | Source |
|-----------|--------|--------|
| OBIS | Species occurrence | api.obis.org |
| GBIF | Species occurrence | api.gbif.org |
| NOAA Coral Reef Watch | Bleaching alerts | coralreefwatch.noaa.gov |
| WoRMS | Taxonomy | marinespecies.org/rest |
| Protected Planet | MPA boundaries | api.protectedplanet.net |
| Copernicus Marine | SST, salinity, currents | marine.copernicus.eu |
| Global Fishing Watch | Vessel tracking | globalfishingwatch.org/api |
| iNaturalist | Community observations | api.inaturalist.org/v1 |
| IUCN Red List | Conservation status | apiv4.iucnredlist.org |
| NOAA ERDDAP | Ocean time-series | coastwatch.pfeg.noaa.gov/erddap |
| Argo | Depth profiles | argo.ucsd.edu |

- **Guardian archetypes:** Reef · Bay · Species · Fishery · Coastal-Community · Migratory-Corridor · Sanctuary · Stranding-Network
- **Who uses it:** Developers (REST API) · researchers (connector queries) · NGOs (dashboard access) · Guardian agents (live data grounding)

---

## Layer 3: Agent Interfaces

### [marine-mcp](https://github.com/frankxai/marine-mcp) — TypeScript MCP Server

Install once, query everything:

```bash
claude mcp add marine -- npx @frankxai/marine-mcp
```

**Available tools:**

| Tool | What it does |
|------|-------------|
| `species-lookup` | Returns species page + IUCN status + live connector link |
| `region-briefing` | Returns regional briefing + active Guardian agents |
| `guardian-query` | Queries a named Guardian agent for current signals |
| `connector-signal` | Calls a live data connector for current readings |
| `practice-guide` | Returns sustainable practice guidance by domain |
| `wisdom-query` | Queries the ocean wisdom library by topic |

- **Who uses it:** Agentic developers building on any MCP-capable AI assistant (Claude, GPT-4o, Gemini, etc.)

### [marine-agent-skills](https://github.com/frankxai/marine-agent-skills) — Claude Code Skill Pack

**Available skills:**

| Skill | Purpose |
|-------|--------|
| `/species-page` | Generate a schema-valid species page |
| `/field-mission` | Create a field mission protocol |
| `/ethics-check` | Run ethics review on a draft artifact |
| `/source-verify` | Verify all citations against SOURCES.md tiers |
| `/guardian-spawn` | Scaffold a new Guardian agent definition |
| `/connector-build` | Scaffold a new OIS data connector |
| `/validate-artifact` | Full schema + ethics + source validation pass |
| `/open-artifact-pr` | Push a validated artifact and open a PR |

- **Who uses it:** Claude Code users contributing to the commons or building ocean applications

---

## Data Flow

```
[Live APIs: OBIS, GBIF, NOAA CRW, WoRMS, Copernicus, GFW, iNaturalist, IUCN, ERDDAP, Argo]
        |
        ▼
[OIS Connectors — polling, normalization, anomaly detection]
        |
        ▼
[Guardian Agents — ecosystem watch, alert generation, synthesis]
        |                        ▲
        ▼                        |
[REST Gateway]        [BLC Knowledge Layer — species, regions, practices, wisdom]
        |                        ▲
        ▼                        |
[Applications]        [marine-mcp / marine-agent-skills — agent access]
```

---

## Verified API Sources (all open / free tier)

| API | Signal | Rate Limit |
|-----|--------|----------|
| OBIS (api.obis.org) | Species occurrence | None |
| GBIF (api.gbif.org) | Species occurrence | None |
| NOAA Coral Reef Watch | Bleaching alerts | None |
| WoRMS (marinespecies.org/rest) | Taxonomy | None |
| Protected Planet (api.protectedplanet.net) | MPAs | Free key required |
| Copernicus Marine | SST, salinity, currents | Free account required |
| Global Fishing Watch | Vessel tracking | Free token required |
| iNaturalist (api.inaturalist.org/v1) | Community observations | None |
| IUCN Red List (apiv4.iucnredlist.org) | Conservation status | Free token required |
| NOAA ERDDAP | Ocean time-series | None |
| Argo (argo.ucsd.edu) | Depth profiles | None |

---

## Governance Principles

1. **Knowledge stays free.** BLC is CC-BY-4.0 permanently. No exceptions.
2. **Intelligence is open-source.** OIS is MIT. The code is yours.
3. **Agent interfaces are open-source.** marine-mcp and marine-agent-skills are MIT.
4. **Science and ethics gates are non-negotiable.** Every artifact in BLC passes source, ethics, and schema review. Community vote cannot override ETHICS.md or SOURCES.md.
5. **Attribution travels with artifacts.** Every BLC artifact carries contributor credit and source citations through all downstream uses.

---

*For the full contributor guide, see [CONTRIBUTING.md](CONTRIBUTING.md). For persona-specific guides, see [docs/personas/](docs/personas/).*
