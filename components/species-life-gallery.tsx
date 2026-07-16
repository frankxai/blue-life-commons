import type { Artifact } from "@/lib/types"
import {
  getSpeciesGallery,
  getSpeciesVideoLinks,
  getUrlHost,
} from "@/lib/media"
import { cn } from "@/lib/utils"

function formatTag(value?: string): string | undefined {
  if (!value) return undefined
  return value.replace(/-/g, " ")
}

/**
 * Educational multi-angle stills + external video link-outs for living species.
 * Real photos stay rights-attributed; concept art is hard-labeled.
 */
export function SpeciesLifeGallery({ artifact }: { artifact: Artifact }) {
  const gallery = getSpeciesGallery(artifact)
  const videos = getSpeciesVideoLinks(artifact)
  if (!gallery.length && !videos.length) return null

  return (
    <section
      aria-labelledby="life-gallery-heading"
      className="mt-10 rounded-3xl border border-border bg-card/80 p-5 shadow-[var(--shadow-elevated)] sm:p-8"
    >
      <p className="text-xs font-semibold uppercase tracking-[0.14em] text-primary">
        Life gallery
      </p>
      <h2
        id="life-gallery-heading"
        className="mt-2 font-serif text-2xl font-semibold tracking-tight text-foreground sm:text-3xl"
      >
        Angles, life stages, and trusted video
      </h2>
      <p className="mt-3 max-w-3xl text-sm leading-relaxed text-muted-foreground sm:text-[15px]">
        Curated educational media for this species. Primary identification uses
        approved real photography when available. Generated concept panels teach
        scale and life history only — they are never field ID or conservation
        evidence. Videos open on institutional or educational hosts (link-out).
      </p>

      {gallery.length > 0 && (
        <div className="mt-6 grid gap-4 sm:grid-cols-2 xl:grid-cols-3">
          {gallery.map((item) => {
            const stage = formatTag(item.life_stage)
            const angle = formatTag(item.angle)
            const sourceHost = getUrlHost(item.source_url)
            return (
              <figure
                key={item.asset_id ?? item.imageUrl}
                className="overflow-hidden rounded-2xl border border-border bg-secondary/40"
              >
                <div className="relative aspect-[16/11] bg-abyss-deep">
                  <img
                    src={item.imageUrl}
                    alt={item.alt_text ?? item.caption ?? "Species educational image"}
                    loading="lazy"
                    decoding="async"
                    referrerPolicy="no-referrer"
                    className={cn(
                      "h-full w-full",
                      item.isConcept ? "object-cover" : "object-cover",
                    )}
                  />
                  <div className="pointer-events-none absolute inset-x-0 top-0 flex flex-wrap gap-1.5 p-2.5">
                    {item.isConcept ? (
                      <span className="rounded-full bg-black/55 px-2 py-0.5 text-[10px] font-semibold uppercase tracking-[0.1em] text-white backdrop-blur-sm">
                        Concept
                      </span>
                    ) : (
                      <span className="rounded-full bg-glow/95 px-2 py-0.5 text-[10px] font-semibold uppercase tracking-[0.1em] text-abyss-deep">
                        Real photo
                      </span>
                    )}
                    {stage && (
                      <span className="rounded-full border border-white/20 bg-black/35 px-2 py-0.5 text-[10px] font-medium capitalize text-white backdrop-blur-sm">
                        {stage}
                      </span>
                    )}
                    {angle && (
                      <span className="rounded-full border border-white/20 bg-black/35 px-2 py-0.5 text-[10px] font-medium capitalize text-white backdrop-blur-sm">
                        {angle}
                      </span>
                    )}
                  </div>
                </div>
                <figcaption className="space-y-2 p-4">
                  <p className="text-sm font-medium leading-snug text-foreground">
                    {item.caption ?? item.alt_text}
                  </p>
                  {item.isConcept && (
                    <p className="text-xs leading-relaxed text-muted-foreground">
                      {item.use_limitations ??
                        "Generated educational reconstruction — not soft-tissue proof, not identification media."}
                    </p>
                  )}
                  <div className="flex flex-wrap gap-x-3 gap-y-1 text-xs text-muted-foreground">
                    {item.creator && <span>{item.creator}</span>}
                    {item.license && <span>{item.license}</span>}
                    {item.source_url && (
                      <a
                        href={item.source_url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="font-medium text-primary underline decoration-primary/30 underline-offset-2 hover:decoration-primary"
                      >
                        Source{sourceHost ? `: ${sourceHost}` : ""}
                      </a>
                    )}
                  </div>
                </figcaption>
              </figure>
            )
          })}
        </div>
      )}

      {videos.length > 0 && (
        <div className="mt-8">
          <h3 className="text-sm font-semibold uppercase tracking-[0.12em] text-primary">
            Watch & learn
          </h3>
          <ul className="mt-3 grid gap-3 sm:grid-cols-2">
            {videos.map((video) => (
              <li key={video.id ?? video.url}>
                <a
                  href={video.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="group flex h-full flex-col rounded-2xl border border-border bg-secondary/50 p-4 transition-colors hover:border-primary/40 hover:bg-primary/5"
                >
                  <div className="flex flex-wrap items-center gap-2">
                    {video.provider && (
                      <span className="rounded-full bg-primary/10 px-2 py-0.5 text-[10px] font-semibold uppercase tracking-[0.1em] text-primary">
                        {video.provider}
                      </span>
                    )}
                    {video.topic && (
                      <span className="rounded-full border border-border px-2 py-0.5 text-[10px] font-medium capitalize text-muted-foreground">
                        {formatTag(video.topic)}
                      </span>
                    )}
                  </div>
                  <p className="mt-2 text-sm font-semibold leading-snug text-foreground group-hover:text-primary">
                    {video.title}
                  </p>
                  {video.educational_use && (
                    <p className="mt-2 text-xs leading-relaxed text-muted-foreground">
                      {video.educational_use}
                    </p>
                  )}
                  {video.rights_note && (
                    <p className="mt-2 text-[11px] leading-relaxed text-muted-foreground/90">
                      {video.rights_note}
                    </p>
                  )}
                  <span className="mt-3 text-xs font-semibold text-primary">
                    Open external video →
                  </span>
                </a>
              </li>
            ))}
          </ul>
        </div>
      )}
    </section>
  )
}
