import type { Artifact } from "@/lib/types"
import { Container } from "@/components/primitives"
import {
  Chip,
  IucnBadge,
  ReviewDot,
  SourceTierChip,
  StatusPill,
  TypeChip,
  WelfareBadge,
} from "@/components/badges"
import { ArtifactCard } from "@/components/artifact-card"
import { ArtifactHeroMedia } from "@/components/artifact-media"
import { getApprovedSpeciesMedia } from "@/lib/media"
import { GITHUB_REPO_URL, cn, formatRegion } from "@/lib/utils"
import Link from "next/link"

function Breadcrumb({ trail }: { trail: { label: string; href?: string }[] }) {
  return (
    <nav aria-label="Breadcrumb" className="text-sm text-muted-foreground">
      <ol className="flex flex-wrap items-center gap-1.5">
        {trail.map((item, i) => (
          <li key={item.label} className="flex items-center gap-1.5">
            {i > 0 && <span aria-hidden>/</span>}
            {item.href ? (
              <Link href={item.href} className="transition-colors hover:text-primary">
                {item.label}
              </Link>
            ) : (
              <span aria-current="page" className="text-foreground">
                {item.label}
              </span>
            )}
          </li>
        ))}
      </ol>
    </nav>
  )
}

function MetaRow({ label, value }: { label: string; value?: React.ReactNode }) {
  if (!value) return null
  return (
    <div className="flex items-baseline justify-between gap-4 text-sm">
      <dt className="shrink-0 text-muted-foreground">{label}</dt>
      <dd className="text-right font-medium text-foreground">{value}</dd>
    </div>
  )
}

function BridgeRail({ artifact }: { artifact: Artifact }) {
  // folder-based guild from path
  const parts = artifact.path.split(/[/\\]/)
  const idx = parts.indexOf("species")
  const guild = idx >= 0 && parts[idx + 1] ? parts[idx + 1] : "other"

  if (guild === "marine-reptiles") {
    return (
      <div className="mt-5 rounded-xl border border-primary/20 bg-primary/8 p-4">
        <h3 className="text-xs font-semibold uppercase tracking-[0.16em] text-primary">
          Deep Time bridge
        </h3>
        <p className="mt-2 text-sm leading-relaxed text-foreground">
          This entry is a Mesozoic marine reptile — not a dinosaur. Compare body
          plans with living ocean apex predators and sea turtles.
        </p>
        <div className="mt-3 flex flex-col gap-2 text-sm font-semibold">
          <Link href="/species/deep-time" className="text-primary hover:underline">
            Deep Time hub
          </Link>
          <Link
            href="/species/sharks-rays/great-white-shark"
            className="text-primary hover:underline"
          >
            Living: great white shark
          </Link>
          <Link
            href="/species/turtles/leatherback-turtle"
            className="text-primary hover:underline"
          >
            Living: leatherback turtle
          </Link>
        </div>
      </div>
    )
  }

  if (guild === "sharks-rays" || guild === "cetaceans" || guild === "turtles") {
    return (
      <div className="mt-5 rounded-xl border border-border bg-secondary p-4">
        <h3 className="text-xs font-semibold uppercase tracking-[0.16em] text-primary">
          Through deep time
        </h3>
        <p className="mt-2 text-sm leading-relaxed text-muted-foreground">
          Curious about “ocean dinosaurs”? Start with Mesozoic marine reptiles —
          mosasaurs, plesiosaurs, and ichthyosaurs — in the Deep Time section.
        </p>
        <Link
          href="/species/deep-time"
          className="mt-3 inline-flex text-sm font-semibold text-primary hover:underline"
        >
          Open Deep Time hub
        </Link>
      </div>
    )
  }

  return null
}

