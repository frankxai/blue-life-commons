/**
 * Contribution packet validation.
 *
 * A packet is what a contributor — person or agent — submits before opening a
 * PR. This validator is the workbench: it runs the same checks a reviewer would,
 * in a fixed order, and prints a receipt that says exactly what passed, what
 * failed, and what status every claim will carry once published.
 *
 * It refuses to produce a machine-readable export while any error stands.
 */

import { indexGraph, checkStructure, SCHEMA_VERSION } from "./graph.mjs"
import { deriveAllClaimStatuses } from "./status.mjs"
import {
  auditLocationLeaks,
  publicProjection,
  requiresRegionalGeneralization,
} from "./projection.mjs"

/** Licences a public commons artifact or asset may carry. */
export const PUBLIC_LICENSE_ALLOWLIST = Object.freeze([
  "CC0-1.0",
  "CC-BY-4.0",
  "CC-BY-SA-4.0",
  "public-domain",
])

/** Accepted but flagged: non-commercial blocks the reuse the commons exists for. */
export const RESTRICTED_LICENSES = Object.freeze(["CC-BY-NC-4.0"])

const CHECK_ORDER = [
  "schema",
  "structure",
  "citation",
  "license",
  "location-sensitivity",
  "review-state",
  "ethics",
  "attribution",
  "export",
]

const err = (check, nodeId, message) => ({ check, severity: "error", nodeId, message })
const warn = (check, nodeId, message) => ({ check, severity: "warning", nodeId, message })

/**
 * @param {object} packet ContributionPacket
 * @param {{ now?: number }} options
 * @returns PacketReceipt
 */
