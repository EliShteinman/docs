---
title: "Context compaction for AI agents: a complete guide"
linkTitle: "Context compaction for AI agents: a complete guide"
url: "/blog/context-compaction/"
description: "Your agent just spent 40 turns debugging a gnarly authentication issue. It found the root cause, mapped out a fix, and started implementing. Then, somewhere around turn 45, it forgot everything it..."
date: 2026-05-25
blogCategories:
- "Tech DE"
authors:
- "Jim Allen Wallace"
lastmod: 2026-05-27
hidden: true
---

*By Jim Allen Wallace, Sr. Product Marketing Manager · Published 25 May 2026 · updated 27 May 2026*

![Context compaction: keeping AI agents on task as sessions grow](/images/blog/a4840624ce2d8c66371129bfe27792148aa87075-2400x1256.webp)

Your agent just spent 40 turns debugging a gnarly authentication issue. It found the root cause, mapped out a fix, and started implementing. Then, somewhere around turn 45, it forgot everything it learned and started investigating from scratch.

This is what happens when context windows fill up without a plan. As agents take on longer tasks, it's happening more often. This guide covers what context compaction is, why it matters, how it differs from truncation and retrieval-augmented generation (RAG), and where Redis fits in a broader context architecture.

## Why context compaction matters now

Context compaction matters because long agent sessions get expensive, slow, and forgetful fast. Without optimizations like prompt caching, every token in the context window typically gets re-processed and billed on every API call, so as conversation history piles up, each new inference call works through everything that came before. A session that keeps growing costs more per turn the longer it runs.

Cost is only part of the problem. As context length grows, latency also rises and recall can degrade. Bigger windows give agents more room to work, but they don't guarantee the model will keep using earlier information effectively. Context management has become a practical design problem, not just a model-capability problem.

That's why compaction is showing up alongside RAG and bigger context windows instead of competing with them. Each one solves a different problem, and compaction fills the gap the other two leave behind.

## What context compaction actually is

Context compaction takes a conversation approaching the context window limit, condenses its contents into a structured, high-fidelity representation, and reinitiates a new context window with that condensed form in place of the raw history. The goal is to let the agent continue with minimal performance degradation.

Think of it as a skilled engineering handoff note. After a two-week sprint, a senior engineer doesn't hand the next engineer a full Slack export. They write a structured document covering decisions made, the reasoning behind them, open issues, and current system state. The raw back-and-forth is gone, but everything needed to continue without losing ground is preserved.

This is different from naive truncation, which mechanically removes tokens at a boundary to stay within the limit. Truncation doesn't care whether it's cutting a critical architectural decision made early in a session or throwaway chatter. It's also different from basic summarization, which rewrites history as prose and may drop specific numbers or exact phrasing whose importance only becomes apparent later.

Good compaction preserves active constraints the agent is still bound by, open decisions not yet acted on, and completed-task state. It discards the exploratory process that led to decisions, redundant tool outputs already reflected in agent state, and verbose intermediate steps.

## How context compaction fits into your context strategy

With the definition in place, the next question is where compaction sits in a broader context strategy. It's one piece of a bigger picture, not a standalone fix. It's the "compress what's already in the window" step: keep the tokens the model still needs, drop the rest, and keep the session moving.

A simple priority order helps here. Start with raw context. Move to reversible compaction (where dropped content still exists elsewhere and can be fetched back) when the window gets tight. Only fall back to lossy summarization (where dropped content is permanently destroyed) when nothing cheaper works. Compaction lives in the middle of that stack: useful when the raw history no longer fits, but before you start throwing signal away.

Reach for compaction when long tasks need continuity across many tool calls, when tool results are blowing up the context, or when agents have to keep working across context resets. Skip lossy compaction when exact wording matters, like legal text or precise API responses, or when the task still fits comfortably in the window.

## Common patterns for context compaction

Once you've decided compaction belongs in your stack, the next decision is how to implement it. There's no single "right" way to compact context. Most teams pick from a handful of common patterns based on how long their sessions run, how much tool output they generate, and how much they can afford to lose. Here are the main ones.

### Sliding windows

Sliding windows keep the last N conversation turns and drop everything older. Context size stays predictable and bounded, but anything from dropped turns is gone for good. It works best for stateless or short-horizon tasks where early turns genuinely don't matter later.

### Token-count thresholds with lossy summarization

This pattern watches token usage and triggers summarization once the context hits a set fraction of the window. It's easy to wire up, but LLM-based summarization gives you limited control over what survives, and the output can vary from run to run.

### Tool output offloading (reversible)

Tool output offloading writes large tool results to an external store and leaves a reference pointer plus a short preview in the context. Nothing is destroyed, and the agent can pull the full content back when it needs it. This is a good fit when tool calls return long payloads the agent only occasionally needs in full.

### Staged compaction under pressure

