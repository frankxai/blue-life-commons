import { IUCN_META, TYPE_LABELS, WELFARE_META, cn } from "@/lib/utils"
import type { ReviewState } from "@/lib/types"

export function Chip({
  children,
  className,
  tone = "neutral",
}: {
  children: React.ReactNode
  className?: string
  tone?: "neutral" | "primary" | "accent" | "muted" | "onDark"
}) {
  const tones: Record<string, string> = {
    neutral: "bg-muted text-muted-foreground",
    primary: "bg-primary/10 text-primary",
    accent: "bg-accent/15 text-accent-foreground",
    muted: "bg-muted text-muted-foreground",
    onDark: "bg-white/10 text-abyss-foreground",
  }
  return (
    <span
      className={cn(
        "inline-flex items-center gap-1.5 rounded-full px-2.5 py-1 text-xs font-medium",
        tones[tone],
        className,
      )}
    >
      {children}
    </span>
  )
}

export function TypeChip({ type, className }: { type: string; className?: string }) {
  return (
    <span
      className={cn(
        "inline-flex items-center gap-1.5 rounded-full border border-border bg-card px-2.5 py-1 text-xs font-medium text-muted-foreground",
        className,
      )}
    >
      <span
        className="size-1.5 rounded-full"
        style={{ background: `var(--color-primary)` }}
        aria-hidden
      />
      {TYPE_LABELS[type] ?? type}
    </span>
  )
}

export function IucnBadge({
  category,
  size = "md",
}: {
  category?: string
  size?: "sm" | "md"
}) {
  if (!category) return null
  const meta = IUCN_META[category] ?? IUCN_META.NE
  return (
    <span
      className={cn(
        "inline-flex items-center gap-2 rounded-full font-semibold",
        size === "sm" ? "px-2.5 py-1 text-xs" : "px-3 py-1.5 text-sm",
      )}
      style={{ background: meta.color, color: meta.textOnColor }}
      title={`IUCN Red List: ${meta.label}`}
    >
      <span className="font-mono tracking-tight">{category}</span>
      <span className="font-medium opacity-90">{meta.label}</span>
    </span>
  )
}

export function WelfareBadge({ state }: { state?: string }) {
  if (!state) return null
  const meta = WELFARE_META[state] ?? { label: state, color: "var(--color-muted-foreground)" }
  return (
    <span className="inline-flex items-center gap-2 rounded-full border border-border bg-card px-3 py-1.5 text-sm font-medium">
      <span
        className="size-2.5 rounded-full"
        style={{ background: meta.color }}
        aria-hidden
      />
      {meta.label}
    </span>
  )
}

const REVIEW_TONE: Record<ReviewState, { label: string; dot: string }> = {
  approved: { label: "Approved", dot: "var(--color-kelp)" },
  pending: { label: "Pending", dot: "var(--color-amber)" },
  required: { label: "Needed", dot: "var(--color-coral)" },
  "not-applicable": { label: "N/A", dot: "var(--color-muted-foreground)" },
}

export function ReviewDot({ state, label }: { state?: ReviewState; label: string }) {
  const meta = state ? REVIEW_TONE[state] : REVIEW_TONE["not-applicable"]
  return (
    <span className="inline-flex items-center gap-2 text-sm">
      <span className="size-2 rounded-full" style={{ background: meta.dot }} aria-hidden />
      <span className="text-muted-foreground">{label}</span>
      <span className="font-medium text-foreground">{meta.label}</span>
    </span>
  )
}

const TIER_META: Record<number, { label: string; tone: string }> = {
  1: { label: "Tier 1 · Peer-reviewed", tone: "bg-primary/12 text-primary" },
  2: { label: "Tier 2 · Institutional", tone: "bg-kelp/15 text-foreground" },
  3: { label: "Tier 3 · Reputable", tone: "bg-muted text-muted-foreground" },
}

export function SourceTierChip({ tier }: { tier?: number }) {
  if (!tier) return null
  const meta = TIER_META[tier]
  if (!meta) return null
  return (
    <span className={cn("rounded px-1.5 py-0.5 text-[11px] font-medium", meta.tone)}>
      {meta.label}
    </span>
  )
}

export function StatusPill({ status }: { status?: string }) {
  if (!status) return null
  const map: Record<string, { label: string; dot: string }> = {
    draft: { label: "Draft", dot: "var(--color-muted-foreground)" },
    "needs-expert-review": { label: "In expert review", dot: "var(--color-amber)" },
    approved: { label: "Approved", dot: "var(--color-kelp)" },
    published: { label: "Published", dot: "var(--color-kelp)" },
  }
  const meta = map[status] ?? { label: status, dot: "var(--color-muted-foreground)" }
  return (
    <span className="inline-flex items-center gap-2 rounded-full border border-border bg-card px-2.5 py-1 text-xs font-medium text-muted-foreground">
      <span className="size-1.5 rounded-full" style={{ background: meta.dot }} aria-hidden />
      {meta.label}
    </span>
  )
}
