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

const UNAVAILABLE_GITHUB_OWNER = "frankxai"
const UNAVAILABLE_GITHUB_REPOSITORY = "ocean-intelligence-system"
const UNICODE_HOST_DOTS = /[\u3002\uFF0E\uFF61]/gu
const VALID_PERCENT_RUN = /(?:%[0-9A-Fa-f]{2})+/gu
// These expressions only isolate reference-shaped text. The blocking decision
// is made after WHATWG URL parsing and exact canonical owner/repository comparison.
const REFERENCE_FRAGMENT =
  /[^\s<>"'`()\[\]{}~!,;=|&\u00AB\u00BB\u2013\u2014\u2018\u2019\u201C\u201D\u2026]+/gu

function normalizeUnicodeAndSeparators(value) {
  return value
    .normalize("NFKC")
    .replace(UNICODE_HOST_DOTS, ".")
    .replaceAll("\\", "/")
}

export function safelyDecodePercentEscapes(value) {
  let decoded = value

  for (let pass = 0; pass < 3; pass += 1) {
    const next = decoded.replace(VALID_PERCENT_RUN, (run) => {
      try {
        return decodeURIComponent(run)
      } catch {
        return run
      }
    })
    if (next === decoded) break
    decoded = next
  }

  return decoded
}

function trimTerminalReferencePunctuation(value) {
  return value.replace(/[.:]+$/u, "")
}

function normalizePathSegment(value) {
  return normalizeUnicodeAndSeparators(
    safelyDecodePercentEscapes(value),
  ).toLowerCase()
}

export function canonicalizeGitHubReference(reference) {
  const normalized = trimTerminalReferencePunctuation(
    normalizeUnicodeAndSeparators(safelyDecodePercentEscapes(reference)),
  )
  if (!normalized) return null

  let candidate
  if (normalized.startsWith("//")) {
    candidate = `https:${normalized}`
  } else if (/^https?:\/\//iu.test(normalized)) {
    candidate = normalized
  } else {
    candidate = `https://${normalized}`
  }

  let url
  try {
    url = new URL(candidate)
  } catch {
    return null
  }

  if (url.protocol !== "http:" && url.protocol !== "https:") return null

  const hostname = normalizeUnicodeAndSeparators(url.hostname)
    .toLowerCase()
    .replace(/\.+$/u, "")
    .replace(/^www\./u, "")
  if (hostname !== "github.com") return null

  const segments = url.pathname
    .split("/")
    .filter(Boolean)
    .map(normalizePathSegment)
  if (segments.length < 2) return null

  const owner = segments[0]
  const rawRepository = segments[1]
  const repository = rawRepository.endsWith(".git")
    ? rawRepository.slice(0, -4)
    : rawRepository

  return { hostname, owner, repository }
}

function extractReferenceCandidates(fragment) {
  const normalized = normalizeUnicodeAndSeparators(
    safelyDecodePercentEscapes(fragment),
  )
  const networkReferences = [
    ...normalized.matchAll(/https?:\/\/|\/\//giu),
  ].map((match) => normalized.slice(match.index ?? 0))
  if (networkReferences.length > 0) return [...new Set(networkReferences)]

  const bareReferences = []
  const bareGitHub =
    /(?:^|[=:])(?:www\.)?github\.com(?:\.(?=[:/]|$))?(?=[:/]|$)/giu
  for (const match of normalized.matchAll(bareGitHub)) {
    const value = match[0]
    const prefixLength = value.startsWith(":") || value.startsWith("=") ? 1 : 0
    bareReferences.push(normalized.slice((match.index ?? 0) + prefixLength))
  }

  return [...new Set(bareReferences)]
}

export function findUnavailableRepositoryReferences(source) {
  const normalizedSource = normalizeUnicodeAndSeparators(source)
  const findings = []

  for (const fragment of normalizedSource.matchAll(REFERENCE_FRAGMENT)) {
    for (const candidate of extractReferenceCandidates(fragment[0])) {
      const canonical = canonicalizeGitHubReference(candidate)
      if (
        canonical?.owner === UNAVAILABLE_GITHUB_OWNER &&
        canonical.repository === UNAVAILABLE_GITHUB_REPOSITORY
      ) {
        findings.push({
          index: fragment.index ?? 0,
          value: candidate,
        })
        break
      }
    }
  }

  return findings
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
