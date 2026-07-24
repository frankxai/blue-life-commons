import type { Metadata } from "next"
import { notFound } from "next/navigation"
import {
  getArtifactByHref,
  getArtifactRobots,
  getArtifactsByType,
  getRelatedArtifacts,
} from "@/lib/content"
import { ArtifactDetail } from "@/components/artifact-detail"

export function generateStaticParams() {
  return [
    ...getArtifactsByType("research-summary"),
    ...getArtifactsByType("dataset-card"),
  ].map((a) => ({ slug: a.slug }))
}

export async function generateMetadata({
  params,
}: {
  params: Promise<{ slug: string }>
}): Promise<Metadata> {
  const { slug } = await params
  const artifact = getArtifactByHref(`/research/${slug}`)
  if (!artifact) return {}
  return {
    title: artifact.title,
    description: artifact.excerpt,
    robots: getArtifactRobots(artifact),
  }
}

export default async function ResearchDetailPage({
  params,
}: {
  params: Promise<{ slug: string }>
}) {
  const { slug } = await params
  const artifact = getArtifactByHref(`/research/${slug}`)
  if (!artifact) notFound()

  return (
    <main>
      <ArtifactDetail
        artifact={artifact}
        trail={[
          { label: "Research & datasets", href: "/research" },
          { label: artifact.title },
        ]}
        related={getRelatedArtifacts(artifact)}
      />
    </main>
  )
}
