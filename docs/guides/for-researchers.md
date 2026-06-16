# For Researchers & Academics

You study marine systems for a living. Your friction is rarely curiosity — it's that data dies on hard drives, Darwin Core mapping is manual and late, and the link between a claim and its evidence gets severed at publication. The Ocean Intelligence System is built to close those exact gaps.

## What the system gives you

- **A reviewed, queryable corpus** — species pages and region briefings with dated IUCN provenance, Tier 1–2 citations, and welfare state, served to your notebook or agent through [`marine-mcp`](https://github.com/frankxai/marine-mcp). Provenance rides through every response; the server returns a curated body *as fact only when it's review-approved*, and a typed refusal otherwise. You never get laundered, unsourced prose.
- **Dataset cards** — structured, cited descriptions of the data sources you already use (OBIS, GBIF, WoRMS, iNaturalist, NOAA Coral Reef Watch, Protected Planet). See the six live cards in [`CATALOG.md`](../../CATALOG.md) under *Dataset Cards*.
- **Live occurrence passthrough** — `obis_gbif_passthrough` returns live OBIS/GBIF occurrences, explicitly labelled `unreviewed: true` so external data is never confused with the reviewed corpus.
- **A contribute → DOI path** (specced) — the roadmap target that converts dead hard-drive data into citable knowledge with a version-pinned DOI, accessed-date, and license on every record (the provenance spine). See [`docs/WORKFLOWS.md`](../WORKFLOWS.md).

## How to use it today

1. **Install `marine-mcp`** against your local commons checkout (see [GETTING-STARTED.md](GETTING-STARTED.md) for the exact JSON). Restart Claude Desktop / Cursor.
2. **Query the corpus from your agent:** ask it to `search_species` for your taxon, then `get_species_details` or `get_region_briefing`. Read what comes back — and note whether you got a body or a `needs-expert-review` refusal. The refusal tells you exactly what still needs a reviewer.
3. **Pull live occurrences** via `obis_gbif_passthrough` and compare against the reviewed page — the labelled-unreviewed flag keeps your analysis honest.
4. **Author a dataset card** for a source the commons doesn't yet describe. Copy an existing card from `content/research/` (e.g. `dataset-obis.md`), fill the frontmatter per [`schema/artifact-schema.md`](../../schema/artifact-schema.md), record per-source `tier`, `license`, and `commercial_use_ok`, and cite the source's own documentation.
5. **Validate before you PR:** run `validate_artifact` via the MCP server, or `/validate-artifact` from [`marine-agent-skills`](https://github.com/frankxai/marine-agent-skills), to confirm schema compliance.

## The rules that apply to you

- **Tier 1 sources preferred** for every science claim — peer-reviewed papers, IUCN assessments, government monitoring data ([`SOURCES.md`](../../SOURCES.md)). Record DOIs and access dates.
- **Mark science-sensitive content `review.science: required`.** You don't decide scientific truth in the artifact — reviewers do. A species page reaching `approved` must carry `iucn.assessment_date` + `iucn.version` so a years-old assessment isn't presented as current.
- **Represent disagreement.** Use `consensus_state: contested | emerging` and describe the disagreement rather than flattening it.
- **`commercial_use_ok: false` sources** cannot underpin an artifact whose `impact.eligible_for_hypercert` is true.
- **Location sensitivity** ([`ETHICS.md`](../../ETHICS.md)): coarsen vulnerable-taxa coordinates by *rounding* to the `sensitivity.tier`, never jitter; check the combination attack (coarse coordinate + season + a landmark in attached media must not reconstruct an exact site).

## Your first contribution

Pick a dataset you query often that the commons doesn't yet describe, and **author a dataset card** for it. It's the highest-leverage, lowest-risk entry point — pure metadata, fully citable, and it immediately makes the source discoverable to every agent and researcher downstream. Open a `research-request` or `artifact-request` issue in [`.github/ISSUE_TEMPLATE/`](../../.github/ISSUE_TEMPLATE/), then open your PR.

> Built on SIP · Blue Life Commons (CC-BY-4.0).
