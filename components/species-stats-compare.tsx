import type { Artifact, SpeciesStats } from "@/lib/types"
import { cn } from "@/lib/utils"
import Link from "next/link"
import { getArtifactById } from "@/lib/content"
import { getApprovedSpeciesMedia } from "@/lib/media"

const STAT_LABELS: Record<string, string> = {
  period: "Period",
  length: "Length",
  mass: "Mass",
  diet: "Diet",
  habitat: "Habitat",
  locomotion: "Locomotion",
  range: "Range",
  clade: "Clade",
  discovery: "Discovery",
}

const PREFERRED_ORDER = [
  "period",
  "clade",
  "length",
  "mass",
  "diet",
  "locomotion",
  "habitat",
  "range",
  "discovery",
]

export function SpeciesStatsChips({
  stats,
  tone = "light",
  className,
}: {
  stats?: SpeciesStats
  tone?: "light" | "dark"
  className?: string
}) {
  if (!stats) return null
  const keys = [
    ...PREFERRED_ORDER.filter((k) => stats[k]),
    ...Object.keys(stats).filter((k) => !PREFERRED_ORDER.includes(k) && stats[k]),
  ]
  if (!keys.length) return null

  return (
    <dl
      className={cn(
        "grid grid-cols-2 gap-2.5 sm:grid-cols-3 lg:grid-cols-4",
        className,
      )}
    >
      {keys.map((key) => (
        <div
          key={key}
          className={cn(
            "rounded-xl border px-3 py-2.5 sm:px-3.5 sm:py-3",
            tone === "dark"
              ? "border-abyss-border bg-white/5"
              : "border-border bg-card",
          )}
        >
          <dt
            className={cn(
              "text-[10px] font-semibold uppercase tracking-[0.14em] sm:text-[11px]",
              tone === "dark" ? "text-abyss-muted" : "text-muted-foreground",
            )}
          >
            {STAT_LABELS[key] ?? key.replace(/_/g, " ")}
          </dt>
          <dd
            className={cn(
              "mt-1 text-sm font-semibold leading-snug sm:text-[15px]",
              tone === "dark" ? "text-abyss-foreground" : "text-foreground",
            )}
          >
            {stats[key]}
          </dd>
        </div>
      ))}
    </dl>
  )
}

export function SpeciesCompareMode({ artifact }: { artifact: Artifact }) {
  const links = artifact.compare
  if (!links?.length) return null

  const cards = links
    .map((link) => {
      const target = getArtifactById(link.target_id)
      if (!target) return null
      const media = getApprovedSpeciesMedia(target)
      return { link, target, media }
    })
    .filter(Boolean) as {
    link: NonNullable<Artifact["compare"]>[number]
    target: Artifact
    media: ReturnType<typeof getApprovedSpeciesMedia>
  }[]

  if (!cards.length) return null

  const selfMedia = getApprovedSpeciesMedia(artifact)

  return (
    <section
      aria-labelledby="compare-heading"
      className="mt-10 overflow-hidden rounded-2xl border border-border bg-card shadow-[var(--shadow-elevated)]"
    >
      <div className="border-b border-border bg-secondary/60 px-5 py-4 sm:px-6">
        <p className="text-xs font-semibold uppercase tracking-[0.14em] text-primary">
          Compare mode
        </p>
        <h2
          id="compare-heading"
          className="mt-1 font-serif text-2xl font-semibold tracking-tight text-foreground"
        >
          Side-by-side in the commons
        </h2>
        <p className="mt-2 max-w-2xl text-sm leading-relaxed text-muted-foreground">
          Ecological analogy only — not kinship. Use body plan, size chips, and
          sources on each page before drawing conclusions.
        </p>
      </div>

      <div className="grid lg:grid-cols-2">
        <ComparePanel
          title={artifact.title}
          href={artifact.href}
          note="This entry"
          mediaUrl={selfMedia?.imageUrl}
          alt={selfMedia?.altText}
          stats={artifact.stats}
          current
        />
        {cards.map(({ link, target, media }) => (
          <ComparePanel
            key={target.id}
            title={target.title}
            href={target.href}
            note={link.note ?? link.label}
            mediaUrl={media?.imageUrl}
            alt={media?.altText}
            stats={target.stats}
          />
        ))}
      </div>
    </section>
  )
}

function ComparePanel({
  title,
  href,
  note,
  mediaUrl,
  alt,
  stats,
  current,
}: {
  title: string
  href: string
  note: string
  mediaUrl?: string
  alt?: string
  stats?: SpeciesStats
  current?: boolean
}) {
  return (
    <div
      className={cn(
        "flex flex-col border-border p-4 sm:p-5",
        current ? "bg-primary/5 lg:border-r" : "bg-card",
        "border-t lg:border-t-0",
      )}
    >
      <div className="flex items-start justify-between gap-3">
        <div>
          <p className="text-[11px] font-semibold uppercase tracking-[0.12em] text-muted-foreground">
            {note}
          </p>
          <h3 className="mt-1 font-sans text-lg font-semibold italic leading-snug tracking-tight text-foreground sm:text-xl">
            <Link href={href} className="hover:text-primary">
              {title}
            </Link>
          </h3>
        </div>
        {!current && (
          <Link
            href={href}
            className="shrink-0 rounded-full border border-border px-3 py-1.5 text-xs font-semibold text-foreground transition hover:border-primary/40 hover:text-primary"
          >
            Open
          </Link>
        )}
      </div>
      <div className="mt-4 aspect-[16/10] overflow-hidden rounded-xl bg-abyss-deep">
        {mediaUrl ? (
          // eslint-disable-next-line @next/next/no-img-element
          <img
            src={mediaUrl}
            alt={alt ?? title}
            className="h-full w-full object-cover"
            loading="lazy"
          />
        ) : (
          <div className="flex h-full items-center justify-center text-sm text-abyss-muted">
            No image yet
          </div>
        )}
      </div>
      {stats && (
        <div className="mt-4">
          <SpeciesStatsChips stats={stats} />
        </div>
      )}
    </div>
  )
}
