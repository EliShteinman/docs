---
title: "Reciprocal rank fusion: why combining search results is harder than it looks"
linkTitle: "Reciprocal rank fusion: why combining search results is harder than it looks"
url: "/blog/reciprocal-rank-fusion/"
description: "You run a keyword search and get back a ranked list with Best Matching 25 (BM25) scores. You run a vector search over the same documents and get a second list with cosine similarities. You want to..."
date: 2026-08-09
blogCategories:
- "Tech DE"
authors:
- "Jeff Mills"
lastmod: 2026-08-12
hidden: true
---

*By Jeff Mills, Director, Product Marketing · Published 9 August 2026 · updated 12 August 2026*

![Reciprocal rank fusion: why combining search results is harder than it looks](/images/blog/bcefbc5e7620f682170ea0815b23342a676d02eb-2400x1256.webp)

You run a keyword search and get back a ranked list with Best Matching 25 (BM25) scores. You run a vector search over the same documents and get a second list with cosine similarities. You want to merge them into a single ranking that surfaces the most relevant documents, keeping the exact-term matches keyword search catches and the meaning-based matches vector search catches. Adding the two scores together seems like the obvious way to get there, but it can break your ranking in ways that are easy to miss. The approach many search systems settled on instead is a formula from 2009 that fits on a napkin: reciprocal rank fusion (RRF). This guide covers what reciprocal rank fusion is, why raw scores from different retrievers usually shouldn't be added directly, where rank fusion shows up in production systems, and why retrieval speed matters more than the fusion step itself.

## What is reciprocal rank fusion?

Reciprocal rank fusion combines multiple ranked lists into a single ranking using only each document's position in each list. It ignores raw scores entirely. Introduced in 2009, RRF [almost invariably improved](https://cormack.uwaterloo.ca/cormacksigir09-rrf.pdf) on the best of the combined results when fusing the output of different retrieval systems. The formula is short:

```
RRFscore(d) = Σ 1 / (k + r(d))
```

