---
title: "Vector indexes in Redis: algorithms, hybrid search & scaling"
linkTitle: "Vector indexes in Redis: algorithms, hybrid search & scaling"
url: "/blog/vector-indexes-in-redis/"
description: "You ask a support chatbot a question, and it pulls the right answer from thousands of docs in under 100 milliseconds. Behind that retrieval is a vector index: a data structure that makes high-..."
date: 2026-03-08
blogCategories:
- "Tech DE"
authors:
- "Jim Allen Wallace"
lastmod: 2026-03-11
hidden: true
---

*By Jim Allen Wallace, Sr. Product Marketing Manager · Published 8 March 2026 · updated 11 March 2026*

![Redis](/images/blog/66485f8465e3a924965180c9f28758769f5c523c-1200x628.webp)

You ask a support chatbot a question, and it pulls the right answer from thousands of docs in under 100 milliseconds. Behind that retrieval is a vector index: a data structure that makes high-dimensional similarity search fast enough for production. You don't need an ML background to build this into your app. You need the right infrastructure.

Redis, through the [Redis Query Engine](https://redis.io/docs/latest/develop/ai/search-and-query/vectors/) (previously delivered as the RediSearch module and now integrated into Redis 8 and Redis Cloud), has supported vector search since before it became a dominant topic in AI infrastructure. Redis 8 pushes that forward with billion-scale benchmarks, three index algorithms, hybrid search via FT.HYBRID (Redis 8.4+), and a new vector data type. This guide covers how vector indexes work in Redis, how to choose the right index type for your workload, and where they fit in real production scenarios.

## What are vector indexes?

A vector index is a data structure designed for similarity search rather than exact matching. Traditional indexes like B-trees and hash indexes are built for precise lookups, finding rows where id = 42 or name = 'Redis'. Finding the 10 records most *similar* to a query across hundreds of dimensions is a fundamentally different problem, and traditional indexes aren't built for it.

That's where [vector embeddings](https://redis.io/glossary/vector-embeddings/) come in. A vector embedding is a numerical representation of a piece of data (text, an image, audio, a product description) encoded as an array of floating-point numbers. ML models generate these arrays so that semantically similar inputs produce numerically similar outputs. Two sentences that mean the same thing end up close to each other in vector space, and two unrelated images end up far apart. The vector embedding turns meaning into math, and the vector index makes that math searchable.

The challenge is scale. A naive approach to vector search is brute-force comparison: check a query vector against every stored vector and return the closest matches. This runs in O(n) time, meaning search cost grows linearly with dataset size. It works fine with a few thousand vectors, but at hundreds of millions, it's unusable. A vector index solves this by building an optimized data structure at index time that makes nearest-neighbor search dramatically faster, trading a small amount of accuracy for orders of magnitude better performance.

Once you have a vector index, you also need to choose a distance metric. A distance metric is the formula the index uses to measure how "close" two vectors are, and different metrics capture different kinds of similarity.

- **Cosine similarity** measures the angle between two vectors. It ignores magnitude entirely, so it works well for text embeddings where direction carries the semantic meaning. Two sentences with the same meaning will point in a similar direction regardless of how long the embedding array is.
- **L2 (Euclidean) distance** measures the straight-line distance between two points in vector space. This makes it a good fit for image embeddings and spatial data where the absolute position of a vector matters, not just its direction.
- **Inner product (IP)** multiplies corresponding elements of two vectors and sums the results. Some embedding models are specifically trained for dot-product similarity, making IP the correct metric for those models. On normalized vectors, IP and cosine similarity produce equivalent rankings.

Choosing the right metric for your embedding model matters. Mismatching them degrades search quality regardless of which index type you use.

## How vector indexes work in Redis

Redis provides vector indexing through the Redis Query Engine, a unified query layer that handles storage, indexing, and retrieval alongside full-text search and metadata filtering. Vectors live in Redis Hash or JSON objects. Once indexed, you query them with FT.SEARCH or the dedicated FT.HYBRID command (Redis 8.4+).

Redis supports three index algorithms, each suited to different scale and accuracy requirements. FLAT and HNSW have been available since before Redis 8, and Redis added SVS-VAMANA in 8.2.

### The FLAT index

The FLAT index performs exact nearest-neighbor search by comparing a query vector against every stored vector, guaranteeing it returns the true nearest neighbors. Query time scales linearly with dataset size, which makes FLAT impractical for large-scale production workloads. For smaller datasets where perfect accuracy is a hard requirement, it's the right choice. The index builds fast and uses memory proportional to dataset size.

### The HNSW index

Hierarchical Navigable Small World (HNSW) is the algorithm behind most production vector search deployments. It builds a multi-layer graph at index time, where each layer is a progressively coarser representation of the dataset. At query time, search starts at the top layer and navigates down through increasingly dense layers until it reaches the most similar candidates. HNSW is designed to keep search efficient at scale and usually offers much lower latency than brute-force search on large datasets. The exact recall and latency you get depend on your data, dimensionality, and parameter tuning.

HNSW has two parameters set at index creation time that can't be changed without reindexing: M controls graph connectivity (higher values improve recall but increase memory), and EF_CONSTRUCTION controls index build quality (higher values produce a better graph at the cost of longer build times). A third parameter, EF_RUNTIME, is adjustable at query time and controls how many candidates the search considers. Raising it improves recall until you hit your latency ceiling.

### The SVS-VAMANA index

SVS-VAMANA (Scalable Vector Search with the Vamana graph algorithm) was introduced in Redis 8.2. It's a graph-based ANN index designed for memory efficiency. Where HNSW builds a multi-layer graph, Vamana builds a single-layer graph and compresses vectors internally, which reduces the memory footprint of the index. 

By default, Redis Open Source compresses SVS-VAMANA vectors with 8-bit scalar quantization (SQ8). On Intel platforms with SVS optimizations enabled, SVS-VAMANA can additionally use LVQ and LeanVec compression to further shrink index memory and accelerate search. In Redis' [benchmarks](/blog/tech-dive-comprehensive-compression-leveraging-quantization-and-dimensionality-reduction/), SVS-VAMANA delivered 26–37% total memory savings compared to HNSW at high recall levels, with the largest compression gains tied to Intel-specific LVQ/LeanVec optimizations. On non-Intel platforms and Redis Open Source without Intel SVS, SVS-VAMANA falls back to the SQ8 path. SVS-VAMANA is a strong choice when you need to serve more vectors within a fixed memory budget.

## Dimension selection & supported vector types

Before creating a vector index in Redis, two decisions shape your system's performance: embedding dimensionality and numeric precision.

Dimensionality is the length of your vector embedding arrays. Your embedding model dictates this value. Popular production models output dimensions like 384, 512, 768, 1024, or 1536. In Redis, you set the DIM parameter in your index schema to match the output width of your chosen model. Lower dimensions use less memory and search faster; higher dimensions capture more nuance but cost proportionally more in memory and compute. The right approach is to pick the model that fits your use case, set DIM to match, and then benchmark accuracy against your actual data.

Redis Query Engine supports the following numeric types for vector fields:

- **FLOAT32 and FLOAT64: **supported in all vector-search-capable releases
- **FLOAT16 and BFLOAT16: **supported in Redis Query Engine v2.10 and later
- **INT8 and UINT8: **supported as part of Redis 8's vector quantization features

The INT8 and UINT8 types are part of Redis 8's quantization support. Compressed numeric types reduce memory footprint and can increase query throughput, though the gains depend on your dataset, dimensionality, and hardware.

## Two approaches to vector search in Redis

Beyond choosing an index algorithm, Redis offers two distinct mechanisms for vector search, each designed for different use cases.

### Vector search via Redis Query Engine

The Redis Query Engine is the full-featured path for production apps. It supports all three index types (FLAT, HNSW, SVS-VAMANA), the standard Redis distance metrics (cosine similarity, L2/Euclidean distance, and inner product), hybrid search combining vector similarity with full-text and metadata filters, and [aggregations](https://redis.io/docs/latest/develop/ai/search-and-query/advanced-concepts/aggregations/). You define indexes with FT.CREATE and query them with FT.SEARCH or FT.HYBRID. This is the right choice for any app that needs structured filtering alongside similarity search, like finding the most semantically similar products within a specific price range.

### Vector Sets

[Vector Sets](https://redis.io/docs/latest/develop/data-types/vector-sets/) are a native Redis 8 data type for vector search. They work like sorted sets, but each element is associated with a vector instead of a numeric score. You add elements with VADD and query with VSIM. HNSW indexing is built in automatically, so there's no FT.CREATE step. Vector Sets support attribute-based filtering through JSON attributes attached to elements via VSETATTR, though this is lighter-weight than the structured metadata filtering available through the Redis Query Engine. Vector Sets are a simpler native option when you want Redis-style vector commands without managing a Query Engine index.


| Feature | Vector Sets | Vector search via Redis Query Engine |
|---|---|---|
| Data type | Native vectorset | Hash or JSON with FT.CREATE |
| Indexing | Built-in HNSW, automatic | FLAT, HNSW, or SVS-VAMANA via FT.CREATE |
| Query command | VSIM | FT.SEARCH / FT.HYBRID |
| Filtering | JSON attribute expressions | Full-text, tag, numeric, and geo filters |
| Best for | Lightweight similarity, prototyping | Complex queries with structured filters |

## Hybrid search & vector indexes in Redis 8.4

Redis 8.4 introduced the FT.HYBRID command, which combines vector search and full-text search in a single query. A single call retrieves results that are semantically similar to a query vector, textually relevant to a keyword search, and filtered by metadata, all at once. It merges ranking signals using score fusion, with two methods available: Reciprocal Rank Fusion (RRF) ranks results higher when they appear near the top of both lists, while Linear Combination lets you weight text and vector scores directly. Redis 8.4 also brought search performance gains for distributed workloads. In sharded deployments, parallel I/O processing [reported up to 4.7x](/blog/redis-8-4-open-source-ga/) throughput increases by eliminating a single-thread bottleneck in shard response handling. See the [hybrid search docs](https://redis.io/docs/latest/develop/interact/search-and-query/advanced-concepts/vectors/) for syntax and implementation details.

## Vector indexes for RAG & real-world use cases

Retrieval augmented generation (RAG) is the primary reason vector indexes moved from a niche capability to mainstream infrastructure. In a RAG pipeline, an app embeds a user's query, uses a vector index to retrieve the most semantically similar chunks from a document store, and passes those chunks as context to a large language model (LLM). The quality of the LLM's response depends directly on the quality of the retrieval, which makes the vector index a core part of your architecture.

Redis fits RAG well because it collapses what would otherwise be a multi-system stack. Your app can store document chunks in [Redis JSON](https://redis.io/docs/latest/commands/json.set/) objects, index their embeddings with HNSW, retrieve the top-k most relevant chunks at query time, and cache the LLM's responses using [Redis LangCache](https://redis.io/solutions/semantic-caching/). Redis LangCache uses semantic caching to recognize when two queries carry the same intent despite different wording, serving cached responses rather than making duplicate LLM API calls. For high-repetition workloads, Redis LangCache has [reported up to 15x](/blog/context-window-management-llm-apps-developer-guide/) faster cache-hit responses and [up to 73%](/blog/llm-token-optimization-speed-up-apps/) lower LLM inference costs. Results depend on query redundancy patterns and similarity threshold tuning.

Beyond RAG, vector indexes in Redis support a range of production use cases: semantic search (querying content by meaning rather than exact keywords), real-time recommendation systems (finding similar products, articles, or user profiles), [deduplication](https://redis.io/solutions/deduplication/) (identifying near-duplicate content at scale), and anomaly detection (flagging records that fall outside expected similarity clusters). In each case, the same index types and query patterns apply. What changes is the data being embedded and the business logic surrounding the retrieval.

## Performance at scale

Redis has [benchmarked vector search at billion-scale](/blog/searching-1-billion-vectors-with-redis-8/) on 768-dimensional FLOAT16 vectors, demonstrating high-precision retrieval with sub-second median latency under concurrent query load. The results reflect the fundamental trade-off in approximate nearest-neighbor search: precision and throughput move in opposite directions. You can tune this trade-off at query time by adjusting EF_RUNTIME, no reindexing required.

Redis 8.6 further improves vector set performance. In Redis' benchmarks comparing 8.6 to 8.4, vector set insert performance improved by up to 43% and query performance [by up to 58%](/blog/announcing-redis-86-performance-improvements-streams/), depending on data, configuration, and hardware.

## Vector indexes are infrastructure

Vector search has moved from an experimental AI capability to a core piece of production infrastructure. The teams building the fastest AI apps treat the vector index as load-bearing architecture, the same way they treat their caching layer or primary data store.

Redis provides vector indexes as part of a unified platform that also handles caching, [session management](https://redis.io/solutions/session-management/), streaming, and operational data. Your RAG pipeline, your semantic cache, and your app state can often be consolidated on Redis and Redis-managed services rather than being spread across a separate vector database, cache, and data store. With three index algorithms, full hybrid search via FT.HYBRID, and Vector Sets for lighter-weight use cases, Redis covers the full spectrum from rapid prototyping to enterprise-scale AI infrastructure.

If you're building an AI-powered app and want to see what vector indexes in Redis look like with your actual data, [try Redis free](https://redis.io/try-free/) and start indexing in minutes. If you're evaluating Redis for a larger deployment or want to talk through your architecture, [meet with our team](https://redis.io/meeting/).
