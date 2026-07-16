# Product Excellence Operating System

Last updated: 2026-07-05

Blue Life Commons now has an image-first species encyclopedia, a media intelligence surface, a rights-aware Blob storage boundary, and a public-safe visual explorer contract. This folder turns that production baseline into an operating system for product leadership, user flows, metrics, partner acquisition, validation, and scale decisions.

The rule is simple: grow the catalog without weakening trust. A species page is useful only when the animal, source, image, rights, welfare context, and next action all stay connected.

## Current Baseline

| Surface | State | Source |
|---|---|---|
| Species encyclopedia | 31 tracked species pages with approved primary images | [`media-intelligence-platform-strategy.md`](../visual-system/media-intelligence-platform-strategy.md) |
| Public media coverage | 31 approved primary images, 0 pending primary-image records | [`species-media-blob-manifest.json`](../../content/media/species-media-blob-manifest.json) |
| Public routes | `/species`, `/encyclopedia`, and `/media-intelligence` render through the approved media guard | [`species-media-pipeline.md`](../visual-system/species-media-pipeline.md) |
| Storage | Vercel Blob stores approved species image mirrors; GitHub stores metadata and review trail | [`media-storage-architecture.md`](../visual-system/media-storage-architecture.md) |
| Official domain | Not connected until ownership, DNS, and Vercel verification are complete | [`media-storage-architecture.md`](../visual-system/media-storage-architecture.md) |

## Operating Documents

| Document | Purpose |
|---|---|
| [`prd-species-encyclopedia.md`](prd-species-encyclopedia.md) | Product requirements, scope, non-goals, roadmap, and acceptance criteria |
| [`success-metrics.md`](success-metrics.md) | North star, scorecard, targets, and instrumentation plan |
| [`user-flows.md`](user-flows.md) | Visitor, researcher, contributor, reviewer, partner, and release flows |
| [`research-benchmark-2026-07.md`](research-benchmark-2026-07.md) | Competitive and partner landscape, with official source links |
| [`operating-team.md`](operating-team.md) | Role design, handoffs, RACI, and agent execution model |
| [`validation-and-excellence-loop.md`](validation-and-excellence-loop.md) | Weekly operating cadence, gates, QA, and release discipline |
| [`scale-and-cost-plan.md`](scale-and-cost-plan.md) | Vercel-first scale plan, cost model, optimization path, and migration triggers |
| [`media-economics-and-roi.md`](media-economics-and-roi.md) | Full media economics, budgets, ROI, nonprofit/commercial model, tech ladder |
| [`metrics/monthly-cost-ledger.TEMPLATE.md`](metrics/monthly-cost-ledger.TEMPLATE.md) | Monthly spend + inventory ledger template |

## Decision Rules

1. Source truth before scale. Every factual claim follows [`SOURCES.md`](../../SOURCES.md).
2. Animal welfare before engagement. Every visual and workflow follows [`ETHICS.md`](../../ETHICS.md).
3. Approved media before public rendering. Public routes read the render contract, not reviewer-only candidates.
4. Partner images need written image-level terms before use.
5. Google Images is discovery only. The source of record is the original page or written permission grant.
6. Vercel Blob stays first until transfer, derivative generation, partner archives, or video make a second media provider worth the complexity.
7. Every growth move should create an artifact, issue, PR, review record, or source packet.

## 30-Day Execution Loop

| Week | Product move | Validation |
|---|---|---|
| 1 | Tighten intake: use the media intake issue template for every official, NGO, partner, or photographer lead | At least 10 complete media leads with rights fields |
| 2 | Expand target species queue by guild, source lane, and partner target | Missing-species queue has page/image/outreach state |
| 3 | Promote new approved media only after rights, species match, alt text, crop, and welfare checks pass | `python scripts/validate_species_media.py` |
| 4 | Publish one coherent preview or production release with scorecard update | Build passes, public routes checked, scorecard updated |

## Sources

- Repo strategy: [`STRATEGY.md`](../../STRATEGY.md)
- Public workflows: [`WORKFLOWS.md`](../WORKFLOWS.md)
- Species media pipeline: [`species-media-pipeline.md`](../visual-system/species-media-pipeline.md)
- Media intelligence strategy: [`media-intelligence-platform-strategy.md`](../visual-system/media-intelligence-platform-strategy.md)
- Media storage architecture: [`media-storage-architecture.md`](../visual-system/media-storage-architecture.md)
- Deep Time + living media scale strategy: [`deep-time-media-scale-strategy.md`](../deep-time-media-scale-strategy.md)
- Species Blob manifest: [`species-media-blob-manifest.json`](../../content/media/species-media-blob-manifest.json)
