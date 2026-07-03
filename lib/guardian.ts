import "server-only"

// Live biodiversity signals from the same open, keyless data sources the Ocean
// Intelligence System connectors use: OBIS (marine occurrence records) and GBIF
// (global biodiversity occurrences). Every fetch is cached and degrades
// gracefully — if a source is silent, the signal is marked unavailable rather
// than faked.

const REVALIDATE_SECONDS = 60 * 60 * 6 // 6 hours

export interface SpeciesSignal {
  name: string
  scientificName: string
  href?: string
  iucn?: string
  guild: string
  obisRecords: number | null
  gbifRecords: number | null
  datasets: number | null
  yearRange: [number, number] | null
  available: boolean
}

export interface RecentObservation {
  scientificName: string
  commonName: string
  date: string | null
  country: string | null
  dataset: string | null
}

export interface GuardianData {
  species: SpeciesSignal[]
  recent: RecentObservation[]
  totals: {
    obisRecords: number
    gbifRecords: number
    speciesTracked: number
    sourcesLive: number
    sourcesTotal: number
  }
  fetchedAt: string
  degraded: boolean
}

// Curated flagship set spanning guilds, keyed to their commons pages.
const WATCHLIST: {
  name: string
  scientificName: string
  href: string
  iucn: string
  guild: string
}[] = [
  { name: "Orca", scientificName: "Orcinus orca", href: "/species/cetaceans/orca", iucn: "DD", guild: "Cetaceans" },
  { name: "Blue Whale", scientificName: "Balaenoptera musculus", href: "/species/cetaceans/blue-whale", iucn: "EN", guild: "Cetaceans" },
  { name: "Humpback Whale", scientificName: "Megaptera novaeangliae", href: "/species/cetaceans/humpback-whale", iucn: "LC", guild: "Cetaceans" },
  { name: "North Atlantic Right Whale", scientificName: "Eubalaena glacialis", href: "/species/cetaceans/north-atlantic-right-whale", iucn: "CR", guild: "Cetaceans" },
  { name: "Whale Shark", scientificName: "Rhincodon typus", href: "/species/sharks-rays/whale-shark", iucn: "EN", guild: "Sharks & Rays" },
  { name: "Great White Shark", scientificName: "Carcharodon carcharias", href: "/species/sharks-rays/great-white-shark", iucn: "VU", guild: "Sharks & Rays" },
  { name: "Reef Manta Ray", scientificName: "Mobula alfredi", href: "/species/sharks-rays/reef-manta-ray", iucn: "VU", guild: "Sharks & Rays" },
  { name: "Leatherback Turtle", scientificName: "Dermochelys coriacea", href: "/species/turtles/leatherback-turtle", iucn: "VU", guild: "Sea Turtles" },
  { name: "Green Turtle", scientificName: "Chelonia mydas", href: "/species/turtles/green-turtle", iucn: "EN", guild: "Sea Turtles" },
  { name: "Hawaiian Monk Seal", scientificName: "Neomonachus schauinslandi", href: "/species/pinnipeds/hawaiian-monk-seal", iucn: "EN", guild: "Pinnipeds" },
  { name: "California Sea Lion", scientificName: "Zalophus californianus", href: "/species/pinnipeds/california-sea-lion", iucn: "LC", guild: "Pinnipeds" },
  { name: "Elkhorn Coral", scientificName: "Acropora palmata", href: "/species/reefs/elkhorn-coral", iucn: "CR", guild: "Reefs & Habitat" },
]

async function fetchJson(url: string): Promise<any | null> {
  try {
    const res = await fetch(url, {
      next: { revalidate: REVALIDATE_SECONDS },
      headers: { "User-Agent": "BlueLifeCommons/1.0 (+https://github.com/frankxai/blue-life-commons)" },
    })
    if (!res.ok) return null
    return await res.json()
  } catch {
    return null
  }
}

async function fetchObis(scientificName: string) {
  const data = await fetchJson(
    `https://api.obis.org/v3/statistics?scientificname=${encodeURIComponent(scientificName)}`,
  )
  if (!data) return null
  return {
    records: typeof data.records === "number" ? data.records : null,
    datasets: typeof data.datasets === "number" ? data.datasets : null,
    yearRange: Array.isArray(data.yearrange) && data.yearrange.length === 2
      ? ([data.yearrange[0], data.yearrange[1]] as [number, number])
      : null,
  }
}

async function fetchGbifCount(scientificName: string): Promise<number | null> {
  const data = await fetchJson(
    `https://api.gbif.org/v1/occurrence/search?scientificName=${encodeURIComponent(scientificName)}&limit=0`,
  )
  if (!data) return null
  return typeof data.count === "number" ? data.count : null
}

async function fetchRecent(entry: (typeof WATCHLIST)[number]): Promise<RecentObservation | null> {
  const data = await fetchJson(
    `https://api.gbif.org/v1/occurrence/search?scientificName=${encodeURIComponent(entry.scientificName)}&limit=1&hasCoordinate=true`,
  )
  const r = data?.results?.[0]
  if (!r) return null
  return {
    scientificName: entry.scientificName,
    commonName: entry.name,
    date: r.eventDate ?? null,
    country: r.country ?? null,
    dataset: r.datasetName ?? null,
  }
}

export async function getGuardianData(): Promise<GuardianData> {
  // Fan out all requests in parallel — independent per species and source.
  const signalResults = await Promise.all(
    WATCHLIST.map(async (entry): Promise<SpeciesSignal> => {
      const [obis, gbif] = await Promise.all([
        fetchObis(entry.scientificName),
        fetchGbifCount(entry.scientificName),
      ])
      return {
        name: entry.name,
        scientificName: entry.scientificName,
        href: entry.href,
        iucn: entry.iucn,
        guild: entry.guild,
        obisRecords: obis?.records ?? null,
        gbifRecords: gbif,
        datasets: obis?.datasets ?? null,
        yearRange: obis?.yearRange ?? null,
        available: obis !== null || gbif !== null,
      }
    }),
  )

  const recentResults = (
    await Promise.all(WATCHLIST.slice(0, 8).map(fetchRecent))
  ).filter((r): r is RecentObservation => r !== null)

  recentResults.sort((a, b) => (b.date ?? "").localeCompare(a.date ?? ""))

  const obisRecords = signalResults.reduce((sum, s) => sum + (s.obisRecords ?? 0), 0)
  const gbifRecords = signalResults.reduce((sum, s) => sum + (s.gbifRecords ?? 0), 0)
  const anyLive = signalResults.some((s) => s.available)

  return {
    species: signalResults,
    recent: recentResults,
    totals: {
      obisRecords,
      gbifRecords,
      speciesTracked: signalResults.filter((s) => s.available).length,
      sourcesLive: (obisRecords > 0 ? 1 : 0) + (gbifRecords > 0 ? 1 : 0),
      sourcesTotal: 2,
    },
    fetchedAt: new Date().toISOString(),
    degraded: !anyLive,
  }
}
