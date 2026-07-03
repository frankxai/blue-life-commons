import Image from "next/image"
import { ButtonLink, ArrowRight, Container } from "@/components/primitives"
import type { CommonsStats } from "@/lib/types"

export function HomeHero({ stats }: { stats: CommonsStats }) {
  return (
    <section className="relative isolate overflow-hidden bg-abyss-deep text-abyss-foreground">
      <Image
        src="/images/hero-ocean.png"
        alt=""
        fill
        priority
        sizes="100vw"
        className="object-cover opacity-55"
      />
      <div
        className="absolute inset-0 bg-gradient-to-b from-abyss-deep/70 via-abyss-deep/60 to-abyss-deep"
        aria-hidden
      />
      <div className="absolute inset-0 abyss-grid opacity-30" aria-hidden />

      <Container className="relative py-24 sm:py-32 lg:py-40">
        <div className="max-w-3xl">
          <span className="inline-flex items-center gap-2 rounded-full border border-abyss-border bg-white/5 px-3 py-1.5 text-xs font-medium text-glow backdrop-blur-sm">
            <span className="size-1.5 rounded-full bg-glow signal-dot" aria-hidden />
            Open · Sourced · Ethics-reviewed
          </span>

          <h1 className="mt-6 text-balance font-serif text-4xl font-semibold leading-[1.05] tracking-tight sm:text-5xl lg:text-6xl">
            The open intelligence commons for ocean life.
          </h1>

          <p className="mt-6 max-w-2xl text-pretty text-lg leading-relaxed text-abyss-muted">
            Every species page, region briefing, field mission and dataset is
            cited, ethics-reviewed, and versioned on GitHub. We publish what the
            evidence decides — grounded in sources, or silent. Free for everyone,
            forever.
          </p>

          <div className="mt-9 flex flex-wrap items-center gap-3">
            <ButtonLink href="/species" variant="onDark">
              Explore species intelligence
              <ArrowRight />
            </ButtonLink>
            <ButtonLink href="/contribute" variant="onDarkGhost">
              Contribute an artifact
            </ButtonLink>
          </div>

          <dl className="mt-14 flex flex-wrap gap-x-10 gap-y-4">
            {[
              { value: stats.total, label: "Sourced artifacts" },
              { value: stats.species, label: "Species pages" },
              { value: stats.sources, label: "Cited sources" },
              { value: stats.regions, label: "Region briefings" },
            ].map((s) => (
              <div key={s.label}>
                <dd className="font-serif text-3xl font-semibold tabular-nums text-glow">
                  {s.value}
                </dd>
                <dt className="text-sm text-abyss-muted">{s.label}</dt>
              </div>
            ))}
          </dl>
        </div>
      </Container>
    </section>
  )
}
