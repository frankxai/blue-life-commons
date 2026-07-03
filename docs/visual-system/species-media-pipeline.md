# Species Media Pipeline

Last updated: 2026-07-03

## Outcome

Every species page needs a tracked primary visual or rich embed. The image must belong to the correct animal, carry rights and credit, and pass ethics review before it appears as official species media.

Generated key art can create warmth and story, but it remains supporting media unless a reviewer explicitly marks it as generated conceptual art. It is not identification evidence, a conservation-status source, or a substitute for official/partner/open-license media.

## Source Priority

1. **Official or institutional image**: NOAA, USFWS, NPS, sanctuary, museum, university, or government program media with image-level credit and rights. NOAA Fisheries says NOAA-created photos can be used with NOAA credit, but images credited to outside organizations or people need permission from those owners.
2. **Partner or NGO grant**: partner-provided image with a written license grant, approved surfaces, credit text, and any embargo/sensitivity notes.
3. **Open-license biodiversity media**: Wikimedia Commons, GBIF occurrence media, and iNaturalist/Open Data photos after per-image license, creator, attribution, and commercial-use checks.
4. **Rich embed/source card**: when image reuse is blocked, render the official source page as a cited rich card instead of copying the image.
5. **Generated/source plate**: optional supporting atmosphere only; never the primary official image.

Google Images can be used for discovery only. It is not a source of record, and a result cannot be reused unless the original page provides an acceptable image-level license or permission.

## Candidate Collection

Use the Wikimedia candidate collector for open-license scouting:

```bash
python scripts/collect_wikimedia_species_media.py --per-species 2 --out content/media/candidates/wikimedia-species-media-candidates-YYYY-MM-DD.yaml
```

The output is a review queue, not approved media. Promote a candidate only after checking the Commons file page, original source, image-level license, creator, credit text, species match, crop, alt text, and ethics/location risks.

Then build reviewer packets and stage the top candidate per species:

```bash
python scripts/build_species_media_review_pack.py --stage-registry-candidates
```

This moves records from `needed` to `candidate` only. It does not approve media or download assets.

Then build source-routing and partner/media-grant packets:

```bash
python scripts/build_species_media_source_packets.py
```

The source routing file gives each species a review lane: official/public-domain fast track, open-license attribution review, ethics note review, rich-embed fallback, or partner/new-candidate route. The grant queue turns unclear reuse or desired stronger images into a written-permission ask.

Verify rich source pages and Commons file pages:

```bash
python scripts/verify_species_media_links.py
```

Direct image URLs are excluded from the default link check to avoid Wikimedia upload rate limits; the visual board separately verifies that candidate thumbnails load in context.

Then build publication-safe source-card fallbacks:

```bash
python scripts/build_species_media_embed_fallbacks.py
```

This writes `content/media/species-media-rich-embeds.yaml` and a reviewer packet. A verified source card can appear as a public fallback when no approved primary image exists, but it does not grant permission to copy or crop images from the linked page.

Then build the curator approval queue:

```bash
python scripts/build_species_media_approval_queue.py
```

This writes `content/media/species-media-approval-queue.yaml` and a reviewer packet. It pre-fills candidate source fields, source-card fallback status, required checks, and the approved-primary metadata template, but all decisions remain `pending` until a curator fills reviewer/date/check fields.

Then build the curator action workspace:

```bash
python scripts/build_species_media_curation_workspace.py
```

This writes `content/media/species-media-curation-workspace.yaml` and `content/media/review-packs/species-media-curation-workspace-YYYY-MM-DD.md`. It ranks the queue into source-card rechecks, ethics-first records, official/public-domain fast-track candidates, open public-domain review, open-license attribution review, and partner-grant/replacement work. It does not approve media; it shows why promotion is still blocked and what a curator should do next.

After a curator marks a record `decision: approve_primary`, run a promotion dry run:

```bash
python scripts/promote_species_media.py --artifact-id species-blue-whale
```

If the report shows `promotable`, apply the promotion:

```bash
python scripts/promote_species_media.py --artifact-id species-blue-whale --apply
python scripts/validate_species_media.py
```

The promotion command refuses to update the registry unless every required check is true, reviewer/date fields are set, the candidate still matches the registry, and approved-primary metadata is complete. It writes a promotion report under `content/media/review-packs/`.

For visual QA and curation, export the site data and build the local board:

```bash
python scripts/export_species_media_site_data.py
python scripts/build_species_media_render_contract.py
python scripts/export_species_media_site_data.py
python scripts/build_species_media_curation_workspace.py
python scripts/sync_species_page_media.py --write
python scripts/build_species_media_trace_ledger.py
python scripts/build_species_media_acquisition_plan.py
python scripts/build_species_media_approval_dossiers.py
python scripts/build_species_media_commons_rights_snapshots.py
python scripts/build_species_media_outreach_packets.py
python scripts/build_species_media_approval_workbench.py
python scripts/build_species_media_visual_board.py
python scripts/build_species_media_public_explorer.py
```