export function validatePacket(packet, { now = Date.now() } = {}) {
  const findings = []
  const examined = {}
  const record = (check, count) => {
    examined[check] = count
  }

  // 1. schema ------------------------------------------------------------
  if (packet?.schema !== SCHEMA_VERSION) {
    findings.push(
      err("schema", undefined, `packet schema must be '${SCHEMA_VERSION}', got '${packet?.schema}'`),
    )
  }
  for (const field of ["packetId", "submittedBy", "submittedAt"]) {
    if (!packet?.[field]) findings.push(err("schema", undefined, `packet is missing '${field}'`))
  }
  if (!Array.isArray(packet?.nodes) || packet.nodes.length === 0) {
    findings.push(err("schema", undefined, "packet carries no nodes"))
  }
  record("schema", Array.isArray(packet?.nodes) ? packet.nodes.length : 0)

  if (findings.some((f) => f.severity === "error")) {
    return assemble(packet, findings, examined, [], undefined, now)
  }

  let graph
  try {
    graph = indexGraph({ nodes: packet.nodes, edges: packet.edges ?? [] })
  } catch (error) {
    findings.push(err("structure", undefined, error.message))
    return assemble(packet, findings, examined, [], undefined, now)
  }

  // 2. structure ---------------------------------------------------------
  findings.push(...checkStructure(graph))
  record("structure", graph.nodes.length + graph.edges.length)

  // 3. citation ----------------------------------------------------------
  const claims = graph.ofKind("Claim")
  for (const claim of claims) {
    const sourceIds = claim.sourceIds ?? []
    if (sourceIds.length === 0) {
      findings.push(
        err("citation", claim.id, `claim has no source: "${truncate(claim.statement)}"`),
      )
      continue
    }
    for (const sourceId of sourceIds) {
      const source = graph.get(sourceId)
      if (!source || source.kind !== "Source") {
        findings.push(err("citation", claim.id, `cited source does not resolve: ${sourceId}`))
        continue
      }
      if (!source.url || !source.title) {
        findings.push(err("citation", source.id, "source needs both a url and a title"))
      }
      if (![1, 2, 3].includes(source.tier)) {
        findings.push(err("citation", source.id, "source tier must be 1, 2 or 3"))
      }
      if (!source.accessedAt && !source.publishedAt) {
        findings.push(
          err("citation", source.id, "source needs an accessedAt or publishedAt date to be checked for freshness"),
        )
      }
    }
  }
  record("citation", claims.length)

  // 4. license -----------------------------------------------------------
  const assets = graph.ofKind("MediaAsset")
  for (const artifact of graph.ofKind("Artifact")) {
    checkLicense(findings, artifact.id, artifact.licenseId, artifact.visibility)
  }
  for (const asset of assets) {
    const rights = graph.get(asset.rightsId)
    if (!rights || rights.kind !== "Rights") {
      findings.push(err("license", asset.id, `media asset has no Rights record (${asset.rightsId})`))
      continue
    }
    checkLicense(findings, asset.id, rights.licenseId, asset.visibility)
    if (asset.visibility === "public" && rights.publicUseAllowed !== true) {
      findings.push(
        err("license", asset.id, "asset is public but its Rights record does not allow public use"),
      )
    }
    if (!rights.creditLine || !rights.holder) {
      findings.push(err("license", rights.id, "Rights record needs a holder and a credit line"))
    }
    if (!asset.altText) {
      findings.push(err("license", asset.id, "media asset needs alt text"))
    }
  }
  record("license", graph.ofKind("Artifact").length + assets.length)

  // 5. location sensitivity ---------------------------------------------
  findings.push(...auditLocationLeaks(graph))
  record("location-sensitivity", graph.ofKind("Observation").length)

  // 6. review state ------------------------------------------------------
  const reviews = graph.ofKind("Review")
  for (const review of reviews) {
    const target = graph.get(review.targetId)
    if (!target) {
      findings.push(err("review-state", review.id, `review target does not resolve: ${review.targetId}`))
      continue
    }
    if (review.targetVersion !== target.version) {
      findings.push(
        warn(
          "review-state",
          review.id,
          `review approves v${review.targetVersion} but ${target.id} is now v${target.version}; the approval no longer counts`,
        ),
      )
    }
    if (review.reviewerId === target.owner && review.dimension === "science") {
      findings.push(
        err("review-state", review.id, "a contributor cannot science-review their own node"),
      )
    }
  }
  const statuses = deriveAllClaimStatuses(graph, { now })
  const statusById = new Map(statuses.map((s) => [s.claimId, s]))
  for (const artifact of graph.ofKind("Artifact")) {
    for (const claimId of artifact.claimIds ?? []) {
      const status = statusById.get(claimId)
      if (!status) {
        findings.push(err("review-state", artifact.id, `artifact publishes unknown claim ${claimId}`))
        continue
      }
      if (status.status === "disputed") {
        findings.push(
          err(
            "review-state",
            artifact.id,
            `artifact publishes disputed claim ${claimId}; both sides must be shown as disputed, not published as fact`,
          ),
        )
      }
      if (status.status === "stale" || status.status === "inferred") {
        findings.push(
          warn(
            "review-state",
            artifact.id,
            `claim ${claimId} will publish as '${status.status}' (${status.reason}) and must be labelled as such`,
          ),
        )
      }
    }
  }
  record("review-state", reviews.length + claims.length)

  // 7. ethics ------------------------------------------------------------
  for (const asset of assets) {
    if (asset.provenance?.method === "inferred" && asset.conceptOnly !== true) {
      findings.push(
        err(
          "ethics",
          asset.id,
          "generated media must be marked conceptOnly; it is never identification or conservation evidence",
        ),
      )
    }
  }
  const blockingRules = graph.ofKind("EthicsRule").filter((r) => r.severity === "block")
  for (const rule of blockingRules) {
    const constrained = graph
      .edgesFrom(rule.id, "constrains")
      .map((e) => e.to)
      .filter((id) => graph.byId.has(id))
    for (const targetId of constrained) {
      const approved = reviews.some(
        (r) => r.dimension === "ethics" && r.verdict === "approved" && r.targetId === targetId,
      )
      if (!approved) {
        findings.push(
          err(
            "ethics",
            targetId,
            `blocked by ethics rule ${rule.ruleId} (${rule.prohibition}); an approved ethics review is required`,
          ),
        )
      }
    }
  }
  record("ethics", assets.length + blockingRules.length)

  // 8. attribution -------------------------------------------------------
  const contributors = new Set(graph.ofKind("Contributor").map((c) => c.id))
  for (const contributor of graph.ofKind("Contributor")) {
    if (!contributor.attributionName) {
      findings.push(err("attribution", contributor.id, "contributor needs an attribution name"))
    }
  }
  for (const node of graph.nodes) {
    if (node.kind === "Contributor") continue
    for (const id of node.provenance?.by ?? []) {
      if (id.startsWith("contributor-") && !contributors.has(id)) {
        findings.push(
          err("attribution", node.id, `provenance names a contributor not present in the packet: ${id}`),
        )
      }
    }
  }
  for (const artifact of graph.ofKind("Artifact")) {
    const credited = graph.edgesTo(artifact.id, "contributed")
    if (credited.length === 0) {
      findings.push(err("attribution", artifact.id, "artifact has no credited contributor"))
    }
  }
  record("attribution", contributors.size + graph.ofKind("Artifact").length)

  // 9. export ------------------------------------------------------------
  let exported
  const hasError = findings.some((f) => f.severity === "error")
  if (!hasError) {
    const projected = publicProjection(graph)
    exported = {
      schema: SCHEMA_VERSION,
      generatedAt: new Date(now).toISOString(),
      nodes: projected.nodes,
      edges: projected.edges,
    }
    const leaked = exported.nodes.filter(
      (n) =>
        n.kind === "Observation" &&
        n.coordinates &&
        requiresRegionalGeneralization(graph.get(n.speciesId)),
    )
    for (const node of leaked) {
      findings.push(err("export", node.id, "public export still carries protected coordinates"))
    }
    if (findings.some((f) => f.check === "export" && f.severity === "error")) exported = undefined
  }
  record("export", graph.nodes.length)

  return assemble(packet, findings, examined, statuses, exported, now)
}

