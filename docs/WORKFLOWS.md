# WORKFLOWS.md — Who this serves, how they work, and what we build for them

Blue Life Commons and the Ocean Intelligence System exist to serve real people doing real work for real animals. This document maps those workflows, names the animal's own needs, and sets the build roadmap. It is the synthesis of a four-lens practitioner review (rescue/rehab/sanctuary · animal-welfare science · field research · NGO/community ops), 2026-06-16.

## The people we serve

| Audience | Core workflow | Where it breaks today | What we give them |
|---|---|---|---|
| **Rescue / rehab / sanctuary** | stranding call → triage → transport → rehab → release decision → post-release; lifelong husbandry for non-releasable animals | paper forms re-keyed into 3 systems; no live facility-capacity view; tribal protocol knowledge | `stranding-protocol`, `rehab-case-card`, `release-criteria`, `sanctuary-profile`, `husbandry-guide`; a sanctuary/stranding guardian that *assembles evidence, never adjudicates* |
| **Field researchers** | question → permits → field collection (photo-ID/tag/acoustic/eDNA/transect) → data mgmt → analysis → publication | data dies on hard drives; Darwin Core mapping is manual and late; claim↔evidence link severed at publication | `notebook` artifacts wired to connectors; modality dataset subtypes; a contribute→DOI pipeline; the provenance spine |
| **NGOs & coastal communities** | volunteer programs; advocacy campaigns; grant/impact reporting; community-managed bays/reefs | paper→spreadsheet bottleneck; oral knowledge lost to turnover; output-theater impact reports | `volunteer-program`, `local-knowledge`, impact-report generation; a no-Git conversational on-ramp |
| **Educators, creators, coastal residents** | learn, translate, watch a local place | knowledge stuck in PDFs; nothing place-scoped and plain-language | `lesson` packs grounded in species pages; a community monthly-briefing guardian |

**The contribution invariant (for non-coders):** contribution is a *conversation or a form*; the review/attestation/commit layer is invisible. Most NGO staff, fishers, divers, and volunteers will never touch GitHub — a **commons steward** does the Git step; they contribute knowledge by voice note, interview, or form.

## The animals we serve

Welfare is not only a constraint on us — it is an interest we actively represent. See [WELFARE.md](../WELFARE.md). The core moves:

- **From "do no harm" to "support recovery."** Per-actor distance rules can't stop the *cumulative* harm of the fiftieth boat — so we model a **disturbance budget** (a place/season's carrying capacity for human pressure) and watch utilization, not just compliance.
- **Welfare as a queryable state**, not buried prose: a `welfare` block (state · dominant stressor · Five Domains · confidence) every guardian inherits.
- **Center interests, not feelings.** Affect is inferred only from validated, cited physiological/behavioural correlates, confidence-tagged — never narrated.
- **Help carries cost.** Rescue, rehab, tagging, and approach have welfare footprints. Release > lifelong captivity is the default; the system assembles clinical evidence but never adjudicates dosing/euthanasia/releasability (licensed-vet and authority decisions).
- **Unusual Mortality Events** (NOAA's 7 criteria) are the clearest early alarm — a stranding-rate anomaly escalates a guild.

## What shipped 2026-06-16 (this pass)

- **`WELFARE.md`** — the welfare doctrine (Five Domains, disturbance budget, anti-anthropomorphism positive vocabulary, UME).
- **`ETHICS.md`** — new § *Rehabilitation, sanctuary & individual animals* (no live-animal locations ever, evidence-never-verdict, release>captivity, dignity, honesty about invasiveness).
- **Schema** — 9 new types (welfare/rehab/sanctuary/community) + `welfare`, `disturbance_budget`, `individual_animal`, `last_verified`, `consent` fields.
- **Integrity lint** — new science-sensitive types enforced; **location guardrail in code**: a live/individual-animal artifact with precise coordinates fails CI.
- **Templates** — `welfare-assessment`, `sanctuary-profile`, `stranding-protocol`, `local-knowledge`.
- **Guardian archetypes** (in `ocean-intelligence-system`) — `sanctuary-guardian`, `stranding-network-guardian`.

## Roadmap (specced, not yet built — ranked by leverage)

1. **No-Git conversational on-ramp** (WhatsApp/web/voice → draft artifact → steward review). The gate that makes the commons real for non-coders. *Highest leverage.*
2. **The learning loop / contradiction feedback** — `last_verified` is the field; the missing machinery is post-approval invalidation ("approved ≠ still true") + a study-area-watch guardian that flags when new data contradicts an approved claim.
3. **Provenance spine** — version-pinned DOI + accessed-date + dataset license + connector-version on every cited record (the precondition for trust). Partly seeded (`last_verified`, per-source `license`/`tier`).
4. **`notebook` artifact wired to the tested connectors** — turns reproducible analysis into a commons object (research flow-in).
5. **Contribute → Darwin Core → Zenodo DOI → hypercert pipeline** — converts dead hard-drive data into citable knowledge; attacks the #1 documented research friction.
6. **Modality dataset subtypes** (`edna`/`acoustic`/`photo-id`/`transect`) + Movebank/Happywhale/Wildbook bridges — where the world's marine-individual and movement data actually live.
7. **New welfare connectors** — vessel-noise/AIS-density (the dominant unmodeled chronic stressor), SST/HAB, NOAA stranding feeds (UME), feeding the disturbance budget.
8. **Impact-report generator + `lesson`/`research-to-public` translation** — flow-out: relieve the most-hated NGO ops pain and stop knowledge dying in PDFs.

> Built on SIP · Blue Life Commons. We measure success one way: does this help someone protect the sea — and does it serve the animal, not just the content?
