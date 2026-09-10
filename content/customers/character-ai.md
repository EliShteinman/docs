---
title: "Powering Character.ai’s low-latency, high-availability search with Redis"
linkTitle: "Powering Character.ai’s low-latency, high-availability search with Redis"
url: "/customers/character-ai/"
description: "As Character.ai’s user base grew, its existing stack built on Lancedb and Tantivy started hitting performance limits. Vector search queries were slow, hybrid queries lacked flexibility, and..."
group: "AI Consumer"
lastmod: 2026-02-25
hidden: true
---

*updated 25 February 2026*

###### Challenge

![Redis Case Study Character.ai Diagram1](/images/site-mirror/59a75c33f0edb209240d9f54a4dd5c2f3c11ab61-842x474.svg)

As Character.ai’s user base grew, its existing stack built on Lancedb and Tantivy started hitting performance limits. Vector search queries were slow, hybrid queries lacked flexibility, and advanced filtering by tags or metadata strained system resources. At peak traffic, overall latency increased, reducing the responsiveness of search results during high-demand periods.

The team also needed fresher search results. Their previous system updated indexes once every 24 hours, which delayed new characters and content from appearing in search.

With Redis, they cut that update cycle in half, now refreshing indexes roughly every 12 hours through faster batch updates. The improvement keeps search results more current while reducing the time users wait to see new content.

### Building low-latency, hybrid search for AI-scale workloads

Character.ai’s entertainment AI platform needed to retrieve relevant results quickly from a massive number of user-generated characters, yet their previous setup relied on Lancedb and Tantivy, connected through a complex offline ETL pipeline. The main bottleneck was query latency, which slowed embedding search and limited the system’s ability to handle hybrid queries efficiently. Each update also required rebuilding the vector index and downloading full-text search files from Google Cloud Storage, which delayed Kubernetes pod readiness by nearly two hours. The team also faced a learning curve working with the Lance format, which made index management and iteration slower than expected.

To meet user expectations for instant, intelligent search, Character.ai rebuilt its search layer around Redis. Redis Cloud now serves as the high-performance data store and query engine that supports hybrid, vector, and full-text search within a single, streamlined architecture.

### Redis Cloud: powering fast, flexible AI search

![Redis Case Study Character.ai Diagram2](/images/site-mirror/3a052512ee4481fcc0f890f39c287832a377b0c8-842x474.svg)

Redis Cloud powers the new search architecture with faster embedding search and full support for hybrid queries that combine vector, text, and metadata filters. The previous Lancedb setup stored all this data but struggled with query speed and lacked efficient hybrid search capabilities. By moving to Redis, Character.ai can now serve complex searches at scale with predictable, low latency.

In the new flow, Redis Cloud handles every query from the search service layer. Users initiate search requests through the Character.ai app, which routes them through an API gateway to the search service. Redis Cloud responds with near-instant retrieval, even during live ingestion or index refresh cycles.

This design simplifies operations and cuts response times dramatically. During ingestion, Redis Cloud maintains sub-900 ms P95 latency for union queries and keeps hybrid, full-text, and vector queries under 500 ms. Across all workloads, P95 latency remains below 250 ms, consistently meeting production targets without downtime or service degradation.

During twice-daily index updates, Redis Cloud handles high write throughput of about 650k writes per second. This capacity allows the system to complete ingestion efficiently without impacting live performance.

###### CONCLUSION

Character.ai’s migration to Redis shows what happens when low-latency AI meets real-time data. By unifying vector, full-text, and metadata search in Redis Cloud, the team built a system that can scale with the speed of conversation. Latency dropped, ingestion times shrank, and hybrid search became effortless—freeing engineers to focus on innovation instead of database maintenance.

Today, Redis powers Character.ai’s AI-driven search with sub-250 ms query responses and uninterrupted uptime, even during ingestion. The result: a smarter, faster infrastructure that keeps up with millions of simultaneous conversations.

> At Character.ai, every millisecond matters. Before Redis, we spent too much time fighting latency and managing complex pipelines. Redis Cloud lets us deliver fast, intelligent search that feels instantaneous to our users. By unifying embedding, full-text search and filter, sort, and pagination in one system, we’ve built an architecture that scales as quickly as our characters. Beyond the technology, the Redis team became an invaluable extension of our own, demonstrating a collaborative, agile, and deeply committed partnership in achieving our success.
