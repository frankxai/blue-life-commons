# PRD: Image-First Species Encyclopedia

Last updated: 2026-07-05

## Product Mandate

Build Blue Life Commons into the most useful public trust layer for ocean animal knowledge: a source-backed encyclopedia where every animal page has a correct image or safe rich embed, visible provenance, rights metadata, welfare review, and a contribution path for better media.

The product is not an image scraper. It is an approval, provenance, education, and partner-acquisition system.

## Audiences

| Audience | Primary job |
|---|---|
| Ocean-curious visitor | Understand an animal quickly and trust the image/source |
| Educator or creator | Reuse sourced learning material with credit and license clarity |
| Researcher | Verify claims, taxonomy, sources, and media provenance |
| NGO or partner | Grant better images or request a regional/species workflow |
| Contributor | Propose species, sources, corrections, or image candidates |
| Curator/reviewer | Approve only media that passes rights, species-match, and welfare gates |
| Agent/developer | Read machine-safe contracts without hallucinated claims or candidate leaks |

## Current Production Baseline

| Capability | Current state |
|---|---|
| Species pages tracked | 31 |
| Approved primary images | 31 |
| Pending primary-image records | 0 |
| Object storage | Vercel Blob public store for approved image mirrors |
| Public visual audit | `/media-intelligence` and the public explorer manifest expose ownership, rights, and source metadata |
| Reviewer boundary | Candidate URLs remain in reviewer-only workbench/dossier files |

Sources: [`media-intelligence-platform-strategy.md`](../visual-system/media-intelligence-platform-strategy.md), [`species-media-blob-manifest.json`](../../content/media/species-media-blob-manifest.json), [`species-media-pipeline.md`](../visual-system/species-media-pipeline.md).

## Problems To Solve

1. Ocean knowledge is fragmented across papers, databases, agencies, museums, NGOs, field programs, and open media platforms.
2. Image search results do not prove reuse rights, species match, welfare safety, or source quality.
3. Many contributors have useful media or knowledge but need a simple intake path that preserves review rigor.
4. Public pages need to make trust visible without becoming dense reviewer tooling.
5. The platform needs a repeatable way to add many more animals without pushing unreviewed media live.

## Product Principles

| Principle | Product behavior |
|---|---|
| Grounded or silent | If a claim or media right is not sourced, it does not publish |
| Image belongs to animal | Join by `artifact_id`, species page, source, and render contract, not filename |
| Public-safe by default | Public manifests omit candidate direct URLs and reviewer-only image fields |
| Rights are a product feature | Creator, license, credit, allowed surfaces, and blocked surfaces appear near public media |
| Welfare is part of quality | Captions, crops, maps, and metadata avoid unsafe interaction or sensitive live-animal leakage |
| Partners upgrade quality | Official, institutional, NGO, and photographer grants are preferred when terms are clear |

## Requirements

### Must Have

- Every species page has a registry record in `content/media/species-media-registry.yaml`.
- Every public species visual is selected by `species-media-render-contract.yaml` or the joined public-safe read model.
- Every approved image has source URL, original media URL when applicable, creator, credit line, license, rights status, approved surfaces, blocked surfaces, alt text, species-match basis, welfare notes, reviewer, and review date.
- Public pages show image provenance and license context in a reachable details area.
- Reviewer-only workbench and dossiers can inspect candidate media, but those files must never feed public species heroes, SEO images, or social crops.
- Media intake issues collect rights and welfare fields before a candidate enters approval work.
- Storage keeps GitHub for metadata and Vercel Blob for approved media mirrors.

### Should Have

- Missing-species queue split by `needs_page`, `needs_approved_image`, `needs_better_partner_image`, and `needs_rights_permission`.
- Partner/source registry for NOAA, USFWS, museums, sanctuaries, NGOs, GBIF, iNaturalist, EOL, OBIS, WoRMS, FishBase/SeaLifeBase, Wild Me, Wildlife Insights, Wikimedia Commons, and photographers.
- Batch derivatives for `thumb`, `card`, `hero`, `og`, and `full` image sizes after EXIF stripping and checksum logging are automated.
- Stale-source and stale-license review jobs.
- Analytics that measure whether users open sources, copy attribution, submit corrections, and complete media intake.

### Will Not Do Yet

- Do not claim automated species identification from user-uploaded photos.
- Do not publish generated art as an official species image.
- Do not ingest Google Images as a source of record.
- Do not expose precise sensitive locations, EXIF-derived location clues, or live individual animal locations.
- Do not move to Cloudflare R2 or another provider until the cost/performance triggers in [`scale-and-cost-plan.md`](scale-and-cost-plan.md) are met.

## Experience Requirements

| Surface | Expected first read |
|---|---|
| Species detail | This is the animal, this is the source-backed image, here is why it is safe to trust |
| Encyclopedia index | Browse animals by guild, image coverage, and source confidence |
| Media intelligence | Inspect coverage, rights, source lanes, visual ownership, and next curation work |
| Partner/contributor intake | Submit a useful image lead with the exact permission and welfare details curators need |
| Reviewer workbench | Decide what can be promoted, what is blocked, and which command applies |

## Roadmap

| Horizon | Outcome |
|---|---|
| Now | Lock the operating docs, issue intake, metrics, and release gates |
| Next 30 days | Add complete media-intake leads, build a missing-species queue, and promote new approved images only through the existing gate |
| Next 60 days | Reach 100 tracked animal/habitat-forming species pages with public-safe image or rich embed coverage |
| Next 90 days | Add partner/source registry, analytics events, image derivatives, and stale-source monitoring |

Dates are planning targets from 2026-07-05, not claims of completion.

## Acceptance Criteria

- `python scripts/validate_species_media.py` passes.
- `npm run media:blob:check` passes when Blob URLs or storage manifests change.
- Public species routes never render candidate direct image URLs.
- Every newly promoted image has visible credit, license, source, alt text, and approved/blocked surfaces.
- Every new factual claim in public docs or artifacts has an acceptable source.
- Every release updates the scorecard in [`success-metrics.md`](success-metrics.md).

## Sources

- Blue Life Commons strategy: [`STRATEGY.md`](../../STRATEGY.md)
- Public workflows: [`WORKFLOWS.md`](../WORKFLOWS.md)
- Species media pipeline: [`species-media-pipeline.md`](../visual-system/species-media-pipeline.md)
- Species visual explorer spec: [`species-visual-explorer-spec.md`](../visual-system/species-visual-explorer-spec.md)
- Media intelligence platform strategy: [`media-intelligence-platform-strategy.md`](../visual-system/media-intelligence-platform-strategy.md)
- Media storage architecture: [`media-storage-architecture.md`](../visual-system/media-storage-architecture.md)
