---
title: "Marine Protected Areas"
description: "Designated ocean zones with restrictions on extractive use, ranging from fully no-take reserves to multiple-use areas; currently protecting ~8% of ocean surface against a 30x30 target of 30% by 2030."
type: practice-guide
status: published
scope:
  regions:
    - global
  tags:
    - "mpa", "no-take-zone", "30x30", "ocean-governance", "conservation-planning", "fisheries"
sources:
  - url: "https://www.protectedplanet.net/en"
    title: "Protected Planet / WDPA — World Database on Protected Areas"
    accessed: "2026-06-17"
  - url: "https://missionblue.org/hope-spots/"
    title: "Mission Blue Hope Spots"
    accessed: "2026-06-17"
  - url: "https://www.iucn.org/theme/marine-and-polar/our-work/marine-protected-areas"
    title: "Marine Protected Areas — IUCN"
    accessed: "2026-06-17"
  - url: "https://www.marineconservation.org/"
    title: "Marine Conservation Institute"
    accessed: "2026-06-17"
review:
  ethics: required
  science: required
license: CC-BY-4.0
contributors: []
created: "2026-06-17"
updated: "2026-06-17"
---

# Marine Protected Areas

## What MPAs are

A Marine Protected Area (MPA) is a clearly defined geographic space recognised, dedicated, and managed through legal or other effective means to achieve long-term conservation of nature. The term covers a wide spectrum of protection levels:

| MPA Type | Protection Level | Allowed Activities |
|---|---|---|
| **Fully Protected / No-Take Reserve** | Highest | No extractive use; science only |
| **Highly Protected** | High | Very limited take; mostly non-extractive use |
| **Strongly Protected** | Medium-high | Limited fishing; mostly non-extractive |
| **Partially Protected** | Medium | Multiple use with significant restrictions |
| **Lightly Protected** | Low | Few restrictions; mainly regulatory framework |
| **Minimally Protected** | Lowest | Primarily zoning designation with few active restrictions |

This distinction matters: an MPA that exists only on paper — with no enforcement or management — provides no measurable ecological benefit. The ecological evidence strongly supports no-take or highly protected zones; partially and lightly protected MPAs show weaker or absent ecological benefits.

## Why MPAs work: the evidence

A meta-analysis of over 100 fully or highly protected no-take zones found that fish biomass inside well-enforced MPAs is **4–5x higher** than in adjacent unprotected areas. This "density effect" generates **spillover** — adult fish and larvae disperse out of the MPA into surrounding fishing grounds, replenishing stocks that would otherwise be depleted.

For spillover benefits to reach fishing communities:
- **Minimum MPA size:** approximately 50 km² for meaningful spillover of mobile fish species
- **No-take core:** 20–30% of MPA area in fully protected zones produces measurable spillover
- **Connectivity:** MPA networks work better than isolated MPAs; effective spacing of 10–50 km matches larval dispersal distances for most reef species

**The economic case:** Multiple studies find that spillover benefits to adjacent fishing communities exceed enforcement costs by approximately **3:1** in well-managed MPAs. Fishing communities adjacent to the Merritt Island National Wildlife Refuge (Florida), the Leigh Marine Reserve (New Zealand), and various Philippines community reserves report consistent yield increases in zones adjacent to no-take cores.

## Current global coverage

| Metric | Figure | Source |
|---|---|---|
| Current ocean protection | ~8% of ocean surface | Protected Planet 2024 |
| CBD Kunming-Montreal Target 3 (30x30) | 30% by 2030 | COP15, December 2022 |
| Gap to target | ~22% of ocean surface | — |
| MPAs that are highly/fully protected | ~2–3% | Marine Conservation Institute |

The 30x30 commitment — agreed at COP15 in Montreal in December 2022 — obligates signatory nations to effectively conserve at least 30% of land and ocean by 2030. The gap between current coverage (~8%) and the target (30%) is large. Most of the growth needed is in the high seas, which are outside national jurisdiction and require the newly negotiated BBNJ (High Seas Treaty) agreement to implement.

## Design principles (evidence-based)

Effective MPA design requires more than drawing a boundary. These principles are grounded in ecological evidence:

