import Link from "next/link"
import { cn } from "@/lib/utils"

export function Container({
  children,
  className,
}: {
  children: React.ReactNode
  className?: string
}) {
  return (
    <div className={cn("mx-auto max-w-7xl px-4 sm:px-6 lg:px-8", className)}>
      {children}
    </div>
  )
}

export function SectionHeading({
  eyebrow,
  title,
  description,
  align = "left",
  tone = "light",
}: {
  eyebrow?: string
  title: string
  description?: string
  align?: "left" | "center"
  tone?: "light" | "dark"
}) {
  return (
    <div
      className={cn(
        "flex flex-col gap-3",
        align === "center" && "items-center text-center",
      )}
    >
      {eyebrow && (
        <span
          className={cn(
            "text-xs font-semibold uppercase tracking-[0.16em]",
            tone === "dark" ? "text-glow" : "text-primary",
          )}
        >
          {eyebrow}
        </span>
      )}
      <h2
        className={cn(
          "text-balance font-serif text-3xl font-semibold leading-tight tracking-tight sm:text-4xl",
          tone === "dark" ? "text-abyss-foreground" : "text-foreground",
        )}
      >
        {title}
      </h2>
      {description && (
        <p
          className={cn(
            "max-w-2xl text-pretty text-base leading-relaxed",
            tone === "dark" ? "text-abyss-muted" : "text-muted-foreground",
            align === "center" && "mx-auto",
          )}
        >
          {description}
        </p>
      )}
    </div>
  )
}

export function ButtonLink({
  href,
  children,
  variant = "primary",
  className,
  external,
}: {
  href: string
  children: React.ReactNode
  variant?: "primary" | "secondary" | "ghost" | "onDark"
  className?: string
  external?: boolean
}) {
  const variants: Record<string, string> = {
    primary:
      "bg-primary text-primary-foreground hover:-translate-y-0.5 shadow-[var(--shadow-elevated)]",
    secondary:
      "border border-border bg-card text-foreground hover:border-primary/40 hover:text-primary",
    ghost: "text-primary hover:bg-primary/10",
    onDark:
      "bg-glow text-abyss-deep font-semibold hover:-translate-y-0.5",
  }
  return (
    <Link
      href={href}
      {...(external ? { target: "_blank", rel: "noopener noreferrer" } : {})}
      className={cn(
        "inline-flex items-center justify-center gap-2 rounded-full px-5 py-2.5 text-sm font-semibold transition-all duration-200",
        variants[variant],
        className,
      )}
    >
      {children}
    </Link>
  )
}

export function ArrowRight({ className }: { className?: string }) {
  return (
    <svg
      width="16"
      height="16"
      viewBox="0 0 24 24"
      fill="none"
      className={className}
      aria-hidden
    >
      <path
        d="M5 12h14M13 6l6 6-6 6"
        stroke="currentColor"
        strokeWidth="2"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  )
}
