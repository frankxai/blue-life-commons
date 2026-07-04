import Link from "next/link"
import { Chip, IucnBadge } from "@/components/badges"
import { Container, ArrowRight } from "@/components/primitives"
import { getArtifactsByType, getGuildForArtifact } from "@/lib/content"
import {
  getApprovedSpeciesMedia,
  getMediaCreditText,
  getUrlHost,
  type ApprovedSpeciesMedia,
} from "@/lib/media"
import { GUILD_META } from "@/lib/utils"
import type { Artifact } from "@/lib/types"

interface SpeciesEntry {
  artifact: Artifact
  guild: string
  media?: ApprovedSpeciesMedia
}

function statLabel(value: number, singular: string, plural: string) {
  return `${value} ${value === 1 ? singular : plural}`
}

function Stat({
  label,
  value,
  detail,
}: {
  label: string
  value: string
  detail: string
}) {
  return (
    <div className="border-t border-abyss-border pt-4">
      <p className="font-serif text-3xl font-semibold text-abyss-foreground">
        {value}
      </p>
      <p className="mt-1 text-xs font-semibold uppercase tracking-[0.14em] text-glow">
        {label}
      </p>
      <p className="mt-2 text-sm leading-relaxed text-abyss-muted">{detail}</p>
    </div>
  )
}

function HeroMosaic({ entries }: { entries: SpeciesEntry[] }) {
  const featured = entries.filter((entry) => entry.media).slice(0, 7)
  const primary = featured[0]
  const secondary = featured.slice(1)

  if (!primary?.media) return null

  return (
    <div className="grid min-w-0 gap-3 sm:grid-cols-[1.25fr_0.75fr]">
      <Link
        href={primary.artifact.href}
        className="group min-w-0 overflow-hidden rounded-2xl border border-abyss-border bg-white/5"
      >
        <div className="aspect-[4/3] bg-abyss-deep">
          <img
            src={primary.media.imageUrl}
            alt={primary.media.altText}
            loading="eager"
            decoding="async"
            className="h-full w-full object-contain transition-transform duration-300 group-hover:scale-[1.015]"
          />
        </div>
        <div className="border-t border-abyss-border p-4">
          <p className="text-xs font-semibold uppercase tracking-[0.14em] text-glow">
            Featured entry
          </p>
          <p className="mt-1 font-serif text-xl font-semibold text-abyss-foreground">
            {primary.artifact.title}
          </p>
        </div>
      </Link>

      <div className="grid grid-cols-2 gap-3 sm:grid-cols-1">
        {secondary.map((entry) => (
          <Link
            key={entry.artifact.id}
            href={entry.artifact.href}
            className="group min-w-0 overflow-hidden rounded-xl border border-abyss-border bg-white/5"
          >
            <div className="aspect-[4/3] bg-abyss-deep">
              <img
                src={entry.media?.imageUrl}
                alt={entry.media?.altText ?? entry.artifact.title}
                loading="lazy"
                decoding="async"
                className="h-full w-full object-contain transition-transform duration-300 group-hover:scale-[1.02]"
              />
            </div>
          </Link>
        ))}
      </div>
    </div>
  )
}

