#!/usr/bin/env node
/**
 * blc-validate — the contribution workbench.
 *
 * Runs the checks a reviewer would run, in a fixed order, against a
 * CommonsGraph.v1 contribution packet, and prints a receipt. Nothing is
 * exported while an error stands.
 *
 *   node bin/blc-validate.mjs <packet.json>
 *   node bin/blc-validate.mjs <packet.json> --json
 *   node bin/blc-validate.mjs <packet.json> --export out/packet.graph.json
 *
 * Exit code 0 when the packet is ready to open a PR with, 1 when it is not.
 */

import { readFile, writeFile, mkdir } from "node:fs/promises"
import { dirname, resolve } from "node:path"
import process from "node:process"

import { validatePacket, formatReceipt } from "../lib/commons-graph/packet.mjs"

const USAGE = `blc-validate — validate a Blue Life Commons contribution packet

  node bin/blc-validate.mjs <packet.json> [options]

Options
  --json                 print the receipt as JSON instead of text
  --export <path>        write the machine-readable graph export (only when the packet passes)
  --now <ISO date>       evaluate citation freshness as of this date
  -h, --help             show this message

Checks, in order: schema, structure, citation, license, location-sensitivity,
review-state, ethics, attribution, export.
`

function parseArgs(argv) {
  const args = { packet: undefined, json: false, exportPath: undefined, now: undefined }
  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i]
    if (arg === "-h" || arg === "--help") return { help: true }
    else if (arg === "--json") args.json = true
    else if (arg === "--export") args.exportPath = argv[++i]
    else if (arg === "--now") args.now = argv[++i]
    else if (arg.startsWith("-")) throw new Error(`unknown option: ${arg}`)
    else if (!args.packet) args.packet = arg
    else throw new Error("only one packet may be validated at a time")
  }
  return args
}

async function main() {
  let args
  try {
    args = parseArgs(process.argv.slice(2))
  } catch (error) {
    process.stderr.write(`${error.message}\n\n${USAGE}`)
    process.exitCode = 2
    return
  }

  if (args.help || !args.packet) {
    process.stdout.write(USAGE)
    process.exitCode = args.help ? 0 : 2
    return
  }

  const packetPath = resolve(process.cwd(), args.packet)
  let packet
  try {
    packet = JSON.parse(await readFile(packetPath, "utf8"))
  } catch (error) {
    process.stderr.write(`could not read packet ${packetPath}: ${error.message}\n`)
    process.exitCode = 2
    return
  }

  let now = Date.now()
  if (args.now) {
    const parsed = Date.parse(args.now)
    if (Number.isNaN(parsed)) {
      process.stderr.write(`--now is not a date: ${args.now}\n`)
      process.exitCode = 2
      return
    }
    now = parsed
  }

  const receipt = validatePacket(packet, { now })

  if (args.json) {
    process.stdout.write(`${JSON.stringify(receipt, null, 2)}\n`)
  } else {
    process.stdout.write(`${formatReceipt(receipt)}\n`)
  }

  if (args.exportPath) {
    if (!receipt.export) {
      process.stderr.write("no export written: the packet has unresolved errors\n")
    } else {
      const out = resolve(process.cwd(), args.exportPath)
      await mkdir(dirname(out), { recursive: true })
      await writeFile(out, `${JSON.stringify(receipt.export, null, 2)}\n`, "utf8")
      process.stdout.write(`export written to ${out}\n`)
    }
  }

  process.exitCode = receipt.ok ? 0 : 1
}

await main()
