import type { Artifact } from "@/lib/types"
import type { ApprovedSpeciesMedia } from "@/lib/media"
import {
  getApprovedSpeciesMedia,
  getMediaCreditText,
  getUrlHost,
} from "@/lib/media"
import { cn } from "@/lib/utils"
import { HeroVideoPlayer } from "@/components/hero-video-player"

function MediaImage({
  media,
  loading,
  className,
  fit = "cover",
}: {
  media: ApprovedSpeciesMedia
  loading: "eager" | "lazy"
  className?: string
  fit?: "cover" | "contain"
}) {
  return (
    <img
      src={media.imageUrl}
      alt={media.altText}
      loading={loading}
      decoding="async"
      referrerPolicy="no-referrer"
      className={cn(
        "h-full w-full",
        fit === "cover" ? "object-cover" : "object-contain",
        className,
      )}
    />
  )
}

/** Full-bleed cinematic hero for species pages — large stage, 16:9 video/image. */
export function ArtifactCinematicHero({
  artifact,
  titleNode,
  metaNode,
}: {
  artifact: Artifact
  titleNode?: React.ReactNode
  metaNode?: React.ReactNode
}) {
  const media = getApprovedSpeciesMedia(artifact)
  if (!media) return null

  const isConcept = Boolean(media.conceptReconstruction)

  return (
    <figure className="relative overflow-hidden rounded-none border-b border-abyss-border bg-abyss-deep sm:rounded-3xl sm:border sm:shadow-[var(--shadow-elevated)]">
      {/* Mobile-first stage: shorter on phones, tall cinematic on desktop */}
      <div className="relative aspect-[16/11] min-h-[240px] max-h-[70dvh] w-full sm:aspect-[16/9] sm:min-h-[340px] sm:max-h-none lg:min-h-[420px] xl:min-h-[500px]">
        {media.videoUrl ? (
          <HeroVideoPlayer
            src={media.videoUrl}
            poster={media.imageUrl}
            ariaLabel={media.altText}
          />
        ) : (
          <MediaImage
            media={media}
            loading="eager"
            fit="cover"
            className="absolute inset-0"
          />
        )}
        <div
          className="pointer-events-none absolute inset-0 bg-gradient-to-t from-abyss-deep via-abyss-deep/40 to-transparent"
          aria-hidden
        />
        <div
          className="pointer-events-none absolute inset-0 bg-gradient-to-r from-abyss-deep/55 via-transparent to-transparent"
          aria-hidden
        />

        <figcaption className="absolute inset-x-0 bottom-0 p-4 sm:p-7 lg:p-9">
          <div className="flex flex-wrap items-center gap-2">
            <span className="rounded-full bg-glow px-2.5 py-1 text-[11px] font-semibold uppercase tracking-[0.12em] text-abyss-deep">
              {isConcept ? "Concept reconstruction" : "Approved primary image"}
            </span>
            {media.videoUrl && (
              <span className="rounded-full border border-white/20 bg-black/30 px-2.5 py-1 text-[11px] font-semibold uppercase tracking-[0.12em] text-white backdrop-blur-sm">
                Cinematic loop
              </span>
            )}
            {media.rightsStatus && (
              <span className="rounded-full border border-white/15 bg-black/25 px-2.5 py-1 text-[11px] font-medium capitalize text-white/85 backdrop-blur-sm">
                {media.rightsStatus.replace(/-/g, " ")}
              </span>
            )}
          </div>
          {titleNode}
          {metaNode}
          <p className="mt-2.5 max-w-3xl text-sm leading-relaxed text-white/80 sm:mt-3 sm:text-[15px]">
            {media.altText}
          </p>
          {isConcept && (
            <p className="mt-2 max-w-2xl text-xs leading-relaxed text-white/55">
              Generated educational art — not fossil evidence, identification
              media, or proof of soft-tissue color or behavior.
            </p>
          )}
        </figcaption>
      </div>
    </figure>
  )
}

/** Compact side card (legacy/supporting surfaces). */
export function ArtifactHeroMedia({ artifact }: { artifact: Artifact }) {
  const media = getApprovedSpeciesMedia(artifact)
  if (!media) return null

  const sourceHost = getUrlHost(media.sourceUrl)
  const originalHost = getUrlHost(media.originalMediaUrl)
  const isConcept = Boolean(media.conceptReconstruction)

  return (
    <figure className="overflow-hidden rounded-2xl border border-border bg-card shadow-[var(--shadow-elevated)]">
      <div className="relative aspect-[16/10] bg-abyss-deep">
        {media.videoUrl ? (
          <HeroVideoPlayer
            src={media.videoUrl}
            poster={media.imageUrl}
            ariaLabel={media.altText}
          />
        ) : (
          <MediaImage media={media} loading="eager" fit="cover" />
        )}
      </div>
      <figcaption className="border-t border-border p-4">
        <div className="flex flex-wrap items-center gap-2">
          <span className="rounded-full bg-primary/10 px-2.5 py-1 text-xs font-semibold text-primary">
            {isConcept ? "Concept reconstruction" : "Approved primary image"}
          </span>
          {media.videoUrl && (
            <span className="rounded-full bg-accent/15 px-2.5 py-1 text-xs font-semibold text-foreground">
              Cinematic loop
            </span>
          )}
        </div>
        <p className="mt-3 text-sm leading-relaxed text-foreground">
          {media.altText}
        </p>
        {isConcept && (
          <p className="mt-2 text-xs leading-relaxed text-muted-foreground">
            Generated educational art. Not fossil evidence or soft-tissue proof.
          </p>
        )}
        <div className="mt-3 flex flex-wrap gap-x-4 gap-y-1 text-xs font-medium">
          {media.sourceUrl && (
            <a
              href={media.sourceUrl}
              target="_blank"
              rel="noopener noreferrer"
              className="text-primary underline decoration-primary/40 underline-offset-2 hover:decoration-primary"
            >
              Source{sourceHost ? `: ${sourceHost}` : ""}
            </a>
          )}
          {media.originalMediaUrl && !media.originalMediaUrl.startsWith("/") && (
            <a
              href={media.originalMediaUrl}
              target="_blank"
              rel="noopener noreferrer"
              className="text-primary underline decoration-primary/40 underline-offset-2 hover:decoration-primary"
            >
              Original{originalHost ? `: ${originalHost}` : ""}
            </a>
          )}
        </div>
      </figcaption>
    </figure>
  )
}

export function ArtifactCardMedia({
  artifact,
  className,
}: {
  artifact: Artifact
  className?: string
}) {
  return (
    <MediaCardPreview
      media={getApprovedSpeciesMedia(artifact)}
      className={className}
    />
  )
}

export function MediaCardPreview({
  media,
  className,
}: {
  media?: ApprovedSpeciesMedia
  className?: string
}) {
  if (!media) return null

  const credit = getMediaCreditText(media)

  return (
    <div
      className={cn(
        "mt-4 overflow-hidden rounded-lg border border-border bg-muted",
        className,
      )}
    >
      <div className="aspect-[16/10] bg-muted">
        <MediaImage
          media={media}
          loading="lazy"
          fit="cover"
          className="transition-transform duration-300 group-hover:scale-[1.015]"
        />
      </div>
      {credit && (
        <p className="line-clamp-1 border-t border-border bg-card px-3 py-2 text-[11px] leading-tight text-muted-foreground">
          Image: {credit}
        </p>
      )}
    </div>
  )
}
