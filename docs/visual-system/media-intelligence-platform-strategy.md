# Media Intelligence Platform Strategy

Last updated: 2026-07-04

## Outcome

Blue Life Commons should become the public trust layer for animal visuals: every species page gets an approved primary image, visible provenance, source context, rights metadata, welfare review, and a route for better partner media over time.

It should not try to replace the major biodiversity platforms. The useful move is to interoperate with them, curate from them, and publish only the image records that survive a stricter public-use contract.

## Current Production Baseline

- Current corpus: 31 species pages.
- Current approved primary images: 31.
- Current production status: species detail pages, species cards, catalog cards, and social metadata render through the approved media guard.
- Current media intelligence surface: `/media-intelligence` renders live coverage counts, guild and rights summaries, a public visual audit board, competitor/partner lessons, source lanes, and the expansion loop.
- Current visual audit board: every approved primary image is mapped to its owning animal page, guild, source host, rights status, license, asset id, and source page link.
- Current public safety stance: candidate and reviewer-only media URLs are blocked from public rendering.

## Competitive And Partner Landscape

| Platform | What it is best at | What Blue Life should learn | Source |
| --- | --- | --- | --- |
| iNaturalist / Seek | Community observations and image recognition from community-identified observations. | Use as a discovery and observation-signal lane, then re-check image rights, species match, welfare context, and location sensitivity before publication. | <https://www.inaturalist.org/pages/seek_app> |
| GBIF | Occurrence data and occurrence-linked multimedia infrastructure. | Use for broad candidate discovery and occurrence context, but keep image-level creator, license, publisher, and confirmation state in Blue Life. | <https://techdocs.gbif.org/en/openapi/images> |
| GBIF multimedia publishing | Media metadata patterns, including creator/license fields and Darwin Core multimedia extensions. | Align the Blue Life registry with creator, license, identifier, format, and extension-style provenance fields. | <https://techdocs.gbif.org/en/data-publishing/multimedia-publishing> |
| Encyclopedia of Life | Species knowledge and trait data across a very large species corpus. | Use EOL as a species-page/trait enrichment partner; Blue Life adds approved visuals, ocean action context, and welfare framing. | <https://naturalhistory.si.edu/research/eol> |
| OBIS | Marine occurrence records from thousands of datasets and marine-scale access paths. | Use OBIS for ocean occurrence and signal context, not as an image-rights shortcut. | <https://obis.org/data/access/> |
| WoRMS | Marine taxonomy and AphiaID services. | Normalize marine species names and identifiers before image intake. | <https://www.marinespecies.org/rest/> |
| Wild Me / Wildbook | Individual animal photo-identification and collaboration from researcher/public imagery. | Partner where individual identification matters; keep Blue Life focused on species-page media approval and public publishing. | <https://www.wildme.org/what-we-do.html> |
| Wildlife Insights | Camera-trap upload, machine learning identification, analysis, and project exploration. | Borrow the workflow lesson: bulk intake, machine assist, human verification, analysis, and public publishing should be separate stages. | <https://www.wildlifeinsights.org/> |
| FishBase / SeaLifeBase | Fish species data and picture access routes. | Treat as fish-specific source/candidate lane; verify license and attribution per image before public use. | <https://www.fishbase.se/hints.htm> |
| NOAA, USFWS, museums, sanctuaries | Official or institutional images, often with high trust and clear context. | Prefer these for primary images when image-level rights and credit are clear. | <https://www.fisheries.noaa.gov/national/about-us/website-policies-and-disclaimers> |

## Platform Position

Blue Life Commons is strongest when it is:

- An approval and provenance layer, not another unreviewed image search.
- A publishing layer, not a raw media warehouse.
- A bridge across official media, Commons media, occurrence networks, partner grants, and welfare review.
- A source of public, reusable species cards that cite source, rights, credit, and blocked surfaces.
- A public visual audit board that lets contributors inspect which image belongs to which animal before proposing replacements.
- A contributor workflow where missing animals and better images become reviewable queues, not ad hoc uploads.

## Source Priority

1. Official or institutional media with image-level credit and rights.
2. Partner or NGO media grants with written surface permissions.
3. Wikimedia Commons and other open-license images after per-file metadata review.
4. GBIF/iNaturalist occurrence media after publisher/license confirmation and location review.
5. FishBase/SeaLifeBase media for fish after image-level license and attribution checks.
6. Source-card fallback when image reuse is not confirmed.
7. Generated visual material only as supporting conceptual media, never primary identification evidence.

Google Images remains discovery-only. It can help find original pages, but it is not a source of record and cannot be used as image permission.

## More Animals And Images Live

The scale path is a repeatable six-step loop:

1. Normalize the animal record.
   Join common name, scientific name, taxon identifier, artifact id, and page path before collecting media.

2. Collect candidates as reviewer-only data.
   Pull source pages, file pages, thumbnails, and metadata into a private review record. Do not expose candidate image URLs on public pages.

3. Score source and rights confidence.
   Rank official/public-domain, open-license, partner-grant, and blocked/needs-permission lanes by license clarity, source quality, species match, and welfare risk.

4. Approve one primary image.
   Promote only after rights, credit, alt text, crop, species-match basis, and sensitive-location checks are complete.

5. Publish with provenance.
   Render image, creator, license, source, original, approved surfaces, blocked surfaces, and last-review state.

6. Refresh continuously.
   Track stale images, missing taxa, better partner replacements, source changes, and future species pages as an operating queue.

## What Is Live Now

- A public `/media-intelligence` route for current coverage, benchmark lessons, source lanes, a visual audit board, and the expansion loop.
- Navigation from the primary header and footer so reviewers and partners can reach the media platform surface.
- Live server-side counts from the same species/media contract used by production species pages.
- A public grid of all approved animal images with page ownership, source host, rights status, license, asset id, and source link.

## What To Build Next

- A contributor media submission template that requests source URL, original URL, creator, license, permission terms, species-match basis, and sensitive-location notes.
- A source-partner registry for NOAA, USFWS, Wikimedia Commons, GBIF, iNaturalist, EOL, OBIS, WoRMS, FishBase, Wild Me, Wildlife Insights, NGOs, and photographers.
- A missing-species queue that separates "needs page", "needs approved image", "needs better partner image", and "needs rights permission".
- A reviewer dashboard that never leaks candidate image URLs into public manifests.
- Automated stale-source checks for approved images and source-card fallbacks.

## Guardrails

- Do not publish any image whose source, creator, license, and allowed surfaces are unclear.
- Do not publish candidate or reviewer-only direct image URLs.
- Do not use generated art as an official species image.
- Do not infer image rights from the existence of a photo in search results, GBIF, iNaturalist, EOL, or a partner page.
- Do not expose precise live-animal locations, sensitive habitats, or welfare-risk context through captions, maps, EXIF text, or crop choices.
- Do not claim Blue Life identifies animals from photos unless a reviewed identification workflow is actually implemented and disclosed.

## Best-Platform Answer

The best platform is not the one with the most copied images. It is the one that makes animal visuals trustworthy and useful:

- correct species
- visible source
- visible creator and license
- welfare-safe context
- source-backed science
- contributor path for better media
- partner path for image grants
- public rendering that never leaks unapproved candidate data

That is the gap Blue Life Commons can own.
