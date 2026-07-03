import type { Metadata } from "next"
import { getArtifactsByType } from "@/lib/content"
import { Container, SectionHeading } from "@/components/primitives"
import { ArtifactCard } from "@/components/artifact-card"

export const metadata: Metadata = {
  title: "Research & Datasets",
  description:
    "Plain-language research summaries and dataset cards for the open ocean data the commons builds on — OBIS, GBIF, Coral Reef Watch and more.",
}

export default function ResearchIndexPage() {
  const research = getArtifactsByType("research-summary")
  const datasets = getArtifactsByType("dataset-card")

  return (
    <main>
      <div className="border-b border-border bg-secondary">
        <Container className="py-14 sm:py-20">
          <SectionHeading
            eyebrow="Research & datasets"
            title="The evidence layer, explained plainly"
            description="Research summaries translate peer-reviewed science into accessible language without losing precision. Dataset cards document the open data sources every artifact builds on."
          />
        </Container>
      </div>

      <Container className="py-12 sm:py-16">
        <section aria-labelledby="research-heading">
          <h2 id="research-heading" className="font-serif text-2xl font-semibold text-foreground">
            Research summaries
          </h2>
          <div className="mt-6 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
            {research.map((a) => (
              <ArtifactCard key={a.id} artifact={a} />
            ))}
          </div>
        </section>

        <section aria-labelledby="datasets-heading" className="mt-16">
          <h2 id="datasets-heading" className="font-serif text-2xl font-semibold text-foreground">
            Dataset cards
          </h2>
          <p className="mt-2 max-w-2xl text-sm leading-relaxed text-muted-foreground">
            The open datasets that power the commons and the Ocean Intelligence
            System connectors — what they contain, how they are licensed, and how
            to use them well.
          </p>
          <div className="mt-6 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
            {datasets.map((a) => (
              <ArtifactCard key={a.id} artifact={a} />
            ))}
          </div>
        </section>
      </Container>
    </main>
  )
}
