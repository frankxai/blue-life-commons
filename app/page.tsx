import type { Metadata } from "next"
import { HomeHero } from "@/components/home/hero"
import { ModelSection } from "@/components/home/model-section"
import { DeepTimeHomeStrip } from "@/components/home/deep-time-strip"
import { Featured } from "@/components/home/featured"
import { Principles } from "@/components/home/principles"
import { GuardianPreview, ClosingCta } from "@/components/home/closing"
import {
  getAllArtifacts,
  getCommonsStats,
  getGuildForArtifact,
} from "@/lib/content"
import { getApprovedSpeciesMedia } from "@/lib/media"

export const metadata: Metadata = {
  alternates: { canonical: "/" },
  openGraph: { url: "/" },
}

export default function HomePage() {
  const stats = getCommonsStats()
  const all = getAllArtifacts()
  const whaleShark = all.find((artifact) => artifact.id === "species-whale-shark")
  const whaleSharkMedia = whaleShark
    ? getApprovedSpeciesMedia(whaleShark)
    : undefined
  const proof =
    whaleShark && whaleSharkMedia
      ? {
          title: whaleShark.title,
          href: whaleShark.href,
          githubPath: whaleShark.githubPath,
          status: whaleShark.status ?? "needs-expert-review",
          review: whaleShark.review,
          sourceCount: whaleShark.sources.length,
          imageUrl: whaleSharkMedia.imageUrl,
          sourceUrl: whaleSharkMedia.sourceUrl,
          creator: whaleSharkMedia.creator,
          license: whaleSharkMedia.license,
          licenseUrl: whaleSharkMedia.licenseUrl,
          altText: whaleSharkMedia.altText,
          mediaChecks: whaleShark.media?.review?.checks_complete ?? 0,
          mediaChecksTotal: whaleShark.media?.review?.checks_total ?? 0,
        }
      : undefined

  // Featured: mix living species with one deep-time bridge entry.
  const livingSpecies = all.filter(
    (a) =>
      a.type === "species-page" &&
      a.iucn?.category &&
      getGuildForArtifact(a) !== "marine-reptiles",
  )
  const deepTime = all.find((a) => a.id === "species-mosasaurus-hoffmannii")
  const others = all.filter(
    (a) => a.type === "region-briefing" || a.type === "field-mission",
  )
  const featured = [
    ...livingSpecies.slice(0, 3),
    ...(deepTime ? [deepTime] : []),
    ...others.slice(0, 2),
  ].slice(0, 6)

  return (
    <>
      <HomeHero stats={stats} proof={proof} />
      <ModelSection />
      <DeepTimeHomeStrip />
      <Featured artifacts={featured} />
      <Principles />
      <GuardianPreview />
      <ClosingCta />
    </>
  )
}
