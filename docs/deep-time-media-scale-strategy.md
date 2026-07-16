# Deep Time + Living Media Scale Strategy

**Status:** Living operating plan · 2026-07-16  
**Product:** Blue Life Commons (`bluelifecommons.org`)  
**Sibling:** Dino Life Commons (terrestrial dinosaurs)

---

## 1. Are there “ocean dinosaurs”?

### Short answer

**No — not in the popular “sea monster” sense.** The animals people mean by “ocean dinosaurs” are almost always **Mesozoic marine reptiles**, not members of Dinosauria living full-time in the open ocean.

| Group | What it is | Ocean role |
|-------|------------|------------|
| **Mosasaurs** | Giant marine lizards (Squamata) | Late Cretaceous apex predators |
| **Plesiosaurs / pliosaurs** | Four-flipper marine reptiles | Long-neck vs short-neck body plans |
| **Ichthyosaurs** | Fully marine reptiles, dolphin-like | Jurassic–Triassic open-water forms |
| **Thalattosuchians** | Marine crocodylomorphs | Fully marine crocs (not dinosaurs) |
| **Dinosaurs** | Dinosauria (mostly terrestrial) | Rare aquatic *foraging* adaptations only |
| **Avian dinosaurs** | Birds (incl. diving *Hesperornis*) | Flying/diving birds — still not mosasaurs |

### Edge cases (document, don’t confuse)

1. ***Spinosaurus*** — a **dinosaur** with aquatic foraging traits. Belongs in a future **“aquatic dinosaurs”** lane (or dino-life-commons), **not** the marine-reptiles guild as if it were a mosasaur.
2. ***Hesperornis*** — flightless diving **bird** (avian dinosaur in the broad clade sense). Teaching point for convergence; not a plesiosaur.
3. ***Megalodon*** — giant **shark** (fish), Cenozoic. Living-ocean lineage story, not Deep Time marine reptiles.

**Product rule:** Deep Time guild = marine reptiles (+ marine crocs). Optional future guilds: `aquatic-dinosaurs`, `deep-time-sharks`. Never flatten labels for SEO alone.

---

## 2. How many more deep-time marine reptiles are there?

### Scientific reality

There are **hundreds** of named marine reptile genera/species across Triassic–Cretaceous (Paleobiology Database + monographs). A complete encyclopedia is multi-year specialist work.

### Product reality (teachable set)

| Tier | Count | Purpose |
|------|-------|---------|
| **A — Core teaching set** | ~12–20 | Body plans every student should know |
| **B — Museum / regional stars** | +30–50 | Famous specimens, formation stories |
| **C — Long-tail taxa** | hundreds | Specialist expansion, needs experts |

**Shipped / shipping in this wave:** 13 Deep Time entries (7 prior + 6 new).  
**Next A-tier backlog (examples):** *Prognathodon*, *Plotosaurus*, *Dolichorhynchops*, *Cryptoclidus*, *Ophthalmosaurus* family expansions, *Mixosaurus*, *Cymbospondylus*, *Geosaurus*, *Rhomaleosaurus*.

**Stop condition for “done enough” Core set:** every major body plan has ≥2 exemplars + living-ocean compare links + labeled concept media.

---

## 3. Media doctrine (deep-time vs living)

### Deep Time (extinct)

| Asset | Policy |
|-------|--------|
| **Still (PNG hero)** | **Required** for every public deep-time page | Concept reconstruction via Grok Imagine |
| **Video (MP4)** | **Optional flagship only** | 1–3 per major body-plan family |
| Label | Always **concept reconstruction** — never fossil evidence |

**Why not video for all?** Cost, storage, diminishing UX returns, and accessibility (motion). Stills + one loop per family already sell the wonder.

### Living animals (existing ~31+ species)

| Asset | Policy |
|-------|--------|
| **Primary still** | Prefer **real photography** with rights: Wikimedia PD/CC, NOAA, partner grants, iNat open licenses after QA |
| **Generated still** | Supporting / concept only — never primary identification |
| **Video** | Only when it teaches motion/behavior (e.g. whale breach, manta feeding) **and** rights allow |
| **Animate still → video** | Use sparingly for hero marketing pages — not every species |

**Pipeline order for living species**

1. Registry + rights check (existing BLC media system).  
2. Prefer Blob-mirrored approved primaries.  
3. Fill gaps with partner grants / open licenses.  
4. AI only as supporting key-art with hard labels.  
5. Video only for tier-A charismatic species or explicit missions.

---

## 4. Storage math (honest scale)

Assumptions from current Deep Time batch (~2026-07-16):

| Asset type | Typical size |
|------------|--------------|
| Hero still 1280×720 PNG | **~0.7–1.3 MB** (avg **~1.0 MB**) |
| Flagship 6s 720p MP4 | **~6–7 MB** |

### Scenarios

