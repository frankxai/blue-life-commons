/**
 * Binds the runtime declaration (`index.d.mts`) to the schema types
 * (`types.ts`) so `tsc --noEmit` actually checks that the two agree. Without a
 * .ts file importing the runtime, the declaration would never be typechecked.
 *
 * This file asserts shapes only. It has no runtime behaviour.
 */

import {
  deriveClaimStatus,
  indexGraph,
  projectLocation,
  validatePacket,
} from "./index.mjs"
import type {
  ClaimStatus,
  ClaimStatusExplanation,
  CommonsGraph,
  ContributionPacket,
  LocationProjection,
  PacketReceipt,
  RegionNode,
  RightsNode,
  SpeciesNode,
} from "./types"

/** Consumed by Ocean Intelligence. Renaming any of these needs a new schema version. */
export type { RegionNode, RightsNode, SpeciesNode }

type AssertAssignable<Expected, Actual extends Expected> = Actual

export type _StatusIsExplanation = AssertAssignable<
  ClaimStatusExplanation,
  ReturnType<typeof deriveClaimStatus>
>
export type _ReceiptIsReceipt = AssertAssignable<
  PacketReceipt,
  ReturnType<typeof validatePacket>
>
export type _ProjectionIsProjection = AssertAssignable<
  LocationProjection,
  ReturnType<typeof projectLocation>
>

/** Status is a closed set; adding a value is a breaking schema change. */
export const CLAIM_STATUSES: readonly ClaimStatus[] = [
  "reviewed",
  "disputed",
  "stale",
  "inferred",
]

export function readPacket(packet: ContributionPacket): PacketReceipt {
  return validatePacket(packet)
}

export function readGraph(graph: CommonsGraph): ClaimStatusExplanation[] {
  const indexed = indexGraph({ nodes: graph.nodes, edges: graph.edges })
  return indexed.ofKind("Claim").map((claim) => deriveClaimStatus(indexed, claim.id))
}
