---
title: "Vector search in production: index trade-offs, failure modes & what to watch"
linkTitle: "Vector search in production: index trade-offs, failure modes & what to watch"
url: "/blog/vector-search-practical-guide/"
description: "Vector search runs on a simple idea: turn data into coordinates, and treat similarity as distance. An embedding model maps each sentence, image, or document to a point in a few hundred dimensions..."
date: 2026-08-14
blogCategories:
- "Tech DE"
authors:
- "Cedric Turner"
lastmod: 2026-08-19
hidden: true
---

*By Cedric Turner, Solution Architect · Published 14 August 2026 · updated 19 August 2026*

![Mastering Vector Similarity Search: A Practical Guide](/images/site-mirror/f16f881280f216824e31cc4a4b7d185d6dfad353-2400x1256.webp)

Vector search runs on a simple idea: turn data into coordinates, and treat similarity as distance. An embedding model maps each sentence, image, or document to a point in a few hundred dimensions of space, where items with related meaning land near each other. Finding the "most similar" result becomes a nearest-neighbor problem, one a database can index and answer in milliseconds. If you want the fundamentals first, start with our [complete guide](/blog/vector-search-guide/) and come back here for the production view.

This guide covers how indexing algorithms trade accuracy for speed, where vector search runs in production, what tends to break as datasets and traffic grow, and how to think about the operational choices behind each.

## Vector embeddings & how they capture meaning

Comparing meaning starts with representing it numerically. A vector embedding is a dense numerical representation of a piece of data (text, an image, an audio clip) produced by an embedding model trained to place items with similar meaning close together in vector space. They are numerical fingerprints of data, and distance between fingerprints stands in for similarity of meaning.

Here's a concrete example. Take three sentences, "The weather is lovely today," "It's sunny out," and "He drove to the stadium." Run them through all-MiniLM-L6-v2, a small open-source model that turns text into 384-dimensional vectors, and the two weather sentences land close together while the stadium sentence sits off on its own. The first two don't share a single word, yet the model still places them near each other, because it's matching on meaning rather than exact wording. That's the whole idea. Similar meaning lands in similar places, so you can find related text even when it's worded completely differently.

Vector search doesn't replace keyword search outright. When you search for an exact string like the error code ERR_PAYMENT_GATEWAY_TIMEOUT, you want that literal match, not other documents that are [thematically similar](https://www.infoq.com/articles/vector-search-hybrid-retrieval-rag) but don't contain it. Because vector search matches on meaning rather than exact characters, it can push those near-misses to the top and bury the one you were looking for. Keyword search tends to win on identifiers and rare terms; vector search tends to win when users paraphrase, ask questions in natural language, or use different words for the same concept.

## Index types: trading accuracy for speed

Once your data is embedded, the next problem is finding nearest neighbors fast. Exact search compares the query against every stored vector, which is designed to return the true nearest neighbors but scales linearly with dataset size. That's why many production systems use approximate nearest neighbor (ANN) search, which gives up a little recall (the fraction of true nearest neighbors actually returned) in exchange for large speed gains.

