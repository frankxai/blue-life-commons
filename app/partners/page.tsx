import type { Metadata } from "next"
import { getArtifactsByType } from "@/lib/content"
import { Container, SectionHeading } from "@/components/primitives"
import { ArtifactCard } from "@/components/artifact-card"

export const metadata: Metadata = {
  title: "Partners",
  description:
    "The NGOs, research programs and community organizations whose work the commons documents, links and supports.",
}

export default function PartnersPage() {
  const partners = getArtifactsByType("partner-profile")

  return (
    <main>
      <div className="border-b border-border bg-secondary">
        <Container className="py-14 sm:py-20">
          <SectionHeading
            eyebrow="Partners"
            title="Organizations doing the work on the water"
            description="Partner profiles document real conservation organizations — what they do, where they operate, and how the commons' knowledge and missions connect to their programs."
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
            Partner with the commons
          </h2>
          <p className="mt-2 max-w-2xl text-sm leading-relaxed text-muted-foreground">
            If your organization protects ocean life and wants its work
            represented accurately — or wants an intelligence system of its own —
            open a profile PR or reach out through the ecosystem page.
          </p>
        </div>
      </Container>
    </main>
  )
}
