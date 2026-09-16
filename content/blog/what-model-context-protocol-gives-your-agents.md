---
title: "What Model Context Protocol gives your agents & what it leaves to you"
linkTitle: "What Model Context Protocol gives your agents & what it leaves to you"
url: "/blog/what-model-context-protocol-gives-your-agents/"
description: "If you've shipped an AI agent that connects to tools, you've probably felt the relief of having one standard way to wire it all up. Model Context Protocol (MCP) handles that part well. But there's..."
date: 2026-06-12
blogCategories:
- "Tech DE"
authors:
- "Jim Allen Wallace"
lastmod: 2026-06-17
hidden: true
mirrored: true
---

*By Jim Allen Wallace, Sr. Product Marketing Manager · Published 12 June 2026 · updated 17 June 2026*

![What Model Context Protocol gives your agents & what it leaves to you](/images/site-mirror/9cea08d65d62382c03a72bb40887b6f6f0a23c53-2400x1256.webp)

If you've shipped an AI agent that connects to tools, you've probably felt the relief of having one standard way to wire it all up. Model Context Protocol (MCP) handles that part well. But there's a gap that catches a lot of teams off guard: your agent can call a tool through MCP, complete the action, and still walk into the next session knowing nothing about what just happened.

That's not a bug. It's the boundary of what the protocol was built to do. MCP standardizes how agents talk to tools and data. It doesn't standardize memory, freshness, or reliability. Those still live below the protocol, and they're still yours to build.

This article covers what MCP standardizes, why tool calls are stateless by design, the three problems MCP leaves on your plate, and where a fast data layer fits underneath it all.

## What does Model Context Protocol standardize?

MCP is an open protocol that connects LLM apps to external tools and data. Think of it like a USB-C port for AI apps: one standardized connector, many devices.

Before MCP, every agent-to-tool connection was its own project. Wiring up an agent to a new tool meant a custom integration for each pairing, which led to fragmentation and duplicated work. Build MCP into your agent once, and you can talk to any compatible MCP server without writing fresh glue code. That's the whole pitch: a universal, open standard for connecting AI systems to data.

The protocol pins down a few specific things:

