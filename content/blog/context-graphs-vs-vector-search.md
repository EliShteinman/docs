---
title: "Context graphs: when nearest-neighbor search isn't enough"
linkTitle: "Context graphs: when nearest-neighbor search isn't enough"
url: "/blog/context-graphs-vs-vector-search/"
description: "Your retrieval-augmented generation (RAG) pipeline works well on simple questions. You embedded your documents, built a vector index, and retrieval does its job. Then someone asks something that..."
date: 2026-05-31
blogCategories:
- "Tech DE"
authors:
- "Jim Allen Wallace"
lastmod: 2026-06-03
hidden: true
---

*By Jim Allen Wallace, Sr. Product Marketing Manager · Published 31 May 2026 · updated 3 June 2026*

![Context graphs: when nearest-neighbor search isn't enough](/images/blog/c64be5ba12c3a00fa3cff0f953b6cec5d0154c5a-2400x1256.webp)

Your retrieval-augmented generation (RAG) pipeline works well on simple questions. You embedded your documents, built a vector index, and retrieval does its job. Then someone asks something that requires distributed facts, and the whole thing falls apart. The answer exists in your data. Your vector search often won't surface it reliably.

Approximate nearest neighbor (ANN) search finds chunks that are semantically similar to your query, but semantic similarity can diverge from task relevance. Context graphs take a different approach: they structure knowledge as entities and relationships that AI agents can traverse.

This article covers where vector-only retrieval breaks down, what context graphs actually are, and when a dual-channel approach combining both methods makes sense for your RAG pipeline.

## Why vector-only RAG misses connected information

Vector-only RAG treats every chunk as an isolated object, with no native way to represent how chunks relate to each other. In a typical pipeline, your app converts documents into chunks, embeds each chunk as a high-dimensional vector, and stores those vectors in an index. At query time, the app embeds the user's question, retrieves the closest vectors by distance, and passes those chunks to the LLM as context.

That works when the answer lives inside a single chunk that's semantically close to the question. The blind spot is everything else: because each chunk is embedded independently, the index knows what each chunk means but not how chunks relate. A fact about Entity A in one document and a fact about Entity B in another stay disconnected, even when answering the question depends on the link between them. That gap shows up in several concrete ways.

### Multi-hop questions break vector retrieval

ANN search doesn't provide a native mechanism to follow a chain of relationships across documents. It retrieves chunks by similarity to the query embedding alone, with nothing to connect related facts. That gap widens as questions get harder: in [one evaluation on telecom specifications](https://arxiv.org/html/2507.03608v1), vector RAG trailed graph-based retrieval, with the gap most pronounced on multi-hop questions that require reasoning across documents.

### Chunk boundaries fragment context

Most default chunking approaches split documents by size or syntax, not at the boundaries of a complete idea. A single requirement, definition, or regulation can land across two chunks so that neither one holds the full answer. Nearest-neighbor search might retrieve the chunk that's most similar to the query and miss the other half entirely, leaving the model with a [partial picture](https://www.frontiersin.org/journals/artificial-intelligence/articles/10.3389/frai.2025.1697169/full).

### Similarity differs from relevance

The top-k most similar chunks aren't always the top-k most relevant chunks for a reasoning task. When LLMs generate responses from noisy context without external verification, they may follow off-topic details and incorporate them into their answers.

### Exact matches get lost

Vector embeddings prioritize meaning over literal strings. When someone searches for "error code 0x80070005," they want documents containing that exact string, but embeddings might surface conceptually related content about Windows permissions errors and miss the specific code entirely.

These issues often persist even after adjusting chunk size or tweaking index parameters. In many workloads, they're tied to how ANN search represents and retrieves information.

## What context graphs actually are

A context graph represents a document corpus as a network of entities (nodes) and the relationships between them (labeled, directed edges). It sits as a discrete [graph indexing layer](https://arxiv.org/html/2509.16780v1) between your raw documents and the generation stage of your RAG pipeline.

Traditional RAG indexes unstructured documents using dense embeddings. Graph-based retrieval instead constructs an [entity network](https://arxiv.org/html/2509.16780v1), a structured semantic layer that's especially useful in domains where the relationships among concepts carry the answer.

Three components typically show up in this framing:

- **Entity and relationship extraction:** An LLM reads the source documents at indexing time and pulls out the entities and the relationships between them.
- **Knowledge graph construction:** Extracted entities become nodes, and the relationships between them become typed edges.
- **Graph-aware retrieval:** At query time, graph traversal replaces or supplements flat ANN search.

A more advanced technique uses graph clustering algorithms to organize the knowledge graph into [graph communities](https://arxiv.org/html/2502.11371v3). Each community gets a textual summary, with lower-level communities capturing fine-grained information and higher-level communities providing increasingly abstract representations. That lets retrieval target semantically dense subgraphs instead of traversing the entire graph.

The shift in question is simple. [Vector-space ANN](https://arxiv.org/html/2507.03226v2) asks which chunks are closest to the query in vector space. Context graphs ask which entities are connected to the query, and what paths link them to other relevant entities.

## Where context graphs outperform vector-only search

Context graphs win on queries where relationships carry the answer. Once knowledge is represented as entities and edges, retrieval can follow connections that flat similarity search can't.

### Multi-hop question answering

Graph-based retrieval helps when the answer requires connecting facts across documents, because it can follow entity paths that a single similarity pass would likely miss. On the 2WikiMultiHopQA benchmark, a graph-based approach using personalized PageRank [outscored naive RAG 77.10 to 67.60](https://arxiv.org/html/2508.19855v1).

### Technical specification question answering

Graph retrieval also helps in technical corpora with dense cross-references. On telecom Open Radio Access Network (ORAN) specifications, dual-channel retrieval combining vector and graph retrieval reported [0.58 factual correctness](https://arxiv.org/html/2507.03608v1) and outperformed graph-only and vector-only approaches in that evaluation, with lower faithfulness variability than vector retrieval alone.

### Global & thematic queries

Graph retrieval extends to questions that require corpus-level synthesis. Queries like "catch me up on the last two weeks of updates" need a view across the corpus, and context graphs with community-level summaries can support that. ANN search, by contrast, is primarily designed for per-query nearest-neighbor retrieval.

## When vector-only search still wins

Vector search still wins on single-hop lookups, time-sensitive queries, and workloads where graph construction overhead isn't worth it.

### Single-hop factual lookups

Graph retrieval can underperform on simple lookup tasks. One evaluation measured [13.4% lower accuracy](https://arxiv.org/html/2506.05690v3) than vanilla RAG on Natural Questions, a standard factual retrieval benchmark, and accuracy on time-sensitive queries dropped by 16.6% in the same evaluation.

### Self-contained content

Vector search works well when each chunk already contains its answer. On math textbook page retrieval, standard embedding-based RAG outperformed graph-based retrieval where content was self-contained per page.

### Indexing & latency cost

Graph construction can be [costly to build](https://arxiv.org/html/2506.02404v2), and graph retrieval can have [higher retrieval latency](https://arxiv.org/html/2506.05690v3) than vector-only RAG. Performance also [varies by benchmark](https://arxiv.org/html/2408.04948v1). If the graph structure offers no advantage for a given query type, it adds complexity without much benefit.

If most of your queries are single-hop factual lookups, vector search with good chunking may be all you need.

## Dual-channel retrieval: combining vectors & graphs

A dual-channel retrieval architecture runs vector and graph retrieval side by side, then combines the results so each method covers the other's gaps. The text channel embeds the query and runs ANN search to retrieve the top-k semantically similar passages. The graph channel performs entity linking from the query and extracts relevant subgraphs through multi-hop traversal of entity relationship chains.

In the ORAN specification benchmark, this dual-channel architecture reported the highest factual correctness across the methods tested. Vector search handled simple lookups where a single chunk contained the answer, and graph traversal handled relational queries spanning multiple documents.

Redis supports the vector half of this pattern directly. Redis Query Engine provides vector search, and FT.HYBRID is a unified in-engine API that runs full-text and vector search together and fuses their scores into one ranked list using methods such as Reciprocal Rank Fusion. That single ranked list balances meaning and exact match, complementing graph-style retrieval without traversing a context graph itself.

[Redis Iris](https://redis.io/iris/) extends that into a unified context and memory layer for AI agents. It pairs fast vector and hybrid retrieval with semantic caching, agent memory, and fresh operational state, which makes it a practical foundation for the text channel of a dual-channel design or for a broader context engineering stack that adds a graph layer alongside it.

## Context graphs in the broader context engineering stack

Retrieval, whether vector, graph, or both, is only one part of a larger problem. Context graphs are one piece of context engineering: the practice of designing and managing [LLM context inputs](/blog/context-engineering-ai/) during inference. That includes system instructions, conversation history, retrieved documents, tool definitions, tool call results, and working state: everything that goes into the model's context window, not just the prompt.

That last distinction is what separates context engineering from prompt engineering. Prompt engineering focuses on writing and organizing LLM instructions. Context engineering covers the strategies for curating and maintaining the optimal set of tokens during inference. Without a memory layer, context engineering [becomes prompt engineering](/blog/context-engineering-best-practices-for-an-emerging-discipline/) by another name.

Get this wrong and it shows up in production. Agent systems hit a handful of recurring failure modes that retrieval quality alone can't address: poisoned context, distraction, tool confusion, [conflicts across sources](/blog/context-orchestration/), and context-window degradation. You need ways to control what context gets in, what stays in, and how conflicting signals get resolved. Graph-based architectures may [support structured retrieval](https://arxiv.org/html/2507.13334v1) through more explicit paths, relational filtering, or deduplication, but they're one retrieval mechanism inside a stack that also needs [smart caching](/blog/redis-smart-cache/), memory, real-time data access, and orchestration.

That broader stack is what [Redis Iris](https://redis.io/iris/) is built for. Iris combines five tools into a single runtime: Redis Context Retriever, Redis Data Integration for keeping operational state fresh via change data capture, Redis Agent Memory for working memory and long-term recall across sessions, [semantic caching](https://university.redis.io/course/ihjs7iip0gpkrw) for LLM prompts and responses, and Redis Search for vector, hybrid, and full-text retrieval.

## Vectors & graphs belong in the same retrieval stack

Vector search is strong at semantic lookup. Context graphs are strong at relationship-aware retrieval. [Neither approach dominates](https://arxiv.org/html/2408.04948v1) across all query types, so workloads that mix single-hop lookups with multi-hop reasoning benefit from a dual-channel design rather than forcing one method to do everything.

For teams building RAG pipelines, [AI agents infrastructure](https://redis.io/guides/ai-agents-infrastructure/), or search apps, the retrieval stack also needs fast response times, fresh operational context, memory, and orchestration around it. Redis fits that model by bringing vector search, hybrid retrieval, semantic caching, and context infrastructure into one integrated platform.

[Try Redis free](https://redis.io/try-free/?rcplan=iris) to experiment with hybrid retrieval on your own data, or [talk to the team](https://redis.io/meeting/) about building context-aware AI infrastructure at scale.
