#!/usr/bin/env node
/**
 * Upload Deep Time local concept media (public/media/species/*) to Vercel Blob.
 * Uses BLOB_READ_WRITE_TOKEN from .env.local (vercel env pull) or process env.
 *
 * Usage:
 *   node scripts/upload_deep_time_media_to_blob.mjs           # dry run
 *   node scripts/upload_deep_time_media_to_blob.mjs --write   # upload
 */
import fs from "node:fs"
import path from "node:path"
import { fileURLToPath } from "node:url"
import { put } from "@vercel/blob"

const __dirname = path.dirname(fileURLToPath(import.meta.url))
const ROOT = path.resolve(__dirname, "..")
const MEDIA_DIR = path.join(ROOT, "public", "media", "species")
const OUT_MANIFEST = path.join(
  ROOT,
  "content",
  "media",
  "deep-time-blob-manifest.json",
)
const ENV_PATH = path.join(ROOT, ".env.local")

function loadLocalEnv() {
  if (!fs.existsSync(ENV_PATH)) return
  for (const line of fs.readFileSync(ENV_PATH, "utf8").split(/\r?\n/)) {
    if (!line || line.trimStart().startsWith("#") || !line.includes("=")) continue
    const [key, ...rest] = line.split("=")
    if (!process.env[key]) {
      process.env[key] = rest.join("=").trim().replace(/^["']|["']$/g, "")
    }
  }
}

function contentType(file) {
  if (file.endsWith(".png")) return "image/png"
  if (file.endsWith(".jpg") || file.endsWith(".jpeg")) return "image/jpeg"
  if (file.endsWith(".mp4")) return "video/mp4"
  if (file.endsWith(".webp")) return "image/webp"
  return "application/octet-stream"
}

async function main() {
  loadLocalEnv()
  const write = process.argv.includes("--write")
  const token = process.env.BLOB_READ_WRITE_TOKEN
  if (!token) {
    throw new Error(
      "Missing BLOB_READ_WRITE_TOKEN. Run: vercel env pull .env.local --yes",
    )
  }

  // Prefer RW token for local batch; OIDC is runtime-only.
  delete process.env.VERCEL_OIDC_TOKEN

  const files = fs
    .readdirSync(MEDIA_DIR)
    .filter((f) => /\.(png|jpe?g|mp4|webp)$/i.test(f))
    .sort()

  console.log(
    `${write ? "UPLOAD" : "DRY RUN"}: ${files.length} file(s) from public/media/species`,
  )

  if (!write) {
    for (const f of files) {
      const full = path.join(MEDIA_DIR, f)
      const st = fs.statSync(full)
      console.log(`  plan ${f} (${Math.round(st.size / 1024)} KB) -> deep-time/${f}`)
    }
    console.log("Use --write to upload.")
    return
  }

  const records = []
  for (const f of files) {
    const full = path.join(MEDIA_DIR, f)
    const buffer = fs.readFileSync(full)
    const pathname = `deep-time/species/${f}`
    console.log(`upload ${f} -> ${pathname}`)
    const blob = await put(pathname, buffer, {
      access: "public",
      addRandomSuffix: false,
      allowOverwrite: true,
      cacheControlMaxAge: 31536000,
      contentType: contentType(f),
      token,
    })
    records.push({
      file: f,
      slug: path.parse(f).name,
      kind: f.endsWith(".mp4") ? "video" : "image",
      bytes: buffer.byteLength,
      blob_url: blob.url,
      blob_pathname: blob.pathname,
      download_url: blob.downloadUrl,
      local_public_path: `/media/species/${f}`,
      rights_status: "concept-reconstruction",
      note: "AI concept reconstruction — not fossil evidence",
    })
  }

  const manifest = {
    version: new Date().toISOString().slice(0, 10),
    generated_at: new Date().toISOString(),
    provider: "vercel_blob",
    prefix: "deep-time/species/",
    count: records.length,
    total_bytes: records.reduce((s, r) => s + r.bytes, 0),
    records,
  }
  fs.mkdirSync(path.dirname(OUT_MANIFEST), { recursive: true })
  fs.writeFileSync(OUT_MANIFEST, `${JSON.stringify(manifest, null, 2)}\n`)
  console.log(
    `Wrote ${path.relative(ROOT, OUT_MANIFEST)} (${records.length} objects, ${Math.round(manifest.total_bytes / 1e6)} MB)`,
  )
}

main().catch((err) => {
  console.error(err.message || err)
  process.exit(1)
})
