# STYLE.md — Content Style Guide

## Voice

- Clear, warm, and practical. Write for curious travelers, students, and citizen scientists — not academics.
- Confident about workflow, humble about science. Uncertainty is stated, not hidden.
- No hype, no mysticism presented as fact, no "save the ocean" guilt language. Capability over sentiment.

## Structure

- Every artifact starts with YAML frontmatter conforming to [schema/artifact-schema.md](schema/artifact-schema.md).
- One H1 per document, matching the metadata `title`.
- Short sections with descriptive H2/H3 headings.
- Lead with what the reader can *do*, then context, then sources.
- End every artifact with a `## Sources` section.

## Formatting

- Markdown/MDX only. The website is generated from this repository — no manual web edits.
- Use relative links for internal references (`../species/pinnipeds/harbor-seal.md`).
- Use tables for structured comparisons; lists for steps.
- File names: lowercase kebab-case (`seal-observation-beginner.md`).
- Dates: ISO 8601 (`2026-06-11`).
- Species: common name first mention with scientific name in italics — harbor seal (*Phoca vitulina*) — then common name thereafter.

## Language

- Default language is English. Translations are first-class artifacts (`type: translation`) linked to the source artifact's `id`.
- Define jargon on first use. Beginner missions assume zero prior knowledge.

## Imagery and media

- Only use media with explicit licensing (CC or contributor-owned with grant).
- Credit photographers/creators in captions.
- No imagery depicting harassment or unsafe proximity to wildlife, even if "impressive."
