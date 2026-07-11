import type { Metadata } from "next"
import Link from "next/link"
import { getAllArtifacts, getCommonsStats } from "@/lib/content"
import { Container, SectionHeading } from "@/components/primitives"
import { StatusPill, TypeChip } from "@/components/badges"
import { StatGrid } from "@/components/stat-grid"

export const metadata: Metadata = {
  title: "Impact Ledger",
  description:
    "A transparent ledger of review-complete public-good claims, with repository-derived output counts and visible artifact status.",
  alternates: { canonical: "/impact" },
  openGraph: { url: "/impact" },
}

export default function ImpactPage() {
  const stats = getCommonsStats()
  const registeredClaims = getAllArtifacts().filter((artifact) => artifact.impact?.claim)
  const claims = registeredClaims
    .filter((artifact) => artifact.status === "approved" || artifact.status === "published")
    .sort((a, b) => (b.last_verified ?? "").localeCompare(a.last_verified ?? ""))
  const claimsInReview = registeredClaims.length - claims.length

  return (
    <main>
      <div className="border-b border-border bg-secondary">
        <Container className="py-14 sm:py-20">
          <SectionHeading
            eyebrow="Impact ledger"
            title="Impact you can audit, not impact we assert"
            description="This ledger publishes only claims attached to approved or published artifacts. Registered claims stay out while their science, ethics, editorial, rights, or sensitivity review remains open."
          />
        </Container>
      </div>

      <Container className="py-12 sm:py-16">
        <StatGrid
          stats={[
            { value: stats.total, label: "Artifacts in the commons" },
            { value: stats.sources, label: "Unique cited sources" },
            { value: stats.reviewed, label: "Approved or published artifacts" },
            { value: claimsInReview, label: "Registered claims still in review" },
          ]}
        />

        <section aria-labelledby="claims-heading" className="mt-14">
          <h2 id="claims-heading" className="font-serif text-2xl font-semibold text-foreground">
            The published ledger
          </h2>
          {claims.length > 0 ? (
            <ol className="mt-6 flex flex-col gap-3">
              {claims.map((artifact) => (
                <li key={artifact.id}>
                  <Link
                    href={artifact.href}
                    className="group flex flex-col gap-3 rounded-2xl border border-border bg-card p-5 transition-colors hover:border-primary/40 sm:flex-row sm:items-center sm:justify-between"
                  >
                    <div className="flex min-w-0 flex-col gap-1.5">
                      <div className="flex flex-wrap items-center gap-2">
                        <TypeChip type={artifact.type} />
                        <StatusPill status={artifact.status} />
                      </div>
                      <p className="text-sm font-medium leading-relaxed text-foreground group-hover:text-primary">
                        {artifact.impact?.claim}
                      </p>
                      <p className="text-xs text-muted-foreground">
                        {artifact.title}
                        {artifact.last_verified ? ` · verified ${artifact.last_verified}` : ""}
                      </p>
                    </div>
                  </Link>
                </li>
              ))}
            </ol>
          ) : (
            <div className="mt-6 rounded-2xl border border-border bg-secondary p-6">
              <p className="font-medium text-foreground">No claim has cleared every publication gate yet.</p>
              <p className="mt-2 max-w-2xl text-sm leading-relaxed text-muted-foreground">
                {claimsInReview} registered {claimsInReview === 1 ? "claim remains" : "claims remain"} in
                the review queue. This zero is intentional: repository activity is measurable, but it is
                not presented as verified real-world impact before approval.
              </p>
            </div>
          )}
        </section>

        <section className="mt-14 rounded-2xl border border-border bg-abyss p-8 text-abyss-foreground sm:p-10">
          <h2 className="font-serif text-2xl font-semibold">
            How a claim becomes a public outcome
          </h2>
          <div className="mt-6 grid gap-6 sm:grid-cols-3">
            {[
              {
                step: "01",
                title: "Register",
                body: "A contributor records a specific, checkable claim inside artifact metadata with sources and named review requirements.",
              },
              {
                step: "02",
                title: "Review",
                body: "Science, ethics, editorial, rights, and sensitivity gates remain visible. A pending claim does not enter the published ledger.",
              },
              {
                step: "03",
                title: "Reuse",
                body: "An approved or published artifact can be cited, reused under its license, corrected upstream, and measured against its source record.",
              },
            ].map((item) => (
              <div key={item.step}>
                <span className="font-mono text-sm text-glow">{item.step}</span>
                <h3 className="mt-2 font-serif text-lg font-semibold">{item.title}</h3>
                <p className="mt-2 text-sm leading-relaxed text-abyss-muted">{item.body}</p>
              </div>
            ))}
          </div>
        </section>
      </Container>
    </main>
  )
}
