import type { Metadata } from "next"
import { getArtifactsByType } from "@/lib/content"
import { Container, SectionHeading } from "@/components/primitives"
import { ArtifactCard } from "@/components/artifact-card"

export const metadata: Metadata = {
  title: "Field Missions",
  description:
    "Review-gated citizen-science mission drafts with visible science and ethics state.",
}

export default function MissionsIndexPage() {
  const missions = getArtifactsByType("field-mission")

  return (
    <main>
      <div className="border-b border-border bg-secondary">
        <Container className="py-14 sm:py-20">
          <SectionHeading
            eyebrow="Field missions"
            title="Mission protocols, held until ethics review clears"
            description="Draft missions remain visible for source and review inspection. The public site withholds operational wildlife guidance until ethics approval. When a reviewed mission names a citizen-science platform, submit directly under that platform's terms; Blue Life Commons does not route or credit observations."
          />
        </Container>
      </div>
      <Container className="py-12 sm:py-16">
        <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {missions.map((a) => (
            <ArtifactCard key={a.id} artifact={a} />
          ))}
        </div>
        <div className="mt-12 rounded-2xl border border-border bg-card p-8">
          <h2 className="font-serif text-xl font-semibold text-foreground">
            Want a mission near you?
          </h2>
          <p className="mt-2 max-w-2xl text-sm leading-relaxed text-muted-foreground">
            Missions begin as public GitHub proposals. If a coast, reef, or bay
            lacks a protocol, open an issue with the place, intended observation,
            and source material. Reviewers decide whether it can proceed.
          </p>
          <a
            href="https://github.com/frankxai/blue-life-commons/blob/main/CONTRIBUTING.md"
            target="_blank"
            rel="noopener noreferrer"
            className="mt-4 inline-flex items-center gap-2 text-sm font-semibold text-primary hover:underline"
          >
            Propose a mission on GitHub
          </a>
        </div>
      </Container>
    </main>
  )
}
