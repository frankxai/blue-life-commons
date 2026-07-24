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
const WHATWG_IGNORED = String.raw`[\t\n\r]*`
const WHATWG_IGNORED_CHARACTERS = new Set(["\t", "\n", "\r"])
const HTML_NAMED_REFERENCES = new Map([
  ["Tab", "\t"],
  ["NewLine", "\n"],
  ["amp", "&"],
  ["apos", "'"],
  ["bsol", "\\"],
  ["colon", ":"],
  ["comma", ","],
  ["equals", "="],
  ["gt", ">"],
  ["lpar", "("],
  ["lt", "<"],
  ["nbsp", "\u00A0"],
  ["num", "#"],
  ["percnt", "%"],
  ["period", "."],
  ["quest", "?"],
  ["quot", "\""],
  ["rpar", ")"],
  ["sol", "/"],
])

const tolerantSequence = (value) =>
  [...value].map((character) => `${character}${WHATWG_IGNORED}`).join("")
const TOLERANT_GITHUB_HOST = String.raw`(?:${tolerantSequence("www")}\.${WHATWG_IGNORED})?${tolerantSequence("github")}\.${WHATWG_IGNORED}${tolerantSequence("com")}`
const URL_REFERENCE_START = new RegExp(
  [
    `${tolerantSequence("http")}s?${WHATWG_IGNORED}:${WHATWG_IGNORED}/${WHATWG_IGNORED}/`,
    `/${WHATWG_IGNORED}/`,
    String.raw`(?<![A-Za-z0-9.@/?#_-])${TOLERANT_GITHUB_HOST}(?:\.${WHATWG_IGNORED})?(?=[:/]|$)`,
  ].join("|"),
  "giu",
)
const HARD_URL_BOUNDARY =
  /[<>"'`\[\]{}|=;&~*! \f\v\u00A0\u00AB\u00BB\u2013\u2014\u2018\u2019\u201C\u201D\u2026]/u

function normalizeUnicodeAndSeparators(value) {
  return value
    .normalize("NFKC")
    .replace(UNICODE_HOST_DOTS, ".")
    .replaceAll("\\", "/")
}

function decodeHtmlCodePoint(value, radix, original) {
  const codePoint = Number.parseInt(value, radix)
  if (
    !Number.isInteger(codePoint) ||
    codePoint < 1 ||
    codePoint > 0x10ffff ||
    (codePoint >= 0xd800 && codePoint <= 0xdfff)
  ) {
    return original
  }

  try {
    return String.fromCodePoint(codePoint)
  } catch {
    return original
  }
}

export function decodeHtmlCharacterReferences(value) {
  return value.replace(
    /&(?:#[xX]([0-9A-Fa-f]+);?|#([0-9]+);?|([A-Za-z][A-Za-z0-9]+);)/gu,
    (reference, hexadecimal, decimal, named) => {
      if (hexadecimal) return decodeHtmlCodePoint(hexadecimal, 16, reference)
      if (decimal) return decodeHtmlCodePoint(decimal, 10, reference)
      return HTML_NAMED_REFERENCES.get(named) ?? reference
    },
  )
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

function removeUnbalancedTrailingDelimiter(value, opening, closing) {
  let result = value
  while (result.endsWith(closing)) {
    const openings = [...result].filter((character) => character === opening).length
    const closings = [...result].filter((character) => character === closing).length
    if (closings <= openings) break
    result = result.slice(0, -closing.length)
  }
  return result
}

function trimTerminalReferencePunctuation(value) {
  let result = value
  let previous

  do {
    previous = result
    result = result.replace(/[.,:!?;~*\u2013\u2014\u2026]+$/u, "")
    result = removeUnbalancedTrailingDelimiter(result, "(", ")")
    result = removeUnbalancedTrailingDelimiter(result, "[", "]")
    result = removeUnbalancedTrailingDelimiter(result, "{", "}")
  } while (result !== previous)

  return result
}

function normalizePathSegment(value) {
  return normalizeUnicodeAndSeparators(
    safelyDecodePercentEscapes(value),
  ).toLowerCase()
}

function canonicalizeNormalizedGitHubReference(reference) {
  const normalized = trimTerminalReferencePunctuation(
    normalizeUnicodeAndSeparators(reference),
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

export function canonicalizeGitHubReference(reference) {
  return canonicalizeNormalizedGitHubReference(
    normalizeSourceForIsolation(reference),
  )
}

function isHardUrlBoundary(character) {
  if (WHATWG_IGNORED_CHARACTERS.has(character)) return false
  return HARD_URL_BOUNDARY.test(character) || /\s/u.test(character)
}

function extractCompleteReference(source, start) {
  let end = start
  while (end < source.length && !isHardUrlBoundary(source[end])) end += 1
  return trimTerminalReferencePunctuation(source.slice(start, end))
}

function normalizeSourceForIsolation(source) {
  return normalizeUnicodeAndSeparators(
    safelyDecodePercentEscapes(decodeHtmlCharacterReferences(source)),
  )
}

export function findUnavailableRepositoryReferences(source) {
  const normalizedSource = normalizeSourceForIsolation(source)
  const findings = []

  for (const start of normalizedSource.matchAll(URL_REFERENCE_START)) {
    const index = start.index ?? 0
    const candidate = extractCompleteReference(normalizedSource, index)
    const canonical = canonicalizeNormalizedGitHubReference(candidate)
    if (
      canonical?.owner === UNAVAILABLE_GITHUB_OWNER &&
      canonical.repository === UNAVAILABLE_GITHUB_REPOSITORY
    ) {
      findings.push({ index, value: candidate })
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
