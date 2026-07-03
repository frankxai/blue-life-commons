import { ArtifactCard } from "@/components/artifact-card"
import { ButtonLink, ArrowRight, Container, SectionHeading } from "@/components/primitives"
import type { Artifact } from "@/lib/types"

export function Featured({ artifacts }: { artifacts: Artifact[] }) {
  return (
    <section className="border-t border-border bg-paper py-20 sm:py-28">
      <Container>
        <div className="flex flex-wrap items-end justify-between gap-4">
          <SectionHeading
            eyebrow="From the commons"
            title="Recently sourced intelligence"
            description="A cross-section of the library — species pages, briefings and missions, each backed by cited evidence."
          />
          <ButtonLink href="/catalog" variant="ghost">
            Browse the full catalog
            <ArrowRight />
          </ButtonLink>
        </div>

        <div className="mt-12 grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
          {artifacts.map((a) => (
            <ArtifactCard key={a.id} artifact={a} />
          ))}
        </div>
      </Container>
    </section>
  )
}
