import { Suspense } from "react"
import type { Metadata } from "next"
import { getGuardianData } from "@/lib/guardian"
import { GuardianSignals, RecentFeed } from "@/components/guardian/signals"
import { Container, SectionHeading } from "@/components/primitives"
import { formatDate } from "@/lib/utils"

export const metadata: Metadata = {
  title: "Guardian — Live Ocean Signals",
  description:
    "Live biodiversity signals for flagship ocean species, drawn from the open OBIS and GBIF data sources that power the Ocean Intelligence System. Cached, sourced, never fabricated.",
}

// Revalidate the rendered page every 6 hours to match the data cache.
export const revalidate = 21600

function SignalsSkeleton() {
  return (
    <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3" aria-hidden>
      {Array.from({ length: 6 }).map((_, i) => (
        <div
          key={i}
          className="h-44 animate-pulse rounded-2xl border border-abyss-border bg-white/[0.03]"
        />
      ))}
    </div>
  )
}

async function GuardianContent() {
  const data = await getGuardianData()

  return (
    <div className="flex flex-col gap-14">
      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <StatBlock
          value={data.totals.obisRecords.toLocaleString("en-US")}
          label="OBIS records tracked"
        />
        <StatBlock
          value={data.totals.gbifRecords.toLocaleString("en-US")}
          label="GBIF occurrences"
        />
        <StatBlock
          value={String(data.totals.speciesTracked)}
          label="Flagship species live"
        />
        <StatBlock
          value={`${data.totals.sourcesLive}/${data.totals.sourcesTotal}`}
          label="Sources responding"
        />
      </div>

      {data.degraded && (
        <p className="rounded-xl border border-warning/30 bg-warning/10 px-4 py-3 text-sm text-abyss-foreground">
          Live sources are temporarily unreachable. Signals will refresh
          automatically once OBIS and GBIF respond — nothing shown here is
          simulated.
        </p>
      )}

      <div className="grid gap-10 lg:grid-cols-[1fr_20rem]">
        <GuardianSignals data={data} />
        <div className="lg:sticky lg:top-24 lg:self-start">
          <RecentFeed data={data} />
        </div>
      </div>

      <p className="text-xs text-abyss-muted">
        Last refreshed {formatDate(data.fetchedAt)} · Data:{" "}
        <a
          href="https://obis.org"
          className="underline decoration-dotted underline-offset-2 hover:text-glow"
          target="_blank"
          rel="noopener noreferrer"
        >
          OBIS
        </a>{" "}
        &{" "}
        <a
          href="https://www.gbif.org"
          className="underline decoration-dotted underline-offset-2 hover:text-glow"
          target="_blank"
          rel="noopener noreferrer"
        >
          GBIF
        </a>{" "}
        · CC-BY. Signals are indicative of sampling effort, not absolute
        population counts.
      </p>
    </div>
  )
}

function StatBlock({ value, label }: { value: string; label: string }) {
  return (
    <div className="rounded-2xl border border-abyss-border bg-white/[0.03] p-5">
      <div className="font-serif text-3xl font-semibold tabular-nums text-glow">
        {value}
      </div>
      <div className="mt-1 text-sm text-abyss-muted">{label}</div>
    </div>
  )
}

export default function GuardianPage() {
  return (
    <div className="bg-abyss py-16 sm:py-20">
      <Container>
        <SectionHeading
          eyebrow="Guardian"
          tone="dark"
          title="Live signals from the open ocean record"
          description="The same keyless, open data streams the Ocean Intelligence System watches — surfaced as living context for the commons. Every number is sourced from OBIS and GBIF, cached for six hours, and marked unavailable rather than faked when a source goes quiet."
        />
        <div className="mt-14">
          <Suspense fallback={<SignalsSkeleton />}>
            <GuardianContent />
          </Suspense>
        </div>
      </Container>
    </div>
  )
}
