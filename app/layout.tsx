import type { Metadata, Viewport } from "next"
import { ViewTransition } from "react"
import { Geist, Geist_Mono, Newsreader } from "next/font/google"
import { SiteHeader } from "@/components/site-header"
import { SiteFooter } from "@/components/site-footer"
import "./globals.css"

const geistSans = Geist({
  subsets: ["latin"],
  variable: "--font-geist-sans",
  display: "swap",
})
const geistMono = Geist_Mono({
  subsets: ["latin"],
  variable: "--font-geist-mono",
  display: "swap",
})
const newsreader = Newsreader({
  subsets: ["latin"],
  variable: "--font-newsreader",
  display: "swap",
  style: ["normal", "italic"],
})

const SITE_URL = "https://bluelifecommons.org"

export const metadata: Metadata = {
  metadataBase: new URL(SITE_URL),
  title: {
    default: "Blue Life Commons — The open intelligence commons for ocean life",
    template: "%s — Blue Life Commons",
  },
  description:
    "An open, source-led commons of ocean intelligence. Every species page, region briefing, field mission and dataset is cited, ethics-reviewed, and versioned on GitHub. Free for everyone, forever.",
  keywords: [
    "ocean intelligence",
    "marine conservation",
    "open commons",
    "species intelligence",
    "marine biodiversity",
    "citizen science",
    "ocean data",
  ],
  authors: [{ name: "Starlight Intelligence Systems" }],
  openGraph: {
    type: "website",
    url: SITE_URL,
    title: "Blue Life Commons",
    description:
      "The open intelligence commons for ocean life — sourced, ethics-reviewed, and free for everyone.",
    siteName: "Blue Life Commons",
  },
  twitter: {
    card: "summary_large_image",
    title: "Blue Life Commons",
    description:
      "The open intelligence commons for ocean life — sourced, ethics-reviewed, and free for everyone.",
  },
}

export const viewport: Viewport = {
  themeColor: "#0b1f2a",
  colorScheme: "light",
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html
      lang="en"
      className={`${geistSans.variable} ${geistMono.variable} ${newsreader.variable} bg-background`}
    >
      <body className="min-h-dvh flex flex-col antialiased">
        <a
          href="#main"
          className="sr-only focus:not-sr-only focus:fixed focus:left-4 focus:top-4 focus:z-[100] focus:rounded-md focus:bg-primary focus:px-4 focus:py-2 focus:text-primary-foreground"
        >
          Skip to content
        </a>
        <SiteHeader />
        <ViewTransition
          enter={{ "nav-forward": "nav-forward", "nav-back": "nav-back", default: "none" }}
          exit={{ "nav-forward": "nav-forward", "nav-back": "nav-back", default: "none" }}
          default="none"
        >
          <main id="main" className="flex-1">
            {children}
          </main>
        </ViewTransition>
        <SiteFooter />
      </body>
    </html>
  )
}
