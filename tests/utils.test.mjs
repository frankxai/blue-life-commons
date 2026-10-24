import test from "node:test";
import assert from "node:assert/strict";
import { cn, titleCase, formatRegion, formatDate } from "../lib/utils.ts";

test("cn combines valid classes and ignores falsy values", () => {
  assert.equal(cn("foo", "bar"), "foo bar");
  assert.equal(cn("foo", false, "bar", null, undefined, ""), "foo bar");
  assert.equal(cn(null, undefined, false), "");
  assert.equal(cn("a", "b", "c"), "a b c");
});

test("titleCase capitalizes words and replaces separators with spaces", () => {
  assert.equal(titleCase("hello_world"), "Hello World");
  assert.equal(titleCase("foo-bar-baz"), "Foo Bar Baz");
  assert.equal(titleCase("single"), "Single");
  assert.equal(titleCase("already Title Cased"), "Already Title Cased");
});

test("formatRegion is an alias for titleCase", () => {
  assert.equal(formatRegion("north_atlantic"), "North Atlantic");
  assert.equal(formatRegion("pacific-ocean"), "Pacific Ocean");
});

test("formatDate formats valid dates correctly", () => {
  // The function parses the input as a UTC date because it is in YYYY-MM-DD format.
  // It then outputs it using the local timezone.
  // We mock the local timezone to UTC for this test to avoid timezone-dependent failures.
  const originalTZ = process.env.TZ;
  process.env.TZ = "UTC";

  try {
    assert.equal(formatDate("2023-10-24"), "Oct 24, 2023");
    assert.equal(formatDate("2024-01-01"), "Jan 1, 2024");
  } finally {
    process.env.TZ = originalTZ;
  }
});

test("formatDate returns the input for invalid dates", () => {
  assert.equal(formatDate("not-a-date"), "not-a-date");
  assert.equal(formatDate("invalid"), "invalid");
});

test("formatDate returns empty string for empty input", () => {
  assert.equal(formatDate(""), "");
  assert.equal(formatDate(undefined), "");
});
