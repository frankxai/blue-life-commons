# AGENTS.md — Rules for Coding Agents

This project is **agent-native by default**. Contributors are encouraged to use Claude Code, Codex, Cursor, or any coding agent. These rules are binding for every agent-assisted contribution.

## Before you generate anything

1. **Read [ETHICS.md](ETHICS.md)** before creating any animal interaction guidance.
2. **Read [SOURCES.md](SOURCES.md)** — every factual claim needs a source.
3. **Read [STYLE.md](STYLE.md)** for tone, structure, and formatting.
4. Read the metadata schema in [schema/artifact-schema.md](schema/artifact-schema.md).
5. Read any existing related content (e.g., `content/species/`, `content/regions/`, `missions/`) before creating new artifacts, and reuse existing templates.

## Hard rules

- **Every factual claim needs a source.** No source, no claim.
- **Do not invent conservation claims.** Population numbers, threat status, and legal protections must be cited.
- **Do not claim to translate animals.** No anthropomorphic "what the whale is saying" content presented as fact.
- **Use the metadata schema.** Every artifact carries machine-readable YAML frontmatter conforming to `schema/artifact-schema.md`.
- **Generate PRs, not direct commits.** All changes flow through pull request review.
- Mark science-sensitive content `status: needs-expert-review` in metadata. You do not decide scientific truth; reviewers do.
- Do not weaken, remove, or bypass review requirements, ethics rules, or citation standards.

## What a good agent-assisted PR contains

- The new MDX/Markdown artifact with complete metadata frontmatter
- Citations for every factual claim
- Valid internal and external links
- A PR description stating: the issue addressed, sources used, and any claims needing expert review
- A filled-in review checklist (see `.github/PULL_REQUEST_TEMPLATE.md`)

## Agent harness

Role-specific briefs live in [`/agent`](agent/):

| Brief | Use for |
|---|---|
| `agent/research-agent.md` | Research summaries, source gathering, dataset cards |
| `agent/field-mission-agent.md` | Citizen-science and travel field missions |
| `agent/content-review-agent.md` | Pre-review of clarity, structure, schema compliance |
| `agent/ethics-review-agent.md` | Flagging wildlife-interaction and claim risks |
| `agent/map-agent.md` | Map layers and geodata artifacts |
| `agent/mcp-builder-agent.md` | MCP connector stubs, tests, docs, example prompts |

## Example invocation

```
Read AGENTS.md and issue #42.
Create the requested region briefing.
Use existing templates.
Add sources.
Do not make unsupported claims.
Open a PR.
```
