/**
 * Typed declaration for the CommonsGraph.v1 runtime.
 * Downstream consumers import values from `lib/commons-graph/index.mjs` and
 * types from `lib/commons-graph/types`.
 */

import type {
  ClaimStatusExplanation,
  CommonsGraph,
  ContributionPacket,
  EdgeKind,
  GraphEdge,
  GraphNode,
  LicenseId,
  LocationProjection,
  LocationSensitivity,
  NodeKind,
  ObservationNode,
  PacketFinding,
  PacketReceipt,
  ProjectionAudience,
  SchemaVersion,
  SourceNode,
  SpeciesNode,
  SupersessionNode,
  ContradictionNode,
  ClaimClass,
} from "./types"

export interface IndexedGraph {
  nodes: GraphNode[]
  edges: GraphEdge[]
  byId: Map<string, GraphNode>
  get(id: string): GraphNode | undefined
  ofKind<K extends NodeKind>(kind: K): Extract<GraphNode, { kind: K }>[]
  edgesFrom(id: string, kind?: EdgeKind): GraphEdge[]
  edgesTo(id: string, kind?: EdgeKind): GraphEdge[]
}

export declare const SCHEMA_VERSION: SchemaVersion
export declare const NODE_KINDS: readonly NodeKind[]
export declare const EDGE_KINDS: readonly EdgeKind[]

export declare function indexGraph(input: {
  nodes: GraphNode[]
  edges?: GraphEdge[]
}): IndexedGraph
export declare function checkStructure(graph: IndexedGraph): PacketFinding[]
export declare function supersessionChain(
  graph: IndexedGraph,
  claimId: string,
): { head: string; chain: string[]; cyclic: boolean }
export declare function isSuperseded(graph: IndexedGraph, claimId: string): boolean

export declare const FRESHNESS_BUDGET_DAYS: Readonly<Record<ClaimClass, number>>
export declare const DEFAULT_FRESHNESS_BUDGET_DAYS: number
export declare function freshnessBudgetDays(claimClass: ClaimClass): number
export declare function sourceEffectiveDate(source: SourceNode | undefined): number | null
export declare function deriveClaimStatus(
  graph: IndexedGraph,
  claimId: string,
  options?: { now?: number },
): ClaimStatusExplanation
export declare function deriveAllClaimStatuses(
  graph: IndexedGraph,
  options?: { now?: number },
): ClaimStatusExplanation[]
export declare function withDerivedStatus(
  graph: IndexedGraph,
  options?: { now?: number },
): GraphNode[]

export declare function contradictionsFor(
  graph: IndexedGraph,
  claimId: string,
): ContradictionNode[]
export declare function openContradictionsFor(
  graph: IndexedGraph,
  claimId: string,
): ContradictionNode[]
export declare function raiseContradiction(
  graph: IndexedGraph,
  input: {
    id: string
    claimIds: [string, string]
    rationale: string
    raisedBy: string
    raisedAt: string
    owner?: string
  },
): { node: ContradictionNode; edges: GraphEdge[] }
export declare function resolveBySupersession(
  contradiction: ContradictionNode,
  supersession: SupersessionNode,
): ContradictionNode
export declare function resolveByScope(
  graph: IndexedGraph,
  contradiction: ContradictionNode,
  scopeNote: string,
): ContradictionNode

export declare function sensitivityRank(sensitivity: LocationSensitivity | undefined): number
export declare function requiresRegionalGeneralization(species: SpeciesNode | undefined): boolean
export declare function projectLocation(
  graph: IndexedGraph,
  observation: ObservationNode,
  audience?: ProjectionAudience,
): LocationProjection
export declare function auditLocationLeaks(graph: IndexedGraph): PacketFinding[]
export declare function publicProjection(graph: IndexedGraph): {
  nodes: GraphNode[]
  edges: GraphEdge[]
}

export declare const PUBLIC_LICENSE_ALLOWLIST: readonly LicenseId[]
export declare const RESTRICTED_LICENSES: readonly LicenseId[]
export declare function validatePacket(
  packet: ContributionPacket,
  options?: { now?: number },
): PacketReceipt
export declare function formatReceipt(receipt: PacketReceipt): string

export type { CommonsGraph, ContributionPacket, PacketReceipt }
