import type { Metadata } from "next"
import { getAllArtifacts } from "@/lib/content"
import { Container, SectionHeading, ButtonLink, ArrowRight } from "@/components/primitives"
import { TransitionLink } from "@/components/transition-link"

export const metadata: Metadata = {
  title: "Support the Commons",
  description:
    "Support source gathering, expert review, ethical field methods, and public infrastructure while commons artifacts remain reusable under CC BY 4.0.",
}

const CHANNELS = [
  {
    name: "Open Collective",
    role: "Transparent-budget model",
    body: "Open Collective is one option for a future public budget and expense ledger. A Blue Life Commons collective is not represented as active here.",
    href: "https://opencollective.com",
    cta: "Learn about Open Collective",
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
    role: "Explore outcome records",
    body: "A review-complete artifact may become eligible for an outcome record after separate governance review. Eligibility metadata is not proof of impact or issuance.",
    href: "https://hypercerts.org",
    cta: "Learn about Hypercerts",
  },
]

export default function SupportPage() {
  const all = getAllArtifacts()
  const fundable = all
    .filter(
      (artifact) =>
        artifact.impact?.eligible_for_hypercert &&
        (artifact.status === "approved" || artifact.status === "published"),
    )
    .slice(0, 6)

  return (
    <main>
      <div className="border-b border-border bg-secondary">
        <Container className="py-14 sm:py-20">
          <SectionHeading
            eyebrow="Support"
            title="Fund evidenced work, not vague promises"
            description="Public artifacts carry a CC BY 4.0 reuse license. Support can sustain source gathering, expert review, ethical field methods, and data infrastructure without buying influence over scientific conclusions."
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
              title="Review-complete work eligible for further governance"
              description="These artifacts are both approved or published and flagged as potentially eligible in repository metadata. Issuance or funding still requires a separate human decision."
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
