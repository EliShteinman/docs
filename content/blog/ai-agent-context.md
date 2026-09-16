---
title: "Context engineering for AI agents: the infrastructure behind every decision"
linkTitle: "Context engineering for AI agents: the infrastructure behind every decision"
url: "/blog/ai-agent-context/"
description: "Your agent is only as good as the information it can see at decision time. The data sitting in your infrastructure doesn't count, and neither does what the model learned in training months ago...."
date: 2026-06-09
blogCategories:
- "Tech DE"
authors:
- "Jim Allen Wallace"
lastmod: 2026-06-10
hidden: true
mirrored: true
---

*By Jim Allen Wallace, Sr. Product Marketing Manager · Published 9 June 2026 · updated 10 June 2026*

![Context engineering for AI agents: the infrastructure behind every decision](/images/site-mirror/260ce2e01fd30c991b2ccdfa73189efba4372ab2-2400x1256.webp)

Your agent is only as good as the information it can see at decision time. The data sitting in your infrastructure doesn't count, and neither does what the model learned in training months ago. What counts is the specific tokens loaded into its context window the moment it picks its next action.

Context engineering is how you curate what goes into that window from an ever-growing pile of possible inputs. It's the whole information lifecycle: selection, retrieval, filtering, compression, and refresh. Prompt engineering is about *how* you describe the task. Context engineering is about *what* the model can actually see at every inference step.

That difference matters because agents run in loops. Each iteration, the model gets a context window and produces an action. Every token wasted on low-signal content is a token your agent can't use to reason. A lot of agent failures you'll debug at 3 AM aren't model failures. They're context failures.

This article covers what context actually contains when an agent makes a decision, the six inputs fighting for that finite token budget, and why assembling them fast enough is an infrastructure problem, not a prompt problem.

## What goes into an AI agent's context window

Every agent decision draws on the same finite context window, and six categories of input compete for that space at every inference call:

- **System instructions:** The agent's standing orders. Its role, rules, and constraints, loaded once and held for the whole session.
- **Goal specification:** The job for this run. It's the directive the agent measures its progress against.
- **Conversation memory:** What's happened so far in the session: prior turns, tool call results, and intermediate reasoning.
- **Retrieved external knowledge:** Docs, facts, or records fetched from sources the model wasn't trained on.
- **Tool definitions:** Structured schemas that tell the model what it can call and what each call expects.
- **Execution state:** Where the agent is in its task, what it's done, and what's still left to do.

The engineering challenge is deciding what earns its way into the window at each step. The sections below walk through these inputs and the demand each one places on your infrastructure.

## System instructions & goal: what stays constant

System instructions and the goal are the parts of context that stay stable across an entire run. System instructions define who the agent is, how it operates, and what rules it follows. They load first and persist across the full session, setting the behavioral frame for every decision that follows.

The goal is structurally separate, even though it feels just as constant. System instructions are role-defining: they describe the agent. The goal is task-defining: it describes what the agent is trying to accomplish in this specific run. The agent evaluates progress against the goal at every step.

Together, these two inputs form the scaffolding that everything else hangs on. They rarely change mid-session, but they consume tokens that the dynamic inputs have to work around.

## Agent memory: what carries across turns & sessions

While instructions and the goal stay fixed, memory is the first of the dynamic inputs. It carries useful information forward, both between steps in a single run and across sessions. Agents need it because LLMs don't retain anything between inference calls on their own; every turn starts from a blank slate unless memory feeds context back in. There are two types, and they solve different problems.

### Short-term memory

Short-term memory is the running record of the current interaction: prior turns, tool call results, and intermediate reasoning. It lives inside the context window itself, which means it's fast to access but bounded by the model's token limit. Even with large context windows, dumping full conversation history into every inference call drives up cost and latency. Teams typically trim older messages, summarize completed phases into compressed representations, or filter by relevance to keep the window lean.

### Long-term memory

Long-term memory outlives a single session. It stores past events, generalized facts, and user preferences that should carry across conversations, so the agent remembers what a user told it last week, not just last turn. Because it lives in an external store, every read and write adds time to the loop, which makes speed the core infrastructure requirement for memory.

## Retrieval & RAG: pulling external knowledge at query time

Memory covers what the agent has already seen. Retrieval covers what it hasn't: knowledge from outside the session that the model wasn't trained on, like your company's docs, product catalog, or customer records. Retrieval-augmented generation (RAG) supplies an LLM with this external knowledge at inference time. The pipeline has three stages: generate vector embeddings for the query, search an index for the most similar chunks, and inject those chunks into the context window alongside the original query.

