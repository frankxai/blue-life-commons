import type { Metadata } from "next"
import { Suspense } from "react"
import { getAllArtifacts } from "@/lib/content"
import { getApprovedSpeciesMedia } from "@/lib/media"
import { Container, SectionHeading } from "@/components/primitives"
import { CatalogExplorer, type CatalogItem } from "@/components/catalog-explorer"

export const metadata: Metadata = {
  title: "Catalog",
  description:
    "The full catalog of the Blue Life Commons — every species page, region briefing, field mission, dataset card and welfare assessment, searchable and filterable.",
}

export default function CatalogPage() {
  const items: CatalogItem[] = getAllArtifacts().map((a) => ({
    id: a.id,
    type: a.type,
    title: a.title,
    href: a.href,
    excerpt: a.excerpt,
    region: a.region ?? [],
    audience: a.audience ?? [],
    iucn: a.iucn?.category,
    status: a.status,
    sourceCount: a.sources.length,
    media: getApprovedSpeciesMedia(a),
  }))

  return (
    <main>
      <div className="border-b border-border bg-secondary">
        <Container className="py-14 sm:py-20">
          <SectionHeading
            eyebrow="Full catalog"
            title="Everything the commons has verified"
            description={`${items.length} artifacts across seven types — every one cited, licensed CC-BY, and versioned on GitHub.`}
          />
        </Container>
      </div>
      <Container className="py-10 sm:py-14">
        <Suspense>
          <CatalogExplorer items={items} />
        </Suspense>
      </Container>
    </main>
  )
}
