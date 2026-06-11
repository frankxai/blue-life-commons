# MCP Builder Agent Brief

Role: build MCP connector stubs, tests, docs, and example prompts.

## Before starting

Read [AGENTS.md](../AGENTS.md) and the metadata schema in [schema/artifact-schema.md](../schema/artifact-schema.md).

## Tasks you handle

- MCP connector stubs (e.g., source registry lookup, species metadata, region briefing retrieval)
- Tests for every connector
- Connector documentation and example prompts

## A complete MCP contribution contains

1. The connector implementation (in the `marine-mcp` repo)
2. Tests covering the connector's tools/resources
3. Updated docs: what it does, configuration, limitations
4. Example prompts demonstrating intended use
5. An `mcp-connector` metadata artifact registering it in the commons

## Rules

- Connectors must only serve reviewed, published content — never draft or unreviewed artifacts as fact.
- Responses must carry source attribution through to the consumer.
- No connector may generate wildlife-interaction guidance dynamically; it serves reviewed artifacts only.
- Follow the repository's existing language/tooling conventions; add no new dependencies without need.