function SpeciesCard({ entry }: { entry: SpeciesEntry }) {
  const media = entry.media
  const sourceHost = getUrlHost(media?.sourceUrl)
  const credit = media ? getMediaCreditText(media) : undefined
  const guildLabel = GUILD_META[entry.guild]?.label ?? entry.guild

  return (
    <article className="group flex h-full flex-col overflow-hidden rounded-xl border border-border bg-card transition-all duration-300 hover:-translate-y-1 hover:border-primary/40 hover:shadow-[var(--shadow-elevated)]">
      <Link href={entry.artifact.href} className="block bg-muted">
        {media ? (
          <div className="aspect-[4/3]">
            <img
              src={media.imageUrl}
              alt={media.altText}
              loading="lazy"
              decoding="async"
              className="h-full w-full object-contain transition-transform duration-300 group-hover:scale-[1.015]"
            />
          </div>
        ) : (
          <div className="flex aspect-[4/3] items-center justify-center px-6 text-center text-sm text-muted-foreground">
            Image pending approved media
          </div>
        )}
      </Link>

      <div className="flex flex-1 flex-col p-5">
        <div className="flex flex-wrap items-center gap-2">
          <Chip tone="primary">{guildLabel}</Chip>
          <IucnBadge category={entry.artifact.iucn?.category} size="sm" />
          {media?.imageUrlSource === "vercel_blob" && (
            <Chip tone="accent">Vercel hosted</Chip>
          )}
        </div>

        <h3 className="mt-4 font-serif text-xl font-semibold leading-snug text-foreground group-hover:text-primary">
          <Link href={entry.artifact.href}>{entry.artifact.title}</Link>
        </h3>

        {entry.artifact.excerpt && (
          <p className="mt-2 line-clamp-3 text-sm leading-relaxed text-muted-foreground">
            {entry.artifact.excerpt}
          </p>
        )}

        <dl className="mt-4 grid gap-2 text-xs text-muted-foreground">
          <div className="flex items-center justify-between gap-4 border-t border-border pt-2">
            <dt>Sources</dt>
            <dd className="font-semibold text-foreground">
              {entry.artifact.sources.length}
            </dd>
          </div>
          {media?.rightsStatus && (
            <div className="flex items-center justify-between gap-4 border-t border-border pt-2">
              <dt>Image rights</dt>
              <dd className="max-w-[11rem] truncate font-semibold capitalize text-foreground">
                {media.rightsStatus.replace(/-/g, " ")}
              </dd>
            </div>
          )}
          {sourceHost && (
            <div className="flex items-center justify-between gap-4 border-t border-border pt-2">
              <dt>Image source</dt>
              <dd className="max-w-[11rem] truncate font-semibold text-foreground">
                {sourceHost}
              </dd>
            </div>
          )}
        </dl>

        {credit && (
          <p className="mt-4 line-clamp-2 text-xs leading-relaxed text-muted-foreground">
            Image: {credit}
          </p>
        )}

        <div className="mt-auto flex flex-wrap gap-x-4 gap-y-2 pt-5 text-sm font-semibold">
          <Link href={entry.artifact.href} className="text-primary hover:underline">
            Open entry
          </Link>
          {media?.sourceUrl && (
            <a
              href={media.sourceUrl}
              target="_blank"
              rel="noopener noreferrer"
              className="text-primary hover:underline"
            >
              Source page
            </a>
          )}
        </div>
      </div>
    </article>
  )
}

