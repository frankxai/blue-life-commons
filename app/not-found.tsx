import { Container, ButtonLink, ArrowRight } from "@/components/primitives"

export default function NotFound() {
  return (
    <div className="bg-abyss">
      <Container className="flex min-h-[60vh] flex-col items-center justify-center gap-6 py-24 text-center">
        <span className="text-xs font-semibold uppercase tracking-[0.2em] text-glow">
          Uncharted waters
        </span>
        <h1 className="max-w-xl text-balance font-serif text-4xl font-semibold leading-tight text-abyss-foreground sm:text-5xl">
          This part of the ocean has not been mapped yet
        </h1>
        <p className="max-w-md text-pretty text-base leading-relaxed text-abyss-muted">
          The page you are looking for does not exist — or has not been
          contributed to the commons yet. Perhaps you will be the one to add
          it.
        </p>
        <div className="flex flex-wrap items-center justify-center gap-3">
          <ButtonLink href="/catalog" variant="onDark">
            Browse the catalog
            <ArrowRight />
          </ButtonLink>
          <ButtonLink href="/contribute" variant="onDarkGhost">
            Contribute a page
          </ButtonLink>
        </div>
      </Container>
    </div>
  )
}
