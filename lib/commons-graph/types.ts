/**
 * CommonsGraph.v1 — the claim/provenance graph of Blue Life Commons.
 *
 * This file is the stable typed contract. Downstream consumers (notably the
 * Ocean Intelligence Guardian product) import `SpeciesNode`, `RegionNode` and
 * `RightsNode` from here. Adding optional fields is a minor change; renaming or
 * removing an exported name requires a new SCHEMA_VERSION.
 *
 * The commons is a reviewed knowledge record, not a monitoring system. Nothing
 * in this graph is live; every node carries the provenance of how it got here.
 */

export const SCHEMA_VERSION = "CommonsGraph.v1" as const
export type SchemaVersion = typeof SCHEMA_VERSION

/* ------------------------------------------------------------------ *
 * Node and edge kinds
 * ------------------------------------------------------------------ */

export type NodeKind =
  | "Taxon"
  | "Species"
  | "Region"
  | "Habitat"
  | "Observation"
  | "Claim"
  | "Source"
  | "Dataset"
  | "MediaAsset"
  | "Rights"
  | "EthicsRule"
  | "Review"
  | "Artifact"
  | "Contributor"
  | "Contradiction"
  | "Supersession"

export type EdgeKind =
  /** Claim -> Source. The citation that carries the claim. */
  | "cites"
  /** Claim -> Species | Region | Habitat | Taxon. What the claim is about. */
  | "about"
  /** Review -> Claim | Artifact. A reviewer's verdict on a specific version. */
  | "reviews"
  /** Contradiction -> Claim. Both sides are attached; neither is deleted. */
  | "contradicts"
  /** Supersession -> Claim. The editorial act that retires a claim version. */
  | "supersedes"
  /** Observation -> Species. What was seen. */
  | "observed"
  /** Observation | Source -> Dataset. Where the record came from. */
  | "drawnFrom"
  /** MediaAsset -> Rights. Licence and permission record for an asset. */
  | "licensedUnder"
  /** EthicsRule -> Species | Region | MediaAsset. What the rule constrains. */
  | "constrains"
  /** Artifact -> Claim | MediaAsset. What a published page is built from. */
  | "composes"
  /** Contributor -> Artifact | Claim | MediaAsset. Attribution. */
  | "contributed"
  /** Species -> Taxon, Habitat -> Region. Containment. */
  | "partOf"

/* ------------------------------------------------------------------ *
 * Universal node metadata — owner, provenance, version, visibility, evaluation
 * ------------------------------------------------------------------ */

/** How a node came to exist. `inferred` never reads as established fact. */
export type ProvenanceMethod =
  /** A person wrote it and stands behind it. */
  | "authored"
  /** Copied from a named external record without transformation. */
  | "imported"
  /** Computed from other nodes by a deterministic, auditable rule. */
  | "derived"
  /** Produced by a model or heuristic. Always surfaced as inferred. */
  | "inferred"

export interface Provenance {
  method: ProvenanceMethod
  /** Contributor ids or agent identifiers responsible for this node version. */
  by: string[]
  /** ISO date the node version was produced. */
  at: string
  /** For `imported`: the external system and record id. */
  importedFrom?: { system: string; recordId: string; url?: string }
  /** For `derived` / `inferred`: the rule or model that produced it. */
  rule?: string
  /** Node ids this version was computed from. */
  inputs?: string[]
}

/**
 * Publication visibility. `restricted` nodes exist in the graph but are
 * withheld from public export; `embargoed` additionally carries a release date.
 */
export type Visibility = "public" | "restricted" | "embargoed"

/**
 * Every node declares how it is to be judged. The rule is named, not free text,
 * so a validator can actually run it.
 */
