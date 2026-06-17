---
id: sustainable-aquaculture
type: practice-guide
title: "Sustainable Aquaculture"
status: needs-expert-review
sources:
  - url: "https://www.asc-aqua.org/"
    title: "Aquaculture Stewardship Council (ASC)"
    accessed: "2026-06-17"
    tier: 2
  - url: "https://www.msc.org/"
    title: "Marine Stewardship Council (MSC)"
    accessed: "2026-06-17"
    tier: 2
  - url: "https://www.fao.org/fishery/en/aquaculture"
    title: "FAO Aquaculture — Food and Agriculture Organization"
    accessed: "2026-06-17"
    tier: 2
  - url: "https://www.fisheries.noaa.gov/topic/aquaculture"
    title: "NOAA Aquaculture Program"
    accessed: "2026-06-17"
    tier: 2
review:
  science: required
  ethics: not-applicable
  editor: required
outputs:
  website_path: /practices/sustainable-aquaculture
  github_path: content/practices/sustainable-aquaculture.md
license: CC-BY-4.0
contributors:
  - github: frankxai
---

# Sustainable Aquaculture

## The scale of aquaculture

Aquaculture — the farming of fish, shellfish, crustaceans, and seaweed in controlled or semi-controlled aquatic environments — now produces approximately **50% of all seafood consumed globally**. It has been the fastest-growing food production sector in the world for decades. Wild-capture fisheries have been roughly flat since the 1990s (most commercially important wild stocks are at or beyond maximum sustainable yield), so essentially all growth in seafood supply since then has come from aquaculture.

This makes aquaculture a critical component of global food security. It also makes the sustainability of aquaculture practices one of the most important questions in ocean conservation — poor aquaculture can devastate coastal ecosystems; well-designed aquaculture can produce protein with lower environmental impact than almost any land-based animal production system.

## The sustainability challenges

Intensive aquaculture produces a range of ecological impacts:

| Challenge | Driver | Key examples |
|---|---|---|
| **Water pollution (eutrophication)** | Excess nutrients (nitrogen, phosphorus) from fish waste and unconsumed feed | Net-pen salmon; intensive shrimp ponds |
| **Disease transmission** | Dense populations facilitate pathogen spread; can spill into wild populations | Sea lice from Atlantic salmon net-pens |
| **Genetic escapement** | Escaped farmed fish interbreed with wild populations, reducing genetic fitness | Atlantic salmon escaping Norwegian net-pens |
| **Habitat destruction** | Clearing mangroves or other coastal habitat for pond construction | Shrimp aquaculture in Southeast Asia |
| **Feed dependence** | Many carnivorous farmed species require fishmeal/fish oil from wild-caught "forage fish" | Atlantic salmon (3–5 kg wild fish per kg farmed) |
| **Antibiotic and chemical use** | Disease control in intensive systems; antibiotic resistance concerns | Shrimp; freshwater fish |
| **Invasive species** | Escape of non-native farmed species into local ecosystems | Pacific oysters displacing native species in some regions |

These impacts are not uniformly distributed across all aquaculture types. Species and system design determine the impact profile. Bivalves and seaweed have near-zero negative impacts; intensive salmon net-pens have high impacts without strong management.

## The certification standards

**Marine Stewardship Council (MSC):** Certification for **wild-caught** seafood. The MSC label on a seafood product means the fishery met independent assessment criteria for sustainable stock levels, minimal ecosystem impact, and effective management. MSC does not certify farmed seafood.

**Aquaculture Stewardship Council (ASC):** Certification for **farmed** seafood. ASC standards assess environmental performance (water quality, habitat, chemicals), social performance (worker rights, community relations), and management systems. Currently certifies salmon, shrimp, tilapia, bivalves, pangasius, trout, abalone, and other species.

Key distinction: **MSC = wild-caught**, **ASC = farmed.** Both are third-party certifications with supply-chain chain-of-custody requirements. Neither is perfect, but both represent a significantly higher bar than uncertified alternatives.

