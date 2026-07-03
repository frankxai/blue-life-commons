# Blue Life Commons — Visual Assets Registry

Living record of all generated and curated visual assets. Every entry includes prompt, metadata, QA, and grounding.

**Schema for each asset:**
- **slug**: kebab filename
- **category**: core-brand | key-art | infographic | inspirational | pattern | other
- **title**: human name
- **use_cases**: comma list (hero, species-page, social-1x1, favicon, academy-cover, etc.)
- **aspect**: 1:1 | 16:9 | 9:16 | 4:3 | 3:4 | auto
- **prompt**: FULL verbatim prompt used for generation (or reference to batch file)
- **generated**: date + tool (grok-image_gen | edit | other)
- **file**: relative path in repo (brand/visuals/...)
- **variants**: notes on alternates
- **qa**: bullet observations (composition, warmth/hope, accuracy/grounding, text legibility if any, palette fidelity, ethics, issues) — to be filled after inspection
- **verdict**: approved | needs-edit | concept-only | fallback-to-code
- **grounding**: links to species/region md or facts used
- **notes**: next actions, handover prompt id, etc.

---

## 2026-06-26 First Production Batch (Grok Imagine)

### blc-logo-icon-01
- **category**: core-brand
- **title**: Logo Icon / Monogram Concept 01
- **use_cases**: favicon, avatar, monogram lockups, merch, UI
- **aspect**: 1:1
- **prompt**: see brand/prompts/core-brand-batch-2026-06-26.md
- **generated**: 2026-06-26 grok-image_gen
- **file**: brand/visuals/blc-logo-icon-01.jpg
- **qa**: (pending visual inspection + edit loop)
- **verdict**: concept
- **grounding**: hero.svg icon language + fluke/wave motif
- **notes**: Pure icon to sidestep text issues. Strong candidate for tracing to SVG master.

### blc-palette-specimen-01
- **category**: core-brand
- **title**: Official Palette Specimen Card
- **use_cases**: brand guidelines, docs, onboarding, design system page
- **aspect**: 16:9
- **prompt**: see batch file
- **generated**: 2026-06-26 grok-image_gen
- **file**: brand/visuals/blc-palette-specimen-01.jpg
- **qa**:
- **verdict**:
- **grounding**: exact hex from hero.svg + extended life accents
- **notes**: Includes text labels — test legibility.

### blc-logo-lockup-horizontal-01
- **category**: core-brand
- **title**: Horizontal Wordmark + Icon Lockup
- **use_cases**: website header, hero, email, print
- **aspect**: 16:9
- **prompt**: see batch file
- **generated**: 2026-06-26 grok-image_gen
- **file**: brand/visuals/blc-logo-lockup-horizontal-01.jpg
- **qa**:
- **verdict**:
- **grounding**: hero + brand guidelines
- **notes**: Primary text test. May refine with edit or hand to Codex.

### blc-logo-lockup-vertical-01
- **category**: core-brand
- **title**: Vertical Stacked Lockup
- **use_cases**: tall headers, mobile, cards, presentations
- **aspect**: 3:4
- **prompt**: see batch file
- **generated**: 2026-06-26 grok-image_gen
- **file**: brand/visuals/blc-logo-lockup-vertical-01.jpg
- **qa**:
- **verdict**:
- **grounding**:
- **notes**:

### blc-hero-banner-01
- **category**: core-brand
- **title**: Extended Hero Banner
- **use_cases**: landing page hero, social cover, slide background
- **aspect**: 16:9
- **prompt**: see batch file (explicitly matches existing hero.svg)
- **generated**: 2026-06-26 grok-image_gen
- **file**: brand/visuals/blc-hero-banner-01.jpg
- **qa**:
- **verdict**:
- **grounding**: .github/hero.svg structure and palette
- **notes**: Typography treatment in image — experiment.

### blc-keyart-blue-whale-01
- **category**: key-art
- **title**: Blue Whale Signature Portrait
- **use_cases**: species page header (cetaceans), region pages, academy, social
- **aspect**: 16:9
- **prompt**: see batch file
- **generated**: 2026-06-26 grok-image_gen
- **file**: brand/visuals/blc-keyart-blue-whale-01.jpg
- **qa**:
- **verdict**:
- **grounding**: content/species/cetaceans/blue-whale.md (IUCN EN, vessel strike, pleats, flukes, recovering trend)
- **notes**: Grounded + warm light priority.

