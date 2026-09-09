---
title: "CP AXTRA boosts e-commerce recommendations with vector search"
linkTitle: "CP AXTRA boosts e-commerce recommendations with vector search"
url: "/customers/cp-axtra/"
description: "Watch the video"
lastmod: 2026-03-11
hidden: true
---

*updated 11 March 2026*

###### Watch the case study video

[Watch the video](https://redis-1.wistia.com/medias/86l8gqnla4)

###### Challenge

### Fast responses with flexible configurability

CP AXTRA’s e-commerce apps (Makro PRO and Lotus’s Smart App) serve a fast-changing grocery catalog where **80% of all user sessions begin with search and recommendations**—making latency and relevance directly tied to revenue. Traditional keyword search struggled with Thai-language tokenization and user typos, which resulted in subpar recommendations and low purchase rates.

![Fast responses with flexible configurability](/images/site-mirror/275a21c71970c74493d6c00622fc8a94679f42d2-792x415.svg)

CP AXTRA needed vector embeddings with 4,096 dimensions to provide the relevancy they needed to give users quality recommendations across their catalog. On the infrastructure side, OpenSearch couldn’t keep up with the dynamic updates required for live product discovery at scale with 4096 embeddings size, limiting conversion and click-through rates (CTR).

CP AXTRA required in their solution:

- **P95 vector search under 50ms** to meet <300ms end-to-end SLA and user expectations
- **4k dimensional embeddings** for highly relevant recommendations and support PEFT‑tuned LLAMA 3‑Thai model embeddings
- **Fast indexing** to support 100k+ SKU catalog that is updated constantly
- **Multi-cloud support** to prevent CSP lock-in and provide support across countries & regions

###### SOLUTION

### Redis search for instant, relevant recommendations

CP AXTRA adopted Redis Cloud on AWS as the real-time backbone cache-vector engine for their search and recommendations, combining keyword and vector retrieval into hybrid search with dynamic signals to deliver relevant results.

> Speed, performance, supportability, and cost—Redis was the only choice that let us hit our goals. With query performance factor and the right query strategies, we drove P95 down to ~30 ms—and we can even get sub‑10 ms with higher threading.

What they built:

- **Vector search in Redis** with 4,096‑dimensional embeddings to capture nuanced product semantics and user intent.
- **Multi-threaded query execution** with 2x query performance factor on Redis Query Engine to meet stringent tail-latency targets. Production latencies converged around 30 ms P95. CP AXTRA also tested sub‑10 ms vector search results via 8X threading with query performance factor, but deemed that much speed unnecessary.
- **Caching and pub/sub** in Redis for autocorrect pipelines and dynamic results reuse, reducing compute and ensuring consistent UX under load.

![Redis](/images/site-mirror/f4124a298d1fc7364e061ef57acfbc5aca4adede-1684x948.webp)

How CP AXTRA ’s search works:

1. User query (e.g., “chiken”) goes through autocorrect (Redis pub/sub)
1. Results are enriched with user context + product metadata
1. The enriched query is vectorized via LLM into 4k-dimension vector
1. Redis executes a vector search for relevant products and returns similar products and popular results
1. Results are passed to reranking model (trained with PEFT + few-shot signals) and returned to the user

Platform choices and integrations:

- [Redis Cloud through AWS Marketplace](https://aws.amazon.com/marketplace/pp/prodview-e6y7ork67pjwg)
- [Redis vector database](https://redis.io/solutions/vector-database/)
- [Redis hybrid search](https://redis.io/docs/latest/commands/ft.hybrid/)
- [RedisVL](https://docs.redisvl.com/en/latest/)

### Why Redis?

Redis was chosen because it delivered the fastest vector search performance, unified operations across their stack, supported real-time index updates, and avoided the limitations of alternatives like Milvus, Quadrant, and pgvector specially for 4096 embedding size.

- **Performance at scale:** Redis delivered 10–30 ms typical vector retrieval with headroom for sub‑10 ms under higher threading, outperforming competitors in testing. Milvus’ latency was 65-90 ms on their workloads and was more complex to operate. Quadrant came in at 90-125. And Postgres pgvector hit dimensionality and scalability constraints since it was limited to 1024 dimensions and wouldn’t support their Thai vector embedding model.
- **Unified operations:** Redis offered a familiar operational model across caching, pub/sub, and vectors—no new tooling required for teams already using Redis patterns.
- **Dynamic updates:** Real-time updates to HNSW indexes without degrading recall or inflating latencies allowed for a constantly changing grocery catalog.
- **Cloud-managed reliability:** Fully-managed Redis Cloud with straightforward AWS Marketplace made their solution easy to procure and support.

> It’s not only that Redis was fast, it’s that the other solutions were prohibitively slow.

### The results: 2X revenue and basket additions from search

CP AXTRA gave customers the products they wanted, which led to customers buying more items more often.

- **Revenue nearly doubled** from search by growing the CTR 2X from faster, more relevant search results
- **108% increase to basket additions** from “Top 5” recommendations
- **10% overall increase in search conversion rate** from improved product discovery
- **50% search-to-purchase rate achieved** through superior results

### Looking ahead

CP AXTRA plans to scale the stack across additional countries and languages, consolidate keyword and vector search further, and continue optimizing for cost and performance as usage grows.

- Expand with the same stack for their Malaysia launch
- Move additional workloads from OSS to Redis Cloud
- Expand into additional countries
