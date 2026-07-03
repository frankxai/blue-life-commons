"use client"

import { useMemo, useState, useDeferredValue } from "react"
import Link from "next/link"
import { useSearchParams } from "next/navigation"
import { TYPE_LABELS, cn, titleCase } from "@/lib/utils"
import { Chip, IucnBadge, StatusPill, TypeChip } from "@/components/badges"
import { MediaCardPreview } from "@/components/artifact-media"
import type { ApprovedSpeciesMedia } from "@/lib/media"

export interface CatalogItem {
  id: string
  type: string
  title: string
  href: string
  excerpt: string
  region: string[]
  audience: string[]
  iucn?: string
  status?: string
  sourceCount: number
  media?: ApprovedSpeciesMedia
}

const TYPE_ORDER = [
  "species-page",
  "region-briefing",
  "field-mission",
  "dataset-card",
  "research-summary",
  "partner-profile",
  "welfare-assessment",
]

export function CatalogExplorer({ items }: { items: CatalogItem[] }) {
  const searchParams = useSearchParams()
  const [query, setQuery] = useState("")
  const [type, setType] = useState<string>(searchParams.get("type") ?? "all")
  const [region, setRegion] = useState<string>("all")
  const deferredQuery = useDeferredValue(query)

  const regions = useMemo(() => {
    const set = new Set<string>()
    for (const item of items) for (const r of item.region) set.add(r)
    return [...set].sort()
  }, [items])

  const filtered = useMemo(() => {
    const q = deferredQuery.trim().toLowerCase()
    return items.filter((item) => {
      if (type !== "all" && item.type !== type) return false
      if (region !== "all" && !item.region.includes(region)) return false
      if (q && !`${item.title} ${item.excerpt}`.toLowerCase().includes(q))
        return false
      return true
    })
  }, [items, type, region, deferredQuery])

  const counts = useMemo(() => {
    const map = new Map<string, number>()
    for (const item of items) map.set(item.type, (map.get(item.type) ?? 0) + 1)
    return map
  }, [items])

  return (
    <div>
      {/* Controls */}
      <div className="flex flex-col gap-4">
        <div className="relative max-w-xl">
          <svg
            width="18"
            height="18"
            viewBox="0 0 24 24"
            fill="none"
            aria-hidden
            className="pointer-events-none absolute left-4 top-1/2 -translate-y-1/2 text-muted-foreground"
          >
            <circle cx="11" cy="11" r="7" stroke="currentColor" strokeWidth="2" />
            <path d="m20 20-3.5-3.5" stroke="currentColor" strokeWidth="2" strokeLinecap="round" />
          </svg>
          <input
            type="search"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Search species, regions, missions, datasets…"
            aria-label="Search the catalog"
            className="w-full rounded-full border border-border bg-card py-3 pl-11 pr-4 text-sm text-foreground outline-none transition-colors placeholder:text-muted-foreground focus:border-primary/50 focus:ring-2 focus:ring-primary/20"
          />
        </div>

        <div className="flex flex-wrap gap-2" role="group" aria-label="Filter by type">
          <button
            type="button"
            onClick={() => setType("all")}
            className={cn(
              "rounded-full px-4 py-2 text-sm font-medium transition-colors",
              type === "all"
                ? "bg-primary text-primary-foreground"
                : "border border-border bg-card text-muted-foreground hover:text-foreground",
            )}
            aria-pressed={type === "all"}
          >
            All · {items.length}
          </button>
          {TYPE_ORDER.filter((t) => counts.get(t)).map((t) => (
            <button
              key={t}
              type="button"
              onClick={() => setType(t)}
              className={cn(
                "rounded-full px-4 py-2 text-sm font-medium transition-colors",
                type === t
                  ? "bg-primary text-primary-foreground"
                  : "border border-border bg-card text-muted-foreground hover:text-foreground",
              )}
              aria-pressed={type === t}
            >
              {TYPE_LABELS[t]} · {counts.get(t)}
            </button>
          ))}
        </div>

        <div className="flex items-center gap-3">
          <label htmlFor="region-filter" className="text-sm text-muted-foreground">
            Region
          </label>
          <select
            id="region-filter"
            value={region}
            onChange={(e) => setRegion(e.target.value)}
            className="rounded-full border border-border bg-card px-4 py-2 text-sm text-foreground outline-none focus:border-primary/50"
          >
            <option value="all">All regions</option>
            {regions.map((r) => (
              <option key={r} value={r}>
                {titleCase(r)}
              </option>
            ))}
          </select>
          <span className="text-sm text-muted-foreground" aria-live="polite">
            {filtered.length} {filtered.length === 1 ? "result" : "results"}
          </span>
        </div>
      </div>

      {/* Results */}
      {filtered.length === 0 ? (
        <div className="mt-10 rounded-2xl border border-dashed border-border p-12 text-center">
          <p className="font-medium text-foreground">Nothing matches that filter.</p>
          <p className="mt-1 text-sm text-muted-foreground">
            Try a broader search — or contribute the artifact you were looking for.
          </p>
        </div>
      ) : (
        <ul className="mt-8 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {filtered.map((item) => (
            <li key={item.id}>
              <Link
                href={item.href}
                className="group flex h-full flex-col gap-3 rounded-2xl border border-border bg-card p-5 transition-all hover:-translate-y-0.5 hover:border-primary/40 hover:shadow-[var(--shadow-elevated)]"
              >
                <div className="flex flex-wrap items-center gap-2">
                  <TypeChip type={item.type} />
                  <IucnBadge category={item.iucn} size="sm" />
                </div>
                <MediaCardPreview media={item.media} className="mt-0" />
                <h3 className="font-serif text-lg font-semibold leading-snug text-foreground group-hover:text-primary">
                  {item.title}
                </h3>
                <p className="line-clamp-2 text-sm leading-relaxed text-muted-foreground">
                  {item.excerpt}
                </p>
                <div className="mt-auto flex flex-wrap items-center gap-2 pt-1">
                  <StatusPill status={item.status} />
                  {item.sourceCount > 0 && (
                    <Chip tone="muted">{item.sourceCount} sources</Chip>
                  )}
                </div>
              </Link>
            </li>
          ))}
        </ul>
      )}
    </div>
  )
}
