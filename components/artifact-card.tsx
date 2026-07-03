import { TransitionLink } from "@/components/transition-link"
import { ArtifactCardMedia } from "@/components/artifact-media"
import { IucnBadge, TypeChip } from "@/components/badges"
import { GUILD_META, cn } from "@/lib/utils"
import type { Artifact } from "@/lib/types"

export function ArtifactCard({
  artifact,
  className,
}: {
  artifact: Artifact
  className?: string
}) {
  const meta: string[] = []
  if (artifact.region?.length) meta.push(artifact.region[0])
  if (artifact.difficulty) meta.push(artifact.difficulty)
  if (artifact.species_group?.length)
    meta.push(
      GUILD_META[artifact.species_group[0]]?.label ?? artifact.species_group[0],
    )

  return (
    <TransitionLink
      href={artifact.href}
      className={cn(
        "group relative flex flex-col rounded-xl border border-border bg-card p-5 transition-all duration-300 hover:-translate-y-1 hover:border-primary/40 hover:shadow-[var(--shadow-elevated)]",
        className,
      )}
    >
      <div className="flex items-center justify-between gap-2">
        <TypeChip type={artifact.type} />
        {artifact.iucn?.category && (
          <IucnBadge category={artifact.iucn.category} size="sm" />
        )}
      </div>

      <ArtifactCardMedia artifact={artifact} />

      <h3 className="mt-4 text-pretty font-serif text-lg font-semibold leading-snug text-card-foreground group-hover:text-primary">
        {artifact.title}
      </h3>

      {artifact.excerpt && (
        <p className="mt-2 line-clamp-2 text-sm leading-relaxed text-muted-foreground">
          {artifact.excerpt}
        </p>
      )}

      <div className="mt-auto flex flex-wrap items-center gap-x-3 gap-y-1 pt-4 text-xs text-muted-foreground">
        {meta.slice(0, 2).map((m) => (
          <span key={m} className="capitalize">
            {m}
          </span>
        ))}
        <span className="ml-auto inline-flex items-center gap-1.5">
          <span className="size-1 rounded-full bg-kelp" aria-hidden />
          {artifact.sources.length} source{artifact.sources.length === 1 ? "" : "s"}
        </span>
      </div>
    </TransitionLink>
  )
}
