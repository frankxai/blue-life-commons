# Releasing Blue Life Commons

Blue Life Commons separates public knowledge, repository releases, package
metadata, and production deployments. One never silently authorizes another.

## Current truth

- `CHANGELOG.md` is the curated repository change history.
- `docs/releases/release-ledger.json` is the machine-readable release state.
- `docs/releases/v0.2.0.md` is a draft candidate, not a published release.
- `v0.1.0` is the only existing Git tag and GitHub release.
- Production is currently verified at the candidate boundary SHA.
- The public site does not yet have a `/changelog` route.
- `package.json` is private. Its `1.0.0` value is application metadata, not a
  published package or repository-release receipt.

## Meaningful-update rhythm

Update the changelog when a reader, contributor, steward, reviewer, operator,
privacy boundary, or production truth materially changes. Batch small internal
chores into the next meaningful entry. Weekly audits are useful for finding
missing receipts; a calendar week alone is not a reason to invent a public
announcement.

Every candidate must name immutable proof: an audited source SHA, the previous
release boundary, merged pull requests, production deployment state, validation
results, and known gaps. Scientific or conservation claims still follow
`SOURCES.md`, `ETHICS.md`, and the repository's review-state rules.

## Release boundary semantics

The candidate SHA is the immutable product boundary being blessed. Release
governance commits may land on `main` after that boundary. The draft workflow
therefore requires the candidate to be an ancestor of current `main`; it does
not retarget the release to a newer unaudited commit.

## GitHub release path

1. Update `CHANGELOG.md`, the candidate notes, and the release ledger.
2. Run `npm run audit:release` and the normal repository gates.
3. Merge the release-governance change through a reviewed pull request.
4. In a follow-up reviewed change, set `release.status` to `ready`,
   `validationComplete` to `true`, and `humanReleaseApproval` to `true`.
5. Configure required reviewers on the `github-release-draft` environment.
6. Manually run **Draft GitHub release** from `main` with the ledger's exact
   version and candidate SHA.
7. Review the generated draft on GitHub. Publishing remains a human action.

The workflow rejects a non-main run, a non-ancestor or mismatched SHA, a tag at
another commit, an unapproved ledger, or a version mismatch. Safe retries may
reuse the exact annotated tag or draft. The workflow never publishes a release.

## Production and public changelog

Creating a GitHub release does not deploy the website. Production follows the
existing Vercel Git integration and must be verified independently. Before a
push intended to build a preview or production deployment, check that no recent
deployment for this project is still building.

A future `/changelog` page should consume curated repository release data, link
to relevant records and governance surfaces, and include useful structured
metadata. It must pass the Premium Intelligence Web OS, responsive,
accessibility, performance, and visual QA gates before being described as live.

## References

- [GitHub generated release notes](https://docs.github.com/en/repositories/releasing-projects-on-github/automatically-generated-release-notes)
- [GitHub deployment environments](https://docs.github.com/en/actions/reference/workflows-and-actions/deployments-and-environments)
- [Semantic Versioning](https://semver.org/)
