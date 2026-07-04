#!/usr/bin/env node
import { createHash } from "node:crypto"
import fs from "node:fs"
import path from "node:path"
import { fileURLToPath } from "node:url"
import { put } from "@vercel/blob"
import YAML from "yaml"

const __dirname = path.dirname(fileURLToPath(import.meta.url))
const ROOT = path.resolve(__dirname, "..")
const STORAGE_MANIFEST_PATH = path.join(
  ROOT,
  "content",
  "media",
  "species-media-storage-manifest.yaml",
)
const BLOB_MANIFEST_PATH = path.join(
  ROOT,
  "content",
  "media",
  "species-media-blob-manifest.json",
)
const ENV_PATH = path.join(ROOT, ".env.local")

function readJson(pathname, fallback) {
  if (!fs.existsSync(pathname)) return fallback
  return JSON.parse(fs.readFileSync(pathname, "utf8"))
}

function loadLocalEnv() {
  if (!fs.existsSync(ENV_PATH)) return
  const lines = fs.readFileSync(ENV_PATH, "utf8").split(/\r?\n/)
  for (const line of lines) {
    if (!line || line.trimStart().startsWith("#") || !line.includes("=")) continue
    const [key, ...rest] = line.split("=")
    if (!process.env[key]) {
      process.env[key] = rest.join("=").trim().replace(/^["']|["']$/g, "")
    }
  }
}

function parseArgs(argv) {
  const args = new Set(argv)
  const valueAfter = (name) => {
    const index = argv.indexOf(name)
    return index >= 0 ? argv[index + 1] : undefined
  }
  return {
    write: args.has("--write"),
    check: args.has("--check"),
    force: args.has("--force"),
    limit: Number(valueAfter("--limit") ?? 0),
    only: valueAfter("--only"),
  }
}

function sha256(buffer) {
  return createHash("sha256").update(buffer).digest("hex")
}

function nowIsoDate() {
  return new Date().toISOString().slice(0, 10)
}

function publicRecordFromUpload(record, source, blob, buffer) {
  return {
    artifact_id: record.artifact_id,
    website_path: record.website_path,
    taxon_group: record.taxon_group,
    slug: record.slug,
    common_name: record.common_name,
    scientific_name: record.scientific_name,
    approved_asset_id: record.approved_asset_id,
    source_url: record.source_url,
    original_media_url: record.original_media_url,
    rights_status: record.rights_status,
    license: record.license,
    creator: record.creator,
    storage: {
      provider: "vercel_blob",
      store: record.storage?.store ?? "blue-life-commons-media",
      status: "uploaded",
      uploaded_at: new Date().toISOString(),
      source_pathname: source.pathname,
      source_content_type: blob.contentType,
      source_content_length: buffer.byteLength,
      source_sha256: sha256(buffer),
      blob_url: blob.url,
      blob_download_url: blob.downloadUrl,
      blob_pathname: blob.pathname,
    },
  }
}

async function fetchSource(record) {
  const url = record.current_public_media_url || record.original_media_url
  if (!url) throw new Error(`No source URL for ${record.approved_asset_id}`)
  const response = await fetch(url, {
    headers: {
      "User-Agent":
        "BlueLifeCommonsMediaMirror/1.0 (+https://github.com/frankxai/blue-life-commons)",
    },
  })
  if (!response.ok) {
    throw new Error(
      `${record.approved_asset_id} fetch failed: ${response.status} ${response.statusText}`,
    )
  }
  const contentType =
    response.headers.get("content-type")?.split(";")[0] ||
    "application/octet-stream"
  const arrayBuffer = await response.arrayBuffer()
  return { buffer: Buffer.from(arrayBuffer), contentType }
}

function sourceVariant(record) {
  const variants = record.storage?.variants ?? []
  const original = variants.find((variant) => variant.name === "original")
  if (!original?.object_key) {
    throw new Error(`Missing original object key for ${record.approved_asset_id}`)
  }
  return {
    name: "original",
    pathname: original.object_key,
  }
}

function buildOutput(existing, records) {
  return {
    version: nowIsoDate(),
    generated_at: new Date().toISOString(),
    provider: "vercel_blob",
    store: "blue-life-commons-media",
    source_manifest: "content/media/species-media-storage-manifest.yaml",
    public_use: true,
    note:
      "Public Vercel Blob URLs for approved Blue Life Commons species media. Source URLs and credits remain the attribution source of record.",
    summary: {
      approved_species_records: records.length,
      uploaded_records: existing.length,
      pending_records: Math.max(0, records.length - existing.length),
    },
    records: existing.sort((a, b) =>
      String(a.common_name).localeCompare(String(b.common_name)),
    ),
  }
}

async function main() {
  const options = parseArgs(process.argv.slice(2))
  loadLocalEnv()

  const storageManifest = YAML.parse(
    fs.readFileSync(STORAGE_MANIFEST_PATH, "utf8"),
  )
  let records = (storageManifest.records ?? []).filter(
    (record) =>
      record.storage?.provider === "vercel_blob" &&
      record.storage?.mirror_allowed_by_current_rights_status === true &&
      record.migration_gate?.ready_for_mirror_review === true,
  )
  if (options.only) {
    records = records.filter(
      (record) =>
        record.approved_asset_id === options.only ||
        record.artifact_id === options.only ||
        record.slug === options.only,
    )
  }
  if (options.limit > 0) records = records.slice(0, options.limit)

  const existingManifest = readJson(BLOB_MANIFEST_PATH, { records: [] })
  const existingByAsset = new Map(
    (existingManifest.records ?? []).map((record) => [
      record.approved_asset_id,
      record,
    ]),
  )

  if (options.check) {
    const missing = records.filter(
      (record) => existingByAsset.get(record.approved_asset_id)?.storage?.status !== "uploaded",
    )
    if (missing.length) {
      console.error(
        `Blob manifest is missing ${missing.length} uploaded record(s): ${missing
          .slice(0, 8)
          .map((record) => record.approved_asset_id)
          .join(", ")}${missing.length > 8 ? ", ..." : ""}`,
      )
      process.exit(1)
    }
    console.log(`Blob manifest covers ${records.length} approved species image(s).`)
    return
  }

  if (!options.write) {
    const pending = records.filter(
      (record) => !existingByAsset.has(record.approved_asset_id),
    )
    console.log(
      `Dry run: ${records.length} approved image(s), ${pending.length} pending Blob upload(s). Use --write to upload.`,
    )
    return
  }

  const token = process.env.BLOB_READ_WRITE_TOKEN
  if (!token) {
    throw new Error(
      "Missing BLOB_READ_WRITE_TOKEN. Run `vercel env pull` or create/connect a Vercel Blob store first.",
    )
  }

  // Force read-write token auth for local batch uploads. OIDC is for Vercel runtime.
  delete process.env.VERCEL_OIDC_TOKEN
  delete process.env.BLOB_STORE_ID

  const uploaded = [...(existingManifest.records ?? [])]
  for (const record of records) {
    if (!options.force && existingByAsset.has(record.approved_asset_id)) {
      console.log(`skip ${record.approved_asset_id} (already uploaded)`)
      continue
    }

    const source = sourceVariant(record)
    console.log(`upload ${record.approved_asset_id} -> ${source.pathname}`)
    const { buffer, contentType } = await fetchSource(record)
    const blob = await put(source.pathname, buffer, {
      access: "public",
      addRandomSuffix: false,
      allowOverwrite: true,
      cacheControlMaxAge: 31536000,
      contentType,
      token,
    })
    const publicRecord = publicRecordFromUpload(record, source, blob, buffer)
    const existingIndex = uploaded.findIndex(
      (item) => item.approved_asset_id === record.approved_asset_id,
    )
    if (existingIndex >= 0) uploaded[existingIndex] = publicRecord
    else uploaded.push(publicRecord)
  }

  const output = buildOutput(uploaded, storageManifest.records ?? [])
  fs.writeFileSync(BLOB_MANIFEST_PATH, `${JSON.stringify(output, null, 2)}\n`)
  console.log(
    `Wrote ${path.relative(ROOT, BLOB_MANIFEST_PATH)} with ${output.summary.uploaded_records} uploaded image(s).`,
  )
}

main().catch((error) => {
  console.error(error.message)
  process.exit(1)
})
