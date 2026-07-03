import type { Metadata } from "next"
import { notFound } from "next/navigation"
import {
  getArtifactByHref,
  getArtifactsByType,
  getRelatedArtifacts,
} from "@/lib/content"
import { ArtifactDetail } from "@/components/artifact-detail"
import { getApprovedSpeciesMedia } from "@/lib/media"
import { GUILD_META } from "@/lib/utils"

export function generateStaticParams() {
  return getArtifactsByType("species-page").map((a) => {
    const [, , guild, slug] = a.href.split("/")
    return { guild, slug }
  })
}

async function getArtifact(params: Promise<{ guild: string; slug: string }>) {
  const { guild, slug } = await params
  return getArtifactByHref(`/species/${guild}/${slug}`)
}

export async function generateMetadata({
  params,
}: {
  params: Promise<{ guild: string; slug: string }>
}): Promise<Metadata> {
  const artifact = await getArtifact(params)
  if (!artifact) return {}
  const media = getApprovedSpeciesMedia(artifact)
  return {
    title: artifact.title,
    description: artifact.excerpt,
    openGraph: media
      ? {
          images: [
            {
              url: media.imageUrl,
              alt: media.altText,
            },
          ],
        }
      : undefined,
  }
}

export default async function SpeciesDetailPage({
  params,
}: {
  params: Promise<{ guild: string; slug: string }>
}) {
  const { guild } = await params
  const artifact = await getArtifact(params)
  if (!artifact) notFound()

  return (
    <main>
      <ArtifactDetail
        artifact={artifact}
        trail={[
          { label: "Species", href: "/species" },
          { label: GUILD_META[guild]?.label ?? guild, href: `/species#${guild}` },
          { label: artifact.title },
        ]}
        related={getRelatedArtifacts(artifact)}
      />
    </main>
  )
}