export type EvaluationRuleName =
  /** Needs an approved Review at the current node version. */
  | "review-required"
  /** Needs at least one resolvable citation. */
  | "citation-required"
  /** Needs a Rights node with a licence in the allowlist. */
  | "rights-required"
  /** Needs an EthicsRule check to pass before public export. */
  | "ethics-gated"
  /** Machine-generated; correctness is the rule's, not a reviewer's. */
  | "derived-only"

export interface Evaluation {
  rule: EvaluationRuleName
  /** ISO date the rule was last run against this node version. */
  lastEvaluated?: string
}

export interface NodeMeta {
  owner: string
  provenance: Provenance
  /** Integer, monotonic per node id. Reviews bind to a specific version. */
  version: number
  visibility: Visibility
  evaluation: Evaluation
}

export interface GraphNodeBase<K extends NodeKind> extends NodeMeta {
  id: string
  kind: K
  label: string
}

export interface GraphEdge extends NodeMeta {
  id: string
  kind: EdgeKind
  from: string
  to: string
  note?: string
}

/* ------------------------------------------------------------------ *
 * Domain nodes
 * ------------------------------------------------------------------ */

export type TaxonRank =
  | "kingdom"
  | "phylum"
  | "class"
  | "order"
  | "family"
  | "genus"
  | "species"

export interface TaxonNode extends GraphNodeBase<"Taxon"> {
  rank: TaxonRank
  scientificName: string
  parentTaxonId?: string
}

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

/**
 * GBIF's four-category generalization model, extended with `public` and
 * `extreme`. Anything at `medium` or above is never published with coordinates.
 */
export type LocationSensitivity = "public" | "low" | "medium" | "high" | "extreme"

export interface SpeciesNode extends GraphNodeBase<"Species"> {
  scientificName: string
  commonName?: string
  taxonId: string
  /** Conservation status is itself a claim; this is the cached head value. */
  iucnCategory?: IucnCategory
  iucnClaimId?: string
  protection: {
    locationSensitivity: LocationSensitivity
    rationale?: string
    /** Ids of EthicsRule nodes that constrain how this species is published. */
    ethicsRuleIds?: string[]
  }
}

export interface RegionNode extends GraphNodeBase<"Region"> {
  /** Stable slug used across the commons and by downstream consumers. */
  slug: string
  /** Coarse bounding box. Regions are the public unit of place. */
  bbox?: [west: number, south: number, east: number, north: number]
  /** ISO 3166 codes the region overlaps, where meaningful. */
  countries?: string[]
  parentRegionId?: string
}

export interface HabitatNode extends GraphNodeBase<"Habitat"> {
  regionId: string
  habitatType: string
  depthRangeMeters?: [number, number]
}

export interface Coordinates {
  lat: number
  lon: number
  /** Coordinate uncertainty as recorded by the source, in metres. */
  uncertaintyMeters?: number
}

export interface ObservationNode extends GraphNodeBase<"Observation"> {
  speciesId: string
  /** ISO date of the observation, not of its import. */
  observedAt: string
  /** Raw coordinates. Never exported publicly for protected species. */
  coordinates?: Coordinates
  regionId?: string
  datasetId?: string
  individualCount?: number
}

/**
 * Claim classes drive citation freshness. A morphology claim ages slowly; a
 * population estimate does not.
 */
export type ClaimClass =
  | "taxonomy"
  | "morphology"
  | "behavior"
  | "distribution"
  | "population-estimate"
  | "conservation-status"
  | "regulation"
  | "threat"
  | "other"

/**
 * Derived, never hand-set. `deriveClaimStatus` computes it from Review,
 * Contradiction and source-freshness records.
 */
export type ClaimStatus = "reviewed" | "disputed" | "stale" | "inferred"

export interface ClaimNode extends GraphNodeBase<"Claim"> {
  claimClass: ClaimClass
  /** The assertion in one sentence, as it would be read by a person. */
  statement: string
  /** Node ids the claim is about (Species, Region, Habitat, Taxon). */
  subjectIds: string[]
  /** Source node ids. A claim with none cannot pass validation. */
  sourceIds: string[]
  /**
   * Scope narrows the claim so two claims that look contradictory can both be
   * true — e.g. different subpopulations or assessment years.
   */
  scope?: { regionId?: string; subpopulation?: string; period?: string }
  /** Present only on nodes whose status has been derived. Read-only output. */
  readonly derivedStatus?: ClaimStatus
}

