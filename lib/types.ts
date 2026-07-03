export type ArtifactType =
  | "species-page"
  | "region-briefing"
  | "field-mission"
  | "dataset-card"
  | "research-summary"
  | "partner-profile"
  | "welfare-assessment"

export type ReviewState = "required" | "pending" | "approved" | "not-applicable"
export type ArtifactStatus =
  | "draft"
  | "needs-expert-review"
  | "reviewed"
  | "published"

export type IucnCategory =
  | "EX"
  | "EW"
  | "CR"
  | "EN"
  | "VU"
  | "NT"
  | "LC"
  | "DD"
  | "NE"

export interface Source {
  url: string
  title: string
  tier?: 1 | 2 | 3
  accessed?: string
  doi?: string
}

export interface Review {
  science?: ReviewState
  ethics?: ReviewState
  editor?: ReviewState
}

export interface Iucn {
  category?: IucnCategory
  assessment_date?: string
  version?: string
  scope?: string
  population_trend?: string
}

export interface FiveDomains {
  nutrition?: string
  environment?: string
  health?: string
  behaviour?: string
  mental_state?: string
}

export interface Welfare {
  state?: string
  dominant_stressor?: string
  confidence?: string
  five_domains?: FiveDomains
}

export interface Sensitivity {
  tier?: string
  rationale?: string
  generalized_to?: string
}

export interface Impact {
  claim?: string
  eligible_for_hypercert?: boolean
}

export interface Contributor {
  github?: string
  name?: string
}

export interface Outputs {
  website_path?: string
  github_path?: string
  map_layer?: boolean
}

export interface ArtifactMediaPrimary {
  asset_id?: string
  path?: string
  source_url?: string
  public_media_url?: string
  original_media_url?: string
  creator?: string
  credit?: string
  license?: string
  license_url?: string
  rights_status?: string
  alt_text?: string
  qa_status?: string
}

export interface ArtifactMediaEmbed {
  provider?: string
  url?: string
  rights_status?: string
  notes?: string
  domain?: string
  license?: string
}

export interface ArtifactMediaRender {
  strategy?: string
  public_visual_kind?: string
  public_visual_public_use?: boolean
  species_page_visual_slot?: boolean
  species_page_hero_image_allowed?: boolean
  candidate_thumbnail_allowed?: boolean
  candidate_public_use?: boolean
}

export interface ArtifactMediaReview {
  primary_status?: string
  curation_decision?: string
  checks_complete?: number
  checks_total?: number
  promotion_allowed_now?: boolean
}

export interface ArtifactMedia {
  registry_record?: string
  render_contract?: string
  public_explorer_record?: string
  primary?: ArtifactMediaPrimary
  embeds?: ArtifactMediaEmbed[]
  render?: ArtifactMediaRender
  review?: ArtifactMediaReview
}

export interface Artifact {
  id: string
  type: ArtifactType
  title: string
  slug: string
  path: string
  href: string
  githubPath: string
  bodyHtml: string
  bodyText: string
  excerpt: string
  readingMinutes: number

  species_group?: string[]
  species?: string[]
  region?: string[]
  audience?: string[]
  difficulty?: string
  status?: ArtifactStatus
  sources: Source[]
  review?: Review
  iucn?: Iucn
  welfare?: Welfare
  sensitivity?: Sensitivity
  consensus_state?: string
  last_verified?: string
  impact?: Impact
  contributors: Contributor[]
  license?: string
  media?: ArtifactMedia
  mapLayer?: boolean
}

export interface CommonsStats {
  total: number
  species: number
  regions: number
  missions: number
  datasets: number
  research: number
  partners: number
  welfare: number
  sources: number
  contributors: number
  hypercertEligible: number
  reviewed: number
}
