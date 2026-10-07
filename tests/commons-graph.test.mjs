import { test } from "node:test"
import assert from "node:assert/strict"
import { readFileSync } from "node:fs"
import { fileURLToPath } from "node:url"

import {
  SCHEMA_VERSION,
  NODE_KINDS,
  indexGraph,
  supersessionChain,
  deriveClaimStatus,
  freshnessBudgetDays,
  raiseContradiction,
  resolveBySupersession,
  resolveByScope,
  projectLocation,
  publicProjection,
  validatePacket,
  formatReceipt,
} from "../lib/commons-graph/index.mjs"

const fixture = (name) =>
  JSON.parse(
    readFileSync(fileURLToPath(new URL(`../lib/commons-graph/fixtures/${name}`, import.meta.url)), "utf8"),
  )

const VALID = fixture("valid-packet.json")
const UNSOURCED = fixture("unsourced-claim-packet.json")
const PROTECTED = fixture("protected-location-packet.json")

/** Fixed clock so freshness assertions do not drift with the wall calendar. */
const NOW = Date.parse("2026-09-01T00:00:00Z")

const graphOf = (packet) => indexGraph({ nodes: packet.nodes, edges: packet.edges ?? [] })

test("the schema declares sixteen node types", () => {
  assert.equal(SCHEMA_VERSION, "CommonsGraph.v1")
  assert.equal(NODE_KINDS.length, 16)
  assert.equal(new Set(NODE_KINDS).size, 16)
})

test("the valid fixture passes every check and produces an export", () => {
  const receipt = validatePacket(VALID, { now: NOW })
  const failed = receipt.checks.filter((c) => !c.passed).map((c) => c.check)
  assert.deepEqual(failed, [], `unexpected failures: ${JSON.stringify(receipt.checks, null, 2)}`)
  assert.equal(receipt.ok, true)
  assert.equal(receipt.errorCount, 0)
  assert.ok(receipt.export, "a passing packet must produce a machine-readable export")
  assert.equal(receipt.export.schema, SCHEMA_VERSION)
  assert.ok(formatReceipt(receipt).includes("READY"))
})

test("an unsourced claim fails the citation check and blocks the export", () => {
  const receipt = validatePacket(UNSOURCED, { now: NOW })
  assert.equal(receipt.ok, false)
  const citation = receipt.checks.find((c) => c.check === "citation")
  assert.equal(citation.passed, false)
  assert.match(citation.findings[0].message, /no source/)
  assert.equal(receipt.export, undefined)
  assert.ok(formatReceipt(receipt).includes("BLOCKED"))
})

test("a protected-species coordinate leak fails and never reaches the export", () => {
  const receipt = validatePacket(PROTECTED, { now: NOW })
  assert.equal(receipt.ok, false)
  const location = receipt.checks.find((c) => c.check === "location-sensitivity")
  assert.equal(location.passed, false)
  assert.match(location.findings[0].message, /coordinates/)
  assert.equal(receipt.export, undefined)

  // The citation check is clean — this packet fails for exactly one reason.
  assert.equal(receipt.checks.find((c) => c.check === "citation").passed, true)
})

test("claim status is derived, and a hand-set status is rejected", () => {
  const graph = graphOf(VALID)
  const reviewed = deriveClaimStatus(graph, "claim-humpback-iucn-status", { now: NOW })
  assert.equal(reviewed.status, "reviewed")
  assert.deepEqual(reviewed.approvedReviewIds, ["review-humpback-status-science"])

  const unreviewed = deriveClaimStatus(graph, "claim-humpback-monterey-seasonality", { now: NOW })
  assert.equal(unreviewed.status, "inferred")
  assert.match(unreviewed.reason, /no approved review/)

  const tampered = structuredClone(VALID)
  const claim = tampered.nodes.find((n) => n.id === "claim-humpback-iucn-status")
  claim.derivedStatus = "reviewed"
  const receipt = validatePacket(tampered, { now: NOW })
  assert.equal(receipt.ok, false)
  const structure = receipt.checks.find((c) => c.check === "structure")
  assert.match(structure.findings.map((f) => f.message).join(" "), /derived and must not be set by hand/)
})

