---
title: "Get faster LLM inference and cheaper responses with LMCache and Redis"
linkTitle: "Get faster LLM inference and cheaper responses with LMCache and Redis"
url: "/blog/get-faster-llm-inference-and-cheaper-responses-with-lmcache-and-redis/"
description: "As GenAI applications evolve—think agents, copilots, and chatbots—developers need more than just a connection to an LLM. These applications demand fast, cost-efficient inference. By default, LLMs..."
date: 2025-07-28
blogCategories:
- "Tech"
authors:
- "Rini Vasan"
- "Yihua Cheng"
lastmod: 2026-06-01
hidden: true
mirrored: true
---

*By Rini Vasan, Yihua Cheng · Published 28 July 2025 · updated 1 June 2026*

![Get faster LLM inference and cheaper responses with LMCache and Redis](/images/site-mirror/ca17416e45af42b7716d2192ba2681536970f78e-772x552.webp)

As GenAI applications evolve—think agents, copilots, and chatbots—developers need more than just a connection to an LLM. These applications demand fast, cost-efficient inference. By default, LLMs repeatedly recompute the same outputs for common inputs, wasting tokens and increasing latency.

That’s where LMCache and Redis come in. LMCache reduces redundant computation by caching and reusing key-value (KV) pairs for repeated token chunks. Redis provides the real-time infrastructure to store and retrieve those chunks at scale. Together, they enable faster inference at large context sizes by allowing models to skip recomputation for overlapping content. This improves latency and makes more efficient use of compute, especially in multi-turn chat or long-form generation.

Let’s explore how LMCache works, why Redis is the ideal backend, and how you can use both to scale smarter AI pipelines.

## What is a KV cache?

