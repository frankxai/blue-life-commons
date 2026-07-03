import type { Metadata } from "next"
import Link from "next/link"
import { getAllArtifacts, getCommonsStats } from "@/lib/content"
import { Container, SectionHeading } from "@/components/primitives"
import { Chip, TypeChip } from "@/components/badges"
import { StatGrid } from "@/components/stat-grid"

export const metadata: Metadata = {
  title: "Impact Ledger",
  description:
    "A transparent ledger of what the commons has produced — verifiable impact claims drawn directly from each artifact, with hypercert eligibility.",
}

export default function ImpactPage() {
  const stats = getCommonsStats()
  const claims = getAllArtifacts()
    .filter((a) => a.impact?.claim)
    .sort((a, b) => (b.last_verified ?? "").localeCompare(a.last_verified ?? ""))

  return (
    <main>
      <div className="border-b border-border bg-secondary">
        <Container className="py-14 sm:py-20">
          <SectionHeading
            eyebrow="Impact ledger"
            title="Impact you can audit, not impact we assert"
            description="Every entry below is an impact claim written into an artifact's own metadata, reviewed in the open on GitHub. When impact funding mechanisms like hypercerts mature, these claims are the record they will settle against."
          />
        </Container>
      </div>

      <Container className="py-12 sm:py-16">
        <StatGrid
          stats={[
            { value: stats.total, label: "Artifacts in the commons" },
            { value: stats.sources, label: "Unique cited sources" },
            { value: claims.length, label: "Registered impact claims" },
            { value: stats.hypercertEligible, label: "Hypercert-eligible" },
          ]}
        />

        <section aria-labelledby="claims-heading" className="mt-14">
          <h2 id="claims-heading" className="font-serif text-2xl font-semibold text-foreground">
            The ledger
          </h2>
          <ol className="mt-6 flex flex-col gap-3">
            {claims.map((a) => (
              <li key={a.id}>
                <Link
                  href={a.href}
                  className="group flex flex-col gap-3 rounded-2xl border border-border bg-card p-5 transition-colors hover:border-primary/40 sm:flex-row sm:items-center sm:justify-between"
                >
                  <div className="flex min-w-0 flex-col gap-1.5">
                    <div className="flex flex-wrap items-center gap-2">
                      <TypeChip type={a.type} />
                      {a.impact?.eligible_for_hypercert && (
                        <Chip tone="primary">Hypercert-eligible</Chip>
                      )}
                    </div>
                    <p className="text-sm font-medium leading-relaxed text-foreground group-hover:text-primary">
                      {a.impact?.claim}
                    </p>
                    <p className="text-xs text-muted-foreground">
                      {a.title}
                      {a.last_verified ? ` · verified ${a.last_verified}` : ""}
                    </p>
                  </div>
                </Link>
              </li>
            ))}
          </ol>
        </section>

        <section className="mt-14 rounded-2xl border border-border bg-abyss p-8 text-abyss-foreground sm:p-10">
          <h2 className="font-serif text-2xl font-semibold">
            How impact becomes funding
          </h2>
          <div className="mt-6 grid gap-6 sm:grid-cols-3">
            {[
              {
                step: "01",
                title: "Claim",
                body: "Contributors register a specific, checkable impact claim inside the artifact itself \u2014 reviewed like any other change.",
              },
              {
                step: "02",
                title: "Verify",
                body: "Science, ethics and editorial review gates confirm the claim before it enters the ledger. Weak claims never ship.",
              },
              {
                step: "03",
                title: "Fund",
                body: "Sponsors fund concrete objects \u2014 a species guild, a region, a mission \u2014 and hypercerts can later certify who did the work.",
              },
            ].map((s) => (
              <div key={s.step}>
                <span className="font-mono text-sm text-glow">{s.step}</span>
                <h3 className="mt-2 font-serif text-lg font-semibold">{s.title}</h3>
                <p className="mt-2 text-sm leading-relaxed text-abyss-muted">{s.body}</p>
              </div>
            ))}
          </div>
        </section>
      </Container>
    </main>
  )
}
