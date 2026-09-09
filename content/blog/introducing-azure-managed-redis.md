---
title: "Introducing Azure Managed Redis"
linkTitle: "Introducing Azure Managed Redis"
url: "/blog/introducing-azure-managed-redis/"
description: "Today Microsoft announced Azure Managed Redis, a new fully-managed, first-party Redis offering in Microsoft Azure. Azure Managed Redis is available today in public preview. Microsoft Azure is the..."
date: 2024-11-19
blogCategories:
- "Announcements"
- "Company"
- "News"
- "Partners"
authors:
- "Rowan Trollope"
lastmod: 2026-08-13
hidden: true
---

*By Rowan Trollope, CEO · Published 19 November 2024 · updated 13 August 2026*

![Blog tile image](/images/site-mirror/87dbf648e72e425bcb52d3a93f71aad02d956938-772x552.webp)

Today Microsoft announced [Azure Managed Redis](http://aka.ms/Ignite24/Redis), a new fully-managed, first-party Redis offering in Microsoft Azure. Azure Managed Redis is available today in public preview. Microsoft Azure is the first major cloud service provider to offer its customers a licensed, multi-tiered Redis service.

This is a major milestone in our collaboration with Microsoft Azure, and a huge step forward for Azure customers already using the predecessor Azure Cache for Redis.

Every customer that migrates from any Azure Cache for Redis tier to Azure Managed Redis will gain access to years of Redis innovation. This builds on our existing integration with Microsoft Azure on the Enterprise and Enterprise Flash tiers for Azure Cache for Redis. With the introduction of Azure Managed Redis, users on Azure Cache for Redis can now access features that were previously found only on the Azure Cache for Redis Enterprise and Enterprise Flash tiers.

Azure Managed Redis users will gain access to Redis 7.4, and soon gain access to Redis 8.0, which will be available from [redis.io](https://redis.io) and can be hosted on any hyperscale cloud. This builds on our decade-plus long commitment to delivering new features and advancements while ensuring full compatibility with previous versions of Redis.

Azure Managed Redis gives developers the flexibility they need whether they have transaction, memory, or storage-heavy workloads. It covers the entire gamut of use cases from devs trying Redis for the first time, to expert engineers scaling hundreds of Redis instances.

## The most advanced and performant Redis offering yet

Azure Managed Redis introduces eight new data structures—JSON, vector, time series, and five probabilistic types—along with the fastest and most scalable Redis Query Engine to date. And with the introduction of new built-in advanced capabilities such as vector search, secondary indexing for full-text search, exact matching, geospatial queries, numeric data handling, and fast data processing, Azure Managed Redis delivers as a true multi-model real-time platform.

Devs that use Azure Managed Redis can more simply build better apps that deliver on real-time sub-millisecond latency. The built-in Redis Query Engine ensures apps get the specific data they need faster by aggregating, transforming, and filtering data straight in Redis. Devs won’t need to juggle where to store their various pieces of data to speed them up since the most common data types can now all be stored and accessed fast straight from Redis.

## Delivers on industry leading scale and security

Azure Managed Redis delivers on the best scale and SLA in the industry, building on the advancements first introduced by the Azure Cache for Redis Enterprise tier. Users can now experience up to 99.999% availability when leveraging multi-region Active-Active, the highest availability offered in the market, powered by CRDT. Apps built with Azure Managed Redis can deliver down to sub-millisecond local latency to users globally and simultaneously no matter which continent or region they’re located on.

Azure Managed Redis meets [regulatory compliance standards](https://learn.microsoft.com/en-us/azure/azure-cache-for-redis/security-controls-policy) including FedRamp, HIPAA, PCI DDS, and ISO 27001. Native Microsoft EntraID (formerly Azure Active Directory) integration allows secure, password-less access to Azure Managed Redis instances. Users can trust in knowing that data stored on Azure Managed Redis meets the industry standards that your organization or enterprise requires.

## Build on the best from the Redis and Azure ecosystems

Azure Managed Redis interoperates with [Azure AI](https://azure.microsoft.com/en-us/solutions/ai), and by leveraging the [Redis Connector for Azure Semantic Store](https://learn.microsoft.com/en-us/semantic-kernel/concepts/vector-store-connectors/out-of-the-box-connectors/redis-connector?pivots=programming-language-csharp), devs can experience the fastest benchmarked vector database in the market, helping them build faster and more real-time RAG, agents, and gateways into their GenAI apps. When used together with the [Redis Vector Library](https://redis.io/redis-for-ai/) and an ecosystem of 30+ integrations with leading GenAI offerings, including [LlamaIndex](https://github.com/run-llama/llama_index/tree/main/llama-index-integrations/vector_stores/llama-index-vector-stores-redis) and [LangChain](https://github.com/langchain-ai/langchain-redis), devs can get new GenAI capabilities and features in their apps to production faster than ever before.

Azure Managed Redis devs also have access to client libraries for .NET, Python, Java, Go, and Node that are officially supported by us and guaranteed to work seamlessly with it. Every user can utilize [Redis Insight](https://redis.io/insight/)—the official GUI for Redis—and our AI assistant [Redis Copilot](/blog/redis-copilot-built-on-redis-for-ai/), which helps devs build Redis queries and make sense of their real-time data faster. That means Redis devs can build their apps on Redis even faster while ensuring what they build works more reliably and delivers better performance.

## Get started today

Existing Azure Cache for Redis customers can easily migrate to the public preview of AMR. Please reach out to either your Microsoft or Redis representative to get access to the resource you need for the migration process.

If you are not an existing Azure Cache for Redis customer or a Microsoft Azure customer, please reach out to us [here](https://redis.io/meeting/).

And if you are an AWS or GCP customer, you can get access to Redis straight from [redis.io](http://redis.io) or directly through the [AWS Marketplace](https://aws.amazon.com/marketplace/pp/prodview-mwscixe4ujhkq) or the [Google Cloud Marketplace](https://console.cloud.google.com/marketplace/product/redis-marketplace-isaas/redis-enterprise-cloud-flexible-plan?project=redis-marketplace-isaas&utm_source=web&utm_medium=web&utm_campaign=Cloud_essentials&utm_id=Cloud_essentials).

This is an exciting new chapter in our collaboration with Microsoft. And we are excited for you to join us in this journey in building fast apps faster.
