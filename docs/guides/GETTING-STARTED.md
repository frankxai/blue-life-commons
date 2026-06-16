# Getting Started with the Ocean Intelligence System

Welcome. You're holding the front door to an **open-source Ocean Intelligence commons** — a place where ocean curiosity becomes useful, reviewed, citable knowledge that humans *and* AI agents can trust.

This guide gives you the whole system in one read: what it is, how the three layers fit together, a five-minute tour, how to plug it into your AI assistant, and how to make your first contribution — whether or not you use Git.

---

## What this is

Blue Life Commons turns a conversation about whales, seals, turtles, sharks, rays, or reefs into an **artifact**: a species page, a region briefing, a field mission, a welfare assessment, a dataset card. Every artifact is schema-validated, sourced, ethics-checked, and reviewed before it counts as fact. Nothing ships on vibes.

The promise underneath everything:

> **Grounded or silent.** Every factual claim traces to a real source. No invented populations, no anthropomorphic "what the whale is saying," no precise locations of vulnerable animals. If it isn't sourced and reviewed, the system stays quiet rather than guess.

The knowledge stays free forever (CC-BY-4.0). The animals come first — their welfare is not just a constraint on what we publish, it's an interest the system actively represents (see [`WELFARE.md`](../../WELFARE.md)).

---

## The three-layer triad

Ocean intelligence is built in three deliberately separate layers. Keep them distinct — it's what makes the trust hold.

