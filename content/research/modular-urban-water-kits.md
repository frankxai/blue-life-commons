---
id: research-modular-urban-water-kits-001
type: research-summary
title: "Modular Urban Water Kits: From Terrace Bench to Reviewed Field Trial"
region:
  - netherlands
audience:
  - citizen-scientist
  - educator
  - researcher
  - developer
status: needs-expert-review
consensus_state: emerging
last_verified: "2026-09-24"
sources:
  - url: "https://experts.illinois.edu/en/publications/floating-treatment-wetland-retrofit-in-a-stormwater-wet-pond-prov/"
    title: "Field study: limited water-quality improvements from a wetland retrofit"
    accessed: "2026-09-24"
    tier: 1
  - url: "https://pubmed.ncbi.nlm.nih.gov/28177425/"
    title: "Effects on the underlying water column by extensive floating treatment wetlands"
    accessed: "2026-09-24"
    tier: 1
  - url: "https://pubmed.ncbi.nlm.nih.gov/38557712/"
    title: "Wetland coverage, residence time, oxygen and nitrogen removal"
    accessed: "2026-09-24"
    tier: 1
  - url: "https://research.wur.nl/en/publications/the-contribution-of-plant-uptake-to-nutrient-removal-by-floating-/"
    title: "Wageningen controlled nutrient-uptake experiment"
    accessed: "2026-09-24"
    tier: 1
  - url: "https://www.agv.nl/zelf-regelen/vergunning/beschoeiing-aanleggen-of-vervangen/"
    title: "AGV guidance on water-edge materials and leaching"
    accessed: "2026-09-24"
    tier: 1
  - url: "https://www.agv.nl/zelf-regelen/vergunning/steigers-ligplaatsen/"
    title: "AGV guidance on jetties, water movement and ecology"
    accessed: "2026-09-24"
    tier: 1
  - url: "https://www.rivm.nl/pfas/pfas-in-oppervlaktewater"
    title: "RIVM on PFAS and use of surface water"
    accessed: "2026-09-24"
    tier: 1
  - url: "https://www.zwemwater.nl/schoon-water/"
    title: "Official bathing-water assessment information"
    accessed: "2026-09-24"
    tier: 1
  - url: "https://www.adafruit.com/product/381"
    title: "Adafruit DS18B20 price and use limitations"
    accessed: "2026-09-24"
    tier: 2
  - url: "https://www.seeedstudio.com/SenseCAP-S2100-LoRaWAN-Data-Logger-p-5361.html"
    title: "Seeed S2100 logger specifications and list price"
    accessed: "2026-09-24"
    tier: 2
  - url: "https://www.dfrobot.com/product-1628.html"
    title: "DFRobot dissolved oxygen kit price and upkeep"
    accessed: "2026-09-24"
    tier: 2
  - url: "https://atlas-scientific.com/embedded-solutions/ezo-conductivity-circuit/"
    title: "Atlas EZO-EC communications and calibration"
    accessed: "2026-09-24"
    tier: 2
  - url: "https://help.prusa3d.com/product/mk3s/material-guide_220"
    title: "Prusa PETG and ASA material comparison"
    accessed: "2026-09-24"
    tier: 2
  - url: "https://oshwa.org/resources/sharing-best-practices/"
    title: "OSHWA best practices for editable design files"
    accessed: "2026-09-24"
    tier: 2
review:
  science: required
  ethics: required
  editor: pending
outputs:
  website_path: /research/modular-urban-water-kits
  github_path: content/research/modular-urban-water-kits.md
  map_layer: false
sensitivity:
  tier: high
  rationale: Home-based water access and small habitats should not reveal the precise property or sensitive fauna.
  generalized_to: Amsterdam district only
impact:
  claim: "Proposed a reproducible, review-gated urban-water kit system."
  eligible_for_hypercert: false
contributors:
  - github: frankxai
license: CC-BY-4.0
---

# Modular Urban Water Kits: From Terrace Bench to Reviewed Field Trial

## What to build first

