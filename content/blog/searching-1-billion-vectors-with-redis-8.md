---
title: "Searching 1 billion vectors with Redis 8"
linkTitle: "Searching 1 billion vectors with Redis 8"
url: "/blog/searching-1-billion-vectors-with-redis-8/"
description: "As more and more companies get GenAI apps into production, we’re seeing increasing requests from customers for larger vector databases. We see use cases for a billion or more vectors and we’re..."
date: 2025-03-07
blogCategories:
- "Tech"
authors:
- "Lior Kogan"
- "Adriano Amaral"
- "Filipe Oliveira"
lastmod: 2026-06-01
hidden: true
mirrored: true
---

*By Lior Kogan, Adriano Amaral, Filipe Oliveira · Published 7 March 2025 · updated 1 June 2026*

![Blog tile image](/images/site-mirror/cca9b1ebf1366dd3cf286f869bd01bc82f8b5a89-772x552.webp)

As more and more companies get GenAI apps into production, we’re seeing increasing requests from customers for larger vector databases. We see use cases for a billion or more vectors and we’re happy to share our benchmarking results at this scale.

From our tests, we reached 90% precision with a **median latency of 200ms**, and 95% precision with a median latency of 1.3 seconds for the top 100 nearest neighbors, while executing 50 search queries concurrently.

Scaling vector search to a billion vectors is no small feat—but Redis 8 Community Edition makes it look easy. Today, we’ll show how Redis handles large scale apps by demonstrating real-time search on **one billion 768-dimensional vectors **with high precision. We rigorously tested indexing and search performance, proving that Redis isn’t just [the fastest vector database](/blog/benchmarking-results-for-vector-databases/)—it scales from millions to billions of vectors while maintaining real-time latency. Check out the details below.

## Our setup

We used a vector dataset prepared in collaboration with Intel®, consisting of one billion 768-dimensional vectors, using FLOAT16 precision and 10K queries with 100 ground truth (exact neighbors) per query. It was derived from the [LAION-5B dataset](https://laion.ai/blog/laion-5b/), an open large-scale dataset for training next-generation image-text models like [Stable Diffusion](https://github.com/CompVis/stable-diffusion/blob/main/Stable_Diffusion_v1_Model_Card.md) and [OpenClip](https://github.com/mlfoundations/open_clip).

The vector index used the Euclidean distance metric and FLOAT16 precision, and the following parameters were varied to achieve different precision during query time:

- EF_CONSTRUCTION (set at index creation): Number of maximum allowed potential outgoing edges candidates for each node in the graph during the graph building.
- M (set at index creation): Number of maximum allowed outgoing edges for each node in the graph in each layer. On layer zero the maximal number of outgoing edges will be 2M.
- EF_RUNTIME (variable at query time): The number of maximum top candidates to hold during the KNN search. Higher values of EF_RUNTIME will lead to more accurate results at the expense of a longer runtime.

The dataset’s ground truth of 100 nearest neighbors was used to evaluate the accuracy (recall) of each reply, and we varied M between 4, 8, 16, and 32 outgoing edges, EF_CONSTRUCTION between 4, 8, 16, and 32, and EF_RUNTIME between 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096, and 8192. To ensure reproducible results, each configuration was run 3 times, and the best results were chosen. You can [learn more about the HNSW configuration parameters and query](https://redis.io/docs/latest/develop/interact/search-and-query/advanced-concepts/vectors/) in our docs.

## Redis 8 Community Edition billion scale benchmark

In our previous [vector database benchmarks](/blog/announcing-faster-redis-query-engine-and-our-vector-database-leads-benchmarks/) blog, we focused on proving that Redis is the fastest vector database. Now we prove that we can extend from millions of vectors to billions of vectors for use cases while preserving real-time latency.

### Our results

At a billion-vectors scale, with real time indexing, Redis 8 Community Edition can sustain 66K vector insertions per second for an indexing configuration that allows precision of at least 95% (M 16 and EF_CONSTRUCTION 32). For indexing configurations that result in lower precisions (M 4 and EF_CONSTRUCTION 4), Redis 8 Community Edition can sustain higher ingestion rates of 160K vector insertions per second. Throughput can be increased further by using more servers.

For high precision queries, we can see that larger HNSW indices (higher M and EF_CONSTRUCT) improves the search quality at the expense of latency. We reach 90% precision with a median latency including RTT of 200ms, and 95% precision with a median latency includ/ing RTT of 1.3 seconds for the top 100 nearest neighbors, while executing 50 search queries concurrently.

Since the required precision and latency trade off are use case dependent, it is important to tune your HNSW parameters as depicted in the chart above.

## Get started with Redis 8 today

Redis 8 Community Edition proves that real-time vector search isn’t just for millions of vectors—it scales to billions while maintaining high performance. With the right HNSW tuning, you can balance precision, latency, and throughput to fit your use case, achieving up to 95% recall with real-time queries. Whether you’re building AI-powered search, recommendation engines, or any vector-based application, Redis gives you the fast, scalable performance you need.

Ready to scale up? Try Redis 8 Community Edition today and explore the possibilities. [Get started](https://redis.io/docs/latest/get-started/) or check out our [docs](https://redis.io/docs/latest/).
