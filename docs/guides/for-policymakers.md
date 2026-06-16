# For Policymakers & Marine Managers

You make decisions that move populations — protected-area boundaries, vessel rules, fishery limits, stranding response capacity. You need evidence assembled to a citable standard, honest about uncertainty, and clear about cumulative pressure. The commons assembles exactly that — and is deliberately built to stop short of handing you a verdict.

## What the system gives you

- **Region briefings** — place-scoped, source-cited overviews of what lives in a managed area, what's protected, and what's under pressure (Monterey Bay, Ningaloo Coast, Wadden Sea today; see [`CATALOG.md`](../../CATALOG.md)).
- **Welfare assessments** — a queryable welfare state per species or place (`favourable | pressured | critical | recovering | unknown`), a named `dominant_stressor`, the Five Domains, and a `confidence` tag (`measured | modeled | expert-opinion`). See the four live assessments in `content/welfare/` (right whale, Hawaiian monk seal, southern resident orca, vaquita).
- **The disturbance-budget frame** — the cumulative-pressure model your single-actor rules can't capture. Welfare is *additive*: the science is Population Consequences of Disturbance (PCoD). A `disturbance_budget` represents a place/season's carrying capacity for human pressure, so you can manage *utilization*, not just per-actor compliance ([`WELFARE.md`](../../WELFARE.md)).
- **An impact ledger** — merged artifacts carry an `impact.claim`, giving a credible, contributor-credited record for accountability and reporting.
- **Governance grounding** — research summaries like *Ocean Governance Frameworks in 2026* (Ocean Decade, SDG 14, 30x30, High Seas Treaty) connect local evidence to the frameworks you work within.

## How to use it today

1. **Pull the region briefing for your managed area** — read it as a cited baseline of species, protections, and pressures.
2. **Read the relevant welfare assessment** — note the `state`, the `dominant_stressor`, and crucially the `confidence` tag. A `modeled` or `expert-opinion` confidence tells you where the evidence is strong and where it's judgment.
3. **Apply the disturbance budget to a cumulative-pressure question** — when a single-vessel rule clearly isn't protecting a haul-out or foraging ground, the `disturbance_budget` frame is the tool: manage total utilization across all actors, per season.
4. **Trace every figure to its source** — every claim links to a Tier 1–2 authority (IUCN, government monitoring, peer-reviewed) with an access date ([`SOURCES.md`](../../SOURCES.md)). Use the `iucn.assessment_date` to confirm a status isn't stale.
5. **Note what's contested** — `consensus_state: contested | emerging` artifacts represent the disagreement rather than flattening it. That's where to commission review, not assume settled fact.

## The rules that apply to you

- **The system assembles evidence; it never adjudicates.** It compiles evidence against published criteria and stays silent on the verdict — dosing, euthanasia, releasability, and legal determinations remain decisions for licensed authorities ([`ETHICS.md`](../../ETHICS.md)). *Grounded or silent extends to evidence, never verdict.*
- **Confidence is always tagged.** Most stressor→population links are `modeled` or `expert-opinion`; the artifacts say so. Don't read a modeled inference as a measurement.
- **Welfare claims are cited, not emotive** — energetic budgets, vital rates, disturbance thresholds, recovery trajectories — never "the animals are frightened" ([`WELFARE.md`](../../WELFARE.md)).
- **No precise locations of vulnerable populations** in published artifacts — regional granularity protects the very populations you're managing.
- **`approved` ≠ `still true`.** The `last_verified` field exists because an approved claim can go stale; check it before relying on a figure.

## Your first contribution

**Commission or request a welfare assessment for a population in your jurisdiction.** It produces exactly the artifact you need for a defensible decision: a cited welfare state, a named dominant stressor, the Five Domains, and an honest confidence tag — plus a disturbance-budget frame for cumulative pressure. Open an `artifact-request` issue in [`.github/ISSUE_TEMPLATE/`](../../.github/ISSUE_TEMPLATE/), or have your team author it from the `welfare-assessment` template; it ships only after science and ethics review.

> Built on SIP · Blue Life Commons (CC-BY-4.0).
