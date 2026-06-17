---
id: the-30x30-goal
type: wisdom
title: "The 30x30 Goal — What It Is, Why It Matters, and How Far We Have to Go"
status: needs-expert-review
sources:
  - url: "https://www.cbd.int/gbf/targets/3"
    title: "CBD Global Biodiversity Framework Target 3 (30x30)"
    accessed: "2026-06-17"
    tier: 2
  - url: "https://www.protectedplanet.net/en"
    title: "Protected Planet / WDPA Annual Report"
    accessed: "2026-06-17"
    tier: 2
  - url: "https://www.marineconservation.org/"
    title: "Marine Conservation Institute"
    accessed: "2026-06-17"
    tier: 2
  - url: "https://www.iucn.org/theme/marine-and-polar/our-work/marine-protected-areas"
    title: "IUCN Marine Protected Areas"
    accessed: "2026-06-17"
    tier: 2
review:
  science: required
  ethics: not-applicable
  editor: required
outputs:
  website_path: /wisdom/the-30x30-goal
  github_path: content/wisdom/the-30x30-goal.md
license: CC-BY-4.0
contributors:
  - github: frankxai
---

# The 30x30 Goal — What It Is, Why It Matters, and How Far We Have to Go

In December 2022, 196 countries made the most ambitious ocean protection commitment in history. Most people have never heard of it. That gap — between what was agreed and what the public understands — is part of why it may not be achieved.

---

## What Was Agreed

At **COP15** of the Convention on Biological Diversity (CBD), held in Kunming and Montreal in December 2022, parties to the CBD adopted the **Kunming-Montreal Global Biodiversity Framework (GBF)**. Target 3 — the "30x30" goal — reads:

> *"Protect and conserve at least 30 per cent of terrestrial, inland water, and coastal and marine areas, especially areas of particular importance for biodiversity and ecosystem functions and services... through effectively and equitably managed, ecologically representative and well-connected systems of protected areas and other effective area-based conservation measures..."*

In plain language: **30% of the ocean protected by 2030**, with meaningful management — not just lines on a map.

This is binding under international law for countries that ratify it. **196 countries signed.** It covers both land (30% of terrestrial areas) and ocean (30% of marine areas). The ocean target is the one least likely to be met.

---

## Where We Are Now

Current protection levels:
- **~8%** of the global ocean has some form of official protected status
- **Less than 3%** is strictly protected — fully no-take zones with active management and enforcement
- **Less than 1.2%** of the high seas (areas beyond national jurisdiction) is protected

To reach 30% by 2030 from 8% today requires protection to **more than triple** in approximately **four years**. At current rates of MPA designation, we will not get there.

The scale of the gap is not a reason for despair. It is a reason for urgency. The designation process, when political will is present, can move quickly. The question is whether institutional momentum can build fast enough.

---

## Why 30%?

The 30% threshold is not arbitrary. It reflects converging scientific consensus from IPBES (the Intergovernmental Science-Policy Platform on Biodiversity and Ecosystem Services) and IUCN (International Union for Conservation of Nature) on what minimum fraction of protected area is needed to:

1. **Halt the trajectory of marine biodiversity loss.** We are currently in the sixth mass extinction. Marine species are declining across every taxonomic group. Without space free from industrial extraction, populations cannot recover.

2. **Maintain ecosystem services.** Coral reefs, kelp forests, seagrass beds, and deep-sea ecosystems provide services — carbon sequestration, coastal protection, fisheries productivity, oxygen production — that human civilization depends on. These services require intact, functioning ecosystems.

3. **Buffer climate change impacts.** MPAs reduce local stressors (overfishing, pollution, coastal disturbance) that compound climate impacts. Reef systems with intact herbivore fish populations can survive bleaching events that destroy similarly warmed reefs where fish have been removed.

4. **Enable fisheries recovery.** Counterintuitively, fishing communities benefit from protection. No-take zones function as nurseries — fish reproduce inside and spill over into fishing areas outside, increasing yields. The science is robust: well-enforced MPAs increase fish biomass inside by 600% on average.

---

## The "Paper Parks" Problem

The 8% figure is itself an overcount. A significant proportion of existing MPAs are **"paper parks"** — designated on paper and in databases, but receiving no meaningful management. They exist in Protected Planet databases and in national progress reports, but not in the water.

