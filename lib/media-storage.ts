export interface MediaStorageVariant {
  name: string
  role: string
  publicUse: boolean
  format: string
  width?: number
  height?: number
}

export interface MediaStorageLayer {
  name: string
  job: string
  stores: string
  reason: string
}

export const MEDIA_STORAGE_PUBLIC_BASE_URL =
  "https://7xuojupgkl56rqhi.public.blob.vercel-storage.com"

export const MEDIA_STORAGE_STACK: MediaStorageLayer[] = [
  {
    name: "GitHub",
    job: "Truth and review trail",
    stores:
      "Code, source metadata, licenses, object keys, public-safe manifests, and evidence.",
    reason:
      "Git should stay small, reviewable, and transparent; it should not become the image warehouse.",
  },
  {
    name: "Vercel Blob",
    job: "First owned pixel store",
    stores:
      "The first 31 approved species images, public Blob URLs, and the upload manifest used by production routes.",
    reason:
      "Vercel-native storage gets the encyclopedia fully owned and hosted without adding a second infrastructure provider at launch.",
  },
  {
    name: "Postgres",
    job: "Operational registry",
    stores:
      "Asset rows, variant rows, grants, reviews, checksums, stale-source state, and audit events.",
    reason:
      "A database is the right layer for search, workflow state, permission expiry, and contributor operations at scale.",
  },
  {
    name: "Vercel",
    job: "Application and publishing layer",
    stores:
      "Next.js routes, reviewer UI, environment variables, Blob store connection, and production deployments.",
    reason:
      "The app and first media store now live together; R2 remains the later option if high image traffic makes egress economics more important.",
  },
]

export const MEDIA_STORAGE_VARIANTS: MediaStorageVariant[] = [
  {
    name: "original",
    role: "Private approved source copy",
    publicUse: false,
    format: "source",
  },
  {
    name: "thumb",
    role: "Compact grid and admin thumbnail",
    publicUse: true,
    format: "webp",
    width: 320,
  },
  {
    name: "card",
    role: "Species cards and visual audit board",
    publicUse: true,
    format: "webp",
    width: 640,
  },
  {
    name: "hero",
    role: "Species page hero",
    publicUse: true,
    format: "webp",
    width: 1280,
  },
  {
    name: "og",
    role: "Social preview image",
    publicUse: true,
    format: "jpg",
    width: 1200,
    height: 630,
  },
  {
    name: "full",
    role: "Public high-resolution inspection",
    publicUse: true,
    format: "webp",
    width: 1920,
  },
]

export function mediaStorageObjectPrefix({
  taxonGroup,
  slug,
  assetId,
}: {
  taxonGroup: string
  slug: string
  assetId: string
}): string {
  return `species/${taxonGroup}/${slug}/${assetId}/`
}
