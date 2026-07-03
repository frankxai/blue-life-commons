# Blue Life Commons — Visual Strategy & Asset Plan (L99)

**Date:** 2026-06-26
**Scope:** Core branding, key art, infographics, educational visuals, inspirational assets for Blue Life Commons (Ocean Intelligence Commons) and companion Ocean Intelligence Systems.
**Owner:** Visual intelligence build with Grok Imagine + handover to Codex / Antigravity / Infogenius pipelines.
**Principles:** Source-led accuracy, ethics-first depiction, warm hopeful stewardship, premium professional quality, accessible to citizen scientists + researchers.

## 1. Context & Alignment

Blue Life Commons is the public-good layer of Starlight Marine Intelligence Systems:

- **Blue Life Commons** (this repo): open corpus of species pages, region briefings, field missions, datasets — CC-BY, review-gated.
- **Ocean Intelligence OS**: productized software, agents, dashboards, MCPs.
- **Starlight Marine Intelligence Systems**: business layer for reach and sustainability.

Visuals must:
- Nourish connection to the ocean and its animals.
- Make people feel capable, inspired, and warmly invited into observation + contribution.
- Educate accurately without guilt or hype (per STYLE.md).
- Signal "sources + ethics + public artifact" at a glance (echo hero.svg).
- Scale across web, print field guides, academy, social, maps, partner materials, presentations.

