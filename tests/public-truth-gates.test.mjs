import assert from "node:assert/strict"
import { readdir, readFile } from "node:fs/promises"
import path from "node:path"
import test from "node:test"
import { fileURLToPath } from "node:url"
import {
  isMissionOperationallyPublishable,
  isReviewComplete,
} from "../lib/review-gates.ts"

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

test("field missions require publication and ethics approval", async () => {
  const [indexPage, detailComponent] = await Promise.all([
    read("app/missions/page.tsx"),
    read("components/artifact-detail.tsx"),
  ])

  assert.match(
    indexPage,
    /withholds operational wildlife guidance until publication and ethics approval/,
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
  const [support, appFiles, libFiles, readme, strategy] = await Promise.all([
    read("app/support/page.tsx"),
    readdir(path.join(ROOT, "app"), { recursive: true, withFileTypes: true }),
    readdir(path.join(ROOT, "lib"), { recursive: true, withFileTypes: true }),
    read("README.md"),
    read("STRATEGY.md"),
  ])

  assert.doesNotMatch(support, /github\.com\/sponsors\/frankxai/)
  assert.match(support, /No verified GitHub Sponsors checkout/)

  const publicSourceFiles = [...appFiles, ...libFiles].filter(
    (entry) =>
      entry.isFile() &&
      /\.(?:ts|tsx|js|mjs)$/.test(entry.name),
  )
  for (const entry of publicSourceFiles) {
    const source = await readFile(path.join(entry.parentPath, entry.name), "utf8")
    assert.doesNotMatch(source, /github\.com\/frankxai\/ocean-intelligence-system/)
  }

  for (const source of [readme, strategy]) {
    assert.doesNotMatch(source, /github\.com\/frankxai\/ocean-intelligence-system/)
    assert.match(source, /github\.com\/frankxai\/marine-mcp/)
  }
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
