# ETHICS.md — Wildlife Guidance Ethics Policy

All content in Blue Life Commons that touches living animals — field missions, observation guides, species pages, tourism guidance — must comply with this policy. Ethics review is **required** for any artifact involving animal interaction, and is recorded in the artifact's metadata (`review.ethics`).

## Core principles

1. **Animal welfare over content value.** If guidance could plausibly cause disturbance, stress, habitat damage, or behavioral change in wildlife, it does not ship.
2. **Distance first.** All observation guidance must specify minimum approach distances consistent with local regulations and recognized guidelines (e.g., national marine mammal viewing rules). When regulations differ, cite the strictest applicable standard.
3. **No interaction promotion.** Do not encourage touching, feeding, baiting, chasing, surrounding, or swimming-with programs for wild animals unless operated under documented scientific or regulatory permits — and even then, describe rather than promote.
4. **No location precision for vulnerable populations.** Do not publish exact haul-out sites, nesting beaches, den locations, or aggregation coordinates for sensitive or exploited species. Use regional granularity.
5. **Legal compliance is the floor, not the ceiling.** Cite applicable laws (e.g., habitat directives, marine mammal protection acts, local protected-area rules) and exceed them where welfare science suggests.
6. **No anthropomorphic claims as fact.** Do not claim to translate, interpret, or speak for animals. Behavioral interpretation must be cited to published research.
7. **No invented conservation claims.** Population status, threat level, and trend statements require citations to recognized authorities (e.g., IUCN Red List, regional monitoring programs).

## Field mission requirements

Every field mission must include:

- Minimum distances and disengagement rules ("when to leave")
- Signs of disturbance for the target species, with sources
- Seasonal sensitivities (breeding, pupping, nesting, molting)
- Local regulations and permit requirements
- A "do no harm" section that overrides all other instructions

## Welfare beyond constraint

The rules above are the floor — what not to do. The animals' positive interest in recovering and flourishing is a first-class concern, represented in [WELFARE.md](WELFARE.md) (the Five Domains, the disturbance budget, welfare-as-state). Harm is **cumulative**: an artifact or guardian must reason about total human pressure on a place/population, not only single-actor compliance.

## Rehabilitation, sanctuary & individual animals

Artifacts about stranding response, rehabilitation, sanctuaries, and individual animals (`rehab-case-card`, `stranding-protocol`, `release-criteria`, `sanctuary-profile`, `husbandry-guide`, `necropsy-summary`, and any artifact with `individual_animal: true`) carry the strictest rules:

1. **No precise locations of live animals — ever.** This extends the vulnerable-taxa location rule to *every* animal in rehab, in transport, and **post-release** (released/tagged animals are harassment targets). Regional granularity only; telemetry tracks are aggregated and delayed, never live-public.
2. **The system assembles evidence; it never adjudicates.** Dosing, euthanasia, and releasability are decisions for licensed veterinarians and the responsible authority (e.g., the NOAA Regional Administrator). An artifact or guardian may compile evidence against published criteria and must stay silent on the verdict — *grounded or silent extends to evidence, never verdict*.
3. **Release > lifelong captivity is the default.** Sanctuary residency for non-releasable animals is the justified exception, never framed as a happy outcome. **No glamorizing captivity.**
4. **Individual-animal dignity.** Case cards are de-identified; "patient story" content never overrides welfare (welfare-over-content holds). Donor storytelling around a named animal must not compromise the animal's interests or location.
5. **Honesty about invasiveness.** Tagging, sampling, and handling are described plainly with their welfare cost, never euphemized.
6. **Clinical content is review-gated and credentialed.** Triage, dosing, and medical protocols set `review.ethics: required` and `review.science: required`; reviewers should include relevant veterinary/rehabilitation expertise.

## Review process

- Artifacts with `review.ethics: required` cannot be published until an ethics reviewer approves.
- Ethics reviewers may block publication regardless of other approvals.
- Animal safety rules are **not subject to governance votes**. They are standards.

## Reporting concerns

Open an issue labeled `needs-expert-review` describing the concern. Do not debate animal welfare in chat channels — bring it to GitHub where decisions are recorded.
