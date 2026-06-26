# Blue Life Commons

Blue Life Commons is an open-source **Ocean Intelligence commons** where citizens, researchers, developers, educators, travelers, and conservation organizations turn ocean curiosity into useful artifacts: species guides, field missions, maps, research summaries, datasets, notebooks, MCP tools, films, and local action systems.

[![Catalog](https://img.shields.io/badge/catalog-living%20index-0f766e)](CATALOG.md)
[![Sources](https://img.shields.io/badge/sources-required-2563eb)](SOURCES.md)
[![Ethics](https://img.shields.io/badge/ethics-review%20gated-7c3aed)](ETHICS.md)
[![Agents](https://img.shields.io/badge/agents-PRs%20not%20direct%20commits-f59e0b)](AGENTS.md)
[![License: CC BY 4.0](https://img.shields.io/badge/content-CC%20BY%204.0-0891b2)](https://creativecommons.org/licenses/by/4.0/)

An initiative by Starlight Intelligence Systems — starting with whales, dolphins, seals, sea lions, turtles, sharks, rays, and reef ecosystems.

## 90-second start

Choose the lane that matches why you are here:

| I want to... | Start with |
|---|---|
| Browse published artifacts | [`CATALOG.md`](CATALOG.md) |
| Contribute a species page, region briefing, mission, or dataset card | [`CONTRIBUTING.md`](CONTRIBUTING.md) |
| Use a coding agent safely | [`AGENTS.md`](AGENTS.md) |
| Check source requirements | [`SOURCES.md`](SOURCES.md) |
| Check wildlife interaction rules | [`ETHICS.md`](ETHICS.md) |

Fast local checks:

```bash
python scripts/build_catalog.py --check
python scripts/validate_artifacts.py
python scripts/lint_content.py
```

## The hard rule

> Every conversation becomes an issue. Every issue becomes an artifact. Every artifact becomes public knowledge, partner leverage, or funded impact.

And its corollary:

> Discord discusses. GitHub decides. Website publishes. Ledger records.

## The core model

```
Person / Researcher / Agent / NGO
        ↓
GitHub Issue / Mission / Research Request
        ↓
AI-assisted contribution
        ↓
Pull Request
        ↓
Review: source, ethics, quality
        ↓
Website / Map / Notebook / MCP / Report / Film
        ↓
Impact record + contributor credit
        ↓
Funding, sponsorship, grants, reputation
```

Every action must end as an artifact. This repository is the machine room: the source of truth from which public pages, maps, lessons, and impact records are generated.

## The three-layer system

| Layer | Surface | Role |
|---|---|---|
| **Blue Life Commons** (this project) | Public-good knowledge + open-source workflows + impact ledger | Creates trust |
| **Ocean Intelligence OS** | Productized software + agent systems + dashboards + partner portals | Creates continuity |
| **Starlight Marine Intelligence Systems** | Business / implementation / media / institutional adoption | Creates reach |

The commons stays free. The business sells speed, implementation, design, integration, and institutional reliability — never access to ocean knowledge.

## Repository structure

```
blue-life-commons
├── content/              # species, regions, guides — versioned knowledge
│   ├── species/          # species guilds: cetaceans, pinnipeds, turtles, sharks-rays, reefs
│   └── regions/          # regional ocean briefings
├── missions/             # citizen science + travel field missions
├── schema/               # the metadata schema that connects every artifact
├── agent/                # agent harness: role briefs for coding agents
├── governance/           # funding architecture, governance stages, impact records
├── docs/                 # contributor onboarding, researcher guides
└── .github/              # issue templates, PR template, validation workflows
```

## Browse the commons

[`CATALOG.md`](CATALOG.md) is a living, auto-generated index of every published artifact (species pages, region briefings, missions, dataset cards, partner profiles), grouped by type. Regenerate it with `python scripts/build_catalog.py`; CI fails if it is stale.

## How to contribute

1. Read [CONTRIBUTING.md](CONTRIBUTING.md) and pick an artifact class (species page, region briefing, field mission, dataset card, MCP connector, translation, lesson…).
2. Find or open an issue using the templates in `.github/ISSUE_TEMPLATE/`.
3. Create your artifact with the metadata schema in [schema/artifact-schema.md](schema/artifact-schema.md).
4. Open a pull request. Reviews check **sources, ethics, and clarity**.
5. Once merged, your artifact flows to the website, map, academy, and impact ledger — with your credit attached.

Using a coding agent (Claude Code, Codex, Cursor)? Start at [AGENTS.md](AGENTS.md).

## Agent tooling (the IS-engine)

Two companion repos let any agent work the commons safely:

- **[`marine-mcp`](https://github.com/frankxai/marine-mcp)** — a review-gated MCP server that serves this corpus to agents. It returns a curated body *as fact* only when the artifact is review-approved, and carries `sources[]` through every response (`grounded or silent`).
- **[`marine-agent-skills`](https://github.com/frankxai/marine-agent-skills)** — a Claude Code skill pack (`/species-page`, `/field-mission`, `/ethics-check`, `/source-verify`, `/validate-artifact`, `/open-artifact-pr`) so contributions are schema-valid, sourced, and ethics-checked before the PR.

## Non-negotiable standards

These are standards, not popularity contests, and are never subject to community vote:

- Scientific truth and citation standards — see [SOURCES.md](SOURCES.md)
- Animal safety and wildlife interaction rules — see [ETHICS.md](ETHICS.md)
- Expert review requirements for science-sensitive content

## License

Content is licensed [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/) unless an artifact's metadata states otherwise. Code is open source.
