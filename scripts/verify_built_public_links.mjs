import { readdir, readFile, stat } from "node:fs/promises"
import path from "node:path"
import { fileURLToPath } from "node:url"
import { findUnavailableRepositoryReferences } from "./verify_public_links.mjs"

const REPOSITORY_ROOT = path.resolve(
  path.dirname(fileURLToPath(import.meta.url)),
  "..",
)
const BUILD_DIST_ROOT = path.join(REPOSITORY_ROOT, ".next")
// Next 16.3.8 writes prerendered app HTML to .next/server/app by default, but
// when a build adapter is active (Vercel: "Applying modifyConfig from Vercel")
// it writes it to .next/server/route-cache/APP_PAGE/<hash>/$/<route>.html instead.
// Audit both so the guard sees the real emitted HTML in every environment.
const BUILD_OUTPUT_ROOTS = [
  path.join(BUILD_DIST_ROOT, "server", "app"),
  path.join(BUILD_DIST_ROOT, "server", "route-cache"),
]
const PRERENDER_MANIFEST = path.join(BUILD_DIST_ROOT, "prerender-manifest.json")
const EMITTED_TEXT_EXTENSIONS = new Set([
  ".html",
  ".js",
  ".json",
  ".rsc",
  ".txt",
])

async function walkEmittedText(root, directory, files) {
  const entries = await readdir(directory, { withFileTypes: true })
  for (const entry of entries) {
    const absolutePath = path.join(directory, entry.name)
    if (entry.isSymbolicLink()) {
      throw new Error(
        `Built-output audit refuses symbolic link: ${path.relative(root, absolutePath)}`,
      )
    }
    if (entry.isDirectory()) {
      await walkEmittedText(root, absolutePath, files)
      continue
    }
    if (
      entry.isFile() &&
      EMITTED_TEXT_EXTENSIONS.has(path.extname(entry.name).toLowerCase())
    ) {
      files.push(absolutePath)
    }
  }
}

async function isDirectory(directory) {
  try {
    return (await stat(directory)).isDirectory()
  } catch (error) {
    if (error.code === "ENOENT") return false
    throw error
  }
}

export async function auditBuiltPublicLinks(
  buildRoots = BUILD_OUTPUT_ROOTS,
  displayRoot = REPOSITORY_ROOT,
) {
  const roots = Array.isArray(buildRoots) ? buildRoots : [buildRoots]
  const files = []
  const auditedRoots = []
  for (const root of roots) {
    if (!(await isDirectory(root))) continue
    auditedRoots.push(root)
    await walkEmittedText(root, root, files)
  }
  if (auditedRoots.length === 0) {
    throw new Error(
      `Built-output audit found no build output directory (looked in ${roots
        .map((root) => path.relative(displayRoot, root))
        .join(", ")}); refusing to pass`,
    )
  }

  const htmlFiles = files.filter((file) => path.extname(file) === ".html")
  const findings = []
  for (const file of files.sort()) {
    const source = await readFile(file, "utf8")
    const references = findUnavailableRepositoryReferences(source)
    for (const reference of references) {
      findings.push({
        path: path.relative(displayRoot, file),
        value: reference.value,
      })
    }
  }

  return { files, htmlFiles, findings, auditedRoots }
}

async function countPrerenderedHtmlRoutes() {
  const manifest = JSON.parse(await readFile(PRERENDER_MANIFEST, "utf8"))
  return Object.values(manifest.routes ?? {}).filter(
    (route) => typeof route.htmlSize === "number" && route.htmlSize > 0,
  ).length
}

async function main() {
  const { files, htmlFiles, findings, auditedRoots } =
    await auditBuiltPublicLinks()
  if (htmlFiles.length === 0) {
    throw new Error("Built-output audit found no emitted HTML; refusing to pass")
  }
  const expectedHtml = await countPrerenderedHtmlRoutes()
  if (htmlFiles.length < expectedHtml) {
    throw new Error(
      `Built-output audit found ${htmlFiles.length} HTML files but the prerender manifest lists ${expectedHtml} prerendered HTML routes; refusing to pass`,
    )
  }
  if (findings.length === 0) {
    const where = auditedRoots
      .map((root) => path.relative(REPOSITORY_ROOT, root).replaceAll("\\", "/"))
      .join(", ")
    console.log(
      `Built-output guard checked ${htmlFiles.length} HTML files (${expectedHtml} prerendered routes) and ${files.length} emitted text files in ${where}: 0 unavailable private repository references.`,
    )
    return
  }

  for (const finding of findings) {
    console.error(
      `${finding.path}: emitted unavailable private repository reference: ${finding.value}`,
    )
  }
  process.exitCode = 1
}

if (
  process.argv[1] &&
  path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)
) {
  await main()
}