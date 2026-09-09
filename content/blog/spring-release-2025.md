---
title: "Introducing LangCache and vector sets, simple solutions for high-performing AI apps"
linkTitle: "Introducing LangCache and vector sets, simple solutions for high-performing AI apps"
url: "/blog/spring-release-2025/"
description: "Today, we announced two new offerings for AI developers to help them build better apps. Redis LangCache, a new fully-managed semantic caching service for AI apps and agents, provides a hosted..."
date: 2025-04-08
blogCategories:
- "Announcements"
- "Company"
- "News"
authors:
- "Rowan Trollope"
lastmod: 2026-08-13
hidden: true
---

*By Rowan Trollope, CEO · Published 8 April 2025 · updated 13 August 2026*

![Blog tile image](/images/blog/41328b9a2aafc3f3c511e8acbd077848d0e8d71a-1544x1104.webp)

Today, we announced two new offerings for AI developers to help them build better apps. Redis LangCache, a new fully-managed semantic caching service for AI apps and agents, provides a hosted semantic cache using an API connection that makes AI apps faster and more accurate. Vector sets, a new native data type for Redis, allows developers to easily access and work with vectors and use them in more composable and scalable ways. Both give developers a simpler way to work with the complex data needed to build agentic apps.

Both of these, alongside a host of other new tools, features, upgrades, and integrations provide the comprehensive real-time data architecture developers need to build faster, more accurate GenAI apps and agents. We can’t wait for you to get started.

### LangCache: fully managed semantic caching powered by Redis

LangCache, our new managed service for semantic caching, is now available in private preview. With LangCache, you can seamlessly integrate LLM response caching into your application. It features a REST API interface for effortless implementation and includes advanced optimizations to ensure highly accurate caching performance. Semantic caching is essential for GenAI applications, as it significantly reduces response latency and improves cost efficiency while maintaining high-quality user interactions.

LangCache lets you:

