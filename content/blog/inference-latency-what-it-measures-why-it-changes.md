---
title: "Inference latency: what it measures & why it varies"
linkTitle: "Inference latency: what it measures & why it varies"
url: "/blog/inference-latency-what-it-measures-why-it-changes/"
description: "Ask an engineer what their LLM app's inference latency is, and the honest answer is \"which one?\" The time to the first visible token, the time to the finished response, and the time an agent spends..."
date: 2026-08-06
blogCategories:
- "Tech DE"
authors:
- "Jeff Mills"
lastmod: 2026-08-12
hidden: true
mirrored: true
---

*By Jeff Mills, Director, Product Marketing · Published 6 August 2026 · updated 12 August 2026*

![Inference latency: what it measures & why the answer changes](/images/site-mirror/24a4a3580bf21e34e752e9d405df79b71e16bb77-2400x1256.webp)

Ask an engineer what their LLM app's inference latency is, and the honest answer is "which one?" The time to the first visible token, the time to the finished response, and the time an agent spends across a chain of calls are three different numbers. They can even disagree about which system is faster. This guide covers what inference latency measures, why it splits into several metrics, where the time actually goes in production pipelines, and when avoiding a model call can be faster.

## What is inference latency?

Inference latency is really just how long you wait between firing off a request and getting the output back. It's a different question from throughput, the number benchmarks usually quote: throughput is how many tokens or requests a system handles per second across everyone using it, while latency is how long your one request waits. The two can pull in opposite directions: push more requests through at once and throughput goes up, but each one waits longer [in a queue](https://redis.io/glossary/redis-queue/) for its share of GPU time. A "tokens per second" figure tells you almost nothing about what a single user feels.

For a traditional machine learning (ML) model that returns a single prediction, latency is one clean number. But an LLM writes its answer one token at a time, so it splits into several that move independently:

- **First-token time (TTFT):** how long until the first token or visible text appears.
- **Per-token time (TPOT):** how long each following token takes to stream.
- **Total response time (end-to-end latency):** how long until the full response finishes.
- **Agent run time:** the total time a multi-step agent takes across its chained calls.

Under the hood, the model works in two phases: it reads your whole prompt in one pass (prefill) to produce the first token, then streams the rest one at a time (decode). That's why the same request can give you very different numbers: the first token might land in under 200 ms while the full response takes more than a second to finish, and no single figure captures both.

