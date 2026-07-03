import type { Metadata } from "next"
import { getDocHtml } from "@/lib/content"
import { Container, SectionHeading } from "@/components/primitives"
import { GITHUB_REPO_URL } from "@/lib/utils"

export const metadata: Metadata = {
  title: "Governance & Ethics",
  description:
    "How the Blue Life Commons is governed: staged governance, welfare-first ethics, transparent funding architecture, and decisions recorded in public on GitHub.",
}

const PRINCIPLES = [
  {
    title: "Staged governance",
    body: "Benevolent architecture first. Formal governance arrives only when there is real treasury, real contributors, and real decisions to make — not before.",
  },
  {
    title: "Decisions in public",
    body: "Every decision that shapes the commons is recorded in GitHub issues and pull requests. There is no private roadmap.",
  },
  {
    title: "Welfare before content",
    body: "Science-sensitive and welfare-sensitive pages require expert review before publishing. The commons never trades animal welfare for engagement.",
  },
  {
    title: "The commons stays free",
    body: "Every artifact is CC-BY-4.0, forever. Funding sustains the work — it never paywalls the knowledge.",
  },
]

export default function GovernancePage() {
  const governance = getDocHtml("governance/README.md")
  const funding = getDocHtml("governance/funding.md")

  return (
    <main>
      <div className="border-b border-border bg-secondary">
        <Container className="py-14 sm:py-20">
          <SectionHeading
            eyebrow="Governance & ethics"
            title="Run in the open, accountable by design"
            description="The commons is governed in stages that match its real maturity — with every decision, review, and dollar recorded in public."
          />
        </Container>
      </div>

      <Container className="py-12 sm:py-16">
        <div className="grid gap-4 sm:grid-cols-2">
          {PRINCIPLES.map((p) => (
            <div
              key={p.title}
              className="rounded-2xl border border-border bg-card p-6"
            >
              <h2 className="font-serif text-lg font-semibold text-foreground">
                {p.title}
              </h2>
              <p className="mt-2 text-sm leading-relaxed text-muted-foreground">
                {p.body}
              </p>
            </div>
          ))}
        </div>

        <div className="mt-16 grid gap-12 lg:grid-cols-2">
          {governance && (
            <section aria-labelledby="gov-doc">
              <h2
                id="gov-doc"
                className="text-xs font-semibold uppercase tracking-[0.16em] text-primary"
              >
                Governance model
              </h2>
              <div
                className="prose-ocean mt-4"
                dangerouslySetInnerHTML={{ __html: governance.html }}
              />
            </section>
          )}
          {funding && (
            <section aria-labelledby="funding-doc">
              <h2
                id="funding-doc"
                className="text-xs font-semibold uppercase tracking-[0.16em] text-primary"
              >
                Funding architecture
              </h2>
              <div
                className="prose-ocean mt-4"
                dangerouslySetInnerHTML={{ __html: funding.html }}
              />
            </section>
          )}
        </div>

        <div className="mt-16 rounded-2xl border border-border bg-secondary p-6 sm:p-8">
          <h2 className="font-serif text-xl font-semibold text-foreground">
            Read the source, not the summary
          </h2>
          <p className="mt-2 max-w-2xl text-sm leading-relaxed text-muted-foreground">
            Everything on this page is rendered directly from the governance
            documents in the repository. If the site and the repo ever
            disagree, the repo wins.
          </p>
          <a
            href={`${GITHUB_REPO_URL}/tree/main/governance`}
            target="_blank"
            rel="noopener noreferrer"
            className="mt-4 inline-flex items-center gap-2 text-sm font-semibold text-primary hover:underline"
          >
            governance/ on GitHub
          </a>
        </div>
      </Container>
    </main>
  )
}
