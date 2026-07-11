import type { Metadata } from "next"
import { Container, SectionHeading, ButtonLink, ArrowRight } from "@/components/primitives"
import { GITHUB_REPO_URL } from "@/lib/utils"

export const metadata: Metadata = {
  title: "Contribute",
  description:
    "Turn ocean curiosity into sourced, review-gated knowledge. Pathways for citizens, researchers, educators and engineers to contribute to the Blue Life Commons.",
  alternates: { canonical: "/contribute" },
  openGraph: { url: "/contribute" },
}

const PATHWAYS = [
  {
    audience: "Citizens & divers",
    title: "Log what you see",
    body: "Submit field observations, licensed photos, and encounter notes. Sensitivity-aware records can strengthen species and region pages after review.",
    steps: [
      "Open a Field Observation issue on GitHub",
      "Add a region-level location, date, species and evidence",
      "A reviewer links it to the right artifacts",
    ],
  },
  {
    audience: "Researchers",
    title: "Publish an intelligence artifact",
    body: "Contribute a species page, region briefing, dataset card or research summary. Every claim is cited, review state stays visible, and authorship remains in Git history.",
    steps: [
      "Fork the repo and copy a template",
      "Write with sources and a welfare note",
      "Open a PR for expert review",
    ],
  },
  {
    audience: "Educators",
    title: "Adapt for the classroom",
    body: "Everything is CC-BY-4.0. Remix pages into lessons, translate them, or design missions that send students into the field with a clear ethical protocol.",
    steps: [
      "Reuse any artifact with attribution",
      "Propose an education-audience mission",
      "Share back what worked",
    ],
  },
  {
    audience: "Engineers",
    title: "Build the intelligence layer",
    body: "Improve the schema, the validators, the connectors, or this very website. The commons and its tooling are open source end to end.",
    steps: [
      "Browse good-first-issue labels",
      "Extend a connector or the schema",
      "Ship a PR with tests",
    ],
  },
]

export default function ContributePage() {
  return (
    <main>
      <div className="border-b border-border bg-secondary">
        <Container className="py-14 sm:py-20">
          <SectionHeading
            eyebrow="Contribute"
            title="Turn curiosity into commons"
            description="Every artifact here was contributed by someone who cared enough to source it. There is a pathway for exactly who you are."
          />
          <div className="mt-8 flex flex-wrap gap-3">
            <ButtonLink href={`${GITHUB_REPO_URL}/issues/new/choose`} variant="primary" external>
              Start on GitHub
              <ArrowRight />
            </ButtonLink>
            <ButtonLink href="/catalog" variant="secondary">
              See what exists
            </ButtonLink>
          </div>
        </Container>
      </div>

      <Container className="py-12 sm:py-16">
        <div className="grid gap-5 lg:grid-cols-2">
          {PATHWAYS.map((p) => (
            <article
              key={p.audience}
              className="flex flex-col rounded-2xl border border-border bg-card p-6 sm:p-7"
            >
              <span className="text-xs font-semibold uppercase tracking-[0.16em] text-primary">
                {p.audience}
              </span>
              <h2 className="mt-2 font-serif text-2xl font-semibold text-foreground">
                {p.title}
              </h2>
              <p className="mt-3 text-sm leading-relaxed text-muted-foreground">
                {p.body}
              </p>
              <ol className="mt-5 flex flex-col gap-2.5 border-t border-border pt-5">
                {p.steps.map((s, i) => (
                  <li key={s} className="flex items-start gap-3 text-sm text-foreground">
                    <span className="flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-primary/10 text-xs font-semibold text-primary">
                      {i + 1}
                    </span>
                    <span className="pt-0.5">{s}</span>
                  </li>
                ))}
              </ol>
            </article>
          ))}
        </div>

        <div className="mt-14 rounded-2xl border border-border bg-secondary p-6 sm:p-8">
          <h2 className="font-serif text-xl font-semibold text-foreground">
            The one rule: cite or stay silent
          </h2>
          <p className="mt-2 max-w-2xl text-sm leading-relaxed text-muted-foreground">
            The commons would rather say nothing than say something unsourced.
            Every factual claim carries a citation, every welfare-sensitive
            page carries a review, and every contributor is credited. That is
            what makes this trustworthy enough to build on.
          </p>
          <a
            href={`${GITHUB_REPO_URL}/blob/main/docs/contributor-onboarding.md`}
            target="_blank"
            rel="noopener noreferrer"
            className="mt-4 inline-flex items-center gap-2 text-sm font-semibold text-primary hover:underline"
          >
            Read the contributor onboarding guide
            <ArrowRight />
          </a>
        </div>
      </Container>
    </main>
  )
}
