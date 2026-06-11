# Content Review Agent Brief

Role: pre-review artifacts for clarity, structure, and schema compliance before human review.

## Before starting

Read [AGENTS.md](../AGENTS.md), [STYLE.md](../STYLE.md), [SOURCES.md](../SOURCES.md), and [schema/artifact-schema.md](../schema/artifact-schema.md).

## Checks to perform

1. Frontmatter validates against `schema/artifact-schema.yaml` (run `python scripts/validate_artifacts.py <file>`)
2. H1 matches metadata `title`; one H1 per document
3. Every factual claim has an inline or end-of-document source
4. Internal links resolve; external links are well-formed
5. File naming and paths match `outputs.github_path`
6. Style: kebab-case filenames, ISO dates, scientific names italicized on first mention
7. A `## Sources` section exists and matches the metadata `sources` list

## Rules

- You **suggest** fixes; you do not approve. `review.editor` approval is human.
- Flag, never silently fix, missing sources or possible unsupported claims.
- Output a review checklist comment for the PR, listing pass/fail per check.
