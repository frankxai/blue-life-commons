# Global Fishing Watch — Fishing Effort Data Integration

| Field | Value |
|---|---|
| Partner | Global Fishing Watch (globalfishingwatch.org) |
| Data Types | AIS vessel tracking · fishing effort grids · port event data |
| License | CC-BY-NC 4.0 |
| API Access | Free token at globalfishingwatch.org/data-download/ |
| OIS Connector | `mcp/servers/global-fishing-watch/` (implemented) |
| Env Variable | `GFW_API_TOKEN` |

Global Fishing Watch (GFW) is the leading open data platform for monitoring fishing activity at sea. By processing satellite-based Automatic Identification System (AIS) transponder signals, GFW produces vessel tracking records, daily fishing effort grids, and port event data covering the global ocean. The data is available under CC-BY-NC 4.0 and is accessible via a free API token — no institutional affiliation required. The OIS `global-fishing-watch` connector is fully implemented and production-ready.

---

## Integration Points

### OIS Connector (`mcp/servers/global-fishing-watch/`)

The connector supports two primary query types:

- **Fishing effort by MMSI**: Query a specific vessel's activity history by Maritime Mobile Service Identity number, returning track points, fishing hours, and flag state.
- **MPA overlap queries**: Supply an MPA polygon (from the `protected-planet` connector) and return fishing effort statistics within that boundary — hours fished, number of vessels, gear types detected.

Set `GFW_API_TOKEN` in the OIS environment before use. Token registration is free at [globalfishingwatch.org/data-download](https://globalfishingwatch.org/data-download/).

### High Seas Fishing Guardian

The High Seas Fishing Guardian uses GFW data as its primary signal source for monitoring Areas Beyond National Jurisdiction (ABNJ). ABNJ — often called the high seas — cover approximately 64% of the ocean's surface and are subject to limited enforcement. GFW fishing effort grids for ABNJ waters feed directly into guardian briefings, providing evidence of activity levels, fleet compositions, and temporal patterns in regions that are otherwise opaque to monitoring.

### NGO Advocacy Use Case

GFW's "fishing in MPAs" query pattern is particularly valuable for advocacy work. Pairing GFW fishing effort data with Protected Planet MPA polygon boundaries produces direct, citable evidence of potential violations. The workflow:

1. Retrieve MPA polygon via `protected-planet` connector
2. Query GFW fishing effort within that polygon for the target time window
3. Export the combined dataset for inclusion in advocacy reports or regulatory submissions

### For Content Authors

BLC wisdom articles and field mission briefs covering overfishing, illegal fishing, or ABNJ governance can reference GFW as a data source. GFW publishes an annual global fishing activity dataset that is frequently cited in peer-reviewed literature, providing citable provenance for factual claims.

---

## License Constraint

GFW data is published under **CC-BY-NC 4.0**. Commercial use of GFW data requires a separate written agreement with Global Fishing Watch. BLC content that incorporates GFW data must:

1. Carry the attribution line below
2. Confirm the use is non-commercial, or obtain a commercial license before use
3. Not pass GFW data to downstream users under terms that strip the NC restriction

---

## Attribution Standard

Every OIS output, BLC artifact, or published content that incorporates GFW data carries:

```
Fishing effort data: Global Fishing Watch (globalfishingwatch.org) · CC-BY-NC 4.0
```

---

*Built on SIP · Blue Life Commons (CC-BY-4.0)*
