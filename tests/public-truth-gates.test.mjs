import assert from "node:assert/strict"
import {
  mkdir,
  mkdtemp,
  readdir,
  readFile,
  rm,
  symlink,
  writeFile,
} from "node:fs/promises"
import os from "node:os"
import path from "node:path"
import test from "node:test"
import { fileURLToPath } from "node:url"
import {
  isMissionOperationallyPublishable,
  isReviewComplete,
} from "../lib/review-gates.ts"
import {
  auditPublishableLinks,
  collectPublishableTextFiles,
  hasUnavailableRepositoryReference,
} from "../scripts/verify_public_links.mjs"

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..")
const read = (relativePath) => readFile(path.join(ROOT, relativePath), "utf8")

async function markdownFiles(directory) {
  const entries = await readdir(path.join(ROOT, directory), {
    recursive: true,
    withFileTypes: true,
  })
  return entries
    .filter((entry) => entry.isFile() && entry.name.endsWith(".md"))
    .map((entry) => path.join(entry.parentPath, entry.name))
}

test("field missions require publication, science, and ethics approval", async () => {
  const [indexPage, detailComponent] = await Promise.all([
    read("app/missions/page.tsx"),
    read("components/artifact-detail.tsx"),
  ])

  assert.match(
    indexPage,
    /withholds operational wildlife guidance until publication, science, and ethics approval/,
  )
  assert.match(indexPage, /does not route or credit observations/)
  assert.doesNotMatch(indexPage, /Every mission carries an ethics review/)
  assert.doesNotMatch(indexPage, /observations feed OBIS/)

  assert.match(detailComponent, /!isMissionOperationallyPublishable\(a\)/)
  assert.match(detailComponent, /This is not operational wildlife guidance\./)
  assert.match(detailComponent, /missionBodyWithheld \? \(/)

  assert.equal(
    isMissionOperationallyPublishable({
      type: "field-mission",
      status: "needs-expert-review",
      review: { science: "required", ethics: "approved" },
    }),
    false,
    "ethics approval must not release a mission that remains in review",
  )
  assert.equal(
    isMissionOperationallyPublishable({
      type: "field-mission",
      status: "published",
      review: { science: "required", ethics: "approved" },
    }),
    false,
    "publication and ethics approval must not bypass the science gate",
  )
  assert.equal(
    isMissionOperationallyPublishable({
      type: "field-mission",
      status: "published",
      review: { science: "approved", ethics: "required" },
    }),
    false,
    "publication status must not bypass the ethics gate",
  )
  assert.equal(
    isMissionOperationallyPublishable({
      type: "field-mission",
      status: "approved",
      review: { science: "approved", ethics: "approved" },
    }),
    true,
  )
})

test("organization profiles never imply an undocumented relationship", async () => {
  const [directoryPage, directoryReadme, files] = await Promise.all([
    read("app/partners/page.tsx"),
    read("content/partners/README.md"),
    markdownFiles("content/partners"),
  ])

  assert.match(directoryPage, /Inclusion does not imply partnership/)
  assert.match(directoryReadme, /does not establish[\s\S]*partnership/)

  for (const file of files) {
    const source = await readFile(file, "utf8")
    assert.doesNotMatch(source, /Starlight Marine Systems/)
    assert.doesNotMatch(source, /as a commons partner/i)
    assert.doesNotMatch(source, /^title:\s*["']?Partner Profile/im)
  }
})

test("public conversion links resolve only to represented public surfaces", async () => {
  const [support, fixtureSource, publishableFiles, audit] = await Promise.all([
    read("app/support/page.tsx"),
    read("tests/fixtures/public-link-guard.json"),
    collectPublishableTextFiles(ROOT),
    auditPublishableLinks(ROOT),
  ])

  assert.doesNotMatch(support, /github\.com\/sponsors\/frankxai/)
  assert.match(support, /No verified GitHub Sponsors checkout/)

  const relativePublishableFiles = publishableFiles.map((file) =>
    path.relative(ROOT, file),
  )
  for (const requiredSurface of [
    "app/support/page.tsx",
    "components/artifact-detail.tsx",
    "content/research/dataset-gbif.md",
    "content/research/dataset-obis.md",
    "docs/guides/for-developers.md",
    "lib/content.ts",
  ]) {
    assert.ok(
      relativePublishableFiles.includes(requiredSurface),
      `${requiredSurface} must remain inside the recursive public-link audit`,
    )
  }

  assert.deepEqual(audit.findings, [])

  const fixtures = JSON.parse(fixtureSource)
  for (const source of fixtures.blocked) {
    assert.equal(
      hasUnavailableRepositoryReference(source),
      true,
      `expected blocked fixture to match: ${source}`,
    )
  }
  for (const source of fixtures.allowed) {
    assert.equal(
      hasUnavailableRepositoryReference(source),
      false,
      `expected allowed fixture not to match: ${source}`,
    )
  }
})

test("nested excluded-name routes remain auditable", async (context) => {
  const fixtureSource = await read("tests/fixtures/public-link-guard.json")
  const fixtures = JSON.parse(fixtureSource)
  const temporaryRoot = await mkdtemp(
    path.join(os.tmpdir(), "blue-life-public-links-nested-"),
  )
  context.after(() => rm(temporaryRoot, { recursive: true, force: true }))

  for (const relativePath of fixtures.nested_excluded_name_routes) {
    const absolutePath = path.join(temporaryRoot, relativePath)
    await mkdir(path.dirname(absolutePath), { recursive: true })
    await writeFile(absolutePath, `${fixtures.blocked[0]}\n`, "utf8")
  }

  const audit = await auditPublishableLinks(temporaryRoot)
  assert.deepEqual(
    audit.findings.map((finding) => finding.path).sort(),
    [...fixtures.nested_excluded_name_routes].sort(),
  )
})

test("symbolic links fail closed, including links outside the audit root", async (context) => {
  const temporaryParent = await mkdtemp(
    path.join(os.tmpdir(), "blue-life-public-links-symlink-"),
  )
  context.after(() => rm(temporaryParent, { recursive: true, force: true }))

  const auditRoot = path.join(temporaryParent, "repository")
  const contentRoot = path.join(auditRoot, "content")
  await mkdir(contentRoot, { recursive: true })

  const inRootTarget = path.join(contentRoot, "target.md")
  await writeFile(inRootTarget, "Inspectable source.\n", "utf8")
  await symlink(inRootTarget, path.join(contentRoot, "in-root-link.md"))
  await assert.rejects(
    auditPublishableLinks(auditRoot),
    /refuses symbolic link: content\/in-root-link\.md/,
  )

  await rm(path.join(contentRoot, "in-root-link.md"))
  const outsideTarget = path.join(temporaryParent, "outside.md")
  await writeFile(outsideTarget, "Outside source.\n", "utf8")
  await symlink(outsideTarget, path.join(contentRoot, "escape-link.md"))
  await assert.rejects(
    auditPublishableLinks(auditRoot),
    /refuses symbolic link: content\/escape-link\.md/,
  )
})

test("in-review artifacts stay out of search indexes and published claims", async () => {
  const routeFiles = [
    "app/missions/[...slug]/page.tsx",
    "app/partners/[slug]/page.tsx",
    "app/regions/[slug]/page.tsx",
    "app/research/[slug]/page.tsx",
    "app/species/[guild]/[slug]/page.tsx",
    "app/welfare/[slug]/page.tsx",
  ]
  const [contentLibrary, sitemap, detailComponent, ...routes] = await Promise.all([
    read("lib/content.ts"),
    read("app/sitemap.ts"),
    read("components/artifact-detail.tsx"),
    ...routeFiles.map(read),
  ])

  assert.match(contentLibrary, /export \{ isReviewComplete \}/)
  assert.equal(isReviewComplete({ status: "approved" }), true)
  assert.equal(isReviewComplete({ status: "published" }), true)
  assert.equal(isReviewComplete({ status: "needs-expert-review" }), false)
  assert.match(sitemap, /\.filter\(isReviewComplete\)/)
  for (const route of routes) assert.match(route, /robots: getArtifactRobots\(artifact\)/)

  assert.match(detailComponent, /Impact claim in review/)
  assert.match(
    detailComponent,
    /not presented as an outcome until review is complete/,
  )
})
