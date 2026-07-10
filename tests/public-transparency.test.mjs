import assert from "node:assert/strict"
import { readFile } from "node:fs/promises"
import test from "node:test"

const read = (path) => readFile(new URL(`../${path}`, import.meta.url), "utf8")

test("privacy route publishes canonical metadata and is discoverable", async () => {
  const [page, header, footer, sitemap] = await Promise.all([
    read("app/privacy/page.tsx"),
    read("components/site-header.tsx"),
    read("components/site-footer.tsx"),
    read("app/sitemap.ts"),
  ])

  assert.match(page, /title: "Privacy & Transparency"/)
  assert.match(page, /alternates: \{ canonical: "\/privacy" \}/)
  assert.match(page, /openGraph: \{ url: "\/privacy" \}/)
  assert.match(header, /href: "\/privacy", label: "Privacy"/)
  assert.match(footer, /href: "\/privacy", label: "Privacy & transparency"/)
  assert.match(sitemap, /"\/privacy"/)
})

test("transparency route has no hidden intake, browser identity, or PII telemetry", async () => {
  const page = await read("app/privacy/page.tsx")
  const packageJson = await read("package.json")

  const forbiddenRuntimePatterns = [
    /["']use client["']/,
    /<form\b/i,
    /<input\b/i,
    /\bfetch\s*\(/,
    /sendBeacon\s*\(/,
    /localStorage/,
    /sessionStorage/,
    /document\.cookie/,
  ]

  for (const pattern of forbiddenRuntimePatterns) assert.doesNotMatch(page, pattern)

  for (const dependency of ["@vercel/analytics", "posthog", "plausible", "segment", "mixpanel", "amplitude"]) {
    assert.doesNotMatch(packageJson, new RegExp(dependency, "i"), dependency)
  }

  assert.match(page, /does not install a browser analytics SDK/)
  assert.match(page, /does not ask for an email address or hide a contribution form/)
})

test("GitHub remains the contribution source of truth", async () => {
  const page = await read("app/privacy/page.tsx")

  assert.match(page, /GitHub is the intake and review record/)
  assert.match(page, /does not collect contribution text/)
  assert.match(page, /GITHUB_REPO_URL\}\/issues\/new\/choose/)
  assert.match(page, /GITHUB_REPO_URL\}\/pulls/)
  assert.match(page, /not a second source of truth/)
})

test("review claims remain item-level and never imply blanket approval", async () => {
  const page = await read("app/privacy/page.tsx")

  assert.match(page, /Citation and review state travel with each artifact/)
  assert.match(page, /pending, required, approved, or not\s+applicable/)
  assert.match(page, /does not claim blanket ethics or scientific\s+approval for the whole site/)
  assert.match(page, /Ethics review is mandatory for\s+artifacts involving animal interaction/)

  for (const claim of [
    /all (?:content|artifacts?) (?:is|are) ethics[- ]reviewed/i,
    /every (?:page|artifact) (?:has|carries) ethics approval/i,
    /fully ethics[- ]reviewed/i,
  ]) {
    assert.doesNotMatch(page, claim)
  }
})

test("scientific dataset boundaries preserve upstream authority", async () => {
  const page = await read("app/privacy/page.tsx")

  assert.match(page, /reads public OBIS and GBIF API responses on the server/)
  assert.match(page, /upstream providers and dataset publishers remain authoritative/)
  assert.match(page, /does not claim ownership or control of those records/)
  assert.match(page, /does not make every destination a Blue Life Commons processor or partner/)
  assert.doesNotMatch(page, /Blue Life Commons is the data controller for (?:OBIS|GBIF)/i)
})
