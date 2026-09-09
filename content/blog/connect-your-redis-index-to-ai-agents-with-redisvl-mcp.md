---
title: "Connect Your Redis index to AI agents with RedisVL MCP"
linkTitle: "Connect Your Redis index to AI agents with RedisVL MCP"
url: "/blog/connect-your-redis-index-to-ai-agents-with-redisvl-mcp/"
description: "If you already use Redis for search, retrieval, or application memory, the RedisVL MCP is a practical next step: making that data available to agents without rebuilding your integration for every..."
date: 2026-06-11
blogCategories:
- "Tech"
authors:
- "Vishal Bala"
lastmod: 2026-06-15
hidden: true
---

*By Vishal Bala, Sr. Applied AI Engineer · Published 11 June 2026 · updated 15 June 2026*

![Connect Your Redis index to AI agents with RedisVL MCP](/images/site-mirror/00470feaee022ac14d1e9ebfcb23b8d9eb276cd6-1200x628.webp)

If you already use Redis for search, retrieval, or application memory, the RedisVL MCP is a practical next step: making that data available to agents without rebuilding your integration for every framework.

As teams connect indexed data to agents, the work shifts to integration. Different clients need access to the same retrieval surfaces, search behavior needs to stay consistent, and platform teams still need control over how that access works. The Model Context Protocol (MCP) addresses this by giving agent systems a standard way to discover and invoke tools. Instead of building a custom Redis integration for every agent stack, teams can expose a smaller, stable interface and reuse it across any MCP-compatible client -- Claude Desktop, Cursor, OpenAI Agents SDK, LangChain, or whatever comes next.

