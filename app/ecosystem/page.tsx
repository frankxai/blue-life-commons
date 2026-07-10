import type { Metadata } from "next"
import { Container, SectionHeading, ButtonLink, ArrowRight } from "@/components/primitives"
import { GITHUB_REPO_URL, OCEAN_INTEL_URL } from "@/lib/utils"

export const metadata: Metadata = {
  title: "Ecosystem",
  description:
    "How Blue Life Commons and the Ocean Intelligence System fit together: the commons is the trust layer, the intelligence system is the sensing layer, and GitHub is the ledger between them.",
}

const LAYERS = [
  {
    name: "Blue Life Commons",
    tag: "Trust layer — this site",
    body: "Source-linked, review-gated, CC BY intelligence artifacts: species pages, region briefings, missions, dataset cards, and welfare assessments. Review state remains visible.",
    href: GITHUB_REPO_URL,
    linkLabel: "blue-life-commons",
  },
  {
    name: "Ocean Intelligence System",
    tag: "Sensing layer",
    body: "Open connectors and agents that watch OBIS, GBIF, NOAA and other live sources — detecting signals, drafting updates, and proposing changes to the commons as pull requests.",
    href: OCEAN_INTEL_URL,
    linkLabel: "ocean-intelligence-system",
  },
  {
    name: "GitHub",
    tag: "Ledger & governance",
    body: "The single source of truth. Contributions arrive as PRs, review happens in the open, CI validates every artifact against the schema, and merged changes publish here automatically.",
    href: GITHUB_REPO_URL,
    linkLabel: "The repository",
  },
]

const FLOW = [
  "A sensor, researcher or citizen produces a signal",
  "The intelligence system (or a human) drafts an artifact",
  "Required reviewers inspect sources, welfare, rights, and schema",
  "CI validates; approved merges become publication candidates",
  "This site renders it; Guardian keeps it living",
  "Approved outcomes can enter the public impact ledger",
]

export default function EcosystemPage() {
  return (
    <main>
      <div className="border-b border-border bg-secondary">
        <Container className="py-14 sm:py-20">
          <SectionHeading
            eyebrow="Ecosystem"
            title="Three layers, one loop"
            description="The commons is not a website with a repo behind it. It is a repo with a website in front of it — and an intelligence system feeding it."
          />
        </Container>
      </div>

      <Container className="py-12 sm:py-16">
        <div className="grid gap-5 lg:grid-cols-3">
          {LAYERS.map((l, i) => (
            <div key={l.name} className="flex flex-col rounded-2xl border border-border bg-card p-6 sm:p-7">
              <span className="font-serif text-4xl font-semibold text-primary/25" aria-hidden>
                {String(i + 1).padStart(2, "0")}
              </span>
              <h2 className="mt-3 font-serif text-xl font-semibold text-foreground">
                {l.name}
              </h2>
              <p className="mt-1 text-xs font-semibold uppercase tracking-[0.12em] text-primary">
                {l.tag}
              </p>
              <p className="mt-3 flex-1 text-sm leading-relaxed text-muted-foreground">
                {l.body}
              </p>
              <a
                href={l.href}
                target="_blank"
                rel="noopener noreferrer"
                className="mt-5 inline-flex items-center gap-1.5 text-sm font-semibold text-primary hover:underline"
              >
                {l.linkLabel}
                <ArrowRight className="h-3.5 w-3.5" />
              </a>
            </div>
          ))}
        </div>

        <section className="mt-16" aria-labelledby="flow-heading">
          <SectionHeading
            eyebrow="The loop"
            title="From signal to sustained impact"
          />
          <ol className="mt-8 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
            {FLOW.map((step, i) => (
              <li key={step} className="flex items-start gap-4 rounded-2xl border border-border bg-card p-5">
                <span className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-primary/10 font-serif text-sm font-semibold text-primary">
                  {i + 1}
                </span>
                <span className="pt-1 text-sm leading-relaxed text-foreground">{step}</span>
              </li>
            ))}
          </ol>
        </section>

        <div className="mt-16 rounded-2xl border border-border bg-secondary p-6 sm:p-8">
          <h2 className="font-serif text-xl font-semibold text-foreground">
            Build on it
          </h2>
          <p className="mt-2 max-w-2xl text-sm leading-relaxed text-muted-foreground">
            Both layers are open source. Fork the commons, run the intelligence
            system against your own waters, or contribute connectors back
            upstream.
          </p>
          <div className="mt-5 flex flex-wrap gap-3">
            <ButtonLink href={GITHUB_REPO_URL} variant="primary" external>
              Commons repository
              <ArrowRight />
            </ButtonLink>
            <ButtonLink href={OCEAN_INTEL_URL} variant="secondary" external>
              Intelligence system
            </ButtonLink>
          </div>
        </div>
      </Container>
    </main>
  )
}
