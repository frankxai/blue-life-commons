# CommonsGraph.v1 — the claim and provenance graph

Blue Life Commons publishes reviewed, cited, openly-licensed knowledge. The
graph is how it stays honest about which parts are actually reviewed.

The rule the whole design serves: **a claim's status is derived, never
declared.** A contributor can write a claim, cite it, and attach a review — but
nobody can write `status: reviewed` into a file. Status is recomputed from the
Review, Contradiction and Source records every time the graph is read.

Normative contract: [`lib/commons-graph/types.ts`](../lib/commons-graph/types.ts).
Envelope schema: [`lib/commons-graph/commons-graph.v1.schema.json`](../lib/commons-graph/commons-graph.v1.schema.json).

## The workbench

Run this before opening a PR:

```bash
node bin/blc-validate.mjs my-packet.json
node bin/blc-validate.mjs my-packet.json --export out/my-packet.graph.json
node bin/blc-validate.mjs my-packet.json --json          # machine-readable receipt
node bin/blc-validate.mjs my-packet.json --now 2027-01-01 # test future freshness
```

It prints a receipt: nine checks in a fixed order, every finding attributed to a
node id, and the status every claim will carry once published. Exit code 0 means
the packet is ready; 1 means it is not, and no export is written.

| Check | What it refuses |
|---|---|
| `schema` | wrong or missing `CommonsGraph.v1` envelope |
| `structure` | a node or edge missing owner, provenance, version, visibility or evaluation — or a hand-set claim status |
| `citation` | a claim with no resolvable, dated source |
| `license` | an artifact or asset whose licence or Rights record does not permit publication |
| `location-sensitivity` | precise coordinates for a species that must be generalised |
| `review-state` | a review that approves a version no longer current, self-review, or an artifact publishing a disputed claim as fact |
| `ethics` | generated media not marked concept-only; a node blocked by an ethics rule with no approved ethics review |
| `attribution` | an artifact with no credited contributor |
| `export` | anything still leaking through the public projection |

Three fixtures in `lib/commons-graph/fixtures/` show the shapes: one that
passes, one with an uncited claim, one that would publish a right whale's
position. Two of the three must fail; `tests/commons-graph.test.mjs` asserts it.

## The sixteen node types

`Taxon` `Species` `Region` `Habitat` `Observation` `Claim` `Source` `Dataset`
`MediaAsset` `Rights` `EthicsRule` `Review` `Artifact` `Contributor`
`Contradiction` `Supersession`

Every node and every edge carries the same five fields, with no exceptions:

- **owner** — who is answerable for it
- **provenance** — `authored`, `imported`, `derived` or `inferred`, by whom, when, and from what
- **version** — an integer; a review binds to one version and is void at the next
- **visibility** — `public`, `restricted` or `embargoed`
- **evaluation** — the named rule that decides whether it is sound

## How claim status is derived

Precedence, highest first. The first rule that fires decides.

1. **disputed** — an open `Contradiction` touches the claim.
2. **inferred** — no resolvable, dated citation.
3. **stale** — the freshest supporting source was last checked longer ago than
   the claim class allows.
4. **reviewed** — an approved science `Review` exists *at the claim's current
   version*.
5. **inferred** — cited and fresh, but nobody has reviewed it yet.

Every derivation returns the rule that decided it plus every signal that fired,
so a reader can always see why a claim reads the way it does. A claim written by
a model keeps `provenance.method: "inferred"` in its signals for life, even
after a reviewer approves it.

### Citation freshness

Budgets are per claim class, because a population estimate goes stale faster
than a description of a flipper.

| Claim class | Budget |
|---|---|
| `regulation` | 2 years |
| `population-estimate`, `threat` | 3 years |
| `taxonomy`, `distribution`, `conservation-status`, `other` | 5 years |
| `morphology`, `behavior` | 10 years |

Freshness runs from `accessedAt` where present, otherwise `publishedAt` — a 1990
paper somebody verified last month is a live citation; a 2024 page nobody has
opened since is not. A source marked `supersededBySourceId` contributes nothing.

## Contradictions are kept, not resolved away

When two claims cannot both be true, `raiseContradiction` creates a
`Contradiction` node linked to both. Nothing is merged and nothing is deleted.
Both claims flip to `disputed`, and an artifact may not publish a disputed claim
as fact — it must show both sides.

A contradiction leaves the open state only by an editorial act:

- **`resolved-by-supersession`** — a `Supersession` node, decided by a named
  reviewer, retires one claim version in favour of another. The retired claim
  stays in the graph; `supersessionChain()` walks the history and detects cycles.
- **`resolved-by-scope`** — the two claims describe different subpopulations,
  regions or periods and never conflicted. Refused when the scopes are identical,
  so this cannot be used to wish a real disagreement away.

## Safe species-location projection

Sensitivity follows the GBIF generalization model. Anything at `medium` or above
is never published with a coordinate.

| Sensitivity | Public projection |
|---|---|
| `public` | exact coordinates |
| `low` | rounded to 0.1° with uncertainty widened to 11 km |
| `medium`, `high`, `extreme`, unknown | region only, coordinates withheld |

Above `low`, coordinates are withheld rather than coarsened: a 0.1° box is still
an 11 km search area. The public projection type has no `coordinates` field at
all, so a caller cannot read one off by mistake — the compiler stops them. An
unknown sensitivity fails safe to region-only.

`publicProjection()` additionally drops every non-public node and every edge
that touches one.

## MCP query contract

[`lib/commons-graph/mcp/tool-contracts.v1.json`](../lib/commons-graph/mcp/tool-contracts.v1.json)
declares `query_species`, `query_claims` and `export_packet` with JSON Schema on
both sides. It is a **definition only** — no server, no endpoint, no transport.
Its invariants bind any implementation: every claim returns with its derived
status and the reason for it, both sides of a dispute are always returned, and
an empty result is a valid answer.

## What this is not

The commons is a reviewed knowledge record. It is not live monitoring, and no
surface built on this graph may say it is. Occurrence records imported from OBIS
or GBIF describe sightings that already happened and are often months or years
behind. Operational, near-real-time work belongs to the Ocean Intelligence
Guardian product, in its own repository.
