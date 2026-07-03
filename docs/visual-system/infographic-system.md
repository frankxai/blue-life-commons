# Infographic System

Blue Life Commons can use beautiful generated imagery, but factual infographics must be exact.

## Hard Rule

If a graphic contains educational text, numbers, maps, claims, workflow labels, source names, or safety guidance, compose it in Markdown, SVG, code, Figma, Canva, or Remotion. Do not ask an image model to render it.

## Recommended Pattern

1. Generate or select a background plate with no text.
2. Inspect the image for subject clarity, crop, and animal-safety issues.
3. Overlay exact labels and source-backed copy in SVG/code.
4. Attach metadata: source, prompt, date, reviewer, rights note.
5. Score with the visual QA gate.

## Initial Infographic Set

| ID | Surface | Data source |
|---|---|---|
| `blc-flow-001` | Artifact to guardian workflow | `README.md`, `docs/from-artifact-to-guardian.md`, Ocean Intelligence README |
| `blc-triad-001` | Trust, continuity, reach model | `README.md`, Ocean Intelligence README |
| `blc-provenance-001` | Provenance survives every hop | Ocean Intelligence `ARCHITECTURE.md` |
| `blc-disturbance-001` | Disturbance budget orientation | `WELFARE.md` |
| `blc-five-domains-001` | Five Domains explainer | `WELFARE.md` |
| `blc-safe-observation-001` | Safe observation decision tree | `ETHICS.md` |
| `blc-catalog-001` | 58-artifact catalog snapshot | `CATALOG.md` |
| `blc-guardian-readiness-001` | Region-to-guardian readiness ladder | `docs/from-artifact-to-guardian.md` |

## Copy Rules

- Keep labels short.
- Use common names before scientific names.
- Do not imply scientific certainty beyond source status.
- Use `needs-expert-review` status visibly where relevant.
- For animal welfare, speak in needs, pressures, and evidence. Do not narrate feelings as fact.

## Visual Rules

- Dark field background with high-contrast text.
- Teal for commons/source steps.
- Signal blue for connectors and guardians.
- Warm steward gold for review, public handoff, and human care.
- Use rounded cards only for actual repeated items, not decorative page sections.
- Keep diagrams readable at 1200px wide and on mobile crops.

## Metadata Block

Use this near each final infographic:

```yaml
id:
surface:
source_docs:
exact_claims:
generated_background:
prompt_id:
tool:
date:
review:
  science:
  ethics:
  editor:
rights:
qa_score:
publication_status:
```
