# Imagegen Batch 004 - 2026-06-26

This batch uses the built-in Codex `image_gen` tool, not Grok or the CLI fallback. It was generated as a focused comparison set after the Grok batches: warm ocean stewardship source plates with stricter constraints against fake text, pseudo-UI, logos, and unsafe animal interactions.

## Output paths

- Selected project assets: `assets/generated/imagegen/2026-06-26-batch-004/`
- Original Codex cache: `C:/Users/frank/.codex/generated_images/019f046a-b1a9-7932-a32b-70efd30b04f9/`
- Visual QA contact sheet: `C:/Users/frank/starlight/repos/_generated/visual-qa/blue-life-commons/imagegen-batch-004/contact-sheet.png`
- Machine-readable manifest: `docs/visual-system/imagegen-batch-004-results.json`

## QA summary

| Asset | Status | Score | Notes |
|---|---:|---:|---|
| `blc-imagegen-commons-current-hero-001.png` | approved draft | 28/30 | Warm, credible commons scene; no readable text visible. |
| `blc-imagegen-humpback-distance-001.png` | approved draft | 27/30 | Ethical vessel distance reads clearly; use as atmosphere, not species evidence. |
| `blc-imagegen-reef-nursery-001.png` | approved draft | 28/30 | Strong restoration source plate with distant diver and no touching. |
| `blc-imagegen-tidepool-learning-001.png` | approved draft | 27/30 | Humane education tone; keep factual overlays separate. |
| `blc-imagegen-ocean-intelligence-signals-001.png` | approved draft | 27/30 | Good abstract Ocean Intelligence background; no fake UI labels. |
| `blc-imagegen-kelp-otter-guardian-002.png` | approved draft | 27/30 | Revision fixed the otter identity problem from the first attempt. |
| `blc-imagegen-mangrove-nursery-001.png` | approved draft | 28/30 | Strong habitat plate with subtle community presence. |
| `blc-imagegen-manta-ray-001.png` | approved draft | 28/30 | Clean, spacious species empathy plate; anatomy reads plausible. |

Rejected experiment: the first kelp/otter attempt stayed in the Codex cache only because it read more like seals or sea lions than sea otters. The revised prompt explicitly added otter anatomy and `no seals, no sea lions`.

## Prompt lessons

- The built-in `image_gen` tool handled the no-text/no-pseudo-text constraint better than the prior paper-heavy Grok prompts.
- Habitat-first prompts are more reliable than dashboard, notebook, or screen-heavy prompts for this brand.
- Species-specific requests need concrete anatomy plus negative constraints, especially for otter/seal/sea-lion separation.
- Use generated images as emotional source plates. Add labels, diagrams, maps, species facts, and welfare guidance later in SVG/code from verified repo sources.

## Prompt set

### 001 commons current hero

```text
Use case: photorealistic-natural
Asset type: Blue Life Commons hero source plate, 16:9 website/banner image
Primary request: a warm, sophisticated ocean stewardship scene where a diverse small team stands at a coastal commons table after a shoreline survey, with ocean water and restored reef habitat visible beyond them
Scene/backdrop: early morning coastline, tide pools and calm blue-green water, modest field equipment arranged neatly on a plain table
Subject: people collaborating with care, hands arranging blank sample jars, a camera, and simple unmarked cards; no readable writing anywhere
Style/medium: photorealistic editorial conservation photography, premium but natural
Composition/framing: wide landscape composition, cinematic eye-level, subject group slightly off-center with usable open water and sky space
Lighting/mood: warm sunrise, hopeful, humane, quiet confidence, natural skin texture and realistic fabric
Color palette: ocean teal, sea-glass green, warm daylight, soft coral accents, neutral field gear
Constraints: no logos, no text, no pseudo-text, no letters, no numbers, no interface glyphs, no maps with labels, no watermark; all paper/card surfaces blank; realistic proportions; ethical non-extractive tone
```

### 002 humpback distance

```text
Use case: photorealistic-natural
Asset type: Blue Life Commons animal welfare source plate, 16:9 website/banner image
Primary request: a humpback whale seen respectfully from a distance, surfacing in open ocean with a small research vessel far in the background keeping ethical distance
Scene/backdrop: expansive open water, clear horizon, low sun, faint seabirds in the distance
Subject: whale back and tail fluke partially visible above water, no close contact, no touching, no chasing
Style/medium: photorealistic documentary ocean photography, natural lens compression, realistic sea texture
Composition/framing: wide landscape with generous negative space, whale in lower third, vessel tiny and distant for scale
Lighting/mood: calm, reverent, spacious, emotionally warm without melodrama
Color palette: deep ocean blue, turquoise highlights, pale gold sunlight, white foam
Constraints: no text, no logos, no watermark, no boats too close to the whale, no drones visible, no anthropomorphic expression, no fantasy scale, no plastic debris, scientifically plausible anatomy and behavior
```

### 003 reef nursery

```text
Use case: scientific-educational
Asset type: Blue Life Commons reef education source plate, 16:9 website/banner image
Primary request: a realistic, hopeful coral reef nursery scene showing healthy coral fragments growing on simple underwater frames, with a single diver observing from a respectful distance
Scene/backdrop: shallow tropical reef restoration site, clear water, sunlight caustics, living reef texture
Subject: coral nursery frames with diverse coral fragments, small reef fish, diver in background not touching anything
Style/medium: photorealistic underwater conservation photography, crisp but natural
Composition/framing: wide landscape, coral nursery as foreground subject, diver small in the middle distance, open blue water above for overlay space
Lighting/mood: warm, nourishing, optimistic, scientifically grounded
Color palette: turquoise water, living coral pink/orange/green accents, neutral metal or rope nursery structure
Constraints: no text, no labels, no pseudo-text, no logos, no watermark; no crowded fantasy reef; no diver touching coral; no damaged coral gore; plausible scale and reef ecology; avoid plastic-looking coral
```

