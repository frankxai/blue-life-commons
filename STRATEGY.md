# Strategy

Why Blue Life Commons exists, how it is built to last, and how it stays free while the work around it becomes sustainable. This is the thinking behind the repository. For how to *contribute*, see [`README.md`](README.md) and [`CONTRIBUTING.md`](CONTRIBUTING.md); this document is the *why*.

---

## The thesis

Ocean knowledge is abundant but fragmented — scattered across papers, databases, agencies, field notes, and the heads of people who spend their lives near the sea. It is rarely in one reviewed, machine-readable, openly-licensed place that a citizen, a researcher, an agent, or an NGO can all build on.

Blue Life Commons is that place: a reviewed, source-led, CC-BY corpus of ocean intelligence, built in the open, that any human or AI system can read from and contribute to. The bet is simple — **a trusted commons is more valuable than any single product built on top of it**, and it is the one thing a commercial vendor cannot easily replicate, because trust is earned through review, not shipped.

---

## The three-layer system

Ocean intelligence is built in three distinct layers. They are kept separate on purpose — conflating them is how a public good quietly becomes a private one.

| Layer | Repository / surface | What it is | What it creates |
|---|---|---|---|
| **Blue Life Commons** (this repo) | Reviewed knowledge + open workflows + impact ledger | Species pages, region briefings, field missions, dataset cards, sources, ethics rules | **Trust** |
| **Ocean Intelligence System** | [`ocean-intelligence-system`](https://github.com/frankxai/ocean-intelligence-system) | The open-source machinery that *acts on* the commons — data connectors, Guardian agents, MCP servers, dashboards | **Continuity** |
| **Starlight Marine Intelligence Systems** | Commercial | Implementation, design, institutional adoption, media | **Reach** |

**The hard boundary.** Each layer reads from the one above it and never overrides it. The commons defines scientific truth, citation standards, and wildlife-interaction ethics; the software layer *applies* those standards and never interprets around them; the business *implements and distributes* and never sells access to the knowledge itself. Knowledge flows down; money never flows up into gating the knowledge.

**Why the separation is load-bearing.** If the business could edit the commons to suit a client, the commons would stop being trustworthy — and its entire value is its trustworthiness. The wall between the layers is what makes the free layer worth building on.

---

## The operating model

Everything in this repository runs on one loop:

```
Person / Researcher / Agent / NGO
        │
        ▼
GitHub Issue  ·  Mission  ·  Research Request
        │
        ▼
AI-assisted contribution
        │
        ▼
Pull Request
        │
        ▼
Review:  sources · ethics · quality
        │
        ▼
Published artifact
  (website · map · notebook · MCP · report · film)
        │
        ▼
Impact record  +  contributor credit
```

Two rules keep the loop honest:

> **Every conversation becomes an artifact.** A discussion that does not end in a reviewed, sourced, openly-licensed artifact did not happen. The artifact is the unit of work, not the conversation about it.

> **Discord discusses. GitHub decides. Website publishes. Ledger records.** Ideas can start anywhere, but decisions live in issues and PRs, published knowledge lives on the website, and impact lives in the ledger. Nothing important is left in a chat log.

This repository is the machine room: the reviewed source of truth from which every public page, map, lesson, MCP response, and impact record is generated.

---

## What stays free, and what the work around it earns

The commons is free forever. Sustainability comes from the *work around* the knowledge, never from gating the knowledge.

| Free, forever (the commons) | What the business does (Starlight Marine Intelligence Systems) |
|---|---|
| Species pages, region briefings, field missions | NGO Research-OS setup and hosting |
| Dataset cards, source registries, ethics rules | Regional ocean-intelligence portals |
| Open-source templates + validation tooling | School / university workshops |
| Basic MCP connectors + agent skills | Custom partner dashboards + data connectors |
| Educational content + contributor onboarding | Research-to-public media packages, grant support |

The business sells **speed, implementation, design, integration, and institutional reliability** — never access to ocean knowledge. Full commercial and funding architecture: [`governance/funding.md`](governance/funding.md).

---

## How it compounds

The commons is designed so that effort accumulates rather than evaporates:

- **Impact records.** Reviewed work opts into structured impact claims (Hypercerts) — what was done, by whom, with evidence that accrues over time. Contributors carry their credit with them. See [`governance/funding.md`](governance/funding.md).
- **Staged governance.** Founder-led today; a maintainer council and proposal governance are added only when there is real treasury, real contributors, and real decisions — not before. Governance theater is avoided by design. See [`governance/README.md`](governance/README.md).
- **Standards that never bend.** Scientific truth, animal-safety rules, citation standards, and expert-review requirements are *standards, not votes* — they are never subject to community or commercial pressure. See [`ETHICS.md`](ETHICS.md) and [`SOURCES.md`](SOURCES.md).

---

## Where this sits in the wider ecosystem

Blue Life Commons is the Ocean Intelligence System of the broader FrankX ecosystem — one architecture on a shared substrate. See [`ECOSYSTEM.md`](ECOSYSTEM.md) for how it composes with the Starlight Intelligence substrate, the [`marine-mcp`](https://github.com/frankxai/marine-mcp) corpus server, and the [`marine-agent-skills`](https://github.com/frankxai/marine-agent-skills) skill pack.

---

*The commons stays free. The work around it becomes sustainable. Trust is the asset, and it is earned one reviewed artifact at a time.*
