# Deep Time Marine Reptiles — special section (2026-07-16)

## Naming (correct the “ocean dinosaur” myth)

Popular culture often says **ocean dinosaurs**. Scientifically:

| Group | What it is | Examples in this ship |
|-------|------------|------------------------|
| **Mosasaurs** | Giant marine lizards (Squamata) | *Mosasaurus hoffmannii*, *Tylosaurus proriger* |
| **Plesiosaurs** | Four-flipper marine reptiles; long-neck branch | *Elasmosaurus platyurus* |
| **Pliosaurs** | Four-flipper marine reptiles; short-neck / big-head branch | *Kronosaurus queenslandicus* |
| **Ichthyosaurs** | Dolphin-shaped marine reptiles | *Ophthalmosaurus icenicus* |
| **Dinosaurs** | Clade Dinosauria — mostly terrestrial | **Not** this guild (see dino-life-commons) |

True dinosaurs were overwhelmingly land animals. The ocean apex of the Mesozoic was dominated by **marine reptiles**.

## Why this belongs on Blue Life Commons

1. Bridge curiosity (“sea monsters”) → accurate ocean deep-time literacy.
2. Same commons discipline: sources, review status, ethics of claims.
3. Generated media is the honest primary visual for soft-tissue extinct taxa — labeled **concept reconstruction**.

Living wildlife remains the core of BLC. This guild is a **special educational section**, not a replacement for living species media pipelines.

## Shipped in this batch

### Content

- `content/species/marine-reptiles/*.md` — 5 species pages
- Guild label: **Deep Time Marine Reptiles**
- Encyclopedia special callout + pinned guild section

### Media (Grok Imagine via CLI)

| Asset | Path |
|-------|------|
| 5 heroes | `public/media/species/{slug}.png` |
| Flagship loops | `mosasaurus-hoffmannii.mp4`, `tylosaurus-proriger.mp4` |
| Provenance | `public/media/species/media-job.json` |

### Product wiring

- `lib/media.ts` — concept reconstruction + optional `videoUrl`
- `components/artifact-media.tsx` — concept badge + muted autoplay hero video
- `lib/utils.ts` — `GUILD_META["marine-reptiles"]`
- `components/species-encyclopedia.tsx` — Deep Time special section

## Anatomy QA (mandatory)

After every still: vision-check that the **filename matches diagnostic anatomy**. Historical failure mode (sibling dino-life-commons): T. rex content written under Ankylosaurus filename.

This batch: PASS for mosasaur / elasmosaur / ichthyosaur stills inspected 2026-07-16.

## Storage note

Host disk was ~17 GiB free. Batch limited to 5 stills + 2 short videos.

## Related

- Sibling: [dino-life-commons](https://github.com/frankxai/dino-life-commons)
- Skill: `life-commons-encyclopedia`
- Media route: Grok CLI `image_gen` + `image_to_video` (Hermes FAL may be unconfigured)
