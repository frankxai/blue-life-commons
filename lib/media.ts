import type {
  Artifact,
  ArtifactMediaGalleryItem,
  ArtifactMediaVideoLink,
} from "@/lib/types"
import blobManifest from "@/content/media/species-media-blob-manifest.json"

export interface ApprovedSpeciesMedia {
  assetId?: string
  imageUrl: string
  imageUrlSource?: "vercel_blob" | "approved_source" | "local_concept"
  sourceUrl?: string
  originalMediaUrl?: string
  ownedStorageUrl?: string
  ownedStorageProvider?: string
  creator?: string
  credit?: string
  license?: string
  licenseUrl?: string
  rightsStatus?: string
  altText: string
  videoUrl?: string
  conceptReconstruction?: boolean
}

export interface SpeciesGalleryItem extends ArtifactMediaGalleryItem {
  imageUrl: string
  isConcept: boolean
}

interface SpeciesBlobRecord {
  approved_asset_id?: string
  storage?: {
    provider?: string
    status?: string
    blob_url?: string
  }
}

function cleanText(value?: string): string | undefined {
  const cleaned = value?.replace(/\s+/g, " ").trim()
  return cleaned || undefined
}

const blobByAssetId = new Map(
  ((blobManifest as { records?: SpeciesBlobRecord[] }).records ?? [])
    .filter(
      (record) =>
        record.approved_asset_id &&
        record.storage?.status === "uploaded" &&
        record.storage?.blob_url,
    )
    .map((record) => [record.approved_asset_id as string, record]),
)

export function getApprovedSpeciesMedia(
  artifact: Artifact,
): ApprovedSpeciesMedia | undefined {
  const primary = artifact.media?.primary
  const render = artifact.media?.render
  const review = artifact.media?.review
  const video = artifact.media?.video

  if (!primary?.public_media_url) return undefined
  if (artifact.type !== "species-page") return undefined
  if (!render || render.strategy !== "approved_primary_image") return undefined
  if (render.public_visual_kind !== "image") return undefined
  if (render.public_visual_public_use !== true) return undefined
  if (review?.primary_status !== "approved") return undefined
  if (primary.qa_status !== "approved") return undefined
  if (render.candidate_public_use === true) return undefined

  const ownedBlob = primary.asset_id ? blobByAssetId.get(primary.asset_id) : undefined
  const ownedStorageUrl = cleanText(ownedBlob?.storage?.blob_url)
  const conceptReconstruction =
    primary.rights_status === "concept-reconstruction" ||
    review?.curation_decision === "approve_concept_reconstruction_deep_time" ||
    video?.rights_status === "concept-reconstruction" ||
    video?.rights_status === "generated-owned"
  const imageUrl = ownedStorageUrl ?? primary.public_media_url
  const imageUrlSource: ApprovedSpeciesMedia["imageUrlSource"] = ownedStorageUrl
    ? "vercel_blob"
    : conceptReconstruction || imageUrl.startsWith("/")
      ? "local_concept"
      : "approved_source"

  return {
    assetId: cleanText(primary.asset_id),
    imageUrl,
    imageUrlSource,
    sourceUrl: cleanText(primary.source_url),
    originalMediaUrl: cleanText(primary.original_media_url),
    ownedStorageUrl,
    ownedStorageProvider: ownedStorageUrl
      ? cleanText(ownedBlob?.storage?.provider) ?? "vercel_blob"
      : undefined,
    creator: cleanText(primary.creator),
    credit: cleanText(primary.credit),
    license: cleanText(primary.license),
    licenseUrl: cleanText(primary.license_url),
    rightsStatus: cleanText(primary.rights_status),
    altText:
      cleanText(primary.alt_text) ??
      `Approved primary species image for ${artifact.title}.`,
    videoUrl: cleanText(video?.public_media_url),
    conceptReconstruction,
  }
}

export function getUrlHost(url?: string): string | undefined {
  if (!url) return undefined
  try {
    return new URL(url).hostname.replace(/^www\./, "")
  } catch {
    return undefined
  }
}

export function getMediaCreditText(media: ApprovedSpeciesMedia): string {
  return [media.creator, media.license].filter(Boolean).join(" / ")
}

/**
 * Educational multi-angle gallery. Only items with public URLs and non-blocked QA.
 * Concept/generated assets must remain labeled in the UI — never as ID evidence.
 */
export function getSpeciesGallery(artifact: Artifact): SpeciesGalleryItem[] {
  const items = artifact.media?.gallery ?? []
  return items
    .map((item) => {
      const imageUrl = cleanText(item.public_media_url)
      if (!imageUrl) return undefined
      if (item.qa_status === "blocked") return undefined
      const isConcept =
        item.concept_only === true ||
        item.rights_status === "concept-reconstruction" ||
        item.rights_status === "generated-owned"
      // Real-photo gallery items should be curated approved (or explicit concept).
      if (!isConcept && item.qa_status && item.qa_status !== "approved") {
        return undefined
      }
      return {
        ...item,
        imageUrl,
        isConcept,
      }
    })
    .filter((item): item is SpeciesGalleryItem => Boolean(item))
}

export function getSpeciesVideoLinks(
  artifact: Artifact,
): ArtifactMediaVideoLink[] {
  return (artifact.media?.video_links ?? []).filter(
    (item) => Boolean(item.url) && Boolean(item.title),
  )
}
