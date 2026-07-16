import type { Metadata } from "next"
import { ArrowRight, ButtonLink, Container, SectionHeading } from "@/components/primitives"
import { GITHUB_REPO_URL } from "@/lib/utils"

export const metadata: Metadata = {
  title: "Terms of use",
  description:
    "Terms for using Blue Life Commons: open content licensing, no warranties, external links, and contribution norms.",
  alternates: { canonical: "/terms" },
  openGraph: { url: "/terms" },
}

const SECTIONS = [
  {
    title: "Acceptable use",
    body: "You may browse, link to, and reuse public content according to the licenses stated on each artifact and in the repository. Do not use this site to harass wildlife, encourage illegal take, or present generated media as identification or legal evidence.",
  },
  {
    title: "Content license",
    body: "Unless a page or file says otherwise, written commons content is intended for reuse under Creative Commons Attribution 4.0 (CC BY 4.0). Give reasonable credit, link the license, and note changes. Media assets may carry different rights — follow the credit, license URL, and review fields on each record.",
  },
  {
    title: "No professional advice",
    body: "Blue Life Commons is educational and research-oriented. It is not legal, veterinary, navigational, or conservation-management advice for a specific operation. Primary sources and qualified practitioners remain authoritative.",
  },
  {
    title: "No warranty",
    body: "The site and repository are provided “as is.” Records may be incomplete, outdated, or marked needs-expert-review. We do not warrant fitness for a particular purpose or uninterrupted availability.",
  },
  {
    title: "External destinations",
    body: "Links to GitHub, scientific datasets (for example OBIS or GBIF), partners, and other operators are third-party destinations under their own terms and privacy policies. Linking does not create a partnership or endorsement beyond what is explicitly documented.",
  },
  {
    title: "Contributions",
    body: "Contributions happen through the public GitHub repository under its contribution and ethics rules. By opening a pull request you confirm you have the rights to submit the material and that factual claims include sources.",
  },
  {
    title: "Commercial services",
    body: "Optional Starlight implementation or services paths (where linked) are separate from free commons reading. Commercial terms, if any, are stated on those surfaces — not implied by browsing the commons.",
  },
  {
    title: "Changes",
    body: "These terms may be updated in the repository and on this page as the public surface evolves. Material changes should remain readable in Git history.",
  },
]

export default function TermsPage() {
  return (
    <main>
      <div className="border-b border-border bg-secondary">
        <Container className="py-14 sm:py-20">
          <SectionHeading
            eyebrow="Terms"
            title="Terms of use for the public commons"
            description="Plain-language rules for reading, reusing, and contributing. This is not a substitute for license text on individual artifacts or for professional advice."
          />
          <div className="mt-8 flex flex-wrap gap-3">
            <ButtonLink href="/privacy" variant="primary">
              Privacy &amp; transparency
              <ArrowRight />
            </ButtonLink>
            <ButtonLink href="/about" variant="secondary">
              About the commons
            </ButtonLink>
            <ButtonLink href={GITHUB_REPO_URL} variant="secondary" external>
              Repository
            </ButtonLink>
          </div>
        </Container>
      </div>

      <Container className="py-12 sm:py-16">
        <div className="grid gap-4 lg:grid-cols-2">
          {SECTIONS.map((item) => (
            <article
              key={item.title}
              className="rounded-2xl border border-border bg-card p-6"
            >
              <h2 className="font-serif text-lg font-semibold text-foreground">
                {item.title}
              </h2>
              <p className="mt-3 text-sm leading-relaxed text-muted-foreground">
                {item.body}
              </p>
            </article>
          ))}
        </div>
        <p className="mt-10 max-w-3xl text-xs leading-relaxed text-muted-foreground">
          Last updated for public route hygiene on 2026-07-16. Prefer the
          repository license files and per-artifact metadata when they are more
          specific than this page.
        </p>
      </Container>
    </main>
  )
}
