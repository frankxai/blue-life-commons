# Operating Team

Last updated: 2026-07-05

The platform needs a small, explicit operating team. A "team" can be humans, agents, or a mixed crew, but the handoffs must stay visible in issues, PRs, review packs, and scorecards.

## Roles

| Role | Owns | Must produce |
|---|---|---|
| Product Orchestrator | PRD, priorities, scorecard, release intent | Product issue/PR brief, scorecard update, decision log |
| Research And Source Lead | Scientific sources, platform benchmarks, source quality | Source list, claim notes, source tier review |
| Taxonomy Integrator | Scientific names, identifiers, guild placement | Taxon match notes, WoRMS/OBIS/GBIF/EOL/FishBase lane decisions |
| Media Rights Curator | Image candidates, licenses, credits, approved/blocked surfaces | Approval queue updates, rights notes, promotion report |
| Welfare And Ethics Reviewer | Animal safety, sensitive locations, captions, crops | Ethics notes, blocked-risk reasons, safe wording |
| Partner Grant Lead | Official, NGO, sanctuary, photographer, and institution outreach | Media-intake issues, outreach packets, permission terms |
| Platform Engineer | App, Blob storage, render contract, validation scripts, deployments | Passing checks, preview/production verification, cost notes |
| Visual QA Lead | Desktop/mobile rendering, alt text, layout, public audit board | Screenshots, visual QA notes, accessibility risks |
| Community Steward | Contributor experience, issue triage, no-Git intake handoff | Clean issues, contributor follow-up, stewarded artifacts |
| Release Captain | Merge discipline, Vercel deployment, production verification | PR checklist, deployment URL, route verification |

## RACI

| Work item | Responsible | Accountable | Consulted | Informed |
|---|---|---|---|---|
| New species page | Research Lead | Product Orchestrator | Taxonomy, Ethics | Community |
| New primary image | Media Rights Curator | Product Orchestrator | Ethics, Visual QA, Partner Lead | Community |
| Partner image grant | Partner Grant Lead | Product Orchestrator | Media Rights, Ethics | Platform |
| Public route change | Platform Engineer | Release Captain | Visual QA, Product | Community |
| Source benchmark update | Research Lead | Product Orchestrator | Platform, Partner Lead | Community |
| Production release | Release Captain | Product Orchestrator | Platform, Visual QA | Community |

## Agent Execution Pattern

Use specialized agents or role prompts only when the output has a clear artifact:

| Agent lane | Input | Output |
|---|---|---|
| Research scout | Species or platform target | Source packet with URLs, licenses, and uncertainty |
| Rights reviewer | Candidate media record | Approve/block recommendation with exact missing fields |
| Welfare reviewer | Image/caption/source context | Safety notes and sensitive-location decision |
| Product analyst | Scorecard and analytics | KPI update and next experiment |
| Release verifier | Preview/production URL | Route checks and residual risk notes |

Avoid a vague "God Agent" pattern. The orchestrator coordinates; specialists produce reviewable evidence; release captain verifies the public result.

## Handoff Contract

Every handoff includes:

- `artifact_id` or issue number
- species page path
- source URL and original media URL when applicable
- rights status and missing fields
- species-match basis
- welfare/sensitive-location notes
- reviewer-only/public-safe boundary
- exact next command or next human action

## Escalation Rules

| Trigger | Escalate to |
|---|---|
| License unclear or commercial-use ambiguity | Media Rights Curator |
| Third-party image credited on official page | Media Rights Curator and Partner Grant Lead |
| Live animal location or individual animal risk | Welfare And Ethics Reviewer |
| Taxon ambiguity | Taxonomy Integrator |
| Candidate URL appears in public manifest | Platform Engineer and Release Captain |
| Monthly Blob transfer cost exceeds planned threshold | Platform Engineer |
| Official domain DNS is unresolved | Release Captain |

## Sources

- Agent rules: [`AGENTS.md`](../../AGENTS.md)
- Ethics policy: [`ETHICS.md`](../../ETHICS.md)
- Source policy: [`SOURCES.md`](../../SOURCES.md)
- Species media pipeline: [`species-media-pipeline.md`](../visual-system/species-media-pipeline.md)
- Media intelligence platform strategy: [`media-intelligence-platform-strategy.md`](../visual-system/media-intelligence-platform-strategy.md)