export function SpeciesEncyclopedia() {
  const entries = getArtifactsByType("species-page").map((artifact) => ({
    artifact,
    guild: getGuildForArtifact(artifact),
    media: getApprovedSpeciesMedia(artifact),
  }))

  const byGuild = new Map<string, SpeciesEntry[]>()
  const sourceUrls = new Set<string>()
  let ownedImages = 0
  let approvedImages = 0

  for (const entry of entries) {
    const list = byGuild.get(entry.guild) ?? []
    list.push(entry)
    byGuild.set(entry.guild, list)
    for (const source of entry.artifact.sources) sourceUrls.add(source.url)
    if (entry.media) approvedImages += 1
    if (entry.media?.imageUrlSource === "vercel_blob") ownedImages += 1
  }

  const guilds = [...byGuild.entries()].sort((a, b) => b[1].length - a[1].length)

  return (
    <main>
      <section className="bg-abyss text-abyss-foreground abyss-grid">
        <Container className="grid gap-10 py-14 sm:py-20 lg:grid-cols-[minmax(0,0.92fr)_minmax(420px,1.08fr)] lg:items-end">
          <div className="min-w-0">
            <p className="text-xs font-semibold uppercase tracking-[0.16em] text-glow">
              Ocean life encyclopedia
            </p>
            <h1 className="mt-4 max-w-full text-balance break-words font-serif text-3xl font-semibold leading-tight sm:text-5xl">
              Every animal entry, image, source, and credit in one living catalog
            </h1>
            <p className="mt-5 max-w-[34ch] break-words text-base leading-relaxed text-abyss-muted sm:max-w-2xl sm:text-pretty sm:text-lg">
              Blue Life Commons now has an image-first species encyclopedia:
              approved media hosted in Vercel Blob, source pages preserved, and
              every animal connected back to its cited public record.
            </p>
            <div className="mt-7 flex flex-wrap gap-3">
              <Link
                href="#atlas"
                className="inline-flex items-center justify-center gap-2 rounded-full bg-glow px-5 py-2.5 text-sm font-semibold text-abyss-deep transition-transform hover:-translate-y-0.5"
              >
                Explore animals
                <ArrowRight className="h-4 w-4" />
              </Link>
              <Link
                href="/media-intelligence"
                className="inline-flex items-center justify-center gap-2 rounded-full border border-abyss-border bg-white/5 px-5 py-2.5 text-sm font-semibold text-abyss-foreground backdrop-blur-sm transition-colors hover:border-glow hover:text-glow"
              >
                Media system
              </Link>
            </div>
            <div className="mt-10 grid gap-5 sm:grid-cols-2">
              <Stat
                value={String(entries.length)}
                label="Animal entries"
                detail="Current public species pages in the commons."
              />
              <Stat
                value={String(ownedImages)}
                label="Hosted images"
                detail="Approved species images now served from Vercel Blob."
              />
              <Stat
                value={String(sourceUrls.size)}
                label="Cited sources"
                detail="Unique source URLs represented by the species corpus."
              />
              <Stat
                value={String(guilds.length)}
                label="Guilds"
                detail="Species grouped for scanning and expansion."
              />
            </div>
          </div>

          <HeroMosaic entries={entries} />
        </Container>
      </section>

      <section className="border-b border-border bg-secondary">
        <Container className="py-8">
          <div className="flex flex-col gap-4 lg:flex-row lg:items-center lg:justify-between">
            <div>
              <p className="text-sm font-semibold text-foreground">
                {statLabel(approvedImages, "approved image", "approved images")} ·{" "}
                {statLabel(ownedImages, "Blob-hosted image", "Blob-hosted images")}
              </p>
              <p className="mt-1 text-sm text-muted-foreground">
                Candidate media remains out of public rendering until approval.
              </p>
            </div>
            <nav aria-label="Animal guilds" className="flex flex-wrap gap-2">
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
          </div>
        </Container>
      </section>

      <Container className="py-12 sm:py-16">
        <div className="flex flex-col gap-16" id="atlas">
          {guilds.map(([guild, list]) => (
            <section
              key={guild}
              id={guild}
              aria-labelledby={`${guild}-heading`}
              className="scroll-mt-24"
            >
              <div className="flex flex-col gap-3 sm:flex-row sm:items-end sm:justify-between">
                <div>
                  <p className="text-xs font-semibold uppercase tracking-[0.14em] text-primary">
                    {list.length} {list.length === 1 ? "entry" : "entries"}
                  </p>
                  <h2
                    id={`${guild}-heading`}
                    className="mt-2 font-serif text-3xl font-semibold text-foreground"
                  >
                    {GUILD_META[guild]?.label ?? guild}
                  </h2>
                </div>
                <Link
                  href={`/catalog?type=species-page`}
                  className="text-sm font-semibold text-primary hover:underline"
                >
                  Search full catalog
                </Link>
              </div>
              <div className="mt-6 grid gap-5 sm:grid-cols-2 xl:grid-cols-3">
                {list.map((entry) => (
                  <SpeciesCard key={entry.artifact.id} entry={entry} />
                ))}
              </div>
            </section>
          ))}
        </div>
      </Container>
    </main>
  )
}