### blc-keyart-brain-coral-01
- **category**: key-art
- **title**: Grooved Brain Coral Healthy Reef Portrait
- **use_cases**: reefs species, GBR region, coral education
- **aspect**: 16:9
- **prompt**: see batch file
- **generated**: 2026-06-26 grok-image_gen
- **file**: brand/visuals/blc-keyart-brain-coral-01.jpg
- **qa**:
- **verdict**:
- **grounding**: content/species/reefs/brain-coral.md + reefs
- **notes**:

### blc-scene-citizen-observer-01
- **category**: inspirational | key-art
- **title**: Ethical Citizen Scientist Observation (Kayak + Humpback)
- **use_cases**: missions, guides for citizen scientists, landing, "nourish" campaign
- **aspect**: 16:9
- **prompt**: see batch file
- **generated**: 2026-06-26 grok-image_gen
- **file**: brand/visuals/blc-scene-citizen-observer-01.jpg
- **qa**:
- **verdict**:
- **grounding**: missions templates + ethics.md (respectful distance)
- **notes**: Strong warmth / agency / hope test case.

### blc-pattern-grid-01
- **category**: pattern
- **title**: Hero Grid + Wave Subtle Pattern Tile
- **use_cases**: website bg, slide masters, overlays, packaging
- **aspect**: 1:1 (tile)
- **prompt**: see batch file
- **generated**: 2026-06-26 grok-image_gen
- **file**: brand/visuals/blc-pattern-grid-01.jpg
- **qa**:
- **verdict**:
- **grounding**: hero.svg grid lines
- **notes**: Seamless tile.

### blc-infographic-workflow-01
- **category**: infographic
- **title**: Contribution Workflow Infographic (4 Steps)
- **use_cases**: docs, contributing page, academy, onboarding, github readme visuals
- **aspect**: 16:9
- **prompt**: see batch file
- **generated**: 2026-06-26 grok-image_gen
- **file**: brand/visuals/blc-infographic-workflow-01.jpg
- **qa**: (critical text legibility check)
- **verdict**:
- **grounding**: README.md + CONTRIBUTING.md flywheel
- **notes**: Text-heavy experiment. Prepare code fallback + Codex handover prompt.

---

## Usage Notes
- Copy approved masters to final production locations as needed.
- For every new generation append using the schema.
- After inspection, use image_edit for refinements where composition or color is close but not perfect.
- Link new entries to brand/prompts/ files.
- Species primary images and rich embeds are tracked separately in `content/media/species-media-registry.yaml`; generated assets listed here may support species pages but are not official species media unless the registry approves them.

**Batch total this run:** 15 assets (plus ready prompts for expansion to 40+). Strong foundation of core branding, 7+ key art portraits/scenes, 2 infographics, patterns.

Additional entries from final batch (see prompts file for full text):
- blc-keyart-whale-shark-ningaloo-01 (16:9) — Ningaloo / whale shark key art, grounded, warm light.
- blc-keyart-gbr-region-01 (16:9) — Great Barrier Reef region hero, vibrant life + warm rays.

Infographics delivered: workflow (horizontal), ethics principles (vertical 9:16). Text experiments logged — recommend code render or Codex/Antigravity pass for production labels.

### blc-keyart-orca-01
- **category**: key-art
- **title**: Orca Signature Portrait
- **use_cases**: cetaceans species, Salish Sea / orca welfare, social
- **aspect**: 16:9
- **prompt**: see batch prompts file
- **generated**: 2026-06-26 grok-image_gen
- **file**: brand/visuals/blc-keyart-orca-01.jpg
- **grounding**: content/species/cetaceans/orca.md (family structure, intelligence)
- **verdict**: concept
- **notes**: Pod + warm light, family/nourish theme.

### blc-keyart-green-turtle-01
- **category**: key-art
- **title**: Green Turtle Over Coral
- **use_cases**: turtles species, GBR / Ningaloo, reef education
- **aspect**: 16:9
- **prompt**: see batch
- **generated**: 2026-06-26 grok-image_gen
- **file**: brand/visuals/blc-keyart-green-turtle-01.jpg
- **grounding**: content/species/turtles/green-turtle.md + reefs
- **verdict**:
- **notes**:

### blc-infographic-ethics-01
- **category**: infographic
- **title**: Ethical Marine Observation Principles (vertical)
- **use_cases**: missions, field guides, social stories 9:16, academy
- **aspect**: 9:16
- **prompt**: see batch (text heavy)
- **generated**: 2026-06-26 grok-image_gen
- **file**: brand/visuals/blc-infographic-ethics-01.jpg
- **grounding**: ETHICS.md + missions
- **verdict**: concept / likely needs code or Codex pass for final labels
- **notes**: Strong vertical format experiment.
