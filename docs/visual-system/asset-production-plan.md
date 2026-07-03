# Asset Production Plan

## Goal

Build a reusable, reviewable visual asset system for Blue Life Commons and the Ocean Intelligence System without weakening the repo's source, ethics, or review rules.

## Phase 1 - Identity Foundation

Produce and test:

- `blue-life-commons-mark.svg`
- `blue-life-commons-mark-one-color.svg`
- `blue-life-commons-lockup.svg`
- `ocean-intelligence-system-lockup.svg`
- favicon and social avatar exports derived from the one-color mark

QA:

- one-color works on light and dark backgrounds
- mark is legible at 16px and 32px
- lockups are readable at README and deck sizes
- no logo depends on glow, tiny details, or model-rendered depth

## Phase 2 - Exact Infographic Kit

Compose source-backed diagrams in SVG/code:

- artifact to guardian flow
- ocean intelligence triad
- connector provenance spine
- disturbance budget explainer
- Five Domains welfare explainer
- safe observation decision tree
- species-page metadata anatomy
- region-to-guardian readiness ladder

Rules:

- every exact claim references repo docs or artifact sources
- no generated text
- no exact sensitive locations
- no unsourced population, threat, or behavior claims

## Phase 3 - Grok Scene Library

Generate 40 draft source images from `grok-prompt-matrix.json`.

Priority order:

1. Brand and hero scenes
2. Guardian/place scenes
3. Animal education frames
4. Human workflow scenes
5. Background plates for exact infographics

Each generated file needs:

- absolute local path
- prompt ID
- tool used
- aspect ratio
- review status
- rights note
- QA note

## Phase 4 - Editorial Assembly

Turn approved source images into final surfaces:

- README hero alternate
- Open Graph image
- social 1:1 and 9:16 campaign frames
- deck section headers
- educator handouts
- dashboard background plates
- partner proposal visuals

Exact text and labels should be overlaid in SVG, Canva, Figma, or code after the generated background is approved.

## Phase 5 - Ocean Intelligence System Handoff

Because `ocean-intelligence-system` is not checked out locally, add a handoff package there when it is available:

- copy `ocean-intelligence-system-lockup.svg`
- add matching `docs/visual-system.md`
- add dashboard visual standards to `dashboards/README.md`
- add generated background plates for guardian dashboards
- keep all claims grounded in Blue Life Commons and connector provenance

Remote repo status checked on 2026-06-26:

- `frankxai/ocean-intelligence-system`
- private
- default branch `main`
- README confirms dashboard, guardian, connector, and provenance architecture

## Definition Of Done

- Docs and vector assets committed on a PR branch.
- Grok experiment outputs inspected.
- Evidence manifest validates.
- Approved generated images have metadata.
- Anything factual is composed as exact text from source-backed repo content.
