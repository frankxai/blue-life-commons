import { HomeHero } from "@/components/home/hero"
import { ModelSection } from "@/components/home/model-section"
import { Featured } from "@/components/home/featured"
import { Principles } from "@/components/home/principles"
import { GuardianPreview, ClosingCta } from "@/components/home/closing"
import { getAllArtifacts, getCommonsStats } from "@/lib/content"

export default function HomePage() {
  const stats = getCommonsStats()
  const all = getAllArtifacts()

  // Featured: prefer species with an IUCN status, then a mix of types.
  const species = all.filter((a) => a.type === "species-page" && a.iucn?.category)
  const others = all.filter(
    (a) => a.type === "region-briefing" || a.type === "field-mission",
  )
  const featured = [...species.slice(0, 4), ...others.slice(0, 2)].slice(0, 6)

  return (
    <>
      <HomeHero stats={stats} />
      <ModelSection />
      <Featured artifacts={featured} />
      <Principles />
      <GuardianPreview />
      <ClosingCta />
    </>
  )
}
