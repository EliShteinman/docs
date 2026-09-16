---
title: "When does the A2A protocol actually matter?"
linkTitle: "When does the A2A protocol actually matter?"
url: "/blog/when-does-a2a-protocol-matter/"
description: "If you're building multi-agent systems, someone has probably asked whether you're \"doing A2A yet,\" with the implication that you should be. When teams actually reach for it, most can't say why they..."
date: 2026-08-04
blogCategories:
- "Tech DE"
authors:
- "Jeff Mills"
lastmod: 2026-08-05
hidden: true
mirrored: true
---

*By Jeff Mills, Director, Product Marketing · Published 4 August 2026 · updated 5 August 2026*

![When does the A2A protocol actually matter?](/images/site-mirror/f430e377d3a159e8d217c8448dbbfff0ee2406dc-2400x1256.webp)

If you're building [multi-agent systems](/blog/ai-agent-orchestration-platforms/), someone has probably asked whether you're "doing A2A yet," with the implication that you should be. When teams actually reach for it, most can't say why they need A2A over MCP. A more useful question: do your agents ever talk to an agent you don't own? If the answer is no, you can likely skip the protocol entirely. A2A is most useful when independently deployed agents, especially those owned by different teams or vendors, need a shared communication contract. Many multi-agent systems never hit that situation. This guide covers what A2A is, the ownership test that decides whether you need it, how its security model works, why production prevalence remains unclear, and how it fits with the Model Context Protocol (MCP).

## What is the A2A protocol?

