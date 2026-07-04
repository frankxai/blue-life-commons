import type { Metadata } from "next"
import Link from "next/link"
import { Container, SectionHeading, ButtonLink, ArrowRight } from "@/components/primitives"
import { getArtifactsByType, getGuildForArtifact } from "@/lib/content"
import type { ApprovedSpeciesMedia } from "@/lib/media"
import { getApprovedSpeciesMedia, getMediaCreditText, getUrlHost } from "@/lib/media"
import {
  MEDIA_BENCHMARKS,
  MEDIA_EXPANSION_STEPS,
  MEDIA_SOURCE_LANES,
} from "@/lib/media-intelligence"
import {
  MEDIA_STORAGE_PUBLIC_BASE_URL,
  MEDIA_STORAGE_STACK,
  MEDIA_STORAGE_VARIANTS,
} from "@/lib/media-storage"
import { GUILD_META } from "@/lib/utils"
import type { Artifact } from "@/lib/types"

export const metadata: Metadata = {
  title: "Media Intelligence",
  description:
    "The Blue Life Commons operating layer for approved animal images, source provenance, partner media, and scalable species visual coverage.",
}

function pct(part: number, whole: number): number {
  if (!whole) return 0
  return Math.round((part / whole) * 100)
}

function StatCard({
  label,
  value,
  detail,
}: {
  label: string
  value: string
  detail: string
}) {
  return (
    <div className="rounded-xl border border-border bg-card p-5">
      <p className="text-xs font-semibold uppercase tracking-[0.14em] text-primary">
        {label}
      </p>
      <p className="mt-2 font-serif text-3xl font-semibold text-foreground">
        {value}
      </p>
      <p className="mt-2 text-sm leading-relaxed text-muted-foreground">
        {detail}
      </p>
    </div>
  )
}

function SourceLink({
  href,
  label = "Source",
}: {
  href: string
  label?: string
}) {
  return (
    <a
      href={href}
      target="_blank"
      rel="noopener noreferrer"
      className="inline-flex items-center gap-1 text-sm font-semibold text-primary underline decoration-primary/30 underline-offset-4 hover:decoration-primary"
    >
      {label}
      <ArrowRight className="h-3.5 w-3.5" />
    </a>
  )
}

interface ApprovedSpeciesRecord {
  artifact: Artifact
  guild: string
  media: ApprovedSpeciesMedia
}

