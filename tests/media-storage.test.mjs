import test from "node:test";
import assert from "node:assert/strict";
import { mediaStorageObjectPrefix } from "../lib/media-storage.ts";

test("mediaStorageObjectPrefix returns the correct path prefix", () => {
  assert.equal(
    mediaStorageObjectPrefix({
      taxonGroup: "fish",
      slug: "clownfish",
      assetId: "12345"
    }),
    "species/fish/clownfish/12345/"
  );
});

test("mediaStorageObjectPrefix handles empty string properties", () => {
  assert.equal(
    mediaStorageObjectPrefix({
      taxonGroup: "",
      slug: "",
      assetId: ""
    }),
    "species////"
  );
});