A2A is an open standard for communication between independent agents, including agents that use different frameworks or languages or come from different vendors. Google announced it in April 2025 at Google Cloud Next, then donated it to the Linux Foundation in June 2025. The Linux Foundation now governs it, with founding members including Amazon Web Services (AWS), Google, Microsoft, and Salesforce. The current spec is [version 1.0.1](https://github.com/a2aproject/A2A/blob/main/CHANGELOG.md), released May 2026.

The protocol runs on a handful of core primitives:

- **Agent Card:** a JSON metadata document that describes an agent's identity, capabilities, skills, service endpoint, and authentication requirements. Clients can obtain it from a well-known URI, a registry, or direct configuration.
- **Task:** the fundamental unit of work, with a unique identifier (ID) and a lifecycle that can pause for input or credentials and end in success, failure, or cancellation.
- **Message and Part:** a single turn of communication, composed of parts carrying text, files, or structured data.
- **Artifact:** a tangible output an agent generates during a task.

Those primitives travel over standard web transport, so it needs no exotic infrastructure. Most implementations run JSON-RPC 2.0 over HTTP, and for tasks that run for hours or days, a server can push updates to a client-provided webhook instead of holding a connection open. One design principle ties it together: opaque execution. Agents collaborate through what they declare and the context they exchange, without exposing their internal logic, memory, or tools to each other.

### What A2A is not

A lot of the confusion about A2A comes from what people assume it replaces. Three things it isn't:

- **A tool-calling protocol.** The MCP section below explains the split between agent collaboration and tool access.
- **An agent framework.** It's a framework-agnostic wire protocol, whether agents use Agent Development Kit, LangGraph, or CrewAI.
- **A mandate to make everything an agent.** A calculator, a weather API, and a database query are straightforward tools, not agents; the agent abstraction adds overhead without adding clarity when the thing has no autonomy or lifecycle of its own.

It's also not a governance layer: it standardizes how agents exchange tasks, but shared enterprise ontologies, data lineage, and governance policies sit above it, not inside.

## Who owns the agent decides whether A2A matters

That boundary question does most of the work. If you own and control every sub-agent inside one runtime and trust boundary, you probably don't need A2A: your orchestration framework can coordinate them, and MCP handles their tool and data access. Adding it on top mostly [adds overhead without benefit](/blog/5-agent-architectures-mcp-a2a-protocol-guide/).

The deciding factor isn't whether agents are "internal." It's whether they cross a genuine boundary, which can happen inside one company: agents that are separately deployed, owned by different teams, or in different trust zones. It's the same call you make with internal APIs. You don't wrap every in-process function call in REST, only the ones that cross a real boundary.

### Inside one boundary, orchestration is enough

When one team owns every agent in the same deployment boundary, frameworks can coordinate them without another network protocol. LangGraph sub-agents coordinate through a shared scratchpad of messages in graph state. CrewAI ships a unified memory system and treats A2A as an option for external collaboration, not a requirement.

Single-boundary systems still need fast, durable state, because agent trajectories get big fast. In one benchmark, a single GitHub issue's trajectory averaged [48.4K tokens](/blog/agentic-ai-architecture-examples/) across 40 steps, and that state must live somewhere agents can read and write quickly. Redis handles short-term caching, long-term recall through vector search, and coordination between agents in one place, with a 20-node AWS cluster benchmark reporting sub-millisecond latency at more than [100 million operations](/blog/redis-enterprise-extends-linear-scalability-200m-ops-sec/) per second. Its managed Agent Memory service, part of the [Redis Iris](https://redis.io/iris/) context engine, keeps short- and long-term memory persistent across sessions. That's why Redis tied with GitHub MCP Server as the top choice for AI agent data storage and memory in the 2025 Stack Overflow AI survey, at [43% adoption](https://survey.stackoverflow.co/2025/ai), and why LangGraph's long-term memory stores include Redis backend support.

### Across boundaries, a shared contract helps

That calculus changes the moment an agent you don't own enters the picture. Without a shared standard, connecting to another company's or team's agent means maintaining bespoke integration code for every partner: peer endpoints, authentication, and interface changes, all by hand. That's the work A2A standardizes, across three mechanisms:

- **Discovery:** instead of hunting for a partner's docs, a client fetches its Agent Card and gets what it needs to start talking.
- **Capability negotiation:** each skill declares what it takes as input and what it returns, so two agents can agree on formats without ever seeing each other's internals.
- **Task lifecycle:** for work that doesn't finish in one request, a task can pause for more input or credentials, and push notifications keep long-running work moving after the client disconnects.

Crossing a boundary adds an observability cost too. As calls fan out from one agent to another, tracing which sub-agent produced a given answer gets harder, autonomous sub-agents are less predictable than deterministic tool calls, and stitching a single coherent trace across separate agents and servers is still largely unsolved. Consistent shared state is what gives you something stable to attribute against.

Those mechanisms standardize collaboration, but they only work safely when identity and authorization stay explicit at the trust boundary. That requirement makes the protocol's transport-layer security model central to any cross-boundary deployment.

## Why security boundaries are the deciding factor

Cross-company setups like those work because A2A treats every remote agent as a standard HTTP-based enterprise app rather than a trusted colleague inside your process. Its payloads carry no user or client identity, so your gateway and identity provider decide who the caller is, not anything inside the agent message. HTTPS is mandatory for production, credentials come from outside the protocol through flows like Open Authorization (OAuth) 2.0, and the server must authenticate every request.

The Agent Card is where an agent declares which authentication schemes it accepts, from OAuth 2.0 flows and API keys to mutual Transport Layer Security (mTLS). Individual skills can be gated behind specific OAuth scopes, and if a task needs extra credentials mid-run, it pauses while the client supplies them out of band. Version 1.0 also added Signed Agent Cards for cryptographic identity verification, so a client can confirm a card is genuine before trusting anything it says.

### Delegating reduced-scope permissions

Delegation is the hardest part of crossing a trust boundary. When one agent hands a task to another, the second shouldn't inherit all of the first's permissions, or you hit the classic confused-deputy problem: an agent borrowing access it was never meant to have. The usual fix is OAuth token exchange, which swaps a token for a narrower one and records who delegated to whom.

A2A leaves this to you. It [doesn't implement](https://github.com/a2aproject/A2A/issues/19) delegated authentication itself, deferring to your external identity provider (IdP), and it doesn't judge whether an agent should be trusted with a task. Standards work is still catching up, with active Internet Engineering Task Force (IETF) drafts on [identity chaining across domains](https://datatracker.ietf.org/doc/draft-ietf-oauth-identity-chaining) and delegated-scope rules, some updated as recently as July 2026. Until those land, teams crossing real boundaries wire up reduced-scope delegation from OAuth themselves.

MCP is further along here, which is part of why teams reach for it first: it treats servers as OAuth resource servers and supports delegated authorization through a third-party authorization server, hardened for enterprise use in its [2025-11-25 spec](https://modelcontextprotocol.io/specification/2025-11-25/basic/authorization).

## Why A2A production prevalence is still unclear

The delegation gap may be slowing adoption, but we don't have enough independent data to say how common production A2A is. The standard had [more than 150 organizations](https://www.linuxfoundation.org/press/a2a-protocol-surpasses-150-organizations-lands-in-major-cloud-platforms-and-sees-enterprise-production-use-in-first-year) publicly listed as supporters as of April 2026, with production deployments reported across industries and integrations on Google, Microsoft, and AWS. Impressive on paper, hard to verify from the outside.

The deeper reason adoption is murky is architectural. Many systems described as "multi-agent" today are really one orchestrator calling tools in sequence, not separate agents crossing a trust boundary. Plenty of 2025's agent demos didn't need A2A at all; they needed better prompts, tools, permissions, and logs.

## How A2A & MCP fit together

Passing on A2A doesn't mean skipping protocols. MCP does a lot of the work people assume A2A does, and the two aren't interchangeable. MCP connects an individual agent to the tools and data sources it needs to do its job, like a GitHub repository or a SQL database. A2A connects agents to each other so they can collaborate across frameworks. That distinction matters more than either protocol's marketing, and MCP's traction reflects it: MCP SDKs logged more than [400 million monthly downloads](https://blog.modelcontextprotocol.io/posts/2026-07-28/) as of July 2026.

The split holds most of the time, but the line is blurrier than the marketing suggests, and it's moving. MCP isn't standing still: it's adding asynchronous, long-running task primitives that overlap with what A2A's task model was built to provide. The tool-versus-agent line blurs too. Asking an agent to shorten a paragraph in a shared doc sounds like a plain tool call, but the underlying call needs a document ID, a segment, and an index the user never supplied, so the "tool" ends up doing agent-like reasoning under the hood. Definitions are converging faster than the protocols meant to separate them.

Imagine a customer talks to a shop manager agent over A2A. The manager runs a diagnostic conversation with a mechanic agent, also over A2A. The mechanic uses MCP to drive its diagnostic scanners and pull up repair manuals. Tools speak MCP; independently deployed agent collaborators may speak A2A. Establish tool access with MCP first, and add A2A only when a boundary becomes a real deployment, ownership, or interoperability constraint.

## A2A is a boundary decision, not a default

The MCP-and-A2A split reinforces the ownership test: use each protocol only at the boundary it was built to handle. If every agent belongs to you and runs inside one trust boundary, your orchestration framework can usually cover coordination while MCP handles tool and data access, and adding A2A gives you a discovery layer, a task lifecycle, and an auth surface you probably don't need yet. Once agents cross into another team's or vendor's territory, with their own deployments and permissions, A2A earns its place with a standardized contract instead of bespoke point-to-point code for every partner.

Whichever side of that line you land on, the protocol layer is only half the system. Neither MCP nor A2A standardizes where agents keep context, remember past work, and resume after a failure. That layer sits underneath both, has no common interface yet, and is where your agents' speed is won or lost. Redis provides that layer with Redis Iris, a real-time context engine for AI agents. Its Agent Memory service holds short- and long-term context across sessions and agents, in memory. [Try Redis Iris](https://redis.io/try-free/?rcplan=iris) to see how it fits your agent stack, or [talk to our team](https://redis.io/meeting/) about the data layer behind your multi-agent architecture.
