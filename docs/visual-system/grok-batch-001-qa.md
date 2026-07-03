# Grok Batch 001 QA

Date: 2026-06-26

Output directory:

```text
C:\Users\frank\starlight\repos\_generated\media\blue-life-commons\2026-06-26-visual-system\batch-001\
```

Tool: Grok Imagine via `grok-build`, six `image_gen` calls.

Important tooling note: Grok rejected `4:5` and accepted `3:4`; future prompt metadata has been updated.

## Scorecard

| Prompt ID | Dimensions | Score | Decision | Notes |
|---|---:|---:|---|---|
| `blc-hero-commons-current-001` | 1280x720 | 23/30 | iterate | Strong field-station warmth and brand mood, but generated forms/notebooks contain pseudo-text. Needs edit/crop or stronger blank-surface prompt. |
| `blc-guardian-reef-ningaloo-001` | 1280x720 | 27/30 | approve as draft source plate | Strong reef scene, no text, no unsafe interaction, good dashboard background potential. Abstract signal paths are acceptable as metaphor. |
| `blc-animal-whale-distance-001` | 1280x720 | 24/30 | iterate | Ethical distance is clear and warm. Notebook/hat details create possible pseudo-text/logo noise; crop or regenerate with blank notebook. |
| `blc-human-ngo-briefing-001` | 1152x864 | 19/30 | restart | Human warmth is good, but the image contains too much fake text, fake UI, and map-like detail. Not publication-ready. |
| `blc-education-turtle-001` | 864x1152 | 26/30 | approve as draft source plate | Strong poster background with negative space and no human interaction. Use only as mood/background, not species-ID proof. |
| `blc-provenance-ledger-001` | 1024x1024 | 26/30 | approve as draft source plate | Strong provenance still life. Minor scribble risk on tag/book surfaces; acceptable for draft, safer after crop/blur. |

## Critic Notes

Strongest element: Grok can produce warm, humane, non-hype ocean scenes that fit the Blue Life Commons emotional direction.

Weakest element: "No text" was not enough. The model still created pseudo-writing on paper, maps, notebooks, and screens.

Prompt fix applied:

```text
For notebooks, forms, cards, laptops, dashboards, posters, or maps: blank surfaces only. No writing, no pseudo-text, no scribbles, no fake interface glyphs.
```

## Next Batch Direction

- Generate fewer paper/screen surfaces unless exact overlays are planned.
- Favor clean negative space and blank physical surfaces.
- Use backgrounds with no maps or forms when factual precision matters.
- Keep exact labels in SVG/code after generation.
- For human workflow scenes, avoid screens and documents unless they are visibly blank.