- Take user queries and return relevant prompts that have been previously stored to save on costly calls to LLMs and speed up GenAI apps.
- Improve accuracy of LLM cache retrieval using our [custom fine-tuned models](https://huggingface.co/redis) and configurable search criteria, including search algorithm and threshold distance.
- Generate embeddings through your model provider of choice. No more separately managing models, API keys, and model-specific variables.
- Govern responses so that apps only return data that’s approved for the current user. Skip building separate security protocols as part of your app.
- Build GenAI apps faster with our fully managed service. You no longer need to set up and manage the vector database and cache invalidation yourself.

Sign up for the private preview [here](https://redis.io/langcache/).

### Introducing vector sets, a new native data type for vector similarity

Vector sets are a groundbreaking native data type that allows developers to easily access and work with vectors. Vector sets were developed by the original creator of Redis, Salvatore Sanfilippo. They take inspiration from sorted sets, and extend this concept to store and query vector embeddings to search data semantically. Like a sorted set, a vector set has string elements, but now they’re associated with a vector instead of a score. The fundamental goal of vector sets is to make it possible to add items, and later get a subset of the added items that are the most similar to a specified vector. We’re excited to see what you build with them. They’re available now in beta with Redis 8. Learn more about vector sets and how to use them [here](/blog/announcing-vector-sets-a-new-redis-data-type-for-vector-similarity/).

Vector search is improving in even more ways. We’re introducing hybrid search which combines full-text search with vector similarity search. By combining different query types, hybrid search delivers more relevant results for your apps. You can implement it yourself with the [new RedisVL 0.5.1 here](https://github.com/redis/redis-vl-python/blob/main/docs/user_guide/release_guide/0_5_0_release.ipynb).

Now, Redis will offer quantization and support int8 as an even more memory-efficient vector type. Previously, Redis supported float64, float32, float16, and bfloat16. Quantization compresses the float embeddings to 8-bit integers, enabling the int8 embeddings to reduce memory usage and cost by 75% and improve search speed by 30%, all while maintaining 99.99% of the original search accuracy.

### Smarter AI agents with LangGraph integration and agent memory

We’re expanding our GenAI ecosystem with a portfolio of [native integrations for LangGraph](https://github.com/redis-developer/langgraph-redis) that are specifically designed for agent architectures and agentic apps. By integrating Redis with LangGraph’s memory architecture, LangGraph agents can leverage Redis as a fast and comprehensive data layer to deliver unmatched speed out of the box. Redis is all you need for building a LangGraph agent’s short-term memory via checkpointers, long-term memory via Store, vector database, LLM cache, and rate limiting.

We’re also releasing [Redis Agent Memory Server](https://github.com/redis-developer/agent-memory-server). It’s our open source service that provides memory management for AI apps and agents. Users can manage short-term and long-term memory for AI conversations, with features like automatic topic extraction, entity recognition, and context summarization.

This builds on our existing portfolio of GenAI integration partnerships with [LangChain](https://github.com/langchain-ai/langchain-redis/blob/main/libs/redis/README.md), [LlamaIndex](https://docs.llamaindex.ai/en/stable/api_reference/storage/vector_store/redis/), [LiteLLM](https://docs.litellm.ai/docs/caching/all_caches#initialize-cache---in-memory-redis-s3-bucket-redis-semantic-disk-cache-qdrant-semantic), [Mem0](https://docs.mem0.ai/components/vectordbs/dbs/redis), and [Haystack](https://haystack.deepset.ai/integrations/basic-agent-memory) that build on Redis as a high-performance vector database and LLM cache. Speed up your development velocity when building agentic applications while ensuring your apps deliver on real-time performance.

To build faster with agents and Redis Cloud, we released our [Redis Cloud Admin API MCP Server](https://github.com/redis/mcp-redis-cloud/). It’s a natural-language Redis Cloud administrator, and you can ask questions about your subscription and take action, like deploying a new database under the subscription. This MCP server can be integrated with MCP-compatible client applications, like Claude Desktop or Cursor.

Learn more on how you can get access to the best of caching and AI [here](https://redis.io/redis-for-ai/).

## Redis Cloud: start and deliver on real-time GenAI faster

As GenAI brings a proliferation of different data types, devs need a platform that handles it all fast wherever you need it: multi-cloud or hybrid, at scale, and with the highest efficiencies to deliver optimized total cost of ownership.

We’re delivering all of that to you with new tools and features on Redis Cloud, including Redis Data Integration, Redis Flex, and Redis Insight.

### Redis Data Integration on Cloud Pro

You now have private preview access to Redis Data Integration (RDI) on Cloud Pro–our change data capture offering–which effortlessly and automatically syncs data between your cache and database. Every update in your database is an event that’s pushed over the RDI pipeline to your cache so data consistency occurs in milliseconds. And you don’t need to worry about the additional complexity this adds to your system that you need to build, test, and maintain because it’s officially supported by us.

### Redis Flex on Cloud Essentials

Public preview access to Redis Flex on Cloud Essentials is open today. Redis Flex is Redis rearchitected to natively span across both RAM and SSD, delivering the fastest speeds from the first byte to the largest of dataset sizes. With Redis Flex, you can store up to five times more data in your app and database for the same price as before. Imagine rather than only having cache hits on the last 3 months of data, your app now has cache hits over the last 15 months. Or rather than only having the last week of data be fast, have the last five weeks be real time. This reduction in latency from the increased cache hits creates better, faster app experiences.

### Redis Insight on cloud

You can view, update, query, and search the data in your Redis database directly from your browser using Redis Insight on cloud available in public preview. The web version includes many of the most commonly used features on the desktop version of Insight, our official Redis developer environment, including the Workbench and tutorials. And new to both the web and desktop versions is query autocompletion which dynamically pulls in and suggests schema, index, and key names from your Redis data in real-time so you can write queries faster and easier. Redis Insight on cloud is available in select regions today and will gradually roll out to additional regions this year.

Lastly, we’re making it possible to Bring Your Own Cloud and run Redis Cloud in your own Virtual Private Cloud today, in your chosen AWS environment while still having the support and expertise of the Redis team.

Get started with all these new features on Redis Cloud with a free trial [here](https://redis.io/try-free/), or reach out to your account manager.

## Redis 8 release candidate available now

We also made a release candidate for Redis 8 available for download. It’s the fastest version of Redis yet, with more than thirty performance improvements, support for eight new data structures, 16X more processing power for Redis Query Engine, and more reliable replication. You can download the release candidate [here](https://hub.docker.com/_/redis).

Redis 8 will be generally available in the coming weeks.
Learn more about the Spring Release at [redis.io/new](https://redis.io/new/) or tune into our [webinar](https://events.redis.io/spring-release-2025-whats-new-at-redis?utm_source=in-product&utm_medium=marketing_sourced&utm_campaign=2025-02-product_launch-release-blog-post&utm_content=wb-2025-04-03-amer-spring_release_webinar-701N100000OC56P) with live developer Q&A next week on April 16, 2025.
