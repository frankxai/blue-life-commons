# CONTRIBUTING.md — How to Contribute

You don't "join a community." You **produce an artifact**. Every contribution becomes a page, tool, map, notebook, video, or partner asset — with your credit attached and an impact record behind it.

## The flywheel

```
Issue → AI-assisted contribution → Pull Request → Review (sources, ethics, quality)
     → Published (website/map/notebook/report) → Impact record + credit → Funding
```

## Artifact classes

Pick one. Each has a home in this repository and a metadata `type`:

| Artifact | `type` | Lives in |
|---|---|---|
| Species Intelligence Page | `species-page` | `content/species/<guild>/` |
| Region Ocean Briefing | `region-briefing` | `content/regions/` |
| Field Mission | `field-mission` | `missions/<region>/` |
| Research Paper Summary | `research-summary` | `content/research/` |
| Dataset Card | `dataset-card` | `content/research/` |
| MCP Connector | `mcp-connector` | (marine-mcp repo) |
| Jupyter Notebook | `notebook` | `content/research/` |
| Map Layer | `map-layer` | (blue-atlas repo) |
| Partner Profile | `partner-profile` | `content/partners/` |
| Translation | `translation` | alongside source artifact |
| Short Film Script | `film-script` | (media-kit repo) |
| Educational Lesson | `lesson` | `content/academy/` |
| Event Report | `event-report` | `content/events/` |
| Photo/Observation Guide | `observation-guide` | `missions/guides/` |
| Funding Proposal | `funding-proposal` | `governance/proposals/` |

## Workflow

1. **Find or open an issue.** Use the templates in `.github/ISSUE_TEMPLATE/`. Issues labeled `good-first-issue` and `agent-ready` are great starting points.
2. **Read the standards.** [ETHICS.md](ETHICS.md), [SOURCES.md](SOURCES.md), [STYLE.md](STYLE.md). Coding agents must read [AGENTS.md](AGENTS.md).
3. **Create the artifact.** Use existing templates (see `missions/templates/`, `content/species/`, `content/regions/`). Include complete YAML frontmatter per [schema/artifact-schema.md](schema/artifact-schema.md).
4. **Open a pull request.** Fill in the PR template checklist. PRs, never direct commits.
5. **Review.** Maintainers check sources, ethics, and clarity. Science-sensitive content requires expert review.
6. **Publication and credit.** Merged artifacts are published to the website and recorded in the impact ledger. Your GitHub handle appears in `contributors` metadata and on your contributor profile.

## Labels

`good-first-issue` · `agent-ready` · `needs-sources` · `needs-expert-review` · `species` · `region` · `mission` · `research-os` · `mcp` · `website` · `funding` · `governance`

## Review standards (non-negotiable)

Scientific truth, animal safety rules, citation standards, and expert review requirements are **standards, not popularity contests**. They are not subject to vote and cannot be waived in review.

## Where discussion happens

Discord/Discourse is for live discussion and social energy. **Truth lives in GitHub.** If a discussion produces a decision or an idea worth keeping, it becomes an issue.

> Discord discusses. GitHub decides. Website publishes. Ledger records.

## Funding and credit

Merged work is eligible for impact records (Hypercerts) per [governance/funding.md](governance/funding.md). Maintainers may be funded via GitHub Sponsors / Open Collective as the funding architecture matures.