- **Wire format:** [JSON-RPC 2.0 messages](https://modelcontextprotocol.io/specification/2025-11-25) with capability negotiation.
- **Architecture:** Three roles. Hosts (the LLM apps), clients (the connectors), and servers (the services that provide context and capabilities).
- **Server primitives:** Three building blocks. Resources for context and data, prompts for templated messages, and tools as executable functions the AI can call.

Tools are model-controlled, so the LLM picks which one to call based on what the user asked.

Governance sits outside any single vendor, which matters for a standard like this. Anthropic [introduced MCP](https://thenewstack.io/why-the-model-context-protocol-won) in November 2024, then donated it to the Agentic AI Foundation, a Linux Foundation fund co-founded with Block and OpenAI, with support from Google, Microsoft, Amazon Web Services (AWS), Cloudflare, and Bloomberg. Adoption looks healthy too: MCP reported 97 million [monthly SDK downloads](https://www.anthropic.com/news/donating-the-model-context-protocol-and-establishing-of-the-agentic-ai-foundation) and 10,000 active servers when the donation was announced. MCP is a real standard with real momentum. The interesting question is what it standardizes, and what it pointedly doesn't.

## Does MCP handle agent memory?

MCP lets your agent act, but it doesn't standardize how your agent remembers. Tool calls are stateless by design, and the spec is moving harder in that direction.

A tools/call request is just a JSON-RPC message with a name and arguments. The response returns content and an error flag. That's the whole contract. Memory and context management are explicitly out of scope for MCP, which focuses on context exchange, not on how AI apps manage what they're given.

Recent drafts double down on this. Proposed changes remove protocol-level session state from the transport, including protocol-level sessions and the Mcp-Session-Id header from the Streamable HTTP transport. The intent is stateful agentic apps running on top of a sessionless protocol.

The reason sessions are getting cut: no two clients agreed on what a session even was. ChatGPT opened a fresh one per tool call, desktop clients opened one per app launch, web clients opened one per page load, and almost none [resumed a session](https://modelcontextprotocol.io/seps/2567-sessionless-mcp) after a disconnect. With the concept meaning something different everywhere, the spec is handing state management back to the app. In its place comes explicit handle passing: a tool returns an identifier like a basket_id, and the model passes that identifier back as an argument on later calls.

The takeaway is simple. Cross-session agent memory belongs at the app or data layer, not in the protocol. MCP gives you the wire format for invoking a tool, nothing more.

## What MCP leaves to you: memory, freshness & reliability

The protocol stops at the tool call. That leaves three problems for you to solve: memory, freshness, and reliability.

### How do AI agents remember across sessions?

Agent memory typically splits into two types. Short-term, or working memory, is thread-scoped and tracks the ongoing conversation. In frameworks like LangGraph, that's handled by checkpointers that [persist graph state](https://docs.langchain.com/oss/python/langgraph/persistence). Long-term memory persists across sessions, scoped to namespaces rather than single thread IDs.

Most production agents use both. MCP can expose memory services through shared tools or resources, but there are [no memory standards](https://www.newamerica.org/insights/ai-agents-and-memory) governing how memory is stored, segmented, or reused.

### Why does retrieved context go stale?

Stale data quietly poisons agent outputs. [Retrieval-augmented generation (RAG)](https://redis.io/glossary/retrieval-augmented-generation/) helps with freshness and factuality, but keeping retrieval indices current takes ongoing effort as your data changes. Systems retrieving by cosine similarity alone can [surface stale context](https://arxiv.org/html/2509.19376) or fail to tell apart novel updates from redundant information: a vendor's deprecated guidance, say, or last month's roster.

Some domains feel this more than others. In cybersecurity, today's attack vector is far more urgent than the same one from a year ago. In healthcare, [outdated studies pose risks](https://arxiv.org/pdf/2507.18910) when systems repeat findings that have since been disproven. And keeping an index fresh is real work: [new source data](https://arxiv.org/html/2603.10765v1) has to be converted into vector embeddings, and some index structures involve costly rebuild paths.

Staleness eventually hits the model layer as [context rot](/blog/context-rot/), the performance degradation that happens when LLMs process increasingly long input contexts. A bigger context window doesn't save you. When stale or excessive retrieved content fills the window, the relevant signal gets buried and the model struggles to act on it.

### Why do long agent chains fail?

Long agent chains fail more often than people expect, because each step has to clear the one before it. If every step is 95% reliable on its own, a 10-step chain succeeds end to end only about 60% of the time, since you multiply 0.95 by itself for each step. Drop per-step reliability to 85% and that same 10-step chain lands around 20%. Add more steps and the number falls faster.

The raw math actually understates the problem, because the output of one step becomes the input to the next. One bad result early breaks everything downstream. This is a systems problem, not a model problem, and retrieval is one of the steps most likely to drag the chain down.

Every retrieval an agent makes is a step that can fail. Slow tools add latency to every query that touches them, and degraded or stale results push low-quality context into the window, which the next step then treats as fact. The more a chain depends on data it has to fetch mid-run, the more its end-to-end reliability rides on how fast and how current that data layer is. None of that is handled at the protocol layer.

## How a real-time data layer fills the gaps MCP leaves

Memory, freshness, and reliability all need the same thing: somewhere to persist, retrieve, and refresh state, fast. That's the job of an in-memory data layer.

Redis is built for that job. As a real-time data platform, enterprise-grade Redis reported over [100 million operations](/blog/redis-enterprise-extends-linear-scalability-200m-ops-sec/) per second at sub-millisecond latency on a 20-node AWS cluster. That matters because agents can make [multiple context retrievals](/blog/build-smarter-ai-agents-manage-short-term-and-long-term-memory-with-redis/) in a single reasoning loop, and that latency stacks up. Beyond caching, Redis brings [vector search](https://university.redis.io/course/1npvvtfft2agew), semantic caching, and the data structures agents lean on for state. Your app can support RAG retrieval, agent memory, and real-time coordination in [one system](/blog/more-than-a-vector-database/) instead of stitching together a separate tool for each.

That maps cleanly to the three problems above. For memory, Redis supports [agent memory tiers](/blog/ai-agent-memory-stateful-systems/): short-term working memory with in-memory data structures, long-term semantic memory through vector search, and episodic memory with streams as logs of past tool calls and outcomes. For freshness, Redis Data Integration syncs changes from source systems into Redis, while Redis LangCache handles semantic caching for repeated or similar prompts, matching queries by [similarity using vector embeddings](/blog/whats-the-best-embedding-model-for-semantic-caching/) so the system serves a cached response even when wording differs. For reliability, the same low-latency layer keeps retrieval fast and current, so fewer steps fail on slow or stale data in the first place.

MCP solves tool connectivity, but it [doesn't solve context fragmentation](/blog/from-demo-to-dependable-ai-in-context/). Closing that gap is the job of Redis Iris, a context engine that sits between an agent and the data it needs, feeding the right context in the right form at the right time. Memory, retrieval, and fresh data stop being three systems your agent has to reconcile and become one fast layer it reads and writes against.

## MCP connects agents to tools, the data layer makes them work

MCP does its job well, and the sessionless direction makes it cleaner still. Tool connectivity is solved. The rest sits one layer down: memory across sessions, freshness against live data, and reliability across long chains. That work runs below the protocol, and Iris is where Redis puts it.

The neat part is how that layer meets MCP. Instead of standing apart from the protocol, Iris exposes its context, memory, and retrieval to agents as MCP tools, the same tools the rest of your stack already calls. The layer that handles what MCP leaves out plugs back into MCP to deliver it.

If you're building agents that need to remember, stay current, and hold up across long workflows, the data layer is the part worth getting right.

[Try Redis free](https://redis.io/try-free/?rcplan=iris) to see how it works with your workload, or [talk to our team](https://redis.io/meeting/) about the context layer under your agents.
