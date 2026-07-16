# Scale And Cost Plan

Last updated: 2026-07-16

## Decision

Start and stay with **Vercel first** (app + Blob). Adding Cloudflare R2 is a **later** decision after delivery optimization and measured transfer cost—not before.

**Full economics, ROI, nonprofit/commercial model, and budget ladders:**  
[`media-economics-and-roi.md`](media-economics-and-roi.md)

Deep Time media doctrine: [`../deep-time-media-scale-strategy.md`](../deep-time-media-scale-strategy.md)

## Current Storage Baseline (2026-07-16)

| Metric | Current value |
|---|---:|
| Species pages (approx) | ~44 |
| Living approved image records on Blob | 31 |
| Living approved original image storage | ~54.1 MB |
| Deep Time concept stills | 13 |
| Deep Time videos (6s 720p) | 13 |
| Deep Time mirrored on Blob | ~81 MB (26 files) |
| Combined media order of magnitude | **≪ 1 GB** |

Sources: `species-media-blob-manifest.json`, `deep-time-blob-manifest.json`, `public/media/species`.

## Cost Model

The important cost driver is **not** storing the first ~100 MB. It is:

1. **Blob / CDN transfer** of hot heroes and especially **autoplay video**
2. **AI generation** (stills + video credits)
3. **Expert review** time
4. App Fast Data Transfer and builds

| Scenario | Storage estimate | Product decision |
|---|---:|---|
| Current (~130 MB combined) | Trivial | Vercel Blob appropriate |
| 200 stills + 20 videos | ~0.3–0.5 GB | Blob + WebP derivatives; video click-to-play |
| 1,000 stills + 50 videos | ~1.5–2.5 GB | Blob still fine; monitor transfer weekly |
| 10,000 stills + heavy video traffic | 10–90 GB class | R2 + custom media domain after optimization |

## Vercel-First Optimization Path

1. Store approved originals once in Vercel Blob (living + deep-time masters).
2. Generate deterministic derivatives:
   - `thumb-320.webp`
   - `card-640.webp`
   - `hero-1280.webp`
   - `og-1200x630.jpg`
3. **Cards never load MP4.** Heroes: poster first; video on intent / muted flagship only.
4. Strip EXIF; checksum; immutable keys with long cache.
5. Track monthly Blob storage, Blob transfer, image optimization, route traffic.
6. Keep GitHub limited to metadata, manifests, review records, scripts.

## Migration Triggers (Blob → R2 or dual-write)

- Monthly Blob **transfer** cost material for **two consecutive months** after derivative optimization.
- Video library multi-GB **and** high play volume.
- Partner archives, custom media domain, regional controls, or lifecycle policies Blob fits poorly.
- Review inventory needs a real media DB beyond YAML.

Do **not** migrate because the first Deep Time video batch “feels big” (~80 MB).

## Monitoring

| Signal | Why it matters |
|---|---|
| Blob storage GB | Catalog scale |
| **Blob transfer GB** | Primary operating cost risk |
| Image optimization usage | Avoid accidental transform spend |
| Average delivered image KB | Oversized cards |
| p95 species page weight | Mobile UX |
| Video play rate | Whether video earns its cost |
| Cost per 1k sessions | Unit economics |

Monthly template: [`metrics/monthly-cost-ledger.TEMPLATE.md`](metrics/monthly-cost-ledger.TEMPLATE.md)

## Domain

Production domain: **https://bluelifecommons.org** (connected). Keep DNS/Vercel project as SSOT.

## Sources

- Media economics & ROI: [`media-economics-and-roi.md`](media-economics-and-roi.md)
- Media storage architecture: [`../visual-system/media-storage-architecture.md`](../visual-system/media-storage-architecture.md)
- Species Blob manifest: [`../../content/media/species-media-blob-manifest.json`](../../content/media/species-media-blob-manifest.json)
- Deep Time Blob manifest: [`../../content/media/deep-time-blob-manifest.json`](../../content/media/deep-time-blob-manifest.json)
- Vercel Blob pricing: <https://vercel.com/docs/vercel-blob/usage-and-pricing>
- Vercel pricing: <https://vercel.com/docs/pricing>
- Cloudflare R2 pricing: <https://developers.cloudflare.com/r2/pricing/>
