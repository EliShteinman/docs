---
title: "The fast lane for your AI stack"
linkTitle: "The fast lane for your AI stack"
url: "/blog/fall-release-2025/"
description: "Today, we’re excited to announce our Fall Release—a comprehensive set of updates across Redis for AI, Redis Cloud, and Redis Open Source. This release brings together core enhancements, new..."
date: 2025-09-04
blogCategories:
- "Announcements"
authors:
- "Rowan Trollope"
lastmod: 2026-06-01
hidden: true
---

*By Rowan Trollope, CEO · Published 4 September 2025 · updated 1 June 2026*

![Fall Release Program](/images/blog/75cb96c1352e15d5f8dfe8c4ddea1fdbcc7a6b36-1544x1104.webp)

Today, we’re excited to announce our Fall Release—a comprehensive set of updates across Redis for AI, Redis Cloud, and Redis Open Source. This release brings together core enhancements, new integrations, and developer tools to help you build fast, reliable applications at scale. Before we get into the details, let's take a look at where Redis is in the new world of AI.

Earlier this summer, [Andrej Karpathy](https://karpathy.ai/), the famous AI researcher, observed that we’ve entered a third wave of software. Instead of writing software line by line like the first wave, then powering it with deep-learning models trained on massive data sets in the second wave, in this third wave—which Karpathy calls [Software 3.0](https://www.youtube.com/watch?v=LCEmiRjPEtQ)—we rely on models (LLMs) that are programmed via prompts in real-time, so the model context matters most.

This is a profoundly exciting time for Redis. In this third wave, we enable instant data access for agents as a real-time context engine that searches and serves secure data fast, so devs can package the right data at the right time.

Just as Redis was a key part of the web and mobile stack, we also play a crucial role in the new agentic stack. Context is very hard to maintain and orchestrate, and Redis uniquely delivers on a few of the key challenges developers face scaling AI apps: latency, performance, security, and reducing the cost of LLM calls.

These new releases—[as well as our intent to acquire real-time data platform Decodable](/blog/redis-to-acquire-decodable-to-turbocharge-our-real-time-data-platform/)—strengthen our position as the real-time context engine in the new agentic stack, while also making scaling much easier with Redis Cloud.

Let’s take a look at what’s new.

## Redis for AI

- **LangCache public preview**: Managed semantic caching for faster responses and lower inference costs
- **Hybrid search enhancements**: New improvements and Reciprocal Rank Fusion (RRF) for unified, relevance‑optimized results
- **Vector compression**: Quantization and dimensionality reduction for 26-37% less memory usage based on Intel SVS
- **Vertical scaling GA**: Now your Redis searches and vector databases are 16X faster than ever
- **New agent framework integrations**: AutoGen, A2A, Cognee, and faster LangGraph, plus robust memory storage

## Redis Cloud

- **Redis 8.2 generally available: **Up to 35% faster than Redis 8.0–get it on Redis Cloud, Redis Software, and Redis Open Source
- **Redis Data Integration (RDI) in Cloud**: Public preview of real‑time data pipelines
- **Redis Insight in Cloud**: Embedded observability and tooling directly in Redis Cloud
- **Enhanced deployments with PrivateLink & CMEK**: New ways to easily and securely connect to Redis Cloud with lower latency
- **Bring Your Own Cloud (BYOC)**: Now on AWS you can use Redis with your existing Cloud provider and infrastructure

## Redis for AI

### langcache {#langcache}

### LangCache public preview: Fully managed semantic caching

LangCache is our fully managed semantic caching solution. It stores and retrieves semantically similar calls to LLMs for chatbots and agents, saving roundtrip latency and drastically cutting token usage.

- **Up to 70% cost savings **by eliminating redundant LLM calls
- **15X faster** response times for cache hits
- **Faster setup **over DIY semantic caching and less maintenance

Get started today with [LangCache](https://redis.io/langcache/) on Redis Cloud and start saving.

### Hybrid search enhancements

Redis is announcing simpler hybrid search to unify text and vector rankings into a single, more relevant result set.

- **Improved accuracy**: Combine text search and semantic relevance using multiple methods including Linear fusions and Reciprocal Rank Fusion (RRF)
- **Simpler implementation:** Out-of-the box so you don’t need custom code
- **No client‑side merging:** Results are fused efficiently on the server

Use hybrid search in chatbots, agents, and search apps to deliver more relevant answers with minimal developer effort. Learn more about [Redis Query Engine](https://redis.io/query-engine/).

### Quantization and dimensionality reduction

Vector search in Redis now supports quantization of embeddings and dimensionality reduction through standard scalar quantization and more advanced algorithms based on Intel SVS. Compress float vectors to 8‑bit or 4-bit integers or reduce number of dimensions for a smaller memory footprint and faster search performance.

- **Up to 37% lower costs** for Redis vector databases
- **144% faster search speeds** to boost user engagement and ROI
- **Low accuracy** impact compared with larger embeddings

Enable quantization and dimensionality reduction in Redis Cloud. Get started with [our instructions here](/blog/quantization-and-dimensionality-reduction-are-now-available-in-redis-query-engine/).

### QPF for Redis Query Engine is generally available

Add up to 16x more processing power to Redis Query Engine with the Query Performance Factor (QPF). The bigger of a factor, the more multi-threading there is so you can deliver real-time results on ever larger datasets across even more complex queries.

- **16X faster** vector search and Redis queries
- **Instantly scale compute** on large Redis Cloud instances
- **No changes** to schema or architecture

Use it now in Redis Cloud and make your current search workloads that much faster. To get started, [read our docs](https://redis.io/docs/latest/operate/oss_and_stack/stack-with-enterprise/search/scalable-query-best-practices/).

### New agent framework integrations and agent memory

To build faster, you want to use the Redis you love with existing AI frameworks and tools. We make this easier with our ecosystem integrations that let you store your data the way you want, without needing to write custom code. We’re adding new integrations with [AutoGen](https://microsoft.github.io/autogen/stable//user-guide/agentchat-user-guide/memory.html), [Cognee](/blog/build-faster-ai-memory-with-cognee-and-redis/), [A2A](https://github.com/redis-developer/a2a-redis), plus [new enhancements with LangGraph](https://github.com/redis-developer/langgraph-redis) to expand how you use our scalable, persistent memory layer for agents and chatbots.

- [**AutoGen**](https://microsoft.github.io/autogen/stable//user-guide/agentchat-user-guide/memory.html) as your framework while getting the fast data memory layer of Redis and build with existing templates
- [**A2A**](https://github.com/redis-developer/a2a-redis) lets you build with Google’s coordination framework and Redis adds persistent task storage, event queue management, and push notifications
- [**Cognee**](/blog/build-faster-ai-memory-with-cognee-and-redis/) to simplify memory management with built-in summarization, planning, and reasoning using Redis as your backbone
- [**LangGraph**](https://github.com/redis-developer/langgraph-redis) with new enhancements and performance boosts to improve your persistent memory and make your AI agents more reliable

[Try it yourself with this notebook](https://github.com/redis-developer/redis-ai-resources/blob/main/python-recipes/agents/03_memory_agent.ipynb) and add Redis to your existing agents today.

### cloud {#cloud}

## Redis Cloud

### Redis 8.2 is generally available

The fastest gets even faster with Redis 8.2, bringing a generational leap in performance and features beyond Redis 7.2.

- **Up to 35% faster** **commands** versus Redis 8.0. That’s 91% faster than Redis 7.2
- **Up to 37% smaller memory footprint **with up to 67% reduction with JSON
- **Do more with the Redis Query Engine**, **18 data structures** including **vector sets**, and **480+ commands** like hash field expiration

Find Redis 8.2 on Redis Open Source today. Redis 8.2 is coming to Redis Software and Redis Cloud—our fully managed offering—in the coming weeks. Get it in [Redis Cloud](https://redis.io/try-free/).

### Redis Data Integration (RDI) public preview

Keep your Redis caches fresh and in-sync with your source database using easy-to-setup data pipelines. Speed up your data to be real time in minutes, not weeks.

- **Always‑in‑sync caching**—eliminate stale data and cache misses
- **Zero‑code pipelines** configured through the Cloud UI
- **Lower database load** and infrastructure costs

Redis Data Integration (RDI) is coming soon to public preview on Redis Cloud, making real‑time data syncing effortless. Learn more with our [Redis Data Integration overview](https://redis.io/data-integration/).

### Redis Insight available on Redis Cloud

Redis Insight on Cloud is available for most Redis Cloud databases so you can act on your Redis data straight from your browser. Visualize and cut debugging time from hours to minutes, without having to open a terminal and context switch, to keep on top of your Redis performance.

Soon, you’ll also get access to a redesigned UI and new onboarding experience for vector search.

- **Web UI **for ease of use and access, directly in your Redis Cloud console
- **Browser **to** **filter, verify, and act on Redis data faster
- **Schema‑aware auto-complete **and** syntax highlighting** to build queries faster

Just log in to Redis Cloud and click on the Redis Insight icon to get started. Learn more with our [Redis Insight overview](https://redis.io/insight/).

### Enhanced AWS deployments: PrivateLink & CMEK

Easily and securely get connected to Redis Cloud using PrivateLink (preview) and meet your regulatory or compliance requirements with support for Customer-Managed Encryption Key (preview). These new capabilities let you maximize your existing cloud commitments and give you the flexibility to run Redis Cloud your way—with enterprise-grade support and what you love about Redis Cloud.

- **Use PrivateLink resource endpoints **to easily connect with Redis Cloud more securely without exposing your VPC and with lower latency
- **Customer-Managed Encryption Key (CMEK) is an additional option for encrypting persistent storage** such as those containing AOF or RDB snapshots. CMEK is supported on both AWS and Google Cloud deployments

To see how you can use Redis with your current AWS setup, [talk to our sales team](https://redis.io/meeting/). To learn more, [read the docs](https://redis.io/docs/latest/operate/rc/security/).

### Bring Your Own Cloud (BYOC): More flexibility, same Redis Cloud

Get the benefits of Redis Cloud on your own infrastructure. With BYOC, you can align Redis Cloud to your business priorities, from ensuring compliance to making the most of your current cloud commitments, while enjoying enterprise-level support and low operational burden.

- **Deploy Redis Cloud in AWS** with minimal setup and less maintenance
- **Retain full control** over network, data, and compliance
- **Pay with existing credits** while getting all the benefits of Redis Cloud

To see how you can use Redis with your current cloud setup, talk to our sales team.  To learn more, [read the docs](https://redis.io/docs/latest/operate/rc/subscriptions/bring-your-own-cloud/).
