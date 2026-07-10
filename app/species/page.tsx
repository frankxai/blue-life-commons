import type { Metadata } from "next"
import { SpeciesEncyclopedia } from "@/components/species-encyclopedia"

export const metadata: Metadata = {
  title: "Ocean Life Encyclopedia",
  description:
    "An image-first encyclopedia of Blue Life Commons species entries, with Vercel-hosted approved animal images, source links, rights metadata, and citations.",
  alternates: { canonical: "/species" },
  openGraph: { url: "/species" },
}

export default function SpeciesIndexPage() {
  return <SpeciesEncyclopedia />
}
