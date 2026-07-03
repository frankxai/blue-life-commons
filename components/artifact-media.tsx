import type { Artifact } from "@/lib/types"
import type { ApprovedSpeciesMedia } from "@/lib/media"
import {
  getApprovedSpeciesMedia,
  getMediaCreditText,
  getUrlHost,
} from "@/lib/media"
import { cn } from "@/lib/utils"

function MediaImage({
  media,
  loading,
  className,
}: {
  media: ApprovedSpeciesMedia
  loading: "eager" | "lazy"
  className?: string
}) {
  return (
    <img
      src={media.imageUrl}
      alt={media.altText}
      loading={loading}
      decoding="async"
      referrerPolicy="no-referrer"
      className={cn("h-full w-full object-contain", className)}
    />
  )
}

export function ArtifactHeroMedia({ artifact }: { artifact: Artifact }) {
  const media = getApprovedSpeciesMedia(artifact)
  if (!media) return null

  const sourceHost = getUrlHost(media.sourceUrl)
  const originalHost = getUrlHost(media.originalMediaUrl)

  return (
    <figure className="overflow-hidden rounded-2xl border border-border bg-card shadow-[var(--shadow-elevated)]">
      <div className="aspect-[4/3] bg-muted">
        <MediaImage media={media} loading="eager" />
      </div>
      <figcaption className="border-t border-border p-4">
        <div className="flex flex-wrap items-center gap-2">
          <span className="rounded-full bg-primary/10 px-2.5 py-1 text-xs font-semibold text-primary">
            Approved primary image
          </span>
          {media.rightsStatus && (
            <span className="rounded-full bg-muted px-2.5 py-1 text-xs font-medium text-muted-foreground">
              {media.rightsStatus.replace(/-/g, " ")}
            </span>
          )}
        </div>
        <p className="mt-3 text-sm leading-relaxed text-foreground">
          {media.altText}
        </p>
        <dl className="mt-3 grid gap-2 text-xs text-muted-foreground sm:grid-cols-2">
          {media.creator && (
            <div>
              <dt className="font-semibold text-foreground">Creator</dt>
              <dd className="mt-0.5 line-clamp-2">{media.creator}</dd>
            </div>
          )}
          {media.license && (
            <div>
              <dt className="font-semibold text-foreground">License</dt>
              <dd className="mt-0.5">
                {media.licenseUrl ? (
                  <a
                    href={media.licenseUrl}
                    target="_blank"
                    rel="license noopener noreferrer"
                    className="underline decoration-primary/40 underline-offset-2 transition-colors hover:text-primary hover:decoration-primary"
                  >
                    {media.license}
                  </a>
                ) : (
                  media.license
                )}
              </dd>
            </div>
          )}
        </dl>
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
          {media.originalMediaUrl && (
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
      <div className="aspect-[4/3] bg-muted">
        <MediaImage
          media={media}
          loading="lazy"
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