test("a review approves one version only; a later edit voids it", () => {
  const bumped = structuredClone(VALID)
  const claim = bumped.nodes.find((n) => n.id === "claim-humpback-iucn-status")
  claim.version = 2
  claim.statement = "Megaptera novaeangliae is assessed globally as Least Concern (edited)."

  const graph = graphOf(bumped)
  const status = deriveClaimStatus(graph, "claim-humpback-iucn-status", { now: NOW })
  assert.equal(status.status, "inferred")
  assert.ok(status.signals.some((s) => s.includes("void-by-version")))
})

test("citation freshness is class-specific and pushes an old claim to stale", () => {
  assert.ok(
    freshnessBudgetDays("population-estimate") < freshnessBudgetDays("morphology"),
    "abundance estimates must age faster than anatomy",
  )

  const aged = structuredClone(VALID)
  const source = aged.nodes.find((n) => n.id === "source-iucn-humpback-2018")
  source.accessedAt = "2015-01-01"
  source.publishedAt = "2014-01-01"

  const status = deriveClaimStatus(graphOf(aged), "claim-humpback-iucn-status", { now: NOW })
  assert.equal(status.status, "stale")
  assert.ok(status.sourceAgeDays > status.freshnessBudgetDays)
})

test("a superseded source stops counting toward freshness", () => {
  const replaced = structuredClone(VALID)
  const source = replaced.nodes.find((n) => n.id === "source-iucn-humpback-2018")
  source.supersededBySourceId = "source-iucn-humpback-2030"

  const status = deriveClaimStatus(graphOf(replaced), "claim-humpback-iucn-status", { now: NOW })
  assert.equal(status.status, "inferred")
  assert.match(status.reason, /accessed or published date/)
})

test("a contradiction keeps both claims and flips both to disputed", () => {
  const conflicted = structuredClone(VALID)
  const original = conflicted.nodes.find((n) => n.id === "claim-humpback-iucn-status")
  const rival = {
    ...structuredClone(original),
    id: "claim-humpback-iucn-status-rival",
    statement: "Megaptera novaeangliae is assessed globally as Vulnerable.",
    scope: { period: "2018 assessment" },
  }
  conflicted.nodes.push(rival)

  const graph = graphOf(conflicted)
  const { node, edges } = raiseContradiction(graph, {
    id: "contradiction-humpback-status",
    claimIds: ["claim-humpback-iucn-status", "claim-humpback-iucn-status-rival"],
    rationale: "Two different global categories are asserted for the same assessment year.",
    raisedBy: "contributor-jlind",
    raisedAt: "2026-08-25",
  })
  conflicted.nodes.push(node)
  conflicted.edges.push(...edges)

  const withConflict = graphOf(conflicted)
  for (const id of node.claimIds) {
    const status = deriveClaimStatus(withConflict, id, { now: NOW })
    assert.equal(status.status, "disputed", `${id} should read as disputed`)
  }
  // Neither claim was removed or merged.
  assert.ok(withConflict.get("claim-humpback-iucn-status"))
  assert.ok(withConflict.get("claim-humpback-iucn-status-rival"))

  // And an artifact may not publish a disputed claim as fact.
  const receipt = validatePacket(conflicted, { now: NOW })
  assert.equal(receipt.ok, false)
  assert.match(
    receipt.checks
      .find((c) => c.check === "review-state")
      .findings.map((f) => f.message)
      .join(" "),
    /disputed claim/,
  )
})

test("a scope resolution is refused when the two claims share a scope", () => {
  const graph = graphOf(VALID)
  const contradiction = {
    id: "contradiction-x",
    kind: "Contradiction",
    label: "x",
    claimIds: ["claim-humpback-iucn-status", "claim-humpback-iucn-status"],
    state: "open",
    rationale: "test",
    raisedBy: "contributor-jlind",
    raisedAt: "2026-08-25",
    owner: "contributor-jlind",
    provenance: { method: "authored", by: ["contributor-jlind"], at: "2026-08-25" },
    version: 1,
    visibility: "public",
    evaluation: { rule: "review-required" },
  }
  assert.throws(
    () => resolveByScope(graph, contradiction, "different subpopulations"),
    /same scope/,
  )
})

