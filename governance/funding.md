# Funding Architecture

The commons stays free. The business sells implementation. Funding records impact — it does not become the religion.

## Principles

- **No early token.** No speculative assets, no fake decentralization before there is actual work.
- **Mature primitives only.** Use established public-good funding tools.
- **Fundable impact objects, not vague donation asks.** Sponsors fund specific, evidenced work.

## The stack

| Need | Tool |
|---|---|
| Fiat donations, invoices, fiscal host | Open Collective |
| Maintainer funding | GitHub Sponsors |
| Web3 public-good grants | Gitcoin / Giveth |
| Governance votes (Stage 3 only) | Snapshot |
| Impact records | Hypercerts |
| Grant/community workspace | CharmVerse |
| Archival research releases | Zenodo |
| ML datasets/models | Hugging Face |

## Impact records (Hypercerts)

A hypercert is a structured claim about work: what was done, by whom, when, and where — with evidence accumulating over time.

Artifacts opt in via metadata:

```yaml
impact:
  claim: "Created educational field mission for ethical seal observation."
  eligible_for_hypercert: true
```

Evidence for a claim includes: GitHub commits, merged PRs, published pages, partner feedback, traffic, educational usage, and completed field missions.

Example impact claims:

- "Built open-source field mission templates for ethical seal observation."
- "Published 25 species intelligence pages with source review."
- "Created GitHub/Markdown onboarding kit for marine researchers."
- "Mapped 100 ocean organizations into partner directory."
- "Ran Blue Life student contribution sprint."

Sponsors can fund: future work, retroactive work, a specific species guild, a specific region, or a specific researcher workflow.

## What stays free vs. what the business charges for

**Commons (free, forever):** public guides, open-source templates, species pages, region briefs, basic MCPs, field missions, educational content, contributor onboarding.

**Business (Starlight Marine Intelligence Systems):** NGO Research OS setup, regional ocean intelligence portals, school/university workshops, eco-tourism education systems, custom partner dashboards, research-to-public media packages, grant/proposal support, custom MCP/data connectors, sponsor-funded open-source programs.

The business never sells access to ocean knowledge. It sells speed, implementation, design, integration, and institutional reliability.

## Legal posture

1. Start under the existing business; keep accounting separate by project.
2. Use Open Collective or a fiscal host when donations become meaningful — a fiscal host can hold funds, generate invoices/receipts, handle compliance, and pay approved expenses.
3. Create a foundation/association only after traction.

## Proposals

Funding proposals are artifacts: `governance/proposals/<proposal-slug>.md` with `type: funding-proposal` frontmatter, reviewed like any other contribution.