function ApprovedMediaCard({ record }: { record: ApprovedSpeciesRecord }) {
  const sourceHost = getUrlHost(record.media.sourceUrl)
  const credit = getMediaCreditText(record.media)
  const guildLabel = GUILD_META[record.guild]?.label ?? record.guild

  return (
    <article className="group overflow-hidden rounded-2xl border border-border bg-card transition-all duration-300 hover:-translate-y-1 hover:border-primary/40 hover:shadow-[var(--shadow-elevated)]">
      <Link href={record.artifact.href} className="block">
        <div className="aspect-[4/3] bg-muted">
          <img
            src={record.media.imageUrl}
            alt={record.media.altText}
            loading="lazy"
            decoding="async"
            referrerPolicy="no-referrer"
            className="h-full w-full object-contain transition-transform duration-300 group-hover:scale-[1.015]"
          />
        </div>
      </Link>
      <div className="border-t border-border p-4">
        <div className="flex flex-wrap gap-2">
          <span className="rounded-full bg-primary/10 px-2.5 py-1 text-[11px] font-semibold uppercase tracking-[0.08em] text-primary">
            Approved
          </span>
          {record.media.rightsStatus && (
            <span className="rounded-full bg-muted px-2.5 py-1 text-[11px] font-medium capitalize text-muted-foreground">
              {record.media.rightsStatus.replace(/-/g, " ")}
            </span>
          )}
        </div>
        <h3 className="mt-3 font-serif text-lg font-semibold leading-snug text-foreground group-hover:text-primary">
          <Link href={record.artifact.href}>{record.artifact.title}</Link>
        </h3>
        <p className="mt-1 text-xs font-semibold uppercase tracking-[0.12em] text-primary">
          {guildLabel}
        </p>
        <dl className="mt-3 grid gap-2 text-xs text-muted-foreground">
          {record.media.assetId && (
            <div>
              <dt className="font-semibold text-foreground">Asset</dt>
              <dd className="mt-0.5 truncate" title={record.media.assetId}>
                {record.media.assetId}
              </dd>
            </div>
          )}
          {record.media.license && (
            <div>
              <dt className="font-semibold text-foreground">License</dt>
              <dd className="mt-0.5 truncate" title={record.media.license}>
                {record.media.license}
              </dd>
            </div>
          )}
          {sourceHost && (
            <div>
              <dt className="font-semibold text-foreground">Source</dt>
              <dd className="mt-0.5 truncate" title={sourceHost}>
                {sourceHost}
              </dd>
            </div>
          )}
        </dl>
        {credit && (
          <p className="mt-3 line-clamp-2 text-xs leading-relaxed text-muted-foreground">
            Image: {credit}
          </p>
        )}
        <div className="mt-4 flex flex-wrap gap-x-4 gap-y-2 text-xs font-semibold">
          <Link href={record.artifact.href} className="text-primary hover:underline">
            Open animal
          </Link>
          {record.media.sourceUrl && (
            <a
              href={record.media.sourceUrl}
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

export default function MediaIntelligencePage() {
  const species = getArtifactsByType("species-page")
  const approved = species
    .map((artifact) => {
      const media = getApprovedSpeciesMedia(artifact)
      if (!media) return undefined
      return {
        artifact,
        guild: getGuildForArtifact(artifact),
        media,
      }
    })
    .filter((record): record is ApprovedSpeciesRecord => Boolean(record))

  const sourceHosts = new Set(
    approved
      .map((record) => getUrlHost(record.media?.sourceUrl))
      .filter((host): host is string => Boolean(host)),
  )
  const rights = new Map<string, number>()
  const guilds = new Map<string, number>()

  for (const record of approved) {
    const rightsStatus = record.media.rightsStatus ?? "not recorded"
    rights.set(rightsStatus, (rights.get(rightsStatus) ?? 0) + 1)

    guilds.set(record.guild, (guilds.get(record.guild) ?? 0) + 1)
  }

  const rightsRows = [...rights.entries()].sort((a, b) => b[1] - a[1])
  const guildRows = [...guilds.entries()].sort((a, b) => b[1] - a[1])
  const coverage = pct(approved.length, species.length)
  const publicStorageVariants = MEDIA_STORAGE_VARIANTS.filter(
    (variant) => variant.publicUse,
  )
  const plannedPublicVariants = approved.length * publicStorageVariants.length
  const plannedStorageObjects = approved.length * MEDIA_STORAGE_VARIANTS.length

  return (
    <main>
      <div className="border-b border-border bg-secondary">
        <Container className="py-14 sm:py-20">
          <div className="grid gap-8 lg:grid-cols-[minmax(0,1.15fr)_minmax(320px,0.85fr)] lg:items-end">
            <SectionHeading
              eyebrow="Media intelligence"
              title="The approved visual layer for ocean life"
              description="Blue Life Commons is not trying to be another image search engine. It turns partner media, biodiversity networks, and public-domain sources into species visuals that are rights-checked, credited, welfare-aware, and ready for public pages."
            />
            <div className="rounded-2xl border border-border bg-card p-5 shadow-[var(--shadow-elevated)]">
              <p className="text-xs font-semibold uppercase tracking-[0.14em] text-primary">
                Current production coverage
              </p>
              <div className="mt-4 flex items-end gap-3">
                <span className="font-serif text-6xl font-semibold leading-none text-foreground">
                  {coverage}%
                </span>
                <span className="pb-1 text-sm font-medium text-muted-foreground">
                  approved image coverage
                </span>
              </div>
              <div className="mt-5 h-2 overflow-hidden rounded-full bg-muted">
                <div
                  className="h-full rounded-full bg-primary"
                  style={{ width: `${coverage}%` }}
                />
              </div>
              <p className="mt-4 text-sm leading-relaxed text-muted-foreground">
                {approved.length} of {species.length} current species pages render
                approved primary images with source, creator, license, alt text,
                and public-use review gates.
              </p>
            </div>
          </div>
        </Container>
      </div>

      <Container className="py-12 sm:py-16">
        <section aria-labelledby="coverage-heading">
          <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
            <StatCard
              label="Tracked animals"
              value={String(species.length)}
              detail="Current species-page corpus in the public commons."
            />
            <StatCard
              label="Approved images"
              value={String(approved.length)}
              detail="Primary visuals allowed on public species surfaces."
            />
            <StatCard
              label="Source domains"
              value={String(sourceHosts.size)}
              detail="Distinct domains behind approved primary image source pages."
            />
            <StatCard
              label="Review leakage"
              value="0"
              detail="Candidate and reviewer-only media stay out of public rendering."
            />
          </div>
        </section>

        <section className="mt-16" aria-labelledby="coverage-detail-heading">
          <SectionHeading
            id="coverage-detail-heading"
            eyebrow="Coverage map"
            title="Every current animal is live; the next job is scale"
            description="The first production pass solved coverage for the current corpus. The platform pass makes the route for more animals explicit: normalize the taxon, collect candidates, approve one primary visual, then publish with provenance."
          />
          <div className="mt-8 grid gap-5 lg:grid-cols-[minmax(0,0.9fr)_minmax(0,1.1fr)]">
            <div className="rounded-2xl border border-border bg-card p-6">
              <h3 className="font-serif text-xl font-semibold text-foreground">
                Approved media by guild
              </h3>
              <div className="mt-5 space-y-4">
                {guildRows.map(([guild, count]) => (
                  <div key={guild}>
                    <div className="flex items-center justify-between gap-3 text-sm">
                      <span className="font-medium text-foreground">
                        {GUILD_META[guild]?.label ?? guild}
                      </span>
                      <span className="text-muted-foreground">{count}</span>
                    </div>
                    <div className="mt-2 h-2 overflow-hidden rounded-full bg-muted">
                      <div
                        className="h-full rounded-full bg-primary"
                        style={{ width: `${pct(count, approved.length)}%` }}
                      />
                    </div>
                  </div>
                ))}
              </div>
            </div>
            <div className="rounded-2xl border border-border bg-card p-6">
              <h3 className="font-serif text-xl font-semibold text-foreground">
                Rights profile
              </h3>
              <div className="mt-5 grid gap-3 sm:grid-cols-2">
                {rightsRows.map(([status, count]) => (
                  <div key={status} className="rounded-xl border border-border bg-secondary p-4">
                    <p className="text-sm font-semibold capitalize text-foreground">
                      {status.replace(/-/g, " ")}
                    </p>
                    <p className="mt-2 font-serif text-3xl font-semibold text-primary">
                      {count}
                    </p>
                    <p className="mt-1 text-xs text-muted-foreground">
                      approved primary {count === 1 ? "image" : "images"}
                    </p>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </section>

        <section className="mt-16" aria-labelledby="visual-ledger-heading">
          <SectionHeading
            id="visual-ledger-heading"
            eyebrow="Visual audit board"
            title="Every approved animal image, mapped to its page"
            description="This is the public ledger layer: each rendered visual is attached to one animal, one source path, one rights status, and one approved public surface. Candidate media stays out of this grid until review promotes it."
          />
          <div className="mt-8 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
            {approved.map((record) => (
              <ApprovedMediaCard key={record.artifact.id} record={record} />
            ))}
          </div>
        </section>

        <section className="mt-16" aria-labelledby="storage-heading">
          <SectionHeading
            id="storage-heading"
            eyebrow="Scale storage"
            title="Git stores truth; object storage stores pixels"
            description="The long-term setup keeps this repo as the rights and review ledger while approved image files move to an R2/S3-compatible media domain. Vercel stays focused on rendering the app."
          />
          <div className="mt-8 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
            <StatCard
              label="Mirror-ready"
              value={String(approved.length)}
              detail="Approved species images mapped to deterministic object-storage prefixes."
            />
            <StatCard
              label="Public variants"
              value={String(plannedPublicVariants)}
              detail={`${publicStorageVariants.length} generated public derivatives per approved image.`}
            />
            <StatCard
              label="Storage objects"
              value={String(plannedStorageObjects)}
              detail="Original plus public derivative objects planned by the storage manifest."
            />
            <StatCard
              label="Git originals"
              value="0"
              detail="Bulk source pixels stay out of the repository."
            />
          </div>
          <div className="mt-8 grid gap-4 lg:grid-cols-4">
            {MEDIA_STORAGE_STACK.map((layer) => (
              <article key={layer.name} className="rounded-2xl border border-border bg-card p-5">
                <p className="text-xs font-semibold uppercase tracking-[0.14em] text-primary">
                  {layer.job}
                </p>
                <h3 className="mt-2 font-serif text-xl font-semibold text-foreground">
                  {layer.name}
                </h3>
                <p className="mt-3 text-sm leading-relaxed text-muted-foreground">
                  {layer.stores}
                </p>
                <p className="mt-4 text-xs font-semibold uppercase tracking-[0.12em] text-foreground">
                  Why
                </p>
                <p className="mt-1 text-sm leading-relaxed text-muted-foreground">
                  {layer.reason}
                </p>
              </article>
            ))}
          </div>
          <div className="mt-6 rounded-2xl border border-border bg-secondary p-5">
            <p className="text-xs font-semibold uppercase tracking-[0.14em] text-primary">
              Media domain
            </p>
            <p className="mt-2 font-mono text-sm text-foreground">
              {MEDIA_STORAGE_PUBLIC_BASE_URL}
            </p>
            <p className="mt-2 text-sm leading-relaxed text-muted-foreground">
              Public routes should switch to owned `card`, `hero`, and `og`
              derivatives only after the manifest row has generated objects,
              checksums, rights review, and an audit event.
            </p>
          </div>
        </section>

        <section className="mt-16" aria-labelledby="benchmark-heading">
          <SectionHeading
            id="benchmark-heading"
            eyebrow="Competitive read"
            title="Build on the ecosystem instead of duplicating it"
            description="The best platform position is not another undifferentiated animal-photo search. It is the public trust layer that joins image rights, taxonomy, source context, welfare review, and action."
          />
          <div className="mt-8 grid gap-4 lg:grid-cols-2">
            {MEDIA_BENCHMARKS.map((item) => (
              <article key={item.name} className="rounded-2xl border border-border bg-card p-6">
                <div className="flex flex-wrap items-start justify-between gap-3">
                  <div>
                    <p className="text-xs font-semibold uppercase tracking-[0.14em] text-primary">
                      {item.category}
                    </p>
                    <h3 className="mt-2 font-serif text-xl font-semibold text-foreground">
                      {item.name}
                    </h3>
                  </div>
                  <SourceLink href={item.sourceUrl} label={item.sourceLabel} />
                </div>
                <dl className="mt-5 grid gap-4 text-sm leading-relaxed">
                  <div>
                    <dt className="font-semibold text-foreground">What they do</dt>
                    <dd className="mt-1 text-muted-foreground">{item.whatTheyDo}</dd>
                  </div>
                  <div>
                    <dt className="font-semibold text-foreground">Blue Life move</dt>
                    <dd className="mt-1 text-muted-foreground">{item.blueLifeMove}</dd>
                  </div>
                </dl>
              </article>
            ))}
          </div>
        </section>

        <section className="mt-16" aria-labelledby="source-lanes-heading">
          <SectionHeading
            id="source-lanes-heading"
            eyebrow="Source lanes"
            title="How more animals and images come online"
            description="Each lane has a role and a gate. This is how we get faster without weakening image rights, source quality, or animal-welfare context."
          />
          <div className="mt-8 grid gap-4 lg:grid-cols-5">
            {MEDIA_SOURCE_LANES.map((lane) => (
              <article key={lane.name} className="rounded-2xl border border-border bg-card p-5">
                <p className="text-xs font-semibold uppercase tracking-[0.14em] text-primary">
                  {lane.role}
                </p>
                <h3 className="mt-2 font-serif text-lg font-semibold text-foreground">
                  {lane.name}
                </h3>
                <p className="mt-3 text-sm leading-relaxed text-muted-foreground">
                  {lane.bestFor}
                </p>
                <p className="mt-4 text-xs font-semibold uppercase tracking-[0.12em] text-foreground">
                  Gate
                </p>
                <p className="mt-1 text-sm leading-relaxed text-muted-foreground">
                  {lane.gate}
                </p>
                <div className="mt-4">
                  <SourceLink href={lane.sourceUrl} />
                </div>
              </article>
            ))}
          </div>
        </section>

        <section className="mt-16" aria-labelledby="loop-heading">
          <SectionHeading
            id="loop-heading"
            eyebrow="Expansion loop"
            title="The repeatable path from animal to live image"
          />
          <ol className="mt-8 grid gap-4 md:grid-cols-2 lg:grid-cols-3">
            {MEDIA_EXPANSION_STEPS.map((step) => (
              <li key={step.name} className="rounded-2xl border border-border bg-card p-6">
                <h3 className="font-serif text-lg font-semibold text-foreground">
                  {step.name}
                </h3>
                <p className="mt-2 text-sm font-semibold text-primary">
                  {step.outcome}
                </p>
                <p className="mt-3 text-sm leading-relaxed text-muted-foreground">
                  {step.detail}
                </p>
              </li>
            ))}
          </ol>
        </section>

        <section className="mt-16 rounded-2xl border border-border bg-secondary p-6 sm:p-8">
          <div className="grid gap-6 lg:grid-cols-[minmax(0,1fr)_auto] lg:items-center">
            <div>
              <h2 className="font-serif text-2xl font-semibold text-foreground">
                Platform answer
              </h2>
              <p className="mt-3 max-w-3xl text-sm leading-relaxed text-muted-foreground">
                Blue Life wins by being the rights-safe, source-backed, welfare-aware
                publishing layer for animal visuals. It should ingest from the best
                biodiversity platforms, partner with the teams that already own strong
                field media, and publish only what survives the approval contract.
              </p>
            </div>
            <div className="flex flex-wrap gap-3">
              <ButtonLink href="/species" variant="primary">
                See live animals
                <ArrowRight />
              </ButtonLink>
              <ButtonLink href="/contribute" variant="secondary">
                Contribute media
              </ButtonLink>
            </div>
          </div>
        </section>
      </Container>
    </main>
  )
}
