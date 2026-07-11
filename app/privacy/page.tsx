import type { Metadata } from "next"
import { ArrowRight, ButtonLink, Container, SectionHeading } from "@/components/primitives"
import { GITHUB_REPO_URL } from "@/lib/utils"

export const metadata: Metadata = {
  title: "Privacy & Transparency",
  description:
    "How Blue Life Commons serves public pages, handles contributions, reads scientific datasets, and exposes item-level citation and review state.",
  alternates: { canonical: "/privacy" },
  openGraph: { url: "/privacy" },
}

const BASELINE = [
  {
    title: "Public website delivery",
    body: "Vercel hosts and delivers this website. As with ordinary web hosting, request information such as IP address, user-agent, requested URL, timestamp, and security diagnostics may be processed to serve and protect a page. We do not publish a retention promise we have not independently verified.",
  },
  {
    title: "No browser identity layer",
    body: "The current site source does not install a browser analytics SDK, advertising pixel, account system, or visitor profile. It does not ask for an email address or hide a contribution form. If that baseline changes, this page and the relevant consent surface must change first.",
  },
  {
    title: "Approved public media",
    body: "Approved image files may be delivered from Vercel Blob. Rights, credit, review state, and source pointers remain in the repository. Candidate and reviewer-only media are not intended for public rendering.",
  },
]

const DATA_BOUNDARIES = [
  {
    label: "Repository artifacts",
    detail:
      "Blue Life Commons renders versioned Markdown and metadata from this repository. Each artifact keeps its own sources, license, contributors, status, and applicable review fields.",
  },
  {
    label: "OBIS and GBIF signals",
    detail:
      "The Guardian route reads public OBIS and GBIF API responses on the server and presents source-labelled counts or availability. The upstream providers and dataset publishers remain authoritative for source records, terms, corrections, and provenance; this site does not claim ownership or control of those records.",
  },
  {
    label: "External destinations",
    detail:
      "GitHub, dataset sources, media sources, sponsors, and partner links are separate destinations. Following a link sends a request to that operator under its own terms and privacy materials. A link does not make every destination a Blue Life Commons processor or partner.",
  },
]

