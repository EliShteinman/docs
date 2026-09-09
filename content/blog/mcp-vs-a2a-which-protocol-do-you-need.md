---
title: "Model Context Protocol (MCP) vs. Agent2Agent (A2A): which protocol do you need?"
linkTitle: "Model Context Protocol (MCP) vs. Agent2Agent (A2A): which protocol do you need?"
url: "/blog/mcp-vs-a2a-which-protocol-do-you-need/"
description: "Somewhere around your third agent, someone in a design review asks, \"Shouldn't we be using A2A for this?\" It's a fair question that most teams can't answer well, because the two big agent protocols..."
date: 2026-07-22
blogCategories:
- "Tech DE"
authors:
- "Jeff Mills"
lastmod: 2026-07-22
hidden: true
---

*By Jeff Mills, Director, Product Marketing · Published 22 July 2026*

![Model Context Protocol (MCP) vs. Agent2Agent (A2A): which protocol do you need?](/images/blog/e983f2dd60e0bb66d869efce0b81e6d6e2de2760-2400x1256.webp)

Somewhere around your third agent, someone in a design review asks, "Shouldn't we be using A2A for this?" It's a fair question that most teams can't answer well, because the two big agent protocols keep getting lumped together when they solve different problems at different layers. The Model Context Protocol (MCP) connects an agent to its tools and data. The Agent2Agent (A2A) protocol connects independent agents to each other. Whether you need one, both, or neither depends less on how many agents you have and more on who owns them. This guide covers what MCP and A2A each do, why the two are designed to work together, and a decision rule for telling whether your system needs A2A or just a good orchestration framework.

## What MCP does & how it works

MCP is an open standard for connecting LLM apps to external tools and data. Its architecture defines three roles:

- **Hosts:** the LLM app coordinating everything
- **Clients:** the connectors inside the host
- **Servers:** the endpoints that expose capabilities

Servers expose those capabilities through three primitives: tools the model can call, resources that supply context, and prompts that template workflows. Under the hood it uses JSON-RPC, a lightweight request-response format, sent over a local connection or HTTP, and it can stream results back as they arrive.

