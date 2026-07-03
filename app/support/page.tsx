import type { Metadata } from "next"
import { getAllArtifacts } from "@/lib/content"
import { Container, SectionHeading, ButtonLink, ArrowRight } from "@/components/primitives"
import { TransitionLink } from "@/components/transition-link"

export const metadata: Metadata = {
  title: "Support the Commons",
  description:
    "Fund specific, evidenced ocean intelligence work — not vague donation asks. Open Collective, GitHub Sponsors, and Hypercert impact records. The commons stays free, forever.",
}

const CHANNELS = [
  {
    name: "Open Collective",
    role: "Fiat donations & transparent budget",
    body: "One-time or recurring contributions with a public ledger. Every expense the commons makes is visible to everyone.",
    href: "https://opencollective.com",
    cta: "Contribute via Open Collective",
  },
  {
    name: "GitHub Sponsors",
    role: "Sustain the maintainers",
    body: "Directly fund the people who review artifacts, maintain the schema, and keep the intelligence layer running.",
    href: "https://github.com/sponsors/frankxai",
    cta: "Sponsor on GitHub",
  },
  {
    name: "Hypercerts",
    role: "Own a record of real impact",
    body: "Completed, evidenced work — a reviewed species guild, a shipped mission protocol — is minted as a Hypercert impact record. Fund outcomes, not promises.",
    href: "https://hypercerts.org",
    cta: "Learn about Hypercerts",
  },
]

export default function SupportPage() {
  const all = getAllArtifacts()
  const fundable = all.filter((a) => a.impact?.eligible_for_hypercert).slice(0, 6)

  return (
    <main>
      <div className="border-b border-border bg-secondary">
        <Container className="py-14 sm:py-20">
          <SectionHeading
            eyebrow="Support"
            title="Fund evidenced work, not vague promises"
            description="The commons stays free and CC-BY forever. What needs funding is the work: expert review, field missions, data infrastructure. Every fundable object below is specific, evidenced, and recorded in public."
          />
        </Container>
      </div>

      <Container className="py-12 sm:py-16">
        <div className="grid gap-5 md:grid-cols-3">
          {CHANNELS.map((c) => (
            <div
              key={c.name}
              className="flex flex-col rounded-2xl border border-border bg-card p-6"
            >
              <h2 className="font-serif text-xl font-semibold text-foreground">
                {c.name}
              </h2>
              <p className="mt-1 text-xs font-semibold uppercase tracking-[0.12em] text-primary">
                {c.role}
              </p>
              <p className="mt-3 flex-1 text-sm leading-relaxed text-muted-foreground">
                {c.body}
              </p>
              <ButtonLink href={c.href} variant="secondary" external className="mt-5 self-start">
                {c.cta}
              </ButtonLink>
            </div>
          ))}
        </div>

        {fundable.length > 0 && (
          <section className="mt-16" aria-labelledby="fundable-heading">
            <SectionHeading
              eyebrow="Fundable impact objects"
              title="Work that is ready to be backed"
              description="These artifacts are flagged Hypercert-eligible in the commons itself — real, reviewable units of impact with named contributors and cited evidence."
            />
            <div className="mt-8 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
              {fundable.map((a) => (
                <TransitionLink
                  key={a.id}
                  href={a.href}
                  className="group rounded-2xl border border-border bg-card p-5 transition-colors hover:border-primary/40"
                >
                  <span className="text-xs font-semibold uppercase tracking-[0.12em] text-primary">
                    {a.type.replace(/-/g, " ")}
                  </span>
                  <h3 className="mt-2 font-serif text-lg font-semibold leading-snug text-foreground group-hover:text-primary">
                    {a.title}
                  </h3>
                  <p className="mt-2 line-clamp-2 text-sm text-muted-foreground">
                    {a.excerpt}
                  </p>
                </TransitionLink>
              ))}
            </div>
          </section>
        )}

        <div className="mt-16 rounded-2xl border border-border bg-secondary p-6 sm:p-8">
          <h2 className="font-serif text-xl font-semibold text-foreground">
            What your support never buys
          </h2>
          <p className="mt-2 max-w-2xl text-sm leading-relaxed text-muted-foreground">
            No paywalls. No tokens. No influence over scientific conclusions.
            Funding sustains the commons — it does not steer it. That
            separation is written into the{" "}
            <TransitionLink href="/governance" className="font-semibold text-primary hover:underline">
              governance model
            </TransitionLink>
            , and it is non-negotiable.
          </p>
          <div className="mt-5 flex flex-wrap gap-3">
            <ButtonLink href="/services" variant="primary">
              Need a marine intelligence system built?
              <ArrowRight />
            </ButtonLink>
          </div>
        </div>
      </Container>
    </main>
  )
}
