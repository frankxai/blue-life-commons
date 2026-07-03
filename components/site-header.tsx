"use client"

import Link from "next/link"
import { usePathname } from "next/navigation"
import { useEffect, useState } from "react"
import { cn } from "@/lib/utils"
import { WaveMark } from "@/components/wave-mark"

const NAV = [
  { href: "/species", label: "Species" },
  { href: "/regions", label: "Regions" },
  { href: "/missions", label: "Missions" },
  { href: "/guardian", label: "Guardian" },
  { href: "/catalog", label: "Catalog" },
  { href: "/impact", label: "Impact" },
  { href: "/governance", label: "Governance" },
]

export function SiteHeader() {
  const pathname = usePathname()
  const [open, setOpen] = useState(false)
  const [scrolled, setScrolled] = useState(false)

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 8)
    onScroll()
    window.addEventListener("scroll", onScroll, { passive: true })
    return () => window.removeEventListener("scroll", onScroll)
  }, [])

  useEffect(() => {
    setOpen(false)
  }, [pathname])

  return (
    <header
      className={cn(
        "sticky top-0 z-50 border-b transition-colors duration-300",
        scrolled
          ? "border-border bg-background/85 backdrop-blur-md"
          : "border-transparent bg-background/40 backdrop-blur-sm",
      )}
    >
      <div className="mx-auto flex h-16 max-w-7xl items-center justify-between gap-4 px-4 sm:px-6 lg:px-8">
        <Link
          href="/"
          className="flex items-center gap-2.5 font-semibold tracking-tight"
        >
          <WaveMark className="size-8 text-primary" />
          <span className="flex flex-col leading-none">
            <span className="text-[15px]">Blue Life Commons</span>
            <span className="text-[10px] font-normal uppercase tracking-[0.16em] text-muted-foreground">
              Ocean Intelligence
            </span>
          </span>
        </Link>

        <nav className="hidden items-center gap-1 lg:flex" aria-label="Primary">
          {NAV.map((item) => {
            const active =
              pathname === item.href || pathname.startsWith(item.href + "/")
            return (
              <Link
                key={item.href}
                href={item.href}
                className={cn(
                  "rounded-full px-3.5 py-2 text-sm font-medium transition-colors",
                  active
                    ? "bg-primary/10 text-primary"
                    : "text-muted-foreground hover:bg-muted hover:text-foreground",
                )}
              >
                {item.label}
              </Link>
            )
          })}
        </nav>

        <div className="flex items-center gap-2">
          <Link
            href="/support"
            className="hidden rounded-full bg-primary px-4 py-2 text-sm font-semibold text-primary-foreground transition-transform hover:-translate-y-0.5 sm:inline-flex"
          >
            Support the commons
          </Link>
          <button
            type="button"
            onClick={() => setOpen((v) => !v)}
            className="inline-flex size-10 items-center justify-center rounded-full border border-border text-foreground lg:hidden"
            aria-expanded={open}
            aria-controls="mobile-nav"
            aria-label="Toggle menu"
          >
            <MenuIcon open={open} />
          </button>
        </div>
      </div>

      {open && (
        <div
          id="mobile-nav"
          className="border-t border-border bg-background lg:hidden"
        >
          <nav
            className="mx-auto flex max-w-7xl flex-col px-4 py-3 sm:px-6"
            aria-label="Mobile"
          >
            {[...NAV, { href: "/contribute", label: "Contribute" }, { href: "/services", label: "Services" }].map(
              (item) => (
                <Link
                  key={item.href}
                  href={item.href}
                  className="rounded-lg px-3 py-3 text-base font-medium text-foreground hover:bg-muted"
                >
                  {item.label}
                </Link>
              ),
            )}
            <Link
              href="/support"
              className="mt-2 rounded-full bg-primary px-4 py-3 text-center text-base font-semibold text-primary-foreground"
            >
              Support the commons
            </Link>
          </nav>
        </div>
      )}
    </header>
  )
}

function MenuIcon({ open }: { open: boolean }) {
  return (
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" aria-hidden>
      {open ? (
        <path
          d="M6 6l12 12M18 6L6 18"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinecap="round"
        />
      ) : (
        <path
          d="M4 7h16M4 12h16M4 17h16"
          stroke="currentColor"
          strokeWidth="2"
          strokeLinecap="round"
        />
      )}
    </svg>
  )
}
