# Validation And Excellence Loop

Last updated: 2026-07-05

This loop keeps Blue Life Commons from becoming a pile of pages. Every release should improve coverage, usefulness, or trust while preserving source, rights, welfare, and production discipline.

## Weekly Loop

| Step | Action | Output |
|---|---|---|
| 1 | Review scorecard | Updated metrics and blockers |
| 2 | Review new issues | Classify species, media, source, partner, bug, or product experiment |
| 3 | Select one coherent change set | PR scope with owner and acceptance criteria |
| 4 | Build or curate | Artifact, media packet, UI change, or script update |
| 5 | Run local gates | Validation output captured in PR |
| 6 | Preview or production verify | Live route checks and visual QA when UI changes |
| 7 | Record learning | Scorecard, docs, issue, or decision note updated |

## Release Gates

| Gate | Required evidence |
|---|---|
| Source gate | Every public factual claim has an acceptable source |
| Ethics gate | Animal interaction, welfare, location, and individual-animal risks reviewed |
| Rights gate | Every public media record has creator, license, credit, approved surfaces, and blocked surfaces |
| Render gate | Public pages read approved render contract or public-safe manifest |
| Candidate safety gate | Reviewer-only candidate URLs do not feed public routes |
| Accessibility gate | Images have alt text and credit/license details are reachable |
| Cost gate | Blob/storage changes follow [`scale-and-cost-plan.md`](scale-and-cost-plan.md) |
| Deployment gate | Local checks pass before preview or production deploy |

## Local Checks

Run the smallest checks that match the change:

```bash
python scripts/validate_artifacts.py
python scripts/lint_content.py
python scripts/validate_species_media.py
npm run media:storage:check
npm run media:blob:check
npm run lint
npm run build
```

For docs-only product changes, `python scripts/lint_content.py`, `python scripts/validate_species_media.py`, and `git diff --check` are usually enough. Run broader checks when the change touches app code, media registries, manifests, scripts, routes, storage, or content artifacts.

## Public Route Verification

After a production or preview release, verify:

- `/`
- `/species`
- `/encyclopedia`
- `/media-intelligence`
- one species detail page from each affected guild
- `/sitemap.xml`

For UI changes, inspect desktop and mobile. For media changes, confirm the visual is the approved public visual and that source/credit/license details are visible or reachable.

## Product Quality Bar

Ship only when:

- the first read is clear
- the user can tell what is official, sourced, approved, or blocked
- no generated or candidate visual is mistaken for official identification evidence
- source/credit/license are visible near media
- welfare risks are handled directly
- metrics and next action are obvious

## Failure Modes To Watch

| Failure | Prevention |
|---|---|
| More animals, weaker sources | Source gate before page expansion |
| Better-looking images, unclear rights | Rights gate before promotion |
| Candidate photo leaks to public | Public-safe manifest and render contract only |
| Partner trust lost | Written image-level terms and visible credit |
| Cost creep | Batch derivatives, cache, avoid hot transforms, monitor transfer |
| Review sprawl | Issues and PRs carry handoff contract |
| Analytics without care | No sensitive animal location or unnecessary personal data |

## Sources

- Source policy: [`SOURCES.md`](../../SOURCES.md)
- Ethics policy: [`ETHICS.md`](../../ETHICS.md)
- Species media pipeline: [`species-media-pipeline.md`](../visual-system/species-media-pipeline.md)
- Media storage architecture: [`media-storage-architecture.md`](../visual-system/media-storage-architecture.md)
- Product scale and cost plan: [`scale-and-cost-plan.md`](scale-and-cost-plan.md)
