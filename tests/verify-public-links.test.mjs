import test from "node:test";
import assert from "node:assert/strict";

import {
  decodeHtmlCharacterReferences,
  safelyDecodePercentEscapes,
  canonicalizeGitHubReference,
  findUnavailableRepositoryReferences,
  hasUnavailableRepositoryReference
} from "../scripts/verify_public_links.mjs";

test("decodeHtmlCharacterReferences decodes standard references", () => {
  assert.equal(decodeHtmlCharacterReferences("Hello&amp;World"), "Hello&World");
  assert.equal(decodeHtmlCharacterReferences("Value&#x3E;"), "Value>");
  assert.equal(decodeHtmlCharacterReferences("Test&#60;"), "Test<");
  assert.equal(decodeHtmlCharacterReferences("A&nbsp;B"), "A\u00A0B");
});

test("decodeHtmlCharacterReferences handles invalid or unknown references", () => {
  assert.equal(decodeHtmlCharacterReferences("Hello&unknown;World"), "Hello&unknown;World");
  // Invalid code points should return original
  assert.equal(decodeHtmlCharacterReferences("Value&#x110000;"), "Value&#x110000;");
});

test("safelyDecodePercentEscapes decodes percent encoding safely", () => {
  assert.equal(safelyDecodePercentEscapes("Hello%20World"), "Hello World");
  // Note safelyDecodePercentEscapes loops up to 3 passes, so it will decode Double%2520Escaped -> Double%20Escaped -> Double Escaped
  assert.equal(safelyDecodePercentEscapes("Double%2520Escaped"), "Double Escaped");
  assert.equal(safelyDecodePercentEscapes("Path%2FTo%2FFile"), "Path/To/File");
});

test("safelyDecodePercentEscapes handles malformed sequences gracefully", () => {
  assert.equal(safelyDecodePercentEscapes("Bad%2"), "Bad%2");
  assert.equal(safelyDecodePercentEscapes("Bad%ZZ"), "Bad%ZZ");
});

test("canonicalizeGitHubReference handles various formats correctly", () => {
  const result1 = canonicalizeGitHubReference("https://github.com/frankxai/blue-life-commons");
  assert.equal(result1?.hostname, "github.com");
  assert.equal(result1?.owner, "frankxai");
  assert.equal(result1?.repository, "blue-life-commons");

  const result2 = canonicalizeGitHubReference("github.com/frankxai/blue-life-commons.git");
  assert.equal(result2?.repository, "blue-life-commons");

  const result3 = canonicalizeGitHubReference("http://www.github.com/other-owner/repo");
  assert.equal(result3?.owner, "other-owner");
  assert.equal(result3?.repository, "repo");
});

test("canonicalizeGitHubReference returns null for invalid or non-GitHub URLs", () => {
  assert.equal(canonicalizeGitHubReference("https://example.com/frankxai/repo"), null);
  assert.equal(canonicalizeGitHubReference("https://github.com/"), null); // No owner/repo
  assert.equal(canonicalizeGitHubReference("not-a-url"), null);
});

test("findUnavailableRepositoryReferences and hasUnavailableRepositoryReference", () => {
  const sourceWithPrivate = "Check out this private repo: https://github.com/frankxai/ocean-intelligence-system it is hidden.";
  const sourceWithoutPrivate = "This is a public one: https://github.com/frankxai/blue-life-commons";

  const findings = findUnavailableRepositoryReferences(sourceWithPrivate);
  assert.equal(findings.length, 1);
  assert.ok(findings[0].value.includes("ocean-intelligence-system"));

  assert.equal(hasUnavailableRepositoryReference(sourceWithPrivate), true);

  const findingsEmpty = findUnavailableRepositoryReferences(sourceWithoutPrivate);
  assert.equal(findingsEmpty.length, 0);

  assert.equal(hasUnavailableRepositoryReference(sourceWithoutPrivate), false);
});
