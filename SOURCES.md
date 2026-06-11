# SOURCES.md — Citation Standards

Blue Life Commons is a trust substrate. That trust depends on one rule:

> **Every factual claim needs a source.**

## What requires a citation

- Species facts: distribution, diet, behavior, lifespan, population
- Conservation status and threats (cite IUCN Red List or equivalent authority)
- Legal protections and regulations
- Scientific findings, statistics, and dataset descriptions
- Historical and ecological claims about regions
- Health/safety guidance for humans (e.g., jellyfish stings, currents)

## What does not require a citation

- First-person field observations clearly labeled as such ("On this trip we observed…")
- Editorial guidance about contribution workflow
- Mission logistics (meeting points, gear lists) — though regulations cited within them do

## Source quality tiers

| Tier | Examples | Use |
|---|---|---|
| 1 — Primary scientific | Peer-reviewed papers, IUCN assessments, government monitoring data | Preferred for all science claims |
| 2 — Institutional | NGO reports, museum/aquarium science pages, university outreach | Acceptable with attribution |
| 3 — Journalistic / educational | Reputable science journalism, documentaries | Context only; not for core claims |
| Not acceptable | Forums, AI output, uncited blogs, social media | Never as a source |

## Format

List sources in the artifact's metadata `sources` block **and** in a "Sources" section at the end of the document:

```yaml
sources:
  - url: "https://www.iucnredlist.org/species/..."
    title: "IUCN Red List: Harbor Seal"
    accessed: "2026-06-11"
```

- Use stable URLs (DOIs where available).
- Record the access date.
- If a claim cannot be sourced, remove the claim or mark the artifact `status: needs-sources`.

## Review

PRs are checked for source coverage during review. Reviewers may request Tier 1–2 sources for any claim. The `needs-sources` label flags artifacts blocked on citations.
