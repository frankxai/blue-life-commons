# From Artifact to Guardian

Blue Life Commons is the knowledge layer. The public [`marine-mcp`](https://github.com/frankxai/marine-mcp) repository exposes reviewed commons records to compatible agents. An **Ocean Guardian** is the place-scoped delivery pattern described here; this repository does not present a separate guardian runtime as publicly available.

This is how a reviewed commons artifact becomes a guardian people can rely on.

## The path

```
Reviewed commons artifact (species page · region briefing · dataset card)
        │  grounds
        ▼
Ocean Guardian (place-scoped implementation)
        │  queries (read-only, provenance preserved)
        ▼
Real marine data via connectors (OBIS, Coral Reef Watch, Protected Planet, …)
        │  produces
        ▼
Briefings · alerts · dashboards for NGOs, researchers, creators, coastal residents
```

## Why the commons comes first

A guardian is only as trustworthy as its grounding. The required rule is **grounded or silent:** a guardian states a fact only if that fact traces to a reviewed commons artifact or a cited Tier 1–2 source. A responsible guardian implementation therefore begins with:

- a **region briefing** for that place,
- **species pages** for its flagship and indicator species, and
- **dataset cards** for the data the guardian will read.

That is why contributing to the commons prepares trustworthy guardian grounding. The page you write today can become the evidence spine of a later reviewed implementation.

## The ethics inheritance

Every guardian implementation must inherit this repository's [`ETHICS.md`](../ETHICS.md) as an upstream, non-waivable standard. It must never publish precise locations of vulnerable populations or generate wildlife-approach guidance dynamically; it may serve a reviewed observation guide instead. An implementation that cannot prove those boundaries is not ready for public reliance.

## What this means for you

| You are | Your path |
|---|---|
| A contributor | Write the species page or region briefing. It becomes guardian grounding. |
| An NGO | Your reviewed artifacts can ground a separately reviewed guardian implementation. |
| A developer | Publish an inspectable connector with tests and safeguards, then register its `dataset-card` here. |
| Someone who lives by the sea | Ask for a guardian for your water. The first step is grounding it — a briefing for your region. |

Knowledge here. Implementation must be inspectable before it is described as available. Ethics stays upstream of both.