## Best-practice species and systems

### Low-impact / recommended species

**1. Bivalves (oysters, mussels, clams, scallops)**
The gold standard for sustainable aquaculture. Bivalves are filter feeders — they extract phytoplankton and particulate organic matter from the water column with no feed input. Benefits:
- Zero feed required (no fishmeal/fish oil dependence)
- Actually improve water quality by filtering nutrients and suspended solids
- Low disease risk compared with finfish
- High protein per unit area
- Can be integrated into marine restoration (oyster reef restoration is dual-purpose)

**2. Seaweed (kelp, dulse, wakame, nori, spirulina)**
Zero feed input; absorbs nutrients from the water column; potential blue carbon function; rapidly growing global market for food, supplements, fertiliser, and bioplastics. Low-impact cultivation at scale represents one of the most environmentally positive food production activities possible.

**3. Integrated Multi-Trophic Aquaculture (IMTA)**
IMTA places complementary species at different trophic levels in a single system. The waste from one species becomes the input for another:

- **Finfish (e.g. salmon)** produce nitrogen-rich waste water → feeds
- **Bivalves (e.g. mussels)** that filter particulate waste → alongside
- **Seaweed (e.g. kelp)** that absorbs dissolved nutrients

The result: dramatically reduced net nutrient discharge; diversified production; improved economics. IMTA is practiced commercially in Norway, Canada, and Chile; uptake is growing but remains a small fraction of total aquaculture production.

**4. Recirculating Aquaculture Systems (RAS)**
Land-based closed-containment systems that recirculate >95% of water through biological filtration. Advantages:
- Zero effluent discharge to natural water bodies
- Zero escapement risk (completely enclosed)
- Zero proximity to wild fish populations (no disease transmission)
- Can be located anywhere (not dependent on coastal access)
- Precise environmental control enables year-round optimised production

Disadvantages:
- High capital cost ($3–5M per tonne of annual capacity)
- High energy intensity (5–10 kWh/kg fish produced vs. <1 kWh for net-pens)
- Carbon footprint depends entirely on energy source

RAS is the direction of travel for Atlantic salmon in environmentally sensitive markets; major facilities now operating in the US, Denmark, Japan, and Singapore.

### High-impact species (proceed with scrutiny)

**Atlantic salmon (net-pen, open water):** Sea lice, nutrient discharge, escapement, and fishmeal dependence make conventional net-pen Atlantic salmon one of the more environmentally costly farmed species. ASC-certified operations are significantly better than uncertified; RAS salmon eliminates most concerns.

**Tropical shrimp (intensive pond):** Historical mangrove destruction, antibiotic use, disease cycles, and effluent discharge characterise the worst of the sector. Improvement is possible with ASC certification, zero-discharge pond design, and mangrove buffer maintenance.

## OIS integration

The Aquaculture Architect Guardian — a specialised OIS guardian instance for coastal aquaculture site planning — uses:
- **Copernicus Marine Service:** water temperature, salinity, chlorophyll-a (productivity proxy), and dissolved oxygen data for site assessment
- **OBIS occurrence data:** local ecosystem species inventory to identify sensitive habitats or protected species in proposed site areas
- **Protected Planet:** MPA boundary data to flag prohibited zones
- **FAO and national fisheries databases:** regional fishmeal and feed ingredient sustainability profiles

The guardian outputs a site suitability matrix that rates species-system combinations against local conditions.

## Sources

- [Aquaculture Stewardship Council (ASC)](https://www.asc-aqua.org/) — global certification standard for farmed seafood; species standards and certification database.
- [Marine Stewardship Council (MSC)](https://www.msc.org/) — certification standard for wild-caught seafood; complementary to ASC.
- [FAO Aquaculture](https://www.fao.org/fishery/en/aquaculture) — production statistics, species profiles, sustainability guidelines.
- [NOAA Aquaculture Program](https://www.fisheries.noaa.gov/topic/aquaculture) — US regulatory framework; sustainable aquaculture guidance.
