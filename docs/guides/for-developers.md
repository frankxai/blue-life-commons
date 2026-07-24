# For Developers & Agentic Builders

You want a clean, normalized surface for reviewed ocean knowledge and a credible path toward ethics-bounded marine agents. Two public repositories are currently inspectable here. Place-scoped guardians and live-source connectors remain an implementation brief until their code and tests are published.

## What the system gives you

- **[`marine-mcp`](https://github.com/frankxai/marine-mcp)** — a review-gated MCP server (TypeScript) that serves the reviewed Blue Life Commons corpus to any MCP client. It wraps every result in `{ data, sources, status, attribution }` and returns a curated body *as fact only when review-approved* — otherwise a typed refusal (`servable: false`). It never launders an unsourced claim.
- **[`marine-agent-skills`](https://github.com/frankxai/marine-agent-skills)** — a Claude Code skill pack: `/species-page`, `/field-mission`, `/ethics-check`, `/source-verify`, `/validate-artifact`, `/open-artifact-pr`.
- **Guardian and live-source contract** — dataset cards in this commons document candidate sources and the required provenance, licensing, sensitivity, and welfare boundaries. This guide does not link to or claim a public guardian or live-source connector implementation.

**Keep reviewed corpus and live signals distinct:** `marine-mcp` serves the reviewed corpus. Any future connector must label live external data as external, preserve its provenance and license, and enforce sensitivity controls. A guardian may compose both only after those boundaries are inspectable and tested.

## How to use it today

1. **Install `marine-mcp` in Claude Desktop / Code / Cursor:**

   ```bash
   git clone https://github.com/frankxai/marine-mcp
   cd marine-mcp && npm install && npm run build
   ```

   ```json
   {
     "mcpServers": {
       "marine": {
         "command": "node",
         "args": ["/abs/path/to/marine-mcp/dist/index.js"],
         "env": { "BLC_PATH": "/abs/path/to/blue-life-commons" }
       }
     }
   }
   ```

2. **Call a tool.** Ask your agent to `search_species` (metadata only — id, title, status, servable flag), then `get_species_details` (gated). Inspect the `{ data, sources, status, attribution }` envelope and confirm you get a typed refusal on a `needs-expert-review` page. That refusal contract is what you build on.
3. **Specify a connector before implementing it.** Author an `mcp-connector` dataset card that names the source, license, provenance envelope, coordinate policy, failure behavior, and test cases.
4. **Publish the implementation evidence.** Put runnable code, fixtures, tests, and a bounded example in a repository reviewers can inspect. Do not describe the connector or guardian as available while that evidence remains private or absent.
5. **Verify before you ship.** Run `npm test` and `npm run typecheck` in `marine-mcp`, then run `validate_artifact` / `/validate-artifact` on any content you generate.

## The rules that apply to you

- **Grounded or silent — in code.** A tool states a fact only if it traces to a reviewed artifact or cited source. Don't add a code path that returns unreviewed bodies as fact or strips `sources[]`.
- **Ethics is upstream and immutable.** The wildlife-interaction rules in [`ETHICS.md`](../../ETHICS.md) bind every agent. No connector or guardian may weaken, bypass, or "interpret around" them.
- **Provenance survives the whole pipeline.** Source attribution and license must ride through every connector response to the consumer.
- **Coordinate coarsening is enforced, not advisory.** A live/individual-animal artifact with precise coordinates fails CI. Coarsen by rounding to `sensitivity.tier`, never jitter.
- **Place-scoped, not planet-scoped.** Guardians are powerful because they're small — one reef, one bay, one species. Don't generalize a guardian past its scope.
- **PRs, not direct commits.** All changes flow through review.

## Your first contribution

**Author an `mcp-connector` dataset card** in the commons for a source the public system does not yet wrap. If you also build the connector, publish its code and tests where reviewers can inspect them; carry provenance and license, enforce coarsening, and make failure states explicit. See the `mcp-builder-agent.md` brief in `agent/` for the role spec, and open an `artifact-request` issue in [`.github/ISSUE_TEMPLATE/`](../../.github/ISSUE_TEMPLATE/).

> Built on SIP · Blue Life Commons (CC-BY-4.0).