export default function PrivacyPage() {
  return (
    <main>
      <div className="border-b border-border bg-secondary">
        <Container className="py-14 sm:py-20">
          <SectionHeading
            eyebrow="Privacy & transparency"
            title="The public surface, without hidden machinery"
            description="What this site handles today, where contributions go, and where the commons stops and upstream scientific systems begin."
          />
          <div className="mt-8 flex flex-wrap gap-3">
            <ButtonLink
              href={`${GITHUB_REPO_URL}/issues/new/choose`}
              variant="primary"
              external
            >
              Contribute on GitHub
              <ArrowRight />
            </ButtonLink>
            <ButtonLink href={`${GITHUB_REPO_URL}/pulls`} variant="secondary" external>
              Review open pull requests
            </ButtonLink>
          </div>
        </Container>
      </div>

      <Container className="py-12 sm:py-16">
        <section aria-labelledby="baseline-heading">
          <div className="max-w-3xl">
            <h2
              id="baseline-heading"
              className="font-serif text-2xl font-semibold text-foreground"
            >
              Current technical baseline
            </h2>
            <p className="mt-3 text-sm leading-relaxed text-muted-foreground">
              This is a source-based description of the deployed public site,
              not a promise about features that may exist later.
            </p>
          </div>
          <div className="mt-6 grid gap-4 lg:grid-cols-3">
            {BASELINE.map((item) => (
              <article key={item.title} className="rounded-2xl border border-border bg-card p-6">
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

        <section aria-labelledby="contribution-heading" className="mt-16">
          <div className="grid gap-8 rounded-2xl border border-border bg-abyss p-6 text-abyss-foreground sm:p-8 lg:grid-cols-[0.9fr_1.1fr] lg:items-start">
            <div>
              <span className="text-xs font-semibold uppercase tracking-[0.16em] text-glow">
                Contribution boundary
              </span>
              <h2 id="contribution-heading" className="mt-3 font-serif text-2xl font-semibold">
                GitHub is the intake and review record
              </h2>
              <p className="mt-3 text-sm leading-relaxed text-abyss-muted">
                This website does not collect contribution text, field records,
                files, email addresses, or grant applications. Contribution
                calls hand off to a GitHub issue or pull request, where the
                submitter can see the repository record and review history.
              </p>
            </div>
            <ol className="grid gap-3">
              {[
                "Start from a repository issue or the documented contribution template.",
                "Put sources, rights, sensitivity, and required review state in the artifact metadata.",
                "Open a pull request. CI and human reviewers inspect the item before its status can advance.",
                "The public site renders the merged repository state; it is not a second source of truth.",
              ].map((step, index) => (
                <li key={step} className="flex gap-3 rounded-xl border border-abyss-border bg-white/5 p-4">
                  <span className="flex size-7 shrink-0 items-center justify-center rounded-full bg-glow text-xs font-semibold text-abyss-deep">
                    {index + 1}
                  </span>
                  <span className="pt-1 text-sm leading-relaxed text-abyss-foreground">
                    {step}
                  </span>
                </li>
              ))}
            </ol>
          </div>
        </section>

        <section aria-labelledby="data-heading" className="mt-16">
          <h2 id="data-heading" className="font-serif text-2xl font-semibold text-foreground">
            Scientific data and controller boundaries
          </h2>
          <p className="mt-3 max-w-3xl text-sm leading-relaxed text-muted-foreground">
            A citation or API read preserves a route back to the source. It does
            not transfer ownership, make the commons the authority for an
            upstream record, or turn a third-party dataset into a verified
            Blue Life Commons artifact.
          </p>
          <dl className="mt-6 divide-y divide-border overflow-hidden rounded-2xl border border-border bg-card">
            {DATA_BOUNDARIES.map((item) => (
              <div key={item.label} className="grid gap-2 p-5 sm:grid-cols-[220px_1fr] sm:gap-6 sm:p-6">
                <dt className="font-semibold text-foreground">{item.label}</dt>
                <dd className="text-sm leading-relaxed text-muted-foreground">{item.detail}</dd>
              </div>
            ))}
          </dl>
        </section>

        <section aria-labelledby="review-heading" className="mt-16">
          <div className="rounded-2xl border border-primary/25 bg-primary/6 p-6 sm:p-8">
            <span className="text-xs font-semibold uppercase tracking-[0.16em] text-primary">
              Item-level trust
            </span>
            <h2 id="review-heading" className="mt-3 font-serif text-2xl font-semibold text-foreground">
              Citation and review state travel with each artifact
            </h2>
            <div className="mt-4 grid gap-4 text-sm leading-relaxed text-muted-foreground lg:grid-cols-2">
              <p>
                Every artifact exposes its own status, source list, license,
                contributors, and applicable science, ethics, and editorial
                review fields. Readers should inspect that item-level evidence,
                including whether a gate is pending, required, approved, or not
                applicable.
              </p>
              <p>
                Blue Life Commons does not claim blanket ethics or scientific
                approval for the whole site. Ethics review is mandatory for
                artifacts involving animal interaction and for the other
                welfare-sensitive cases defined in the repository policy. A
                citation, link, or repository merge is not by itself an expert
                endorsement.
              </p>
            </div>
          </div>
        </section>

        <section aria-labelledby="choices-heading" className="mt-16 grid gap-5 lg:grid-cols-2">
          <article className="rounded-2xl border border-border bg-card p-6 sm:p-7">
            <h2 id="choices-heading" className="font-serif text-xl font-semibold text-foreground">
              Your choices
            </h2>
            <p className="mt-3 text-sm leading-relaxed text-muted-foreground">
              You can read the public site without creating a Blue Life Commons
              account. You can choose whether to follow an external link or
              contribute through GitHub. Do not include sensitive personal,
              clinical, or precise vulnerable-animal location data in a public
              issue; follow the repository sensitivity rules instead.
            </p>
          </article>
          <article className="rounded-2xl border border-border bg-card p-6 sm:p-7">
            <h2 className="font-serif text-xl font-semibold text-foreground">
              Corrections and questions
            </h2>
            <p className="mt-3 text-sm leading-relaxed text-muted-foreground">
              Open a GitHub issue to challenge a public claim, source, rights
              record, review state, or this transparency description. For an
              upstream occurrence record, use the correction path provided by
              the source dataset or publisher as well.
            </p>
            <a
              href={`${GITHUB_REPO_URL}/issues/new/choose`}
              target="_blank"
              rel="noopener noreferrer"
              className="mt-4 inline-flex items-center gap-2 text-sm font-semibold text-primary hover:underline"
            >
              Open the public issue tracker
              <ArrowRight />
            </a>
          </article>
        </section>

        <p className="mt-12 border-t border-border pt-6 text-xs leading-relaxed text-muted-foreground">
          Last reconciled with the public source on 2026-07-10. This page is an
          operational transparency statement, not a substitute for provider
          policies or jurisdiction-specific legal advice.
        </p>
      </Container>
    </main>
  )
}
