import type { Metadata } from "next"
import { getArtifactsByType, getGuildForArtifact } from "@/lib/content"
import { Container, SectionHeading } from "@/components/primitives"
import { ArtifactCard } from "@/components/artifact-card"
import { GUILD_META } from "@/lib/utils"

export const metadata: Metadata = {
  title: "Species Intelligence",
  description:
    "Cited, ethics-reviewed intelligence pages for ocean species — cetaceans, sharks and rays, sea turtles, pinnipeds, reef builders and more.",
}

export default function SpeciesIndexPage() {
  const species = getArtifactsByType("species-page")
  const byGuild = new Map<string, typeof species>()
  for (const s of species) {
    const guild = getGuildForArtifact(s)
    const list = byGuild.get(guild) ?? []
    list.push(s)
    byGuild.set(guild, list)
  }
  const guilds = [...byGuild.entries()].sort((a, b) => b[1].length - a[1].length)

  return (
    <main>
      <div className="border-b border-border bg-secondary">
        <Container className="py-14 sm:py-20">
          <SectionHeading
            eyebrow="Species intelligence"
            title="Every page grounded in sources, or silent"
            description={`${species.length} species intelligence pages, each citing IUCN assessments, peer-reviewed research and institutional data. Organized by guild.`}
          />
          <nav aria-label="Guilds" className="mt-8 flex flex-wrap gap-2">
            {guilds.map(([guild, list]) => (
              <a
                key={guild}
                href={`#${guild}`}
                className="rounded-full border border-border bg-card px-4 py-2 text-sm font-medium text-foreground transition-colors hover:border-primary/40 hover:text-primary"
              >
                {GUILD_META[guild]?.label ?? guild}
                <span className="ml-2 text-muted-foreground">{list.length}</span>
              </a>
            ))}
          </nav>
        </Container>
      </div>

      <Container className="py-12 sm:py-16">
        <div className="flex flex-col gap-16">
          {guilds.map(([guild, list]) => (
            <section key={guild} id={guild} aria-labelledby={`${guild}-heading`} className="scroll-mt-24">
              <div className="flex items-baseline justify-between gap-4">
                <h2
                  id={`${guild}-heading`}
                  className="font-serif text-2xl font-semibold text-foreground"
                >
                  {GUILD_META[guild]?.label ?? guild}
                </h2>
                <span className="text-sm text-muted-foreground">
                  {list.length} {list.length === 1 ? "page" : "pages"}
                </span>
              </div>
              <div className="mt-6 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
                {list.map((a) => (
                  <ArtifactCard key={a.id} artifact={a} />
                ))}
              </div>
            </section>
          ))}
        </div>
      </Container>
    </main>
  )
}