Current seed: `.github/hero.svg` (deep navy-teal gradient #041014→#083241, teal #4FD1C5, sky #38BDF8, gold #F5B84B, clean Inter-style typography, subtle grid + workflow cards).

## 2. Visual Brand Pillars (derived from mission + style)

1. **Reverent Wonder** — Majestic yet intimate. Animals as sovereign beings. Light as life-giver.
2. **Warm Hope & Agency** — Golden-hour surface light, bioluminescent accents, people actively documenting/observing responsibly. Recovery and action over tragedy.
3. **Precision with Warmth** — Scientific accuracy in form/behavior/habitat cues + human, approachable presentation. No sterile lab coldness.
4. **Commons Clarity** — Clean hierarchy, generous space, legible at all sizes. Subtle data or grid motifs from hero. "Source-led" visual language.
5. **Ethical Depiction** — Respectful distances, no harassment, licensed-feel or generated with care notes, citizen science in action.

**Mood keywords (for all prompts):** serene, hopeful, reverent, empowering, warm, professional, cinematic yet clean, nourishing.

**Forbidden (ethics + tone):** distress/dead animals, close harassment, tourist flash, blood, apocalyptic bleached reef without hopeful counter, cartoonish animals unless specified for kids academy, excessive text that will fail rendering.

## 3. Extended Palette (from hero + warm life accents)

**Deep Ocean Base**
- Abyss: #041014
- Midnight Current: #06202A
- Deep Teal: #083241

**Signature**
- Teal Current (primary): #4FD1C5
- Sky Light (secondary): #38BDF8
- Sunbreak Gold (warm hope): #F5B84B

**Light / Text**
- Foam White: #F2FBFF
- Mist Blue: #A9D7E2

**Life Accents (subtle, use sparingly for coral, life, hope)**
- Warm Coral: #E07A5F (sunlit coral, life)
- Kelp Green: #2E8B57 (healthy vegetation)

**Usage rules:** 80% deep base + primary teal for authority/trust. Gold for call-to-action, hero highlights, "good news" elements. Always test on dark (hero is dark) + light surfaces.

Tokens will live in `brand/tokens/brand-tokens.css`.

## 4. Logo System Principles

- Master: wordmark "Blue Life Commons" + optional tag "Ocean Intelligence Commons".
- Icon/monogram: distilled essence (fluke + wave, or open source leaf + current, or elegant whale silhouette + compass minimal).
- Lockups: horizontal (primary), vertical (stacked), icon-only (fav, avatar, tight UI).
- Variants: full color, teal-on-transparent, gold accent, monochrome (white/black), reversed on dark/light.
- Rules: minimum clear space, no distortion, never stretch, work small (16px favicon ok).

Grok will generate high-fidelity raster masters and concepts; final production SVGs can be traced or manually refined from strong concepts.

## 5. Asset Categories & Backlog (prioritized)

### Tier 0 — Core Branding (do first, foundational)
- Logo suite (icon, wordmark lockups, variants) — 6-8 images
- Brand palette cards / swatch hero
- Typography specimen + usage (with ocean motif)
- Pattern set (subtle bathymetric lines, wave, plankton grid, hero extension)
- Primary hero / landing banner extensions (multiple crops/aspects)
- Favicon + social avatar set
- "Sources • Ethics • Public" badge lockup (visual language)

### Tier 1 — Key Art & Species Portraits (inspire + educate)
One signature per major guild + flagship species:
- Blue Whale
- Humpback Whale
- Orca
- Whale Shark
- Great White (respectful, powerful, not fear)
- Green Turtle / Leatherback
- Hawaiian Monk Seal or Harbor Seal
- Brain / Staghorn Coral reef scene (healthy vibrant)
- Region heroes: Great Barrier Reef, Ningaloo, Galapagos, Antarctic Peninsula, Monterey Bay
- Citizen scientist / field moment (kayak notebook, diver logging, ethical whale shark boat)

~15–20 images

### Tier 2 — Infographics & Educational (accuracy critical)
- Contribution workflow (visual evolution of hero.svg cards)
- Ethical observation guidelines (distance rules, boat protocols, 5 domains hint)
- IUCN status + population trend cards (beautiful, not alarming)
- "Anatomy & Field ID" for 3-4 key species (minimal clean labels)
- Region biodiversity comparison or priority map artistic
- "From Curiosity to Artifact" journey
- Dataset value visual (what OBIS/GBIF/iNat give the commons)
- "Warmth of Knowledge" — how observation nourishes protection

~8–12 (text-heavy → careful prompts + code/HTML fallback recommended)

### Tier 3 — Inspirational / Campaign / Social
- "Nourish the Oceans" hero scenes (hands + reef restoration metaphor, light rays, schools of fish)
- Quote cards with powerful facts (text minimal or avoided)
- Academy lesson covers
- Partner co-brand templates
- Social story / post templates (9:16, 1:1, 16:9)

~10

**Total target first pass:** 40+ high-quality assets.

## 6. Generation & Documentation Protocol (this run)

**Tooling:**
- Primary: Grok `image_gen` (this harness) for mood, key art, branding concepts.
- Refinement: `image_edit` loops.
- Text/precision-critical: generate concepts here, then hand over polished prompts to Codex (strong text), Antigravity/NanoBanana (grounded infogenius per acos-visual-gen), or Higgsfield.
- Grounding: always read actual species/region md files first for facts (size, behavior, IUCN, stressors, beauty notes).
- Prompt structure (per imagine skill + infogenius learnings):
  1. Subject + key accurate descriptors.
  2. Action/pose/mood (serene, hopeful).
  3. Setting + lighting (warm golden surface rays, deep blue, biolum accents).
  4. Style: "premium cinematic nature photography in the spirit of Blue Planet / National Geographic, high detail, photoreal or refined scientific illustration hybrid, clean composition".
  5. Composition: rule of thirds, generous negative space for overlays, aspect-matched.
  6. Color lock: "using Blue Life Commons palette — deep #041014 base, teal #4FD1C5 accents, warm gold #F5B84B highlights".
  7. Quality: "professional, no artifacts, sharp focus where needed, emotionally resonant".
  8. For logos/infographics: "clean vector-influenced design, elegant modern typography, high legibility for any text elements, integrated not overlaid".

**Metadata per asset (in registry + per prompt file):**
- slug / filename
- category / use cases
- full prompt used
- aspect_ratio
- generation timestamp / model note
- variants tried
- QA observations (composition, emotion/warmth, accuracy, text legibility if any, ethics pass, palette fidelity)
- recommended crops / next steps (edit or code)
- source grounding links (species md)

**Registry:** `VISUAL-ASSETS-REGISTRY.md` (living table + per-asset sections).

**Prompts archive:** `brand/prompts/` or root `PROMPTS-LIBRARY.md` with full text + metadata.

**Handover pack:** `HANDOVER-PROMPTS.md` — ready-to-paste for Codex/Antigravity with model-specific tips (e.g. "enable grounding", "use vector style", "high thinking for text").

**Experiments run in this session:**
- Prompt length vs. control.
- Explicit "text perfectly legible" vs. integrated design elements.
- Warm lighting variations (golden hour vs. cool).
- Base image + edit for series consistency (e.g. same reef scene different light).
- Logo text vs. icon-only focus.
- Aspect experimentation for different deliverables.

**Post-gen QA loop:** Generate → inspect (via tool read if available or description) → note issues → targeted image_edit or new prompt → document verdict.

## 7. Success Criteria (L99 / premium)

- Warmth score: viewer feels "I want to protect this and I can contribute".
- Accuracy: species recognizable by experts + inspiring to beginners.
- Text: where present, 95%+ legible on first or second pass (or fallback to code render).
- Consistency: all assets feel part of one system (palette lock, lighting language, respectful framing).
- Usability: works on dark hero, light backgrounds, small favicons, large posters.
- Documentation: every asset traceable to prompt + fact source.
- Ethical: zero images that could encourage bad wildlife behavior.

## 8. Phased Execution (this task)

Phase 1 (complete 2026-06-26): Audit complete. Brand system defined in BRAND-GUIDELINES + tokens. Sophisticated plan + full docs + HANDOVER prompts created. 15 high-quality assets generated via Grok Imagine (core logos/palette/hero/pattern + key art for blue whale, brain coral, orca, green turtle, whale shark, citizen scene, GBR, Ningaloo + 2 infographics). All prompts archived with grounding, experiments run on text vs icon, warm light, palette lock, grounded facts. Assets copied to brand/visuals/. Registry populated. Ready for inspection, edit loops, Codex/Antigravity handoff for text precision, and Phase 2 expansion.

Phase 2: Tier 1 key art (species + regions).

Phase 3: Tier 2 infographics + educational (with experiment notes + handovers).

Phase 4: Tier 3 + polish, consistency edits, final registry + handover docs.

Phase 5: (future) Wire into website/academy, generate companion OS visuals, print assets, motion if needed.

## 9. Companion Systems Note

Ocean Intelligence OS and Starlight Marine layer should inherit the same visual language (shared tokens, logo usage, imagery library). Create a thin "marine-visual-tokens" package or symlink later. For now, all assets live here as the source commons.

## 10. References & Best Practices Incorporated

- Existing hero.svg palette + workflow visual language.
- STYLE.md voice (warm, practical, no hype).
- imagine skill: prompt order, code-for-text rule, reference-first, verification loop, aspect matching.
- arcanea-infogenius + acos-visual-gen: research-ground first, style systems (standard/photoreal/minimalist), audience levels, fact inclusion, Gate-like frequency (here: "Flow + Foundation + Heart" for ocean).
- Agentic Income brand structure (folders, tokens, foundation review page, monogram+wordmark).
- General premium: constrained descriptive prose, positive direction, post-gen QA, metadata everywhere.

**Next immediate actions:** Create supporting MDs (BRAND-GUIDELINES, REGISTRY, HANDOVER), generate Tier 0 with experiments, log everything.

---

*This plan is the source of truth. Update it as assets ship. Regenerate CATALOG or add visual section when ready.*
