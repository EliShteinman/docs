---
title: "Long-horizon tasks: building agents that work over hours & days"
linkTitle: "Long-horizon tasks: building agents that work over hours & days"
url: "/blog/long-horizon-ai-agents-memory-state-infrastructure/"
description: "Early AI agents handled one-shot jobs that took a few minutes: fix this bug, write this function, generate this test. More recent workflows are multi-step, tool-using, and stateful over extended..."
date: 2026-05-21
blogCategories:
- "Tech DE"
authors:
- "Jim Allen Wallace"
lastmod: 2026-05-21
hidden: true
---

*By Jim Allen Wallace, Sr. Product Marketing Manager · Published 21 May 2026*

![Long horizon tasks: building agents that work over hours & days](/images/site-mirror/3a613a052b1b91c7970f2ed401392a671f2cf2c8-2400x1256.webp)

Early AI agents handled one-shot jobs that took a few minutes: fix this bug, write this function, generate this test. More recent workflows are multi-step, tool-using, and stateful over extended sessions — an agent might spend a full afternoon refactoring a service, running tests, reading logs, and iterating on the fix.

That kind of run depends on memory, state persistence, failure recovery, and the ability to resume after a crash. This guide covers what long-horizon agents need, why they fail, and how [Redis Iris](https://redis.io/iris/) provides the real-time context engine they depend on.

## What long-horizon tasks look like in the real world

Long-horizon agents are already doing real work across three domains: coding, research, and enterprise operations. The shared trait isn't just duration. It's that the agent has to hold onto state across many steps, often in messy environments where the right next move depends on something it learned an hour ago.

### Multi-hour coding work

Coding agents now sustain multi-hour autonomous work on real codebases. Anthropic reports Claude Sonnet 4.5 can maintain focus on coding tasks for [more than 30 hours](https://www.anthropic.com/news/claude-sonnet-4-5), and [Rakuten](https://www.anthropic.com/customers/rakuten) ran Claude Code for seven hours straight on a vLLM refactor across 12.5 million lines. To measure this kind of work, the field uses [SWE-bench Verified](https://www.swebench.com/) (real GitHub issues against real repos), where success requires tens to hundreds of steps, with state from early exploration shaping decisions hours later.

### Deep research as a shipping feature

Deep research has become the most visible shipping example. [Claude's Research feature](https://www.anthropic.com/engineering/multi-agent-research-system) spawns parallel subagents that explore different angles of a complex question, each in its own isolated context window, and synthesize results back to a lead agent. ChatGPT, Gemini, and Perplexity ship variations of the same pattern. These aren't experimental setups; they're features users hit when they ask anything that needs more than a single web search.

### Enterprise workflows across many systems

Enterprise workflows are where the shape gets hardest: agents have to stay coherent across many systems instead of going deep in one. A support agent might read a ticket in Jira, check a deploy log in CI, ask a teammate for clarification in Slack, pull a spec from a shared drive, and update the original ticket. Any one step is manageable on its own. The hard part is holding onto what was decided in chat an hour ago while reasoning about a file edited yesterday. [TheAgentCompany benchmark](https://the-agent-company.com/) simulates this shape across GitLab, RocketChat, and OwnCloud environments.

That's the promise. The reality is messier. The [task length](https://metr.org/time-horizons/) frontier agents can finish with 50% reliability is [doubling every seven months](https://metr.org/blog/2025-03-19-measuring-ai-ability-to-complete-long-tasks/), but in absolute terms it's still measured in hours, not days. On harder benchmarks like [LongCLI-Bench](https://arxiv.org/abs/2602.14337), state-of-the-art agents land below 20% pass rate; on [SWE-Bench Pro](https://scaleapi.github.io/SWE-bench_Pro-os/), the best public results still leave most tasks unsolved. Headline runs like Rakuten's seven hours are real, but they're the upper bound, not the baseline.

## Why most agents break after a few steps or sessions

Reliability drops sharply as task length grows, and the failures fall into common patterns that compound over long runs. Four failure modes show up again and again.

### Context rot

Even before a context window hits its token limit, reasoning quality can degrade as the model's attention spreads across increasingly noisy history. Every thought-action-observation cycle appends to the context: tool outputs, intermediate conclusions, exploratory reasoning that may have been superseded. Without active management, the window can fill with low-density content that buries the constraints governing the current task. When hard truncation kicks in, it discards content by recency rather than relevance, silently removing early-session constraints that still apply.

### Memory drift

When agents rewrite their own memory through summarization, a different failure class emerges. An agent may distort facts through repeated summarization, reinforce suboptimal workflows, or internalize hallucinations as valid knowledge. Unlike errors in static retrieval where a bad result is isolated to a single step, errors in evolving memory are cumulative and persistent.

### Goal coherence loss

Over long runs, agents lose track of pending subgoals, become fixated on intermediate tool calls, or prematurely declare the task complete. Multi-step plans drift as the agent gets pulled into the most recent tool output and forgets what it was originally trying to do. The result is an agent that's busy but no longer aimed at the right target.

### Error compounding

Small per-step error rates compound across dependent steps into irreversible failures. An agent might hallucinate that a step succeeded and attempt to interact with a UI element that no longer exists, triggering a cascade of downstream errors.

## What long-horizon agents need to remember

LLMs are stateless. Every call starts from a blank slate. To work over hours or days, agents need an external memory layer that holds context the model itself can't. That layer has to do four things at once: keep the current task coherent, recall past decisions, build up knowledge over time, and pick up cleanly after interruptions.

A useful way to think about agent memory borrows from cognitive psychology and breaks it into four types, each playing a role in a long-horizon system:

### Working memory

What's in the model's context window *right now*. It's small, temporary, and disappears at the end of the session unless something else stores it. Everything below exists to decide what gets loaded into working memory at any given moment. [Redis Agent Memory](https://redis.io/agent-memory/) handles this layer with session memory that holds active conversation state, with configurable time-to-live (TTL) settings so context stays accessible without bloating the window.

### Episodic memory

A timeline of what the agent *did*: past conversations, decisions, tool calls, and their outcomes. This is what lets an agent answer "what happened yesterday?" or "did I already try that?" Redis Agent Memory extracts episodic events from session history and persists them to long-term memory, so they remain available even after a context window resets.

### Semantic memory

The agent's knowledge base: facts, rules, and domain context that don't change much over time. This is typically [stored as vectors](/blog/long-term-memory-architectures-ai-agents/) and pulled in through [retrieval-augmented generation (RAG) patterns](/blog/ai-agent-memory-stateful-systems/) when relevant. It's how an agent "knows things" without retraining the model. Redis Agent Memory embeds extracted facts and preferences as vectors for semantic recall, on Redis' in-memory architecture so retrieval doesn't bottleneck the agent loop.

### Procedural memory

The agent's playbook: reusable skills, workflows, and tool definitions. For agents with large tool registries (especially ones spanning multiple business systems), surfacing the right tools at the right moment is its own problem. [Redis Context Retriever](https://redis.io/context-retriever/) addresses this directly: teams define a semantic model of their business data, and Context Retriever auto-generates Model Context Protocol ([MCP](https://modelcontextprotocol.io/)) tools agents can discover and call at runtime. That's how an agent navigates a TheAgentCompany-style workflow across a ticket tracker, a chat system, and a file store without bespoke integrations or a bloated tool prompt.

The big picture: long-horizon reliability depends less on which model you pick and more on how cleanly these four memory types are stored, refreshed, and surfaced at the right moment. Keeping the underlying data current matters too. [Redis Data Integration](https://redis.io/data-integration/) continuously syncs operational databases via change data capture, so a multi-day agent isn't reasoning over data that was true yesterday but isn't now.

## Common patterns for keeping long-horizon agents on track

Memory alone isn't enough. Production agents also need patterns for how state flows, how they recover from failure, and how they avoid drowning in their own context. A handful of patterns show up repeatedly across long-horizon systems, and most production stacks combine several.

### Checkpoint-and-resume

Save the agent's state at every step so it can pick back up after a crash, an approval pause, or a bad decision. The state store needs to be durable, low-latency, and easy to scope to a session, since agents will read and write it constantly. Restarts from scratch are expensive; resumable systems are how small failures stay small instead of becoming catastrophic.

### Plan-then-execute

Instead of mixing planning and action at every step, split them. A larger, more capable model writes the full plan upfront, and a smaller, cheaper model works through the tasks one by one. Independent subtasks run in parallel, and the big model only comes back if the plan needs revision. This keeps cost down and reduces the chance of the agent losing the plot mid-run.

### Append-only event logs

Treat the agent's full history as a log of events you only ever add to. The "current state" is computed by replaying that log. This pattern (borrowed from [event sourcing](https://martinfowler.com/eaaDev/EventSourcing.html) in distributed systems) gives you durable history for audit, replay, and recovery without forcing the full history back into the context window.

### Context isolation & subagents

When one agent's context window starts to fill up, spin up subagents with fresh windows. Each subagent works on a scoped piece of the problem and reports back through a structured handoff rather than dumping its full history. That's what makes deep, multi-step research workflows feasible without melting the lead agent's context.

### Causal event graphs (advanced)

Flat memory tells you *what* happened. Causal graphs try to capture *why*: which events caused which outcomes, which entities are related, and how facts evolved over time. Research architectures like [MAGMA](https://arxiv.org/abs/2601.03236) use graph structures to disentangle temporal, causal, and entity relationships that flat retrieval blurs together. The trade-off: building and traversing these graphs is more complex and expensive than vector search, so most teams reach for this only when simpler patterns fall short.

These patterns compose. Checkpoints pair with event logs for rollback. Plan-then-execute pairs with subagents for clean delegation. Production-grade long-horizon systems usually combine several rather than betting on one.

## Redis Iris: one platform for the long-horizon context engine

Every one of these patterns assumes the same infrastructure: durable state, fast retrieval, and a way to keep underlying data fresh. [Redis Iris](https://redis.io/iris/) packages that infrastructure into a single real-time context engine (Context Retriever, Agent Memory, Redis Data Integration, [Redis LangCache](https://redis.io/langcache/), and Redis Search) instead of leaving teams to stitch together a vector database, a session store, an event log, an integration layer, and a cache.

Iris runs on the same in-memory architecture that already powers caching and real-time workloads at [more than 30%](https://redis.io/press/redis-labs-continues-momentum-large-enterprises-growing-60-percent-year-year/) of the Fortune 50. For agents, that foundation matters because latency has a snowball effect: every slow memory read or stale lookup compounds across hours of runtime, and stacked round-trips across separate services compound it further.

Cost is the other practical concern, since long-horizon memory stores grow with runtime. [Redis Flex](/blog/introducing-another-era-of-fast/), a tiered RAM and SSD storage option, can cut memory costs by up to 80%, so retaining long agent histories doesn't scale the bill linearly with retention.

## Long-horizon agents need memory infrastructure, not just bigger models

Context rot, memory drift, lost goals, and compounding errors aren't model problems. They're what happens when working, episodic, semantic, and procedural memory get jammed into a single context window with nothing to refresh, persist, or scope them. Bigger windows and stronger reasoning push the failure point out by a few hours. They don't change the shape of the curve.

The fix is durable state and fast retrieval outside the model. That's what [Redis Iris](https://redis.io/iris/) is built for: [Agent Memory](https://redis.io/agent-memory/) for session-to-session continuity, [Context Retriever](https://redis.io/context-retriever/) for the navigable tool surface, and [Data Integration](https://redis.io/data-integration/) for keeping the underlying data fresh, all on Redis' real-time data platform.

To get started, [try Redis Iris free](https://redis.io/try-free/?rcplan=iris).