Staged compaction graduates through progressively more aggressive strategies instead of jumping straight to lossy summarization. Lighter moves like masking unused fields or pruning stale turns often free up enough space on their own, so lossy summarization becomes a last resort instead of a default.

### Reversible vs. lossy: the key distinction

The biggest split across these patterns is whether the compaction is reversible or lossy. Reversible compaction removes information that still exists somewhere else, so the agent can fetch it again with a tool call. Lossy summarization permanently destroys whatever doesn't make it into the summary. Which one you choose shapes what the agent can still do later, so it's worth evaluating against the tasks the agent has to finish.

## Context compaction vs. bigger windows & RAG

A common pushback on compaction is that bigger context windows or RAG should make it unnecessary. They don't. Bigger context windows don't eliminate the need for compaction. They increase capacity, but they also raise the risk of higher cost, higher latency, and weaker recall as context grows.

RAG doesn't eliminate the need for compaction either. RAG handles retrieval of external knowledge but does not manage the agent's own evolving working memory across a long-running task. And compaction alone isn't sufficient. In practice, all three strategies often work as complementary layers: RAG retrieves external knowledge, larger windows provide ceiling capacity, and compaction manages accumulated session state within that ceiling.

## Where context engines come in

Compaction doesn't run in isolation. It usually sits inside a broader system that decides what context goes into the model on every turn. That system is the context engine: the architectural layer responsible for determining what information enters the LLM's context window at each reasoning step, managing selection, compression, retrieval, and routing of information from multiple sources into a coherent, token-efficient input.

At the architectural level, compaction can be combined with external memory so the full history is preserved elsewhere before the window is overwritten. The compaction mechanism itself can be implemented without external memory, but recoverable production compaction often relies on external memory so state can be restored after compression. Context compression manages what the agent sees this session, while external memory manages what the agent stores across sessions.

That external memory layer only helps if the data inside it stays current. Batch-oriented pipelines often can't serve the freshness requirements of agentic systems, and if your compacted summaries and embeddings are built on stale data, the agent acts on outdated context regardless of how well the compaction was performed.

## How Redis Iris supports context compaction

All of this is what [Redis Iris](https://redis.io/iris/) is built for. Iris is Redis' real-time context engine for AI: a single layer that sits between the agent and the data it needs, feeding the right context, in the right form, at the right time. It [bundles five tools](/blog/context-is-all-you-need/) (Redis Context Retriever, Redis Agent Memory, Redis Data Integration, Redis LangCache, and Redis Search) into one runtime, so memory, retrieval, freshness, and caching aren't separate vendors glued together. These are managed Redis capabilities, not features you flip on in a self-hosted Redis Open Source build.

For compaction workflows specifically, three pieces of Iris do most of the work.

[Redis Agent Memory](https://redis.io/docs/latest/develop/ai/context-engine/agent-memory), currently in preview, uses a two-tier memory model that maps cleanly to compaction. Working memory holds session-scoped events bounded by a configurable time to live (TTL). Long-term memory persists cross-session knowledge as vector embeddings retrieved through semantic search. Active context stays bounded in the session while high-signal information lives separately and gets pulled in when the agent needs it.

Redis LangCache, a fully managed semantic caching service, [reduces repeated context injection](/blog/context-engineering-best-practices-for-an-emerging-discipline/) by recognizing when queries are semantically similar despite different wording. In Redis benchmarks, LangCache reported [up to 15x faster](/blog/context-window-management-llm-apps-developer-guide/) responses for cache hits and [up to 73% lower](/blog/llm-token-optimization-speed-up-apps/) LLM inference costs without code changes. For compaction workflows, that means fewer redundant LLM calls when agents hit variations of questions they've already answered.

Redis Data Integration [keeps operational state fresh](https://redis.io/redis-for-ai/) so agents act on current business context instead of stale exports. That matters for compaction because a perfectly compressed summary built on yesterday's data still makes the agent act on yesterday's reality.

The shared idea across Iris: one runtime for vectors, caching, memory, retrieval, and operational data, instead of stitching together a separate system for each layer of the context stack.

## Build context compaction into the stack

Context compaction helps agents keep working when sessions get long, tool output grows, and raw history stops being practical. It works best as a deliberate architectural choice, not an emergency move when the window is already full: raw context first, reversible compaction when the window gets tight, lossy summarization only as a last resort.

Bigger windows and RAG help, but they don't replace deliberate context management. Iris gives teams already running Redis for [caching](https://redis.io/glossary/database-row-caching/) or session management a way to layer agent context onto infrastructure they already trust, instead of standing up a separate stack of vector, memory, and caching vendors.

[Try Redis Iris for free](https://redis.io/try-free/?rcplan=iris) to start building context-aware agents on a real-time data layer, or [book a meeting](https://redis.io/meeting/) to talk through how Iris fits into your AI stack.
