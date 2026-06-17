# Guide for NGOs and Conservation Organizations

Blue Life Commons is designed to make ocean science immediately useful for advocacy, grant writing, campaign work, and impact reporting — without requiring a research team to verify every claim.

---

## What Intelligence Is Available for Advocacy Work

The commons provides four categories of content directly relevant to conservation organizations:

**Welfare Assessments** — In-depth welfare status reports for critically threatened species: Hawaiian Monk Seal, North Atlantic Right Whale, Southern Resident Orca, and Vaquita. Each assessment covers population trajectory, primary stressors, welfare indicators, and conservation program effectiveness. These are written to grant-application standard and include Tier 1 (peer-reviewed) citations throughout.

**Species Threat Profiles** — 31 species pages covering cetaceans, sharks, turtles, corals, kelp, seagrass, and sirenians. Each page includes current IUCN status, primary threats ranked by impact, regional distribution, and active conservation programs. Updated as new IUCN assessments are published.

**Regional Briefings** — 8 regional ecosystem briefings (Antarctic, Azores, Galápagos, Great Barrier Reef, Monterey Bay, Ningaloo, Salish Sea, Wadden Sea) covering ecosystem health, key species assemblages, active threats, and ongoing conservation initiatives. Useful for campaign targeting and donor communication.

**Partner Profiles** — 5 profiled partner organizations: Mission Blue, Olive Ridley Project, Point Reyes National Seashore, Reef Check, and Whale and Dolphin Conservation. Useful for identifying collaboration opportunities and referencing peer programs.

**Start here:** [`content/welfare/`](../../content/welfare/) · [`content/species/`](../../content/species/) · [`content/regions/`](../../content/regions/)

---

## Using Guardian Briefings as Grant Evidence

Guardian agents in the [Ocean Intelligence System](https://github.com/frankxai/ocean-intelligence-system) generate regular ecosystem briefings grounded in both BLC knowledge artifacts and live connector data (NOAA Coral Reef Watch, IUCN Red List, OBIS occurrence data, Global Fishing Watch). These briefings are appropriate as supporting evidence in grant applications when:

1. The briefing cites a Tier 1 or Tier 2 source (see [`SOURCES.md`](../../SOURCES.md))
2. The underlying data connector is listed in the verified sources table ([`ECOSYSTEM_MAP.md`](../../ECOSYSTEM_MAP.md))
3. You preserve the attribution chain: BLC artifact → source citation → primary database

For grant applications, reference the artifact directly: `Blue Life Commons, "[Article Title]," CC-BY-4.0, https://github.com/frankxai/blue-life-commons/content/...`

---

## Claim Verification: Validating a Statistic

When you encounter an ocean statistic in media or partner communications, this is how to trace it back to a primary source using BLC and OIS:

1. **Find the relevant BLC artifact.** Search [`CATALOG.md`](../../CATALOG.md) by species, region, or topic. Read the artifact's `sources` metadata block — every claim maps to a numbered source.

2. **Check the source tier.** Open [`SOURCES.md`](../../SOURCES.md). Tier 1 = peer-reviewed journal article or IUCN assessment. Tier 2 = institutional report (NOAA, IPCC, IUCN supplemental). Tier 3 = community/NGO report (use with context).

3. **Query the live connector.** If the claim relates to a measurable signal (sea temperature, bleaching alert, species occurrence), query the relevant OIS connector directly to get the current value. Instructions at [`docs/personas/researcher-guide.md`](researcher-guide.md).

4. **If the claim is not in BLC,** open a GitHub issue. Our science reviewers will trace it and, if valid, add it as a sourced artifact.

---

## Impact Reporting Templates

BLC artifacts are structured to map directly into standard conservation impact reporting frameworks (GRI, IUCN SOS, GEF). Each species page includes:
- Baseline population data with date and source
- Current population trend (stable / declining / unknown)
- Primary threat category (IUCN threat classification)
- Active conservation interventions and program leads

For annual impact reports, you can query the OIS REST gateway to pull current connector readings (e.g., latest bleaching alert tier for a named reef region) alongside the static BLC baseline. Combine these into a before/after or trend narrative with full source attribution intact.

---

## How to Partner and Contribute Data Back

We actively seek contributions from conservation organizations with field data, monitoring datasets, or local expertise that is not yet represented in the commons.

**Contribution paths:**
- **Species page update** — If you have newer population data, field observations, or an updated threat assessment, open a PR against the relevant species page with your source documentation.
- **New welfare assessment** — If your organization monitors a species not yet covered, the [`/species-page`](https://github.com/frankxai/marine-agent-skills) skill in marine-agent-skills will scaffold a schema-valid draft from your notes.
- **Dataset card** — If your organization maintains a monitoring dataset that should be publicly referenced, contribute a dataset card under [`content/research/`](../../content/research/).
- **Partner profile** — Organizations doing consistent, evidence-based conservation work in the focus regions can be added to [`content/partners/`](../../content/partners/) via PR.

All contributions go through science review and ethics gating before merge. Your organization's name and contribution are permanently credited in the artifact metadata and the impact ledger.

**Contact and coordination:** Open an issue using the NGO Contribution template at [`.github/ISSUE_TEMPLATE/`](../../.github/ISSUE_TEMPLATE/).
