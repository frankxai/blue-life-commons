/**
 * Safe species-location projection.
 *
 * Publishing a precise coordinate for a poached, disturbed or nested species is
 * the one mistake in this commons that cannot be taken back. The rule follows
 * the GBIF generalization model: sensitivity decides precision, and for
 * anything at `medium` or above the public projection carries no coordinate
 * field at all — a caller cannot read one off by accident.
 *
 * Rounding is deliberately not used above `low`. Coarsening a coordinate to
 * 0.1 degrees still puts a reader inside an 11 km box, which is a search area.
 */

const SENSITIVITY_ORDER = ["public", "low", "medium", "high", "extreme"]

export function sensitivityRank(sensitivity) {
  const i = SENSITIVITY_ORDER.indexOf(sensitivity)
  return i === -1 ? SENSITIVITY_ORDER.indexOf("high") : i // unknown fails safe
}

/** True when a species' locations must never be published as coordinates. */
export function requiresRegionalGeneralization(species) {
  return sensitivityRank(species?.protection?.locationSensitivity) >= 2
}

function round(value, decimals) {
  const f = 10 ** decimals
  return Math.round(value * f) / f
}

/**
 * Project an observation's location for an audience.
 *
 * @param {object} graph indexed graph
 * @param {object} observation Observation node
 * @param {"public"|"steward"} audience
 * @returns LocationProjection
 */
export function projectLocation(graph, observation, audience = "public") {
  const species = graph.get(observation.speciesId)
  const sensitivity = species?.protection?.locationSensitivity
  const rank = sensitivityRank(sensitivity)
  const regionId = observation.regionId
  const regionLabel = regionId ? graph.get(regionId)?.label : undefined

  if (audience === "steward") {
    if (!observation.coordinates) {
      return {
        precision: "region",
        regionId,
        regionLabel,
        generalizedTo: "region",
        reason: "the source record carried no coordinates",
      }
    }
    return {
      precision: "coordinates",
      coordinates: observation.coordinates,
      regionId,
      generalizedTo: "none",
    }
  }

  if (rank >= 2) {
    if (!regionId) {
      return {
        precision: "withheld",
        generalizedTo: "withheld",
        reason: `location sensitivity '${sensitivity ?? "unknown"}' and no region to generalize to`,
      }
    }
    return {
      precision: "region",
      regionId,
      regionLabel,
      generalizedTo: "region",
      reason: `location sensitivity '${sensitivity ?? "unknown"}': coordinates are withheld from public export`,
    }
  }

  if (!observation.coordinates) {
    return {
      precision: "region",
      regionId,
      regionLabel,
      generalizedTo: "region",
      reason: "the source record carried no coordinates",
    }
  }

  if (rank === 1) {
    return {
      precision: "rounded",
      coordinates: {
        lat: round(observation.coordinates.lat, 1),
        lon: round(observation.coordinates.lon, 1),
        uncertaintyMeters: Math.max(observation.coordinates.uncertaintyMeters ?? 0, 11000),
      },
      regionId,
      generalizedTo: "0.1deg",
    }
  }

  return {
    precision: "coordinates",
    coordinates: observation.coordinates,
    regionId,
    generalizedTo: "none",
  }
}

/**
 * Audit a graph for observations whose raw coordinates would leak through a
 * public export. Returns a finding per offending observation.
 */
export function auditLocationLeaks(graph) {
  const findings = []
  for (const observation of graph.ofKind("Observation")) {
    if (!observation.coordinates) continue
    const species = graph.get(observation.speciesId)
    if (!species || species.kind !== "Species") {
      findings.push({
        check: "location-sensitivity",
        severity: "error",
        nodeId: observation.id,
        message: `observation references unknown species '${observation.speciesId}'; sensitivity cannot be checked`,
      })
      continue
    }
    if (requiresRegionalGeneralization(species) && observation.visibility === "public") {
      findings.push({
        check: "location-sensitivity",
        severity: "error",
        nodeId: observation.id,
        message: `public observation carries coordinates for '${species.scientificName}' at sensitivity '${species.protection.locationSensitivity}'; set visibility to 'restricted' or drop the coordinates`,
      })
    }
  }
  return findings
}

/**
 * Strip everything a public reader must not receive. Restricted and embargoed
 * nodes are dropped whole; public observations of sensitive species keep their
 * region and lose their coordinates.
 */
export function publicProjection(graph) {
  const kept = []
  for (const node of graph.nodes) {
    if (node.visibility !== "public") continue
    if (node.kind === "Observation") {
      const projection = projectLocation(graph, node, "public")
      const { coordinates, ...rest } = node
      kept.push(
        projection.precision === "coordinates" || projection.precision === "rounded"
          ? { ...rest, coordinates: projection.coordinates, locationProjection: projection }
          : { ...rest, locationProjection: projection },
      )
      continue
    }
    kept.push(node)
  }
  const keptIds = new Set(kept.map((n) => n.id))
  const edges = graph.edges.filter(
    (e) => e.visibility === "public" && keptIds.has(e.from) && keptIds.has(e.to),
  )
  return { nodes: kept, edges }
}