Redis already provides the [official Redis MCP Server](https://redis.io/docs/latest/integrate/redis-mcp/) for broad agent access to Redis data structures, query-engine capabilities, and server-management workflows. RedisVL MCP is complementary and more focused: it exposes existing Redis Search indexes as governed retrieval surfaces with predictable tool contracts. Use the official Redis MCP Server when an agent should work with Redis generally. Use RedisVL MCP when the goal is application retrieval with configured search behavior, schema-aware filters, controlled return fields, runtime limits, and optional read-only mode.

For developers, that means less framework-specific glue code. For platform teams, it means a manageable surface for governance, security, and operational control. For Redis users specifically, it means the indexes you already have can become a shared tool layer across your AI stack.

## What the RedisVL MCP exposes

The RedisVL MCP sits at the RedisVL layer, not the raw Redis command layer. It exposes a higher-level interface around existing Redis Search indexes with two tools:

`search-records` -- Search the index by text query. The server handles embedding, query construction, and result normalization. Agents supply query text, pagination, filters, and return fields. They do not decide the search mode (vector, full-text, or hybrid) or tuning parameters -- those are owned by configuration.

`upsert-records` -- Write records to the index. The server validates each record against the index schema, embeds text fields server-side when the record lacks a vector (or always, depending on config), and writes to Redis. Disabled in read-only mode.

Under the hood, the server:

- Binds to one existing Redis index at startup today, with multi-index support planned
- Inspects the index via `FT.INFO` and reconstructs its schema automatically -- no need to redeclare field definitions
- Uses a configured vectorizer when vector search or server-side embedding requires one
- Supports stdio, SSE, and streamable-http transports -- run locally for development or behind the right network and authentication controls for remote deployments
- Keeps search mode and tuning parameters in config, not in the request contract

### Schema introspection and overrides

One design choice worth highlighting: the server reconstructs the full index schema from Redis at startup rather than requiring a separate schema file. This means you point the MCP at an existing index and it can infer the fields it should expose.

For cases where `FT.INFO` does not expose all vector field attributes (e.g., older Redis versions), the config supports `schema_overrides` to patch in missing metadata like dimensionality or distance metric for fields that were already discovered. This keeps the common path simple without blocking edge cases.

## Filtering

Agents can pass structured filters without writing raw Redis query syntax. The filter contract supports tag, text, and numeric fields with logical combinators:

```
{
 "query": "incident response procedures",
 "limit": 5,
 "filter": {
   "and": [
     { "field": "category", "op": "eq", "value": "runbook" },
     { "field": "year", "op": "gte", "value": 2023 }
   ]
 },
 "return_fields": ["title", "content", "category"]
}

```

Supported operators include `eq`, `ne`, `like`, and `in` for tag and text fields. Numeric fields support `eq`, `ne`, `gt`, `gte`, `lt`, `lte`, and `in`. The exists operator is available for any known schema field. Filters can be composed with `and`, `or`, and `not`. Agents can also pass raw Redis filter strings if they need full control.

## Upsert with server-side embedding

When ingestion is enabled, agents send records as plain objects. The server handles the rest:

```
{
 "records": [
   {
     "title": "Incident Response Playbook",
     "content": "Step 1: Identify the scope of the incident...",
     "category": "runbook",
     "year": 2024
   }
 ],
 "id_field": "title"
}

```

The server reads the `content` field (configurable via `default_embed_text_field`), generates the embedding using the configured vectorizer, validates the record against the index schema, and writes it to Redis. If a record already includes a vector, the server skips embedding by default (`skip_embedding_if_present: true`) -- useful when pre-computed embeddings are available.

Batch size is capped by `max_upsert_records` (default: 64) to prevent runaway writes.

## Runtime governance

The MCP server exposes several knobs that platform teams care about:

| Setting | Default | Purpose |
|---|---|---|
| default_limit | 10 | Default result count when caller omits limit |
| max_limit | 100 | Hard cap on results per request |
| max_result_window | 1000 | Maximum offset + limit to prevent deep pagination |
| max_upsert_records | 64 | Maximum records per upsert call |
| max_concurrency | 16 | Concurrent request limit |
| request_timeout_seconds | 60 | Per-request timeout |

Combined with read-only mode (`--read-only flag` or `REDISVL_MCP_READ_ONLY=true`), these give platform teams fine-grained control over what agents can and cannot do.

### Error contract

Errors follow a typed contract with stable error codes (`invalid_request`, `invalid_filter`, `dependency_missing`, `backend_unavailable`, `internal_error`) and a `retryable` flag. This lets agent frameworks distinguish between bad requests that should not be retried, missing dependencies that need operator action, and transient backend failures that should.

## Running the server

Install the MCP extra:

```
pip install redisvl[mcp]

```

The server supports three transport modes. **stdio** is the default and works with local MCP clients like Claude Desktop and Cursor. **SSE** and **streamable-http** run the server as a persistent HTTP service for remote or multi-client deployments.

SSE and streamable-http endpoints are unauthenticated by default. Only bind them to public interfaces on trusted networks or behind an authenticating reverse proxy. If you do not need agent-driven writes, run with `--read-only` so `upsert-records` is not exposed.

```
# stdio (default) -- for local MCP clients
uvx --from redisvl[mcp] rvl mcp --config /path/to/mcp.yaml
# SSE -- remote deployment over Server-Sent Events
uvx --from redisvl[mcp] rvl mcp --config /path/to/mcp.yaml --transport sse --host 0.0.0.0 --port 9000
# Streamable HTTP -- newer HTTP-based streaming transport
uvx --from redisvl[mcp] rvl mcp --config /path/to/mcp.yaml --transport streamable-http --port 8000
For read-only retrieval (any transport), add --read-only:
uvx --from redisvl[mcp] rvl mcp --config /path/to/mcp.yaml --transport sse --port 9000 --read-only

```

### Server configuration

A minimal config looks like this:

```
server:
 redis_url: redis://localhost:6379
indexes:
 my_index:
   redis_name: my_index
search:
   type: hybrid
vectorizer:
   class: OpenAITextVectorizer
   model: text-embedding-3-small
runtime:
   text_field_name: content
   vector_field_name: embedding
   default_embed_text_field: content

```

The `redis_name` field points to the existing Redis index. The server discovers index details such as prefix and field definitions from Redis at startup.

The `search.type` field (`vector`, `fulltext`, or `hybrid`) determines how the server builds queries. Query tuning parameters like `linear_text_weight` or `text_scorer` live under `search.params`, not in the request contract. This separation keeps agent requests simple while letting operators tune behavior.

The `vectorizer` block names a RedisVL vectorizer class and its model. The server instantiates it when vector search or server-side embedding requires it. API keys are resolved from environment variables (e.g., `OPENAI_API_KEY`). Full-text-only deployments can omit vector-only settings and the vectorizer entirely.

### Client configuration

For Claude Desktop, add to your `claude_desktop_config.json`:

```
{
 "mcpServers": {
   "redisvl": {
     "command": "uvx",
     "args": [
       "--from", "redisvl[mcp]",
       "rvl", "mcp",
       "--config", "/path/to/mcp.yaml"
     ],
     "env": {
       "OPENAI_API_KEY": "sk-..."
     }
   }
 }
}

```

For Cursor, add to `.cursor/mcp.json`:

```
{
 "mcpServers": {
   "redisvl": {
     "command": "uvx",
     "args": [
       "--from", "redisvl[mcp]",
       "rvl", "mcp",
       "--config", "/path/to/mcp.yaml"
     ],
     "env": {
       "OPENAI_API_KEY": "sk-..."
     }
   }
 }
}

```

For clients connecting to a remote SSE or streamable-http server, use a URL instead of a command:

```
{
 "mcpServers": {
   "redisvl": {
     "url": "http://your-host:9000/sse"
   }
 }
}

```

## A concrete example

Suppose you have a Redis index called `knowledge_base` with `title` (text), `content` (text), `category` (tag), `year` (numeric), and `embedding` (vector) fields. An agent asks: *"Find recent runbook entries about incident response."*

The agent calls `search-records`:

```
{
 "query": "incident response procedures",
 "limit": 3,
 "filter": {
   "and": [
     { "field": "category", "op": "eq", "value": "runbook" },
     { "field": "year", "op": "gte", "value": 2023 }
   ]
 }
}

```

The server embeds the query, applies the filter, runs a hybrid search, and returns:

```
{
 "search_type": "hybrid",
 "offset": 0,
 "limit": 3,
 "results": [
   {
     "id": "doc:incident-response-playbook",
     "score": 0.92,
     "score_type": "hybrid_score",
     "record": {
       "title": "Incident Response Playbook",
       "content": "Step 1: Identify the scope...",
       "category": "runbook",
       "year": "2024"
     }
   },
   {
     "id": "doc:on-call-escalation-guide",
     "score": 0.87,
     "score_type": "hybrid_score",
     "record": {
       "title": "On-Call Escalation Guide",
       "content": "When an incident is detected...",
       "category": "runbook",
       "year": "2023"
     }
   }
 ]
}

```

The agent gets structured results it can reason over. The vector field is excluded from results by default. Score types are labeled so the agent (or downstream logic) knows how to interpret them.

## What is next

**Multiple indexes** -- Today, each MCP server instance binds to one index. Multi-index support will let a single server expose multiple indexes as separate tools -- for example, `search-knowledge-base` and `search-products` from one process. The config already uses `indexes` as a dict, and this is the natural next step.

## Getting started

If you have an existing Redis index, you can have the MCP server running in under five minutes:

1. `pip install redisvl[mcp]`
1. Write a YAML config pointing at your index
1. Run `rvl mcp --config mcp.yaml`
1. Add the server to your MCP client config

The index schema is introspected automatically. The search mode, vectorizer, and runtime limits are all in config. The request contract stays simple.

For the full configuration reference and more examples, see the [RedisVL documentation](https://docs.redisvl.com/).
