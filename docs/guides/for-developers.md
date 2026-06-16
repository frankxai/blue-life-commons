# For Developers & Agentic Builders

You want a clean, normalized surface over fragmented marine APIs and a reference implementation of an ethics-bounded agent system you can fork. The Ocean Intelligence System is exactly that: a review-gated MCP corpus server, a skill pack, and a place-scoped guardian framework with a tested Python connector layer.

## What the system gives you

- **[`marine-mcp`](https://github.com/frankxai/marine-mcp)** — a review-gated MCP server (TypeScript) that serves the reviewed Blue Life Commons corpus to any MCP client. It wraps every result in `{ data, sources, status, attribution }` and returns a curated body *as fact only when review-approved* — otherwise a typed refusal (`servable: false`). It never launders an unsourced claim.
- **[`marine-agent-skills`](https://github.com/frankxai/marine-agent-skills)** — a Claude Code skill pack: `/species-page`, `/field-mission`, `/ethics-check`, `/source-verify`, `/validate-artifact`, `/open-artifact-pr`.
- **[`ocean-intelligence-system`](https://github.com/frankxai/ocean-intelligence-system)** — the Ocean Guardian framework (place-scoped agents) plus a Python connector layer with **five runnable, unit-tested connectors** sharing one normalized-signal + ethics substrate in `mcp/lib/`: OBIS, GBIF, NOAA Coral Reef Watch, WoRMS, Protected Planet. Coordinate coarsening is enforced *in code*, and provenance + license ride on every record.

**Keep the two MCP surfaces distinct:** `marine-mcp` (TypeScript) serves the *reviewed corpus*; `ocean-intelligence-system/mcp/` (Python) wraps *live external data sources*, always labelled as external. A guardian composes both — grounded narrative from the corpus, live signals from the connectors.

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
3. **Add a connector.** In `ocean-intelligence-system/mcp/servers/`, follow an existing folder (e.g. `obis/`) — reuse the normalized-signal + ethics substrate in `mcp/lib/`, return provenance + license per record, and enforce coordinate coarsening. Add unit tests like the existing connectors do.
4. **Run a guardian offline.** Execute `guardians/demo_ningaloo.py` to see the full pipeline — corpus grounding + live connector signals → grounded briefing — run without outbound calls. Then fork a `guardians/archetypes/` brief for your own coastline.
5. **Verify before you ship.** `npm test` and `npm run typecheck` in `marine-mcp`; the Python connectors carry their own unit tests. Run `validate_artifact` / `/validate-artifact` on any content you generate.

## The rules that apply to you

- **Grounded or silent — in code.** A tool states a fact only if it traces to a reviewed artifact or cited source. Don't add a code path that returns unreviewed bodies as fact or strips `sources[]`.
- **Ethics is upstream and immutable.** The wildlife-interaction rules in [`ETHICS.md`](../../ETHICS.md) bind every agent. No connector or guardian may weaken, bypass, or "interpret around" them.
- **Provenance survives the whole pipeline.** Source attribution and license must ride through every connector response to the consumer.
- **Coordinate coarsening is enforced, not advisory.** A live/individual-animal artifact with precise coordinates fails CI. Coarsen by rounding to `sensitivity.tier`, never jitter.
- **Place-scoped, not planet-scoped.** Guardians are powerful because they're small — one reef, one bay, one species. Don't generalize a guardian past its scope.
- **PRs, not direct commits.** All changes flow through review.

## Your first contribution

**Add or harden one connector** in `ocean-intelligence-system/mcp/servers/`, or **author an `mcp-connector` dataset card** in the commons describing a source the system doesn't yet wrap. Either way: reuse the `mcp/lib/` substrate, carry provenance + license, enforce coarsening, and write the tests. See the `mcp-builder-agent.md` brief in `agent/` for the role spec, and open an `artifact-request` issue in [`.github/ISSUE_TEMPLATE/`](../../.github/ISSUE_TEMPLATE/).

> Built on SIP · Blue Life Commons (CC-BY-4.0).
