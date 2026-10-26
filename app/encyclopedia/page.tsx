import { baseOpenGraph } from "@/lib/open-graph"
import type { Metadata } from "next"
import { SpeciesEncyclopedia } from "@/components/species-encyclopedia"

export const metadata: Metadata = {
  title: "Ocean Life Encyclopedia",
  description:
    "The public Blue Life Commons encyclopedia for ocean animals, approved images, source provenance, rights metadata, and species entries.",
  alternates: { canonical: "/encyclopedia" },
  openGraph: { ...baseOpenGraph, url: "/encyclopedia" },
}

export default function EncyclopediaPage() {
  return <SpeciesEncyclopedia />
}