Averages hide things too. A model can look quick on average while its [99th percentile](https://docs.nvidia.com/aiperf/getting-started/ai-perf-comprehensive-llm-benchmarking) runs more than twice as slow, and those slow requests are the ones users actually notice. That's why teams watch the [worst case](https://sre.google/sre-book/service-level-objectives), not just the mean.

## What affects inference latency?

Whichever metric you pick, the model itself is only one contributor to it.

### Queuing, guardrails & cold starts

When a provider benchmarks a model, they measure the model's own generation time. What your users wait on is that plus everything wrapped around the call. A request often sits in a queue behind other users before it even starts. Guardrails, the safety filters that screen inputs and outputs, run before or after generation and add their own delay. And on serverless infrastructure, if the model isn't already loaded, the first request has to wait for its weights to load into GPU memory, a cold start that can add [tens of seconds](https://arxiv.org/html/2502.15524v1). None of these show up in a model-only benchmark, which is why a model's advertised speed can look nothing like what you measure in production.

### How retrieval adds latency in RAG

[Retrieval-augmented generation (RAG)](https://university.redis.io/course/ihjs7iip0gpkrw) is a pattern where the app pulls relevant context from your own data before calling the model. That means a whole pipeline runs before generation: embed the query, search a vector index, maybe rerank candidates, then assemble the context into the prompt. All of that happens before the model produces a single token. In a tested RAG serving pipeline, retrieval accounted for [41% of end-to-end latency](https://arxiv.org/html/2412.11854v1), and the retrieved documents lengthened the prompt enough to push TTFT higher on top of that.

This is where your data layer earns its keep. [Redis Iris](https://redis.io/docs/latest/develop/ai/context-engine/) is Redis' real-time context engine for AI agents, built on an in-memory store, so many of its cache and state operations run at [sub-millisecond latency](https://university.redis.io/learningpath/hbykf3qrnhwccy), depending on the command and workload. Its retrieval layer, Redis Search, serves the [vector search](https://university.redis.io/course/1npvvtfft2agew) a RAG pipeline needs, alongside session state and feature lookups from the same store, so the layers around the model don't turn into their own latency problem.

## Which latency metric matters for your workload?

Once you know where the time goes, the question becomes which number to improve, and that depends on who, or what, is waiting.

### Chat & streaming latency

For a person reading a streamed reply, TTFT is what they feel: the difference between a response that feels instant and one that feels sluggish. A classic usability model puts the threshold for "instantaneous" at around [0.1 seconds](https://www.nngroup.com/articles/response-times-3-important-limits), with responses under a second keeping the user in their flow of thought. That's why chat optimizes for TTFT, with analyses of interactive workloads suggesting [500 ms–2 second](https://arxiv.org/html/2606.20577v1) targets, tighter for voice or code completion where the user waits on every keystroke. Once tokens stream faster than someone reads, extra decode speed doesn't buy you much.

### Agent & batch job latency

Agents flip that priority. An agent isn't reading tokens as they stream, so a fast first token does little for it; it can only act once a step's output is complete. Each step in a sequential workflow waits on the one before, so latency compounds, with queue waits, network time, tool execution, and retrieval all adding to the total. The metric that matters is trace-level latency, the time across the whole trajectory rather than any single call, and queueing hurts most of all: an agent submits a new request at every step, so every bit of delay stacks up [across the run](https://arxiv.org/html/2603.28101v1).

Batch jobs care about something different again. If you're classifying a million documents overnight, nobody's watching a cursor. What matters is finishing inside the window at a reasonable cost per token. Providers price this trade explicitly: batch APIs typically offer around [50% lower costs](https://platform.openai.com/docs/guides/batch) in exchange for slower, asynchronous turnaround, which makes them a good fit for offline work but not for anything interactive.

## How semantic caching reduces latency

After choosing the right workload metric, consider whether you can avoid some calls entirely. When a safe cache hit is available, skipping the inference call reduces latency more than any amount of tuning the model itself.

Semantic caching is the pattern that makes this possible. It stores model responses keyed by the [vector embedding](https://university.redis.io/course/i3fv2hbhqnpni8) of the query, a numerical representation of the query's meaning. When a new query comes in, the cache compares its embedding to the stored ones, and if they're similar enough, it returns the cached response without calling the model at all. No prefill, no decode, no output tokens billed. This matters because a lot of real traffic repeats itself: one evaluation dataset classified [31% of ChatGPT queries](https://arxiv.org/html/2507.07061v1) as semantically similar to earlier ones.

This is the other place Redis Iris shows up in latency work. Redis LangCache, its managed semantic caching service, reported responses [up to 15x faster](/blog/context-window-management-llm-apps-developer-guide/) for cache hits in benchmarks. In high-repetition workloads, it also reported [up to 73% lower](/blog/llm-token-optimization-speed-up-apps/) LLM inference costs.

Semantic caching isn't free of trade-offs. If the similarity threshold is too loose, the cache can return a response that doesn't quite match what the user asked, and cached answers can [go stale](https://redis.io/glossary/cache-invalidation/) as the underlying facts change. Teams typically manage this with conservative thresholds and expiry on time-sensitive entries.

## How to reduce inference latency

Whether you speed up a model call or skip it with a safe cache hit, the right approach depends on who's waiting. Chat apps often prioritize time to first token, agents prioritize total workflow time, and batch jobs prioritize the deadline and the bill. And because the model shares the clock with retrieval, queues, guardrails, and cold starts, some of the biggest wins come from the layers around the model, or from skipping the call entirely. Redis Iris brings several of those surrounding layers into one in-memory context engine: Redis Search for retrieval, Redis LangCache for semantic caching, and Redis Agent Memory for persistent state, all of which preserve more of your latency budget. [Try Redis Iris](https://redis.io/try-free/?rcplan=iris) to benchmark it against your own workload, or [talk to our team](https://redis.io/meeting/) about where your latency budget is going.
