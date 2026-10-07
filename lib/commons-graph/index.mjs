/**
 * CommonsGraph.v1 — public runtime surface.
 * Types live in `types.ts`; the declaration for this module is `index.d.mts`.
 */

export {
  SCHEMA_VERSION,
  NODE_KINDS,
  EDGE_KINDS,
  indexGraph,
  checkStructure,
  supersessionChain,
  isSuperseded,
} from "./graph.mjs"

export {
  FRESHNESS_BUDGET_DAYS,
  DEFAULT_FRESHNESS_BUDGET_DAYS,
  freshnessBudgetDays,
  sourceEffectiveDate,
  deriveClaimStatus,
  deriveAllClaimStatuses,
  withDerivedStatus,
} from "./status.mjs"

export {
  contradictionsFor,
  openContradictionsFor,
  raiseContradiction,
  resolveBySupersession,
  resolveByScope,
} from "./contradiction.mjs"

export {
  sensitivityRank,
  requiresRegionalGeneralization,
  projectLocation,
  auditLocationLeaks,
  publicProjection,
} from "./projection.mjs"

export {
  PUBLIC_LICENSE_ALLOWLIST,
  RESTRICTED_LICENSES,
  validatePacket,
  formatReceipt,
} from "./packet.mjs"
