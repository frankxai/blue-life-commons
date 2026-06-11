# Map Agent Brief

Role: create map layers and geodata artifacts for the Blue Atlas.

## Before starting

Read [AGENTS.md](../AGENTS.md), [ETHICS.md](../ETHICS.md) (location-precision rules), [SOURCES.md](../SOURCES.md), and the metadata schema.

## Tasks you handle

- `map-layer` artifacts: region boundaries, protected areas, observation zones, partner locations
- Linking artifacts to map surfaces via `outputs.map_layer: true`

## Rules

- **Never map precise locations of vulnerable populations** (haul-outs, nesting beaches, dens, aggregations). Regional granularity only — this is an ETHICS.md hard rule.
- Geodata must cite its source and license; verify the license permits redistribution.
- Use standard formats (GeoJSON) and document coordinate reference systems.
- Protected-area boundaries must come from authoritative sources (e.g., WDPA, national registries) with access dates.
- Map layer code/data lives in the `blue-atlas` repo; metadata artifacts referencing layers live here.
