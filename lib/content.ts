import fs from "node:fs"
import path from "node:path"
import matter from "gray-matter"
import { marked } from "marked"
import type { Artifact, ArtifactMedia, ArtifactType, CommonsStats, Source } from "./types"

const ROOT = process.cwd()

// Directories that hold publishable artifacts, mapped to how we scan them.
const CONTENT_ROOTS = [
  path.join(ROOT, "content"),
  path.join(ROOT, "missions"),
]

// Files/directories we never treat as publishable artifacts.
const IGNORE_SEGMENTS = new Set([
  "_templates",
  "templates",
  "node_modules",
  ".git",
  ".next",
])

marked.setOptions({ gfm: true, breaks: false })

function walk(dir: string, acc: string[] = []): string[] {
  if (!fs.existsSync(dir)) return acc
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    if (IGNORE_SEGMENTS.has(entry.name)) continue
    const full = path.join(dir, entry.name)
    if (entry.isDirectory()) {
      walk(full, acc)
    } else if (entry.isFile() && entry.name.endsWith(".md")) {
      // README/index files are navigation, not artifacts.
      if (entry.name.toLowerCase() === "readme.md") continue
      acc.push(full)
    }
  }
  return acc
}

const VALID_TYPES: ArtifactType[] = [
  "species-page",
  "region-briefing",
  "field-mission",
  "dataset-card",
  "research-summary",
  "partner-profile",
  "welfare-assessment",
]

function toArray(value: unknown): string[] {
  if (!value) return []
  if (Array.isArray(value)) return value.map((v) => String(v))
  return [String(value)]
}

function normalizeSources(raw: unknown): Source[] {
  if (!Array.isArray(raw)) return []
  return raw
    .filter((s) => s && typeof s === "object")
    .map((s) => {
      const src = s as Record<string, unknown>
      return {
        url: String(src.url ?? ""),
        title: String(src.title ?? src.url ?? "Source"),
        tier: src.tier ? (Number(src.tier) as 1 | 2 | 3) : undefined,
        accessed: src.accessed ? String(src.accessed) : undefined,
        doi: src.doi ? String(src.doi) : undefined,
      }
    })
    .filter((s) => s.url)
}

function asRecord(value: unknown): Record<string, unknown> | undefined {
  return value && typeof value === "object" && !Array.isArray(value)
    ? (value as Record<string, unknown>)
    : undefined
}

function optionalString(value: unknown): string | undefined {
  if (value === undefined || value === null || value === "") return undefined
  return String(value)
}

function optionalBoolean(value: unknown): boolean | undefined {
  return typeof value === "boolean" ? value : undefined
}

function optionalNumber(value: unknown): number | undefined {
  if (value === undefined || value === null || value === "") return undefined
  const n = Number(value)
  return Number.isFinite(n) ? n : undefined
}

function normalizeMedia(raw: unknown): ArtifactMedia | undefined {
  const media = asRecord(raw)
  if (!media) return undefined

  const primary = asRecord(media.primary)
  const render = asRecord(media.render)
  const review = asRecord(media.review)

  const embeds = Array.isArray(media.embeds)
    ? media.embeds
        .map(asRecord)
        .filter((embed): embed is Record<string, unknown> => Boolean(embed))
        .map((embed) => ({
          provider: optionalString(embed.provider),
          url: optionalString(embed.url),
          rights_status: optionalString(embed.rights_status),
          notes: optionalString(embed.notes),
          domain: optionalString(embed.domain),
          license: optionalString(embed.license),
        }))
    : undefined

  return {
    registry_record: optionalString(media.registry_record),
    render_contract: optionalString(media.render_contract),
    public_explorer_record: optionalString(media.public_explorer_record),
    primary: primary
      ? {
          asset_id: optionalString(primary.asset_id),
          path: optionalString(primary.path),
          source_url: optionalString(primary.source_url),
          public_media_url: optionalString(primary.public_media_url),
          original_media_url: optionalString(primary.original_media_url),
          creator: optionalString(primary.creator),
          credit: optionalString(primary.credit),
          license: optionalString(primary.license),
          license_url: optionalString(primary.license_url),
          rights_status: optionalString(primary.rights_status),
          alt_text: optionalString(primary.alt_text),
          qa_status: optionalString(primary.qa_status),
        }
      : undefined,
    embeds,
    render: render
      ? {
          strategy: optionalString(render.strategy),
          public_visual_kind: optionalString(render.public_visual_kind),
          public_visual_public_use: optionalBoolean(render.public_visual_public_use),
          species_page_visual_slot: optionalBoolean(render.species_page_visual_slot),
          species_page_hero_image_allowed: optionalBoolean(render.species_page_hero_image_allowed),
          candidate_thumbnail_allowed: optionalBoolean(render.candidate_thumbnail_allowed),
          candidate_public_use: optionalBoolean(render.candidate_public_use),
        }
      : undefined,
    review: review
      ? {
          primary_status: optionalString(review.primary_status),
          curation_decision: optionalString(review.curation_decision),
          checks_complete: optionalNumber(review.checks_complete),
          checks_total: optionalNumber(review.checks_total),
          promotion_allowed_now: optionalBoolean(review.promotion_allowed_now),
        }
      : undefined,
  }
}