A KV cache, or Key-Value cache, is a memory management technique used in large language models (LLMs), to improve inference speed. It works by storing previously computed key and value tensors (the "K" and "V" in KV) from self-attention layers, allowing the model to reuse this information for subsequent computations rather than recalculating it from scratch. This significantly speeds up the inference process, especially when generating text token by token. You can read more details [here](https://huggingface.co/blog/not-lain/kv-caching).

## What is LMCache?

[LMCache](https://github.com/LMCache/LMCache) is an open source library that accelerates LLM serving by reusing KV caches for repeated token sequences. Instead of caching full prompts or responses, LMCache operates at the chunk level—identifying commonly repeated text spans across retrieval systems, documents, or conversations, and storing their precomputed KV cache.

This is especially valuable in Retrieval-Augmented Generation (RAG), multi-turn chat, or summarization tasks, where the same passages appear repeatedly. LMCache recognizes those overlaps and skips recomputation by injecting cached KV directly into the model.

It’s lightweight, model agnostic, and integrates with serving frameworks like [vLLM](https://github.com/vllm-project/vllm), an open source engine that delivers fast, efficient LLM inference with support for popular models and token streaming. LMCache is designed to work with open-weight, self-hosted models like [Mistral](https://mistral.ai/news/announcing-mistral-7b), [Qwen](https://huggingface.co/Qwen), and [Llama](https://www.llama.com/). For these models, it caches KV matrices to avoid recomputation during inference. LMCache does not support KV reuse or token caching for hosted APIs like OpenAI or Anthropic. Token caching, when used, is typically handled by other components in the serving stack.

LMCache lets LLMs prefill each reusable chunk only once. It caches token-level KV pairs for all previously seen content—not just prefixes—and reuses them even if the same text appears later in the prompt or in a different order. The cache works across any serving engine instance, making reuse possible at scale. This drastically reduces prefill delay (also known as time to first token, or TTFT) while saving valuable GPU cycles and memory.

LMCache works at the chunk level, so it can skip recomputation for repeated text wherever it shows up in the conversation. Unlike traditional prefix caching, which only helps when repeated tokens appear at the start, chunk-level caching captures overlaps even if the tokens show up in a different position.

For example, imagine a customer support agent that handles returns and shipping queries. The phrase *“You can return your item within 30 days of purchase”* appears frequently in support responses, sometimes at the start of the answer, sometimes at the end. LMCache stores the KV cache for that phrase once and reuses it, even if it appears later or in a different order in a new prompt.

When paired with high-throughput engines like vLLM, LMCache has shown significant speedups in multi-turn QA, RAG, and chat-style applications.

## Why pair LMCache with Redis?

LMCache manages which token chunks are reusable. Redis stores and retrieves those chunks with low latency.

Redis is a high performance backend that stores both the KV cache for each chunk and any related metadata, such as model name, format, and temperature, in structured fields. This metadata can be stored separately or embedded in the KV cache itself, often keyed by a hash for efficient retrieval. Redis supports storing these as JSON, hashes, or other structures depending on how you configure LMCache.

Using Redis with LMCache unlocks:

- **Low latency retrieval** at scale
- **Hybrid filtering** based on metadata like temperature or model
- **Time to Live (TTL) management** to control cache freshness
- **Production scalability** across thousands of requests or replicas

LMCache defaults to using open source Redis. You can also configure it to work with Redis Cloud by supplying your Redis connection string.

## How LMCache works with Redis

Redis is the default remote store for LMCache. Here’s how the caching flow works:

   1. LMCache receives a chunk of input tokens for processing–such as

```
“You can return your item within 30 days.”

```

   2. It computes a SHA-256 hash of the chunk and constructs a Redis key using the format: format@model_name@world_size@worker_id@chunk_hash. For example:

```
vllm@mistralai/Mistral-7B-Instruct-v0.2@1@0@a1b2c3d4e5f6...

```

   3. LMCache then stores two separate entries in Redis:

         a. One for metadata, under a key ending in @metadata. This entry is stored as a Redis hash with key-value fields. For example:

```
1) "model"  => "Mistral-7B-Instruct-v0.2"
2) "format" => "vllm"
...

```

         b. One for the KV cache, under a key ending in @kv_bytes. This is stored as a binary blob (serialized with pickle by default) For example:

```
b'\x80\x04\x95~\x02...'  # Binary data serialized with pickle

```

   4. On future requests, LMCache hashes the chunk again and queries Redis for both the metadata and KV bytes

   5. If a match is found, LMCache injects the cached KV values directly into the model. This skips the LLM’s forward pass over that chunk, including token embedding and attention computation, so the model can continue generating without reprocessing already-seen content.

LMCache also includes a set of configurable settings that let you fine-tune how caching works. These cover things like chunk size, cache priority, and storage options. Here’s a quick overview of the most important options and their defaults:

| Setting | What it controls | Default |
|---|---|---|
| Chunking behavior | Token size, overlap, and chunk splitting strategy | 128-token chunks with optional overlap |
| Backend priority | Order of cache layers (RAM, disk, Redis) | In-memory first, then Redis |
| Storage options | Serialization format, expiration, eviction policy | Pickle format, no Redis TTL |

These options let you fine-tune reuse accuracy, memory footprint, and performance to fit your GenAI app.

## Example: Inspect LMCache data with redis-cli

Before inspecting Redis, make sure[ LMCache is running](https://github.com/LMCache/LMCache/tree/dev/examples/redis_lookup#configuration-steps) as part of your LLM inference workflow. It automatically stores KV cache entries and metadata during generation. Once that happens, you can use the CLI to explore what’s been stored.

First, connect to Redis

```
redis-cli -h localhost -p 6379

```

To list LMCache keys

```
# Show all keys
KEYS *
# Show keys for a specific model
KEYS *Mistral-7B*

```

Here’s sample output from a Redis instance running LMCache:

```
localhost:6379> KEYS *
1)"vllm@mistralai/Mistral-7B-Instruct-v0.2@1@0@2aea46f4fa38170e8425a6e6ee3c5173a1fa97917bc1a583888c87ad4f9a9a20metadata"
2)"vllm@mistralai/Mistral-7B-Instruct-v0.2@1@0@2aea46f4fa38170e8425a6e6ee3c5173a1fa97917bc1a583888c87ad4f9a9a20kv_bytes"

```

This helps validate reuse behavior, debug model responses, and optimize cache logic.

Try it yourself using the [redis_lookup example](https://github.com/LMCache/LMCache/tree/dev/examples/redis_lookup). This example shows you how to inspect what LMCache stores in Redis. You’ll be able to view metadata like model name and chunk info, as well as the raw KV cache entries, using simple redis-cli commands.

## Conclusion

LLMs are powerful but computationally expensive. LMCache speeds them up by reusing past work. Redis makes that reuse fast, scalable, and production ready.

By caching reusable chunks instead of full prompts, LMCache speeds up response time and reduces GPU overhead. Redis powers the fast, scalable infrastructure that makes it all production-ready.

Together, LMCache and Redis are the fastest way to build smarter, cheaper GenAI apps.

**Ready to try it? Start here:**

- [Talk to our team](https://redis.io/meeting-4/?utm_campaign=&utm_source=&utm_medium=&utm_term=&utm_content=&gclid=) to see learn how Redis can power your LLM infrastructure
- Explore the [LMCache GitHub repo](https://github.com/LMCache/LMCache)
- Check out the [LMCache + Redis integration docs](https://docs.lmcache.ai/kv_cache/redis.html)
- Browse the full [LMCache examples directory](https://github.com/LMCache/LMCache/tree/dev/examples)
- [Run the redis_lookup example yourself](https://github.com/LMCache/LMCache/tree/dev/examples/redis_lookup)
