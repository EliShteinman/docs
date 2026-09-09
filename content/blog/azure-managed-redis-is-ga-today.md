---
title: "Azure Managed Redis is GA today"
linkTitle: "Azure Managed Redis is GA today"
url: "/blog/azure-managed-redis-is-ga-today/"
description: "Last winter, we announced Azure Managed Redis, a new fully-managed, first-party Redis offering co-engineered in partnership with Microsoft Azure. Today, we’re proud to announce that it’s generally..."
date: 2025-05-19
blogCategories:
- "Announcements"
- "News"
- "Product Releases"
- "Uncategorized"
authors:
- "Rowan Trollope"
lastmod: 2026-08-13
hidden: true
---

*By Rowan Trollope, CEO · Published 19 May 2025 · updated 13 August 2026*

![Blog tile image](/images/blog/aa3d47e544441514a7e3bc591983178c17aa677e-772x552.webp)

Last winter, we announced Azure Managed Redis, a new fully-managed, first-party Redis offering co-engineered in partnership with Microsoft Azure. Today, we’re proud to announce that it’s generally available to all [Azure Customers](https://azure.microsoft.com/en-us/products/managed-redis). Microsoft Azure is the first major cloud service provider to offer its customers a licensed, multi-tiered Redis service, assuring that they always have access to new features and advancements, while ensuring full compatibility with previous versions of Redis. Azure Managed Redis (AMR) is built on Redis 7.4, and users will soon have access to [Redis 8.0](https://redis.io/docs/latest/develop/whats-new/8-0/), the latest version of Redis which [we released earlier this month](/blog/redis-8-ga/).

It’s the most advanced Redis offering on Azure to date, supporting both traditional caching and caching for AI apps and workloads, offering vector data structures and vector search, alongside secondary indexing for full-text search, exact matching, geospatial queries, numeric data handling, and fast data processing.

Azure Managed Redis builds on our existing integration with Microsoft Azure on the Enterprise and Enterprise Flash tiers for Azure Cache for Redis. Customers that migrate from any Azure Cache for Redis tier get higher throughput and substantial cost savings at equivalent memory sizes as well as simplified deployment workflow, secure-by-default approach, and deep integration within the Microsoft Azure ecosystem. Developers can use the full stack of Redis capabilities on all Azure tiers, whether they’re just starting out, or building for production.

**The fastest, most flexible way to access Redis on Azure**

Azure Managed Redis is a key piece of infrastructure for Azure developers building high-performance GenAI and agentic apps, delivering better performance and scalability at a lower cost than previous Redis services on Azure.

- **Performance:** We have introduced significant performance improvements to core Redis and customers can now take [advantage of these improvements](https://learn.microsoft.com/en-us/azure/redis/best-practices-performance?tabs=50threads6clients) on Azure Managed Redis with the GA release. Along with this, Azure Managed Redis introduces eight new data structures—JSON, vector, time series, and five probabilistic types—along with the fastest and most scalable Redis Query Engine to date. And with the introduction of new built-in advanced capabilities such as vector search, secondary indexing for full-text search, exact matching, geospatial queries, numeric data handling, and fast data processing, Azure Managed Redis is a true multi-model, real-time platform.
- **Scale and security:** Azure Managed Redis delivers unmatched scale and SLA. Users can now experience up to 99.99% using only two availability regions instead of the usual three, and 99.999% availability when using multi-region Active-Active. Users can easily scale Azure Managed Redis up and down as needed, and apps built with AMR can deliver down to sub-millisecond local latency to users globally and simultaneously no matter which continent or region they’re located on. It also meets regulatory compliance standards including FedRamp, HIPAA, PCI DDS, and ISO 27001. Secured by default, AMR comes with built-in features like TLS, Private Link and password-free authentication using Microsoft Entra.
- **Lower total cost of ownership:** Azure Managed Redis leverages multi-core utilization, allowing for higher throughput and lower latencies compared to single-threaded architecture of Redis OSS. The flexible tiering – Memory Optimized, Balanced, Compute Optimized and Flash Optimized – offers users best performance configurations for their workload avoiding unnecessary costs. With built-in vector search and real-time processing, Azure Managed Redis enhances AI applications without requiring additional infrastructure.

**Get the best from the Redis and Azure ecosystems**

Azure Managed Redis also seamlessly integrates with [Azure AI](https://azure.microsoft.com/en-us/solutions/ai), and by leveraging the [Redis Connector for Azure Semantic Store](https://learn.microsoft.com/en-us/semantic-kernel/concepts/vector-store-connectors/out-of-the-box-connectors/redis-connector?pivots=programming-language-csharp), AMR devs can experience the fastest benchmarked vector database in the market, helping them build faster and more real-time RAG, agents, and gateways into their GenAI apps. When used together with the [Redis Vector Library](https://redis.io/redis-for-ai/) and an ecosystem of 30+ integrations with leading GenAI offerings, including [LlamaIndex](https://github.com/run-llama/llama_index/tree/main/llama-index-integrations/vector_stores/llama-index-vector-stores-redis) and [LangChain](https://github.com/langchain-ai/langchain-redis), devs can get new GenAI capabilities and features in their apps to production faster than ever before.

AMR devs also have access to client libraries for .NET, Python, Java, Go, and Node that are officially supported by us and guaranteed to work seamlessly with AMR. Every AMR dev can use [Redis Insight](https://redis.io/insight/)—the official GUI for Redis—and our AI assistant [Redis Copilot](/blog/redis-copilot-built-on-redis-for-ai/), which helps devs build Redis queries and make sense of their real-time data faster. That means Redis devs can build their apps on Redis even faster while ensuring what they build works more reliably and delivers better performance.

**Get started today**

Existing Azure Cache for Redis customers can easily migrate to Azure Managed Redis. Please reach out to either your Microsoft or Redis representative to get access to the resource you need for the migration process.

If you are not an existing Azure Cache for Redis customer or a Microsoft Azure customer, please reach out to us [here](https://redis.io/meeting/).

And if you are an AWS or GCP customer, you can get access to Redis straight from [redis.io](https://redis.io) or directly through the [AWS Marketplace](https://aws.amazon.com/marketplace/pp/prodview-mwscixe4ujhkq) or the [Google Cloud Marketplace](https://console.cloud.google.com/marketplace/product/redis-marketplace-isaas/redis-enterprise-cloud-flexible-plan?project=redis-marketplace-isaas&utm_source=web&utm_medium=web&utm_campaign=Cloud_essentials&utm_id=Cloud_essentials).