test("supersession requires a named reviewer decision and builds a chain", () => {
  const contradiction = {
    id: "contradiction-y",
    kind: "Contradiction",
    claimIds: ["claim-a", "claim-b"],
    state: "open",
    version: 1,
  }
  assert.throws(
    () =>
      resolveBySupersession(contradiction, {
        id: "supersession-1",
        fromClaimId: "claim-a",
        toClaimId: "claim-b",
      }),
    /reviewer decision/,
  )

  const resolved = resolveBySupersession(contradiction, {
    id: "supersession-1",
    fromClaimId: "claim-a",
    toClaimId: "claim-b",
    decidedByReviewId: "review-1",
  })
  assert.equal(resolved.state, "resolved-by-supersession")
  assert.equal(resolved.version, 2)

  const chained = structuredClone(VALID)
  const meta = {
    owner: "contributor-jlind",
    provenance: { method: "authored", by: ["contributor-jlind"], at: "2026-08-25" },
    version: 1,
    visibility: "public",
    evaluation: { rule: "review-required" },
  }
  chained.nodes.push({
    id: "claim-humpback-iucn-status-v2",
    kind: "Claim",
    label: "Humpback whale global conservation status, reassessed",
    claimClass: "conservation-status",
    statement: "Megaptera novaeangliae is assessed globally as Least Concern (2018, reconfirmed).",
    subjectIds: ["species-humpback-whale"],
    sourceIds: ["source-iucn-humpback-2018"],
    ...meta,
  })
  chained.nodes.push({
    id: "supersession-humpback-status",
    kind: "Supersession",
    label: "Humpback status claim superseded",
    fromClaimId: "claim-humpback-iucn-status",
    fromClaimVersion: 1,
    toClaimId: "claim-humpback-iucn-status-v2",
    reason: "Restated against the reconfirmed assessment.",
    decidedByReviewId: "review-humpback-status-science",
    decidedAt: "2026-08-25",
    ...meta,
  })

  const graph = graphOf(chained)
  const chain = supersessionChain(graph, "claim-humpback-iucn-status")
  assert.deepEqual(chain.chain, ["claim-humpback-iucn-status", "claim-humpback-iucn-status-v2"])
  assert.equal(chain.head, "claim-humpback-iucn-status-v2")
  assert.equal(chain.cyclic, false)
  // The retired claim is still in the graph.
  assert.ok(graph.get("claim-humpback-iucn-status"))
})

test("a supersession cycle is detected rather than looped", () => {
  const cyclic = structuredClone(VALID)
  const meta = {
    owner: "contributor-jlind",
    provenance: { method: "authored", by: ["contributor-jlind"], at: "2026-08-25" },
    version: 1,
    visibility: "public",
    evaluation: { rule: "review-required" },
  }
  cyclic.nodes.push(
    {
      id: "supersession-a",
      kind: "Supersession",
      label: "a",
      fromClaimId: "claim-humpback-iucn-status",
      fromClaimVersion: 1,
      toClaimId: "claim-humpback-monterey-seasonality",
      reason: "test",
      decidedByReviewId: "review-humpback-status-science",
      decidedAt: "2026-08-25",
      ...meta,
    },
    {
      id: "supersession-b",
      kind: "Supersession",
      label: "b",
      fromClaimId: "claim-humpback-monterey-seasonality",
      fromClaimVersion: 1,
      toClaimId: "claim-humpback-iucn-status",
      reason: "test",
      decidedByReviewId: "review-humpback-status-science",
      decidedAt: "2026-08-25",
      ...meta,
    },
  )
  const chain = supersessionChain(graphOf(cyclic), "claim-humpback-iucn-status")
  assert.equal(chain.cyclic, true)
})