### 1. Size
Larger is almost always better. Minimum effective size for mobile reef fish is approximately 50 km². For large pelagic species (tuna, sharks, whales), effective protection requires MPAs of thousands of km².

### 2. No-take core zones
Mixed-use MPAs with no-take cores outperform fully mixed-use MPAs. At least 20–30% of the MPA area should be in a fully no-take zone to generate measurable spillover.

### 3. Connectivity
MPA networks are more effective than isolated MPAs. Larvae from one MPA seed the next. Design targets: network spacing of 10–50 km to match larval dispersal distances. The OSPAR network (Northeast Atlantic) and the Coral Triangle MPAs are design examples.

### 4. Enforcement
MPAs without enforcement show little to no ecological benefit. This is the most consistent finding in MPA science. Paper parks — MPAs in name but with no patrol, no fines, and no compliance monitoring — fail. Enforcement cost is the binding constraint in low-income coastal nations.

### 5. Community buy-in
Top-down MPAs imposed without local consultation consistently show lower compliance and worse outcomes than co-managed MPAs designed with fishing communities. The most effective models are **co-management agreements** where fishing communities participate in rule-setting, monitoring, and enforcement.

## Timeline for results

| Metric | Timeline |
|---|---|
| Initial fish density increase inside MPA | 2–5 years |
| Measurable fish spillover to adjacent fishing grounds | 5–15 years |
| Trophic rebalancing (apex predator recovery) | 20–50 years |
| Full reef ecosystem recovery | 50–100+ years |

## The high seas gap

Roughly 60% of the ocean is high seas — beyond any national 200-nautical-mile exclusive economic zone. Currently, less than 2% of the high seas are protected. The **BBNJ Agreement** (Agreement under UNCLOS on the conservation and sustainable use of marine biological diversity of areas beyond national jurisdiction), agreed in 2023, provides the first legal mechanism to establish high seas MPAs under a multilateral framework. Ratification and implementation will determine whether the 30x30 target is achievable.

## Key tools and databases

- **Protected Planet / WDPA** — the World Database on Protected Areas; authoritative global registry of all MPAs; OIS connector; updated monthly
- **Mission Blue Hope Spots** — Sylvia Earle's curated network of places critical to ocean health that need protection; advocacy-focused rather than regulatory
- **IUCN Green List of Protected and Conserved Areas** — certification for well-managed, effectively governed MPAs; fewer than 100 marine sites certified globally
- **Marine Conservation Institute MPAtlas** — tracks protection quality, not just extent; flags "paper parks"

## OIS integration

The OIS Protected Planet connector ingests the WDPA dataset monthly. Guardian instances use MPA boundary data to:
- Flag whether a monitored species occurrence falls inside or outside protected area boundaries
- Detect Global Fishing Watch vessel tracks inside no-take MPAs as potential violations
- Track protection coverage percentage for a region over time and compare against 30x30 commitments

## What advocates can do

- **Push for no-take core zones** in any MPA design process — mixed-use-only MPAs have much weaker outcomes.
- **Fund enforcement capacity** in low-income coastal nations — the global MPA system has enormous coverage gaps, but funded enforcement transforms coverage into outcomes.
- **Advocate for BBNJ ratification and implementation** — high seas protection requires this treaty to work.
- **Monitor paper parks** — organisations like the Marine Conservation Institute track MPA quality; supporting their work exposes the gap between nominal and effective coverage.
- **Support co-management models** — advocate for fishing community participation in MPA design and governance.

## SDG alignment

- **SDG 14.2** — Sustainably manage and protect marine and coastal ecosystems.
- **SDG 14.5** — Conserve at least 10% of coastal and marine areas (now superseded by 30x30 target at national level).

## Sources

- [Protected Planet / WDPA](https://www.protectedplanet.net/en) — global MPA registry; OIS data connector source.
- [Mission Blue Hope Spots](https://missionblue.org/hope-spots/) — curated network of critical ocean areas needing protection.
- [Marine Protected Areas — IUCN](https://www.iucn.org/theme/marine-and-polar/our-work/marine-protected-areas) — IUCN MPA guidelines, Green List certification, policy frameworks.
- [Marine Conservation Institute](https://www.marineconservation.org/) — MPAtlas; protection quality tracking; paper park identification.