export function ArtifactDetail({
  artifact,
  trail,
  related,
}: {
  artifact: Artifact
  trail: { label: string; href?: string }[]
  related: Artifact[]
}) {
  const a = artifact
  const editUrl = `${GITHUB_REPO_URL}/blob/main/${a.githubPath}`
  const approvedMedia = getApprovedSpeciesMedia(a)
  const impactIsPublished = a.status === "approved" || a.status === "published"
  const parts = a.path.split(/[/\\]/)
  const spIdx = parts.indexOf("species")
  const guildFolder = spIdx >= 0 && parts[spIdx + 1] ? parts[spIdx + 1] : ""

  return (
    <article>
      <header className="border-b border-border bg-secondary">
        <Container className="py-10 sm:py-14">
          <Breadcrumb trail={trail} />
          <div
            className={cn(
              "mt-6 grid gap-8",
              approvedMedia &&
                "lg:grid-cols-[minmax(0,1fr)_minmax(320px,460px)] lg:items-end",
            )}
          >
            <div>
              <div className="flex flex-wrap items-center gap-2">
                <TypeChip type={a.type} />
                <StatusPill status={a.status} />
                {guildFolder === "marine-reptiles" && (
                  <Chip tone="primary">Deep Time</Chip>
                )}
                {a.sensitivity?.tier === "sensitive" && (
                  <Chip tone="accent">Location generalized</Chip>
                )}
              </div>
              <h1 className="mt-4 max-w-3xl text-balance font-serif text-3xl font-semibold leading-tight tracking-tight text-foreground sm:text-4xl lg:text-5xl">
                {a.title}
              </h1>
              <div className="mt-5 flex flex-wrap items-center gap-3">
                <IucnBadge category={a.iucn?.category} />
                <WelfareBadge state={a.welfare?.state} />
                {a.region?.map((r) => (
                  <Chip key={r} tone="primary">
                    {formatRegion(r)}
                  </Chip>
                ))}
              </div>
            </div>
            <ArtifactHeroMedia artifact={a} />
          </div>
        </Container>
      </header>

      <Container className="py-10 sm:py-14">
        <div className="grid gap-12 lg:grid-cols-[minmax(0,1fr)_320px]">
          <div>
            <div
              className="prose-ocean"
              dangerouslySetInnerHTML={{ __html: a.bodyHtml }}
            />
          </div>

          <aside className="lg:sticky lg:top-24 lg:self-start" aria-label="Provenance">
            <div className="rounded-2xl border border-border bg-card p-6">
              <h2 className="text-xs font-semibold uppercase tracking-[0.16em] text-primary">
                Provenance
              </h2>
              <dl className="mt-4 flex flex-col gap-3">
                <MetaRow label="Reading time" value={`${a.readingMinutes} min`} />
                <MetaRow label="Last verified" value={a.last_verified} />
                <MetaRow label="License" value={a.license ?? "CC-BY-4.0"} />
                <MetaRow
                  label="Media"
                  value={
                    approvedMedia
                      ? approvedMedia.conceptReconstruction
                        ? "Concept reconstruction"
                        : "Approved primary image"
                      : undefined
                  }
                />
                <MetaRow
                  label="Consensus"
                  value={
                    a.consensus_state
                      ? a.consensus_state.replace(/-/g, " ")
                      : undefined
                  }
                />
                <MetaRow label="Difficulty" value={a.difficulty} />
              </dl>

              {a.review && (
                <div className="mt-5 border-t border-border pt-5">
                  <h3 className="text-xs font-semibold uppercase tracking-[0.16em] text-primary">
                    Review gates
                  </h3>
                  <div className="mt-3 flex flex-col gap-2">
                    <ReviewDot state={a.review.science} label="Science" />
                    <ReviewDot state={a.review.ethics} label="Ethics" />
                    <ReviewDot state={a.review.editor} label="Editorial" />
                  </div>
                </div>
              )}

              {a.welfare?.five_domains && (
                <div className="mt-5 border-t border-border pt-5">
                  <h3 className="text-xs font-semibold uppercase tracking-[0.16em] text-primary">
                    Five Domains
                  </h3>
                  <dl className="mt-3 flex flex-col gap-2">
                    {Object.entries(a.welfare.five_domains).map(([k, v]) => (
                      <MetaRow
                        key={k}
                        label={k
                          .replace(/_/g, " ")
                          .replace(/^./, (c) => c.toUpperCase())}
                        value={String(v).replace(/-/g, " ")}
                      />
                    ))}
                  </dl>
                </div>
              )}

              <BridgeRail artifact={a} />

              {a.impact?.claim && (
                <div className="mt-5 rounded-xl bg-primary/8 p-4">
                  <h3 className="text-xs font-semibold uppercase tracking-[0.16em] text-primary">
                    {impactIsPublished
                      ? "Published impact claim"
                      : "Proposed impact claim"}
                  </h3>
                  <p className="mt-2 text-sm leading-relaxed text-foreground">
                    {a.impact.claim}
                  </p>
                  {a.impact.eligible_for_hypercert && (
                    <p className="mt-2 text-xs font-medium text-primary">
                      {impactIsPublished
                        ? "Hypercert eligibility metadata · not proof of issuance"
                        : "Eligibility metadata only · not issued or certified"}
                    </p>
                  )}
                </div>
              )}

              <a
                href={editUrl}
                target="_blank"
                rel="noopener noreferrer"
                className="mt-6 inline-flex w-full items-center justify-center gap-2 rounded-full border border-border px-4 py-2.5 text-sm font-semibold text-foreground transition-colors hover:border-primary/40 hover:text-primary"
              >
                View source on GitHub
              </a>
            </div>
          </aside>
        </div>

        {a.sources.length > 0 && (
          <section
            aria-labelledby="sources-heading"
            className="mt-14 border-t border-border pt-10"
          >
            <h2
              id="sources-heading"
              className="font-serif text-2xl font-semibold text-foreground"
            >
              Sources ({a.sources.length})
            </h2>
            <p className="mt-2 max-w-2xl text-sm leading-relaxed text-muted-foreground">
              Every claim in this artifact traces to one of the citations below.
              Anything that could not be sourced was left out.
            </p>
            <ol className="mt-6 grid gap-3 sm:grid-cols-2">
              {a.sources.map((s, i) => (
                <li key={s.url}>
                  <a
                    href={s.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="group flex h-full flex-col gap-2 rounded-xl border border-border bg-card p-4 transition-colors hover:border-primary/40"
                  >
                    <div className="flex items-start justify-between gap-3">
                      <span className="font-mono text-xs text-muted-foreground">
                        [{i + 1}]
                      </span>
                      <SourceTierChip tier={s.tier} />
                    </div>
                    <span className="text-sm font-medium leading-snug text-foreground group-hover:text-primary">
                      {s.title}
                    </span>
                    {s.accessed && (
                      <span className="mt-auto text-xs text-muted-foreground">
                        Accessed {s.accessed}
                      </span>
                    )}
                  </a>
                </li>
              ))}
            </ol>
          </section>
        )}

        {related.length > 0 && (
          <section
            aria-labelledby="related-heading"
            className="mt-14 border-t border-border pt-10"
          >
            <h2
              id="related-heading"
              className="font-serif text-2xl font-semibold text-foreground"
            >
              Related in the commons
            </h2>
            <div className="mt-6 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
              {related.map((r) => (
                <ArtifactCard key={r.id} artifact={r} />
              ))}
            </div>
          </section>
        )}
      </Container>
    </article>
  )
}
