---
title: "Chunking for RAG: Strategies, tradeoffs & common mistakes"
linkTitle: "Chunking for RAG: Strategies, tradeoffs & common mistakes"
url: "/blog/chunking-strategy-rag-pipelines/"
description: "Your retrieval-augmented generation (RAG) pipeline keeps pulling back irrelevant chunks, or worse, chunks that are almost right but missing the one detail that matters. Nine times out of ten, the..."
date: 2026-04-13
blogCategories:
- "Tech DE"
authors:
- "Jim Allen Wallace"
lastmod: 2026-04-15
hidden: true
---

*By Jim Allen Wallace, Sr. Product Marketing Manager · Published 13 April 2026 · updated 15 April 2026*

![Chunking for RAG: Strategies, tradeoffs & common mistakes](/images/blog/263569ddbd3335d8e4836c825b40260aa9de81c6-2400x1256.webp)

Your retrieval-augmented generation (RAG) pipeline keeps pulling back irrelevant chunks, or worse, chunks that are almost right but missing the one detail that matters. Nine times out of ten, the problem isn't your embedding model or your prompt. It's how you split your documents in the first place.

Chunking is the process of breaking documents into smaller segments before embedding and indexing them for vector search. It sounds like a preprocessing detail, but it's one of the more important decisions in your RAG pipeline, affecting retrieval precision, index size, query latency, and the quality of LLM answers. Split documents too aggressively, and you get fragments stripped of context. Split them too conservatively, and your vector embeddings dilute multiple topics into a single representation that matches nothing well.

This guide covers the main chunking strategies, how chunk size affects retrieval quality, and where newer techniques are headed.

## Why chunking exists

To make better chunking decisions, it helps to step back and look at why chunking exists in the first place. Embedding models have fixed maximum sequence lengths. Any text that exceeds a model's max sequence length gets truncated, which means the end of your chunk disappears. Chunking keeps your text within those limits while trying to preserve meaningful context.

