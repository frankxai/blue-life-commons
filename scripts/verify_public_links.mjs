import { lstat, readdir, readFile } from "node:fs/promises"
import path from "node:path"
import { fileURLToPath } from "node:url"

const REPOSITORY_ROOT = path.resolve(
  path.dirname(fileURLToPath(import.meta.url)),
  "..",
)

export const ROOT_EXCLUDED_DIRECTORY_NAMES = new Set([
  ".git",
  ".next",
  ".vercel",
  "coverage",
  "node_modules",
  "tests",
])

export const PUBLISHABLE_TEXT_EXTENSIONS = new Set([
  ".css",
  ".csv",
  ".html",
  ".js",
  ".jsx",
  ".json",
  ".md",
  ".mdx",
  ".mjs",
  ".py",
  ".sh",
  ".svg",
  ".toml",
  ".ts",
  ".tsx",
  ".txt",
  ".xml",
  ".yaml",
  ".yml",
])

const unavailableRepositoryPath = [
  "github.com",
  "frankxai",
  "ocean-intelligence-system",
].join("/")

const escapedUnavailableRepositoryPath = unavailableRepositoryPath.replace(
  /[.*+?^${}()|[\]\\]/g,
  String.raw`\$&`,
)

const unavailableRepositoryPattern = new RegExp(
  String.raw`(?<![A-Za-z0-9.-])(?:https?://|//)?(?:www\.)?${escapedUnavailableRepositoryPath}(?:\.git)?(?![A-Za-z0-9_-])`,
  "giu",
)

export function findUnavailableRepositoryReferences(source) {
  return [...source.matchAll(unavailableRepositoryPattern)].map((match) => ({
    index: match.index ?? 0,
    value: match[0],
  }))
}

export function hasUnavailableRepositoryReference(source) {
  return findUnavailableRepositoryReferences(source).length > 0
}

async function walkPublishableTextFiles(root, directory, files) {
  const entries = await readdir(directory, { withFileTypes: true })

  for (const entry of entries) {
    const absolutePath = path.join(directory, entry.name)
    const relativePath = path.relative(root, absolutePath)
    const isRootEntry = path.dirname(relativePath) === "."

    if (
      entry.isDirectory() &&
      isRootEntry &&
      ROOT_EXCLUDED_DIRECTORY_NAMES.has(entry.name)
    ) {
      continue
    }

    if (entry.isSymbolicLink()) {
      throw new Error(
        `Public-link audit refuses symbolic link: ${relativePath || "."}`,
      )
    }

    if (entry.isDirectory()) {
      await walkPublishableTextFiles(root, absolutePath, files)
      continue
    }

    if (
      entry.isFile() &&
      PUBLISHABLE_TEXT_EXTENSIONS.has(path.extname(entry.name).toLowerCase())
    ) {
      files.push(absolutePath)
    }
  }
}

export async function collectPublishableTextFiles(root = REPOSITORY_ROOT) {
  const rootMetadata = await lstat(root)
  if (rootMetadata.isSymbolicLink()) {
    throw new Error("Public-link audit root must not be a symbolic link")
  }
  if (!rootMetadata.isDirectory()) {
    throw new Error("Public-link audit root must be a directory")
  }

  const files = []
  await walkPublishableTextFiles(root, root, files)
  return files.sort()
}

function lineNumberAt(source, index) {
  return source.slice(0, index).split("\n").length
}

export async function auditPublishableLinks(root = REPOSITORY_ROOT) {
  const files = await collectPublishableTextFiles(root)
  const findings = []

  for (const absolutePath of files) {
    const source = await readFile(absolutePath, "utf8")
    for (const match of findUnavailableRepositoryReferences(source)) {
      findings.push({
        path: path.relative(root, absolutePath),
        line: lineNumberAt(source, match.index),
        value: match.value,
      })
    }
  }

  return { files, findings }
}

async function main() {
  const { files, findings } = await auditPublishableLinks()
  if (findings.length > 0) {
    for (const finding of findings) {
      console.error(
        `${finding.path}:${finding.line}: unavailable private repository reference: ${finding.value}`,
      )
    }
    process.exitCode = 1
    return
  }

  console.log(
    `Public-link guard checked ${files.length} publishable text files: 0 unavailable private repository references.`,
  )
}

if (
  process.argv[1] &&
  path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)
) {
  await main()
}