function stripMarkdown(md: string): string {
  return md
    .replace(/```[\s\S]*?```/g, " ")
    .replace(/!\[[^\]]*\]\([^)]*\)/g, " ")
    .replace(/\[([^\]]*)\]\([^)]*\)/g, "$1")
    .replace(/[#>*_`~|-]/g, " ")
    .replace(/\s+/g, " ")
    .trim()
}

let cache: Artifact[] | null = null

export function getAllArtifacts(): Artifact[] {
  if (cache) return cache

  const files = CONTENT_ROOTS.flatMap((root) => walk(root))
  const artifacts: Artifact[] = []

  for (const file of files) {
    const raw = fs.readFileSync(file, "utf8")
    const { data, content } = matter(raw)
    const type = data.type as ArtifactType | undefined
    if (!type || !VALID_TYPES.includes(type)) continue

    const relPath = path.relative(ROOT, file).replace(/\\/g, "/")
    const outputs = (data.outputs ?? {}) as Record<string, unknown>
    const href =
      (outputs.website_path as string | undefined) ??
      "/" + relPath.replace(/\.md$/, "")
    const slug = href.split("/").filter(Boolean).slice(-1)[0] ?? data.id

    // If sources exist in frontmatter, drop the markdown "Sources" section —
    // the site renders a structured sources grid instead.
    const sources = normalizeSources(data.sources)
    let body = content
    if (sources.length > 0) {
      body = body.replace(/^##\s+Sources\s*$[\s\S]*?(?=^##\s|(?![\s\S]))/m, "")
    }

    const bodyText = stripMarkdown(body)
    const bodyHtml = marked.parse(body) as string
    const words = bodyText ? bodyText.split(/\s+/).length : 0

    // Excerpts: prefer frontmatter summary; otherwise use the body with the
    // leading H1 and the "Status: needs expert review..." blockquote removed
    // so cards lead with real content instead of boilerplate.
    let excerptSource = data.summary ? String(data.summary) : ""
    if (!excerptSource) {
      const cleaned = body
        .split("\n")
        .filter(
          (line) =>
            !/^#{1,6}\s/.test(line) &&
            !/^\s*\|/.test(line) &&
            !/^>\s*Status:/i.test(line),
        )
        .join("\n")
      excerptSource = stripMarkdown(cleaned)
    }
    const excerpt = excerptSource.slice(0, 220).trim()

    artifacts.push({
      id: String(data.id ?? slug),
      type,
      title: String(data.title ?? slug),
      slug: String(slug),
      path: relPath,
      href,
      githubPath: String(outputs.github_path ?? relPath),
      bodyHtml,
      bodyText,
      excerpt,
      readingMinutes: Math.max(1, Math.round(words / 200)),
      species_group: toArray(data.species_group),
      species: toArray(data.species),
      region: toArray(data.region),
      audience: toArray(data.audience),
      difficulty: data.difficulty ? String(data.difficulty) : undefined,
      status: data.status,
      sources,
      review: data.review,
      iucn: data.iucn,
      welfare: data.welfare,
      sensitivity: data.sensitivity,
      consensus_state: data.consensus_state ? String(data.consensus_state) : undefined,
      last_verified: data.last_verified ? String(data.last_verified) : undefined,
      impact: data.impact,
      contributors: Array.isArray(data.contributors) ? data.contributors : [],
      license: data.license ? String(data.license) : undefined,
      media: normalizeMedia(data.media),
      mapLayer: Boolean(outputs.map_layer),
    })
  }

  artifacts.sort((a, b) => a.title.localeCompare(b.title))
  cache = artifacts
  return artifacts
}

export function getArtifactsByType(type: ArtifactType): Artifact[] {
  return getAllArtifacts().filter((a) => a.type === type)
}

export function getArtifactByHref(href: string): Artifact | undefined {
  const normalized = "/" + href.split("/").filter(Boolean).join("/")
  return getAllArtifacts().find((a) => a.href === normalized)
}

export function getArtifactById(id: string): Artifact | undefined {
  return getAllArtifacts().find((a) => a.id === id)
}

export function getSpeciesGuilds(): { guild: string; count: number }[] {
  const map = new Map<string, number>()
  for (const a of getArtifactsByType("species-page")) {
    // guild is the folder under content/species/<guild>/
    const parts = a.path.split("/")
    const idx = parts.indexOf("species")
    const guild = idx >= 0 && parts[idx + 1] ? parts[idx + 1] : "other"
    map.set(guild, (map.get(guild) ?? 0) + 1)
  }
  return [...map.entries()]
    .map(([guild, count]) => ({ guild, count }))
    .sort((a, b) => b.count - a.count)
}

export function getGuildForArtifact(a: Artifact): string {
  const parts = a.path.split("/")
  const idx = parts.indexOf("species")
  return idx >= 0 && parts[idx + 1] ? parts[idx + 1] : "other"
}

export function getRelatedArtifacts(a: Artifact, limit = 4): Artifact[] {
  const all = getAllArtifacts().filter((x) => x.id !== a.id)
  const scored = all.map((x) => {
    let score = 0
    const overlap = (arr1?: string[], arr2?: string[]) => {
      if (!arr1 || !arr2) return 0
      const set = new Set(arr1)
      return arr2.filter((v) => set.has(v)).length
    }
    score += overlap(a.species_group, x.species_group) * 2
    score += overlap(a.species, x.species) * 3
    score += overlap(a.region, x.region) * 2
    if (x.type === a.type) score += 1
    return { x, score }
  })
  return scored
    .filter((s) => s.score > 0)
    .sort((a, b) => b.score - a.score)
    .slice(0, limit)
    .map((s) => s.x)
}

/**
 * Load a plain markdown document (governance, docs) as HTML.
 * Returns null if the file does not exist.
 */
export function getDocHtml(relativePath: string): { title: string; html: string } | null {
  const filePath = path.join(ROOT, relativePath)
  if (!fs.existsSync(filePath)) return null
  const raw = fs.readFileSync(filePath, "utf-8")
  const { content } = matter(raw)
  const titleMatch = content.match(/^#\s+(.+)$/m)
  const title = titleMatch ? titleMatch[1].trim() : relativePath
  // Drop the first H1 — pages render their own title.
  const body = content.replace(/^#\s+.+$/m, "")
  return { title, html: marked.parse(body) as string }
}

export function getCommonsStats(): CommonsStats {
  const all = getAllArtifacts()
  const sourceUrls = new Set<string>()
  const contributors = new Set<string>()
  let hypercertEligible = 0
  let reviewed = 0

  for (const a of all) {
    for (const s of a.sources) sourceUrls.add(s.url)
    for (const c of a.contributors) if (c.github) contributors.add(c.github)
    if (a.impact?.eligible_for_hypercert) hypercertEligible++
    if (a.status === "reviewed" || a.status === "published") reviewed++
  }

  const count = (t: ArtifactType) => all.filter((a) => a.type === t).length

  return {
    total: all.length,
    species: count("species-page"),
    regions: count("region-briefing"),
    missions: count("field-mission"),
    datasets: count("dataset-card"),
    research: count("research-summary"),
    partners: count("partner-profile"),
    welfare: count("welfare-assessment"),
    sources: sourceUrls.size,
    contributors: contributors.size,
    hypercertEligible,
    reviewed,
  }
}