test("public projection withholds coordinates for a protected species", () => {
  const graph = graphOf(PROTECTED)
  const observation = graph.get("observation-right-whale-fundy-2026")

  const publicView = projectLocation(graph, observation, "public")
  assert.equal(publicView.precision, "region")
  assert.equal("coordinates" in publicView, false, "a public projection must carry no coordinate field")
  assert.equal(publicView.regionId, "region-bay-of-fundy")

  const stewardView = projectLocation(graph, observation, "steward")
  assert.equal(stewardView.precision, "coordinates")
  assert.equal(stewardView.coordinates.lat, 44.8412)

  const projected = publicProjection(graph)
  const projectedObservation = projected.nodes.find((n) => n.id === observation.id)
  assert.equal(projectedObservation.coordinates, undefined)
})

test("an unknown sensitivity fails safe rather than publishing", () => {
  const unknown = structuredClone(PROTECTED)
  unknown.nodes.find((n) => n.id === "species-north-atlantic-right-whale").protection = {}
  const graph = graphOf(unknown)
  const projection = projectLocation(graph, graph.get("observation-right-whale-fundy-2026"), "public")
  assert.equal(projection.precision, "region")
})

test("low-sensitivity coordinates are coarsened, not published raw", () => {
  const low = structuredClone(VALID)
  low.nodes.find((n) => n.id === "species-humpback-whale").protection.locationSensitivity = "low"
  const graph = graphOf(low)
  const projection = projectLocation(graph, graph.get("observation-humpback-monterey-2026"), "public")
  assert.equal(projection.precision, "rounded")
  assert.equal(projection.coordinates.lat, 36.8)
  assert.equal(projection.generalizedTo, "0.1deg")
  assert.ok(projection.coordinates.uncertaintyMeters >= 11000)
})

test("generated media must be labelled concept-only", () => {
  const generated = structuredClone(VALID)
  const asset = generated.nodes.find((n) => n.id === "media-humpback-fluke")
  asset.provenance = { method: "inferred", by: ["contributor-mreyes"], at: "2026-08-20", rule: "image model" }
  const receipt = validatePacket(generated, { now: NOW })
  assert.equal(receipt.checks.find((c) => c.check === "ethics").passed, false)
})

test("an unpublishable licence blocks a public asset", () => {
  const restricted = structuredClone(VALID)
  restricted.nodes.find((n) => n.id === "rights-humpback-fluke-photo").licenseId = "all-rights-reserved"
  const receipt = validatePacket(restricted, { now: NOW })
  assert.equal(receipt.checks.find((c) => c.check === "license").passed, false)
})

test("a contributor cannot science-review their own claim", () => {
  const selfReviewed = structuredClone(VALID)
  selfReviewed.nodes.find((n) => n.id === "review-humpback-status-science").reviewerId =
    "contributor-mreyes"
  const receipt = validatePacket(selfReviewed, { now: NOW })
  assert.equal(receipt.checks.find((c) => c.check === "review-state").passed, false)
})

test("restricted nodes never reach the public projection", () => {
  const held = structuredClone(VALID)
  held.nodes.find((n) => n.id === "observation-humpback-monterey-2026").visibility = "restricted"
  const projected = publicProjection(graphOf(held))
  assert.equal(
    projected.nodes.some((n) => n.id === "observation-humpback-monterey-2026"),
    false,
  )
  assert.equal(
    projected.edges.some((e) => e.from === "observation-humpback-monterey-2026"),
    false,
    "edges to a withheld node must be dropped too",
  )
})

test("the MCP tool contract declares three read-only tools and no server", () => {
  const contract = JSON.parse(
    readFileSync(
      fileURLToPath(new URL("../lib/commons-graph/mcp/tool-contracts.v1.json", import.meta.url)),
      "utf8",
    ),
  )
  assert.equal(contract.graphSchema, SCHEMA_VERSION)
  assert.deepEqual(
    contract.tools.map((t) => t.name),
    ["query_species", "query_claims", "export_packet"],
  )
  for (const tool of contract.tools) {
    assert.equal(tool.readOnly, true)
    assert.ok(tool.inputSchema, `${tool.name} needs an input schema`)
    assert.ok(tool.outputSchema, `${tool.name} needs an output schema`)
  }
  assert.equal("endpoint" in contract, false, "the contract must not declare a server")
})