| Catalog | Stills only | + 10% video flagships | + 30% video |
|---------|-------------|------------------------|-------------|
| 50 species | ~50 MB | ~80–90 MB | ~140 MB |
| 200 species | ~200 MB | ~320–360 MB | ~560 MB |
| 1,000 species | ~1.0 GB | ~1.6–1.8 GB | ~2.8 GB |
| 10,000 species | ~10 GB | ~16–18 GB | ~28 GB |

**Repo rule (non-negotiable at scale):**  
GitHub stores **code + metadata**, not bulk originals. Object storage holds media (existing policy: Vercel Blob now → R2 later).

Current deep-time media in `public/media/species` is a **bootstrap** (~20 MB). Do **not** keep multi-GB video libraries in git long-term.

---

## 5. Vercel cost vs Cloudflare R2

### Now (correct default)

- **Vercel Blob** for approved public mirrors (already in `species-media-storage-policy.yaml`).  
- App stays on Vercel; domain `bluelifecommons.org`.  
- Git remains small.

### When to move hot media to R2

Trigger any of:

1. Media library **> ~5–10 GB** or rising transfer costs.  
2. Partner libraries / large originals / many videos.  
3. Need multi-product CDN (BLC + Dino + GenCreator) under one media plane.  
4. Egress economics beat Blob after measured traffic (not guesses).

### Cost intuition (order-of-magnitude, verify on live dashboards)

| Layer | What you pay for | Scale note |
|-------|------------------|------------|
| **Vercel App** | Builds, bandwidth for HTML/JS | Dominated by traffic, not species count |
| **Vercel Blob** | Storage + transfer of images/video | Fine for MB–low GB |
| **R2** | Storage + ops; **$0 egress to internet** (Cloudflare model) | Better when video/library grows |
| **GitHub** | Repo size / LFS pain | Avoid bulk media |

**Strategy:** stay Blob until measured pain → dual-write to R2 → cut over public URLs → keep Blob as temporary edge cache if useful.

---

## 6. Product value (why this is worth doing)

### User value

1. **Curiosity → accuracy:** fix the “ocean dinosaur” myth without killing wonder.  
2. **One UX contract:** living + deep-time share encyclopedia chrome, sources, review gates.  
3. **Mobile-first wonder:** large hero, short reading chips, optional motion with controls.  
4. **Bridge to action:** living pages still carry welfare, missions, rights-safe media.

### Business / commons value

1. Differentiates BLC from generic animal lists and pure entertainment paleo.  
2. Feeds social / education clips **with** provenance culture.  
3. Template for other commons (dino, forests, museums).  
4. Partner path: museums can co-own specimen pages later (Tier B).

### What we do *not* claim

- AI soft tissue as science fact.  
- Complete global marine reptile taxonomy.  
- That video equals better conservation outcomes without living-species action paths.

---

## 7. Mobile experience principles

1. Hero height capped on small screens (`max-h-[70dvh]`).  
2. Stat chips 2-column on mobile.  
3. Video: play/mute controls; reduced-motion = no autoplay.  
4. Sticky provenance only `lg+`.  
5. Compare mode stacks vertically on mobile.  
6. Prefer stills when data is expensive / offline-first teaching packs later.

---

## 8. Operating plan (drive)

### Wave 0 — Done / in flight

- Core UX, compare mode, stats chips, 13 deep-time taxa, selective videos, domain live.

### Wave 1 — Deep Time Core complete (this quarter)

1. Finish Tier A roster (~15–20).  
2. Still for every entry; max **1 video per body-plan family**.  
3. Move new large media off-git to Blob ASAP after approval.  
4. Expert review queue for science claims.

### Wave 2 — Living species media completeness

1. Close rights gaps for remaining living pages.  
2. Blob mirror all approved primaries.  
3. Video only for ~10 flagship living species.  
4. No AI primary heroes for living ID pages.

### Wave 3 — Scale economics

1. Instrument Blob storage + transfer monthly.  
2. Prototype R2 dual-write at 5 GB media.  
3. CDN custom media domain if multi-brand.

### Wave 4 — Depth products

1. Compare packs (school mode).  
2. Timeline UI (Triassic → Cretaceous).  
3. Optional `aquatic-dinosaurs` mini-guild (Spinosaurus et al.) clearly labeled.

---

## 9. Decision checklist (every media batch)

- [ ] Rights / concept label correct?  
- [ ] Anatomy matches filename (vision QA)?  
- [ ] Still required; video justified?  
- [ ] Disk + git size impact acceptable?  
- [ ] Blob path or public/ only for bootstrap?  
- [ ] Mobile hero + controls checked?  
- [ ] Sources + `needs-expert-review` set?

---

## 10. Related files

- `content/species/marine-reptiles/README.md`  
- `content/media/species-media-storage-policy.yaml`  
- `docs/product/scale-and-cost-plan.md`  
- `docs/visual-system/media-storage-architecture.md`  
- Sibling: `frankxai/dino-life-commons`

---

*Steward: Starlight / Blue Life Commons agents · Update after each media wave with real GB and traffic numbers.*
