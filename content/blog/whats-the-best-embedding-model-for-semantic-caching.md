---
title: "What’s the best embedding model for semantic caching?"
linkTitle: "What’s the best embedding model for semantic caching?"
url: "/blog/whats-the-best-embedding-model-for-semantic-caching/"
description: "Semantic caching is changing how we optimize systems reliant on large language models (LLMs). By using vector embeddings, it enables faster, cost-effective responses for similar queries. But to get..."
date: 2025-02-04
blogCategories:
- "Tech"
authors:
- "Robert Shelton"
lastmod: 2025-10-01
hidden: true
---

*By Robert Shelton, AI Engineer at Redis · Published 4 February 2025 · updated 1 October 2025*

![Blog tile image](/images/blog/7e48cb7a717207ad5dc136bcbdb565e6f10f7b10-772x552.webp)

Semantic caching is changing how we optimize systems reliant on large language models (LLMs). By using vector embeddings, it enables faster, cost-effective responses for similar queries. But to get it right, developers need to tackle three main challenges:

1. How to evaluate embedding models for best performance
1. How to set the right distance threshold
1. How to solve the cold start problem when populating the cache

### What’s a semantic cache?

Like a traditional cache, a [semantic cache](/blog/what-is-semantic-caching/) serves as an in-memory layer that delivers pre-calculated responses, avoiding the need to repeat lengthy computations. But unlike a traditional cache that retrieves data based on exact key matches, a semantic cache retrieves matches based on similarity. It uses [vector embeddings](https://redis.io/glossary/vector-embeddings/) to represent queries, and a cache hit occurs when the distance between two query vectors is below a set threshold. This lets the system serve pre-calculated responses for similar queries, even if they aren’t identical.

Why is this important? Invoking LLMs is often the most expensive, slow, and repetitive ([Gill et al., 2024](https://arxiv.org/pdf/2403.02694)) part of RAG/Agentic systems. Semantic caching helps by:

1. Cutting costs through intercepting duplicate queries
1. Decreasing system latency by skipping the slow inference step

### What’s the catch?

Semantic caching works well for many use cases, but it can also lead to false positives and false negatives.

In a traditional cache, a key is either present or absent, resulting in a binary outcome. With semantic caching, a cached response could be returned for a query that is semantically similar but requires a different answer. This makes it crucial to set the right distance threshold and use effective embedding models to ensure accuracy.

## Study process overview

To evaluate embedding models for semantic caching, we started with [this dataset](https://quoradata.quora.com/First-Quora-Dataset-Release-Question-Pairs) structured as pairs of questions labeled as duplicates or not. For example:

| question1 | question2 | is_duplicate |
|---|---|---|
| what color are bananas? | what colour are bananas? | 1 |
| what is the capital city of Australia? | what is the largest city in Australia? | 0 |

Using this dataset, we generated embeddings for each pair of questions with five models:

- llmrails/ember-v1
- BAAI/bge-large-en-v1.5
- intfloat/e5-large-v2
- sentence-transformers/all-mpnet-base-v2
- openai/text-embedding-ada-002

We evaluated the results using confusion matrices to track true positives, false positives, true negatives, and false negatives across various distance thresholds. From these matrices, we derived key metrics including precision, recall, and F1 score to assess model performance. We then recorded average latency for each model and measured embedding dimensions as a proxy for memory usage. Finally, we compiled the metrics, visualized the results, and identified the best-performing model for semantic caching applications.

## The winner: all-mpnet-base-v2

The overall winner from our study was the sentence-transformers **all-mpnet-base-v2** embedding model when it came to optimizing precision, recall, memory, latency, and F1 score for use in semantic caching.

![](/images/blog/94c1f911bb6aef259a13842458be43a54cc89818-1003x978.webp)

### Key takeaways and next steps

Our small study showed that many embedding models do a good job out-of-the-box at capturing the positive case when two queries are truly duplicates. But they can struggle when it comes to figuring out when two queries are similar but not true duplicates. The models that performed the best had a broader spread for the negative case.

Looking at the figures below, you can see that there is a significant amount of overlap between true duplicate questions and similar questions that are not true duplicates below a certain threshold. Ideally, these plots would be entirely separate with no overlap between the green or blue. That way, you could set a distance threshold that drew a line in between them.

![](/images/blog/35dd21fa2b5e4066c3fa2586a12a80a30443680a-1600x426.webp)

Our study shows how important it is to pick the right embedding model to optimize semantic caching for both precision and efficiency.

While models all-mpnet-base-v2 performed well, there remains room for improvement in separating true duplicates from semantically similar but non-duplicate queries. Moving forward, we aim to explore advanced techniques such as training custom embedding models, incorporating query rewriting processes, and training classifiers for cacheable prerouting. These steps will help make semantic caching systems even more accurate and scalable for real-world use.
