import type { Metadata } from "next"

export const WHALE_SHARK_IMAGE =
  "https://commons.wikimedia.org/wiki/Special:FilePath/OLYMPUS_DIGITAL_CAMERA_%2827591269541%29.jpg?width=1200"

export const WHALE_SHARK_ALT =
  "Whale shark from the Blue Life Commons approved CC0 species media record."

// Next.js replaces a parent's openGraph object instead of merging it, so a page
// that sets only { url } silently drops the site image. Every page spreads this.
export const baseOpenGraph = {
  type: "website",
  siteName: "Blue Life Commons",
  images: [{ url: WHALE_SHARK_IMAGE, alt: WHALE_SHARK_ALT }],
} satisfies NonNullable<Metadata["openGraph"]>
