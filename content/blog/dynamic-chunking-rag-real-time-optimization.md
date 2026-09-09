---
title: "Dynamic chunking for RAG: building context infrastructure that adapts"
linkTitle: "Dynamic chunking for RAG: building context infrastructure that adapts"
url: "/blog/dynamic-chunking-rag-real-time-optimization/"
description: "Most teams pick a chunk size once and never touch it again. Copy the settings a tutorial used (usually 512-token chunks with 50 tokens of overlap between them), and ship it. Then the corpus grows,..."
date: 2026-07-11
blogCategories:
- "Tech DE"
authors:
- "Jeff Mills"
lastmod: 2026-07-16
hidden: true
---

*By Jeff Mills, Director, Product Marketing · Published 11 July 2026 · updated 16 July 2026*

![Dynamic chunking for RAG: building context infrastructure that adapts](/images/blog/008061fb0f1c65a00a1f9b89315e1cae551b1714-2400x1256.webp)

Most teams pick a chunk size once and never touch it again. Copy the settings a tutorial used (usually 512-token chunks with 50 tokens of overlap between them), and ship it. Then the corpus grows, the queries get stranger, and that early choice quietly caps retrieval quality.

Chunking looks like a standalone decision, but it's the entry point into a bigger pipeline: the context infrastructure that retrieves, ranks, caches, and remembers data so an AI app or agent gets the right context fast enough to use it.

Retrieval-augmented generation (RAG) is the clearest example of that pipeline at work. It retrieves relevant context from your own data before the LLM generates an answer, and chunking decides what's available to retrieve in the first place. This guide covers why fixed-size chunking struggles as documents and queries get more varied, what "dynamic chunking" means, the main adaptive strategies and their tradeoffs, and how teams improve retrieval in real time as context changes mid-session.

## Why fixed-size chunking breaks down

Fixed-size chunking splits text at arbitrary token counts, with no regard for where an idea begins or ends. When a boundary lands mid-argument, vector search may retrieve only half of it, and the model fills the gap with whatever its training data suggests instead of your document. That's the irony: fixed-size chunking can reintroduce the exact hallucination problem RAG was built to prevent.

