---
title: "Prefill vs Decode: LLM Inference Phases Explained"
linkTitle: "Prefill vs Decode: LLM Inference Phases Explained"
url: "/blog/prefill-vs-decode/"
description: "Every LLM request runs in two distinct phases: prefill, where the model reads your prompt in one parallel burst, and decode, where it generates the response one token at a time, each one depending..."
date: 2026-04-28
blogCategories:
- "Tech DE"
authors:
- "Jim Allen Wallace"
lastmod: 2026-04-29
hidden: true
---

*By Jim Allen Wallace, Sr. Product Marketing Manager · Published 28 April 2026 · updated 29 April 2026*

![Prefill vs decode: The two phases shaping your LLM app's speed](/images/blog/75bfcc6f0e694bc947af33b701199bde48b5315b-2400x1256.webp)

Every LLM request runs in two distinct phases: prefill, where the model reads your prompt in one parallel burst, and decode, where it generates the response one token at a time, each one depending on the last. These two phases have different performance characteristics, hit different hardware bottlenecks, and need different optimization strategies.

If your chatbot feels sluggish before the first word appears, that's usually a prefill problem. If it crawls once tokens start coming, that's decode. This guide covers what prefill and decode mean, how they affect time to first token (TTFT) and inter-token latency (ITL), and which optimization levers matter for each phase.

## What "prefill vs decode" actually means for your LLM app

Prefill and decode stress different parts of the GPU, which is why a single optimization rarely improves both:

- **Prefill** processes your entire input prompt at once, including system instructions, retrieved context, and the user message. It builds the internal state, called the [key-value (KV) cache](https://arxiv.org/html/2512.22066v1), that the model needs for generation.
- **Decode** generates the response one token at a time. Using the cached state from prefill, it produces a token, feeds it back in, and repeats until the response is complete.

Specifically, prefill is usually compute-bound, meaning it's limited by how fast the GPU can do math. Decode is usually memory-bandwidth-bound, meaning it's limited by how fast the GPU can move data around. That difference shapes serving decisions like request scheduling and hardware allocation.

## Prefill: prompt processing that drives time to first token

Take prefill first. The model reads your entire prompt in one shot, processing every token in parallel. That parallel nature means prefill can fully use the GPU's compute power, but the total work still scales with prompt length. That's what makes it compute-bound.

### Why longer prompts mean longer waits

Attention is the catch. Every token in your prompt has to interact with every other token, so the work grows faster than the prompt itself. Doubling a long prompt from 16K to 32K tokens roughly quadruples the attention work. All that parallel math is what makes prefill compute-bound: the more tokens, the more the GPU has to crunch through.

One [Llama 3.1 70B benchmark](https://developer.nvidia.com/blog/low-latency-inference-chapter-2-blackwell-is-coming-nvidia-gh200-nvl32-with-nvlink-switch-gives-signs-of-big-leap-in-time-to-first-token-performance) shows the pattern. TTFT rose with prompt length and scaled more than linearly at the longest contexts tested:

- **32,768 input tokens:** 472 ms TTFT
- **122,880 input tokens:** ~2.2 seconds TTFT

TTFT grew faster than the prompt itself, and that gap widens as contexts get longer.

### How users experience prefill speed

From a user's perspective, prefill is the wait between sending a request and seeing the first token. That wait is what TTFT measures. In a streaming chat interface, it's the blank-screen pause before any text appears.

Prefill has to finish before the model can emit anything, so [TTFT mostly reflects](https://arxiv.org/html/2412.06198v1) prefill runtime plus queuing and network overhead. For short prompts, that's usually near-instant. But for retrieval-augmented generation (RAG) workflows that prepend thousands of context tokens, or long-context chats that include the full conversation history, users can wait multiple seconds before the response starts.

## Decode: token-by-token generation that users feel

After prefill, decode takes over with a slower kind of work. Each token has to be generated one at a time, with each one depending on the ones before it. That sequential nature means decode can't use parallel hardware the way prefill can, and it spends a lot of time moving data around. That's what makes it memory-bandwidth-bound.

### The KV cache keeps growing

Every decode step depends on every prior token, so the model has to remember the full context. That memory is the KV cache. It starts at the size of your prompt and grows by one entry per generated token. At scale, with long responses across many concurrent requests, the cache can balloon to several times the size of the model itself. Every decode step has to read all of that, which is a big reason decode is memory-bandwidth-bound.

### How users experience decode speed

From a user's perspective, decode is what they see as the response streams in. The time between each token is what ITL measures. In a streaming chat interface, low ITL feels like smooth typing while high ITL feels like pauses between words.

Decode also dominates total response time. A 500-token response with 80 ms ITL spends about 40 seconds in decode alone. TTFT might add another 200 ms, but that's negligible next to the decode total. The longer the output, the more decode drives the experience.

## Prefill vs decode tradeoffs: how they shape speed & cost

Because both phases compete for the same GPU, optimizing for one can degrade the other. Prefill requests can block decode streams and cause visible stuttering for users already receiving tokens. Long prefill workloads can also delay incoming requests and inflate TTFT.

That's why scheduling matters. An early policy in one inference framework prioritized prefills to improve TTFT but starved decode and slowed ITL.

### Different workloads, different pain points

Which phase hurts more depends on your workload's [input-to-output ratio](https://developer.nvidia.com/blog/llm-benchmarking-fundamental-concepts/), the quickest signal for where latency will show up:

- **RAG apps** tend to be prefill-heavy. You're processing thousands of retrieved context tokens but generating relatively short answers. TTFT is usually the pain point.
- **Code generation & long-form writing** tend to be decode-heavy. Short prompts, long outputs. ITL and total generation time matter more.
- **Chatbots & interactive apps** need both phases performing well, with tail latency especially important for responsiveness.
- **Batch processing** cares less about latency and more about throughput and cost per token.

That pattern gives you a practical way to map user complaints to the phase that's probably slow. One optimization strategy rarely helps every LLM workload equally.

## Finding your bottleneck: prefill-bound or decode-bound

That makes diagnosis the next step. Figure out which phase is actually slow before you optimize. The wrong fix wastes engineering time and can make the other phase worse. Three signals will get you most of the way to a diagnosis: sequence length distribution, TTFT, and ITL.

### Start with your sequence length distribution

Your request length distribution is the fastest signal for which phase matters more. Long inputs with short-to-moderate outputs suggest a prefill bottleneck. Short inputs with long outputs point to decode. If both are long, both phases are likely stressed. Batch size, model architecture, and semantic features shift the picture too, but input/output length is where to start.

### TTFT and ITL tell different stories

TTFT and ITL each diagnose a different phase, and you need both. TTFT is the best proxy for prefill latency, though it also includes queuing and network overhead. If TTFT is high and scales with input length, prefill is likely the constraint. ITL is the decode diagnostic, calculated as end-to-end latency minus TTFT, divided by output tokens minus one. End-to-end latency alone hides which phase is slow.

### Match the fix to the bottleneck

Once you know which phase is slow, the kind of fix follows:

- **If prefill-bound:** Look at fixes that make prompt processing cheaper or skip it altogether. Efficient attention algorithms and semantic caching are the main ones.
- **If decode-bound:** Look at fixes that reduce the data the model has to move on every step. Quantization (smaller numeric formats), speculative decoding (multiple tokens per pass), and larger batch sizes are common.

This won't diagnose every workload, but it's a strong first pass before deeper profiling.

## Optimization levers for prefill

If diagnosis points to prefill, you have two options: make prompt processing cheaper, or avoid it entirely. Efficient attention kernels fall in the first camp. Semantic caching falls in the second.

### Efficient attention and FlashAttention

A class of optimizations called efficient attention (FlashAttention is the best-known) reorganizes how the model processes long prompts to make prefill faster. The model produces the same output, just faster. Many modern inference frameworks ship FlashAttention by default, so you may already have it.

### Semantic caching: bypassing inference entirely

Semantic caching operates at the app layer, above the inference pipeline. It caches complete LLM responses and reuses them when a new query is [semantically equivalent](https://arxiv.org/html/2507.07061v1) to a previous one, regardless of exact wording. On a cache hit, the query never reaches the model.

Under the hood, semantic caching is a vector search problem. Incoming queries are embedded as vectors, compared against cached query vectors using a similarity metric, and served from cache when the similarity exceeds a configured threshold. Redis combines vector search with sub-millisecond reads in one real-time data platform, which is exactly what semantic caching needs. Redis LangCache, [currently in public preview](https://redis.io/docs/latest/operate/rc/langcache/), is a managed semantic caching service built on Redis.

Semantic caching is often confused with prefix caching, but the distinction is simpler than it sounds: semantic caching can bypass inference entirely on a cache hit, while prompt-prefix reuse only reduces repeated prompt-processing work. They're complementary techniques, not substitutes. That makes semantic caching one of the few optimizations that can erase prefill work instead of merely shrinking it.

## Optimization levers for decode

Decode optimizations work differently. They live inside the model-serving stack, not the data layer. The goal is to move less data per step or get more work out of each memory load.

### Speculative decoding

Speculative decoding uses a small, fast [draft model](https://arxiv.org/html/2506.20675v1) to guess what tokens the main model would produce, then has the main model verify them in parallel. When the guesses are right, you get multiple tokens for the cost of a single decode step. One benchmark on Llama 3.3 70B [reported a 3.55× speedup](https://developer.nvidia.com/blog/boost-llama-3-3-70b-inference-throughput-3x-with-nvidia-tensorrt-llm-speculative-decoding/). The catch: the draft model's own latency becomes the new bottleneck, so it has to be fast first and accurate second.

### Quantization

Quantization shrinks the numeric representation of the model's data, using fewer bits per number to store roughly the same information. Less data means less to move on every decode step. Different formats trade off accuracy and speed differently:

- 4-bit KV cache quantization (INT4) reported a [57% decode latency reduction](https://arxiv.org/abs/2405.14256) on LLaMA3-8B in one benchmark.
- 8-bit weights and activations (W8A8) reported gains of 20–30% on prefill and 40–60% on decode [in another](https://arxiv.org/html/2405.06001v1). 4-bit weights with 16-bit activations (W4A16) gave more variable results.

The common thread across decode levers is simple: make each generation step ask less of memory. These optimizations pair well with app-layer techniques like semantic caching, which avoids the decode step entirely on a cache hit.

## Prefill and decode need different fixes

If you don't know which phase is slow, you're probably tuning the wrong thing. Long waits before the first token point to prefill, while slow streaming after that points to decode. Most LLM apps need to watch both TTFT and ITL, because they shape UX in different ways. The optimization families for each phase rarely overlap.

Redis is a real-time data platform for low-latency AI infrastructure. By combining vector search with semantic caching, it can bypass inference entirely on cache hits, eliminating both prefill and decode costs.

[Try Redis free](https://redis.io/try-free/) to see how semantic caching and vector search perform with your workload, or [talk to our team](https://redis.io/meeting/) about optimizing your [AI infrastructure](https://redis.io/guides/ai-agents-infrastructure/).
