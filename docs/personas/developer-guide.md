# Guide for App Developers and Agentic Developers

The ocean intelligence stack exposes two complementary interfaces: a REST API via the Ocean Intelligence System for server-to-server and browser applications, and an MCP server for AI assistants and agentic workflows. Both are open-source and free to use.

---

## Quick Start: marine-mcp (AI Agents)

If you're building with Claude Code, Claude Desktop, or any MCP-capable AI assistant, install the marine MCP server:

```bash
claude mcp add marine -- npx @frankxai/marine-mcp
```

This gives your AI assistant access to 6 ocean intelligence tools:

| Tool | What it does |
|------|-------------|
| `species-lookup` | Returns species page, IUCN status, range, threats, and live connector link |
| `region-briefing` | Returns full regional briefing + active Guardian agent signals |
| `guardian-query` | Queries a named Guardian for current ecosystem signals |
| `connector-signal` | Calls a live data connector for a current reading |
| `practice-guide` | Returns sustainable practice guidance by domain (fisheries, diving, etc.) |
| `wisdom-query` | Queries the ocean wisdom library by topic or keyword |

All tools return grounded responses — they only assert facts that are review-approved in BLC, and they carry `sources[]` in every response payload.

Full marine-mcp documentation: [github.com/frankxai/marine-mcp](https://github.com/frankxai/marine-mcp)

---

## OIS REST API

Base URL: `https://api.ocean-intelligence.org/v1`

Authentication: Free API key via [ocean-intelligence-system/README.md](https://github.com/frankxai/ocean-intelligence-system#api-access). Pass as `Authorization: Bearer YOUR_TOKEN`.

### Key Endpoints

```
GET  /guardians                          — List all active Guardian agents
GET  /guardians/:id                      — Guardian status + current signals
GET  /guardians/:id/briefing             — Latest Guardian briefing document
GET  /connectors                         — List available data connectors
GET  /connectors/:id/query               — Query a connector with params
GET  /signals                            — Recent anomaly signals (all regions)
GET  /signals?region=:region             — Signals filtered by region
POST /webhooks                           — Subscribe to Guardian alert webhooks
GET  /species/:name                      — Species page from BLC
GET  /regions/:id                        — Region briefing from BLC
```

### TypeScript / JavaScript Example

```typescript
const OIS_BASE = "https://api.ocean-intelligence.org/v1";
const TOKEN = process.env.OIS_API_TOKEN;

// Fetch all active Guardian agents
const res = await fetch(`${OIS_BASE}/guardians`, {
  headers: { Authorization: `Bearer ${TOKEN}` }
});
const { guardians } = await res.json();

// Query OBIS connector for species occurrence in a region
const occurrence = await fetch(
  `${OIS_BASE}/connectors/obis/query?scientificname=Megaptera+novaeangliae&area=monterey-bay`,
  { headers: { Authorization: `Bearer ${TOKEN}` } }
);
const data = await occurrence.json();
// data.occurrences[], data.total_records, data.date_range, data.sources[]

// Subscribe to bleaching alerts for a region
await fetch(`${OIS_BASE}/webhooks`, {
  method: "POST",
  headers: {
    Authorization: `Bearer ${TOKEN}`,
    "Content-Type": "application/json"
  },
  body: JSON.stringify({
    region: "great-barrier-reef",
    signals: ["bleaching_alert", "sst_anomaly"],
    threshold: "moderate",
    callback_url: "https://your-app.com/webhooks/ocean"
  })
});
```

---

## Guardian Archetype Quick Reference

| Archetype | Watch Focus | Primary Connectors |
|-----------|-------------|-------------------|
| **Reef** | Coral bleaching, thermal stress | NOAA CRW, Copernicus SST |
| **Bay** | Ecosystem health, species assemblage | OBIS, GBIF, ERDDAP |
| **Species** | Population signals for a named species | IUCN, OBIS, GBIF |
| **Fishery** | Fishing pressure, vessel activity | Global Fishing Watch |
| **Coastal-Community** | Stranding events, pollution signals | iNaturalist, OBIS |
| **Migratory-Corridor** | Species movement, corridor integrity | OBIS, GBIF, Argo |
| **Sanctuary** | MPA compliance, boundary monitoring | Protected Planet, GFW |
| **Stranding-Network** | Stranding reports, rescue coordination | iNaturalist, community reports |

---

## Webhook Payload Structure

Guardian alert webhooks deliver a structured JSON payload:

```typescript
interface GuardianAlert {
  alert_id: string;
  guardian_id: string;
  region: string;
  signal_type: "bleaching_alert" | "sst_anomaly" | "occurrence_gap" | "fishing_pressure" | "stranding_event";
  severity: "low" | "moderate" | "high" | "critical";
  value: number;
  baseline: number;
  deviation_pct: number;
  connector: string;
  timestamp: string;                   // ISO 8601
  briefing_url: string;
  sources: Array<{ citation: string; url: string; tier: 1 | 2 | 3 }>;
}
```

---

## marine-agent-skills (Contributing via Claude Code)

If you want to contribute artifacts to BLC from a Claude Code workflow:

```bash
npx skills add frankxai/marine-agent-skills
```

Available skills: `/species-page` · `/field-mission` · `/ethics-check` · `/source-verify` · `/guardian-spawn` · `/connector-build` · `/validate-artifact` · `/open-artifact-pr`

See [github.com/frankxai/marine-agent-skills](https://github.com/frankxai/marine-agent-skills) for full skill documentation and the contribution workflow.

---

## Full API Documentation

Complete API reference, authentication setup, rate limits, and SDK clients: [github.com/frankxai/ocean-intelligence-system/docs/api/](https://github.com/frankxai/ocean-intelligence-system/docs/api/)

Ecosystem architecture: [`ECOSYSTEM_MAP.md`](../../ECOSYSTEM_MAP.md)
