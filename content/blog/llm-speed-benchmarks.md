---
title: "LLM speed benchmarks: metrics & infrastructure guide"
linkTitle: "LLM speed benchmarks: metrics & infrastructure guide"
url: "/blog/llm-speed-benchmarks/"
description: "Your LLM-powered feature crushes it in staging. Then you ship it, and users sit watching a loading spinner for 30 seconds while the model thinks. Speed benchmarks exist to help you predict and..."
date: 2026-05-10
blogCategories:
- "Tech DE"
authors:
- "Jim Allen Wallace"
lastmod: 2026-05-13
hidden: true
mirrored: true
---

*By Jim Allen Wallace, Sr. Product Marketing Manager · Published 10 May 2026 · updated 13 May 2026*

![LLM speed benchmarks: the metrics, models & infrastructure that matter for production AI](/images/site-mirror/1a1c89b8b9846e20d733bfb5e024b3cbd6fa8edd-2400x1256.webp)

Your LLM-powered feature crushes it in staging. Then you ship it, and users sit watching a loading spinner for 30 seconds while the model thinks. Speed benchmarks exist to help you predict and prevent that experience before it hits production.

But LLM speed isn't a single number. The auto-regressive, token-by-token generation process creates distinct performance phases, each with different bottlenecks and different implications for your users. Picking the wrong model for your use case because you optimized for the wrong metric is an expensive mistake.

This guide covers the core metrics for LLM inference benchmarking, what actually drives inference speed in production, and how [semantic caching](/blog/prompt-caching-vs-semantic-caching/) can bypass the inference bottleneck entirely.

## The six metrics that actually matter

LLM speed breaks down into six metrics that map to different parts of the inference pipeline and different user experiences. Traditional request latency and throughput aren't enough because generation happens in two computational phases: prefill, which processes the input prompt, and decode, which generates tokens one at a time. Each phase has its own performance characteristics, and picking the right metric depends on which phase your users actually feel.

### Time to first token (TTFT)

TTFT is the elapsed time from sending a request to receiving the first token back, and it's often the primary responsiveness indicator for chatbots and interactive apps. It captures the prefill stage, where the model processes your entire input prompt before generation begins. In standard auto-regressive LLM inference, token generation begins after the prefill phase has processed the input context. Some serving systems also use chunked prefill, but TTFT still primarily reflects prompt processing before visible output.

Reasoning and extended thinking modes change what TTFT actually measures. In those deployments, time to first answer token (TTFAT) is often the operationally relevant metric because it includes both input processing and internal reasoning time before visible answer tokens appear. Benchmark platforms may still label this latency as TTFT, so be careful not to compare reasoning and non-reasoning modes as if they represent the same thing.

### Output speed (tokens per second)

Output speed is the average number of tokens received per second after the first token arrives, and it's often the leading metric for workflows where users read along as content streams in. It captures the decode stage: the sustained generation rate your users see once text starts flowing. Code generation, document summarization, and any streaming UX tend to live or die on this number.

### Inter-token latency (ITL)

ITL is the average time between consecutive output tokens, and it often matters more than average output speed when responses stream to users. Most benchmark tools also call this time per output token (TPOT), with ITL more often used to describe the per-token distribution and TPOT used for the mean. Variable ITL can cause perceptible stuttering even when aggregate tokens per second looks acceptable. If your app streams responses, smooth pacing typically drives perceived quality more than raw throughput.

### End-to-end latency

End-to-end latency is the total wall-clock time from request submission to final token, and it's typically the metric that matters most for non-streaming, synchronous apps. It breaks down as TTFT plus mean ITL multiplied by the number of output tokens. Batch API calls and document processing pipelines don't benefit from streaming, so the full completion time is what your users actually wait on.

### System throughput & requests per second

System throughput is the total output tokens generated per second across all concurrent requests, and it's often one of the primary metrics for infrastructure capacity planning. It's distinct from per-request output speed because it aggregates across the whole serving system. Requests per second (RPS) tracks complete inference requests processed per second. TTFT and ITL are key latency metrics for interactive retrieval-augmented generation (RAG) and agentic systems workloads, while throughput metrics such as RPS are more often emphasized for batch or high-throughput serving scenarios.

