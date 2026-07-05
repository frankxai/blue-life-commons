# Scale And Cost Plan

Last updated: 2026-07-05

## Decision

Start and stay with Vercel first. Blue Life Commons already uses Vercel for the Next app and Vercel Blob for approved species images. Adding Cloudflare now would add operational surface before the current catalog or traffic requires it.

The near-term work is image optimization, derivative generation, analytics, and monitoring. Provider migration is a later decision with clear triggers.

## Current Storage Baseline

| Metric | Current value |
|---|---:|
| Approved image records | 31 |
| Total approved original image bytes | 56,772,199 bytes |
| Total approved original image storage | 54.142 MB |
| Average original image size | 1.747 MB |
| Largest approved original | 5.977 MB |

Source: calculated from `records[].storage.source_content_length` in [`species-media-blob-manifest.json`](../../content/media/species-media-blob-manifest.json).

## Cost Model

The important cost driver is not storing the first 31 images. It is transfer volume, hot image transformation, and larger media types.

Vercel Blob pricing should be checked against the live Vercel dashboard before a provider change. As of this plan, the Vercel Blob pricing docs list resource-based pricing for storage and data transfer. The product should track both monthly storage and monthly Blob transfer.

| Scenario | Storage estimate at current average size | Product decision |
|---|---:|---|
| 31 images | 54.142 MB | Vercel Blob is appropriate |
| 100 images | About 174.7 MB | Vercel Blob plus generated derivatives |
| 1,000 images | About 1.747 GB | Vercel Blob remains plausible; monitor transfer and optimize delivery |
| 10,000 images | About 17.47 GB | Compare Vercel Blob against dedicated object storage and CDN options |

These are storage estimates only. Real monthly cost depends on plan allowances, transfer, cache behavior, image optimization, derivative sizes, and traffic.

## Vercel-First Optimization Path

1. Store approved originals once in Vercel Blob.
2. Generate deterministic derivatives:
   - `thumb-320.webp`
   - `card-640.webp`
   - `hero-1280.webp`
   - `og-1200x630.jpg`
   - `full-1920.webp`
3. Strip EXIF and log checksums before publishing derivatives.
4. Serve card/hero/OG sizes by surface instead of original files.
5. Track monthly Blob storage, Blob transfer, image optimization usage, and route traffic.
6. Keep GitHub limited to metadata, manifests, review records, and scripts.

## Migration Triggers

Re-evaluate Cloudflare R2, S3 plus CDN, or another object-store/CDN architecture when one or more are true:

- Monthly Blob transfer cost is material for two consecutive months after derivative optimization.
- The catalog exceeds 10,000 approved images.
- Video, audio, 3D, or bulk partner archives become a core public product surface.
- Partner contracts require custom media domains, signed access, regional controls, or asset lifecycle policies Vercel Blob does not cover well.
- Review and publication state needs an operational database beyond committed manifests.

Do not migrate because the first image batch feels "big." The current approved originals are about 54.142 MB total.

## Monitoring

| Signal | Why it matters |
|---|---|
| Blob storage GB | Storage cost and catalog scale |
| Blob transfer GB | Primary operating cost risk |
| Image optimization usage | Avoid accidental request-time transformation costs |
| Average delivered image KB | Detect oversized originals reaching cards |
| p95 species page weight | User experience and bandwidth |
| 404/blocked image count | Broken manifest or permission issue |
| Public candidate URL count | Must remain 0 |

## Domain Readiness

The official domain should be connected only after ownership, DNS records, Vercel domain verification, and certificate issuance are complete. Do not claim `bluelifecommons.org` is live until DNS resolves and the Vercel project lists the domain.

## Sources

- Media storage architecture: [`media-storage-architecture.md`](../visual-system/media-storage-architecture.md)
- Species Blob manifest: [`species-media-blob-manifest.json`](../../content/media/species-media-blob-manifest.json)
- Vercel Blob pricing: <https://vercel.com/docs/vercel-blob/usage-and-pricing>
- Vercel pricing: <https://vercel.com/docs/pricing>
- Vercel custom domain guide: <https://vercel.com/docs/domains/set-up-custom-domain>
- Cloudflare R2 pricing: <https://developers.cloudflare.com/r2/pricing/>
