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
import {
  ArtifactCinematicHero,
  ArtifactHeroMedia,
} from "@/components/artifact-media"
import {
  SpeciesCompareMode,
  SpeciesStatsChips,
} from "@/components/species-stats-compare"
import { SpeciesLifeGallery } from "@/components/species-life-gallery"
import { getApprovedSpeciesMedia } from "@/lib/media"
import { GITHUB_REPO_URL, cn, formatRegion } from "@/lib/utils"
import Link from "next/link"

function Breadcrumb({ trail }: { trail: { label: string; href?: string }[] }) {
  return (
    <nav aria-label="Breadcrumb" className="text-sm text-muted-foreground">
      <ol className="flex flex-wrap items-center gap-1.5">
        {trail.map((item, i) => (
          <li key={item.label} className="flex items-center gap-1.5">
            {i > 0 && <span aria-hidden className="text-border">/</span>}
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

/** Parse "Common Name (Genus species)" or bare binomial into display parts. */
function splitSpeciesTitle(title: string): {
  display: string
  scientific?: string
  isBinomial: boolean
} {
  const paren = title.match(/^(.*?)\s*\(([^)]+)\)\s*$/)
  if (paren) {
    return {
      display: paren[1].trim(),
      scientific: paren[2].trim(),
      isBinomial: true,
    }
  }
  // Bare scientific binomial: Genus species [optional subsp]
  const binomial = title.match(/^([A-Z][a-z]+(?:\s+[a-z]+(?:\s+[a-z]+)?)?)$/)
  if (binomial) {
    return {
      display: binomial[1],
      scientific: binomial[1],
      isBinomial: true,
    }
  }
  return { display: title, isBinomial: false }
}

function SpeciesTitle({
  title,
  onDark = false,
}: {
  title: string
  onDark?: boolean
}) {
  const parts = splitSpeciesTitle(title)
  const text = onDark ? "text-white" : "text-foreground"
  const muted = onDark ? "text-white/70" : "text-muted-foreground"

  if (parts.scientific && parts.display !== parts.scientific) {
    return (
      <div className="mt-4 max-w-3xl">
        <h1
          className={cn(
            "text-balance font-serif text-3xl font-semibold leading-[1.08] tracking-[-0.02em] sm:text-4xl lg:text-[2.75rem]",
            text,
          )}
        >
          {parts.display}
        </h1>
        <p
          className={cn(
            "mt-2 font-sans text-lg font-medium italic leading-snug tracking-tight sm:text-xl",
            muted,
          )}
        >
          {parts.scientific}
        </p>
      </div>
    )
  }

  if (parts.isBinomial) {
    // Scientific-only titles: italic sans, not heavy serif (reads cleaner).
    return (
      <h1
        className={cn(
          "mt-4 max-w-3xl text-balance font-sans text-3xl font-semibold italic leading-[1.12] tracking-[-0.025em] sm:text-4xl lg:text-[2.65rem]",
          text,
        )}
      >
        {parts.display}
      </h1>
    )
  }

  return (
    <h1
      className={cn(
        "mt-4 max-w-3xl text-balance font-serif text-3xl font-semibold leading-[1.08] tracking-[-0.02em] sm:text-4xl lg:text-[2.75rem]",
        text,
      )}
    >
      {parts.display}
    </h1>
  )
}

function guildFromPath(path: string): string {
  const parts = path.split(/[/\\]/)
  const idx = parts.indexOf("species")
  return idx >= 0 && parts[idx + 1] ? parts[idx + 1] : "other"
}

function QuickFacts({
  artifact,
  guild,
  tone = "light",
}: {
  artifact: Artifact
  guild: string
  tone?: "light" | "dark"
}) {
  if (artifact.stats && Object.keys(artifact.stats).length > 0) {
    return <SpeciesStatsChips stats={artifact.stats} tone={tone} />
  }

  const facts: { label: string; value: string }[] = []
  if (artifact.iucn?.category) {
    facts.push({
      label: "Status",
      value:
        artifact.iucn.category === "EX"
          ? "Extinct (fossil)"
          : artifact.iucn.category,
    })
  }
  if (guild === "marine-reptiles") {
    facts.push({ label: "Guild", value: "Marine reptile · Deep Time" })
    facts.push({ label: "Not a dinosaur", value: "Mesozoic ocean vertebrate" })
  } else if (artifact.species_group?.[0]) {
    facts.push({
      label: "Guild",
      value: artifact.species_group[0].replace(/-/g, " "),
    })
  }
  if (artifact.difficulty) {
    facts.push({ label: "Reading level", value: artifact.difficulty })
  }
  if (artifact.sources.length) {
    facts.push({ label: "Sources", value: String(artifact.sources.length) })
  }
  if (facts.length === 0) return null

  return (
    <dl className="grid grid-cols-2 gap-2.5 sm:grid-cols-4">
      {facts.map((f) => (
        <div
          key={f.label}
          className={cn(
            "rounded-xl border px-3.5 py-3",
            tone === "dark"
              ? "border-abyss-border bg-white/5"
              : "border-border bg-card/80",
          )}
        >
          <dt
            className={cn(
              "text-[11px] font-semibold uppercase tracking-[0.12em]",
              tone === "dark" ? "text-abyss-muted" : "text-muted-foreground",
            )}
          >
            {f.label}
          </dt>
          <dd
            className={cn(
              "mt-1 text-sm font-semibold capitalize leading-snug",
              tone === "dark" ? "text-abyss-foreground" : "text-foreground",
            )}
          >
            {f.value}
          </dd>
        </div>
      ))}
    </dl>
  )
}

function DeepTimeDepthPanel() {
  return (
    <section
      aria-labelledby="depth-heading"
      className="mt-10 rounded-2xl border border-border bg-secondary/70 p-6 sm:p-8"
    >
      <p className="text-xs font-semibold uppercase tracking-[0.14em] text-primary">
        How to use this page
      </p>
      <h2
        id="depth-heading"
        className="mt-2 font-serif text-2xl font-semibold tracking-tight text-foreground"
      >
        Read deep time with living-ocean tools
      </h2>
      <div className="mt-5 grid gap-4 sm:grid-cols-3">
        {[
          {
            t: "Correct the myth",
            d: "“Ocean dinosaur” is pop culture. These animals are marine reptiles (and related deep-time ocean vertebrates), not Dinosauria.",
          },
          {
            t: "Compare body plans",
            d: "Mosasaurs ≈ marine lizards with tails; plesiosaurs ≈ four flippers; ichthyosaurs ≈ dolphin-like. Use the living bridges for ecological analogy only.",
          },
          {
            t: "Trust the labels",
            d: "Hero media is concept reconstruction. Claims stay sourced; review gates stay visible until experts approve.",
          },
        ].map((item) => (
          <div
            key={item.t}
            className="rounded-xl border border-border bg-card p-4"
          >
            <h3 className="text-sm font-semibold text-foreground">{item.t}</h3>
            <p className="mt-2 text-sm leading-relaxed text-muted-foreground">
              {item.d}
            </p>
          </div>
        ))}
      </div>
      <div className="mt-5 flex flex-wrap gap-3 text-sm font-semibold">
        <Link href="/species/deep-time" className="text-primary hover:underline">
          Deep Time hub
        </Link>
        <Link
          href="/species/sharks-rays/great-white-shark"
          className="text-primary hover:underline"
        >
          Compare: great white
        </Link>
        <Link
          href="/species/cetaceans/blue-whale"
          className="text-primary hover:underline"
        >
          Compare: blue whale
        </Link>
        <Link
          href="/species/turtles/leatherback-turtle"
          className="text-primary hover:underline"
        >
          Compare: leatherback
        </Link>
      </div>
    </section>
  )
}

function BridgeRail({ guild }: { guild: string }) {
  if (guild === "marine-reptiles") {
    return (
      <div className="mt-5 rounded-xl border border-primary/20 bg-primary/8 p-4">
        <h3 className="text-xs font-semibold uppercase tracking-[0.16em] text-primary">
          Deep Time bridge
        </h3>
        <p className="mt-2 text-sm leading-relaxed text-foreground">
          Mesozoic marine reptile — not a dinosaur. Compare body plans with
          living ocean apex predators and sea turtles.
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
          Curious about “ocean dinosaurs”? Start with Mesozoic marine reptiles
          in the Deep Time section.
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
  const missionEthicsReviewOpen =
    a.type === "field-mission" && a.review?.ethics !== "approved"
  const guild = guildFromPath(a.path)
  const isSpecies = a.type === "species-page"
  const cinematic = Boolean(isSpecies && approvedMedia)

  return (
    <article>
      {/* Cinematic species hero — large media stage first */}
      {cinematic ? (
        <header className="border-b border-border bg-abyss text-abyss-foreground">
          <Container className="py-6 sm:py-8 lg:py-10">
            <div className="text-abyss-muted [&_a]:text-abyss-muted [&_a:hover]:text-glow">
              <Breadcrumb trail={trail} />
            </div>

            <div className="mt-5 flex flex-wrap items-center gap-2">
              <TypeChip type={a.type} />
              <StatusPill status={a.status} />
              {guild === "marine-reptiles" && (
                <Chip tone="primary">Deep Time</Chip>
              )}
            </div>

            <div className="mt-5 sm:mt-6">
              <ArtifactCinematicHero
                artifact={a}
                titleNode={
                  <div className="mt-4">
                    <SpeciesTitle title={a.title} onDark />
                  </div>
                }
                metaNode={
                  <div className="mt-4 flex flex-wrap items-center gap-2">
                    <IucnBadge category={a.iucn?.category} />
                    <WelfareBadge state={a.welfare?.state} />
                    {a.region?.map((r) => (
                      <Chip key={r} tone="primary">
                        {formatRegion(r)}
                      </Chip>
                    ))}
                  </div>
                }
              />
            </div>

            <div className="mt-6">
              <QuickFacts artifact={a} guild={guild} tone="dark" />
            </div>
          </Container>
        </header>
      ) : (
        <header className="border-b border-border bg-secondary">
          <Container className="py-10 sm:py-14">
            <Breadcrumb trail={trail} />
            <div
              className={cn(
                "mt-6 grid gap-8",
                approvedMedia &&
                  "lg:grid-cols-[minmax(0,1fr)_minmax(320px,520px)] lg:items-end",
              )}
            >
              <div>
                <div className="flex flex-wrap items-center gap-2">
                  <TypeChip type={a.type} />
                  <StatusPill status={a.status} />
                  {guild === "marine-reptiles" && (
                    <Chip tone="primary">Deep Time</Chip>
                  )}
                  {a.sensitivity?.tier === "sensitive" && (
                    <Chip tone="accent">Location generalized</Chip>
                  )}
                </div>
                <SpeciesTitle title={a.title} />
                <div className="mt-5 flex flex-wrap items-center gap-3">
                  <IucnBadge category={a.iucn?.category} />
                  <WelfareBadge state={a.welfare?.state} />
                  {a.region?.map((r) => (
                    <Chip key={r} tone="primary">
                      {formatRegion(r)}
                    </Chip>
                  ))}
                </div>
                {isSpecies && (
                  <div className="mt-6">
                    <QuickFacts artifact={a} guild={guild} />
                  </div>
                )}
              </div>
              {approvedMedia && <ArtifactHeroMedia artifact={a} />}
            </div>
          </Container>
        </header>
      )}

      <Container className="py-10 sm:py-14">
        {guild === "marine-reptiles" && <DeepTimeDepthPanel />}

        {isSpecies && <SpeciesCompareMode artifact={a} />}

        {isSpecies && <SpeciesLifeGallery artifact={a} />}

        <div
          className={cn(
            "grid gap-12",
            guild === "marine-reptiles" ||
              a.compare?.length ||
              (a.media?.gallery?.length ?? 0) > 0 ||
              (a.media?.video_links?.length ?? 0) > 0
              ? "mt-10"
              : "",
            "lg:grid-cols-[minmax(0,1fr)_minmax(280px,340px)]",
          )}
        >
          <div>
            {missionEthicsReviewOpen ? (
              <section
                aria-labelledby="mission-review-hold"
                className="rounded-2xl border border-coral/35 bg-coral/8 p-6 sm:p-8"
              >
                <p className="text-xs font-semibold uppercase tracking-[0.16em] text-coral">
                  Ethics review open
                </p>
                <h2
                  id="mission-review-hold"
                  className="mt-3 font-serif text-2xl font-semibold text-foreground"
                >
                  This is not operational wildlife guidance.
                </h2>
                <p className="mt-3 max-w-2xl text-sm leading-relaxed text-muted-foreground">
                  The mission body stays off the public site until its ethics
                  review is approved. Reviewers can inspect the sourced draft
                  in GitHub; visitors should follow current local regulations
                  and guidance from the responsible authority.
                </p>
                <a
                  href={editUrl}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="mt-5 inline-flex items-center text-sm font-semibold text-primary hover:underline"
                >
                  Inspect the review draft on GitHub
                </a>
              </section>
            ) : (
              <div
                className="prose-ocean"
                dangerouslySetInnerHTML={{ __html: a.bodyHtml }}
              />
            )}
          </div>

          <aside
            className="lg:sticky lg:top-24 lg:self-start lg:max-h-[calc(100dvh-7rem)] lg:overflow-y-auto"
            aria-label="Provenance"
          >
            <div className="rounded-2xl border border-border bg-card p-6 shadow-[var(--shadow-elevated)]">
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

              <BridgeRail guild={guild} />

              {a.impact?.claim && (
                <div className="mt-5 rounded-xl bg-primary/8 p-4">
                  <h3 className="text-xs font-semibold uppercase tracking-[0.16em] text-primary">
                    {impactIsPublished
                      ? "Published impact claim"
                      : "Impact claim in review"}
                  </h3>
                  <p className="mt-2 text-sm leading-relaxed text-foreground">
                    {impactIsPublished
                      ? a.impact.claim
                      : "A proposed claim exists in repository metadata, but it is not presented as an outcome until review is complete."}
                  </p>
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
              className="font-serif text-2xl font-semibold tracking-tight text-foreground"
            >
              Sources ({a.sources.length})
            </h2>
            <p className="mt-2 max-w-2xl text-sm leading-relaxed text-muted-foreground">
              Every claim traces to one of the citations below. Anything that
              could not be sourced was left out.
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
              className="font-serif text-2xl font-semibold tracking-tight text-foreground"
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
