import { execFileSync } from 'node:child_process'
import { readFileSync } from 'node:fs'
import { resolve } from 'node:path'
import process from 'node:process'

const root = resolve(import.meta.dirname, '..')
const read = (path) => readFileSync(resolve(root, path), 'utf8')
const fail = (message) => {
  throw new Error(`release contract: ${message}`)
}

const ledger = JSON.parse(read('docs/releases/release-ledger.json'))
const changelog = read('CHANGELOG.md')
const githubWorkflow = read('.github/workflows/draft-github-release.yml')
const packageManifest = JSON.parse(read('package.json'))
const releaseNotes = read(`docs/releases/${ledger.release.tag}.md`)

if (ledger.schemaVersion !== 1) fail('schemaVersion must be 1')
if (ledger.repository !== 'frankxai/blue-life-commons') {
  fail('repository must be frankxai/blue-life-commons')
}
if (ledger.defaultBranch !== 'main') fail('defaultBranch must be main')

const semver = /^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-[0-9A-Za-z.-]+)?$/
if (!semver.test(ledger.release.version)) fail('release.version must be SemVer')
if (ledger.release.tag !== `v${ledger.release.version}`) {
  fail('release.tag must match release.version')
}
if (!['draft', 'ready', 'published'].includes(ledger.release.status)) {
  fail('release.status must be draft, ready, or published')
}
if (ledger.release.published !== (ledger.release.status === 'published')) {
  fail('release.published must agree with release.status')
}
if (!/^[0-9a-f]{40}$/.test(ledger.source.auditedHead)) {
  fail('source.auditedHead must be a full SHA')
}
if (ledger.release.targetSha !== ledger.source.auditedHead) {
  fail('release.targetSha must equal source.auditedHead')
}
if (ledger.source.previousReleaseTag !== 'v0.1.0') {
  fail('previous release boundary must remain v0.1.0')
}
if (!Number.isInteger(ledger.source.commitCount) || ledger.source.commitCount < 1) {
  fail('source.commitCount must be a positive integer')
}
if (!Array.isArray(ledger.receipts.pullRequests) || ledger.receipts.pullRequests.length < 10) {
  fail('at least ten merged pull-request receipts are required for this candidate')
}

const receiptNumbers = new Set()
for (const receipt of ledger.receipts.pullRequests) {
  if (!Number.isInteger(receipt.number) || receiptNumbers.has(receipt.number)) {
    fail('pull-request receipt numbers must be unique integers')
  }
  receiptNumbers.add(receipt.number)
  if (receipt.url !== `https://github.com/frankxai/blue-life-commons/pull/${receipt.number}`) {
    fail(`pull-request receipt ${receipt.number} has the wrong URL`)
  }
  if (!/^[0-9a-f]{40}$/.test(receipt.mergeCommit)) {
    fail(`pull-request receipt ${receipt.number} must use a full merge SHA`)
  }
}

if (!changelog.includes(`Release candidate: \`${ledger.release.tag}\``)) {
  fail('CHANGELOG.md must identify the draft candidate')
}
if (!releaseNotes.includes(ledger.source.auditedHead)) {
  fail('release notes must name the audited SHA')
}
if (ledger.production.deploymentSha !== ledger.source.auditedHead) {
  fail('production deployment SHA must match the audited source')
}
if (ledger.production.deploymentStatus !== 'ready') {
  fail('production deployment must be recorded as ready')
}
if (ledger.production.changelogRoute.status !== 'missing-404') {
  fail('public changelog route must remain explicitly recorded as missing-404')
}
if (!packageManifest.private || ledger.packagePublishing.status !== 'not-applicable') {
  fail('private application must not expose a package publication path')
}
if (ledger.packagePublishing.manifestVersion !== packageManifest.version) {
  fail('package metadata version must match package.json')
}

if (!githubWorkflow.includes('workflow_dispatch:')) {
  fail('GitHub release workflow must be manual-only')
}
if (/^ {2}(push|pull_request|release|schedule):/m.test(githubWorkflow)) {
  fail('GitHub release workflow may not have an automatic trigger')
}
if (!githubWorkflow.includes('environment: github-release-draft')) {
  fail('GitHub release workflow must use its protected environment')
}
if (!githubWorkflow.includes('--draft')) {
  fail('GitHub release workflow may only create a draft')
}
if (githubWorkflow.includes('gh release edit') || githubWorkflow.includes('--latest')) {
  fail('GitHub release workflow may not publish or promote a release')
}

const assertCommitAncestor = (commit, descendant, message) => {
  try {
    execFileSync('git', ['cat-file', '-e', `${commit}^{commit}`], {
      cwd: root,
      stdio: 'ignore',
    })
    execFileSync('git', ['merge-base', '--is-ancestor', commit, descendant], {
      cwd: root,
      stdio: 'ignore',
    })
  } catch {
    fail(message)
  }
}

assertCommitAncestor(
  ledger.source.previousReleaseTag,
  ledger.source.auditedHead,
  'audited boundary must descend from the previous release tag',
)
assertCommitAncestor(
  ledger.source.auditedHead,
  'HEAD',
  'audited boundary must exist and be an ancestor of HEAD',
)
for (const receipt of ledger.receipts.pullRequests) {
  assertCommitAncestor(
    receipt.mergeCommit,
    ledger.source.auditedHead,
    `pull-request receipt ${receipt.number} is not in the audited boundary`,
  )
}

const mode = process.env.RELEASE_MODE ?? 'validate'
if (mode === 'github-release-draft') {
  if (ledger.release.status !== 'ready') fail('GitHub release requires release.status=ready')
  if (!ledger.approvals.humanReleaseApproval) {
    fail('GitHub release requires human approval')
  }
  if (!ledger.approvals.validationComplete) {
    fail('GitHub release requires completed validation')
  }
  if (process.env.RELEASE_VERSION !== ledger.release.version) {
    fail('workflow version must match ledger')
  }
  if (process.env.RELEASE_TARGET_SHA !== ledger.release.targetSha) {
    fail('workflow SHA must match ledger')
  }
}

process.stdout.write(
  `release contract ok: ${ledger.release.tag} ${ledger.release.status} at ${ledger.source.auditedHead}\n`,
)