| Layer | Repo | What it is | What it creates |
|---|---|---|---|
| **Blue Life Commons** | [`blue-life-commons`](https://github.com/frankxai/blue-life-commons) | The reviewed knowledge corpus — species pages, region briefings, field missions, welfare assessments, dataset cards, sanctuary/rehab/stranding artifacts, templates. Schema-validated and integrity-linted in CI. | **Trust** |
| **Ocean Intelligence System** | [`marine-mcp`](https://github.com/frankxai/marine-mcp) + [`marine-agent-skills`](https://github.com/frankxai/marine-agent-skills) + [`ocean-intelligence-system`](https://github.com/frankxai/ocean-intelligence-system) | The working software — an MCP server that serves the corpus to AI agents, a Claude Code skill pack for authoring compliant artifacts, and the Ocean Guardian framework (place-scoped agents + a Python connector layer to OBIS, GBIF, WoRMS, Coral Reef Watch, Protected Planet). | **Continuity** |
| **Starlight Marine Intelligence Systems** | (commercial) | Implementation, design, institutional adoption, media. Sells speed and reliability — never access to ocean knowledge. | **Reach** |

The commons stays free. The business sells implementation, never access. The hard boundary: every software layer **reads** the commons and can never override its science, sourcing, or ethics standards.

---

## The hard rule (and its corollary)

> Every conversation becomes an issue. Every issue becomes an artifact. Every artifact becomes public knowledge, partner leverage, or funded impact.

> Discord discusses. GitHub decides. Website publishes. Ledger records.

Decisions are made where they're recorded. That's why animal-welfare debates go to a GitHub issue, never a chat thread.

---

## 5-minute tour

1. **Read the README** — [`README.md`](../../README.md). The core model, the three layers, the hard rule.
2. **Browse the catalog** — [`CATALOG.md`](../../CATALOG.md) is the living, auto-generated index of every published artifact (species pages, region briefings, missions, dataset cards, partner profiles), grouped by type. This is the fastest way to see what already exists.
3. **Read one gold-standard artifact** — open [`content/species/turtles/green-turtle.md`](../../content/species/turtles/green-turtle.md). Notice the YAML frontmatter (machine-readable metadata), the `## At a glance` source table, the dated IUCN status, and the **"This page does not provide approach guidance"** discipline. That's the quality bar.
4. **Read the welfare doctrine** — [`WELFARE.md`](../../WELFARE.md). The Five Domains, the disturbance budget, welfare-as-a-queryable-state. This is what separates us from a wiki.
5. **Pick your guide** — open [`docs/guides/README.md`](README.md) and jump to the guide written for *your* role. Ten audiences, each with a concrete "how to use it today" walkthrough.

---

## Install `marine-mcp` (serve the commons to your AI assistant)

`marine-mcp` is a review-gated MCP server. It lets Claude Desktop, Claude Code, or Cursor query the reviewed corpus — and it returns a curated body **as fact only when that artifact is review-approved**, otherwise a typed refusal that names the status. Every response carries its `sources[]`.

**1. Clone and build:**

```bash
git clone https://github.com/frankxai/marine-mcp
cd marine-mcp
npm install
npm run build
```

**2. Add it to Claude Desktop** (`claude_desktop_config.json`) or Claude Code (`.mcp.json`):

```json
{
  "mcpServers": {
    "marine": {
      "command": "node",
      "args": ["/abs/path/to/marine-mcp/dist/index.js"],
      "env": { "BLC_PATH": "/abs/path/to/blue-life-commons" }
    }
  }
}
```

`BLC_PATH` points at your local checkout of `blue-life-commons`. Restart your client.

**3. Ask your assistant a grounded question:**

> "Use the marine tools to search for green turtle and get its details."

Behind the scenes it calls `search_species`, then `get_species_details` — and if the page is still `needs-expert-review`, you get a typed refusal naming the status instead of unreviewed prose. That refusal *is* the feature.

**The tools:** `search_species`, `get_species_details`, `get_region_briefing`, `get_active_missions`, `lookup_source`, `validate_artifact`, `obis_gbif_passthrough` (live OBIS/GBIF occurrences, explicitly labelled `unreviewed: true`).

---

## How to contribute

### If you use Git (researchers, developers, NGO staff with technical capacity)

1. Read [`CONTRIBUTING.md`](../../CONTRIBUTING.md), [`AGENTS.md`](../../AGENTS.md), [`ETHICS.md`](../../ETHICS.md), and [`SOURCES.md`](../../SOURCES.md).
2. Open or claim an issue using a template in [`.github/ISSUE_TEMPLATE/`](../../.github/ISSUE_TEMPLATE/) (`artifact-request`, `field-mission`, `research-request`).
3. Author your artifact with the metadata schema in [`schema/artifact-schema.md`](../../schema/artifact-schema.md), reusing an existing template (e.g. `content/welfare/_templates/welfare-assessment-template.md`).
4. Using a coding agent? Install [`marine-agent-skills`](https://github.com/frankxai/marine-agent-skills) and run the pipeline: `/species-page` or `/field-mission` → `/source-verify` → `/ethics-check` → `/validate-artifact` → `/open-artifact-pr`.
5. Open a pull request. Review checks **sources, ethics, and clarity**. Once merged, your artifact flows to the website, map, academy, and impact ledger — with your credit attached.

### If you don't use Git (fishers, divers, volunteers, community elders, most NGO field staff)

**Contribution is a conversation, not a commit.** The contribution invariant: the review/attestation/commit layer is *invisible* to you. You bring the knowledge — by voice note, interview, photo, or a filled-in form — and a **commons steward** does the Git step on your behalf, with your attribution and consent recorded (`consent` field in the schema).

The fastest path today: open an issue describing what you know (a sighting, a local pattern, a stranding protocol your team uses) using the issue templates, and tag it for a steward. The no-Git conversational on-ramp (WhatsApp/web/voice → draft artifact → steward review) is the highest-leverage item on the roadmap in [`docs/WORKFLOWS.md`](../WORKFLOWS.md).

---

## The rules that bind everyone

These are standards, not popularity contests. They are never subject to community vote:

- **Every factual claim needs a source** — [`SOURCES.md`](../../SOURCES.md). No source, no claim.
- **Animal welfare over content value** — [`ETHICS.md`](../../ETHICS.md). If it could disturb wildlife, it doesn't ship.
- **No precise locations of vulnerable or individual animals** — ever. Regional granularity only; this extends to post-release tagged animals.
- **The system assembles evidence; it never adjudicates.** Dosing, euthanasia, and releasability are decisions for licensed vets and the responsible authority — *grounded or silent extends to evidence, never verdict.*
- **No anthropomorphic claims as fact.** No translating animals.

---

## Where to go next

- Find your role in [`docs/guides/README.md`](README.md) and read your guide.
- See a guardian run end-to-end: [`ocean-intelligence-system/docs/case-study-ningaloo.md`](https://github.com/frankxai/ocean-intelligence-system/blob/main/docs/case-study-ningaloo.md).
- Read the welfare orientation in [`WELFARE.md`](../../WELFARE.md) — it's the soul of the project.

> Built on SIP · Blue Life Commons (CC-BY-4.0).
