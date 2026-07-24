# For Conservation NGOs

You run volunteer programs, advocacy campaigns, and grant-and-impact reporting — often with a paper-to-spreadsheet bottleneck, oral knowledge lost to staff turnover, and impact reports that feel like output-theater. Blue Life Commons offers a grounded knowledge spine and a way to make contribution feel like a conversation, not a Git lesson.

## What the system gives you

- **A Research-OS starting point** — the public [`marine-mcp`](https://github.com/frankxai/marine-mcp) repository serves reviewed commons records to compatible agents. Dataset cards describe candidate external sources, but this guide does not claim public live-source connectors.
- **A contract for an Ocean Guardian** — a place- or population-scoped agent can be commissioned around named decisions and review boundaries. Its operator, data sources, code, tests, and welfare safeguards must be inspectable before the result is treated as operational.
- **A no-Git on-ramp** — the contribution invariant: most of your field staff, fishers, divers, and volunteers will *never* touch GitHub. They contribute knowledge by voice note, interview, or form; a **commons steward** does the Git step, with attribution and consent recorded.
- **Artifact types built for your ops** — `volunteer-program`, `local-knowledge`, plus region briefings and welfare assessments that ground your advocacy in cited evidence.
- **An impact ledger** — every merged artifact carries an `impact.claim` and may be `eligible_for_hypercert`, giving you a credible, contributor-credited record for grant and sponsor reporting.

## How to use it today

1. **Browse the commons** — open [`CATALOG.md`](../../CATALOG.md). See the partner profiles already published (Mission Blue, Olive Ridley Project, Reef Check, WDC, Point Reyes) for the shape of a credible org artifact.
2. **Write the guardian brief for your place** — name its scope, decisions, allowed data precision, source contracts, review owners, and stopping conditions. Commission an implementation only when its evidence can be reviewed.
3. **Capture local knowledge without a steward bottleneck** — collect a sighting, a seasonal pattern, or a community-managed-bay protocol as a voice note or interview, then hand it to a commons steward who drafts a `local-knowledge` artifact with your contributor's `consent` recorded.
4. **Author an independent organization profile** for your org so agents and researchers can find its work with correct, cited framing. Inclusion does not imply a Blue Life Commons partnership.
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
