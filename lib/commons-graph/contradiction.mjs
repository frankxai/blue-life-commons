/**
 * Contradiction handling.
 *
 * The commons never auto-merges two conflicting claims and never silently
 * drops one. Both are kept, both flip to `disputed`, and the disagreement
 * becomes a first-class node a reader can see. A contradiction leaves the open
 * state only by an editorial act: a Supersession decided by a named reviewer,
 * or a finding that the two claims had different scopes all along.
 */

/** Contradictions touching a claim, in any state. */
export function contradictionsFor(graph, claimId) {
  return graph.ofKind("Contradiction").filter((c) => c.claimIds.includes(claimId))
}

export function openContradictionsFor(graph, claimId) {
  return contradictionsFor(graph, claimId).filter((c) => c.state === "open")
}

/**
 * Build an open Contradiction node plus its two `contradicts` edges.
 * Pure: returns nodes and edges to add, and never mutates the graph.
 */
export function raiseContradiction(
  graph,
  { id, claimIds, rationale, raisedBy, raisedAt, owner = raisedBy },
) {
  if (!Array.isArray(claimIds) || claimIds.length !== 2) {
    throw new Error("a contradiction holds exactly two claims")
  }
  if (claimIds[0] === claimIds[1]) {
    throw new Error("a claim cannot contradict itself")
  }
  for (const claimId of claimIds) {
    const node = graph.get(claimId)
    if (!node || node.kind !== "Claim") {
      throw new Error(`not a claim: ${claimId}`)
    }
  }
  if (!rationale) throw new Error("a contradiction must say why both cannot be true")

  const meta = {
    owner,
    provenance: { method: "authored", by: [raisedBy], at: raisedAt },
    version: 1,
    visibility: "public",
    evaluation: { rule: "review-required" },
  }

  const node = {
    id,
    kind: "Contradiction",
    label: `Contradiction: ${claimIds[0]} vs ${claimIds[1]}`,
    claimIds: [claimIds[0], claimIds[1]],
    state: "open",
    rationale,
    raisedBy,
    raisedAt,
    ...meta,
  }

  const edges = claimIds.map((claimId, i) => ({
    id: `${id}-edge-${i + 1}`,
    kind: "contradicts",
    from: id,
    to: claimId,
    ...meta,
  }))

  return { node, edges }
}

/**
 * Resolve by supersession: one claim version is retired in favour of another.
 * Both claims remain in the graph; the retired one keeps its history and its
 * place in the chain. Returns the updated Contradiction node.
 */
export function resolveBySupersession(contradiction, supersession) {
  if (contradiction.state !== "open") {
    throw new Error(`contradiction ${contradiction.id} is already resolved`)
  }
  if (!contradiction.claimIds.includes(supersession.fromClaimId)) {
    throw new Error("the supersession does not retire either contradicting claim")
  }
  if (!supersession.decidedByReviewId) {
    throw new Error("supersession requires a reviewer decision; it is not automatic")
  }
  return {
    ...contradiction,
    state: "resolved-by-supersession",
    supersessionId: supersession.id,
    version: contradiction.version + 1,
  }
}

/**
 * Resolve by scope: the two claims were never in conflict because they describe
 * different subpopulations, regions or periods. Requires that the scopes
 * actually differ — otherwise this would be a way to wish a conflict away.
 */
export function resolveByScope(graph, contradiction, scopeNote) {
  if (contradiction.state !== "open") {
    throw new Error(`contradiction ${contradiction.id} is already resolved`)
  }
  const [a, b] = contradiction.claimIds.map((id) => graph.get(id))
  if (scopesEqual(a?.scope, b?.scope)) {
    throw new Error(
      "both claims share the same scope; a scope resolution would hide a real conflict",
    )
  }
  if (!scopeNote) throw new Error("a scope resolution must state the distinction")
  return {
    ...contradiction,
    state: "resolved-by-scope",
    scopeNote,
    version: contradiction.version + 1,
  }
}

function scopesEqual(a = {}, b = {}) {
  const norm = (s) =>
    JSON.stringify({
      regionId: s?.regionId ?? null,
      subpopulation: s?.subpopulation ?? null,
      period: s?.period ?? null,
    })
  return norm(a) === norm(b)
}
