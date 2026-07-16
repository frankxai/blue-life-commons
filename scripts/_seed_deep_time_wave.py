from pathlib import Path
from textwrap import dedent

DIR = Path("content/species/marine-reptiles")

TAXA = [
    dict(
        slug="ichthyosaurus-communis",
        title="Ichthyosaurus communis",
        period="Early Jurassic",
        clade="Ichthyosauria",
        length="~1.5–3 m (typical)",
        diet="Fish & cephalopods",
        locomotion="Dolphin-like swimming",
        habitat="Early Jurassic seas",
        body="Classic ichthyosaur type genus — streamlined, long snout, crescent tail.",
        difficulty="beginner",
        compare=[
            ("species-ophthalmosaurus-icenicus", "Ophthalmosaurus", "Related ichthyosaur body plan"),
            ("species-blue-whale", "Blue whale", "Convergent streamlining only"),
        ],
        consensus="settled",
        brit="ichthyosaur",
    ),
    dict(
        slug="plesiosaurus-dolichodeirus",
        title="Plesiosaurus dolichodeirus",
        period="Early Jurassic",
        clade="Plesiosauria",
        length="~3–5 m (typical)",
        diet="Fish & cephalopods (model-dependent)",
        locomotion="Four-flipper swimming",
        habitat="Early Jurassic seas",
        body="Type plesiosaur — relatively long neck, four flippers, compact body.",
        difficulty="beginner",
        compare=[
            ("species-elasmosaurus-platyurus", "Elasmosaurus", "Longer-neck elasmosaurid extreme"),
            ("leatherback-turtle", "Leatherback turtle", "Living marine reptile"),
        ],
        consensus="settled",
        brit="plesiosaur",
    ),
    dict(
        slug="platecarpus-tympaniticus",
        title="Platecarpus tympaniticus",
        period="Late Cretaceous",
        clade="Mosasauridae",
        length="~4–7 m (typical)",
        diet="Fish & marine prey",
        locomotion="Tail-powered swimming",
        habitat="Western Interior Seaway & warm seas",
        body="Well-known mid-sized mosasaur — common museum teaching taxon.",
        difficulty="beginner",
        compare=[
            ("species-mosasaurus-hoffmannii", "Mosasaurus", "Larger mosasaur relative"),
            ("great-white-shark", "Great white shark", "Living apex analogy"),
        ],
        consensus="settled",
        brit="mosasaur",
    ),
    dict(
        slug="temnodontosaurus-platyodon",
        title="Temnodontosaurus platyodon",
        period="Early Jurassic",
        clade="Ichthyosauria",
        length="Large ichthyosaur (multi-meter class)",
        diet="Marine vertebrates (model-dependent)",
        locomotion="Powerful open-water swimming",
        habitat="Early Jurassic seas",
        body="Large early Jurassic ichthyosaur with robust snout and large eyes.",
        difficulty="intermediate",
        compare=[
            ("species-ichthyosaurus-communis", "Ichthyosaurus", "Smaller classic ichthyosaur"),
            ("species-shonisaurus-popularis", "Shonisaurus", "Giant ichthyosaur comparison"),
        ],
        consensus="settled",
        brit="ichthyosaur",
    ),
    dict(
        slug="dakosaurus-maximus",
        title="Dakosaurus maximus",
        period="Late Jurassic",
        clade="Thalattosuchia (marine crocodylomorph)",
        length="~4–5 m (typical ranges)",
        diet="Apex marine predator",
        locomotion="Tail-powered marine swimming",
        habitat="Late Jurassic seas",
        body="Marine crocodylomorph — not a dinosaur, not a mosasaur; short snout, ziphodont teeth.",
        difficulty="intermediate",
        compare=[
            ("species-mosasaurus-hoffmannii", "Mosasaurus", "Different marine reptile guild"),
            ("great-white-shark", "Great white shark", "Living apex analogy"),
        ],
        consensus="settled",
        brit="crocodilian",
    ),
    dict(
        slug="metriorhynchus-superciliosus",
        title="Metriorhynchus superciliosus",
        period="Middle–Late Jurassic",
        clade="Thalattosuchia (marine crocodylomorph)",
        length="~3 m class (typical)",
        diet="Fish & marine prey",
        locomotion="Fully marine swimming",
        habitat="Jurassic epicontinental seas",
        body="Fully marine crocodylomorph with paddle-like limbs and hypocercal tail — ocean lifestyle, not dinosaur.",
        difficulty="intermediate",
        compare=[
            ("species-dakosaurus-maximus", "Dakosaurus", "Related marine crocodylomorph"),
            ("leatherback-turtle", "Leatherback turtle", "Living marine reptile"),
        ],
        consensus="settled",
        brit="crocodilian",
    ),
]


