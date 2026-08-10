# Release-foundation audit — 2026-08-10

## Outcome

Blue Life Commons had one public GitHub release (`v0.1.0`) and 27 commits of
unreleased mainline work. This foundation records that work as a guarded
`v0.2.0` candidate without creating a tag, publishing a release, changing
content review state, or promoting production.

## Verified evidence

- Previous release: `v0.1.0`, published 2026-06-16.
- Audited main boundary: `8c78ce83b83696e565900c71289f9c7e31e85767`.
- Vercel production deployment: `dpl_6FPex1nwQjXRx4StZrXQXKCDniiX`, `READY`,
  at the same SHA.
- Canonical domain: <https://bluelifecommons.org> (`200`).
- Robots: <https://bluelifecommons.org/robots.txt> (`200`).
- Sitemap: <https://bluelifecommons.org/sitemap.xml> (`200`).
- Changelog route: <https://bluelifecommons.org/changelog> (`404`, `noindex`).
- Existing open PR #27 was inspected; its CI/package changes do not overlap this
  release-governance lane.

## Decisions

- Use `v0.2.0` because `v0.1.0` is the only published repository release and
  this is the next reviewed product boundary. The private package's `1.0.0`
  metadata is not treated as a release receipt.
- Keep the candidate fixed to the deployed product SHA. Later governance-only
  commits may follow it on `main` without silently expanding the release scope.
- Require protected-environment review and explicit ledger approvals before a
  manual workflow can create an annotated tag and draft GitHub release.
- Keep release publication, npm publication, and production promotion outside
  the workflow.

## Validation receipt

- Release-ledger contract: passed.
- Simulated publication mode: blocked as designed while status is `draft` and
  human approval is false.
- YAML parse: passed for the release configuration and both workflows.
- Public transparency: 6/6 tests passed.
- Artifact schema validation: 84/84 artifacts passed.
- Integrity lint: 0 errors and 0 warnings.
- Catalog regeneration check: current.
- `git diff --check`: passed.
- The public-truth and media-guard contracts exercise Linux filename and
  symlink behavior that cannot run fully in this Windows session. Their failing
  paths are unchanged from `origin/main`; Ubuntu CI remains the authoritative
  run for those cases.
- Local build: held by the machine-performance gate (RAM reserve and active
  task-runtime budget). The Vercel preview is the build authority for this lane.

## Open gap

The public site has no changelog page. That should be a separate visual-product
change with a page/scene brief, structured metadata, responsive inspection,
accessibility checks, performance validation, and the repository's visual QA
gate. Until then, `CHANGELOG.md` is the public source of truth.
