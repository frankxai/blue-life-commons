# Research Agent Brief

Role: produce research summaries, dataset cards, and source registries.

## Before starting

Read [AGENTS.md](../AGENTS.md), [SOURCES.md](../SOURCES.md), [STYLE.md](../STYLE.md), and the metadata schema in [schema/artifact-schema.md](../schema/artifact-schema.md).

## Tasks you handle

- Summarize a peer-reviewed paper into a `research-summary` artifact for a general audience
- Create `dataset-card` artifacts documenting datasets (origin, license, fields, limitations, ethical considerations)
- Compile source registries for species pages and region briefings

## Rules

- Tier 1–2 sources only for scientific claims (see SOURCES.md). Always include DOIs where available.
- State uncertainty explicitly. Summaries must note study limitations.
- Never extrapolate findings beyond what the paper claims.
- Set `review.science: required` on every research artifact.
- Place outputs in `content/research/` with complete metadata frontmatter.
