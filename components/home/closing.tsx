import Image from "next/image"
import { ButtonLink, ArrowRight, Container } from "@/components/primitives"

export function GuardianPreview() {
  return (
    <section className="py-20 sm:py-28">
      <Container>
        <div className="grid items-center gap-10 overflow-hidden rounded-3xl border border-border bg-abyss text-abyss-foreground lg:grid-cols-2">
          <div className="p-8 sm:p-12">
            <span className="text-xs font-semibold uppercase tracking-[0.16em] text-glow">
              Guardian signals
            </span>
            <h2 className="mt-4 text-balance font-serif text-3xl font-semibold leading-tight">
              The commons, watching in real time
            </h2>
            <p className="mt-4 text-pretty leading-relaxed text-abyss-muted">
              Guardian layers live public data over source-linked records whose
              review state remains visible — biodiversity occurrence records
              from OBIS and GBIF, the same open sources the Ocean Intelligence
              System watches. Facts appear only when the source responds.
            </p>
            <div className="mt-8">
              <ButtonLink href="/guardian" variant="onDark">
                Open the Guardian dashboard
                <ArrowRight />
              </ButtonLink>
            </div>
          </div>
          <div className="relative min-h-64 lg:h-full">
            <Image
              src="/images/reef-signal.png"
              alt="Coral reef transitioning from healthy to bleached, monitored by satellite"
              fill
              sizes="(max-width: 1024px) 100vw, 50vw"
              className="object-cover"
            />
            <div
              className="absolute inset-0 bg-gradient-to-r from-abyss/60 to-transparent lg:from-abyss/40"
              aria-hidden
            />
          </div>
        </div>
      </Container>
    </section>
  )
}

export function ClosingCta() {
  return (
    <section className="bg-abyss-deep py-20 text-abyss-foreground abyss-grid sm:py-28">
      <Container>
        <div className="mx-auto max-w-2xl text-center">
          <h2 className="text-balance font-serif text-3xl font-semibold leading-tight sm:text-4xl">
            Turn ocean curiosity into evidence the world can trust.
          </h2>
          <p className="mx-auto mt-5 max-w-xl text-pretty leading-relaxed text-abyss-muted">
            Whether you observe, research, teach, fund or build — there is a place
            for you in the commons. Everything you add stays open and credited.
          </p>
          <div className="mt-9 flex flex-wrap justify-center gap-3">
            <ButtonLink href="/contribute" variant="onDark">
              Find your pathway
              <ArrowRight />
            </ButtonLink>
            <ButtonLink href="/support" variant="onDarkGhost">
              Sustain the commons
            </ButtonLink>
          </div>
        </div>
      </Container>
    </section>
  )
}
