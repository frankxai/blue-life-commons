# User Flows

Last updated: 2026-07-05

## Flow 1: Visitor Learns An Animal

| Step | User expectation | Product response |
|---|---|---|
| Enters `/species` or `/encyclopedia` | Quickly find animals by name or guild | Searchable cards with image, common name, scientific name, guild, and status |
| Opens species detail | See the animal and understand what makes it trustworthy | Approved image or source-card fallback, source, creator, license, and credit near the visual |
| Reads content | Get plain-language, sourced facts | Every claim traces to acceptable sources under `SOURCES.md` |
| Checks media details | Understand reuse and attribution | License, credit, source URL, approved surfaces, blocked surfaces, and alt text are available |
| Needs more context | Move to source or related pages | Source links, related species, guild pages, and public media intelligence route |

Success: the visitor leaves with a useful, cited understanding and no confusion between official media, source cards, candidates, or generated supporting art.

## Flow 2: Educator Or Creator Uses A Species Page

| Step | User expectation | Product response |
|---|---|---|
| Finds relevant animal | Need reliable learning material | Species page has reviewed metadata and source list |
| Checks image reuse | Need credit and license clarity | Media details expose creator, license, credit line, approved surfaces, and blocked surfaces |
| Copies citation or attribution | Need clean reuse path | Future event: `attribution_copied`; current path: visible credit/source fields |
| Shares with students/audience | Need safe behavior framing | Captions and context avoid unsafe approach, feeding, touching, chasing, crowding, or sensitive location exposure |

Success: reuse is easier and more ethical than grabbing a random image result.

## Flow 3: Researcher Verifies A Claim

| Step | User expectation | Product response |
|---|---|---|
| Opens species page | Need scientific and source trail | Scientific name, sources, and reviewed status are visible |
| Opens media source | Need species-match basis and provenance | Source URL, original media URL, creator, license, and match basis are preserved |
| Checks taxonomy/data context | Need authoritative identifiers | Product roadmap uses WoRMS, OBIS, GBIF, EOL, FishBase/SeaLifeBase, and partner lanes as enrichment sources |
| Finds stale or weak source | Need correction path | Opens issue or PR, or uses research request template |

Success: researcher can inspect the trust chain without reverse-engineering site internals.

## Flow 4: Contributor Proposes A Better Image

| Step | User expectation | Product response |
|---|---|---|
| Finds current image | Needs to know what can improve | Media intelligence shows current source family, rights status, and next action |
| Opens media intake issue | Needs a form, not a vague ask | `.github/ISSUE_TEMPLATE/media-intake.yml` requests source, owner, license, permission, credit, species match, and welfare notes |
| Submits lead | Needs clear review path | Issue becomes reviewable work for media rights curator and welfare reviewer |
| Curator reviews | Needs no public leak | Candidate links stay in reviewer-only dossiers/workbench until approval |
| Promotion passes | Needs durable publication | Promotion updates registry, render contract, species page media block, Blob manifest if hosted, and public pages |

Success: better images arrive with enough metadata to approve or reject them quickly.

## Flow 5: Partner Or NGO Grants Media

| Step | Partner expectation | Product response |
|---|---|---|
| Wants impact and credit | Clear credit and usage terms | Intake records owner, credit, license/grant, approved surfaces, and blocked surfaces |
| Shares image or source page | Confidence it will not be misused | Curator blocks surfaces not covered by permission and keeps source record visible |
| Needs sensitive context protected | Avoids location and welfare risk | Ethics review generalizes or removes sensitive context |
| Wants publication proof | Sees public page and attribution | Public page links source/credit; scorecard tracks partner media grants |

Success: partners trust Blue Life because it treats images as credited conservation media, not scraped decoration.

## Flow 6: Reviewer Approves Or Blocks A Candidate

| Step | Reviewer expectation | Product response |
|---|---|---|
| Opens approval workbench | One joined operating view | Workbench joins queue, dossiers, rights snapshots, acquisition plan, outreach, public explorer, and trace ledger |
| Checks image | Verify actual depiction | Candidate thumbnail/file page only in reviewer-only context |
| Checks rights | Verify source, creator, license, permitted surfaces | Approval queue requires complete fields |
| Checks species match | Verify caption, taxon page, expert note, or partner assertion | Promotion refuses incomplete match basis |
| Checks welfare | No unsafe approach, sensitive location, or harmful framing | Ethics/location notes required |
| Promotes or blocks | Needs exact command | Promotion command is provided and validated |

Success: reviewer action is reproducible and cannot accidentally publish a candidate image.

## Flow 7: Release Captain Publishes

| Step | Release expectation | Product response |
|---|---|---|
| Runs local checks | Avoid cloud churn | Validate content, media, links, storage, lint/build as relevant |
| Opens PR | Keep review trail | PR summarizes sources, ethics, checks, and risk |
| Deploys preview | Verify actual site | Check public routes, media rendering, source links, mobile/desktop when UI changes |
| Promotes production | Ship only coherent changes | One production deployment per meaningful change set |
| Updates scorecard | Make progress observable | Product metrics and residual risks updated |

Success: production changes are deliberate, verified, and cheap to operate.

## Sources

- Public workflows: [`WORKFLOWS.md`](../WORKFLOWS.md)
- Species media pipeline: [`species-media-pipeline.md`](../visual-system/species-media-pipeline.md)
- Species visual explorer spec: [`species-visual-explorer-spec.md`](../visual-system/species-visual-explorer-spec.md)
- Media intelligence platform strategy: [`media-intelligence-platform-strategy.md`](../visual-system/media-intelligence-platform-strategy.md)
- Ethics policy: [`ETHICS.md`](../../ETHICS.md)
