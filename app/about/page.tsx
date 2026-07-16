import type { Metadata } from "next"
import { ArrowRight, ButtonLink, Container, SectionHeading } from "@/components/primitives"
import { GITHUB_REPO_URL } from "@/lib/utils"

export const metadata: Metadata = {
  title: "About",
  description:
    "What Blue Life Commons is: an open, source-led ocean intelligence commons with citations, review state, rights metadata, and Git history.",
  alternates: { canonical: "/about" },
  openGraph: { url: "/about" },
}

const PILLARS = [
  {
    title: "Source-led by default",
    body: "Every public artifact is expected to carry citations. If a claim cannot be sourced, it stays out of the public record rather than being invented for polish.",
  },
  {
    title: "Review state is visible",
    body: "Records publish with explicit review posture — not a flattened “approved” marketing claim. Needs-expert-review content remains honest about what is still open.",
  },
  {
    title: "Rights and media stay legible",
    body: "Approved media keeps credit, license, and source pointers. Candidate or reviewer-only media is not presented as identification or conservation evidence.",
  },
  {
    title: "Git is the continuity layer",
    body: "The commons is a repository first. History, PRs, issues, and licenses are part of the product surface — not back-office afterthoughts.",
  },
]

export default function AboutPage() {
  return (
    <main>
      <div className="border-b border-border bg-secondary">
        <Container className="py-14 sm:py-20">
          <SectionHeading
            eyebrow="About"
            title="The open intelligence commons for ocean life"
            description="Blue Life Commons is a public, source-led library of ocean intelligence: species and region briefings, missions, research pointers, and media records that keep provenance visible from GitHub to the public site."
          />
          <div className="mt-8 flex flex-wrap gap-3">
            <ButtonLink href="/catalog" variant="primary">
              Browse the catalog
              <ArrowRight />
            </ButtonLink>
            <ButtonLink href="/contribute" variant="secondary">
              How to contribute
            </ButtonLink>
            <ButtonLink href={GITHUB_REPO_URL} variant="secondary" external>
              Open the repository
            </ButtonLink>
          </div>
        </Container>
      </div>

      <Container className="py-12 sm:py-16">
        <section aria-labelledby="what-heading" className="max-w-3xl">
          <h2
            id="what-heading"
            className="font-serif text-2xl font-semibold text-foreground"
          >
            What this is — and is not
          </h2>
          <p className="mt-3 text-sm leading-relaxed text-muted-foreground">
            Blue Life Commons is stewarded as a public good by Starlight
            Intelligence Systems. It is not a wildlife translation product, not
            a closed commercial encyclopedia, and not a place for unsourced
            population or threat claims. Free reading and reuse under CC BY 4.0
            stay open; deeper implementation work for teams routes through
            Starlight services when that is the honest path.
          </p>
        </section>

        <section aria-labelledby="pillars-heading" className="mt-14">
          <h2
            id="pillars-heading"
            className="font-serif text-2xl font-semibold text-foreground"
          >
            Operating pillars
          </h2>
          <div className="mt-6 grid gap-4 md:grid-cols-2">
            {PILLARS.map((item) => (
              <article
                key={item.title}
                className="rounded-2xl border border-border bg-card p-6"
              >
                <h3 className="font-serif text-lg font-semibold text-foreground">
                  {item.title}
                </h3>
                <p className="mt-3 text-sm leading-relaxed text-muted-foreground">
                  {item.body}
                </p>
              </article>
            ))}
          </div>
        </section>

        <section aria-labelledby="next-heading" className="mt-14 max-w-3xl">
          <h2
            id="next-heading"
            className="font-serif text-2xl font-semibold text-foreground"
          >
            Where to go next
          </h2>
          <ul className="mt-4 space-y-2 text-sm leading-relaxed text-muted-foreground">
            <li>
              <a className="underline underline-offset-2 hover:text-foreground" href="/governance">
                Governance &amp; ethics
              </a>{" "}
              — contribution and review posture
            </li>
            <li>
              <a className="underline underline-offset-2 hover:text-foreground" href="/privacy">
                Privacy &amp; transparency
              </a>{" "}
              — what the public site processes today
            </li>
            <li>
              <a className="underline underline-offset-2 hover:text-foreground" href="/terms">
                Terms of use
              </a>{" "}
              — reuse, no-warranty, and external links
            </li>
            <li>
              <a className="underline underline-offset-2 hover:text-foreground" href="/support">
                Support the commons
              </a>{" "}
              — sustain open publication
            </li>
          </ul>
        </section>
      </Container>
    </main>
  )
}
