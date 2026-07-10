import Image from "next/image"
import { ArrowRight, ButtonLink, Container } from "@/components/primitives"
import type { CommonsStats } from "@/lib/types"
import { GITHUB_REPO_URL } from "@/lib/utils"

interface CommonsProof {
  title: string
  href: string
  githubPath: string
  status: string
  sourceCount: number
  imageUrl: string
  sourceUrl?: string
  creator?: string
  license?: string
  licenseUrl?: string
  altText: string
  mediaChecks: number
  mediaChecksTotal: number
}

export function HomeHero({
  stats,
  proof,
}: {
  stats: CommonsStats
  proof?: CommonsProof
}) {
  return (
    <section className="relative isolate overflow-hidden bg-abyss-deep text-abyss-foreground">
      <div className="absolute inset-0 abyss-grid opacity-25" aria-hidden />
      <div className="absolute inset-x-0 top-0 h-px bg-gradient-to-r from-transparent via-glow/50 to-transparent" />

      <Container className="relative py-16 sm:py-20 lg:py-24">
        <div className="grid items-center gap-12 lg:grid-cols-[minmax(0,0.88fr)_minmax(30rem,1.12fr)] lg:gap-16">
          <div className="max-w-3xl">
            <span className="inline-flex items-center gap-2 rounded-full border border-abyss-border bg-white/5 px-3 py-1.5 text-xs font-medium text-glow">
              <span className="size-1.5 rounded-full bg-glow" aria-hidden />
              Open · Source-linked · Review-gated
            </span>

            <h1 className="mt-6 text-balance font-serif text-4xl font-semibold leading-[1.02] tracking-tight sm:text-5xl lg:text-6xl xl:text-7xl">
              The open intelligence commons for ocean life.
            </h1>

            <p className="mt-6 max-w-2xl text-pretty text-lg leading-relaxed text-abyss-muted">
              Species records, region briefings, field missions, and datasets
              publish with citations, rights, welfare safeguards, and visible
              review state. The knowledge is versioned on GitHub and licensed
              for reuse.
            </p>

            <div className="mt-9 flex flex-wrap items-center gap-3">
              <ButtonLink href="/species" variant="onDark">
                Explore species records
                <ArrowRight />
              </ButtonLink>
              <ButtonLink href="/contribute" variant="onDarkGhost">
                Contribute with sources
              </ButtonLink>
            </div>

            <dl className="mt-12 grid max-w-2xl grid-cols-2 gap-x-8 gap-y-5 sm:grid-cols-4">
              {[
                { value: stats.total, label: "Artifacts" },
                { value: stats.species, label: "Species records" },
                { value: stats.sources, label: "Cited sources" },
                { value: stats.regions, label: "Region briefings" },
              ].map((stat) => (
                <div key={stat.label}>
                  <dd className="font-serif text-3xl font-semibold tabular-nums text-glow">
                    {stat.value}
                  </dd>
                  <dt className="mt-1 text-xs text-abyss-muted">{stat.label}</dt>
                </div>
              ))}
            </dl>
          </div>

          {proof && (
            <article className="overflow-hidden rounded-2xl border border-abyss-border bg-abyss shadow-2xl shadow-black/25">
              <figure className="relative aspect-[4/3] overflow-hidden bg-abyss-deep">
                <Image
                  src={proof.imageUrl}
                  alt={proof.altText}
                  fill
                  priority
                  sizes="(max-width: 1024px) 100vw, 48vw"
                  className="object-cover"
                />
                <div className="absolute inset-x-0 bottom-0 bg-gradient-to-t from-abyss-deep via-abyss-deep/75 to-transparent px-5 pb-5 pt-20">
                  <div className="flex flex-wrap gap-2 text-[11px] font-semibold uppercase tracking-[0.12em]">
                    <span className="rounded-full bg-glow px-2.5 py-1 text-abyss-deep">
                      Approved media
                    </span>
                    <span className="rounded-full border border-white/25 bg-black/25 px-2.5 py-1 text-white backdrop-blur-sm">
                      Science review pending
                    </span>
                  </div>
                  <h2 className="mt-3 font-serif text-2xl font-semibold text-white sm:text-3xl">
                    {proof.title}
                  </h2>
                </div>
              </figure>

              <div className="p-5 sm:p-6">
                <p className="font-mono text-[10px] font-semibold uppercase tracking-[0.15em] text-glow">
                  One public record, end to end
                </p>
                <ol className="mt-4 grid gap-px overflow-hidden rounded-xl border border-abyss-border bg-abyss-border sm:grid-cols-2">
                  {[
                    ["01 · Record", proof.githubPath],
                    ["02 · Evidence", `${proof.sourceCount} cited authorities`],
                    [
                      "03 · Rights",
                      `${proof.license ?? "Licensed"} · ${proof.mediaChecks}/${proof.mediaChecksTotal} media checks`,
                    ],
                    ["04 · Reuse", "CC BY 4.0 artifact + attribution"],
                  ].map(([label, value]) => (
                    <li key={label} className="source-trace bg-abyss-deep p-3.5">
                      <span className="block font-mono text-[9px] uppercase tracking-[0.12em] text-glow">
                        {label}
                      </span>
                      <strong className="mt-1.5 block break-words text-xs font-medium leading-relaxed text-abyss-foreground">
                        {value}
                      </strong>
                    </li>
                  ))}
                </ol>

                <div className="mt-5 flex flex-wrap items-center justify-between gap-3 text-xs">
                  <div className="text-abyss-muted">
                    Image: {proof.creator ?? "Source contributor"} ·{" "}
                    {proof.licenseUrl ? (
                      <a
                        href={proof.licenseUrl}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="underline underline-offset-2 hover:text-white"
                      >
                        {proof.license ?? "license"}
                      </a>
                    ) : (
                      proof.license
                    )}
                  </div>
                  <div className="flex gap-3 font-semibold text-glow">
                    <a href={proof.href} className="hover:underline">
                      Open record
                    </a>
                    {proof.sourceUrl && (
                      <a
                        href={proof.sourceUrl}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="hover:underline"
                      >
                        Source image
                      </a>
                    )}
                    <a
                      href={`${GITHUB_REPO_URL}/blob/main/${proof.githubPath}`}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="hover:underline"
                    >
                      History
                    </a>
                  </div>
                </div>
              </div>
            </article>
          )}
        </div>
      </Container>
    </section>
  )
}
