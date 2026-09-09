---
title: "Context assembly: building the prompt the model actually sees"
linkTitle: "Context assembly: building the prompt the model actually sees"
url: "/blog/context-assembly-building-the-prompt-the-model-sees/"
description: "The prompt a production LLM receives is almost never something a person wrote. By the time a request reaches the model, your app has stitched together system instructions, retrieved documents,..."
date: 2026-07-22
blogCategories:
- "Tech DE"
authors:
- "Jeff Mills"
lastmod: 2026-07-22
hidden: true
---

*By Jeff Mills, Director, Product Marketing · Published 22 July 2026*

![Context assembly: building the prompt the model actually sees](/images/site-mirror/f8ea8cadbffac61fc60f0158aae879d4eafbafb5-2400x1256.webp)

The prompt a production LLM receives is almost never something a person wrote. By the time a request reaches the model, your app has stitched together system instructions, retrieved documents, conversation history, tool schemas, and stored memories into one long token sequence. That stitching step is context assembly, and it can strongly influence answer quality alongside the model you picked or the exact wording of your system prompt. The discipline around it now has a name: [context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents), the practice of curating and maintaining the right set of tokens for the model during inference, including everything that lands in the window beyond the prompt itself.

Think of it as the part of your AI stack that decides what the model gets to know before it answers. This guide covers what goes into a single assembly pass, why ordering and token budgets change what the model actually uses, why stale inputs cause so many bad responses, and when it's time to stop hand-rolling the assembly layer.

## Every prompt is assembled, not written

Context engineering decides what fills the context window; prompt engineering only shapes the words inside it. In any real app, most of what reaches the model isn't hand-written text, it's stitched together on the fly for each query or each step of an agent's reasoning, from whatever sources the current request needs.

One tidy way to describe it: context = Assemble(instructions, knowledge, tools, memory, state, query). Your app runs that function on every request, whether you designed it deliberately or it grew out of string concatenation over six sprints. Retrieval-augmented generation (RAG) is the most familiar version: the app embeds the user's query, pulls the most similar chunks from a vector store, and combines those chunks with the original prompt before calling the model. The database stores and retrieves; the app orchestrates.

## Retrieval, memory, tools, & history: one assembly pass

The Assemble() function typically pulls from five kinds of input, and each competes for the same finite window:

1. **System instructions:** Set the model's behavior and capabilities. Even this "static" piece is often templated per user, context, or conversation stage.
1. **Retrieved knowledge:** RAG chunks pulled by vector search, often refined by routers that pick a retriever and postprocessors that filter and re-rank results.
1. **Conversation history:** Short-term memory for the current session, usually trimmed, deleted, or summarized when it outgrows the window.
1. **Long-term memory:** Cross-session facts and preferences, typically a persistent store with put, get, and search operations.
1. **Tool definitions:** JSON schemas describing what the model can call. Their wording steers tool-calling behavior, so they deserve the same care as the prompt itself.

The common thread: most of these inputs come from stores queried on every request, which makes store latency part of every response. That's why these per-request lookups increasingly route through one layer built for the job instead of a patchwork of separate stores. Redis Iris is that layer, running on Redis's in-memory operations at [sub-millisecond latency](/blog/redis-enterprise-extends-linear-scalability-200m-ops-sec/) so retrieval, session state, and memory reads don't eat the request budget. Short-term agent memory in particular tends to live in memory precisely because it's read at the start of every turn.

## Order changes what the model actually uses

