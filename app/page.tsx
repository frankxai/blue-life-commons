import { HomeHero } from "@/components/home/hero"
import { ModelSection } from "@/components/home/model-section"
import { Featured } from "@/components/home/featured"
import { Principles } from "@/components/home/principles"
import { GuardianPreview, ClosingCta } from "@/components/home/closing"
import { getAllArtifacts, getCommonsStats } from "@/lib/content"
import { getApprovedSpeciesMedia } from "@/lib/media"

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

  // Featured: prefer species with an IUCN status, then a mix of types.
  const species = all.filter((a) => a.type === "species-page" && a.iucn?.category)
  const others = all.filter(
    (a) => a.type === "region-briefing" || a.type === "field-mission",
  )
  const featured = [...species.slice(0, 4), ...others.slice(0, 2)].slice(0, 6)

  return (
    <>
      <HomeHero stats={stats} proof={proof} />
      <ModelSection />
      <Featured artifacts={featured} />
      <Principles />
      <GuardianPreview />
      <ClosingCta />
    </>
  )
}
