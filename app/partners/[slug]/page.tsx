import type { Metadata } from "next"
import { notFound } from "next/navigation"
import {
  getArtifactByHref,
  getArtifactsByType,
  getRelatedArtifacts,
} from "@/lib/content"
import { ArtifactDetail } from "@/components/artifact-detail"

export function generateStaticParams() {
  return getArtifactsByType("partner-profile").map((a) => ({ slug: a.slug }))
}

export async function generateMetadata({
  params,
}: {
  params: Promise<{ slug: string }>
}): Promise<Metadata> {
  const { slug } = await params
  const artifact = getArtifactByHref(`/partners/${slug}`)
  if (!artifact) return {}
  return { title: artifact.title, description: artifact.excerpt }
}

export default async function PartnerDetailPage({
  params,
}: {
  params: Promise<{ slug: string }>
}) {
  const { slug } = await params
  const artifact = getArtifactByHref(`/partners/${slug}`)
  if (!artifact) notFound()

  return (
    <main>
      <ArtifactDetail
        artifact={artifact}
        trail={[{ label: "Partners", href: "/partners" }, { label: artifact.title }]}
        related={getRelatedArtifacts(artifact)}
      />
    </main>
  )
}