function checkLicense(findings, nodeId, licenseId, visibility) {
  if (!licenseId) {
    findings.push(err("license", nodeId, "no licence declared"))
    return
  }
  if (PUBLIC_LICENSE_ALLOWLIST.includes(licenseId)) return
  if (RESTRICTED_LICENSES.includes(licenseId)) {
    findings.push(
      warn("license", nodeId, `licence '${licenseId}' blocks commercial reuse and limits the commons`),
    )
    return
  }
  if (visibility === "public") {
    findings.push(
      err("license", nodeId, `licence '${licenseId}' is not publishable; allowed: ${PUBLIC_LICENSE_ALLOWLIST.join(", ")}`),
    )
  }
}

function truncate(text = "", max = 60) {
  return text.length > max ? `${text.slice(0, max - 1)}…` : text
}

function assemble(packet, findings, examined, claimStatuses, exported, now) {
  const checks = CHECK_ORDER.map((check) => {
    const own = findings.filter((f) => f.check === check)
    return {
      check,
      passed: !own.some((f) => f.severity === "error"),
      examined: examined[check] ?? 0,
      findings: own,
    }
  })
  const errorCount = findings.filter((f) => f.severity === "error").length
  const warningCount = findings.filter((f) => f.severity === "warning").length
  return {
    schema: SCHEMA_VERSION,
    packetId: packet?.packetId ?? "(unknown)",
    validatedAt: new Date(now).toISOString(),
    ok: errorCount === 0,
    errorCount,
    warningCount,
    checks,
    claimStatuses,
    ...(exported ? { export: exported } : {}),
  }
}

/** Render a receipt as plain text for the CLI. */
export function formatReceipt(receipt) {
  const lines = []
  const rule = "─".repeat(72)
  lines.push(rule)
  lines.push(`Blue Life Commons — contribution packet receipt`)
  lines.push(`packet    ${receipt.packetId}`)
  lines.push(`schema    ${receipt.schema}`)
  lines.push(`validated ${receipt.validatedAt}`)
  lines.push(rule)

  for (const check of receipt.checks) {
    const hasWarnings = check.findings.some((f) => f.severity === "warning")
    const mark = !check.passed ? "FAIL" : hasWarnings ? "warn" : "pass"
    lines.push(`${mark.padEnd(5)} ${check.check.padEnd(21)} ${check.examined} examined`)
    for (const finding of check.findings) {
      const tag = finding.severity === "error" ? "error" : "warn "
      lines.push(`      ${tag}  ${finding.nodeId ? `${finding.nodeId}: ` : ""}${finding.message}`)
    }
  }

  if (receipt.claimStatuses.length > 0) {
    lines.push(rule)
    lines.push("Derived claim status (never hand-set)")
    for (const status of receipt.claimStatuses) {
      lines.push(`  ${status.status.padEnd(9)} ${status.claimId}`)
      lines.push(`            ${status.reason}`)
    }
  }

  const count = (n, word) => `${n} ${word}${n === 1 ? "" : "s"}`
  const tally = `${count(receipt.errorCount, "error")}, ${count(receipt.warningCount, "warning")}`
  lines.push(rule)
  lines.push(
    receipt.ok
      ? `READY — ${tally}. Machine-readable export produced.`
      : `BLOCKED — ${tally}. No export produced.`,
  )
  lines.push(rule)
  return lines.join("\n")
}
