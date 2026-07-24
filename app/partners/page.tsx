import type { Metadata } from "next"
import { getArtifactsByType } from "@/lib/content"
import { Container, SectionHeading } from "@/components/primitives"
import { ArtifactCard } from "@/components/artifact-card"

export const metadata: Metadata = {
  title: "Ocean Organization Profiles",
  description:
    "Independent, source-linked profiles of ocean organizations. Inclusion does not imply partnership, endorsement, or affiliation.",
}

export default function PartnersPage() {
  const partners = getArtifactsByType("partner-profile")

  return (
    <main>
      <div className="border-b border-border bg-secondary">
        <Container className="py-14 sm:py-20">
          <SectionHeading
            eyebrow="Organization directory"
            title="Organizations doing the work on the water"
            description="These independent profiles summarize public information about conservation organizations and their programs. Inclusion does not imply partnership, endorsement, affiliation, or a data-sharing relationship."
          />
        </Container>
      </div>
      <Container className="py-12 sm:py-16">
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {partners.map((a) => (
            <ArtifactCard key={a.id} artifact={a} />
          ))}
        </div>
        <div className="mt-12 rounded-2xl border border-border bg-card p-8">
          <h2 className="font-serif text-xl font-semibold text-foreground">
            Add or correct an organization profile
          </h2>
          <p className="mt-2 max-w-2xl text-sm leading-relaxed text-muted-foreground">
            If your organization protects ocean life and wants its public work
            represented accurately, open a sourced profile PR or correction.
            Formal relationships are described only after they are documented.
          </p>
        </div>
      </Container>
    </main>
  )
}
