---
title: "RedisVL momentum & what’s next"
linkTitle: "RedisVL momentum & what’s next"
url: "/blog/redisvl-momentum-and-whats-next/"
description: "Redis, a longtime favorite of developers, is seeing unprecedented velocity around AI use cases. RedisVL, initially a simple convenience layer for vector search, has quickly evolved into the AI-..."
date: 2025-11-14
blogCategories:
- "Tech"
authors:
- "Tyler Hutcherson"
- "Brian Sam-Bodden"
- "Justin Cechmanek"
lastmod: 2025-11-14
hidden: true
mirrored: true
---

*By Tyler Hutcherson, Brian Sam-Bodden, Justin Cechmanek · Published 14 November 2025*

![RedisVL momentum & what’s next](/images/site-mirror/208db42c6122dd15c4a08f01413bca5d765fa5f5-1200x628.webp)

Redis, a longtime favorite of developers, is seeing unprecedented velocity around AI use cases. RedisVL, initially a simple convenience layer for vector search, has quickly evolved into the AI-native developer interface for using Redis as a real-time context engine for LLM applications, including agents.

## RedisVL is taking off

We’ve seen steady package downloads growth over the course of the calendar year with a surge to ~500k downloads in October alone. In Q3 of this year we saw a ~67% increase in cumulative downloads compared to Q2.

![Fig 1. RedisVL downloads by day, month, and quarter during 2025.](/images/site-mirror/67cee742a308190ce478aab72d6ccbfd15720fa1-1600x946.webp)

*Fig 1. RedisVL downloads by day, month, and quarter during 2025.*

The RedisVL growth is being heavily driven by the adoption of our [LangGraph Checkpointer ](https://github.com/redis-developer/langgraph-redis)integration that helps developers scale and manage agent state.

![Fig 2. LangChain and LangGraph partner package contributions to overall RedisVL downloads.](/images/site-mirror/e6a37f5626fcda54ffef9f152510bf09a6d0d66f-1600x496.webp)

*Fig 2. LangChain and LangGraph partner package contributions to overall RedisVL downloads.*

Redis is also showing up in more customer POCs, production deployments, and open source projects as the go-to agent storage layer because it can satisfy both the speed and flexibility requirements.

This momentum is the reason we’re investing. It’s why the next phase of RedisVL is about improved developer ergonomics, more functionality, and multi-language support.

## What’s new in the latest Python RedisVL release?

RedisVL 0.11.0 introduces powerful new capabilities that make it easier than ever to build context-aware, multimodal, and low-latency AI applications.

### 1. Multi-vector queries

RedisVL takes vector search to the next level with [multi-vector queries](https://github.com/redis-developer/redis-ai-resources/blob/main/python-recipes/vector-search/05_multivector_search.ipynb) — enabling you to search across multiple embeddings at once to capture deeper context.

For example:

- Find documents similar to both a short text description and an image embedding
- Search for a song that matches both the lyrics and the audio track
- Recommend clothing that aligns with both a photo and a written style description

Each document can contain multiple vector fields. RedisVL combines their similarity scores into a single, weighted result — letting you control how much each vector input contributes.

This expands RedisVL’s reach into multimodal search while keeping the developer experience simple and familiar.

### 2. Enhanced full-text query & index customization

RedisVL now gives developers finer control over text relevance and performance.

- [Text field weighting](https://docs.redisvl.com/en/stable/api/query.html#redisvl.query.TextQuery.text_field_name): Perform similarity searches across multiple text fields and tune how much each word or field influences the result.

*Example:* A query for “new Nike Air Jordans” can prioritize *Nike* and *Jordans* over *new* — improving ranking quality without reindexing your data.

- Field-level control: Support for Redis field attributes like UNF (un-normalized form) and NOINDEX gives you more precision in how fields are indexed and sorted — ideal for high-volume or latency-sensitive workloads.

Together, these enhancements make it easier to create relevant, context-aware text search experiences using familiar RedisVL tools and patterns.

### 3. New vector index: SVS-Vamana

RedisVL 0.11.0 adds support for [**SVS-Vamana**](https://github.com/redis-developer/redis-ai-resources/tree/main/python-recipes/vector-search#:~:text=3%20weeks%20ago-,06_hnsw_to_svs_vamana_migration.ipynb,last%20week,-redis%2Dai%2Dresources), a new vector indexing algorithm optimized for both memory and performance.

Built with advanced compression techniques, SVS-Vamana offers:

- Lower memory usage
- High query throughput
- Optimizations for Intel hardware

This gives teams more flexibility to balance speed, scalability, and resource efficiency for large-scale AI workloads.

### 4. LangCache integration

Redis [LangCache](https://redis.io/langcache/), the semantic caching service for LLM applications, is now natively integrated into RedisVL.

This allows developers to combine RedisVL’s AI-native tooling with a production-grade caching layer that:

- Stores and reuses LLM responses
- Reduces API costs and latency
- Maintains consistent context across sessions

With LangCache built in, developers can now build faster, cheaper, and more consistent GenAI applications — all within a single Redis-powered platform for caching, vector storage, and semantic retrieval.

## RedisVL now speaks Java — and it's just the beginning

A brand new Java RedisVL client library is also now available!

### Why Java?

As enterprises adopt generative AI, Java developers face a familiar infrastructure dilemma. Python developers have been building AI applications with RedisVL since 2022, using a single library for vector search, semantic caching, embeddings storage, and session management.

Java teams, meanwhile, have been evaluating options—standalone vector databases like Pinecone or Weaviate, PostgreSQL with pgvector, or attempting to build their own vector search capabilities. Each approach adds complexity: another database to manage, another API to learn, data synchronization challenges, and operational overhead.

For many organizations, Redis is already running in production—handling caching, session storage, pub/sub messaging, and real-time data. RedisVL Java now unlocks a huge class of AI use cases living in enterprise and JVM-heavy infrastructure: Spring ecosystems, multi-service backends, large internal platforms, financial pipelines, streaming apps, etc.

### Getting started

RedisVL Java provides a complete Redis-based AI infrastructure:

- Vector search with schema management and flexible querying.
- Semantic caching for LLM API cost reduction.
- Embeddings cache to prevent redundant computation of vector embeddings.
- Message history for conversational AI state management.
- Document storage for binary content (images, PDFs).

It also includes [LangChain4J](https://docs.langchain4j.dev/) integration via standard interfaces like [EmbeddingStore](https://docs.langchain4j.dev/apidocs/dev/langchain4j/store/embedding/EmbeddingStore.html) and [ContentRetriever](https://docs.langchain4j.dev/apidocs/dev/langchain4j/rag/content/retriever/ContentRetriever.html).

The library is built on [Jedis](https://redis.github.io/jedis/), the established Redis client for Java, providing a familiar connection model for teams already using Redis.

Add the RedisVL dependency to your project:

```
<dependency>
  <groupId>com.redis</groupId>
  <artifactId>redisvl</artifactId>
  <version>0.1.0</version>
</dependency>

```

Follow our RedisVL [Java user guide to get started!](https://redis.github.io/redis-vl-java/redisvl/current/getting-started.html)

More languages are planned in the coming year. The goal is simple: RedisVL should meet you in your language, not the other way around.

## Closing

RedisVL started as a thin layer to help reduce boilerplate. It’s turning into a cross-language developer framework for building context-rich, low-latency AI systems — vector indexes, semantic caches, agent memory layers, LLM routers, and beyond.

The growth we’re seeing is a signal that more developers are standardizing on Redis as the real-time context engine for AI. RedisVL is the front door to that developer experience.
