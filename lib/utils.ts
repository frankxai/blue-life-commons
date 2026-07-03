export function cn(...classes: (string | false | null | undefined)[]): string {
  return classes.filter(Boolean).join(" ")
}

export const TYPE_LABELS: Record<string, string> = {
  "species-page": "Species",
  "region-briefing": "Region",
  "field-mission": "Mission",
  "dataset-card": "Dataset",
  "research-summary": "Research",
  "partner-profile": "Partner",
  "welfare-assessment": "Welfare",
}

export const TYPE_HUES: Record<string, string> = {
  "species-page": "var(--color-primary)",
  "region-briefing": "var(--color-kelp)",
  "field-mission": "var(--color-accent)",
  "dataset-card": "var(--color-abyss-muted)",
  "research-summary": "var(--color-abyss-muted)",
  "partner-profile": "var(--color-amber)",
  "welfare-assessment": "var(--color-coral)",
}

export const IUCN_META: Record<
  string,
  { label: string; color: string; textOnColor: string }
> = {
  EX: { label: "Extinct", color: "oklch(0.2 0.02 0)", textOnColor: "#fff" },
  EW: { label: "Extinct in the Wild", color: "oklch(0.3 0.03 0)", textOnColor: "#fff" },
  CR: { label: "Critically Endangered", color: "oklch(0.55 0.2 25)", textOnColor: "#fff" },
  EN: { label: "Endangered", color: "oklch(0.66 0.17 45)", textOnColor: "#fff" },
  VU: { label: "Vulnerable", color: "oklch(0.78 0.14 75)", textOnColor: "#1a1206" },
  NT: { label: "Near Threatened", color: "oklch(0.82 0.11 105)", textOnColor: "#151a06" },
  LC: { label: "Least Concern", color: "oklch(0.62 0.13 150)", textOnColor: "#fff" },
  DD: { label: "Data Deficient", color: "oklch(0.6 0.02 240)", textOnColor: "#fff" },
  NE: { label: "Not Evaluated", color: "oklch(0.7 0.01 240)", textOnColor: "#152030" },
}

export const WELFARE_META: Record<string, { label: string; color: string }> = {
  thriving: { label: "Thriving", color: "var(--color-kelp)" },
  stable: { label: "Stable", color: "var(--color-primary)" },
  pressured: { label: "Pressured", color: "var(--color-amber)" },
  critical: { label: "Critical", color: "var(--color-coral)" },
}

export const GUILD_META: Record<string, { label: string }> = {
  cetaceans: { label: "Cetaceans" },
  "sharks-rays": { label: "Sharks & Rays" },
  turtles: { label: "Sea Turtles" },
  pinnipeds: { label: "Pinnipeds" },
  reefs: { label: "Reefs & Habitat" },
  sirenians: { label: "Sirenians" },
  other: { label: "Other" },
}

export const GITHUB_REPO_URL = "https://github.com/frankxai/blue-life-commons"
export const OCEAN_INTEL_URL = "https://github.com/frankxai/ocean-intelligence-system"

export function formatRegion(s: string): string {
  return titleCase(s)
}

export function titleCase(s: string): string {
  return s
    .replace(/[-_]/g, " ")
    .replace(/\b\w/g, (c) => c.toUpperCase())
}

export function formatDate(input?: string): string {
  if (!input) return ""
  const d = new Date(input)
  if (Number.isNaN(d.getTime())) return input
  return d.toLocaleDateString("en-US", {
    year: "numeric",
    month: "short",
    day: "numeric",
  })
}
