# Research Benchmark: Species Media And Ocean Knowledge Platforms

Last updated: 2026-07-05

This benchmark defines what Blue Life Commons should learn from adjacent biodiversity, media, and ocean-data platforms. It does not authorize copying images from those platforms. Image-level rights still need source, creator, license, credit, and permitted-surface review.

## Strategic Position

Blue Life Commons should become the approval and provenance layer for public ocean animal pages. The strongest move is not to beat every platform at its own job. The strongest move is to interoperate with them, curate from them, cite them, and publish only records that survive stricter public-use, welfare, and rights gates.

## Platform Lessons

| Platform | What it is best at | What Blue Life should adopt | What Blue Life should avoid | Official source |
|---|---|---|---|---|
| iNaturalist / Seek | Community observation and image-recognition discovery | Use as a discovery lane and observation signal, then re-check license, species match, and location sensitivity | Do not treat image search or observations as publication permission | <https://www.inaturalist.org/pages/seek_app> |
| GBIF Images API | Occurrence-linked image discovery and metadata | Use for candidate discovery, occurrence context, and data joins | Do not skip image-level creator/license review | <https://techdocs.gbif.org/en/openapi/images> |
| GBIF multimedia publishing | Multimedia metadata patterns | Align fields for creator, license, identifier, format, and Darwin Core style provenance | Do not rely on metadata presence as approval | <https://techdocs.gbif.org/en/data-publishing/multimedia-publishing> |
| Encyclopedia of Life | Species knowledge and trait aggregation | Use as a species knowledge and enrichment partner | Do not replace Blue Life review with broad aggregation | <https://naturalhistory.si.edu/research/eol> |
| OBIS | Marine occurrence data access | Use for marine distribution/context lanes and dataset references | Do not use occurrence data to expose sensitive live-animal locations | <https://obis.org/data/access/> |
| WoRMS | Marine taxonomy and AphiaID services | Normalize scientific names and identifiers before image intake | Do not let common-name ambiguity drive media ownership | <https://www.marinespecies.org/rest/> |
| Wild Me / Wildbook | Photo-identification and collaboration for individual animals | Learn from individual-ID workflows and partner science patterns | Do not claim individual identification unless reviewed tooling exists | <https://www.wildme.org/what-we-do.html> |
| Wildlife Insights | Camera-trap media upload, AI assistance, review, analysis, and public project workflows | Separate bulk intake, machine assist, human verification, analysis, and publishing | Do not publish AI-assisted media without human review | <https://www.wildlifeinsights.org/> |
| FishBase / SeaLifeBase | Fish species data and picture access routes | Use as a fish-specific enrichment and source-discovery lane | Do not assume picture reuse rights without image-level terms | <https://www.fishbase.se/hints.htm> |
| NOAA and official agencies | Institutional media and policy context | Prefer official/institutional media when image-level credit and reuse terms are clear | Do not assume third-party credited agency-page images are reusable | <https://www.fisheries.noaa.gov/national/about-us/website-policies-and-disclaimers> |

## What Competitors Teach

1. Broad platforms win at breadth, but breadth can blur rights, welfare, and public-use readiness.
2. Observation platforms are powerful discovery engines, not automatic publishing sources.
3. Taxonomy authority needs a dedicated service layer, especially for marine species.
4. Partner and institution media can raise trust when permission and credit are explicit.
5. Reviewer-only and public-safe data models should stay separate.
6. Blue Life's edge is the joined trust chain: species page, source, media, rights, welfare, render rule, and public route.

## Partner Strategy

| Partner lane | Use |
|---|---|
| Official agencies | Primary image upgrades, source cards, policy context, species pages |
| Museums and universities | Taxonomy, specimen/context media, expert review, collection links |
| NGOs and sanctuaries | Image grants, welfare-safe context, education routes |
| Photographers | High-quality species images with written usage grants |
| Open biodiversity platforms | Discovery, occurrence context, source metadata, candidate leads |
| Marine data platforms | Taxonomy, occurrence, ecosystem context, dataset cards |

## Product Implications

- Build source-partner registry entries with owner, source URL, contact route, license behavior, attribution needs, and blocked surfaces.
- Keep media intake as a formal issue or form, not a casual upload.
- Prefer official or partner grants for hero images when quality and terms are strong.
- Use source-card fallbacks when copying media is blocked.
- Make public visual ownership inspectable so users can see which image belongs to which animal.
- Add analytics around source opens and media details, not just page views.

## Sources

- iNaturalist Seek app: <https://www.inaturalist.org/pages/seek_app>
- GBIF Images API: <https://techdocs.gbif.org/en/openapi/images>
- GBIF multimedia publishing: <https://techdocs.gbif.org/en/data-publishing/multimedia-publishing>
- Encyclopedia of Life at Smithsonian National Museum of Natural History: <https://naturalhistory.si.edu/research/eol>
- OBIS data access: <https://obis.org/data/access/>
- WoRMS REST webservice: <https://www.marinespecies.org/rest/>
- Wild Me: <https://www.wildme.org/what-we-do.html>
- Wildlife Insights: <https://www.wildlifeinsights.org/>
- FishBase hints and picture guidance: <https://www.fishbase.se/hints.htm>
- NOAA Fisheries website policies and disclaimers: <https://www.fisheries.noaa.gov/national/about-us/website-policies-and-disclaimers>
