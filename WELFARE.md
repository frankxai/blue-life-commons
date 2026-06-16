# WELFARE.md — Animal Welfare as a First-Class Interest

Blue Life Commons exists to help people protect marine life. That means the animals are not only a *subject* of our content and a *constraint* on our behaviour — their welfare is an **interest the system actively represents and supports.**

[ETHICS.md](ETHICS.md) tells contributors what *not* to do (don't disturb, don't reveal locations, don't anthropomorphize). This document tells the system what to *watch for and support* on the animals' behalf. The two are complements: ETHICS is the floor, WELFARE is the orientation.

> **The shift:** from "do no harm" (per-interaction, per-actor) to "support flourishing and recovery" (cumulative, population- and individual-aware).

## 1. The Five Domains, adapted to marine life

We use the **Five Domains Model** (Mellor et al. 2020) — the current scientific standard, which explicitly added *human–animal interaction* as a welfare input. The four physical/functional domains feed the fifth (mental state), which we only ever *infer*, never narrate.

| Domain | What the animal needs | What the commons can represent / a guardian can watch |
|---|---|---|
| **Nutrition** | Adequate prey of adequate quality | Forage-stock status, primary productivity, fishery removal on the same prey stock; (rehab) feeding response, body condition |
| **Environment** | Intact critical habitat | Thermal regime (heat-stress), water quality / HAB risk, ice phenology, **acoustic habitat (noise budget)**, physical disturbance (vessel density) |
| **Health** | Freedom from injury & disease | Entanglement/ship-strike risk, body condition, stranding/morbidity rates, disease outbreaks (morbillivirus, HAB toxicosis) |
| **Behaviour** | Freedom to perform natural behaviours | Undisturbed foraging, resting/haul-out, breeding, migration — represented as *disturbance events that interrupt a behavioural budget* |
| **Mental state** | (the output) | Inferred **only** from validated physiological/behavioural correlates, with citation and a confidence tag — never introspected |

## 2. Welfare is cumulative — the Disturbance Budget

A per-actor rule ("stay 100 m back") cannot protect an animal from the *fiftieth* boat at 100 m that flushes the haul-out. Real harm is **additive** — the science is the **Population Consequences of Disturbance (PCoD)** framework: repeated sub-lethal disturbance → physiology → health → vital rates → population decline.

So the commons represents a **disturbance budget**: the cumulative human-pressure capacity of a place/season/population (vessels, noise, approaches). A guardian watches *utilization* against that budget, not just individual compliance. This is the `disturbance_budget` field in the artifact schema.

## 3. Welfare as a queryable state

Welfare must not be buried in prose where no agent can act on it. A `species-page` (and a region briefing) can carry a `welfare` block:

```yaml
welfare:
  state: pressured            # favourable | pressured | critical | recovering | unknown
  dominant_stressor: vessel-noise
  confidence: modeled         # measured | modeled | expert-opinion
  five_domains:
    environment: "Chronic shipping-noise exposure in core foraging habitat (cite)."
    behaviour: "Vessel density displaces foraging in summer (cite)."
```

Every guardian inherits this; a "critical" welfare state with a named stressor is something the system can surface, not something a reader has to infer.

## 4. The anti-anthropomorphism tightrope

We center the animal's *interests* without claiming to read its *feelings*. The discipline:

- **Represent affect only via validated, cited proxies.** Not "the whale is stressed" but "*fecal glucocorticoid metabolites are an established stress correlate in this taxon (cite); vessel-noise exposure here is associated with elevated values (cite).*" (Right-whale glucocorticoids measurably dropped when shipping fell after 9/11 — Rolland et al.)
- **Speak in needs and evidence, not emotions.** "Flushing from a haul-out imposes an energetic and predation cost" (measurable) — not "the seals are frightened."
- **Confidence-tag every welfare inference** (`measured` / `modeled` / `expert-opinion`). Most stressor→population links are modeled or expert judgment; say so.
- The bans in ETHICS.md stay. This adds a **positive, citable vocabulary** — energetic budgets, vital rates, disturbance thresholds, recovery trajectories — so the system can *advocate* while staying inside the science.

## 5. Unusual Mortality Events (UME)

A spike in strandings is the clearest early welfare alarm. We map to NOAA's seven UME criteria (magnitude, temporal, spatial, species composition, pathology, vulnerable stock, concurrent declines). A stranding-rate anomaly escalates a guild and prompts a `necropsy-summary` / region review. This connects the welfare frame directly to the rehab/stranding workflow (see [ETHICS.md](ETHICS.md) § Rehabilitation, sanctuary & individual animals).

## 6. Welfare during human "help"

Rescue, rehab, tagging, and even well-meant approach carry welfare cost. The system represents the disturbance footprint of the activity it *encourages*, and honours: **release > lifelong captivity** as the default; **no clinical adjudication** by the system (it assembles evidence; licensed vets and regulators decide); and **honesty about invasiveness** (a tag is described plainly, never euphemized).

## Sources

- Mellor, D. J., et al. (2020). *The 2020 Five Domains Model.* Animals 10(10):1870. https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7602120/
- National Academies (2017). *Approaches to Understanding the Cumulative Effects of Stressors on Marine Mammals (PCoD).* https://nap.nationalacademies.org/read/23479/chapter/2
- Rolland, R. M., et al. (2012). *Evidence that ship noise increases stress in right whales.* Proc. R. Soc. B.
- NOAA Fisheries. *Understanding Marine Mammal Unusual Mortality Events.* https://www.fisheries.noaa.gov/insight/understanding-marine-mammal-unusual-mortality-events

> Built on SIP · Blue Life Commons. Welfare is the orientation; ethics is the floor.