MCP spread fast once the major AI providers lined up behind it. OpenAI [adopted MCP](https://techcrunch.com/2025/03/26/openai-adopts-rival-anthropics-standard-for-connecting-ai-models-to-data) in March 2025 in its Agents SDK, with ChatGPT desktop support announced as coming soon. Google added [native MCP support](https://thenewstack.io/google-embraces-mcp) to the Gemini API and SDK. MCP later moved under the [Agentic AI Foundation](https://blog.modelcontextprotocol.io/posts/2025-11-25-first-mcp-anniversary) at the Linux Foundation.

In production, MCP shows up most clearly in three places:

- **Developer tooling and observability:** during an incident, an agent pulls logs and metrics from systems like Grafana and Datadog in one place, instead of an engineer tabbing between dashboards at 2 a.m.
- **Knowledge-worker copilots:** a chat assistant reaches into systems of record like Salesforce and meeting notes to prep for a call.
- **Self-serve analytics:** non-technical teams query an internal data warehouse in plain language instead of filing a ticket to the data team.

Those uses are appealing, but governance is the gating question, and MCP provides little of it on its own. Enterprises split into two camps: those building their own access control, audit logging, and middleware now because they can't wait, and those holding sensitive workloads back until the protocol matures.

Two traits define MCP's shape, and both resurface when you weigh it against A2A. First, the interaction is hierarchical: an agent calls down to a passive server that answers and waits. Second, there's no built-in discovery; you point each client at a preconfigured server endpoint.

## What A2A does & where it came from

That hierarchical, preconfigured model is exactly what A2A isn't. A2A is built for communication between independent, potentially opaque agents owned by different teams, vendors, or companies. It defines three core pieces:

- **Agent Cards:** [JSON documents](https://a2a-protocol.org/latest/topics/key-concepts) served at /.well-known/agent.json that declare an agent's identity, endpoint, authentication requirements, and skills.
- **Tasks:** stateful units of work with a defined lifecycle, including human-in-the-loop pauses.
- **Artifacts:** the concrete outputs a remote agent returns.

Like MCP, A2A runs JSON-RPC 2.0 over HTTP, but it adds Server-Sent Events (SSE) streaming and push notifications for tasks that can run for hours or days.

Google introduced A2A, then donated it to the Linux Foundation in June 2025 with founding members including AWS, Microsoft, Salesforce, and SAP. One year in, [more than 150 organizations](https://www.linuxfoundation.org/press/a2a-protocol-surpasses-150-organizations-lands-in-major-cloud-platforms-and-sees-enterprise-production-use-in-first-year) supported the standard, and it had landed in major cloud and agent platforms.

For all that surface adoption, A2A is still mostly exploratory in practice. Real cross-organization, cross-framework agent traffic remains rare, and most systems described as "multi-agent" today are really one team's orchestrator calling tools in sequence, not independent agents crossing a trust boundary. That gap between ambition and practice is worth keeping in mind.

## Complementary, not competing

None of this makes the two protocols rivals. A2A complements MCP by drawing a line between agents partnering on tasks and agents using capabilities. That tool-vs-agent split shapes the dimensions that typically drive architecture decisions:

| Dimension | MCP | A2A |
|---|---|---|
| Purpose | Agent-to-tool integration | Agent-to-agent collaboration |
| Communication model | Client-server; agent calls a passive tool | Peer-to-peer; agent delegates to another agent |
| Interaction pattern | Request-response per the spec (servers may hold state) | Stateful, multi-turn, long-running tasks |
| Discovery | Explicitly configured endpoints | Agent Cards at a well-known URL |
| Core primitives | Tools, resources, prompts | Tasks, messages, artifacts, Agent Cards |

The split looks like an auto repair shop: a customer's agent talks to the shop manager agent over A2A, the manager runs a multi-turn diagnostic conversation with a mechanic agent over A2A, and the mechanic invokes its diagnostic tools over MCP. With MCP under the Agentic AI Foundation and A2A under the Linux Foundation, the governance story is converging too.

In practice, the tool-versus-agent line is blurrier than the table suggests. Ask an assistant to shorten a paragraph in a shared document: it sounds like a simple tool call. But to make the edit, the document's API needs to know a document ID, a section ID, and where in the text to cut, none of which the user provided. The "tool" has to work those out on its own, which is the kind of reasoning we associate with agents. What you label a component matters less than what the task actually requires of it.

## The real question: do you own your agents?

The question that trips teams up is easy to ask and easy to get wrong: should we be using A2A? A2A gets read as the multi-agent protocol, so any system with more than one agent starts to feel like it needs one. It usually doesn't. A network protocol like A2A adds real cost in setup, authentication, and moving parts, and that cost only pays off when your agents have to work with software you don't own or control. Inside a codebase you do own, a framework like [LangGraph or CrewAI](/blog/ai-agent-orchestration-platforms/) can coordinate your agents without a protocol in the middle.

A2A's design backs this up. The protocol is built so agents can work together without exposing their "internal memory, [tools, or proprietary logic](https://a2a-protocol.org/latest/)" to each other. That secrecy is the whole point when you're handing work to a partner's agent or a vendor's black box. When you own the agent on the other side, there's little to hide, so you pay the protocol's overhead without getting much interoperability in return.

So the useful question isn't how many agents you have, but whether they cross a real boundary. Do they sit behind separate security and permission scopes, or do they all run under one team's control? Several agents built by the same team, sharing the same permissions, rarely need a formal protocol between them. A2A earns its place when an agent brings its own identity and permissions that yours has to respect, not simply when there's more than one agent in play.

None of this is a knock on A2A; it's about fit. The case for it is strongest exactly where simple tool-calling breaks down: work that hands off between agents asynchronously, waits on human approval, or runs as a long back-and-forth instead of a single request and response. Large teams tend to land here in practice. LinkedIn, for one, adopted MCP and A2A together for its enterprise agents while still treating A2A as [the more experimental](https://www.infoq.com/news/2025/09/linkedin-multi-agent) of the two.

So it comes down to one question: who owns the agents? That splits the decision two ways:

- **Reach for A2A** when work delegates across a boundary you don't control and neither side can expose internal tools or memory, when tasks run long enough to need a stateful lifecycle with approval gates, or when agents on different frameworks must interoperate without custom glue.
- **Stick with in-framework orchestration** when all your agents are white-box components in a codebase you own. That's a classical orchestration problem, not an interoperability one.

Like most architecture guidelines, this one bends with your workload, but it catches the common mistake: adopting a cross-organization protocol for a single-team system.

## The problems neither protocol fully addresses

Whichever side of that line you land on, both protocols leave the same work to you. They carry messages between agents; they don't manage the state, visibility, speed, or memory underneath.

### Correlating state across a workflow

Neither spec ties the pieces of a workflow together. Even with A2A's contextId for grouping related tasks, nothing links an agent's internal context, MCP server state, and A2A task identifiers into one traceable thread. It's part of a broader class of multi-agent problems: task allocation, [context management, and memory](https://arxiv.org/html/2601.11369v2) all get harder than they are in single-agent designs.

### Observability & performance

Watching what your system does gets harder too. Once one agent starts calling others, it's tough to tell which agent or tool actually produced a given answer, and the more they call each other, the tougher it gets. Agents are also less predictable than a plain tool, so even confirming that one ran and did its job well is real work. And piecing together a single, end-to-end picture of what happened across both MCP and A2A is still something every team hacks together on its own.

Speed is the other half of this. In one analysis of agent workloads, the model's own thinking took [69.4% of the time](https://arxiv.org/html/2506.04301v2) on average, and running tools took another 30.2%. You can't overlap the two much, since each waits on the other. MCP adds its own catch: every tool you connect has to be described to the model, and those descriptions eat into its context window. Past a point, adding more tools [makes agents worse](/blog/from-reasoning-to-retrieval-solving-the-mcp-tool-overload-problem/), not better, with the model picking the wrong tool more often and responses slowing down and costing more.

### No standard for agent memory

There's also no common interface for agent memory itself. Teams improvise how agents store and recall state, and whether that memory is a flat file or something more structured, because no protocol standardizes it. That's the layer that decides whether work survives a crash or a returning user, and it sits below whichever protocol carries the messages.

### Where Redis fits

[Redis Iris](https://redis.io/iris/) is built for exactly this layer: a real-time context engine that sits between your agents and the data they act on, on the same Redis many teams already use for [caching and sessions](/blog/cache-layer-architecture-guide/). It handles the work agents keep reinventing, remembering context across sessions, caching repeated calls, and retrieving the right data fast. Picture a travel-planning agent that holds context across steps and picks up where it left off after a failure, or when a customer returns days later. That state has to live somewhere, no matter which protocol moves the messages.

Redis keeps that layer in memory for speed. [Core in-memory operations](/blog/ai-agent-api/) run at sub-millisecond latency. Vector search is heavier, but in a billion-vector benchmark with 50 concurrent queries retrieving the top 100 nearest neighbors, Redis reported [90% precision](/blog/searching-1-billion-vectors-with-redis-8/) at ~200ms median latency, including round-trip time. And Redis LangCache, its semantic caching service, reported up to [73% lower costs](/blog/llm-token-optimization-speed-up-apps/) for LLM inference in high-repetition workloads.

Redis plugs into both protocols directly, too. The [Redis MCP Server](/blog/introducing-model-context-protocol-mcp-for-redis/) gives MCP clients like Claude Desktop, Cursor, and the OpenAI Agents SDK a natural-language interface to data in Redis, and Redis added [A2A integrations](/blog/agents-vs-workflows/) in its Fall 2025 release. Because Redis sits outside any single framework, it becomes [the layer frameworks share](/blog/agent-interoperability-complete-integration-guide/) instead of another silo.

## Build what the protocols leave to you

The protocol question turns out to be a boundary question. Reach for A2A when your agents cross a boundary you don't own, and lean on orchestration and shared state when they don't.

Either way, the protocol only moves the messages. The context behind them, session state, memory, fast retrieval, and coordination, is yours to build, and its cost multiplies at every hop in a chained workflow. Redis Iris is that layer, on infrastructure many teams already run, whichever protocol carries the messages. [Try Redis free](https://redis.io/try-free/) to see how it fits your agent stack, or [talk to our team](https://redis.io/meeting/) about your AI infrastructure.
