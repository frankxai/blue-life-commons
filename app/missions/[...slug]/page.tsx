import type { Metadata } from "next"
import { notFound } from "next/navigation"
import {
  getArtifactByHref,
  getArtifactsByType,
  getRelatedArtifacts,
} from "@/lib/content"
import { ArtifactDetail } from "@/components/artifact-detail"

export function generateStaticParams() {
  return getArtifactsByType("field-mission").map((a) => ({
    slug: a.href.split("/").filter(Boolean).slice(1),
  }))
}

export async function generateMetadata({
  params,
}: {
  params: Promise<{ slug: string[] }>
}): Promise<Metadata> {
  const { slug } = await params
  const artifact = getArtifactByHref(`/missions/${slug.join("/")}`)
  if (!artifact) return {}
  return { title: artifact.title, description: artifact.excerpt }
}

export default async function MissionDetailPage({
  params,
}: {
  params: Promise<{ slug: string[] }>
}) {
  const { slug } = await params
  const artifact = getArtifactByHref(`/missions/${slug.join("/")}`)
  if (!artifact) notFound()

  return (
    <main>
      <ArtifactDetail
        artifact={artifact}
        trail={[{ label: "Missions", href: "/missions" }, { label: artifact.title }]}
        related={getRelatedArtifacts(artifact)}
      />
    </main>
  )
}
