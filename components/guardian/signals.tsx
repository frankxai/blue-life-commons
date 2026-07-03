import Link from "next/link"
import type { GuardianData, SpeciesSignal } from "@/lib/guardian"
import { IucnBadge } from "@/components/badges"
import { formatDate, titleCase } from "@/lib/utils"

function formatNumber(n: number | null): string {
  if (n === null) return "—"
  return n.toLocaleString("en-US")
}

function SignalCard({ signal }: { signal: SpeciesSignal }) {
  const Wrapper = signal.href ? Link : "div"
  const wrapperProps = signal.href ? { href: signal.href } : {}
  return (
    <Wrapper
      {...(wrapperProps as { href: string })}
      className="group flex flex-col gap-4 rounded-2xl border border-abyss-border bg-white/[0.03] p-5 transition-colors hover:border-glow/40"
    >
      <div className="flex items-start justify-between gap-3">
        <div className="min-w-0">
          <h3 className="truncate font-serif text-lg font-semibold text-abyss-foreground group-hover:text-glow">
            {signal.name}
          </h3>
          <p className="truncate text-xs italic text-abyss-muted">
            {signal.scientificName}
          </p>
        </div>
        <IucnBadge category={signal.iucn} size="sm" />
      </div>

      {signal.available ? (
        <dl className="grid grid-cols-2 gap-3 text-sm">
          <div>
            <dd className="font-serif text-xl font-semibold tabular-nums text-glow">
              {formatNumber(signal.obisRecords)}
            </dd>
            <dt className="text-xs text-abyss-muted">OBIS records</dt>
          </div>
          <div>
            <dd className="font-serif text-xl font-semibold tabular-nums text-glow">
              {formatNumber(signal.gbifRecords)}
            </dd>
            <dt className="text-xs text-abyss-muted">GBIF records</dt>
          </div>
          <div>
            <dd className="text-sm font-medium tabular-nums text-abyss-foreground">
              {formatNumber(signal.datasets)}
            </dd>
            <dt className="text-xs text-abyss-muted">Datasets</dt>
          </div>
          <div>
            <dd className="text-sm font-medium tabular-nums text-abyss-foreground">
              {signal.yearRange ? `${signal.yearRange[0]}–${signal.yearRange[1]}` : "—"}
            </dd>
            <dt className="text-xs text-abyss-muted">Year range</dt>
          </div>
        </dl>
      ) : (
        <p className="rounded-lg bg-white/5 px-3 py-2 text-xs text-abyss-muted">
          Source silent right now — no signal fabricated.
        </p>
      )}
    </Wrapper>
  )
}

export function GuardianSignals({ data }: { data: GuardianData }) {
  const byGuild = new Map<string, SpeciesSignal[]>()
  for (const s of data.species) {
    const list = byGuild.get(s.guild) ?? []
    list.push(s)
    byGuild.set(s.guild, list)
  }

  return (
    <div className="flex flex-col gap-10">
      {[...byGuild.entries()].map(([guild, signals]) => (
        <section key={guild} aria-labelledby={`guild-${guild}`}>
          <h2
            id={`guild-${guild}`}
            className="text-xs font-semibold uppercase tracking-[0.16em] text-glow"
          >
            {guild}
          </h2>
          <div className="mt-4 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
            {signals.map((s) => (
              <SignalCard key={s.scientificName} signal={s} />
            ))}
          </div>
        </section>
      ))}
    </div>
  )
}

export function RecentFeed({ data }: { data: GuardianData }) {
  if (data.recent.length === 0) return null
  return (
    <div className="rounded-2xl border border-abyss-border bg-white/[0.03]">
      <div className="border-b border-abyss-border px-5 py-4">
        <h2 className="text-xs font-semibold uppercase tracking-[0.16em] text-glow">
          Latest observations
        </h2>
        <p className="mt-1 text-xs text-abyss-muted">
          Most recent georeferenced records from GBIF, refreshed every 6 hours.
        </p>
      </div>
      <ul className="divide-y divide-abyss-border">
        {data.recent.map((r, i) => (
          <li
            key={`${r.scientificName}-${i}`}
            className="flex items-center justify-between gap-4 px-5 py-3.5"
          >
            <div className="min-w-0">
              <p className="truncate text-sm font-medium text-abyss-foreground">
                {r.commonName}
              </p>
              <p className="truncate text-xs text-abyss-muted">
                {r.country ? titleCase(r.country.toLowerCase()) : "Unknown location"}
                {r.dataset ? ` · ${r.dataset}` : ""}
              </p>
            </div>
            <time className="shrink-0 text-xs tabular-nums text-abyss-muted">
              {r.date ? formatDate(r.date) : "—"}
            </time>
          </li>
        ))}
      </ul>
    </div>
  )
}
