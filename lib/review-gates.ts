import type { Artifact } from "./types"

export function isReviewComplete(
  artifact: Pick<Artifact, "status">,
): boolean {
  return artifact.status === "approved" || artifact.status === "published"
}

export function isMissionOperationallyPublishable(
  artifact: Pick<Artifact, "type" | "status" | "review">,
): boolean {
  return (
    artifact.type === "field-mission" &&
    isReviewComplete(artifact) &&
    artifact.review?.ethics === "approved"
  )
}