The problem is that [one fixed strategy](https://arxiv.org/pdf/2603.25333) rarely fits all document types. A legal filing with nested subsections, a Python codebase, and a blog post all carry information differently. Treating them the same way during chunking means at least two of those three will get worse results.

## The main chunking strategies

Now that the reason for chunking is clear, the next question is which strategy fits that tradeoff for your data. The right choice depends on your document types, query patterns, and compute budget.

### Fixed-size chunking

Text gets divided into segments of uniform length (by character count, word count, or token count) with optional overlap between consecutive chunks. Splitting happens sequentially without regard to sentence or paragraph boundaries.

This is one of the simplest approaches to implement. It's fine for prototyping and baseline benchmarking, but fixed-size chunking [loses meaning](https://arxiv.org/html/2506.16035v1) and breaks coherent concepts across multiple chunks. If you're working with homogeneous plain text and need speed over precision, it works. For anything with structure, you'll usually want a better option.

### Recursive chunking

Recursive chunking applies a prioritized list of separators in sequence (typically paragraph breaks first, then line breaks, then spaces) and recursively splits any chunk that exceeds the target size using progressively finer-grained delimiters. This preserves global structure better than fixed-size splitting, at the expense of some variation in chunk size.

For many RAG pipelines, recursive chunking is a common starting point. It balances semantic coherence with simplicity and doesn't require embedding API calls during ingestion.

### Semantic chunking

If fixed boundaries still feel too blunt, semantic chunking tries to place boundaries where the topic actually shifts. Rather than splitting at fixed positions, semantic chunking groups sentences based on [sentence similarity](https://arxiv.org/html/2512.05411v1). Cosine similarity is computed between adjacent sentence embeddings, and when similarity falls below a breakpoint threshold, a chunk boundary gets placed.

The result is chunks where adjacent sentences are more likely to stay thematically connected rather than arbitrarily divided, but one comparison of semantic and recursive chunking on the same corpus found more chunks with semantic chunking than with recursive chunking, increasing index size. Whether that improves retrieval depends on the corpus and should be benchmarked.

That said, comparisons of semantic chunking to simpler approaches show [mixed gains](https://aclanthology.org/2025.findings-naacl.114.pdf), and the added compute costs aren't always justified by consistent performance improvements. That doesn't mean semantic chunking is never better. It means you should benchmark it against recursive chunking on your own corpus before assuming improvement.

### Document-structure-based chunking

If semantic chunking still isn't enough, the next step is to use the structure the document already gives you. For structured documents (legal filings, technical manuals, API docs, financial reports), chunks can be derived from headings, sections, paragraphs, and tables. Individual elements are only split if they exceed the maximum chunk size; otherwise they stay intact.

Legal texts, for example, are organized with [nested sections](https://arxiv.org/html/2510.06999v1) and dense cross-references. Standard chunking strategies ignore that hierarchy, cutting off logical connections between subsections. When document structure carries semantic meaning, structure-aware chunking preserves it.

### Agentic & LLM-driven chunking

If document structure still leaves retrieval gaps, chunking can get even more granular. At the high end of the compute spectrum, an LLM can convert text into [atomic propositions](https://aclanthology.org/2025.icnlsp-1.15.pdf)—standalone statements conveying a single fact—and then group those propositions into coherent chunks. This approach is flexible but requires well-crafted prompts and depends on the capability of the LLM being used. It's the highest-latency and highest-cost ingestion approach, best suited for high-value, low-volume corpora.

## How chunk size affects retrieval quality

Once you've picked a strategy, chunk size becomes the next lever. The key takeaway is that your [query type](https://arxiv.org/abs/2505.21700) should drive your chunk size. The same corpus can need different chunk sizes depending on whether you're answering fact-based questions or narrative comprehension questions.

Smaller chunks tend to win for precise fact retrieval. In [one study](https://arxiv.org/abs/2505.21700), reducing chunk size from 1,024 tokens to 64 tokens improved fact-based recall@1 by 10 to 15 percentage points on entity-heavy datasets, because each vector represents a tighter, more specific concept. The tradeoff is that small chunks lose surrounding context, which hurts narrative-style queries that depend on broader passages to answer correctly. For those, larger chunks preserve the continuity that short chunks strip away.

There's also a generation-quality ceiling to watch for. Beyond approximately [2,500 tokens of context](https://arxiv.org/abs/2601.14123), generation quality can start to degrade. More retrieved context doesn't always mean [better answers](/blog/llm-context-windows/). The practical implication: even if your retrieval is good, stuffing too many chunks into the prompt can still hurt the final response.

## Common chunking mistakes in production

Once chunk size is on the table, the next problem is avoiding the mistakes that degrade retrieval quality in production. Chunking errors compound downstream. A suboptimal chunking decision flows through retrieval, reranking, and generation, degrading quality at each stage.

### Chunks that are too small

If you're still using 200-character defaults from an old tutorial, your embedding model has almost nothing to work with. Framework defaults have evolved, and chunk size should be treated as a tunable parameter rather than copied from an old setup.

### Chunks that are too large

On the flip side, chunks that span multiple topics dilute retrieval precision—the vector can't represent any concept clearly. Including an entire PDF in the prompt isn't a shortcut; it's where the context ceiling problems described above start. A common pattern to address this: index small chunks for retrieval precision and return the surrounding larger parent chunk to the LLM for generation. This separates retrieval granularity from generation context size.

### Ignoring document structure

Applying one chunking strategy uniformly across document types (PDFs, HTML, code, markdown, tables) misses structure that carries meaning. Even within PDFs, when a paragraph [spans pages](https://www.infoq.com/articles/architecting-rag-pipeline/), it's not straightforward to determine whether two separate prose blocks belong together. Tables split from their headers, functions split mid-body, and lists separated from their contextual headings all produce chunks that lose their intended meaning.

### Stripping metadata

Even if chunk boundaries are sound, metadata turns a chunk from an isolated text fragment into a locatable piece of a larger document. Fields like document title, section heading, and page number help both retrieval ranking and generation quality. Questions that require understanding beyond a single chunk can't be answered from that chunk alone. Preserve contextual metadata with each chunk before embedding.

### Relying solely on vector search

Metadata helps, but retrieval strategy matters too. Embedding-based search typically returns nearest neighbors ordered by distance or similarity, though thresholds or metadata filters can still mean some queries return no results. Vector embeddings can also miss exact-match terminology like product names or domain-specific terms. [Hybrid search patterns](/blog/hybrid-search-benefits-rag-systems/) combining Best Match 25 (BM25) scoring with dense vector similarity, often merged via Reciprocal Rank Fusion (RRF), are effective for many RAG pipelines.

## Emerging techniques: preserving context across chunks

If the common mistakes above all boil down to context loss, it's worth looking at newer methods built to reduce it. Several advanced chunking techniques aim to preserve more context at chunk boundaries, each with different cost and complexity tradeoffs.

- **Late chunking** embeds the full document first, then carves out chunks afterward so every token's representation accounts for the entire document's context. In one benchmark, [late chunking](https://arxiv.org/pdf/2409.04701) reported a ~3% average relative improvement over naive chunking on long-document retrieval across four BeIR datasets. The constraint is that your embedding model needs a context window large enough to process the full document in a single pass.
- **Contextual retrieval** prepends an LLM-generated context summary to each chunk before embedding, giving every chunk a sense of where it fits in the overall document. Combined with hybrid retrieval and reranking, this can reduce retrieval failures, but it requires an LLM call per chunk at indexing time, which adds meaningful ingestion cost for large corpora.
- **Pseudo-Instruction Chunking (PIC)** uses a document-level summary to guide chunk boundaries without requiring a full LLM call for every individual chunk. In a controlled evaluation [across six QA datasets](https://aclanthology.org/2025.findings-acl.422.pdf), PIC measured a hits@5 of 58.4 compared to 54.5 for fixed-size and 56.0 for semantic chunking.

Each trades ingestion cost for retrieval quality. The right choice depends on your corpus size, latency budget, and the gap between your current retrieval quality and what your use case requires.

## Chunking's downstream impact on vector search

These techniques help with retrieval quality, but chunking also affects the infrastructure underneath. More chunks mean more vectors, which means a larger index, more memory, and longer build times. Your chunk size determines your vector count, which determines your index memory, which determines your index algorithm, which determines your query latency. These aren't independent decisions—they're a cascade.

### Index size & algorithm selection

At scale, Hierarchical Navigable Small World (HNSW) indexes can reach [hundreds of gigabytes](https://atlarge-research.com/pdfs/2025-iiswc-vectordb.pdf). Finer chunking drives that vector count up, which can force a shift from memory-based indexes to storage-based alternatives with different throughput and accuracy tradeoffs.

### Reranking cost

When chunking produces a retrieval quality gap, reranking can recover some of it, but at a cost. One controlled study measured [9.2× latency](https://arxiv.org/html/2511.18177v1) when adding a reranker, with response time jumping from 0.22 to 2.02 seconds. Reranking isn't free, and it's worth understanding whether your chunking strategy is creating a gap that reranking has to compensate for.

### Where to start

A practical path forward: start with recursive chunking as a baseline, document your query type distribution, treat chunk size and strategy as tunable parameters, and plan your vector index architecture alongside your chunking strategy. There's no universal best chunk size, but there's usually a best chunk size for your workload.

### Vector search infrastructure

This is where your vector database matters. Many teams managing chunked RAG pipelines end up with three separate systems: a vector database, a cache, and an operational store. Redis combines all three in a single real-time data platform with a memory-first architecture, delivering sub-millisecond performance for many core operations. It supports FLAT, HNSW, and Scalable Vector Search with the Vamana graph algorithm ([SVS-VAMANA](https://redis.io/docs/latest/develop/interact/search-and-query/advanced-concepts/vectors/)) indexing, along with [metadata filtering](https://redis.io/docs/latest/develop/ai/search-and-query/vectors/) across text, numerical, geospatial, and tag attributes for hybrid queries that combine vector similarity with structured filters.

Because of this design, chunking decisions that increase vector count don't require rearchitecting your retrieval layer. In a billion-vector benchmark, Redis reported [90% precision](/blog/searching-1-billion-vectors-with-redis-8/) at ~200ms median latency with 50 concurrent queries retrieving the top-100 neighbors, including round-trip time. For document-chunk storage patterns specifically, [JSON multi-value indexing](https://redis.io/docs/latest/develop/ai/search-and-query/indexing/) can store multiple chunk vectors under a single document's JSON structure, keeping your chunks and their parent document together.

## Your chunking strategy is your retrieval strategy

Those infrastructure decisions connect directly to what you've seen throughout this article. The strategy you pick, the chunk sizes you choose, and the metadata you preserve all flow directly into how well your RAG pipeline retrieves and how much infrastructure it needs to do it.

Redis handles vector search, [semantic caching](https://redis.io/docs/latest/operate/rc/langcache/), and operational data in one place, so you can iterate on chunking strategies without coordinating changes across separate systems.

[Try Redis free](https://redis.io/try-free/) to test different chunking configurations against your own data, or [talk to our team](https://redis.io/meeting/) about optimizing your RAG infrastructure.
