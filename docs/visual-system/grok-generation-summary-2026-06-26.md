# Grok Generation Summary

Date: 2026-06-26

Generated source-image library:

```text
C:\Users\frank\starlight\repos\_generated\media\blue-life-commons\2026-06-26-visual-system\
```

Contact sheets:

```text
C:\Users\frank\starlight\repos\_generated\visual-qa\blue-life-commons\grok-contact-sheets\
```

## Totals

| Batch | JPGs | Status |
|---|---:|---|
| `batch-001` | 6 | inspected individually |
| `batch-002` | 12 | inspected by contact sheet plus one individual manta check |
| `batch-003` | 12 | inspected by contact sheet |
| **Total** | **30** | draft source library created |

## QA Rollup

| Decision | Count | Meaning |
|---|---:|---|
| approve as draft source plate | 15 | Usable as background/mood plate after normal editorial review |
| iterate | 14 | Useful direction, but needs crop, edit, or regen before publication |
| restart | 1 | Do not use as publication source |

No generated image is treated as factual evidence, species-ID proof, map data, dashboard data, or safety guidance.

## Approved Draft Source Plates

- `batch-001/blc-guardian-reef-ningaloo-001.jpg`
- `batch-001/blc-education-turtle-001.jpg`
- `batch-001/blc-provenance-ledger-001.jpg`
- `batch-002/blc-animal-coral-close-011.jpg`
- `batch-002/blc-animal-dolphin-coastal-003.jpg`
- `batch-002/blc-animal-humpback-wide-002.jpg`
- `batch-002/blc-animal-kelp-forest-010.jpg`
- `batch-002/blc-animal-mangrove-nursery-012.jpg`
- `batch-002/blc-animal-manta-ray-009.jpg`
- `batch-002/blc-guardian-monterey-kelp-003.jpg`
- `batch-002/blc-guardian-salish-sound-004.jpg`
- `batch-003/blc-background-connector-spine-004.jpg`
- `batch-003/blc-background-five-domains-003.jpg`
- `batch-003/blc-hero-night-signals-005.jpg`
- `batch-003/blc-og-triad-001.jpg`

## Iterate

- `batch-001/blc-hero-commons-current-001.jpg` - good mood, pseudo-text on forms/notebook.
- `batch-001/blc-animal-whale-distance-001.jpg` - ethical distance, but notebook/hat details need crop or regen.
- `batch-002/blc-animal-seal-distance-004.jpg` - safe distance but foreground object/notebook still needs closer check.
- `batch-002/blc-guardian-antarctic-peninsula-006.jpg` - good mood, open book foreground risks pseudo-text.
- `batch-002/blc-guardian-azores-open-ocean-005.jpg` - usable direction, but reads more vessel/deck than community guardian.
- `batch-002/blc-guardian-wadden-bay-002.jpg` - good regional scene, foreground notebook risk.
- `batch-003/blc-background-disturbance-budget-002.jpg` - useful metaphor, but notebook surface risk.
- `batch-003/blc-hero-community-shore-006.jpg` - warm human scene, but too many papers for final use without crop/edit.
- `batch-003/blc-hero-public-library-002.jpg` - strong concept, but library shelves and desk surfaces need closer text check.
- `batch-003/blc-og-commons-library-002.jpg` - strong table scene, likely needs crop/blur for paper surfaces.
- `batch-003/blc-social-provenance-story-004.jpg` - promising vertical still life, paper surfaces need close inspection.
- `batch-003/blc-social-reef-story-002.jpg` - good reef crop, but central glow reads too synthetic.
- `batch-003/blc-social-student-story-003.jpg` - safe behavior and useful social crop, notebook surfaces need check.
- `batch-003/blc-social-whale-story-001.jpg` - ethical distance, but notebook foreground risks pseudo-text.

## Restart

- `batch-001/blc-human-ngo-briefing-001.jpg` - too much fake text, fake UI, and map-like detail.

## Prompt Lessons

1. `4:5` is not supported by Grok Image Gen; use `3:4` or `2:3`.
2. `1.91:1` is not supported directly; use `19.5:9` for Open Graph-like assets.
3. "No text" is weaker than needed. Use: "blank surfaces only, no writing, no pseudo-text, no scribbles, no fake interface glyphs."
4. Human workflow scenes should avoid screens, maps, forms, and documents unless those surfaces are intentionally blank and large enough to inspect.
5. Habitat and distant-animal prompts are much more reliable for this brand than paper/screen-heavy scenes.

## Next Iteration

- Regenerate the NGO/community/human workflow scenes with no screens and no documents.
- Use approved habitat plates as background layers for exact SVG infographics.
- Crop or blur approved draft plates before public use if any pseudo-text survives.
- Compose all captions, labels, claims, and CTAs outside the image model.
