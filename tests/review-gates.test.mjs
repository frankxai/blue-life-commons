import test from "node:test";
import assert from "node:assert/strict";
import { isReviewComplete, isMissionOperationallyPublishable } from "../lib/review-gates.ts";

test("isReviewComplete returns true for approved and published statuses", () => {
  assert.equal(isReviewComplete({ status: "approved" }), true);
  assert.equal(isReviewComplete({ status: "published" }), true);
});

test("isReviewComplete returns false for other statuses", () => {
  assert.equal(isReviewComplete({ status: "draft" }), false);
  assert.equal(isReviewComplete({ status: "needs-expert-review" }), false);
  assert.equal(isReviewComplete({}), false);
});

test("isMissionOperationallyPublishable checks for field-mission type, review completion, and science/ethics approvals", () => {
  const artifact = {
    type: "field-mission",
    status: "published",
    review: {
      science: "approved",
      ethics: "approved"
    }
  };
  assert.equal(isMissionOperationallyPublishable(artifact), true);
});

test("isMissionOperationallyPublishable fails when missing conditions", () => {
  const base = {
    type: "field-mission",
    status: "published",
    review: {
      science: "approved",
      ethics: "approved"
    }
  };

  assert.equal(isMissionOperationallyPublishable({ ...base, type: "species-page" }), false);
  assert.equal(isMissionOperationallyPublishable({ ...base, status: "draft" }), false);
  assert.equal(isMissionOperationallyPublishable({ ...base, review: { science: "pending", ethics: "approved" } }), false);
  assert.equal(isMissionOperationallyPublishable({ ...base, review: { science: "approved", ethics: "pending" } }), false);
});