Inside many nominal MPAs:
- Industrial fishing continues
- There is no enforcement presence
- No monitoring occurs
- No management plan exists

When the CBD GBF requires protection that is "effectively and equitably managed," it is directly addressing this problem. The commitment is not to designation — it is to **functional protection**.

Distinguishing paper parks from effective protection is one of the core research challenges in marine conservation. The Ocean Intelligence System's Protected Planet connector queries the WDPA database and can surface management data alongside boundary data — but management quality assessments require additional sources beyond what the WDPA currently captures comprehensively.

---

## The High Seas Gap

Perhaps the most difficult piece of the 30x30 puzzle is the **high seas** — areas beyond national jurisdiction (ABNJ), which cover approximately **64% of the ocean surface**. These waters are governed by no single nation. The current framework for managing them is fragmented across multiple international bodies with limited enforcement capacity.

Currently: **only ~1.2% of the high seas is under any form of protection**.

The **BBNJ Treaty** — the Agreement on the Conservation and Sustainable Use of Marine Biological Diversity of Areas Beyond National Jurisdiction — is the legal instrument designed to change this. Finalized in 2023 after nearly two decades of negotiation, it creates a framework for:
- Establishing MPAs on the high seas
- Sharing marine genetic resources equitably
- Conducting environmental impact assessments for high-seas activities
- Building capacity in developing nations

The BBNJ Treaty was signed in 2023 but had **not yet entered into force as of mid-2024** — it requires 60 ratifications. The urgency of ratification cannot be overstated: without the treaty, the largest part of the ocean remains essentially unprotectable under the 30x30 framework.

---

## What Indigenous and Community-Led Protection Can Contribute

A critical and often undercounted category in MPA tallies is **OECMs — Other Effective Area-Based Conservation Measures**. These include:

- Indigenous-governed territories where traditional management has maintained biodiversity
- Community-managed fishery closures
- Private conservation initiatives with third-party verification

The CBD GBF explicitly includes OECMs in the 30% accounting, subject to criteria. This matters because many of the most ecologically intact marine areas on Earth are governed by Indigenous peoples and local communities — using traditional management systems that predate the MPA concept by centuries (see: [Indigenous Ocean Stewardship](./indigenous-ocean-stewardship.md)).

Including these areas appropriately — with full recognition of Indigenous rights and consent — could meaningfully accelerate progress toward 30%. Excluding them to favor government-designated MPAs would be both scientifically wrong and ethically indefensible.

---

## How the Ocean Intelligence System Supports 30x30

The Ocean Intelligence System connects to the **Protected Planet** database via the Protected Planet MCP connector, enabling:

- **Real-time MPA boundary queries** — what is protected in a given region, with what designation status
- **Overlap analysis** — which species occurrences (OBIS/GBIF) fall within vs. outside protected areas
- **Fishing vessel tracking inside MPAs** — via the Global Fishing Watch connector, detecting whether no-take designations are being enforced
- **Biodiversity comparison** — do MPAs actually harbor more biodiversity? Cross-referencing occurrence data inside and outside protection boundaries

This is not advocacy. It is evidence. The data either shows that protection is working — or it shows it is not. Both findings are valuable.

---

## What You Can Do

The 30x30 goal will not be achieved by governments acting alone. It requires public demand sufficient to translate political declarations into funded management programs.

**For ratification:** Contact your government representatives about ratifying the BBNJ Treaty. In countries where it is already ratified, advocate for implementation funding.

**For national action:** Many countries have made 30x30 commitments domestically. Holding governments accountable to their own stated targets is one of the most direct levers available to civil society.

**For local action:** Support the designation and meaningful management of MPAs in your coastal region. Local MPAs are where the gap between designation and management is most directly observable — and most directly fixable.

**For awareness:** The 30x30 goal cannot be achieved if most people do not know it exists. Share this with someone who cares about the ocean.

---

*Sources: Convention on Biological Diversity, Kunming-Montreal Global Biodiversity Framework, Target 3 (2022); Protected Planet / WDPA Annual Report (2023); Marine Conservation Institute; IUCN Green Status of Ecosystems; IPBES Global Assessment Report on Biodiversity and Ecosystem Services.*
