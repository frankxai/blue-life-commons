export interface MediaBenchmark {
  name: string
  category: string
  whatTheyDo: string
  blueLifeMove: string
  sourceLabel: string
  sourceUrl: string
}

export interface MediaSourceLane {
  name: string
  role: string
  bestFor: string
  gate: string
  sourceUrl: string
}

export interface MediaExpansionStep {
  name: string
  outcome: string
  detail: string
}

export const MEDIA_BENCHMARKS: MediaBenchmark[] = [
  {
    name: "iNaturalist and Seek",
    category: "Community observation and image recognition",
    whatTheyDo:
      "iNaturalist exposes supported APIs for observations and Seek uses image recognition built from iNaturalist observations and community identifications.",
    blueLifeMove:
      "Use as a discovery and observation-signal lane, then re-check image rights, species match, welfare context, and exact location sensitivity before public use.",
    sourceLabel: "iNaturalist API and Seek pages",
    sourceUrl: "https://www.inaturalist.org/pages/seek_app",
  },
  {
    name: "GBIF",
    category: "Occurrence media infrastructure",
    whatTheyDo:
      "GBIF indexes occurrence-linked media, supports image cache URLs, and warns that occurrence images can carry more restrictive licenses than the occurrence records.",
    blueLifeMove:
      "Use GBIF for broad media discovery and occurrence context, but store image-level creator, license, publisher, and confirmation state in our own approval record.",
    sourceLabel: "GBIF occurrence image API",
    sourceUrl: "https://techdocs.gbif.org/en/openapi/images",
  },
  {
    name: "Encyclopedia of Life",
    category: "Species knowledge graph",
    whatTheyDo:
      "EOL provides free multilingual biodiversity information and curated structured trait data across a very large species corpus.",
    blueLifeMove:
      "Use EOL as a species-page and trait-source partner, while Blue Life adds public media approval, welfare framing, and action-oriented ocean context.",
    sourceLabel: "Smithsonian EOL overview",
    sourceUrl: "https://naturalhistory.si.edu/research/eol",
  },
  {
    name: "OBIS",
    category: "Marine occurrence intelligence",
    whatTheyDo:
      "OBIS harvests marine occurrence records from thousands of datasets and publishes access routes for visual exploration, APIs, and large-scale analysis.",
    blueLifeMove:
      "Use OBIS for marine distribution, occurrence, and signal context so image pages can connect a species visual to real ocean data without exposing sensitive live locations.",
    sourceLabel: "OBIS data access",
    sourceUrl: "https://obis.org/data/access/",
  },
  {
    name: "WoRMS",
    category: "Marine taxonomy backbone",
    whatTheyDo:
      "WoRMS provides marine species name and AphiaID services through its REST interface.",
    blueLifeMove:
      "Use WoRMS identifiers as the stable marine taxon key before importing or approving images at scale.",
    sourceLabel: "WoRMS REST service",
    sourceUrl: "https://www.marinespecies.org/rest/",
  },
  {
    name: "Wild Me / Wildbook",
    category: "Individual animal photo-identification",
    whatTheyDo:
      "Wild Me provides Wildbook platforms for computational photo-identification and collaboration from imagery collected by researchers, tourists, operators, and the public.",
    blueLifeMove:
      "Partner or interoperate where individual identification matters, while Blue Life stays focused on public species pages, rights-safe visuals, and field action context.",
    sourceLabel: "Wild Me what-we-do",
    sourceUrl: "https://www.wildme.org/what-we-do.html",
  },
  {
    name: "Wildlife Insights",
    category: "Camera-trap workflow",
    whatTheyDo:
      "Wildlife Insights lets teams upload camera-trap photos, apply machine learning identification, analyze data, and explore projects.",
    blueLifeMove:
      "Borrow the workflow lesson: bulk image intake needs upload, machine assist, human verification, analysis, and public-safe publishing as separate stages.",
    sourceLabel: "Wildlife Insights home",
    sourceUrl: "https://www.wildlifeinsights.org/",
  },
  {
    name: "FishBase and SeaLifeBase",
    category: "Fish species facts and media",
    whatTheyDo:
      "FishBase exposes fish species data and picture access routes, with image reuse governed by the linked image and citation rules.",
    blueLifeMove:
      "Treat FishBase as a fish-specific candidate and citation lane, not an automatic public-image license.",
    sourceLabel: "FishBase hints",
    sourceUrl: "https://www.fishbase.se/hints.htm",
  },
]