Retrieval quality drives output quality in these systems. Irrelevant material in long contexts can increase hallucination, and relevant documents buried in the wrong position may not influence generation at all. Garbage in, garbage out applies as much to retrieved context as it does to training data.

Search method is part of that quality equation. Pure vector search can miss exact-match terms like product codes, regulatory article numbers, and proper nouns, because vector embeddings compress meaning into continuous space. Hybrid search reduces those misses by pairing vector retrieval with keyword matching, often using Reciprocal Rank Fusion (RRF) to merge the ranked lists.

Retrieval itself can also become autonomous. In agentic RAG, the agent decides when and how to retrieve rather than always retrieving on every query. Some patterns invoke retrieval based on query complexity or model state, and corrective architectures can gate retrieval quality before generation proceeds.

## Tools & state: what the agent can do & where it is

Once retrieval adds outside knowledge, the next constraint is action: what the agent can call and what it knows about its own progress. Tool definitions are not free context. They are injected directly into the model's prompt as JSON Schema specifications, and callable function definitions count against the model's context limit as input tokens.

As the number of available tools grows, this overhead becomes a real problem. Loading all tool definitions upfront creates context window bloat, degraded tool selection accuracy, and increased inference latency. One response is dynamic tool retrieval: bind only the tools that are relevant for a given request. Multi-agent architectures take this further by grouping tools across specialized agents, because an agent is more likely to succeed on a focused task than when selecting from dozens of tools.

The Model Context Protocol (MCP) provides a unified JSON-RPC interface for agent-to-tool communication, which helps standardize how agents discover and invoke tools across platforms. But standardization does not remove the token cost: each tool still consumes context space.

Execution state is the agent's answer to "where was I?" Instead of stuffing full data objects into context, production agents usually keep lightweight references, an ID or a pointer, and pull the actual data through a tool call when they need it. The working context stays small, and the agent doesn't lose access to anything.

## Why assembling context fast is an infrastructure problem

Here's the catch: tools, memory, retrieval, and state don't live in one place. They're spread across systems with different speeds, so every agent decision step kicks off a round of fetches: working state from one store, memory from another, tool definitions, real-time features. The model can't reason until the last one lands.

The latency budget is tight. One paper on real-time voice agents framed [sub-200ms turn latency](https://arxiv.org/html/2603.02206v1) as the threshold for natural-feeling conversation, with that budget covering speech-to-text, context retrieval, LLM generation, and text-to-speech. Real pipelines routinely blow past it: the same paper notes that network round trips to a remotely hosted vector store can consume the entire budget on their own. Per-step costs also multiply: a multi-step agent loop applies retrieval overhead at every step before accounting for inference time.

That's why an AI engineer should think in terms of a [context budget](/blog/engineering-for-ai-agents/) that includes both token count and time. The context layer needs to serve multiple access patterns fast enough to stay off the critical path: key-value reads, [vector and full-text search](https://redis.io/resources/redis-query-engine/), and session state. Redis uses a memory-first architecture and delivers [sub-millisecond performance](/blog/redis-enterprise-extends-linear-scalability-200m-ops-sec/) for many core operations. Even at billion-vector scale, Redis [reported 90% precision](/blog/searching-1-billion-vectors-with-redis-8/) at roughly 200ms median latency when retrieving the top 100 nearest neighbors under 50 concurrent queries.

Writes pile up too. One user turn can fire off several memory writes in a row, and if each one is slow, you're stuck picking between two bad options: block until the writes land and make the user sit through it, or keep moving and let your agent reason on stale memory.

## Context assembly determines agent quality

Context only helps if your system can pull it together fast enough to matter. Every input in this article puts the same demand on your stack: the right data, at the right time, without the user ever noticing the assembly work.

That makes context engineering a data problem, not a model problem. The model can only reason about what lands in its window. The infrastructure underneath decides whether your agent feels snappy or sluggish, whether it works from fresh data or stale snapshots, and whether it holds up at thousands of concurrent sessions or falls over.

[Redis Iris](https://redis.io/iris/) is built for exactly this layer. It's a context engine that sits between your agents and your data and handles the assembly work in one runtime. Context Retriever turns your business data into structured tools agents can actually use, Agent Memory keeps short- and long-term memory across sessions (both are in public preview), Redis LangCache adds semantic caching that can cut your LLM inference costs, Redis Data Integration keeps everything in sync with your source databases, and Redis Search is the fast retrieval layer underneath it all.

[Try Redis free](https://redis.io/try-free/?rcplan=iris) and start building your agent's context layer, or [talk to our team](https://redis.io/meeting/) about getting context infrastructure ready for production.
