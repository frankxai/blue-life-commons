# Core Brand Generation Batch — 2026-06-26 (Grok Imagine)

This file archives the exact prompts used for the first production-grade visual generation pass for Blue Life Commons.

All prompts follow:
- Hero.svg palette lock (#041014, #4FD1C5, #38BDF8, #F5B84B)
- Warm hopeful lighting emphasis (golden rays, life-affirming)
- Professional + serene + nourishing mood
- Imagine skill structure (subject, setting, style, composition, lighting, palette, quality)
- Grounding from repo content where relevant
- Experiment notes on text/structure

## 01 — Logo Icon / Monogram
Prompt:
"Premium minimalist logo icon for Blue Life Commons, an open Ocean Intelligence commons. Clean elegant monogram fusing a gentle stylized whale fluke with a flowing wave element and subtle open source or compass rose suggestion for knowledge and navigation. Vector art quality, balanced modern proportions, refined details. No text whatsoever. Deep transparent or navy background. Primary color #4FD1C5 teal for main lines and fills, subtle warm accent highlights in #F5B84B gold. Professional serene branding, highly scalable, perfect for favicon and small reproduction. Centered, generous negative space, studio quality."

Aspect: 1:1
Result: images/1.jpg → brand/visuals/blc-logo-icon-01.jpg
Experiment: Pure icon focus to avoid text issues. Good for monogram base.

## 02 — Brand Palette Specimen
Prompt:
"Beautiful premium brand palette specimen card for Blue Life Commons. Elegant layout on deep navy background. Large title "Blue Life Commons Palette". Six labeled color swatches in a clean row or grid with exact hex values and names: Abyss #041014, Midnight Current #06202A, Deep Teal #083241, Teal Current #4FD1C5 (primary), Sky Light #38BDF8, Sunbreak Gold #F5B84B (warm hope). Subtle ocean wave or light ray motif integrated. Clean modern typography, high contrast, professional design asset. Generous space, inspiring and clear."

Aspect: 16:9
Result: → blc-palette-specimen-01.jpg
Note: Text labels — experiment for legibility.

## 03 — Horizontal Logo Lockup (text test)
Prompt: (see detailed in file)

Aspect: 16:9 (adjusted from failed 3:1)
Result: → blc-logo-lockup-horizontal-01.jpg
Experiment: Full text + icon. Will QA text rendering.

## 04 — Vertical Lockup
Prompt: (detailed above)
Aspect: 3:4
Result: → blc-logo-lockup-vertical-01.jpg

## 05 — Hero Banner Extension
Prompt: "Extended premium hero banner visual for Blue Life Commons. Deep oceanic dark teal to navy gradient background with subtle elegant grid lines. Large elegant typography treatment of "Blue Life Commons" and "Ocean Intelligence Commons" integrated beautifully. Warm golden light rays and gentle surface highlights. Abstract flowing current and soft marine life silhouettes (distant whale suggestion, wave forms) without being literal. Clean, inspiring, professional, matches the existing SVG hero language exactly in mood and palette (#4FD1C5 teal, #38BDF8 sky, #F5B84B gold). Wide cinematic composition with room for UI overlays."
Aspect: 16:9
Result: → blc-hero-banner-01.jpg

## 06 — Blue Whale Key Art (grounded)
Grounding: read content/species/cetaceans/blue-whale.md (IUCN EN, recovering, vessel strike primary, pleats, flukes, size).
Prompt: detailed cinematic description with palette lock + warm rays + respectful framing.
Aspect: 16:9
Result: → blc-keyart-blue-whale-01.jpg

## 07 — Brain Coral Key Art
Grounding: brain-coral.md + reefs.
Prompt: intricate grooves, vibrant healthy, warm light.
Result: → blc-keyart-brain-coral-01.jpg

## 08 — Citizen Scientist Ethical Scene
Prompt: kayak observer, distant whale, golden hour, notebook, respectful distance.
Result: → blc-scene-citizen-observer-01.jpg
Strong warmth/hope test.

## 09 — Pattern Tile
Prompt: subtle hero grid + wave, low opacity teal on navy, seamless.
Result: → blc-pattern-grid-01.jpg

## 10 — Workflow Infographic (text + structure experiment)
Prompt: four steps, connected, large legible text, palette, clean modern infographic.
Aspect: 16:9
Result: → blc-infographic-workflow-01.jpg
Note: Primary text test case. Likely will need code fallback or Codex refinement for perfect labels.

## Learnings / Adjustments So Far (to prove iteration)
- Locked every prompt to exact hero hex + "warm golden light / sunbreak gold for hope".
- Read actual md for species accuracy before prompting.
- Separated icon-only from text lockups.
- Used valid aspect ratios only.
- Created strong handover prompts in parallel for text-heavy.
- Will run image_edit on promising ones if needed for refinements.
- All prompts are full descriptive prose (not tag lists).

Next batch: more species (orca, whale shark, turtles), region (GBR), ethics infographic, more experiments on text size/placement.
