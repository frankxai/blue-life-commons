import type { Metadata } from "next"
import { getArtifactsByType } from "@/lib/content"
import { Container, SectionHeading } from "@/components/primitives"
import { ArtifactCard } from "@/components/artifact-card"

export const metadata: Metadata = {
  title: "Region Briefings",
  description:
    "Deep briefings on the ocean regions where life concentrates — ecology, threats, protections and the species that depend on them.",
}

export default function RegionsIndexPage() {
  const regions = getArtifactsByType("region-briefing")

  return (
    <main>
      <div className="border-b border-border bg-secondary">
        <Container className="py-14 sm:py-20">
          <SectionHeading
            eyebrow="Region briefings"
            title="The places where ocean life concentrates"
            description={`${regions.length} region briefings covering marine protected areas, migration corridors and biodiversity hotspots — each with cited ecology, threats and protection status.`}
          />
        </Container>
      </div>
      <Container className="py-12 sm:py-16">
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {regions.map((a) => (
            <ArtifactCard key={a.id} artifact={a} />
          ))}
        </div>
      </Container>
    </main>
  )
}