def render(t: dict) -> str:
    compare_yaml = "\n".join(
        f'  - target_id: {tid}\n    label: "{lab}"\n    note: "{note}"'
        for tid, lab, note in t["compare"]
    )
    return f'''---
id: species-{t["slug"]}
type: species-page
title: {t["title"]}
species_group:
  - marine-reptiles
species:
  - {t["slug"]}
difficulty: {t["difficulty"]}
audience:
  - traveler
  - student
  - educator
  - citizen-scientist
  - researcher
status: needs-expert-review
sources:
  - url: https://paleobiodb.org/
    title: Paleobiology Database
    tier: 1
    accessed: "2026-07-16"
  - url: https://www.britannica.com/animal/{t["brit"]}
    title: Encyclopaedia Britannica — related clade overview
    tier: 2
    accessed: "2026-07-16"
  - url: https://ucmp.berkeley.edu/taxa/verts/reptilia/
    title: UCMP Berkeley — Reptilia / marine reptile context
    tier: 2
    accessed: "2026-07-16"
review:
  science: required
  ethics: not-applicable
  editor: pending
iucn:
  category: EX
  assessment_date: "2026-07-16"
  scope: global
  population_trend: extinct
welfare:
  state: unknown
  dominant_stressor: extinction-event
  confidence: expert-opinion
sensitivity:
  tier: public
  rationale: Extinct taxon; no live-location sensitivity.
  generalized_to: global
consensus_state: {t["consensus"]}
last_verified: "2026-07-16"
stats:
  period: "{t["period"]}"
  clade: "{t["clade"]}"
  length: "{t["length"]}"
  diet: "{t["diet"]}"
  locomotion: "{t["locomotion"]}"
  habitat: "{t["habitat"]}"
compare:
{compare_yaml}
outputs:
  website_path: /species/marine-reptiles/{t["slug"]}
  github_path: content/species/marine-reptiles/{t["slug"]}.md
  map_layer: false
impact:
  claim: Published a sourced deep-time encyclopedia entry for {t["title"]} with concept reconstruction media.
  eligible_for_hypercert: false
contributors:
  - github: frankxai
license: CC-BY-4.0
media:
  primary:
    asset_id: blc-concept-{t["slug"]}-01
    path: public/media/species/{t["slug"]}.png
    public_media_url: /media/species/{t["slug"]}.png
    source_url: https://github.com/frankxai/blue-life-commons
    original_media_url: /media/species/{t["slug"]}.png
    creator: Blue Life Commons / Grok Imagine concept reconstruction
    credit: Concept reconstruction — not fossil evidence
    license: CC-BY-4.0
    rights_status: concept-reconstruction
    alt_text: Photoreal concept reconstruction of {t["title"]}. {t["body"]} Cinematic open-ocean lighting.
    qa_status: approved
  embeds:
    - provider: paleobiology_database
      url: https://paleobiodb.org/
      rights_status: link-backed-source-card
      notes: Authoritative occurrence and taxonomy gateway for fossil taxa.
      domain: paleobiodb.org
  render:
    strategy: approved_primary_image
    public_visual_kind: image
    public_visual_public_use: true
    species_page_visual_slot: true
    species_page_hero_image_allowed: true
    candidate_thumbnail_allowed: false
    candidate_public_use: false
  review:
    primary_status: approved
    curation_decision: approve_concept_reconstruction_deep_time
    checks_complete: 6
    checks_total: 9
    promotion_allowed_now: true
  supporting_assets: []
---

# {t["title"]}

> **Not a dinosaur.** {t["body"]} Hero media is **AI concept reconstruction** — not fossil evidence.

## At a glance

| Field | Value | Source |
|---|---|---|
| Scientific name | *{t["title"]}* | Paleobiology Database / literature |
| Guild | Marine reptiles | — |
| “Ocean dinosaur?” | **No** | Britannica / UCMP context |
| IUCN | **Extinct** (fossil taxon) | Deep-time convention |
| Period | {t["period"]} | Paleobiology literature ranges |
| Clade | {t["clade"]} | — |

## Identification

{t["body"]} Do not reconstruct with bipedal theropod posture.

## Ecology and behavior

Diet and locomotion chips above are literature-typical ranges. Exact soft-tissue color, behavior, and maximum sizes remain model-dependent and need expert review.

## Conservation status and threats

Extinct. No living population or modern recovery pathway.

## How to observe responsibly

Museum mounts and specimen-labeled reconstructions. Prefer peer-reviewed paleontology over entertainment “sea monster” framing.

## How you can help

Support open fossil data, museum science, and literacy that separates **dinosaurs**, **marine reptiles**, and living ocean wildlife.

## Media note

Generated hero media is concept reconstruction only.

## Sources

- Paleobiology Database
- Encyclopaedia Britannica clade overview
- UCMP Berkeley reptile / marine context
'''


def main() -> None:
    for t in TAXA:
        path = DIR / f"{t['slug']}.md"
        path.write_text(render(t), encoding="utf-8")
        print("wrote", path)

    (DIR / "README.md").write_text(
        dedent(
            """
            # Mesozoic Marine Reptiles (Deep Time Ocean Giants)

            Popular culture often calls these animals “ocean dinosaurs.” **They are not dinosaurs.**

            They are **marine reptiles** (and related fully marine reptiles such as thalattosuchian crocodylomorphs) that thrived in Mesozoic seas: mosasaurs, plesiosaurs, pliosaurs, ichthyosaurs, and marine crocs.

            **True dinosaurs** were overwhelmingly terrestrial. A few dinosaurs (e.g. *Spinosaurus*) show aquatic foraging adaptations, but they are still **dinosaurs**, not the classic “sea monster” marine reptiles. Birds are avian dinosaurs; *Hesperornis* is a diving bird — still not a mosasaur/plesiosaur.

            This guild is a **special educational section** of Blue Life Commons with concept-reconstruction media.

            See `docs/deep-time-media-scale-strategy.md` for roster scale, storage, and living-species media plan.
            """
        ).lstrip(),
        encoding="utf-8",
    )
    print("readme ok", len(TAXA))


if __name__ == "__main__":
    main()
