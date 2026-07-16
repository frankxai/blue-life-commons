import Link from "next/link"
import { Chip, IucnBadge } from "@/components/badges"
import { Container, ArrowRight } from "@/components/primitives"
import {
  getArtifactsByType,
  getGuildForArtifact,
} from "@/lib/content"
import { getApprovedSpeciesMedia } from "@/lib/media"
import { GUILD_META } from "@/lib/utils"

const LIVING_BRIDGES = [
  {
    href: "/species/sharks-rays/great-white-shark",
    label: "Great white shark",
    note: "Living apex predator — compare with mosasaurs & pliosaurs",
  },
  {
    href: "/species/cetaceans/blue-whale",
    label: "Blue whale",
    note: "Largest living animal — deep-time scale context",
  },
  {
    href: "/species/sharks-rays/whale-shark",
    label: "Whale shark",
    note: "Gentle giant of living seas",
  },
  {
    href: "/species/turtles/leatherback-turtle",
    label: "Leatherback turtle",
    note: "Living marine reptile lineage still in the water",
  },
] as const

export function DeepTimeHub() {
  const entries = getArtifactsByType("species-page")
    .filter((a) => getGuildForArtifact(a) === "marine-reptiles")
    .map((artifact) => ({
      artifact,
      media: getApprovedSpeciesMedia(artifact),
    }))

  const flagship =
    entries.find((e) => e.artifact.id === "species-mosasaurus-hoffmannii") ??
    entries[0]

  return (
    <main>
      <section className="relative overflow-hidden bg-abyss text-abyss-foreground">
        <div className="absolute inset-0">
          {flagship?.media?.videoUrl ? (
            <video
              className="h-full w-full object-cover opacity-45"
              autoPlay
              muted
              loop
              playsInline
              poster={flagship.media.imageUrl}
              aria-hidden
            >
              <source src={flagship.media.videoUrl} type="video/mp4" />
            </video>
          ) : flagship?.media?.imageUrl ? (
            // eslint-disable-next-line @next/next/no-img-element
            <img
              src={flagship.media.imageUrl}
              alt=""
              className="h-full w-full object-cover opacity-45"
              aria-hidden
            />
          ) : null}
          <div className="absolute inset-0 bg-gradient-to-r from-abyss via-abyss/90 to-abyss/55" />
          <div className="absolute inset-0 abyss-grid opacity-20" aria-hidden />
        </div>

        <Container className="relative py-16 sm:py-24">
          <p className="text-xs font-semibold uppercase tracking-[0.16em] text-glow">
            Special section · Deep Time
          </p>
          <h1 className="mt-4 max-w-3xl text-balance font-serif text-4xl font-semibold leading-tight sm:text-5xl lg:text-6xl">
            Ocean “dinosaurs” — actually marine reptiles
          </h1>
          <p className="mt-5 max-w-2xl text-base leading-relaxed text-abyss-muted sm:text-lg">
            Mosasaurs, plesiosaurs, pliosaurs, and ichthyosaurs ruled Mesozoic
            seas. They are <strong className="text-abyss-foreground">not dinosaurs</strong>.
            This educational bridge reuses the Blue Life Commons species page
            pattern — sources, review state, and concept-reconstruction media
            labels — so deep-time curiosity stays accurate.
          </p>
          <div className="mt-8 flex flex-wrap gap-3">
            <Link
              href="#entries"
              className="inline-flex items-center gap-2 rounded-full bg-glow px-5 py-2.5 text-sm font-semibold text-abyss-deep transition-transform hover:-translate-y-0.5"
            >
              Browse deep-time entries
              <ArrowRight className="h-4 w-4" />
            </Link>
            <Link
              href="/species"
              className="inline-flex items-center gap-2 rounded-full border border-abyss-border bg-white/5 px-5 py-2.5 text-sm font-semibold text-abyss-foreground transition-colors hover:border-glow hover:text-glow"
            >
              Living ocean encyclopedia
            </Link>
            <Link
              href="https://github.com/frankxai/dino-life-commons"
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center gap-2 rounded-full border border-abyss-border bg-white/5 px-5 py-2.5 text-sm font-semibold text-abyss-foreground transition-colors hover:border-glow hover:text-glow"
            >
              Terrestrial dinosaurs (sibling)
            </Link>
          </div>
          <dl className="mt-10 grid max-w-xl grid-cols-3 gap-4">
            <div>
              <dd className="font-serif text-3xl font-semibold text-glow">
                {entries.length}
              </dd>
              <dt className="mt-1 text-xs text-abyss-muted">Entries</dt>
            </div>
            <div>
              <dd className="font-serif text-3xl font-semibold text-glow">
                {entries.filter((e) => e.media).length}
              </dd>
              <dt className="mt-1 text-xs text-abyss-muted">Hero stills</dt>
            </div>
            <div>
              <dd className="font-serif text-3xl font-semibold text-glow">
                {entries.filter((e) => e.media?.videoUrl).length}
              </dd>
              <dt className="mt-1 text-xs text-abyss-muted">Video loops</dt>
            </div>
          </dl>
        </Container>
      </section>

      <section className="border-b border-border bg-secondary">
        <Container className="py-8">
          <div className="grid gap-6 lg:grid-cols-3">
            {[
              {
                title: "Not dinosaurs",
                body: "Dinosauria was overwhelmingly terrestrial. Mesozoic ocean apex roles were filled by marine reptiles.",
              },
              {
                title: "Same UI contract",
                body: "Guild pages, species cards, provenance rails, and review chips reuse the living-species encyclopedia UX.",
              },
              {
                title: "Concept media only",
                body: "AI stills and loops are labeled reconstructions — never fossil evidence or soft-tissue proof.",
              },
            ].map((card) => (
              <div
                key={card.title}
                className="rounded-2xl border border-border bg-card p-5"
              >
                <h2 className="font-serif text-xl font-semibold text-foreground">
                  {card.title}
                </h2>
                <p className="mt-2 text-sm leading-relaxed text-muted-foreground">
                  {card.body}
                </p>
              </div>
            ))}
          </div>
        </Container>
      </section>

      <section id="entries" className="scroll-mt-24">
      <Container className="py-12 sm:py-16">
        <div className="flex flex-col gap-3 sm:flex-row sm:items-end sm:justify-between">
          <div>
            <p className="text-xs font-semibold uppercase tracking-[0.14em] text-primary">
              {GUILD_META["marine-reptiles"]?.label}
            </p>
            <h2 className="mt-2 font-serif text-3xl font-semibold text-foreground">
              Species entries
            </h2>
            <p className="mt-2 max-w-2xl text-sm text-muted-foreground">
              {GUILD_META["marine-reptiles"]?.special}
            </p>
          </div>
          <Link
            href="/species#marine-reptiles"
            className="text-sm font-semibold text-primary hover:underline"
          >
            View inside full encyclopedia
          </Link>
        </div>

        <div className="mt-8 grid gap-5 sm:grid-cols-2 xl:grid-cols-3">
          {entries.map(({ artifact, media }) => (
            <article
              key={artifact.id}
              className="group flex h-full flex-col overflow-hidden rounded-xl border border-border bg-card transition-all duration-300 hover:-translate-y-1 hover:border-primary/40 hover:shadow-[var(--shadow-elevated)]"
            >
              <Link href={artifact.href} className="block bg-muted">
                <div className="aspect-[16/10] bg-abyss-deep">
                  {media?.videoUrl ? (
                    <video
                      className="h-full w-full object-cover"
                      autoPlay
                      muted
                      loop
                      playsInline
                      poster={media.imageUrl}
                      aria-label={media.altText}
                    >
                      <source src={media.videoUrl} type="video/mp4" />
                    </video>
                  ) : media ? (
                    // eslint-disable-next-line @next/next/no-img-element
                    <img
                      src={media.imageUrl}
                      alt={media.altText}
                      loading="lazy"
                      className="h-full w-full object-cover transition-transform duration-300 group-hover:scale-[1.015]"
                    />
                  ) : (
                    <div className="flex h-full items-center justify-center px-4 text-center text-sm text-muted-foreground">
                      Media pending
                    </div>
                  )}
                </div>
              </Link>
              <div className="flex flex-1 flex-col p-5">
                <div className="flex flex-wrap items-center gap-2">
                  <Chip tone="primary">Deep Time</Chip>
                  <IucnBadge category={artifact.iucn?.category} size="sm" />
                  {media?.conceptReconstruction && (
                    <Chip tone="accent">Concept art</Chip>
                  )}
                </div>
                <h3 className="mt-4 font-serif text-xl font-semibold leading-snug text-foreground group-hover:text-primary">
                  <Link href={artifact.href}>{artifact.title}</Link>
                </h3>
                {artifact.excerpt && (
                  <p className="mt-2 line-clamp-3 text-sm leading-relaxed text-muted-foreground">
                    {artifact.excerpt}
                  </p>
                )}
                <Link
                  href={artifact.href}
                  className="mt-auto pt-5 text-sm font-semibold text-primary hover:underline"
                >
                  Open entry
                </Link>
              </div>
            </article>
          ))}
        </div>
      </Container>
      </section>

      <section className="border-t border-border bg-paper">
        <Container className="py-12 sm:py-16">
          <h2 className="font-serif text-3xl font-semibold text-foreground">
            Bridge to living seas
          </h2>
          <p className="mt-3 max-w-2xl text-sm leading-relaxed text-muted-foreground sm:text-base">
            Deep Time is not a silo. Use these living records to compare body
            plans, ecological roles, and why accurate ocean literacy matters now.
          </p>
          <div className="mt-8 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
            {LIVING_BRIDGES.map((item) => (
              <Link
                key={item.href}
                href={item.href}
                className="rounded-2xl border border-border bg-card p-5 transition-colors hover:border-primary/40"
              >
                <p className="font-semibold text-foreground">{item.label}</p>
                <p className="mt-2 text-sm leading-relaxed text-muted-foreground">
                  {item.note}
                </p>
              </Link>
            ))}
          </div>
        </Container>
      </section>
    </main>
  )
}
