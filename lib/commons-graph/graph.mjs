/**
 * CommonsGraph.v1 — indexing and structural integrity.
 *
 * Runtime lives in .mjs so the CLI and `node --test` can import it directly
 * with no build step. The typed surface is `types.ts` + `index.d.mts`.
 */

export const SCHEMA_VERSION = "CommonsGraph.v1"

export const NODE_KINDS = Object.freeze([
  "Taxon",
  "Species",
  "Region",
  "Habitat",
  "Observation",
  "Claim",
  "Source",
  "Dataset",
  "MediaAsset",
  "Rights",
  "EthicsRule",
  "Review",
  "Artifact",
  "Contributor",
  "Contradiction",
  "Supersession",
])

export const EDGE_KINDS = Object.freeze([
  "cites",
  "about",
  "reviews",
  "contradicts",
  "supersedes",
  "observed",
  "drawnFrom",
  "licensedUnder",
  "constrains",
  "composes",
  "contributed",
  "partOf",
])

const REQUIRED_META = ["owner", "provenance", "version", "visibility", "evaluation"]

/** Index a node list into a graph view with typed accessors. */
export function indexGraph({ nodes = [], edges = [] } = {}) {
  const byId = new Map()
  const byKind = new Map()
  for (const kind of NODE_KINDS) byKind.set(kind, [])

  for (const node of nodes) {
    if (byId.has(node.id)) {
      throw new Error(`duplicate node id: ${node.id}`)
    }
    byId.set(node.id, node)
    const bucket = byKind.get(node.kind)
    if (!bucket) throw new Error(`unknown node kind: ${node.kind} (${node.id})`)
    bucket.push(node)
  }

  return {
    nodes,
    edges,
    byId,
    get: (id) => byId.get(id),
    ofKind: (kind) => byKind.get(kind) ?? [],
    edgesFrom: (id, kind) =>
      edges.filter((e) => e.from === id && (!kind || e.kind === kind)),
    edgesTo: (id, kind) =>
      edges.filter((e) => e.to === id && (!kind || e.kind === kind)),
  }
}

/**
 * Structural checks every node and edge must pass: the five universal metadata
 * fields, a known kind, an integer version, and resolvable edge endpoints.
 */
export function checkStructure(graph) {
  const findings = []
  const push = (nodeId, message) =>
    findings.push({ check: "structure", severity: "error", nodeId, message })

  for (const node of graph.nodes) {
    if (!node.id) push(undefined, "node is missing an id")
    if (!NODE_KINDS.includes(node.kind)) push(node.id, `unknown node kind ${node.kind}`)
    for (const field of REQUIRED_META) {
      if (node[field] === undefined || node[field] === null) {
        push(node.id, `missing required metadata field '${field}'`)
      }
    }
    if (!Number.isInteger(node.version) || node.version < 1) {
      push(node.id, "version must be an integer >= 1")
    }
    if (node.provenance && !node.provenance.method) {
      push(node.id, "provenance.method is required")
    }
    if (node.provenance && !Array.isArray(node.provenance.by)) {
      push(node.id, "provenance.by must be a list of contributor ids")
    }
    if (node.evaluation && !node.evaluation.rule) {
      push(node.id, "evaluation.rule is required")
    }
    if (node.kind === "Claim" && "derivedStatus" in node) {
      push(node.id, "claim status is derived and must not be set by hand")
    }
  }

  for (const edge of graph.edges) {
    if (!EDGE_KINDS.includes(edge.kind)) {
      push(edge.id, `unknown edge kind ${edge.kind}`)
    }
    if (!graph.byId.has(edge.from)) push(edge.id, `edge 'from' does not resolve: ${edge.from}`)
    if (!graph.byId.has(edge.to)) push(edge.id, `edge 'to' does not resolve: ${edge.to}`)
    for (const field of REQUIRED_META) {
      if (edge[field] === undefined || edge[field] === null) {
        findings.push({
          check: "structure",
          severity: "error",
          nodeId: edge.id,
          message: `edge missing required metadata field '${field}'`,
        })
      }
    }
  }

  return findings
}

/**
 * Walk the supersession chain from a claim to its head.
 * Returns { head, chain, cyclic }. Nothing is deleted along the way; the chain
 * is the audit trail of what replaced what.
 */
export function supersessionChain(graph, claimId) {
  const chain = [claimId]
  const seen = new Set([claimId])
  let current = claimId
  let cyclic = false

  for (;;) {
    const next = graph
      .ofKind("Supersession")
      .find((s) => s.fromClaimId === current)
    if (!next) break
    if (seen.has(next.toClaimId)) {
      cyclic = true
      break
    }
    seen.add(next.toClaimId)
    chain.push(next.toClaimId)
    current = next.toClaimId
  }

  return { head: current, chain, cyclic }
}

/** True when a newer claim has superseded this one. */
export function isSuperseded(graph, claimId) {
  return graph.ofKind("Supersession").some((s) => s.fromClaimId === claimId)
}
