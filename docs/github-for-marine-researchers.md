# GitHub for Marine Researchers

You have knowledge but no public contribution system. This guide turns your work into Markdown, maps, missions, notebooks, and public pages — with citizens, students, and coding agents accelerating the boring parts.

## Why GitHub?

- **Version control for knowledge.** Every edit reviewed, every change attributed, nothing lost.
- **Review built in.** Your standards (sources, ethics, accuracy) are enforced through pull request review — not by hoping a wiki stays correct.
- **Leverage.** Once your work is structured here, it flows automatically to the public website, map layers, lessons, and impact records. One contribution, many outputs.

## Core concepts (5 minutes)

| GitHub term | Research equivalent |
|---|---|
| Repository | A shared, versioned project archive |
| Issue | A research request / task with discussion attached |
| Pull request (PR) | A submitted manuscript: proposed changes under review |
| Review | Peer review — sources, ethics, clarity |
| Merge | Acceptance and publication |

## What you can contribute (no coding required)

- **Research summaries** — your paper, summarized for the public (`type: research-summary`)
- **Dataset cards** — documentation of your datasets (`type: dataset-card`)
- **Species pages and region briefings** — your expertise, structured
- **Expert review** — the most valuable contribution: approving `review.science` on others' artifacts

Everything is plain Markdown text with a small metadata header. See the [contributor onboarding](contributor-onboarding.md) and [schema/artifact-schema.md](../schema/artifact-schema.md).

## A typical workflow

1. Open an issue with the **Research request** template describing your material (include DOIs).
2. A contributor — possibly assisted by a coding agent following [AGENTS.md](../AGENTS.md) — drafts the artifact.
3. You review the science. Your approval is recorded in the artifact metadata (`review.science: approved`).
4. Merged → published → credited → recorded in the impact ledger.

## Archival and data

- Releases of research material can be archived via Zenodo's GitHub integration for DOI-oriented records.
- Datasets and models can be hosted on Hugging Face with dataset cards mirroring our `dataset-card` artifacts.

## The deal

You bring knowledge and review. The commons brings structure, contributors, agents, publication surfaces, and impact records that make your work fundable and visible. Ocean life gets more capable humans.
