/**
 * Derived claim status.
 *
 * `status` is never written by a contributor. It is computed from Review,
 * Contradiction and source-freshness records every time the graph is read, so
 * a claim cannot be talked into looking reviewed.
 *
 * Precedence, highest first:
 *   1. disputed — an open Contradiction touches the claim.
 *   2. inferred — no resolvable citation.
 *   3. stale    — the freshest supporting source is older than the claim
 *                 class's freshness budget.
 *   4. reviewed — an approved science Review exists for the current version.
 *   5. inferred — everything else: asserted, but not review-established.
 */

import { supersessionChain } from "./graph.mjs"

const DAY_MS = 24 * 60 * 60 * 1000

/**
 * Citation freshness budgets, in days, by claim class. A morphology claim ages
 * slowly; a population estimate does not. Chosen to track how often the
 * underlying record is actually reissued, not how often we would like to check.
 */
export const FRESHNESS_BUDGET_DAYS = Object.freeze({
  taxonomy: 1825, // 5y — nomenclatural revisions are infrequent but real
  morphology: 3650, // 10y
  behavior: 3650, // 10y
  distribution: 1825, // 5y
  "population-estimate": 1095, // 3y — abundance estimates go stale fast
  "conservation-status": 1825, // 5y — IUCN reassessment cadence
  regulation: 730, // 2y — listings and protections change with policy
  threat: 1095, // 3y
  other: 1825,
})

export const DEFAULT_FRESHNESS_BUDGET_DAYS = 1825

export function freshnessBudgetDays(claimClass) {
  return FRESHNESS_BUDGET_DAYS[claimClass] ?? DEFAULT_FRESHNESS_BUDGET_DAYS
}

/**
 * The date a source last stood up to a check. `accessedAt` beats `publishedAt`:
 * a 1990 paper someone verified last month is a live citation; a 2024 page
 * nobody has opened since is not.
 */
export function sourceEffectiveDate(source) {
  if (!source) return null
  if (source.supersededBySourceId) return null // a replaced edition is not fresh
  const raw = source.accessedAt ?? source.publishedAt
  if (!raw) return null
  const ms = Date.parse(raw)
  return Number.isNaN(ms) ? null : ms
}

export function daysSince(ms, now) {
  if (ms === null) return null
  return Math.floor((now - ms) / DAY_MS)
}

/**
 * Derive one claim's status.
 * @returns ClaimStatusExplanation
 */
export function deriveClaimStatus(graph, claimId, { now = Date.now() } = {}) {
  const claim = graph.get(claimId)
  if (!claim || claim.kind !== "Claim") {
    throw new Error(`not a claim: ${claimId}`)
  }

  const signals = []
  const budget = freshnessBudgetDays(claim.claimClass)

  if (claim.provenance?.method === "inferred") {
    signals.push("provenance:inferred")
  }

  const openContradictions = graph
    .ofKind("Contradiction")
    .filter((c) => c.state === "open" && c.claimIds.includes(claimId))
  const openContradictionIds = openContradictions.map((c) => c.id)
  if (openContradictionIds.length > 0) {
    signals.push(`contradiction:open x${openContradictionIds.length}`)
  }

  const sources = (claim.sourceIds ?? [])
    .map((id) => graph.get(id))
    .filter((s) => s && s.kind === "Source")
  const dated = sources.map(sourceEffectiveDate).filter((ms) => ms !== null)
  const freshestMs = dated.length > 0 ? Math.max(...dated) : null
  const sourceAgeDays = daysSince(freshestMs, now)

  const approvedReviews = graph
    .ofKind("Review")
    .filter(
      (r) =>
        r.targetId === claimId &&
        r.verdict === "approved" &&
        r.targetVersion === claim.version,
    )
  const approvedReviewIds = approvedReviews.map((r) => r.id)

  const staleReviews = graph
    .ofKind("Review")
    .filter(
      (r) =>
        r.targetId === claimId &&
        r.verdict === "approved" &&
        r.targetVersion !== claim.version,
    )
  if (staleReviews.length > 0) {
    signals.push(
      `review:void-by-version (reviewed v${staleReviews[0].targetVersion}, claim is v${claim.version})`,
    )
  }

  const { chain } = supersessionChain(graph, claimId)
  if (chain.length > 1) signals.push(`superseded-by:${chain[chain.length - 1]}`)

  let status
  let reason

  if (openContradictionIds.length > 0) {
    status = "disputed"
    reason = `open contradiction ${openContradictionIds.join(", ")}`
  } else if (sources.length === 0 || freshestMs === null) {
    status = "inferred"
    reason =
      sources.length === 0
        ? "no resolvable citation"
        : "no source carries an accessed or published date"
    signals.push("citation:missing-or-undated")
  } else if (sourceAgeDays > budget) {
    status = "stale"
    reason = `freshest source checked ${sourceAgeDays}d ago, budget ${budget}d`
    signals.push(`freshness:over-budget ${sourceAgeDays}/${budget}d`)
  } else if (approvedReviewIds.length > 0) {
    status = "reviewed"
    reason = `approved science review at v${claim.version}`
    signals.push(`review:approved ${approvedReviewIds.join(", ")}`)
  } else {
    status = "inferred"
    reason = "cited and fresh, but no approved review at the current version"
    signals.push("review:absent")
  }

  return {
    claimId,
    status,
    reason,
    signals,
    sourceAgeDays,
    freshnessBudgetDays: budget,
    openContradictionIds,
    approvedReviewIds,
  }
}

/** Derive statuses for every claim in the graph, in node order. */
export function deriveAllClaimStatuses(graph, options = {}) {
  return graph.ofKind("Claim").map((c) => deriveClaimStatus(graph, c.id, options))
}

/**
 * Attach derived status to claims for read-side consumers. Returns new objects;
 * the input graph is never mutated, so a hand-set status can never survive.
 */
export function withDerivedStatus(graph, options = {}) {
  const statuses = new Map(
    deriveAllClaimStatuses(graph, options).map((s) => [s.claimId, s]),
  )
  return graph.nodes.map((node) =>
    node.kind === "Claim"
      ? { ...node, derivedStatus: statuses.get(node.id)?.status }
      : node,
  )
}