### 004 tidepool learning

```text
Use case: photorealistic-natural
Asset type: Blue Life Commons education and citizen science source plate, vertical 3:4 social/portrait image
Primary request: a warm coastal learning moment with two teenagers and an elder mentor observing a tide pool from the rocks, using careful non-contact observation
Scene/backdrop: rocky intertidal shore at low tide, small anemones and seaweed visible, ocean softly blurred behind
Subject: students kneeling safely near the tide pool, mentor pointing just above the water without touching animals, simple blank field notebook closed beside them
Style/medium: photorealistic documentary education photography, natural and respectful
Composition/framing: portrait composition, human faces and tide pool both visible, intimate but not crowded
Lighting/mood: gentle afternoon light, wonder, patience, care, inclusive and grounded
Color palette: seaweed greens, slate rock, ocean blue, warm skin tones, muted field clothing
Constraints: no text, no readable writing, no pseudo-text, no logos, no watermark; notebook must be blank or closed; no animal handling; no collecting buckets; no staged classroom props; realistic intertidal organisms and safe body positions
```

### 005 ocean intelligence signals

```text
Use case: stylized-concept
Asset type: Ocean Intelligence Systems abstract background source plate, 16:9 website/slide image
Primary request: an elegant abstract visualization of ocean intelligence: underwater sensor buoys, soft light pathways, and ecological signal flows connecting reef, kelp, and open ocean habitats
Scene/backdrop: semi-realistic underwater-to-surface cross-section, not a literal map, no interface screen
Subject: subtle glowing signal threads moving through water between habitat forms and simple sensor silhouettes
Style/medium: premium cinematic scientific concept art, sophisticated, restrained, editorial
Composition/framing: wide landscape, layered depth from reef foreground to open water horizon, generous calm negative space
Lighting/mood: luminous but natural, inspiring, warm, intelligent, non-corporate
Color palette: deep ocean blue, sea-glass green, plankton gold, coral rose accents, soft white highlights
Constraints: no text, no labels, no numbers, no pseudo-UI glyphs, no fake charts, no logos, no watermark; avoid neon sci-fi overload; no military surveillance feeling; ecological and humane rather than extractive
```

### 006 kelp otter guardian revision

```text
Use case: photorealistic-natural
Asset type: Blue Life Commons kelp forest guardian source plate, 16:9 website/banner image
Primary request: a serene temperate kelp forest scene with a clearly identifiable sea otter floating on its back near the surface above the kelp canopy, seen from a respectful natural distance
Scene/backdrop: split-level underwater perspective in a kelp forest, sunlight through surface ripples, rocky reef and fish below
Subject: one sea otter floating on its back near the surface with visible paws and rounded face, small fish below, kelp fronds surrounding but not obscuring the animal
Style/medium: photorealistic nature photography, high-end conservation editorial, realistic animal anatomy
Composition/framing: wide landscape, sea otter in upper third, kelp columns framing a calm open-water corridor, rich but believable habitat detail
Lighting/mood: calm, nourishing, protective, alive, contemplative
Color palette: kelp amber, deep teal, green-gold sunlight, cool blue shadows
Constraints: no text, no logos, no watermark, no seals, no sea lions, no distressed animals, no touching or feeding, no impossible animal density; realistic marine life scale and behavior
```

### 007 mangrove nursery

```text
Use case: photorealistic-natural
Asset type: Blue Life Commons mangrove nursery source plate, 16:9 website/banner image
Primary request: a healthy mangrove nursery habitat at high tide, showing small fish and juvenile marine life sheltered among mangrove roots, with a gentle human restoration presence far in the background
Scene/backdrop: tropical mangrove edge, clear shallow water, prop roots, soft sky reflection
Subject: mangrove roots with schools of small fish, young mangrove plants, two distant community volunteers on a boardwalk carrying unmarked equipment without disturbing habitat
Style/medium: photorealistic conservation photography, natural and sophisticated
Composition/framing: wide landscape, low near-water perspective, roots creating elegant vertical rhythm, volunteers tiny and secondary
Lighting/mood: warm, protective, alive, resilient, inviting
Color palette: mangrove green, warm brown roots, clear turquoise water, sunlit gold
Constraints: no text, no logos, no labels, no watermark, no plastic debris, no nets, no animal handling, no invasive equipment in foreground, no fantasy colors; plausible coastal ecology and realistic scale
```

### 008 manta ray

```text
Use case: photorealistic-natural
Asset type: Blue Life Commons species empathy source plate, 16:9 website/banner image
Primary request: a manta ray gliding through clear blue water above a healthy reef slope, surrounded by small fish at natural distance
Scene/backdrop: tropical reef slope, filtered sunlight, open water gradient, no humans present
Subject: one manta ray with accurate graceful body shape and cephalic fins, viewed from slightly above and behind, moving calmly
Style/medium: photorealistic underwater wildlife photography, elegant conservation editorial
Composition/framing: wide landscape, manta ray crossing diagonally through frame, open negative space for overlays, reef texture below
Lighting/mood: serene, awe-inspiring, warm, respectful, spacious
Color palette: deep blue, turquoise, pale sand, muted coral, silver fish highlights
Constraints: no text, no logos, no watermark, no divers, no touching, no feeding, no entanglement, no rope-like tail artifacts, no exaggerated fantasy patterns; scientifically plausible manta anatomy and marine behavior
```