For each ranked list where document d appears, take 1 divided by (k plus the document's rank in that list), then sum those contributions across all lists. The constant k is usually set to 60, a value the original researchers found worked well without being especially sensitive. It does two jobs: it softens the impact of one retriever ranking a document unusually high, and it keeps lower-ranked documents from vanishing entirely.

A quick example makes the behavior concrete. A document ranked #2 by keyword search and #5 by vector search scores about 0.0315. A document ranked #1 by keyword search but missing from the vector results scores about 0.016. The document both retrievers agree on wins, even though neither ranked it first. Agreement across retrievers outweighs a single first-place result.

Two properties explain RRF's popularity. It's unsupervised, so you don't need labeled queries or training data. And it accepts ranked lists no matter which retriever produced them.

## Why shouldn't you add BM25 & vector search scores?

Before getting into why RRF works, it helps to understand why the obvious alternative doesn't. Adding scores from different retrievers looks simple, but the underlying scoring methods measure different things on different scales, and the failures show up in subtle ways.

### BM25 & cosine similarity use incompatible scales

The reason RRF avoids raw scores is that those scores usually can't be mixed. BM25 scores don't have a fixed universal range and vary with the implementation, query, and corpus. Their scale isn't directly comparable with cosine similarity, which lives in a fixed range between −1 and 1. Sum the two and BM25 often wins by default, because its absolute values are often an order of magnitude larger.

Normalization is the usual patch. Rescale both score sets to a common range before combining, and the scales at least match. But normalization has sharp edges: a single outlier score can compress everything else into a narrow band, and the right blend between keyword and vector shifts from query to query. Calibrating weights per query at production scale isn't practical.

There's also drift. BM25 score distributions shift as your index grows and term frequencies change, and vector score distributions shift when you swap embedding models. Two scoring streams calibrated against each other in January can be misaligned by June, and the failure isn't always obvious. Ranking quality can gradually decline without anything appearing broken.

Older score-based fusion methods hit the same wall. When their inputs aren't normalized, they carry the underlying scale mismatches straight into the combined ranking, which is why getting normalization right tends to matter more than which score-based fusion algorithm you pick.

## How rank-based fusion sidesteps the score-scale problem

If raw scores are unreliable, the fix is to ignore them and work with something both retrievers agree on: the position of each document in the ranked list. That single change is what makes RRF hold up across very different retrieval methods.

### Ranking by position instead of raw score

Because RRF uses positions rather than scores, it avoids the scale problem entirely. Position #3 means #3 whether it came from an inverted index, an embedding model, or a hand-tuned heuristic. That common scale removes the need for raw-score normalization and reduces sensitivity to score-distribution drift, though changes that alter the underlying rankings can still affect results.

On a 2026 financial question-answering (QA) benchmark, hybrid retrieval with RRF [reported higher recall](https://arxiv.org/pdf/2604.01733) than either keyword-only or vector-only search on its own. That's the kind of retrieval that feeds retrieval-augmented generation (RAG) systems. A separate benchmark on COVID-19 literature [showed the same pattern](https://arxiv.org/abs/2604.13728): RRF fusion reported the best ranking quality on the expert-query set, ahead of both keyword-only and vector-only retrieval. The consistent takeaway across these studies is that combining retrievers tends to surface more relevant results in the top positions than either method on its own.

RRF isn't perfect. It can't distinguish a #1 result that scored 0.99 from a #1 that scored 0.51, and its preference for consensus means a document one retriever loved and the other ignored can lose to a document both merely liked. When you have labeled queries to tune with, a weighted score combination can sometimes outperform RRF. For teams without evaluation infrastructure, though, the zero-tuning starting point is usually the right one.

## Where is reciprocal rank fusion used?

RRF isn't just a hybrid-search trick. Any system that ranks the same items in multiple ways is a candidate for fusion, which is why the formula turns up in search pipelines, recommendation systems, and anywhere multiple signals compete for the top of a list.

### Hybrid search: combining keyword & vector search

Once you have a scale-free way to merge lists, a lot of ranking problems start to look like fusion problems. Hybrid search is where RRF shows up most often. Keyword search catches exact terms and names that embedding models rank too low, while vector search catches paraphrases and natural-language questions that share no words with the target document. Running both and fusing the results gives you the strengths of each.

The pattern is straightforward. The app runs keyword and vector search in parallel, each returning its own top candidates. RRF then merges the two ranked lists so documents ranked well in both rise to the top. Some pipelines add a reranking step on top of that when precision matters more than latency.

A useful way to think about the split: the database handles storage, indexing, and retrieval, and it can run the fusion step itself when hybrid search executes as a single query. The app orchestrates the surrounding pipeline and passes results to whatever comes next, often a large language model (LLM) that uses them as context. Redis Search sits on the retrieval side. It runs keyword, vector, and hybrid search, merging those results with RRF [in a single query](/blog/redis-8-4-open-source-ga/), serving as the fast retrieval layer inside Redis Iris, the real-time context engine for AI agents.

### Rank fusion for recency, personalization & other signals

Two lists is the starting case. Because rank fusion only needs positions, it can accept lists that have nothing else in common: a recency-sorted list, a popularity-sorted list, and a personalized list can all feed the same formula. This is what makes RRF useful beyond hybrid search.

Recommendation systems fuse signals like this constantly, though large platforms often move to learned weights once they have enough behavioral data to train on. RRF is the unsupervised entry point; learned blending is where teams graduate later. The core problem is the same either way: you have several ranked lists that each capture something useful, and you need one final ordering.

## Why does retrieval speed matter more than fusion?

In a typical hybrid pipeline, the fusion arithmetic is cheap. RRF is just addition across a few dozen or a few hundred candidates that have already been retrieved: no model inference, no index lookups, nothing that scales with your corpus. The expensive part is getting the candidates in the first place. Keyword search walks an inverted index, vector search walks a graph structure like Hierarchical Navigable Small World (HNSW), and both grow more expensive as your index grows.

That imbalance has two practical consequences. First, run your retrievers in parallel so total retrieval time tracks the slower retriever rather than the sum of both. Every retriever you add is a potential straggler, while the fusion step barely registers.

Second, latency budgets are tighter than they look. For interactive apps, responses under [100 milliseconds](https://www.nngroup.com/articles/response-times-3-important-limits) tend to feel near-instantaneous. Voice agents and other conversational patterns push that budget even lower. And agentic workflows raise the stakes further, because [AI agents](/blog/what-is-an-ai-agent/) often retrieve several times per task. When retrieval runs many times per request, every millisecond in the retrieval path gets multiplied.

This is why the retrieval layer, not the fusion formula, is usually where hybrid search stands or falls. Fast, in-memory retrieval keeps parallel keyword and vector searches within the latency budget the rest of your app depends on.

## Build fast hybrid search on Redis

Reciprocal rank fusion earned its ubiquity honestly: it merges ranked lists using nothing but positions, needs no training data, and works as a sensible default out of the box. The hard engineering lives on either side of the formula. A practical system still depends on retrievers that surface good candidates and run fast enough that two or three parallel paths fit the workload's latency budget. Redis approaches the problem from that retrieval side. Redis Search provides fast, in-memory keyword, vector, and hybrid search on the same instance that already holds your cache, sessions, and operational data, and it's the retrieval layer inside Redis Iris, Redis' real-time context engine. If you're building RAG or search, [try Redis Iris](https://redis.io/try-free/?rcplan=iris) and run hybrid queries against your own data, or [talk to our team](https://redis.io/meeting/) about where your retrieval latency budget is going.
