import Link from "next/link"
import { ArrowRight, ButtonLink, Container } from "@/components/primitives"
import { getArtifactsByType, getGuildForArtifact } from "@/lib/content"
import { getApprovedSpeciesMedia } from "@/lib/media"

export function DeepTimeHomeStrip() {
  const deepTime = getArtifactsByType("species-page").filter(
    (a) => getGuildForArtifact(a) === "marine-reptiles",
  )
  const withMedia = deepTime
    .map((artifact) => ({
      artifact,
      media: getApprovedSpeciesMedia(artifact),
    }))
    .filter((e) => e.media)
  const flagship =
    withMedia.find((e) => e.artifact.id === "species-mosasaurus-hoffmannii") ??
    withMedia[0]

  if (!flagship?.media) return null

  return (
    <section className="border-t border-border bg-abyss text-abyss-foreground">
      <Container className="grid items-center gap-10 py-16 sm:py-20 lg:grid-cols-[minmax(0,1fr)_minmax(280px,420px)]">
        <div>
          <p className="text-xs font-semibold uppercase tracking-[0.16em] text-glow">
            Special section · Deep Time
          </p>
          <h2 className="mt-3 max-w-xl text-balance font-serif text-3xl font-semibold leading-tight sm:text-4xl">
            From living oceans to Mesozoic seas
          </h2>
          <p className="mt-4 max-w-xl text-pretty leading-relaxed text-abyss-muted">
            Popular culture says “ocean dinosaurs.” The science says{" "}
            <strong className="text-abyss-foreground">marine reptiles</strong>.
            Explore {deepTime.length} sourced deep-time entries that reuse the
            same encyclopedia UX as living species — with concept reconstruction
            media clearly labeled.
          </p>
          <div className="mt-8 flex flex-wrap gap-3">
            <ButtonLink href="/species/deep-time" variant="onDark">
              Open Deep Time hub
              <ArrowRight />
            </ButtonLink>
            <ButtonLink href="/species#marine-reptiles" variant="onDarkGhost">
              Guild in encyclopedia
            </ButtonLink>
          </div>
        </div>

        <Link
          href={flagship.artifact.href}
          className="group overflow-hidden rounded-2xl border border-abyss-border bg-abyss-deep shadow-2xl shadow-black/30"
        >
          <div className="aspect-video bg-abyss-deep">
            {flagship.media.videoUrl ? (
              <video
                className="h-full w-full object-cover transition-transform duration-500 group-hover:scale-[1.02]"
                autoPlay
                muted
                loop
                playsInline
                poster={flagship.media.imageUrl}
                aria-label={flagship.media.altText}
              >
                <source src={flagship.media.videoUrl} type="video/mp4" />
              </video>
            ) : (
              // eslint-disable-next-line @next/next/no-img-element
              <img
                src={flagship.media.imageUrl}
                alt={flagship.media.altText}
                className="h-full w-full object-cover transition-transform duration-500 group-hover:scale-[1.02]"
              />
            )}
          </div>
          <div className="border-t border-abyss-border p-4">
            <p className="text-xs font-semibold uppercase tracking-[0.12em] text-glow">
              Flagship reconstruction
            </p>
            <p className="mt-1 font-serif text-xl font-semibold text-abyss-foreground">
              {flagship.artifact.title}
            </p>
          </div>
        </Link>
      </Container>
    </section>
  )
}
