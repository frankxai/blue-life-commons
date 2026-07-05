# Success Metrics

Last updated: 2026-07-05

## North Star

Approved, source-backed animal knowledge used by real people without weakening animal welfare, factual accuracy, or media rights.

This is measured through a balanced scorecard. Coverage alone is not success if rights, source, welfare, or review quality is weak.

## Current Baseline

| Metric | Baseline | Source |
|---|---:|---|
| Tracked species pages | 31 | [`species-media-blob-manifest.json`](../../content/media/species-media-blob-manifest.json) |
| Approved primary images | 31 | [`species-media-blob-manifest.json`](../../content/media/species-media-blob-manifest.json) |
| Pending primary-image records | 0 | [`species-media-blob-manifest.json`](../../content/media/species-media-blob-manifest.json) |
| Approved media mirrored to Vercel Blob | 31 | [`species-media-blob-manifest.json`](../../content/media/species-media-blob-manifest.json) |
| Current approved original image storage | 54.142 MB | Calculated from `records[].storage.source_content_length` in [`species-media-blob-manifest.json`](../../content/media/species-media-blob-manifest.json) |
| Public candidate image URL leaks allowed | 0 | [`species-media-pipeline.md`](../visual-system/species-media-pipeline.md) |

## Scorecard

| Category | Metric | Target |
|---|---|---|
| Catalog coverage | Species pages with a registry record | 100 percent |
| Image coverage | Species pages with approved primary image or verified rich embed | 100 percent |
| Rights clarity | Approved images with creator, license, credit, allowed surfaces, and blocked surfaces | 100 percent |
| Source integrity | Public factual claims with source links | 100 percent |
| Welfare integrity | New media with ethics/location review notes | 100 percent |
| Candidate safety | Candidate direct URLs in public manifests | 0 |
| Partner quality | New approved images from official, institutional, NGO, or photographer grants | Increase month over month |
| Review throughput | Complete media-intake issues moved to review within 7 days | 90 percent |
| Release quality | Local validation checks before merge | 100 percent of releases |
| Production quality | `/species`, `/encyclopedia`, `/media-intelligence`, and `/sitemap.xml` verified after production deploy | 100 percent of production releases |

## 60-Day Targets

Target date: 2026-09-05.

| Outcome | Target |
|---|---:|
| Tracked species pages | 100 |
| Public-safe visual coverage | 100 percent |
| Official/partner/NGO media leads logged through issue template | 30 |
| New approved media from official/partner/NGO/photographer grants | 10 |
| Source/partner registry entries | 25 |
| Stale-source review candidates identified | 100 percent of approved media older than review window |
| Candidate direct URL leaks | 0 |

Targets are product goals, not current-state claims.

## Instrumentation Plan

| Event | Why it matters |
|---|---|
| `species_view` | Measures animal page demand by guild and source lane |
| `species_source_opened` | Shows whether users verify sources |
| `media_details_opened` | Shows whether rights and credit details are discoverable |
| `attribution_copied` | Measures creator/educator utility |
| `media_intake_started` | Measures partner/contributor intent |
| `media_intake_submitted` | Measures intake completion |
| `reviewer_source_opened` | Helps improve reviewer tooling |
| `public_route_verified` | Tracks post-release production QA |

Do not add analytics that collect sensitive live-animal location, unnecessary personal data, or unapproved media details.

## Review Rhythm

| Cadence | Owner | Output |
|---|---|---|
| Weekly | Product orchestrator | Scorecard update and blockers |
| Weekly | Media rights curator | New leads, approvals, blocks, partner asks |
| Biweekly | Welfare/ethics reviewer | Media and caption risk audit |
| Monthly | Platform engineer | Cost, storage, Blob transfer, derivative status |
| Monthly | Partner lead | Outreach response, grant pipeline, source gaps |

## Sources

- Media intelligence platform strategy: [`media-intelligence-platform-strategy.md`](../visual-system/media-intelligence-platform-strategy.md)
- Species media pipeline: [`species-media-pipeline.md`](../visual-system/species-media-pipeline.md)
- Species Blob manifest: [`species-media-blob-manifest.json`](../../content/media/species-media-blob-manifest.json)
- Source policy: [`SOURCES.md`](../../SOURCES.md)
- Ethics policy: [`ETHICS.md`](../../ETHICS.md)