The render contract writes `content/media/species-media-render-contract.yaml`, which tells public site surfaces what they may render today: approved primary image, verified source-card fallback, source-card recheck placeholder, review-only candidate placeholder, or no public visual. The second site-data export attaches that contract to each frontend-ready record.

The page sync command writes a compact `media` block into each `content/species/**/*.md` artifact. That block points to the central registry, render contract, and public explorer record for the same `artifact_id`, exposes the verified source-card embed URL, mirrors approval check counts, and mirrors approved primary image fields after the promotion tool approves a real primary image.

The trace ledger writes `content/media/species-media-trace-ledger.yaml` and `content/media/review-packs/species-media-trace-ledger-YYYY-MM-DD.md`. It is the machine-checkable "belongs to the right animal" proof layer: one ownership key joins `artifact_id`, species page path, source-card fallback, render contract, public explorer record, curation lane, and review-only candidate ID. It intentionally omits direct candidate image URLs and Commons file-page URLs.

The acquisition plan writes `content/media/species-media-acquisition-plan.yaml` and `content/media/review-packs/species-media-acquisition-plan-YYYY-MM-DD.md`. It is the public-safe next-action layer: one row per species says whether the next move is official/public-domain image-level review, open-license attribution review, open public-domain review, ethics-first review, or partner/NGO media-grant outreach. It keeps candidate direct URLs and Commons file pages out of public-safe metadata.

The approval dossier builder writes `content/media/species-media-approval-dossiers.yaml` and `content/media/review-packs/species-media-approval-dossiers-YYYY-MM-DD.md`. It is reviewer-only and may include candidate file pages and direct image URLs. Use it as the per-species evidence packet for image inspection, rights/credit verification, missing approval checks, missing approved-primary fields, safety notes, and promotion commands. Do not use it as a public website read model.

The Commons rights snapshot builder writes `content/media/species-media-commons-rights-snapshots.yaml` and `content/media/review-packs/species-media-commons-rights-snapshots-YYYY-MM-DD.md`. It refreshes staged Wikimedia Commons candidates from the Commons API, compares file title, file page, direct URL, rights status, creator/credit metadata, and species text signals against the registry, and records automated ethics/location flags. It is reviewer-only, contains candidate URLs, and is not approval; it gives curators stronger evidence for the approval queue.

The outreach packet builder writes `content/media/species-media-outreach-packets.yaml` and `content/media/review-packs/species-media-outreach-packets-YYYY-MM-DD.md`. It is the operational layer for asking the right institution, NGO, partner, or open-license publisher for image-level terms. It groups species by source domain, records request type, required permission fields, blocked surfaces, and email-ready message templates. It omits candidate direct image URLs and Commons file pages, and it never approves media.

The approval workbench builder writes `content/media/species-media-approval-workbench.yaml` and `content/media/review-packs/species-media-approval-workbench-YYYY-MM-DD.html`. It is reviewer-only and joins the approval queue, approval dossiers, Commons snapshots, acquisition plan, outreach packet, public render boundary, and trace ledger into one operating view. It may show candidate thumbnails, candidate file pages, and direct image URLs, but every record is marked `not_public_site_input`, `reviewer_only`, and `candidate_public_use: false`. Use it to answer "does this image belong to the right animal, can we reuse it, what is still missing, and what exact promotion command applies?" without opening seven YAML files.

The generated HTML board embeds candidate thumbnails and official-source links for review, but every candidate remains marked review-only. Its render-strategy filter shows what a public page would be allowed to use without accidentally making a candidate photo the species identity image.

The public explorer builder writes `content/media/species-media-public-explorer-manifest.yaml` plus `content/media/public/species-visual-explorer-YYYY-MM-DD.html`. This is the safer handoff for website implementation: it omits candidate file pages, direct image URLs, candidate titles, and thumbnail fields, then renders only the public visual selected by the render contract. It also joins the acquisition plan so public cards can filter by acquisition lane and target source family while showing the next safe curator action. The 2026-07-03 manifest renders 31 approved primary images, has 31 hero-ready records, needs 0 additional primaries, and keeps all 31 review-candidate records blocked from public use.

## Required Metadata

Each approved primary image needs:

