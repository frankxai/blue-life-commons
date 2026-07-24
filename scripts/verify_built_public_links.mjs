import { readdir, readFile } from "node:fs/promises"
import path from "node:path"
import { fileURLToPath } from "node:url"
import { findUnavailableRepositoryReferences } from "./verify_public_links.mjs"

const REPOSITORY_ROOT = path.resolve(
  path.dirname(fileURLToPath(import.meta.url)),
  "..",
)
const BUILD_APP_ROOT = path.join(REPOSITORY_ROOT, ".next", "server", "app")
const EMITTED_TEXT_EXTENSIONS = new Set([
  ".html",
  ".js",
  ".json",
  ".rsc",
  ".txt",
])

async function walkEmittedText(directory, files) {
  const entries = await readdir(directory, { withFileTypes: true })
  for (const entry of entries) {
    const absolutePath = path.join(directory, entry.name)
    if (entry.isSymbolicLink()) {
      throw new Error(
        `Built-output audit refuses symbolic link: ${path.relative(BUILD_APP_ROOT, absolutePath)}`,
      )
    }
    if (entry.isDirectory()) {
      await walkEmittedText(absolutePath, files)
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

const files = []
await walkEmittedText(BUILD_APP_ROOT, files)

const htmlFiles = files.filter((file) => path.extname(file) === ".html")
if (htmlFiles.length === 0) {
  throw new Error("Built-output audit found no emitted HTML; refusing to pass")
}

const findings = []
for (const file of files.sort()) {
  const source = await readFile(file, "utf8")
  const references = findUnavailableRepositoryReferences(source)
  for (const reference of references) {
    findings.push({
      path: path.relative(REPOSITORY_ROOT, file),
      value: reference.value,
    })
  }
}

if (findings.length > 0) {
  for (const finding of findings) {
    console.error(
      `${finding.path}: emitted unavailable private repository reference: ${finding.value}`,
    )
  }
  process.exitCode = 1
} else {
  console.log(
    `Built-output guard checked ${htmlFiles.length} HTML files and ${files.length} emitted text files: 0 unavailable private repository references.`,
  )
}
