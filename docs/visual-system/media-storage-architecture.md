# Media Storage Architecture

Last updated: 2026-07-04

## Decision

Blue Life Commons now uses this production split:

- GitHub stores code, rights metadata, review trail, source URLs, object pathnames, public manifests, and evidence.
- Vercel Blob stores the first owned copies of approved species images.
- Vercel hosts the Next.js application, project environments, Blob store connection, previews, and production routes.
- Postgres remains the next operational registry layer for grants, review events, stale-source checks, object inventory, and contributor workflows.
- Cloudflare R2 remains a later migration option when traffic, partner libraries, video, or egress economics justify a dedicated media domain.

This matches the current product need: get every approved animal image hosted on the same platform as the app, with minimal infrastructure, while keeping the repo reviewable.

## Why Vercel Blob First

Vercel Blob is integrated with Vercel projects and the `@vercel/blob` SDK. The Vercel docs describe a project-connected Blob store, local `BLOB_READ_WRITE_TOKEN` use for batch uploads, and OIDC as the preferred runtime authentication path. The Vercel CLI also supports Blob store creation and file operations.

Cloudflare R2 is still attractive for a large public media library because its pricing docs list free internet egress for R2 storage classes. For the next phase, however, Vercel Blob is simpler and already connected to the production project.

Sources:

- Vercel Blob docs: <https://vercel.com/docs/vercel-blob>
- Vercel Blob SDK docs: <https://vercel.com/docs/vercel-blob/using-blob-sdk>
- Vercel Blob CLI docs: <https://vercel.com/docs/cli/blob>
- Vercel pricing: <https://vercel.com/docs/pricing>
- Vercel custom domain guide: <https://vercel.com/docs/domains/set-up-custom-domain>
- Cloudflare R2 pricing: <https://developers.cloudflare.com/r2/pricing/>
- GitHub large-file guidance: <https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github>

## Current Production State

| Layer | State |
|---|---|
| Vercel project | `starlight-intelligence/blue-life-commons` |
| Blob store | `blue-life-commons-media` |
| Blob access | public |
| Store region | `iad1` |
| Uploaded approved images | 31 |
| Public Blob manifest | `content/media/species-media-blob-manifest.json` |
| App read behavior | Prefer Blob URL when an approved asset appears in the Blob manifest; fall back to approved source URL otherwise |
| Official domain | Not connected yet; `bluelifecommons.org` was available for purchase on 2026-07-04 |

## Object Pathnames

Approved species media uses this immutable pathname prefix:

```text
species/{taxon_group}/{slug}/{asset_id}/
```

The first Vercel Blob upload pass stores the approved source copy at:

```text
original/source.{source_ext}
```

The storage manifest still tracks the intended derivative slots:

```text
public/thumb-320.webp
public/card-640.webp
public/hero-1280.webp
public/og-1200x630.jpg
public/full-1920.webp
```

Those derivative variants are not required for the first production pass. They should be generated after image transformation, EXIF stripping, checksum logging, and QA are automated.

## Repo Assets

- Storage policy: `content/media/species-media-storage-policy.yaml`
- Storage plan: `content/media/species-media-storage-manifest.yaml`
- Blob upload manifest: `content/media/species-media-blob-manifest.json`
- Human review pack: `content/media/review-packs/species-media-storage-manifest-2026-07-04.md`
- Operational SQL schema: `schema/media-storage-schema.sql`
- Upload script: `scripts/upload_species_media_to_vercel_blob.mjs`
- Env contract: `.env.example`

Commands:

```bash
npm run media:storage
npm run media:storage:check
npm run media:blob:plan
npm run media:blob:upload
npm run media:blob:check
```

`media:blob:upload` reads `.env.local` or `BLOB_READ_WRITE_TOKEN`, uploads only approved media rows, and writes public Blob URLs to the Blob manifest. Secrets are never written to Git.

## Domain Runbook

The app metadata and sitemap are already prepared for:

```text
https://bluelifecommons.org
```

As of 2026-07-04, Vercel reported `bluelifecommons.org` as available for `$9.99/year`; DNS resolution for `bluelifecommons.org` and `www.bluelifecommons.org` failed, and the Vercel project listed only Vercel-managed domains.

To make the official domain live:

1. Purchase or transfer `bluelifecommons.org`.
2. Add `bluelifecommons.org` and `www.bluelifecommons.org` to the Vercel project.
3. If using third-party DNS, configure the Vercel-provided DNS records. Vercel's standard guide uses an apex `A` record to Vercel and a `www` CNAME to Vercel DNS when prompted.
4. Wait for Vercel verification and certificate issuance.
5. Verify `/`, `/species`, `/encyclopedia`, `/media-intelligence`, and `/sitemap.xml` on the official domain.

Do not claim the official domain is connected until DNS resolves and Vercel lists the domain on the project.

## Cost Guardrails

- Store approved originals once; avoid duplicates.
- Keep Git free of bulk binaries.
- Do not run request-time transformations for every page view.
- Generate `thumb`, `card`, `hero`, and `og` variants in a controlled batch before traffic grows.
- Keep original source pages and credits visible even after owned hosting.
- Move to R2 or another dedicated object store only when transfer volume, partner archives, or large media justify the extra provider.

## Scale Model

| Scale | Assets | Expected Path |
|---|---:|---|
| Current | 31 approved images | Vercel Blob originals plus public manifest |
| Near term | 100-1,000 images | Vercel Blob, generated variants, source/rights ledger |
| Growth | 1,000-10,000 images | Postgres registry, queue-based ingest, stale-source jobs |
| Heavy media | 10,000+ images, video, or high transfer | Compare Vercel Blob transfer against R2 free-egress architecture |

The expensive mistakes are not the first 31 images. They are unbounded transfer, hot transformations, storing binaries in Git, and publishing media whose rights or welfare context are unclear.