export type SourceTier = 1 | 2 | 3

export interface SourceNode extends GraphNodeBase<"Source"> {
  url: string
  title: string
  /** 1 = primary literature / official assessment, 3 = general reference. */
  tier: SourceTier
  doi?: string
  /** ISO date the source itself was published or last assessed. */
  publishedAt?: string
  /** ISO date a contributor last checked the source resolves and still says this. */
  accessedAt?: string
  datasetId?: string
  /** Set when a newer edition or assessment replaces this source. */
  supersededBySourceId?: string
}

export interface DatasetNode extends GraphNodeBase<"Dataset"> {
  publisher: string
  url: string
  licenseId: string
  /** ISO date of the dataset snapshot this graph was built against. */
  snapshotAt?: string
  recordCount?: number
}

export interface MediaAssetNode extends GraphNodeBase<"MediaAsset"> {
  mediaType: "image" | "video" | "audio"
  url: string
  rightsId: string
  altText: string
  /** True when the asset is illustrative, not identification evidence. */
  conceptOnly: boolean
  depictsSpeciesId?: string
}

/** Licence identifiers accepted for public export. */
export type LicenseId =
  | "CC0-1.0"
  | "CC-BY-4.0"
  | "CC-BY-SA-4.0"
  | "CC-BY-NC-4.0"
  | "public-domain"
  | "all-rights-reserved"

export interface RightsNode extends GraphNodeBase<"Rights"> {
  licenseId: LicenseId
  licenseUrl?: string
  holder: string
  creditLine: string
  /** False for `all-rights-reserved` and unresolved permissions. */
  publicUseAllowed: boolean
  /** Named restrictions, e.g. "no derivative works", "editorial use only". */
  useLimitations?: string[]
  permissionEvidenceUrl?: string
}

export interface EthicsRuleNode extends GraphNodeBase<"EthicsRule"> {
  /** Machine-checkable rule identifier; the prose lives in ETHICS.md. */
  ruleId: string
  /** What the rule forbids, in one sentence. */
  prohibition: string
  appliesTo: NodeKind[]
  severity: "block" | "warn"
}

export type ReviewDimension = "science" | "ethics" | "editor"
export type ReviewVerdict = "approved" | "changes-requested" | "rejected"

export interface ReviewNode extends GraphNodeBase<"Review"> {
  dimension: ReviewDimension
  verdict: ReviewVerdict
  /** The node this review judged. */
  targetId: string
  /** The exact version reviewed. A later version voids the approval. */
  targetVersion: number
  reviewerId: string
  reviewedAt: string
  note?: string
}

export type ArtifactKind =
  | "species-page"
  | "region-briefing"
  | "field-mission"
  | "dataset-card"
  | "research-summary"

export interface ArtifactNode extends GraphNodeBase<"Artifact"> {
  artifactKind: ArtifactKind
  slug: string
  /** Claim ids the artifact publishes. */
  claimIds: string[]
  mediaAssetIds?: string[]
  licenseId: LicenseId
}

export interface ContributorNode extends GraphNodeBase<"Contributor"> {
  handle: string
  /** Institution, where the contributor chose to state one. */
  affiliation?: string
  /** Attribution is the currency of the commons; it is never optional. */
  attributionName: string
}

export type ContradictionState =
  /** Both claims stand and both read as disputed. */
  | "open"
  /** A Supersession retired one side; the survivor is no longer disputed. */
  | "resolved-by-supersession"
  /** The claims have different scopes and never actually conflicted. */
  | "resolved-by-scope"

