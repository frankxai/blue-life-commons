import Link from "next/link"
import { WaveMark } from "@/components/wave-mark"

const GITHUB = "https://github.com/frankxai/blue-life-commons"

const COLUMNS = [
  {
    title: "Explore",
    links: [
      { href: "/species", label: "Ocean life encyclopedia" },
      { href: "/encyclopedia", label: "All animal entries" },
      { href: "/media-intelligence", label: "Media intelligence" },
      { href: "/regions", label: "Region briefings" },
      { href: "/missions", label: "Field missions" },
      { href: "/research", label: "Research & datasets" },
      { href: "/guardian", label: "Guardian signals" },
      { href: "/catalog", label: "Full catalog" },
    ],
  },
  {
    title: "The commons",
    links: [
      { href: "/impact", label: "Impact ledger" },
      { href: "/governance", label: "Governance & ethics" },
      { href: "/partners", label: "Partners" },
      { href: "/ecosystem", label: "Ecosystem" },
      { href: "/contribute", label: "Contribute" },
    ],
  },
  {
    title: "Sustain it",
    links: [
      { href: "/support", label: "Support the commons" },
      { href: "/services", label: "Services (Starlight)" },
      { href: GITHUB, label: "GitHub repository", external: true },
    ],
  },
]

export function SiteFooter() {
  return (
    <footer className="mt-auto bg-abyss text-abyss-foreground abyss-grid">
      <div className="mx-auto max-w-7xl px-4 py-14 sm:px-6 lg:px-8">
        <div className="grid gap-10 md:grid-cols-[1.4fr_1fr_1fr_1fr]">
          <div className="max-w-xs">
            <Link href="/" className="flex items-center gap-2.5 font-semibold">
              <WaveMark className="size-8 text-glow" />
              <span>Blue Life Commons</span>
            </Link>
            <p className="mt-4 text-sm leading-relaxed text-abyss-muted">
              The open intelligence commons for ocean life. Sources, rights,
              and review state remain visible from GitHub to public record.
            </p>
            <p className="mt-4 text-xs text-abyss-muted">
              A public good stewarded by{" "}
              <span className="text-abyss-foreground">Starlight Intelligence Systems</span>.
            </p>
          </div>

          {COLUMNS.map((col) => (
            <div key={col.title}>
              <h3 className="text-xs font-semibold uppercase tracking-[0.14em] text-glow">
                {col.title}
              </h3>
              <ul className="mt-4 space-y-2.5">
                {col.links.map((link) => (
                  <li key={link.href}>
                    <Link
                      href={link.href}
                      {...("external" in link && link.external
                        ? { target: "_blank", rel: "noopener noreferrer" }
                        : {})}
                      className="text-sm text-abyss-muted transition-colors hover:text-abyss-foreground"
                    >
                      {link.label}
                    </Link>
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>

        <div className="mt-12 flex flex-col gap-4 border-t border-abyss-border pt-6 text-xs text-abyss-muted sm:flex-row sm:items-center sm:justify-between">
          <p>
            Content licensed{" "}
            <a
              href="https://creativecommons.org/licenses/by/4.0/"
              target="_blank"
              rel="noopener noreferrer"
              className="underline underline-offset-2 hover:text-abyss-foreground"
            >
              CC-BY-4.0
            </a>
            . Grounded in cited sources — or silent.
          </p>
          <p>© {new Date().getFullYear()} Blue Life Commons contributors.</p>
        </div>
      </div>
    </footer>
  )
}