Matching metrics to use cases saves you from optimizing for the wrong thing. Interactive chat cares about TTFT. Batch processing cares about end-to-end latency. Multi-tenant API serving cares about system throughput. [Agentic systems infrastructure](https://redis.io/guides/ai-agents-infrastructure/) often cares about TTFAT and end-to-end latency across chained calls.

## How benchmark tradeoffs show up

Agentic and reasoning workloads complicate that mapping further. Even when throughput improves, user-perceived speed can still get worse because those systems generate far more tokens and chain multiple model calls together, so raw tokens-per-second gains don't automatically translate into faster end-user experiences.

Don't trust a single leaderboard. Compare the metric that matches your app, and benchmark your actual deployment path before making latency or service-level commitments.

## What actually drives inference speed

Inference speed comes down to three interacting layers: hardware, software optimizations, and model architecture. Each gives you different levers, and understanding which one is limiting your workload is more useful than chasing a faster GPU by default.

### Hardware: memory bandwidth is often a major bottleneck

The decode phase is typically memory-bandwidth-bound, not compute-bound. Moving model weights and key-value (KV) cache data through memory often matters as much as raw compute, which means hardware selection is less about peak throughput per chip and more about how fast the system can keep data flowing during generation.

### Software: where the big multipliers live

Software optimizations often produce the biggest measured speedups in published benchmarks, sometimes more than a hardware upgrade. Three techniques show up repeatedly:

- **Quantization** reduces numerical precision to shrink memory footprint and improve bandwidth utilization. FP8 (8-bit floating-point) shows up increasingly in modern serving stacks, while more aggressive quantization can reduce memory use further with quality tradeoffs on harder tasks.
- **Continuous batching with PagedAttention** manages the KV cache in non-contiguous memory pages, similar to OS virtual memory. Public benchmarks report large throughput improvements and reduced p50 latency with this approach.
- **Speculative decoding** uses a lightweight draft model to propose multiple candidate tokens verified by the target model in a single pass. Production deployments have reported throughput gains, though the extra inference work can create tradeoffs under high concurrency.

Teams often combine these techniques, and the gains depend on workload, concurrency, and infrastructure. The real lesson is that serving software can change the shape of your latency profile as much as model choice.

### Model architecture: Mixture of Experts (MoE)

Architecture choices shift the balance between raw capability and serving efficiency, and Mixture of Experts (MoE) is the pattern showing up in many recent frontier models ([MoE production](https://arxiv.org/html/2503.04398v5)). Each token activates only a subset of expert layers, which can reduce effective compute per forward pass ([37B active params](https://arxiv.org/html/2601.14053v2)). The tradeoff: MoE deployments add memory-management complexity even as per-token compute drops. Faster inference can come from better GPUs or smarter batching, but sometimes it's baked into how the model routes work internally.

## Semantic caching: skip the inference entirely

The fastest inference call is the one you don't make. Semantic caching avoids the LLM call when you've already answered a similar question by converting incoming prompts into vector embeddings and returning cached responses when cosine similarity exceeds a threshold. Unlike exact-match caching, it recognizes that ["What is semantic caching?"](/blog/prompt-caching-vs-semantic-caching/) and "How does semantic caching work?" mean the same thing.

Published benchmarks show why teams use this approach. On a customer-service Q&A benchmark, one semantic caching system reported [68.8% API reduction](https://arxiv.org/html/2411.05276v3) with a positive hit rate above 97%, and agentic plan caching observed a [27% latency reduction](https://neurips.cc/virtual/2025/poster/116166) across multiple real-world agent apps. Web-search-style traffic shows approximately [33% semantic repeats](https://arxiv.org/html/2504.02268v1), a useful baseline before workload-specific tuning.

There's a real accuracy tradeoff to manage, though. Static cosine similarity thresholds don't provide formal correctness guarantees, which is why some caching systems treat user-defined error rate bounds as a formal constraint. Across different test configurations, one verified cache reported up to [12.5x higher hits](https://openreview.net/forum?id=zF0A0xw3HZ) than static-threshold baselines and up to 26x lower error rates.

Redis fits this picture as a real-time data platform with sub-millisecond latency, and Redis LangCache uses semantic similarity search so prompts with the same meaning map to the same cache entry without a new LLM call. In benchmarks, LangCache reported up to [15x faster responses](/blog/context-window-management-llm-apps-developer-guide/) for cache hits and up to [73% lower](/blog/llm-token-optimization-speed-up-apps/) LLM inference costs without code changes. Teams already using Redis for operational data and [vector search](https://redis.io/resources/redis-query-engine/) often don't need a separate system to add semantic caching.

## LLM inference speed is a systems decision

Getting LLM speed right depends on matching metrics to your use case, understanding the hardware and software factors you can control, and recognizing when avoiding the call matters more than shaving milliseconds off decode time.

For workloads with semantic repetition, semantic caching cuts both latency and cost without changing the model itself. That lever often outweighs marginal inference gains for high-volume chat and agentic traffic.

Redis provides the retrieval, semantic caching, and operational data layers that RAG and agentic apps depend on in a single platform, while the app handles pipeline orchestration. If you're building production [GenAI apps](https://redis.io/redis-for-ai/) and spending too much on inference or waiting too long for responses, [try Redis free](https://redis.io/try-free/) to test semantic caching and vector search with your own workload, or [talk to our team](https://redis.io/meeting/) about optimizing your AI infrastructure stack.