Run a small contained experiment, record honest measurements, and make a beautiful serviceable terrace interface. Do not place any float, cleaner, turbine or mooring in shared water until the owner and water manager have cleared the specific activity. This is a **proposed design**, not an installed or certified water treatment system. The location is deliberately coarse. AGV describes both water movement/ecological effects of jetties and the importance of non-leaching water-edge materials. [AGV jetties](https://www.agv.nl/zelf-regelen/vergunning/steigers-ligplaatsen/) · [AGV materials](https://www.agv.nl/zelf-regelen/vergunning/beschoeiing-aanleggen-of-vervangen/).

| Module | Job, boundary and acceptance test | Indicative parts allowance* |
| --- | --- | ---: |
| K0, sample caddy | Take dated, labeled, duplicate manual samples; no persistent immersion. Ten complete records before claiming a trend. | €90–220 |
| K1, observation cassette | Dry-mounted controller, removable water-rated temperature + conductivity probes, reference comparison, buffered observations. Target ≥95% valid expected readings during first 30 days. | €300–850 |
| K2, paired treatment bench | Two independent lidded 20 L HDPE test vessels with matched flow; compare media and control, including energy and maintenance. No experimental discharge to the canal. | €250–750 |
| G1, herb cabinet | Bolted aluminum frame, replaceable polycarbonate, contained clean irrigation; verify deck load, wind, vent and escape route. | €350–1,200 |
| E1, sensor solar | Protected low-voltage supply for a **measured** sensor load; log Wh/day and dark-day survival before claiming autonomy. | €250–700 |
| K3, living edge | Retrievable plant module with declared buoyancy and ecology review; only an authorized field trial with nearby control and above/below-root oxygen. | €450–1,800 |

*EUR allowances are planning ranges, not quotes; shipping, VAT, paid labor, site works, permits, lab services and replacement consumables are not included. No order is recommended before geometry, materials and rights are checked.

## Why still water changes the answer

The open canal has no known control volume or flow through a root mat. Nutrient uptake, microbe-mediated transformation, shade and wildlife habitat are different mechanisms. A planted raft alone cannot certify swimming or quantify canal-wide cleaning; bathing-water assessment includes requirements beyond household chemistry probes. Published experiments have found both limited water-quality improvements and lower oxygen beneath some floating treatments; hydraulic residence time, temperature and oxygen affect nitrogen removal. Take above/below-root oxygen readings and use a nearby untreated comparison, including warm and post-rain periods. [Official bathing-water information](https://www.zwemwater.nl/schoon-water/) · [field retrofit study](https://experts.illinois.edu/en/publications/floating-treatment-wetland-retrofit-in-a-stormwater-wet-pond-prov/) · [under-raft oxygen](https://pubmed.ncbi.nlm.nih.gov/28177425/) · [residence-time study](https://pubmed.ncbi.nlm.nih.gov/38557712/).

For a **contained** 20 L loop with measured 2 L/min, nominal residence time is 20 ÷ 2 = 10 minutes per pass. Recirculating the same 20 L does not establish removal; use a control with the same pump and compare initial and final **mass**, not concentration alone. For a target nutrient, report initial mass, final dissolved mass, material captured, any harvested biomass and unaccounted mass. Assay total nitrogen/phosphorus through a qualified method; the temperature and conductivity probes alone do not measure them. State the uncertainty and blank/duplicate procedure. Wageningen's iris uptake results came from deliberately dosed controlled vessels and cannot be transferred as a local canal removal forecast. [Wageningen experiment](https://research.wur.nl/en/publications/the-contribution-of-plant-uptake-to-nutrient-removal-by-floating-/).

### K0 and K1: observation bill of materials

| Part/interface | Reference choice | Design note |
| --- | --- | --- |
| Dry-side brain | ESP32-class board with buffered timestamped records, serviceable enclosure, fused protected supply | Select exact board, power source and protocol after site survey; don't invent compatibility. |
| Temperature | Manufacturer-rated water probe for actual local conductivity and immersion time | Adafruit's $9.95 waterproof DS18B20 is for a **contained non-corrosive demonstration only**: the vendor excludes salt water and does not guarantee long-term immersion. [Adafruit](https://www.adafruit.com/product/381). |
| Conductivity | Atlas EZO-EC-compatible probe/circuit or equivalent with temperature compensation | The circuit supports UART/I²C and 2/3-point calibration; circuit and probe are distinct items. Log original µS/cm and calibration solution lot. [Atlas](https://atlas-scientific.com/embedded-solutions/ezo-conductivity-circuit/). |
| Optional radio | Seeed SenseCAP S2100, $72.50 list price on 2026-09-24 | IP66 LoRaWAN logger accepting selected RS485/analog/GPIO inputs; **not** a water probe or gateway. Use simpler home connectivity if reliable. Verify probe voltage/interface. [Seeed](https://www.seeedstudio.com/SenseCAP-S2100-LoRaWAN-Data-Logger-p-5361.html). |
| Optional dissolved oxygen | DFRobot SEN0237-A, $169 list price on 2026-09-24 | Vendor specifies replacement filling solution monthly and more frequent membrane replacement in muddy water; solution is not included. Include upkeep, reference checks and waste in the operating budget. [DFRobot](https://www.dfrobot.com/product-1628.html). |

Record: UTC, coarse public location, sensor ID, probe depth, °C/µS·cm⁻¹, raw reading, quality flag, calibration ID, cleaning event, firmware version and weather context. Keep the precise property coordinate owner-only. A lab result carries its method and detection limit; an LLM never upgrades a raw household reading into a safety declaration.

### K2: contained treatment bench and measurable efficiency

- Build **two separate arms**, each with the same source water volume, pump model, measured flow, illumination and elapsed time. Arm A has a cleanable prefilter and a removable contained substrate cassette; arm B controls for pump, settling and container effects. Repeat with swapped arm positions.
- Use lidded HDPE lab vessels, labeled overflow containment and removable commercial tubing/fittings. Log true pump electricity in Wh, media mass/lot, observed fouling, pressure/flow loss, filter-washing time and spent-media destination. An apparent turbidity improvement is not a pathogen or PFAS claim.
- Define success before testing: repeatable improvement over control for **one named endpoint**, with confidence interval or replicate range, no unmanaged discharge, acceptable € per actual gram removed and named maintenance owner. Stop or redesign if the control improves equally, oxygen worsens or material leaches.

### G1 and E1: usable terrace layers

- G1: aluminum extrusion and bolted joints let the cabinet be reconfigured; UV-rated polycarbonate panels are individually replaced. Put thyme/rosemary/sage in a freely draining tray; parsley/chives in a moister one; mint/lemon balm in contained pots. Food plants receive clean potable or assessed rainwater, not untreated canal water; RIVM identifies possible PFAS exposure routes when surface water is used for food growing. Botanical education is distinct from a therapeutic claim. [RIVM](https://www.rivm.nl/pfas/pfas-in-oppervlaktewater).
- E1: at a **measured** 3 W average, demand is 72 Wh/day. A hypothetical 60 Wp panel × 2 effective sun-hours/day × 0.70 system factor yields 84 Wh/day. Two dark days at 80% usable storage imply ≥180 Wh nominal before cold/aging margins. These are sizing equations, not a winter yield prediction. Qualified electrical design and mounting review precede purchase.
- A still-water turbine has no case without a measured velocity profile. Even the previously modeled 0.5 m² rotor at 0.3 m/s and 25% conversion produces only about 1.7 W; site velocity is unknown and v³ dominates output.

### K3: field ecology that can be retrieved

Consider commercially specified UV-stabilized HDPE marine buoyancy with documented displacement, a separate removable plant basket and captive 316 stainless fittings **only after compatibility checks**. Choose native plants with local ecology and measured salinity in mind. Verify total soaked mass, freeboard, reserve buoyancy, stability, tether loads, storm removal, wildlife entrapment, shaded habitat and potential leaching. Do not use loose expanded-polystyrene foam, salvaged bottles or a printed structural float. Harvested biomass and plant fragments need tracked destinations; the monitoring plan includes an untreated control and an oxygen stop threshold set by the site ecologist. [AGV materials](https://www.agv.nl/zelf-regelen/vergunning/beschoeiing-aanleggen-of-vervangen/) · [under-raft oxygen study](https://pubmed.ncbi.nlm.nih.gov/28177425/).

## What to print and what not to print

Print the proposed [editable dry-side cable-label plate](../../designs/urban-water/dry-side-cable-plate.scad) flat on a suitable printer. Two cable ties hold the plate to an indoor/dry cabinet rail; a separate pair retains the cable, with no drilling into the building. The part is a fit-test candidate and is neither a load-bearing bracket nor a water-contact device. Parameterize the rail tie spacing, plate dimensions, cable diameter, slot clearance and label area; keep the original editable SCAD as well as generated STL and print orientation in any reviewed kit release. PETG is easy to print for fit checks; ASA can suit a dry outdoor location but needs appropriate printing enclosure and ventilation. All printed parts require physical fit, UV-aging and disposal tests. [Prusa material guide](https://help.prusa3d.com/product/mk3s/material-guide_220).

## How a community kit earns its label

1. **Proposed:** bill of materials with manufacturer part numbers, alternate suppliers, price date and shipping/VAT; editable CAD and electrical schematic; source-led mechanism, privacy/ethics and expected failure modes.
2. **Bench tested:** photos of real assembly, firmware revision, measured dimensions/flow/energy, calibration log, replicates with control, hours to service and an honest failure report.
3. **Authorized field trial:** site rights, local permission record, independent engineering/ecology review, retrieval plan, insured operator, wildlife stop conditions and location coarsening.
4. **Replicated:** second independent site, complete material substitution record, comparable endpoints and a published result whether it supports or contradicts the original design.

Document hardware, firmware and written text under **separately chosen compatible licenses** before a release; this proposal and CAD currently follow this repository's CC-BY-4.0 text license. Do not claim OSHWA certification or a validated commercial hardware design. OSHWA asks for original editable files and enough documentation to let others change a design. Community contributions are reviewed PRs with new measurements, not unverified success stories. [OSHWA best practices](https://oshwa.org/resources/sharing-best-practices/).

## Sources

- [Floating wetland retrofit field study, ecological engineering](https://experts.illinois.edu/en/publications/floating-treatment-wetland-retrofit-in-a-stormwater-wet-pond-prov/).
- [Under-raft dissolved oxygen field experiment](https://pubmed.ncbi.nlm.nih.gov/28177425/).
- [Floating-wetland coverage and retention study](https://pubmed.ncbi.nlm.nih.gov/38557712/).
- [Wageningen controlled nutrient-uptake experiment](https://research.wur.nl/en/publications/the-contribution-of-plant-uptake-to-nutrient-removal-by-floating-/).
- [AGV material-leaching guidance](https://www.agv.nl/zelf-regelen/vergunning/beschoeiing-aanleggen-of-vervangen/) and [AGV jetty guidance](https://www.agv.nl/zelf-regelen/vergunning/steigers-ligplaatsen/).
- [RIVM surface-water PFAS guidance](https://www.rivm.nl/pfas/pfas-in-oppervlaktewater) and [official bathing-water information](https://www.zwemwater.nl/schoon-water/).
- [Adafruit DS18B20](https://www.adafruit.com/product/381); [Seeed S2100](https://www.seeedstudio.com/SenseCAP-S2100-LoRaWAN-Data-Logger-p-5361.html); [DFRobot oxygen kit](https://www.dfrobot.com/product-1628.html); [Atlas EZO-EC](https://atlas-scientific.com/embedded-solutions/ezo-conductivity-circuit/).
- [Prusa material guide](https://help.prusa3d.com/product/mk3s/material-guide_220); [OSHWA best practices](https://oshwa.org/resources/sharing-best-practices/).
