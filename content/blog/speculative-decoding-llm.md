---
title: "Speculative decoding: How it works, when it helps & where it fits in your inference stack"
linkTitle: "Speculative decoding: How it works, when it helps & where it fits in your inference stack"
url: "/blog/speculative-decoding-llm/"
description: "You're running LLM inference in production. Semantic caching handles the easy wins: repeated queries with the same intent come back from cache without touching the model. But everything else still..."
date: 2026-04-22
blogCategories:
- "Tech DE"
authors:
- "Jim Allen Wallace"
lastmod: 2026-04-23
hidden: true
mirrored: true
---

*By Jim Allen Wallace, Sr. Product Marketing Manager · Published 22 April 2026 · updated 23 April 2026*

![Redis](/images/site-mirror/b5da8de73f648a3b68589ba5609c207bd7c2b15f-1200x628.webp)

You're running LLM inference in production. Semantic caching handles the easy wins: repeated queries with the same intent come back from cache without touching the model. But everything else still hits the model at full cost, and that adds up fast at scale.

Speculative decoding is one way to speed up those requests without touching the model or its outputs. This guide covers how it works, the variants gaining traction in 2026, when it helps, when it doesn't, and where it fits in a layered inference stack alongside semantic caching.

## What is speculative decoding

Speculative decoding makes LLM responses faster without changing what the model outputs. Instead of generating one token at a time, a small draft model runs ahead and proposes several tokens. The large model checks those proposals in a single pass. When they're accepted, you get multiple tokens for roughly the cost of one. The output stays identical to running the large model alone, so there's no quality tradeoff.