Once you've gathered the pieces, where each one lands in the window matters more than most teams expect. Models use information at the very beginning and very end of their input far better than information in the middle, producing a U-shaped performance curve across positions. In one multi-document question-answering (QA) test, GPT-3.5-Turbo's accuracy [fell to 52.9%](https://arxiv.org/html/2307.03172v1) when the answer sat in the 10th of 20 documents placed in the prompt. That's below its 56.1% no-document score. Burying the right chunk in the middle of a long prompt can be worse than not retrieving it.

Claimed window size doesn't rescue you either. In the RULER benchmark, only [half of models](https://github.com/NVIDIA/RULER) effectively handled 32K-token sequences despite claiming 32K or more, and GPT-4's measured [effective length was 64K](https://arxiv.org/html/2404.06654v1) against its claimed 128K. The mechanics trace back to attention: models disproportionately weight the [first and final tokens](https://arxiv.org/html/2506.22058v3), largely independent of semantic relevance.

Placement has a cost dimension too. Putting stable content first and dynamic content like RAG results and history last maximizes the shared prompt prefix, which makes requests more key-value (KV) cache-friendly and cuts the input tokens processed per request. Stable stuff first, fresh stuff last: it serves both the model's attention pattern and your bill.

## Token budgets force trade-offs before generation starts

Careful ordering assumes everything fits, and in agentic systems it often doesn't. Tool definitions alone can eat a startling share of the window. One documented setup had [58 tools consuming approximately 55K](https://www.anthropic.com/engineering/advanced-tool-use) tokens before the conversation even started, with a single Jira server using roughly 17K. Every one of those tokens is budget that retrieval, memory, and history can no longer spend.

Teams manage the squeeze in a few recurring ways. On-demand tool discovery loads only the tools relevant to the current task instead of preloading everything. Compaction summarizes a conversation nearing the limit and restarts a new window with the summary. Provider prompt caching changes the economics of whatever you keep: on Anthropic's API, cache reads are billed at [10% of base input](https://docs.anthropic.com/en/docs/about-claude/pricing) price. All of these decisions happen before generation; by the time the model produces its first token, the trade-offs are locked in.

## Stale & missing inputs explain many bad responses

Even a perfectly sized budget can't save an assembly pass that pulls in the wrong data. Context breaks down in [four common failure modes](https://www.oreilly.com/radar/working-with-contexts/):

- **Context poisoning:** A hallucination or error enters the context and gets repeatedly referenced. This is the nastiest because output becomes input: a confused step conditions every step after it.
- **Context distraction:** The context grows so long the model over-focuses on it and neglects its training.
- **Context confusion:** Superfluous content steers a low-quality response.
- **Context clash:** Newly accrued information conflicts with what's already in the prompt.

A broader pattern sits underneath all four: context rot, where LLMs get less effective as context grows, even on simple tasks, with distractors doing amplified damage in longer contexts. Better retrieval alone doesn't fix it. In one long-context evaluation, even when models could perfectly retrieve all relevant information, performance still degraded [13.9%–85% as input grew](https://arxiv.org/html/2510.05381v1), including when whitespace replaced the irrelevant tokens.

Missing inputs are the mirror-image failure. Production agents often exhaust their effective context windows, forcing devs to choose between cutting transcripts and degrading performance. Either way, the assembly step already shaped the response: the model answered the prompt it was given, and the prompt was wrong.

## Hand-rolling the layer vs. building on one

These failure modes are why teams eventually stop concatenating f-strings and treat assembly as its own layer. A bigger window can't be the single scaling strategy; context needs to be handled as a first-class system with its own architecture, lifecycle, and constraints. Agent frameworks cover the orchestration half of that. LangGraph passes a state object between nodes and lets you selectively include context before each model call, LlamaIndex structures retrieval and re-ranking, and Model Context Protocol (MCP) standardizes tool connections.

The data half is a latency problem. In one benchmark, retrieval accounted for [45%–47% of time-to-first-token](https://arxiv.org/html/2412.11854v1) in RAG serving. In another analysis, a query to a remote vector store added [50–300ms network round-trip](https://arxiv.org/html/2603.02206v1) latency. That alone can consume a real-time latency budget. For latency-sensitive agent apps, an assembly layer that runs on every request works best with stores that answer in the low milliseconds or faster.

Redis Iris is built for that data half: a real-time context engine that brings together memory, retrieval, fresh operational data, and semantic caching for AI agents. Within it, Redis Agent Memory is a memory layer with configurable extraction strategies, MCP integration, and multi-provider LLM support through LiteLLM, and Redis LangCache handles the semantic caching piece. LangCache benchmarks reported cache hits with [up to 15x faster](/blog/context-window-management-llm-apps-developer-guide/) responses and [up to 73% lower](/blog/llm-token-optimization-speed-up-apps/) LLM inference costs in high-repetition workloads. On the retrieval side, a billion-vector benchmark reported [90% precision at ~200ms](/blog/searching-1-billion-vectors-with-redis-8/) median latency while retrieving the top 100 neighbors, running with 50 concurrent queries and including round-trip time. Redis Agent Memory is currently in preview.

## Assembly quality is response quality

The model's answer depends on what your assembly step hands it. What you include, where you place it, how much budget each piece gets, and how fresh it is at request time can shape the answer as much as the prompt text itself. Hand-rolled concatenation holds up fine with a handful of tools and a short history, then quietly degrades as memory, retrieval, and tool schemas pile into the same window.

Assembly runs on the hot path of every request, which is exactly where Redis is fast. Instead of running a separate vector database, cache, memory server, and session store, you get one platform for the retrieval, memory, and caching pieces of your context layer, and there's a decent chance your app team already runs it. [Try Redis free](https://redis.io/try-free/?rcplan=iris) to see how it handles your context workloads, or [talk to our team](https://redis.io/meeting/) about what your assembly layer should look like.