export interface ContradictionNode extends GraphNodeBase<"Contradiction"> {
  /** Exactly two claim ids. Nothing is merged; both are kept. */
  claimIds: [string, string]
  state: ContradictionState
  /** Why these two cannot both be true as written. */
  rationale: string
  raisedBy: string
  raisedAt: string
  /** Set only when state is `resolved-by-supersession`. */
  supersessionId?: string
  /** Set only when state is `resolved-by-scope`. */
  scopeNote?: string
}

export interface SupersessionNode extends GraphNodeBase<"Supersession"> {
  /** The retired claim and the version at which it was retired. */
  fromClaimId: string
  fromClaimVersion: number
  /** The claim that replaces it. */
  toClaimId: string
  reason: string
  /** Supersession is an editorial act; it names the reviewer who made it. */
  decidedByReviewId: string
  decidedAt: string
}

export type GraphNode =
  | TaxonNode
  | SpeciesNode
  | RegionNode
  | HabitatNode
  | ObservationNode
  | ClaimNode
  | SourceNode
  | DatasetNode
  | MediaAssetNode
  | RightsNode
  | EthicsRuleNode
  | ReviewNode
  | ArtifactNode
  | ContributorNode
  | ContradictionNode
  | SupersessionNode

export interface CommonsGraph {
  schema: SchemaVersion
  /** ISO date the graph document was assembled. */
  generatedAt: string
  nodes: GraphNode[]
  edges: GraphEdge[]
}

/* ------------------------------------------------------------------ *
 * Derived outputs
 * ------------------------------------------------------------------ */

export interface ClaimStatusExplanation {
  claimId: string
  status: ClaimStatus
  /** The single rule that decided the status, named. */
  reason: string
  /** Every rule that fired, in precedence order, for auditability. */
  signals: string[]
  /** Days since the freshest supporting source was checked. */
  sourceAgeDays: number | null
  /** Freshness budget for the claim class, in days. */
  freshnessBudgetDays: number
  openContradictionIds: string[]
  approvedReviewIds: string[]
}

/**
 * Safe location projection. The public variant has no `coordinates` field at
 * all, so a caller cannot read coordinates off a public projection by mistake.
 */
export type LocationProjection =
  | {
      precision: "coordinates"
      coordinates: Coordinates
      regionId?: string
      generalizedTo: "none"
    }
  | {
      precision: "rounded"
      coordinates: Coordinates
      regionId?: string
      /** e.g. "0.1deg" */
      generalizedTo: string
    }
  | {
      precision: "region"
      regionId?: string
      regionLabel?: string
      generalizedTo: "region"
      /** Why the coordinates were withheld. */
      reason: string
    }
  | {
      precision: "withheld"
      generalizedTo: "withheld"
      reason: string
    }

export type ProjectionAudience = "public" | "steward"

/* ------------------------------------------------------------------ *
 * Contribution packets
 * ------------------------------------------------------------------ */

/**
 * A contribution packet is what a contributor (human or agent) submits before
 * opening a PR. It is a graph fragment plus the artifact it builds.
 */
export interface ContributionPacket {
  schema: SchemaVersion
  packetId: string
  submittedBy: string
  submittedAt: string
  nodes: GraphNode[]
  edges?: GraphEdge[]
}

export type CheckSeverity = "error" | "warning"

export interface PacketFinding {
  check: string
  severity: CheckSeverity
  nodeId?: string
  message: string
}

export interface PacketCheckResult {
  check: string
  passed: boolean
  /** Number of nodes the check examined. */
  examined: number
  findings: PacketFinding[]
}

export interface PacketReceipt {
  schema: SchemaVersion
  packetId: string
  validatedAt: string
  ok: boolean
  errorCount: number
  warningCount: number
  checks: PacketCheckResult[]
  claimStatuses: ClaimStatusExplanation[]
  /** The machine-readable export, present only when `ok` is true. */
  export?: CommonsGraph
}