For smaller datasets, a FLAT index provides exact nearest-neighbor search through a brute-force linear scan. It requires no training step and avoids the recall-latency tuning controls used by ANN indexes, though you still configure the vector schema and distance metric. A FLAT index stores raw, uncompressed vectors, so its memory footprint is predictable and scales directly with the data: a standard float32 vector takes [4 bytes per dimension](https://github.com/facebookresearch/faiss/wiki/Guidelines-to-choose-an-index/d733a58d8f18c23b8e722c92231489fc3384748e), which puts a 768-dimensional vector at about 3 KB. As a general pattern, FLAT works well for smaller datasets or when exact nearest-neighbor results matter more than latency, though the right cutoff depends on your workload.

Graph-based indexes like Hierarchical Navigable Small World (HNSW) have become one of the primary approaches to approximate search. HNSW builds a multi-layer graph where each layer gives a different level of abstraction. A search starts at the top, hops toward the query, and descends, so it typically scales logarithmically rather than linearly. The trade-off is memory. That overhead is set by M, the number of neighbor links HNSW keeps per node: a higher M improves recall but uses more RAM. Across the M values the paper recommends (roughly 6 to 48), that works out to [48–384 bytes per object](https://arxiv.org/pdf/1603.09320v2) on top of the vectors themselves.

HNSW exposes controls that trade recall against RAM, build time, and query latency. The recall-latency trade is steep at the top end. On one dataset, HNSW recall increased from 0.8 to 0.95. This [increased HNSW query latency](/blog/common-challenges-working-with-vector-databases/) by about 31%.

## Distance metrics: cosine, Euclidean & dot product

An index also needs a definition of "close," and three metrics cover most workloads. Cosine similarity measures the angle between vectors and ignores magnitude, which is why it's the [default in Sentence Transformers](https://sbert.net/docs/sentence_transformer/usage/semantic_textual_similarity.html) and the common choice for text. Euclidean (L2) distance measures straight-line distance and is standard in [vector space classification](https://nlp.stanford.edu/IR-book/html/htmledition/document-representations-and-measures-of-relatedness-in-vector-spaces-1.html) like k-nearest neighbors (KNN). Dot product (inner product) is sensitive to magnitude, but for length-normalized vectors, [cosine equals dot product](https://web.stanford.edu/class/cs276/19handouts/lecture6-tfidf-1per.pdf), and the dot product is cheaper to compute.

If your embedding model normalizes its output, all three metrics produce the same rankings, which is why many teams pick dot product for speed. Redis supports three distance metrics across all of its vector index types: L2, inner product (IP), and COSINE.

## Where vector search runs in production

With those pieces in place, the interesting question is what people actually build. Five patterns show up repeatedly in production:

- **RAG:** your app chunks documents, generates vector embeddings, and stores them. At query time, the app embeds the user's question, retrieves the most similar chunks, and passes them to the [LLM as context](https://university.redis.io/course/ihjs7iip0gpkrw). The database stores, indexes, and retrieves; the app orchestrates.
- **Hybrid search:** runs a Best Matching 25 (BM25) lexical retriever and a vector retriever in parallel, then merges the ranked lists, often with [reciprocal rank fusion](https://cormack.uwaterloo.ca/cormacksigir09-rrf.pdf) (RRF), which merges lists by rank rather than by score. It exists because dense retrievers can stumble outside their training domain: on the Benchmarking Information Retrieval (BEIR) benchmark, the top-performing dense model in that evaluation beat BM25 on only [9 of 18 datasets](https://ar5iv.labs.arxiv.org/html/2104.08663). Combining both can recover exact-match precision and semantic recall.
- **Semantic caching:** stores vector embeddings of prompts alongside their LLM responses. When a new prompt lands within a similarity threshold of a cached one, the system returns the cached response and skips the LLM call. Repeated queries make up about [31% of queries](https://arxiv.org/html/2403.02694v2) in studied workloads. Redis reported up to [73% cost reduction](/blog/llm-token-optimization-speed-up-apps/) in high-repetition workloads with Redis LangCache, its managed semantic caching service (in public preview).
- **Recommendations:** two-tower models embed users and items into a shared space and score relevance by dot product. Item vectors can be pre-computed and cached offline, and Snap's production retrieval system queries HNSW indexes to serve results.
- **Agent memory:** long-term memory stores facts extracted from past sessions as vector embeddings so an [AI agent](/blog/what-is-an-ai-agent/) can recall relevant history across conversations. Redis stores those memories as an HNSW vector field with tag filters, so an agent can retrieve semantically relevant history for a single user in [one](https://redis.io/docs/latest/develop/use-cases/agent-memory) [FT.SEARCH](http://FT.SEARCH) [call](https://redis.io/docs/latest/develop/use-cases/agent-memory).

Most of these patterns put the vector index directly on the request path, which means retrieval latency adds to user-facing latency on queries that invoke retrieval.

## What breaks as datasets grow & how teams handle it

Sitting on the request path is also where the pain shows up as you scale, and memory usually bites first. HNSW keeps its whole graph in RAM right next to the vectors. That's what makes queries fast, but it also means your memory bill climbs as fast as your data does. At a billion vectors, the index alone can run into hundreds of gigabytes. The usual fix is quantization, which compresses those float32 vectors into a smaller, lower-precision or binary form so a bigger index still fits in memory.

Filtering trips people up in a less obvious way. Say you add a metadata filter that only a handful of documents match. HNSW still walks its graph hunting for near neighbors, but when most nodes fail the filter, the paths it would normally follow get cut off, and it can skip right past vectors that actually qualify. So the tighter the filter, the more [recall tends to drop](https://arxiv.org/html/2602.11443), and the results you get back can be less relevant than you'd expect.

Embedding drift catches teams that swap out their model without a plan. Build an index with one embedding model, then query it with another, and the results are effectively random: each model arranges vectors in its own space, and the two don't line up. There's no shortcut around it, since changing models means re-embedding every document. Track which model built each index from day one and you'll spare yourself a painful rebuild later.

The risk running under all of these is your defaults. Index parameters, similarity thresholds, embedding dimensions: they get set once, early, and rarely touched again, and what works for a prototype often falls apart under real traffic. Benchmark against your own data, and [track query latency percentiles](https://university.redis.io/course/sdm9uvjmd0iedp) and recall against a held-out set you trust, not just whether the service is up.

## How Redis supports vector search

Many of these challenges come down to where the vector index lives and how much of the stack it can replace. Redis Iris, the real-time context engine for AI apps and agents, runs retrieval on the same system that holds your caching and session data, so semantic search sits next to what your app already serves. Underneath, Redis Search indexes vectors on hash and [JSON documents](https://university.redis.io/learningpath/6q3tbh3qk2gexx) and supports [three index types](https://redis.io/docs/latest/develop/ai/search-and-query/vectors): FLAT for exact search, HNSW for approximate search, and SVS-VAMANA, a graph index built on Intel's Scalable Vector Search (SVS) library. It also supports [8-bit scalar quantization](/blog/fall-release-2025/) for vector compression. A single query can combine vector similarity with filters on [supported metadata fields](/blog/rediscover-redis-for-vector-similarity-search/), including GEO, NUMERIC, TAG, and TEXT. Redis 8.4 also added FT.HYBRID, which uses [native score fusion](https://redis.io/docs/latest/operate/oss_and_stack/stack-with-enterprise/release-notes/redisce/redisos-8.4-release-notes) to merge full-text relevance and vector similarity in one execution plan.

At scale, Redis published a billion-vector benchmark using 768-dimensional vectors and including round-trip time. It ran 50 concurrent queries, each requesting the top-100 neighbors. Under that workload, Redis reported [90% precision at ~200ms](/blog/searching-1-billion-vectors-with-redis-8/) median latency. The test also covered insertions, with throughput reaching around 66,000 vectors per second and search precision holding at roughly 95% during ingestion. These are Redis' own benchmarks, run on Redis' hardware; benchmark against your own vector embeddings before you [size a cluster](https://redis.io/docs/latest/operate/rs/clusters/).

For Python teams, [the RedisVL Python client](https://redis.io/integrate/redisvl/) supports schema management, vector queries, hybrid queries, and semantic caching abstractions. And because Redis can handle these workloads in one system, teams can often simplify the request path instead of standing up a separate [vector database](https://redis.io/glossary/databases/) and cache.

## Vector search is infrastructure, not a feature

The core ideas are simple. Vector embeddings turn meaning into geometry, index choice trades recall against latency and memory, and hybrid retrieval covers the exact-match cases where semantics alone falls short. The hard part is operational. Memory footprint, filtered recall, embedding drift, and defaults that never get revisited are the parts that trip teams up in production. Those problems get easier when the vector index sits close to the data your app already serves instead of in yet another system. Redis Iris provides a fast, in-memory, real-time context layer for vector search, caching, and session data. [Try Redis Iris](https://redis.io/try-free/?rcplan=iris) to test vector search against your own vector embeddings, or [talk to our team](https://redis.io/meeting/) about your AI retrieval architecture.