- `artifact_id` and `species_page`
- common name, scientific name, and species slug
- `approved_asset_id` and local path or approved external embed URL
- source URL and original image URL when different
- creator/photographer
- credit line
- license and rights status
- permitted surfaces
- blocked surfaces
- alt text
- species-match basis, such as official caption, taxon page, expert review, or partner assertion
- ethics notes, including no unsafe proximity or sensitive live-animal location leakage
- QA status and reviewer/date

## File And Asset Naming

Use stable IDs that cannot drift across species:

```text
species/<group>/<species-slug>/<asset-role>-<source>-<sequence>.<ext>
```

Examples:

```text
assets/species/cetaceans/blue-whale/primary-noaa-001.webp
assets/species/turtles/hawksbill-turtle/primary-wikimedia-001.webp
assets/species/sharks-rays/reef-manta-ray/embed-manta-trust-001.json
```

Every copied asset needs a registry record before use. Do not place loose files in `assets/` without an `artifact_id`, `species_page`, source, and rights trail.

## Site Explorer Behavior

The website should expose a visual explorer backed by `content/media/species-media-registry.yaml`:

- Species cards show primary media status: `approved`, `candidate`, `needed`, `rich_embed_only`, or `blocked`.
- Filters include taxon group, source route, source-card fallback status, source family, rights status, QA status, and supporting generated assets.
- The inspector panel shows source URL, license, creator, credit, approved surfaces, and species-match basis.
- Public species surfaces follow `content/media/species-media-render-contract.yaml` or the joined `render_contract` object in `content/media/species-media-site-data.json`.
- Curator dashboards can follow `content/media/species-media-curation-workspace.yaml` for batch order, blockers, and per-species next actions.
- Acquisition dashboards can follow `content/media/species-media-acquisition-plan.yaml` for public-safe next actions without exposing review-only candidate URLs.
- Public explorer dashboards can follow `content/media/species-media-public-explorer-manifest.yaml` when they need both render-contract visual slots and acquisition-plan lane/target metadata in one public-safe read model.
- Curator approval dashboards can follow `content/media/species-media-approval-dossiers.yaml` only in reviewer-only contexts because it intentionally includes candidate file pages and direct image URLs.
- Commons rights review dashboards can follow `content/media/species-media-commons-rights-snapshots.yaml` only in reviewer-only contexts because it includes candidate URLs and API-derived file metadata.
- Outreach dashboards can follow `content/media/species-media-outreach-packets.yaml` to group official, partner, NGO, or open-license permission asks by source target without exposing review-only candidate image URLs.
- Reviewer approval dashboards can follow `content/media/species-media-approval-workbench.yaml` only in restricted contexts because it intentionally contains candidate image URLs, approval YAML starters, rights snapshots, and promotion commands.
- Species pages use `approved` primary media first. If absent, use a verified source-card fallback, not an unapproved candidate photo or generated art.
- Generated assets display a visible "concept/supporting" label in editorial surfaces.

The current static prototype is `content/media/review-packs/species-media-visual-board-YYYY-MM-DD.html`. It is generated from `content/media/species-media-site-data.json`, which joins `content/media/species-media-source-routing.yaml`, `content/media/species-media-rich-embeds.yaml`, `content/media/species-media-approval-queue.yaml`, and `content/media/species-media-render-contract.yaml`. The curation workspace is the companion operating view for batch review; treat both as reviewer tools, not public species pages.

The current public-safe prototype is `content/media/public/species-visual-explorer-YYYY-MM-DD.html`, generated from `content/media/species-media-public-explorer-manifest.yaml`. Treat that manifest as the public website read model until the application renders the same contract directly. It is safe for approved primary image cards and public attribution metadata, but it still does not authorize blocked surfaces such as merchandise, paid ads without extra rights review, or social crops without visible credit.

## Review Gate

Approval requires:

1. Image-level rights are known and compatible with the intended surface.
2. The species match is grounded in a source caption, taxon page, partner assertion, or reviewer note.
3. The depiction does not encourage unsafe approach, feeding, touching, baiting, chasing, crowding, or captivity glamour.
4. Sensitive location clues are absent or generalized.
5. Crop, alt text, credit, and mobile/desktop behavior are checked.
6. `python scripts/validate_species_media.py` passes.

## Source Notes

- NOAA Fisheries copyright policy: <https://www.fisheries.noaa.gov/national/about-us/website-policies-and-disclaimers>
- NOAA digital media policy: <https://sos.noaa.gov/copyright/>
- GBIF occurrence image API: <https://techdocs.gbif.org/en/openapi/images>
- GBIF multimedia publishing guidance: <https://techdocs.gbif.org/en/data-publishing/multimedia-publishing>
- Wikimedia Commons API: <https://commons.wikimedia.org/wiki/Commons:API>
- iNaturalist API docs: <https://api.inaturalist.org/v2/docs/>