How much faster depends on how often the large model agrees with the draft. When the two align closely, the gains are meaningful. When they diverge, the overhead of running the draft model eats into the benefit. Early experiments on large models [measured 2–2.5× speedups](https://arxiv.org/abs/2302.01318) in distributed setups, but results vary widely depending on model pairing and workload.

## The memory-bandwidth problem with autoregressive decoding

LLMs generate text slowly not because the math is hard, but because of how much data has to move. Every token your model generates requires loading the entire set of model weights from memory (tens of gigabytes for a large model), doing a small amount of arithmetic on them, and then producing a single token. Then repeating the whole thing for the next token.

The GPU's arithmetic units finish their work fast. The bottleneck is the memory transfer: fetching all those weights takes far longer than the actual computation. So the GPU sits partially idle between tokens, waiting on memory reads rather than doing useful work.

That idle compute is the gap speculative decoding exploits. It's also why semantic caching complements it: for repeated or semantically similar queries, no token generation runs at all. The answer is returned from cache. Speculative decoding speeds up the requests that do make it to the model.

## How the draft-verify loop works

The core idea: run a cheap model ahead of the expensive one, then check its work in bulk. Here's how that plays out in practice.

A small draft model generates several candidate tokens from the current context. This is fast and inexpensive compared to running the large model. The large model then checks all those candidates in a single pass. As covered above, that check costs roughly the same as generating one token the normal way.

Each candidate either passes or fails the check. The first failure stops the loop, and the large model corrects from that point. If all candidates pass, the large model adds one more token on top. The result: between one and several tokens produced per large-model pass, depending on how well the draft and target models agree.

The output is [provably identical](https://proceedings.neurips.cc/paper_files/paper/2024/file/e7349e785900b93d8b4971a3f2c1cefe-Paper-Conference.pdf) to what the large model would have generated on its own. Speculative decoding is a latency optimization, not an approximation.

## Variants gaining traction in 2026

The base algorithm has spawned a range of variants, each solving a different limitation: draft model overhead, memory footprint, workload structure, or hardware constraints. Here are the ones showing up in recent research and production frameworks.

### EAGLE-3: higher acceptance rates

EAGLE-3 is a speculative decoding method that improves how well the draft model predicts what the large model will output. Better predictions mean more draft tokens get accepted, and more accepted tokens means more output per large-model pass. The EAGLE family achieves this by attaching a lightweight head directly to the target model rather than training a separate model from scratch. EAGLE-3 advances on earlier versions by predicting tokens directly (rather than intermediate model features) and drawing on representations from multiple layers of the target model rather than just the top one. Across tested configurations, EAGLE-3 [reported 3.0–6.5× speedups](https://arxiv.org/pdf/2505.19634) over standard generation, with a 20–40% improvement over EAGLE-2. A newer extension, P-EAGLE, pushes further by generating all draft tokens in a single pass, [reporting 1.10–1.36×](https://arxiv.org/abs/2602.01469) additional gains over EAGLE-3 in large-scale model benchmarks.

### SuffixDecoding: training-free for agentic workloads

SuffixDecoding is useful when your workload produces repetitive, structured outputs — multi-step SQL generation, tool-calling loops, or code pipelines where the same patterns appear across requests. Instead of training a draft model, it builds draft candidates by matching the current generation against a history of past outputs. It maintains two pools of that history: one for the current request, and a shared pool across all prior requests. The shared pool drives most of the speedup, because cross-request repetition is where the gains are. No model training required means it can be layered onto an existing inference stack. [SuffixDecoding reported a mean 5.3× speedup](https://openreview.net/forum?id=uwL0vbeEVn) on AgenticSQL benchmarks.

### LayerSkip: smaller memory footprint

LayerSkip reduces memory overhead by using the target model itself as the draft. Instead of loading a separate model, it exits the target model's layers early to produce draft tokens, then runs the remaining layers to verify. The tradeoff: this only works with models specifically trained for it. You can't apply LayerSkip to an off-the-shelf model. It requires a model built or fine-tuned with the LayerSkip training recipe. For teams who can commit to that, [benchmarks reported up to 2.16×](https://arxiv.org/html/2404.16710v4) with pretraining-based configurations on H100 GPUs.

### Saguaro: overlapping draft & verify

Saguaro speeds things up by running drafting and verification at the same time rather than in sequence. While the large model is verifying one set of candidates, the draft model is already generating the next. The result: [benchmarks reported](https://openreview.net/forum?id=aL1Wnml9Ef) an average 30% improvement over optimized speculative decoding baselines, and up to 5× over standard autoregressive decoding. The tradeoff is hardware: achieving that overlap means running the draft model on separate GPUs from the target model, which adds to infrastructure cost.

### Reasoning-specific methods

Standard speculative decoding generates draft tokens one at a time, which hits a ceiling for reasoning models that produce thousands of chain-of-thought tokens. Methods like SpecReason and Lookahead Reasoning address this by drafting entire reasoning steps rather than individual tokens, then verifying them for semantic correctness rather than exact token match. [One benchmark reported up to 2.1×](https://openreview.net/forum?id=JxxKj8pow1) when combined with n-gram speculative decoding on open-source reasoning models.

## When speculative decoding helps & when it doesn't

Each of those variants targets a different constraint, but knowing which one fits your architecture is only half the equation. Batch size, workload shape, and hardware profile all determine whether speculative decoding helps or hurts. Understanding those variables is the difference between a meaningful latency reduction and wasted engineering effort.

### Batch size is the biggest variable

At low batch sizes, speculative decoding delivers real speedups. At high batch sizes with short-to-medium context lengths, it can slow things down. Verification overhead outpaces the gains. Long-context serving is a meaningful exception: when batch size is large and sequences are long, the KV cache itself becomes the memory bottleneck, which [can restore the conditions](https://arxiv.org/abs/2408.11049) where speculative decoding helps. This is the most important production consideration that benchmark headlines tend to obscure.

In one benchmark on Qwen3-8B, [speedup degraded](https://arxiv.org/html/2601.19278v1) from 1.93× to 0.99× as batch size grew from 2 to 48.

Adaptive speculation addresses this by dynamically choosing the draft length γ based on current batch size. Adaptive approaches measured an [average 1.94×](https://arxiv.org/pdf/2310.18813) across all batch sizes in one study, where fixed-length speculation performed worse and gains diminished at batch size 32+.

### High-gain workloads

Agentic, reasoning, and code generation workloads tend to show the largest gains. The common thread is repetitive, structured, multi-step output patterns: exactly the kind of sequences where a draft model can predict what comes next with high acceptance rates.

### Where gains diminish

High-concurrency batch serving, highly stochastic sampling (high temperature, top-k with wide distributions), and scenarios without a well-matched draft model all reduce the benefits. Those conditions lower acceptance rates or make verification overhead harder to amortize across tokens.

### Hardware matters too

The memory-bandwidth gap that speculative decoding exploits varies by GPU. In one comparison using Mamba 2.8B with a 130M draft model, an RTX 3090 measured [1.5× speedup](https://arxiv.org/html/2408.15237v4) while an H100 showed no speedup under the same configuration. Higher-bandwidth GPUs leave less idle compute for speculative decoding to reclaim.

The practical takeaway: benchmark with your actual model, batch shape, hardware, and sampling settings before committing to speculative decoding in production.

## Where speculative decoding fits in the optimization stack

Once you've validated that speculative decoding fits your workload, the next question is where it sits in your serving stack. Production inference systems combine multiple optimizations, and the interactions between layers typically matter more than any single technique.

Here's how the layers typically stack up:

- Semantic caching eliminates inference calls entirely for repeated or semantically similar queries by returning a previously cached response. When a cache hit occurs, the request never reaches the model.
- Prefix and key-value (KV) cache reuse reduces redundant prefill computation across requests that share context like system prompts or few-shot examples.
- Speculative decoding reduces per-token latency for individual requests that proceed to full inference.
- Continuous batching maximizes GPU utilization across concurrent requests.
- Prefill-decode disaggregation optimizes hardware allocation by routing the compute-heavy prefill and memory-heavy decode phases to separate hardware pools.

These layers aren't all additive. Speculative decoding and continuous batching can be in tension: as covered earlier, speculative decoding's speedup typically decreases as batch size grows, though the effect depends on workload and system conditions. Speculative decoding can also conflict with [prefill-decode disaggregation](https://arxiv.org/html/2510.22876v1) in some serving architectures, since the decode phase is where speculative decoding operates.

Semantic caching and speculative decoding, by contrast, are naturally complementary. A cache hit makes speculative decoding irrelevant for that request. A cache miss routes to the inference stack where speculative decoding reduces latency for the full generation. The two techniques cover different parts of the request distribution without interfering with each other.

Redis handles both the vector search and semantic caching layers for AI workloads. [Redis LangCache](/blog/langcache-public-preview/), currently in public preview, is a fully managed semantic caching service that handles embedding generation, similarity matching, and cached response retrieval through a Representational State Transfer (REST) API. No separate vector database or custom pipeline required.

## Speculative decoding is a latency tool, not a silver bullet

Used with the right workload, speculative decoding meaningfully reduces per-request latency without changing model outputs. The benchmarks are real — the key is matching the technique to your batch size, context length, and draft model before committing.

The larger gains come from combining it with other techniques. Semantic caching eliminates inference calls for repeated queries. Speculative decoding speeds up what's left. Redis supports both as a single data layer for semantic caching and vector search, rather than separate infrastructure for each.

[Try Redis free](https://redis.io/try-free/) to see how semantic caching works with your inference pipeline, or [talk to the team](https://redis.io/meeting/) about optimizing your AI infrastructure.
