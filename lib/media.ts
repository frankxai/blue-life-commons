import type { Artifact } from "@/lib/types"

export interface ApprovedSpeciesMedia {
  assetId?: string
  imageUrl: string
  sourceUrl?: string
  originalMediaUrl?: string
  creator?: string
  credit?: string
  license?: string
  licenseUrl?: string
  rightsStatus?: string
  altText: string
}

function cleanText(value?: string): string | undefined {
  const cleaned = value?.replace(/\s+/g, " ").trim()
  return cleaned || undefined
}

export function getApprovedSpeciesMedia(
  artifact: Artifact,
): ApprovedSpeciesMedia | undefined {
  const primary = artifact.media?.primary
  const render = artifact.media?.render
  const review = artifact.media?.review

  if (!primary?.public_media_url) return undefined
  if (artifact.type !== "species-page") return undefined
  if (!render || render.strategy !== "approved_primary_image") return undefined
  if (render.public_visual_kind !== "image") return undefined
  if (render.public_visual_public_use !== true) return undefined
  if (review?.primary_status !== "approved") return undefined
  if (primary.qa_status !== "approved") return undefined
  if (render.candidate_public_use === true) return undefined

  return {
    assetId: cleanText(primary.asset_id),
    imageUrl: primary.public_media_url,
    sourceUrl: cleanText(primary.source_url),
    originalMediaUrl: cleanText(primary.original_media_url),
    creator: cleanText(primary.creator),
    credit: cleanText(primary.credit),
    license: cleanText(primary.license),
    licenseUrl: cleanText(primary.license_url),
    rightsStatus: cleanText(primary.rights_status),
    altText:
      cleanText(primary.alt_text) ??
      `Approved primary species image for ${artifact.title}.`,
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