export const MEDIA_SOURCE_LANES: MediaSourceLane[] = [
  {
    name: "Official and public-domain institutions",
    role: "First-choice primary media",
    bestFor: "NOAA, USFWS, museums, government programs, sanctuaries",
    gate: "Confirm image-level credit, public-domain or license status, and whether non-agency credits require extra permission.",
    sourceUrl: "https://www.fisheries.noaa.gov/national/about-us/website-policies-and-disclaimers",
  },
  {
    name: "Commons and open-license media",
    role: "Fast scalable coverage",
    bestFor: "Wikimedia Commons, iNaturalist open photos, GBIF multimedia records",
    gate: "Require creator, license URL, source page, species-match basis, crop approval, and blocked-surface notes.",
    sourceUrl: "https://commons.wikimedia.org/wiki/Commons:API",
  },
  {
    name: "Biodiversity knowledge networks",
    role: "Taxon and trait enrichment",
    bestFor: "EOL, WoRMS, OBIS, IUCN, FishBase, SeaLifeBase",
    gate: "Use as source context or identifiers; do not infer image rights from data availability.",
    sourceUrl: "https://naturalhistory.si.edu/research/eol",
  },
  {
    name: "Partner and NGO grants",
    role: "High-trust replacement images",
    bestFor: "Conservation NGOs, researchers, sanctuaries, photographers, field programs",
    gate: "Written permission must name surfaces, credit line, expiry, embargoes, and sensitive-location constraints.",
    sourceUrl: "https://www.wildme.org/what-we-do.html",
  },
  {
    name: "Machine-assisted intake",
    role: "Scale review without publishing mistakes",
    bestFor: "Candidate clustering, duplicate checks, taxonomy hints, quality triage",
    gate: "AI suggestions never publish directly; every public visual needs human approval and provenance.",
    sourceUrl: "https://www.wildlifeinsights.org/",
  },
]

export const MEDIA_EXPANSION_STEPS: MediaExpansionStep[] = [
  {
    name: "1. Normalize the taxon key",
    outcome: "One stable animal record",
    detail:
      "Join common name, scientific name, WoRMS or other taxon identifier, artifact id, and page path before collecting images.",
  },
  {
    name: "2. Collect candidates, not assets",
    outcome: "Review-only media queue",
    detail:
      "Pull source pages, thumbnails, file pages, and metadata into reviewer-only records. Do not make candidate image URLs public.",
  },
  {
    name: "3. Score rights and fit",
    outcome: "Prioritized curator lane",
    detail:
      "Rank official/public-domain, open-license, partner-grant, and blocked/needs-permission records by source confidence, license clarity, species match, and welfare risk.",
  },
  {
    name: "4. Approve one primary visual",
    outcome: "Public species media",
    detail:
      "Promote only after image-level rights, credit, alt text, crop, sensitive-location review, and species-match evidence are complete.",
  },
  {
    name: "5. Publish with provenance",
    outcome: "Useful public page",
    detail:
      "Render the image with source, creator, license, approved surfaces, blocked surfaces, and links back to original evidence.",
  },
  {
    name: "6. Keep refreshing",
    outcome: "Living visual commons",
    detail:
      "Track stale images, better partner replacements, new source records, missing taxa, and review gaps as a repeatable operating queue.",
  },
]
