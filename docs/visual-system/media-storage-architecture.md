# Media Storage Architecture

Last updated: 2026-07-04

## Decision

Blue Life Commons should use this split:

- GitHub stores code, metadata, review trail, source URLs, license fields, object keys, and public-safe manifests.
- Cloudflare R2 stores approved originals and generated public derivatives.
- Postgres stores the operational registry, review events, partner grants, object inventory, and stale-source state.
- Vercel hosts the Next.js application, reviewer/contributor interfaces, and production routes.

This keeps the repository light and reviewable while making the image platform durable enough for tens of thousands or millions of assets.

## Why R2 First

Cloudflare documents R2 as S3-compatible object storage and lists the S3 API endpoint pattern as `https://<ACCOUNT_ID>.r2.cloudflarestorage.com`. R2 public buckets can be connected to a custom domain for public reads. Cloudflare's R2 pricing page also says there are no egress bandwidth charges for any storage class, while storage and operations are metered.

Vercel Blob remains a good fallback for simple Vercel-native uploads, but Vercel Blob has storage, operation, and data-transfer pricing. For a public animal image library, the lower egress-risk architecture is R2 plus pre-generated derivatives served from a media domain.

GitHub is not the pixel warehouse. GitHub's large-file guidance discourages large binary repositories; the repo should keep media truth and review data, not bulk originals.

Sources:

- Cloudflare R2 overview: <https://developers.cloudflare.com/r2/>
- Cloudflare R2 S3 API: <https://developers.cloudflare.com/r2/api/s3/>
- Cloudflare R2 S3 compatibility endpoint: <https://developers.cloudflare.com/r2/api/s3/api/>
- Cloudflare R2 public buckets: <https://developers.cloudflare.com/r2/buckets/public-buckets/>
- Cloudflare R2 pricing: <https://developers.cloudflare.com/r2/pricing/>
- Vercel Blob docs: <https://vercel.com/docs/vercel-blob>
- Vercel pricing: <https://vercel.com/docs/pricing>
- GitHub large-file guidance: <https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github>

## Buckets

Use three buckets:

| Bucket | Access | Purpose |
|---|---|---|
| `blue-life-media-prod` | public derivatives through `media.bluelifecommons.org`; originals private by default | Approved production media |
| `blue-life-media-staging` | private or restricted | Variant generation, QA, migration batches |
| `blue-life-media-review` | private | Contributor uploads, partner originals, reviewer-only candidates |

Writes use the S3-compatible R2 endpoint. Public reads use the custom media domain.

## Object Keys

Approved species media uses this immutable prefix:

```text
species/{taxon_group}/{slug}/{asset_id}/
```

Inside each prefix:

```text
original/source.{source_ext}
public/thumb-320.webp
public/card-640.webp
public/hero-1280.webp
public/og-1200x630.jpg
public/full-1920.webp
```

Never overwrite an approved asset prefix. If a species gets a better image, create a new asset id and retire the older asset in the database.

## Current Setup In Repo

- Storage policy: `content/media/species-media-storage-policy.yaml`
- Generated storage manifest: `content/media/species-media-storage-manifest.yaml`
- Human review pack: `content/media/review-packs/species-media-storage-manifest-2026-07-04.md`
- Operational SQL schema: `schema/media-storage-schema.sql`
- Env contract: `.env.example`
- Generator: `scripts/build_species_media_storage_manifest.py`

Run:

```bash
python scripts/build_species_media_storage_manifest.py
python scripts/build_species_media_storage_manifest.py --check
```

The first generated manifest maps the current 31 approved species images into deterministic object keys and derivative URLs, but it does not download, transform, upload, or sign any file.

## Migration Flow

1. Keep using the existing approved source URLs in production until owned derivatives exist.
2. Create the three R2 buckets and connect `media.bluelifecommons.org` to the production bucket.
3. Add the `.env.example` variables to Vercel and local secret storage.
4. Run the storage manifest generator.
5. For each approved image, re-check rights, source, credit, blocked surfaces, and EXIF/sensitive-location constraints.
6. Mirror only media whose rights allow copying and derivative generation.
7. Generate the fixed derivatives.
8. Insert `media_asset`, `media_variant`, `media_rights_grant`, and `media_review_event` rows.
9. Export a public-safe manifest back to Git.
10. Switch public routes from `original_media_url` to the owned `card`, `hero`, and `og` variants.

## Cost Guardrails

- Pre-generate variants instead of relying on request-time transformations.
- Prefer `<picture>`/`srcset` with immutable variant URLs.
- Do not use Vercel Image Optimization as the default path for the large public library.
- Keep originals private unless public inspection requires a public `full` derivative.
- Strip EXIF before public derivative generation.
- Keep partner originals private unless the grant explicitly allows public hosting.
- Track stale source URLs and license changes as review events.

## Scale Model

| Scale | Assets | Expected Path |
|---|---:|---|
| Current | 31 approved images | external approved URLs plus storage manifest |
| Near term | 1k-5k assets | R2 buckets, generated derivatives, manifest exports |
| Growth | 30k-500k assets | Postgres registry, queue-based ingest, stale-source jobs |
| Commons scale | 1M+ assets | dedicated media service, search index, partner grant automation |

The expensive mistakes are not storage itself. They are hot transformations, unbounded egress, committing binaries to Git, and publishing assets whose rights or welfare context are unclear.