The problem compounds because chunk size interacts with query type. In some question-answering (QA) workloads, shorter chunks of [64–128 tokens](https://arxiv.org/abs/2505.21700) tend to work better for concise, fact-based questions, while longer chunks of [512–1024 tokens](https://arxiv.org/abs/2407.19794) work better when a query needs broader context. A single fixed size can't serve both, so teams often reach for two common fixes: overlapping chunks so fewer boundaries cut through an answer, and simply feeding the model more context to be safe. Neither held up under measurement. In one systematic QA analysis, overlap increased indexing cost with [no measurable benefit](https://arxiv.org/abs/2601.14123), and more context didn't help either: answer quality peaked, then declined past a context cliff around 2.5k tokens.

None of this means fixed-size chunking is always the wrong call. On non-synthetic datasets reflecting real-world documents, fixed-size chunking [often performed better](https://aclanthology.org/2025.findings-naacl.114.pdf) than semantic chunking, one of the alternative strategies covered below, and embedding quality frequently mattered more than chunking strategy. Fixed-size chunking specifically struggles in predictable situations: mixed-format corpora, varied query types, and documents where structure carries meaning.

## What "dynamic chunking" actually means

Dynamic chunking is the umbrella term for strategies that adjust chunk boundaries or chunk selection based on the content or the query, instead of applying one fixed rule to everything. It's the direct answer to the problems above: rather than picking one chunk size and living with its blind spots, dynamic chunking adapts.

In practice, "dynamic chunking" refers to two distinct approaches, and they aren't interchangeable:

- **Content-adaptive at ingestion:** chunk boundaries adapt to document structure and complexity rather than a fixed token count. You'll also see this called "adaptive" or "content-aware" chunking.
- **Query-adaptive at retrieval time:** the system adjusts chunk selection or granularity based on the query, in some proposals integrating user queries at the chunking step itself.

The two solve different halves of the problem: content-adaptive chunking fixes what you store, and query-adaptive chunking fixes what you pull back out.

## Common dynamic chunking strategies & their tradeoffs

Most production work happens on the content-adaptive side, where the practical question is which strategy fits your corpus and budget.

### Semantic chunking

Semantic chunking splits at meaning shifts instead of token counts, using embedding similarity to group related sentences together. Results are mixed: in one cross-strategy evaluation, semantic chunking degraded retrieval on the FiQA financial dataset by [23–27% across models](https://arxiv.org/abs/2602.16974), despite improvements on other datasets. It also costs more, since you embed every sentence just to find boundaries. It tends to help most on documents with high topic diversity and least on already well-structured content.

### Late chunking

Late chunking flips the order: embed the entire document with a long-context model first, then segment the token embeddings, so every chunk carries full-document context. In its original evaluation, late chunking reported a [3.63% relative improvement](https://arxiv.org/abs/2409.04701) over naive chunking with sentence boundaries, with larger gains on longer documents and little effect on short ones. It requires a long-context embedding model, which not every stack has.

### Hierarchical chunking

Hierarchical (parent-child) chunking indexes small child chunks for retrieval precision but returns larger parent chunks for generation context, easing the precision-versus-context tension directly. The tradeoff is maintaining a dual index, which adds complexity over flat strategies. This pattern fits well when short snippets identify relevance but the answer needs surrounding sections, tables, or definitions.

### Proposition-based chunking

Proposition-based chunking breaks passages into atomic, self-contained factoids using a fine-tuned model. It reported an average [10.1-point Recall@20 improvement](https://arxiv.org/abs/2312.06648) over passage-based retrieval with unsupervised dense retrievers, but it's among the most expensive ingestion approaches and struggles with multi-hop reasoning. It's usually worth considering when fact-level recall matters more than ingestion speed or preserving the original passage shape.

### Agentic & query-aware chunking

Agentic chunking has an LLM read each document and choose boundaries, or pick a chunking strategy per document type. The LLM call per document adds ingestion latency, which limits production use for large document collections. Query-aware approaches like Mix-of-Granularity instead pre-segment at multiple granularity levels and route each query to the right one, though routing adds its own overhead. Evaluation also has to include operations: many chunking methods fail in practice from timeouts, memory issues, or poor scalability, so reliability and efficiency belong in your evaluation alongside retrieval metrics.

## Real-time retrieval improvements: adapting context mid-session

Choosing a chunking strategy fixes how documents get stored, but that happens once, at ingestion. It can't respond to what a user actually asks. Re-chunking mid-conversation isn't practical, since it means re-embedding and re-indexing the whole corpus, which is slow batch work. So the real-time half of retrieval quality happens at query time, by adapting what you pull back and how you rank it for each specific question.

Re-ranking is the workhorse. Instead of trusting the first retrieval pass, you cast a wide net with a fast retriever, then run the candidates through a slower, more accurate model (a cross-encoder) that scores how well each chunk actually answers the query and reorders them, sending only the top few to the LLM. This catches relevant chunks that the first pass ranked too low. The cost is latency: the extra scoring step depends on model size and how many candidates you re-rank, and it can be too slow for latency-sensitive cases like voice interfaces.

Not every query needs the same effort. A simple factual lookup and a multi-part research question shouldn't run the same expensive pipeline. Adaptive routing predicts how hard a query is and matches the effort to it: skip retrieval for questions the model can already answer, do a single pass for straightforward ones, and reserve multi-step retrieval for the genuinely complex. You spend your latency budget only where it changes the answer.

Follow-up questions are the hard case. When a user asks "what about the second one?", the retriever sees a query full of pronouns and implicit references, and matches almost nothing useful. Query rewriting fixes this by rewriting the follow-up into a standalone question ("what are the fees for the premium plan?") before it hits retrieval. The catch is that rewriting adds an LLM call before you even start retrieving, so in chat-heavy workloads it can become the slowest step. One way around that bottleneck is model racing: run several rewriting models at once and take the first valid response, which pulls the median latency down.

The order you place chunks in also matters, not just which ones you pick. Models pay the most attention to the start and end of the context window and tend to [lose track of the middle](https://arxiv.org/abs/2307.03172), so putting your strongest chunks at the top and bottom (rather than burying them in the middle) is a cheap change worth testing. Chunk quality feeds two failure modes practitioners now name directly: irrelevant chunks cause context confusion, where the model gets distracted by off-topic text, and bloated low-value chunks cause context rot, where useful signal gets diluted across too many tokens.

## Redis Iris: the context engine underneath your chunking strategy

Everything above, from ingestion-time chunking to query-time re-ranking, routing, rewriting, and assembly, is work that depends on how fast the layer underneath can store, index, and retrieve vectors. [Redis Iris](https://redis.io/iris/) is a unified, real-time context engine built for that layer: it keeps operational data fresh, gives agents structured paths through business entities, persists memory across sessions, and serves cached responses for semantically similar prompts. Underneath it, Redis provides sub-millisecond latency for many core operations. That speed matters here because retrieval sits directly in the response path of every RAG query, and every extra millisecond is context the user or agent is waiting on.

Redis doesn't chunk documents. Your app chunks, embeds, and orchestrates. Redis stores the vectors that chunking produces, indexes them with Hierarchical Navigable Small World (HNSW), FLAT, or Scalable Vector Search with Vamana graphs (SVS-VAMANA) [index algorithms](https://redis.io/docs/latest/develop/interact/search-and-query/advanced-concepts/vectors/), and retrieves them fast. That clean division of labor is what lets the strategies above run against one system:

- **Query-time tuning without reindexing:** the HNSW parameter EF_RUNTIME can be [adjusted at query time](/blog/vector-indexes-in-redis/) to trade precision against latency per query, no rebuild required.
- **Fast re-indexing when you do re-chunk:** in its billion-vector benchmark, Redis measured roughly [66,000 vector insertions](/blog/searching-1-billion-vectors-with-redis-8/) per second at ~95% precision. The same benchmark reported 90% search precision at ~200ms median latency for top-100 nearest-neighbor search, including round-trip time, with 50 concurrent queries. Re-chunking experiments hurt less when ingestion is fast.
- **Hybrid search & filtering in one operation:** [hybrid search](/blog/redis-8-4-open-source-ga/) combines full-text/Best Matching 25 (BM25) retrieval with vector similarity, and Redis also supports tag, numeric, geo, and text filters in the same query so metadata about chunk granularity or document structure can shape retrieval directly.
- **Semantic caching to skip retrieval entirely:** Redis LangCache returns cached responses for semantically similar prompts. Redis reports cache hits are [up to 15x faster](/blog/context-window-management-llm-apps-developer-guide/), and LLM inference costs are [up to 73% lower](/blog/llm-token-optimization-speed-up-apps/) in high-repetition workloads.
- **Redis Agent Memory for stateful context:** conversation history, user preferences, and session state all live in the same platform as your vector index, so agents can pull retrieved chunks and prior context from one retrieval layer instead of stitching them across systems.

The best chunking strategy is workload-dependent and often changes as your corpus and queries change. A context engine that supports fast re-indexing, query-time tuning, and stateful memory keeps those changes low-cost instead of turning every experiment into an infrastructure project.

## Chunking is a moving target, not a setting

RAG was the first pattern for giving LLMs external knowledge. Context infrastructure is the production-grade layer that makes that knowledge usable: retrieved, ranked, cached, remembered, and delivered fast enough for AI apps and agents. Fixed-size chunking is where most teams start, but as documents get more varied and queries get more conversational, adaptive strategies tend to earn their extra cost, and much of the work moves to query time.

The teams that get this right treat chunking as something they'll measure, revisit, and re-run, not a config value they set in week one. That iteration only works if the infrastructure underneath doesn't punish you for it. Redis Iris gives you fast vector search, hybrid filtering, semantic caching, and agent memory in one real-time context engine, so re-chunking experiments, query-time tuning, and mid-session retrieval improvements all run against the same fast context layer your app already uses. [Try Redis Iris](https://redis.io/try-free/?rcplan=iris) to benchmark your own chunking experiments against real workloads, or [contact our team](https://redis.io/meeting/) about building the context layer for your RAG pipeline.
