import type { Metadata } from "next"
import { getArtifactsByType } from "@/lib/content"
import { Container, SectionHeading } from "@/components/primitives"
import { ArtifactCard } from "@/components/artifact-card"

export const metadata: Metadata = {
  title: "Field Missions",
  description:
    "Structured citizen-science missions with ethics review built in — observe ocean life, follow welfare-first protocols, feed real datasets.",
}

export default function MissionsIndexPage() {
  const missions = getArtifactsByType("field-mission")

  return (
    <main>
      <div className="border-b border-border bg-secondary">
        <Container className="py-14 sm:py-20">
          <SectionHeading
            eyebrow="Field missions"
            title="Citizen science with ethics built in"
            description="Every mission carries an ethics review, welfare-first observation protocols, and a defined data destination. Your observations feed OBIS, iNaturalist and partner datasets — credited to you."
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
            Missions are proposed and reviewed in the open on GitHub. If your
            coast, reef or bay needs a structured observation protocol, propose
            one — the community and ethics reviewers will help you shape it.
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
