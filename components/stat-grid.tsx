import { cn } from "@/lib/utils"

export interface Stat {
  value: string | number
  label: string
  sub?: string
}

export function StatGrid({
  stats,
  tone = "light",
  className,
}: {
  stats: Stat[]
  tone?: "light" | "dark"
  className?: string
}) {
  return (
    <dl
      className={cn(
        "grid grid-cols-2 gap-px overflow-hidden rounded-2xl border sm:grid-cols-3 lg:grid-cols-6",
        tone === "dark"
          ? "border-abyss-border bg-abyss-border"
          : "border-border bg-border",
        className,
      )}
    >
      {stats.map((s) => (
        <div
          key={s.label}
          className={cn(
            "flex flex-col gap-1 p-5",
            tone === "dark" ? "bg-abyss" : "bg-card",
          )}
        >
          <dd
            className={cn(
              "font-serif text-3xl font-semibold tabular-nums tracking-tight",
              tone === "dark" ? "text-glow" : "text-primary",
            )}
          >
            {s.value}
          </dd>
          <dt
            className={cn(
              "text-sm font-medium",
              tone === "dark" ? "text-abyss-foreground" : "text-foreground",
            )}
          >
            {s.label}
          </dt>
          {s.sub && (
            <span
              className={cn(
                "text-xs",
                tone === "dark" ? "text-abyss-muted" : "text-muted-foreground",
              )}
            >
              {s.sub}
            </span>
          )}
        </div>
      ))}
    </dl>
  )
}
