# Blue Life Commons Visual System

This folder defines the first reviewable visual asset system for Blue Life Commons and the Ocean Intelligence triad. It is intentionally split between exact assets and generative briefs:

- Vector/SVG assets are used for logos, diagrams, exact text, labels, and infographics.
- Grok-generated imagery is used for warmth, story, hero scenes, campaign frames, and animal/place atmospheres.
- Built-in `image_gen` imagery is used for selected comparison plates where stricter no-text and no-pseudo-UI constraints are useful.
- Science-sensitive content stays source-led. Generated imagery is never treated as biological evidence, a map, a chart, or a conservation claim.

## First read

Blue Life Commons is the public-good knowledge layer for ocean intelligence: sources, ethics, artifacts, and contribution workflows. Ocean Intelligence System is the guardian and connector layer that turns reviewed knowledge into briefings, dashboards, and alerts.

## Visual idea

The system should feel like a clear, caring ocean field station: warm enough to invite students, volunteers, creators, and coastal communities; rigorous enough for researchers, NGOs, and institutional partners.

The ownable idea is the **commons current**: sourced artifacts moving through review into guardians and public surfaces, like a current carrying care from people to places.

## Included assets

| Asset | Path | Purpose |
|---|---|---|
| Blue Life Commons mark | `assets/brand/blue-life-commons-mark.svg` | Primary vector logo application |
| One-color mark | `assets/brand/blue-life-commons-mark-one-color.svg` | Favicon, small mark, monochrome test |
| Blue Life Commons lockup | `assets/brand/blue-life-commons-lockup.svg` | README, deck, social header, sponsor docs |
| Ocean Intelligence lockup | `assets/brand/ocean-intelligence-system-lockup.svg` | Companion identity for the private/runtime layer |
| Artifact to guardian flow | `assets/infographics/commons-to-guardian-flow.svg` | Exact infographic for docs/decks |
| Ocean triad diagram | `assets/infographics/ocean-intelligence-triad.svg` | Trust, continuity, reach model |
| Grok prompt matrix | `docs/visual-system/grok-prompt-matrix.json` | 40 generation-ready image briefs |
| Grok handoff | `docs/visual-system/grok-handoff.md` | Batch execution instructions for Codex, Grok, or Antigravity |
| Imagegen batch 004 | `docs/visual-system/imagegen-batch-004.md` | Built-in image generation prompts, QA notes, and output paths |
| Infographic system | `docs/visual-system/infographic-system.md` | Rules for exact text, data, sources, and overlays |
| Species media pipeline | `docs/visual-system/species-media-pipeline.md` | Source priority, metadata, rights, and approval gate for official species visuals |
| Species visual explorer spec | `docs/visual-system/species-visual-explorer-spec.md` | Site surface spec for media coverage, provenance, and curation queue |
| Media intelligence platform strategy | `docs/visual-system/media-intelligence-platform-strategy.md` | Live media-intelligence surface, public visual audit board, competitive/partner benchmark, and expansion model for scaling approved animal images |
| Media storage architecture | `docs/visual-system/media-storage-architecture.md` | Vercel-Blob-first storage split, official-domain runbook, and later R2 scale option for animal image storage |
| Product excellence OS | `docs/product/README.md` | PRD, success metrics, user flows, benchmark, operating team, validation loop, and scale/cost plan for the animal encyclopedia |
| Species source routing | `content/media/species-media-source-routing.yaml` | Machine-readable review lanes, partner/grant targets, and reviewer actions |
| Species rich embeds | `content/media/species-media-rich-embeds.yaml` | Verified source-card fallbacks when approved primary images are absent |
| Species approval queue | `content/media/species-media-approval-queue.yaml` | Curator worksheet for promoting review-only candidates to approved primary media |
| Species render contract | `content/media/species-media-render-contract.yaml` | Public-site rule layer for approved images, source-card fallbacks, and non-public placeholders |
| Species curation workspace | `content/media/species-media-curation-workspace.yaml` | Batch-ranked curator action view for rechecks, fast-track candidates, attribution work, and blockers |
| Species public explorer manifest | `content/media/species-media-public-explorer-manifest.yaml` | Public-safe read model that omits candidate URLs while exposing render-contract visual slots and acquisition-plan next-action metadata |
| Species public explorer prototype | `content/media/public/species-visual-explorer-2026-07-03.html` | Static public-safe explorer prototype with 31 approved primary images, attribution metadata, acquisition filters, target-source filters, and no review-only thumbnails |
| Species storage policy | `content/media/species-media-storage-policy.yaml` | Vercel Blob store, pathname, upload, environment, and repo-boundary contract |
| Species storage manifest | `content/media/species-media-storage-manifest.yaml` | Generated pathname and derivative-slot plan for approved species images |
| Species Blob manifest | `content/media/species-media-blob-manifest.json` | Public Vercel Blob URLs for 31 uploaded approved species images |
| Species trace ledger | `content/media/species-media-trace-ledger.yaml` | Ownership proof layer linking each species page, public source card, render rule, curation lane, and review-only candidate ID |
| Species trace ledger review pack | `content/media/review-packs/species-media-trace-ledger-2026-07-03.md` | Human-readable trace matrix for checking which visual/source record belongs to which animal |
| Species acquisition plan | `content/media/species-media-acquisition-plan.yaml` | Public-safe next-action layer for official/public-domain review, open-license review, ethics-first review, and partner/NGO media outreach |
| Species acquisition review pack | `content/media/review-packs/species-media-acquisition-plan-2026-07-03.md` | Human-readable board showing approved-primary maintenance state and public-safe source/rights metadata for each species |
| Species approval dossiers | `content/media/species-media-approval-dossiers.yaml` | Reviewer-only evidence packets with candidate links, missing checks, safety notes, and promotion commands for each species |
| Species approval dossier review pack | `content/media/review-packs/species-media-approval-dossiers-2026-07-03.md` | Human-readable per-species approval packet; not a public site data source |
| Species Commons rights snapshots | `content/media/species-media-commons-rights-snapshots.yaml` | Reviewer-only Commons API metadata snapshots for staged Wikimedia candidates |
| Species Commons rights review pack | `content/media/review-packs/species-media-commons-rights-snapshots-2026-07-03.md` | Human-readable rights/species/ethics signal board for Commons candidates |
| Species outreach packets | `content/media/species-media-outreach-packets.yaml` | Public-safe partner/institution/NGO/open-license outreach packets with permission fields and request templates |
| Species outreach review pack | `content/media/review-packs/species-media-outreach-packets-2026-07-03.md` | Human-readable outreach board grouped by source target; omits candidate image URLs |
| Species approval workbench | `content/media/species-media-approval-workbench.yaml` | Reviewer-only joined operating view for candidate image inspection, Commons rights snapshots, approval blockers, outreach state, trace ownership, and promotion commands |
| Species approval workbench prototype | `content/media/review-packs/species-media-approval-workbench-2026-07-03.html` | Static reviewer workbench with candidate thumbnails and filters; not a public site data source |
| Evidence manifest | `docs/visual-system/design-loop-evidence-2026-06-26.json` | Loop trace and QA status for the original visual system pass |
| Species media evidence | `docs/visual-system/design-loop-evidence-2026-07-03-species-media.json` | Loop trace, QA status, and known risks for the species media pipeline |
| Media intelligence evidence | `docs/visual-system/design-loop-evidence-2026-07-04-media-intelligence.json` | Loop trace, QA status, and production surface proof for the media intelligence platform pass |
| Media storage evidence | `docs/visual-system/design-loop-evidence-2026-07-04-media-storage.json` | Loop trace, QA status, and architecture proof for the long-term media storage pass |
| Encyclopedia Blob evidence | `docs/visual-system/design-loop-evidence-2026-07-04-encyclopedia-blob.json` | Loop trace, QA status, Blob upload proof, and ship-readiness evidence for the image-first animal encyclopedia |

