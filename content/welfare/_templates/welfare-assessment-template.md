---
id: welfare-assessment-species-or-region
type: welfare-assessment
title: "Welfare Assessment: <Species or Place>"
species_group:
  - cetaceans
species:
  - scientific-name-slug
region:
  - region-slug
status: needs-expert-review
welfare:
  state: pressured            # favourable | pressured | critical | recovering | unknown
  dominant_stressor: vessel-noise
  confidence: modeled          # measured | modeled | expert-opinion
  five_domains:
    nutrition: "<prey availability/quality note, cited>"
    environment: "<habitat/thermal/noise/disturbance note, cited>"
    health: "<injury/disease/entanglement note, cited>"
    behaviour: "<foraging/resting/breeding interruption note, cited>"
    mental_state: "<inferred ONLY from cited physiological/behavioural correlates>"
consensus_state: contested
last_verified: "2026-06-16"
sources:
  - url: ""
    title: "<Tier 1 source — peer-reviewed / IUCN / government monitoring>"
    tier: 1
    accessed: "2026-06-16"
review:
  science: required
  ethics: required
  editor: pending
outputs:
  website_path: /welfare/<slug>
  github_path: content/welfare/<slug>.md
contributors:
  - github: your-handle
license: CC-BY-4.0
---

# Welfare Assessment: <Species or Place>

> Read [WELFARE.md](../../WELFARE.md) and [ETHICS.md](../../ETHICS.md) before writing. Center the animal's *interests*, not its *feelings*. Every welfare claim is cited and confidence-tagged.

## Summary

One paragraph: current welfare state, the dominant stressor, and the confidence basis. No anthropomorphism.

## Five Domains

For each domain, state the need, the current pressure, and the cited evidence. Mark mental-state inferences with their physiological/behavioural correlate and citation.

- **Nutrition** —
- **Environment** —
- **Health** —
- **Behaviour** —
- **Mental state (inferred)** —

## Cumulative pressure (disturbance budget)

Describe total human pressure on this population/place/season — not just single-actor compliance. If a `disturbance_budget` can be estimated, state it and its utilization.

## What supports recovery

Cited, concrete interventions that would move the welfare state toward `favourable`/`recovering`. No advocacy beyond the evidence.

## Sources

- <Tier 1–2 citations with DOIs and access dates>
