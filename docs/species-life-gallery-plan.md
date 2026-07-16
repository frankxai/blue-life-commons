# Living species life gallery — media plan (Blue Whale pilot)

**Status:** pilot on `species-blue-whale`  
**Date:** 2026-07-16  
**Branch:** `feat/blue-whale-life-gallery`

## Decision: can / should we pull multi-angle media into the species page?

**Yes — as a curated educational gallery, not as silent live scrape.**

Blue Life Commons already forbids publishing unapproved candidate image URLs as identity media. The pilot adds:

| Surface | Source of truth | Rule |
|---------|-----------------|------|
| **Hero primary** | Registry-approved real photo (NOAA PD) | Identification surface |
| **Life gallery stills** | Frontmatter `media.gallery[]` | Multi-angle education; real photos `qa_status: approved` |
| **Concept panels** | Generated + local path | Scale / life-stage teaching only; hard **Concept** badge |
| **Video** | `media.video_links[]` | **Link-out** to NOAA / Sanctuaries hosts (no rehost without rights) |
| **Generated hero video** | Optional flagship only | Not required for every living species |

## Pull live vs generate

### Prefer live / open rights (Tier A)

| Need | Where | Notes |
|------|-------|-------|
| Adult identity / surface | Wikimedia + NOAA Photo Library (already candidates) | Promote with rights QA |
| Body plan / aerial proportion | NOAA PD body image | Good teaching angle |
| Fluke / dive angle | Wikimedia PD fluke | Field-ID practice |
| Status & threats video | NOAA Fisheries species page + Video Gallery | Link-out |
| Classroom whale packs | NOAA Sanctuaries teacher video hub | Link-out |
| Additional open photos | Wikimedia collect script; iNaturalist open data after ethics QA | Never auto-publish candidates |

### Prefer generate (Tier B concept)

| Need | Why generate | Label |
|------|--------------|-------|
| Size / scale comparison | Clean infographic with controlled metaphors | Concept reconstruction |
| Mother + calf life stage | High-quality open calf photos are sparse / rights-messy | Concept only |
| Cross-section / anatomy teaching | Needs deterministic labels (hybrid later) | Concept + text-on-page |
| Deep-time extinct taxa | Soft tissue unknown | Primary concept OK |

### Do **not** generate as primary for living species

- “This is what a blue whale looks like in the field” hero without real photo
- Fake IUCN charts / fake maps as evidence
- Precise breeding-site photography composites that defeat sensitivity rules

### Video policy

1. **Default:** link NOAA / Sanctuaries / peer NGO open education pages.  
2. **Rehost MP4:** only with clear PD/CC + ethics QA + Blob storage path.  
3. **AI image→video:** marketing/flagship only; label concept; tight disk budgets.

## Blue Whale pilot inventory

### Real stills (gallery)

1. `Bluewhale877.jpg` — adult surface (also primary)  
2. `Blue_Whale_001_body_bw.jpg` — body plan  
3. `Blue_whale_tail_fluke.JPG` — fluke  
4. `Anim1754_-_Flickr_-_NOAA_Photo_Library.jpg` — second NOAA surface  

### Concept stills (gallery)

5. Scale concept panel (generated)  
6. Mother–calf educational concept (generated)

### Video link-outs

- NOAA Fisheries blue whale profile  
- NOAA Sanctuaries whale education videos  
- NOAA B-roll Pacific whales  
- Sanctuaries ship-strike education path  

## Rollout for rest of catalog

1. **Schema/UI shipped once** (`gallery`, `video_links`, `SpeciesLifeGallery`).  
2. Per species:  
   - Run Wikimedia collect if candidates thin  
   - Curate 3–6 real angles (adult, feature, habitat, calf if rights OK)  
   - Add 0–2 concept panels only when education needs them  
   - Add 2–4 institutional video links  
3. Priority wave (charismatic living): blue whale → humpback → orca → sperm → right whale → whale shark → leatherback → great white.  
4. Keep Deep Time on concept-primary path (existing).  
5. Storage: prefer hotlink Commons Special:FilePath / Blob mirrors; avoid bulk local MP4 on laptop.

## Ops commands

```bash
python scripts/collect_wikimedia_species_media.py --per-species 4 --out content/media/candidates/...
python scripts/validate_species_media.py
python scripts/validate_artifacts.py content/species/cetaceans/blue-whale.md
npm run build
```

## Non-negotiables

- Sourced or silent for factual claims  
- Generated media never identification or conservation evidence  
- No precise sensitive locations in captions  
- Draft PR path for product changes  
