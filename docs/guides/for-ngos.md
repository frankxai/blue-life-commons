# For Conservation NGOs

You run volunteer programs, advocacy campaigns, and grant-and-impact reporting — often with a paper-to-spreadsheet bottleneck, oral knowledge lost to staff turnover, and impact reports that feel like output-theater. The Ocean Intelligence System gives your team a grounded operating spine and a way to make contribution feel like a conversation, not a Git lesson.

## What the system gives you

- **A Research-OS starting point** — the [`ocean-intelligence-system`](https://github.com/frankxai/ocean-intelligence-system) ships connectors to occurrence, protected-area, and fishing-effort data (OBIS, GBIF, WoRMS, NOAA Coral Reef Watch, Protected Planet), each normalized with provenance carried through.
- **An Ocean Guardian for your work** — a place- or population-scoped agent that turns raw feeds into briefings your team and supporters can actually read. A `coastal-community-guardian` or `species-guardian` watches the signals you can't watch full-time and explains what changed.
- **A no-Git on-ramp** — the contribution invariant: most of your field staff, fishers, divers, and volunteers will *never* touch GitHub. They contribute knowledge by voice note, interview, or form; a **commons steward** does the Git step, with attribution and consent recorded.
- **Artifact types built for your ops** — `volunteer-program`, `local-knowledge`, plus region briefings and welfare assessments that ground your advocacy in cited evidence.
- **An impact ledger** — every merged artifact carries an `impact.claim` and may be `eligible_for_hypercert`, giving you a credible, contributor-credited record for grant and sponsor reporting.

## How to use it today

1. **Browse the commons** — open [`CATALOG.md`](../../CATALOG.md). See the partner profiles already published (Mission Blue, Olive Ridley Project, Reef Check, WDC, Point Reyes) for the shape of a credible org artifact.
2. **Stand up a guardian for your place** — fork the Ocean Guardian framework, pick the closest archetype in `ocean-intelligence-system/guardians/archetypes/` (`coastal-community-guardian`, `bay-guardian`, `reef-guardian`, `species-guardian`), and run the Ningaloo demo (`guardians/demo_ningaloo.py`) to see the full pipeline execute offline before you wire your own.
3. **Capture local knowledge without a steward bottleneck** — collect a sighting, a seasonal pattern, or a community-managed-bay protocol as a voice note or interview, then hand it to a commons steward who drafts a `local-knowledge` artifact with your contributor's `consent` recorded.
4. **Author a partner profile** for your org so agents and researchers surface your work with correct, cited framing.
5. **Generate impact records** from merged artifacts for your next grant report — the `impact.claim` field is designed to be lifted directly.

## The rules that apply to you

- **Advocacy must stay inside the evidence.** Welfare assessments center the animal's *interests*, not feelings, with cited, confidence-tagged proxies ([`WELFARE.md`](../../WELFARE.md)). "Support recovery," not "the seals are frightened."
- **No precise locations** of vulnerable populations or individual animals — regional granularity only ([`ETHICS.md`](../../ETHICS.md)).
- **Consent and attribution** for community knowledge: the `consent` field records who shared it, their permission, and attribution preference. Don't publish a community's knowledge without it.
- **Decisions are recorded, not chatted.** Don't debate welfare in Discord — bring it to a GitHub issue. *Discord discusses. GitHub decides.*
- **No invented conservation claims.** Population, threat, and legal-protection statements need citations to recognized authorities.

## Your first contribution

**Author a partner profile for your organization.** It's the natural first artifact — you're the expert on your own work — and it plugs your org into the commons so every downstream agent, researcher, and journalist references you accurately. Open an `artifact-request` issue in [`.github/ISSUE_TEMPLATE/`](../../.github/ISSUE_TEMPLATE/), or have a steward do it, and use an existing profile in `content/partners/` as your template.

> Built on SIP · Blue Life Commons (CC-BY-4.0).
