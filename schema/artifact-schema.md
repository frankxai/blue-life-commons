# Artifact Metadata Schema

Every artifact in Blue Life Commons carries machine-readable YAML frontmatter. This schema is the **connective tissue**: it lets one contribution appear on the website, map, academy, field passport, research dashboard, impact ledger, contributor profile, and sponsor reports.

The machine-readable definition lives in [`artifact-schema.yaml`](artifact-schema.yaml). CI validates every artifact's frontmatter against it.

## Fields

| Field | Required | Type | Description |
|---|---|---|---|
| `id` | yes | string | Globally unique, kebab-case, e.g. `mission-nl-seal-observation-001` |
| `type` | yes | enum | Artifact class — see allowed values below |
| `title` | yes | string | Human-readable title; matches the document H1 |
| `region` | no | list | Region slugs, e.g. `netherlands`, `north-sea` |
| `species_group` | no | list | Guild slugs: `cetaceans`, `pinnipeds`, `turtles`, `sharks-rays`, `reefs` |
| `species` | no | list | Species slugs, e.g. `harbor-seal` |
| `difficulty` | no | enum | `beginner` \| `intermediate` \| `advanced` |
| `audience` | no | list | e.g. `traveler`, `student`, `citizen-scientist`, `researcher`, `developer`, `educator` |
| `status` | yes | enum | `draft` \| `needs-sources` \| `needs-expert-review` \| `approved` \| `published` |
| `sources` | yes | list | Objects with `url`, optional `title`, `accessed` |
| `review` | yes | object | `science`, `ethics`, `editor` — each `pending` \| `required` \| `approved` \| `not-applicable` |
| `outputs` | yes | object | `website_path`, `github_path`, `map_layer` (bool) |
| `impact` | no | object | `claim` (string), `eligible_for_hypercert` (bool) |
| `sensitivity` | no | object | Location-data sensitivity per the GBIF four-category model — `tier` (`public`\|`low`\|`medium`\|`high`\|`extreme`), `rationale`, `generalized_to` |
| `iucn` | no | object | Red List provenance — `category`, `assessment_date`, `version`, `population_trend`, `scope` (`global`\|`regional`) |
| `consensus_state` | no | enum | `settled` \| `contested` \| `emerging` — contested/emerging artifacts must represent the disagreement |
| `contributors` | yes | list | Objects with `github` handle |
| `license` | yes | string | Default `CC-BY-4.0` |

### Source object fields

Each entry in `sources` has `url` (required) plus optional `title`, `accessed`, `doi`, `tier` (`1`–`3` per [SOURCES.md](../SOURCES.md)), `license`, and `commercial_use_ok`. **A `commercial_use_ok: false` source must not underpin an artifact whose `impact.eligible_for_hypercert` is true** — you cannot build a commercial impact claim on a non-commercial source.

### Scientific-integrity rules (added 2026-06-15)

- **Location sensitivity.** For vulnerable taxa, set `sensitivity.tier` and publish locations no finer than the tier allows (GBIF generalization: `extreme` → no coordinates / ≥1°; `high` → ~0.1°; `medium` → ~0.01°; `low`/`public` → as cited). Coarsen by **rounding**, never by random jitter. Check the *combination attack*: a coarse coordinate + season + a landmark in attached media must not reconstruct an exact site.
- **IUCN staleness.** A `species-page` reaching `approved`/`published` should carry `iucn.assessment_date` + `iucn.version` so a years-old assessment is not presented as current truth.
- **Claim sourcing.** Every factual sentence must trace to a source; `scripts/lint_content.py` fails CI on a science-sensitive artifact with no sources and on anthropomorphic claims presented as fact.

### Allowed `type` values

`species-page` · `region-briefing` · `field-mission` · `research-summary` · `dataset-card` · `mcp-connector` · `notebook` · `map-layer` · `partner-profile` · `translation` · `film-script` · `lesson` · `event-report` · `observation-guide` · `funding-proposal`

## Canonical example

```yaml
id: mission-nl-seal-observation-001
type: field-mission
title: Ethical Seal Observation on the Dutch Coast
region:
  - netherlands
  - north-sea
species_group:
  - pinnipeds
species:
  - harbor-seal
  - grey-seal
difficulty: beginner
audience:
  - traveler
  - student
  - citizen-scientist
status: needs-expert-review
sources:
  - url: ""
review:
  science: pending
  ethics: required
  editor: approved
outputs:
  website_path: /missions/netherlands/seal-observation
  github_path: missions/netherlands/seal-observation.md
  map_layer: false
impact:
  claim: "Created educational field mission for ethical seal observation."
  eligible_for_hypercert: true
contributors:
  - github: username
license: CC-BY-4.0
```

## Rules

- `id` is permanent. Never reuse or rename an `id` after publication.
- Artifacts involving live-animal interaction must set `review.ethics: required` (see [ETHICS.md](../ETHICS.md)).
- An artifact may only move to `status: published` when all applicable reviews are `approved` or `not-applicable`.
- Translations reference the source artifact's `id` in an additional `translates: <id>` field.
