# For Journalists & Creators

You need ocean facts you can publish without getting burned — claims that trace to real authorities, statuses that are current, and an honest line between what's settled and what's contested. The commons is a trust substrate built on exactly that discipline: grounded or silent.

## What the system gives you

- **A grounded source of truth** — every claim a species page, region briefing, or guardian surfaces traces back to a reviewed artifact and a Tier 1–2 citation (IUCN, government monitoring, peer-reviewed). No invented facts, no anthropomorphic "what the whale is saying."
- **Dated, honest conservation status** — the green turtle page is the model: a 2025 IUCN downlisting framed *correctly* — "this is not 'recovered everywhere'," with some subpopulations still threatened and the species still on CITES Appendix I. That's the nuance a careful story needs ([`content/species/turtles/green-turtle.md`](../../content/species/turtles/green-turtle.md)).
- **A settled-vs-contested signal** — `consensus_state: settled | contested | emerging` tells you which claims have scientific consensus and which are live debates you should represent as such.
- **`marine-mcp` for fact-checking on the fly** — ask an AI assistant a grounded question and get sources back, or a typed refusal when a page isn't review-approved. The refusal is a green flag, not a failure: it means the system won't hand you unreviewed prose as fact.

## How to use it today

1. **Start at the catalog** — [`CATALOG.md`](../../CATALOG.md) is the index of every published artifact. Find the species, region, or research summary your story touches.
2. **Read the artifact and follow the citations** — every figure links to its authority with an access date. Quote the source, not the summary, and report figures *as the cited authority states them* ([`SOURCES.md`](../../SOURCES.md)).
3. **Check the status and the date** — note whether the artifact is `needs-expert-review` vs `published`, and read `iucn.assessment_date` so you don't present a years-old status as current. `approved` ≠ `still true` — check `last_verified`.
4. **Represent the disagreement** — if `consensus_state` is `contested` or `emerging`, your story should reflect the debate, not flatten it into false certainty.
5. **Fact-check with `marine-mcp`** (optional) — install it (see [GETTING-STARTED.md](GETTING-STARTED.md)) and have your assistant pull `get_species_details`; the `{ data, sources, status, attribution }` envelope gives you the citation trail directly.

## The rules that apply to you

- **Cite to the authority, not the commons summary** — the commons points you to Tier 1–2 sources; quote those. Forums, AI output, and uncited blogs are never sources ([`SOURCES.md`](../../SOURCES.md)).
- **No anthropomorphism as fact** ([`ETHICS.md`](../../ETHICS.md)) — behavioral interpretation must be cited to published research, never "the whale is telling us…".
- **No precise locations of vulnerable animals** — don't publish exact nesting beaches, haul-outs, or aggregation sites, and watch the combination attack (coarse location + season + a landmark in an image can reconstruct a site). Protecting the animal beats the vivid detail.
- **Welfare-honest language** — center the animal's *interests* via cited proxies (energetic cost, vital rates), not narrated feelings ([`WELFARE.md`](../../WELFARE.md)).
- **Honesty about invasiveness** — if you cover tagging, rehab, or research handling, describe the welfare cost plainly; the commons never euphemizes it, and neither should the story.

## Your first contribution

**File a correction or a sourced addition.** If your reporting turns up a newer IUCN assessment, a fresh peer-reviewed finding, or a factual gap, that's a real contribution: open an `artifact-request` issue in [`.github/ISSUE_TEMPLATE/`](../../.github/ISSUE_TEMPLATE/) with the source, or — if you're comfortable — author the fix with [`marine-agent-skills`](https://github.com/frankxai/marine-agent-skills) `/source-verify` and `/open-artifact-pr`. Journalists are natural keepers of the `last_verified` discipline: you notice when the published story has moved on.

> Built on SIP · Blue Life Commons (CC-BY-4.0).