## Production stance

Generated visuals are drafts until inspected. Exact educational assets should be composed in SVG, Markdown, Figma, Canva, Remotion, or code from sourced repo content. Grok should not be asked to render readable captions, data labels, maps, dashboards, or factual claims inside the pixels.

Species media is tracked in `content/media/species-media-registry.yaml`. Official or partner/open-license media must be approved there before it becomes a primary species image; verified source cards in `content/media/species-media-rich-embeds.yaml` are safe fallbacks but do not grant image reuse. Curator decisions are staged in `content/media/species-media-approval-queue.yaml` before registry promotion, and `content/media/species-media-curation-workspace.yaml` ranks the work into practical review batches. The acquisition plan in `content/media/species-media-acquisition-plan.yaml` turns those batches into public-safe next actions for official review, open-license attribution, ethics-first checks, and partner/NGO outreach. The approval dossiers in `content/media/species-media-approval-dossiers.yaml` are reviewer-only packets for the actual image inspection and approval work. The Commons rights snapshots in `content/media/species-media-commons-rights-snapshots.yaml` add API-derived source metadata for staged Wikimedia candidates without treating that metadata as approval. The outreach packets in `content/media/species-media-outreach-packets.yaml` turn next actions into source-owner permission requests without exposing candidate image URLs. The approval workbench in `content/media/species-media-approval-workbench.yaml` is the joined reviewer-only surface for inspecting the candidate image, rights evidence, species match, source card, outreach target, trace key, missing checks, approval YAML starter, and exact promotion command for the same animal. Public pages follow `content/media/species-media-render-contract.yaml` or the sanitized `content/media/species-media-public-explorer-manifest.yaml`, so candidate photos stay out of species hero slots until approval. Generated assets remain supporting concept plates unless explicitly labeled otherwise.

## Review gates

- Factual claims trace to `SOURCES.md` rules.
- Animal depictions avoid harassment, unsafe proximity, feeding, touching, chasing, captivity glamor, or exact sensitive locations.
- Logo mark works in one color and at small sizes.
- Infographics use exact SVG/code text, not model-rendered text.
- Grok outputs require local file paths, prompt metadata, and QA notes before publication.
- Every species page has a registry record with media status, source candidates, and next action.
- Public species visuals come from the render contract, never directly from candidate image URLs.
- Reviewer-only workbench and dossier artifacts may contain candidate URLs, but they must stay marked `not_public_site_input`.
