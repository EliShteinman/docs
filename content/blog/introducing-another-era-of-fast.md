---
title: "Introducing another era of fast"
linkTitle: "Introducing another era of fast"
url: "/blog/introducing-another-era-of-fast/"
description: "Today, we’re announcing new products and capabilities, which are each different articulations of our core mission: to help developers build fast apps – fast."
date: 2024-08-23
blogCategories:
- "Announcements"
- "Company"
- "Tech"
authors:
- "Rowan Trollope"
lastmod: 2026-08-13
hidden: true
---

*By Rowan Trollope, CEO · Published 23 August 2024 · updated 13 August 2026*

![Blog tile image](/images/blog/1f133595813f27e8946dba5a485e27b3c9f657ed-772x552.webp)

Today, we’re announcing new products and capabilities, which are each different articulations of our core mission: to help developers build fast apps – fast.

Redis was built to handle the speed and scale of the emerging mobile and cloud era. Redis’ creator, Salvatore Sanfilippo, started building Redis in 2009 as an internal tool to help scale his own startup. As many of those side projects seem to go, it quickly became the star product.

There’s a lot of parallels between the problems Salvatore was trying to solve back then and the challenges companies face today as they build a modern AI stack. Redis helped meet the new speed and scale demands of the mobile and cloud era. Now, we’re looking ahead to do the same for GenAI. We’re at the start of Redis’ second act — a new era of fast, where Redis is an essential part of the new stack for AI.

The new products and capabilities include:

- **Redis for AI** — Our package of capabilities gives companies foundational infrastructure for building and deploying AI apps.
- **Redis Flex** — By integrating our Speedb acquisition, we lower costs by 80%.
- **Redis 8** — This fast, flexible, and free foundation is the evolution of 15 years of work.
- **Redis Copilot** — Your new AI assistant for Redis helps you build faster on Redis.
- **Redis Data Integration** — Coming soon to Redis Cloud, you can speed up existing databases with automated data pipelines.

### Redis for AI: products, tools, and support for building fast GenAI apps

Bringing GenAI apps into production and scaling them is tough. To help make this simpler, we’re introducing Redis for AI. Redis for AI is an integrated package of all Redis’ AI capabilities and support needed to bring GenAI apps into production.

Developers can use Redis for AI for:

- **RAG with the world’s fastest vector database: **Real-time architecture for GenAI apps
- **Semantic caching: **Retrieve stored answers fast and save >30% on costly LLM calls
- **LLM memory:** Personalize user sessions with all the data LLM needs at the right time
- **Agentic memory:** Make agents faster for more complex reasoning and better answers
- **Feature store:** Get predictions in less than 1 millisecond for production ML models

It includes recipes, reference architectures, the new [RedisVL 0.3.0](https://github.com/redis/redis-vl-python), and new dedicated partner packages [langchain-redis](https://github.com/langchain-ai/langchain-redis) and [llama-index-vector-stores-redis](https://github.com/run-llama/llama_index/tree/main/llama-index-integrations/vector_stores/llama-index-vector-stores-redis). You also get our incredible ecosystem of integrations and partners, all built on our real-time data platform and [benchmark-leading vector database](/blog/benchmarking-results-for-vector-databases/).

Redis for AI offers the same flexibility Redis has always been known for, supporting several different data types, and working across cloud, on-prem, and hybrid environments. Our dedicated support lets you work with experts who have implemented Redis for AI at some of the largest companies in the world.

*“We would not have been able to scale ChatGPT without Redis.” – OpenAI*

Learn more about [Redis for AI](https://redis.io/redis-for-ai).

### Cache 5X more for the same price, from 1 GB to terabytes, with Redis Flex.

Previously, Redis Auto Tiering was only available for large caches. And devs wanted to use Redis in more places, but had to keep caches small because of cost. Small caches often need special caching strategies and application logic to handle this restriction, and create more cache misses. Now you can get 5 GB of cache for the same price as 1 GB, for all cache sizes down to 1 GB with Redis Cloud Essentials, so you can cache more.

With the acquisition of Speedb this year, we could ‌reduce the cost for caches of all sizes. At Redis, we’re always analyzing technology trends, and we saw major advancements in solid-state drives (SSDs) that we could leverage to unlock more value for Redis users. Redis Flex is designed to run on DRAM and SSDs, which makes it faster and cheaper than other memory solutions like ElastiCache, Memorystore, and even Community Edition. So you get up to 80% lower costs for not just Redis Software and Redis Cloud, but compared to self-managed Redis, without needing to change your existing data infrastructure.

Redis Flex public preview is coming soon.

To sign up, [book a meeting today](https://redis.io/meeting/).

### Redis 8 is the best version of Redis ever.

Our source-available Community Edition (CE) is used by millions of developers around the world. It’s the foundation for everything we build, but devs have told us it can be hard to get started. There’s so many different options and clients with no clear sign posts on which way is best. Recently, there have been some new forks of Redis, but our Community Edition remains the most advanced and well-supported with loads of new features. Now, it’s faster and much easier to begin.

Redis Stack has become the go-to way for users to get started with Redis, and now all of the features of Redis Stack are integrated into Redis Community Edition. When you get started with Redis Software or Redis Cloud, you get a streamlined, simplified experience.

Redis 8 helps you start faster with everything from Redis 7.4 CE and Redis Stack 7.4.

- **Store, update, and retrieve JSON data** — Directly query JSON data to enable fast, responsive operations and dynamic interactions.
- **Build smarter, faster GenAI apps with vector database** – Harness the world’s fastest vector database. The enhanced Redis Query Engine boosts previous Redis query throughput 16X, making Redis faster than any other vector database we benchmarked.
- **Search and query your data** — Find, filter, aggregate, and sort through millions of records quickly to transform your data into action.
- **Optimize time series data **— Efficiently collect, store, and analyze time series data with high throughput and minimal latency, enabling real-time insights and analytics.
- **Process streams and large data sets** — Extremely fast approximation of counts, frequencies, and rankings with Redis probabilistic data structures.

Redis 8 is coming this fall.

### Boost developer productivity with Redis Copilot and more.

Developers need to build apps faster than ever. To help make devs more efficient, we built Redis Copilot, your virtual assistant for all things Redis. Copilot is free and is now generally available inside [Redis Insight](https://redis.io/insight/). We also are releasing a [Redis supported Visual Studio Code extension](https://marketplace.visualstudio.com/items?itemName=redis.redis-for-vscode) so you can build with Redis easily in your IDE.

Redis Copilot helps you:

- **Retrieve information from docs faster** – Get the answer to questions such as how do I format a query or what is the best process for setting up a cluster.
- **Automatically write code** – Tell Copilot what you are trying to do and Copilot can generate code snippets or commands that accomplish what you asked‌ for.
- **Ask questions about your data** – Make requests in English or other languages and Copilot will write a query to use on your data to answer your question.

Just like many of our customers that are building their own virtual assistants, we built Redis Copilot to provide fast responses at scale. Redis Copilot leverages the Redis real-time data platform and Redis for AI with capabilities like semantic caching, vector database, and rate limiting so that you get fast and accurate responses.

Redis Copilot is now GA. [Get it in Redis Insight today](https://redis.io/insight/#insight-form).

[Redis for VS Code is available now](https://marketplace.visualstudio.com/items?itemName=redis.redis-for-vscode) in the Visual Studio Marketplace.

### Work simpler with Redis Data Integration (RDI), coming soon to Redis Cloud.

We recently [announced Redis Data Integration](/blog/redis-data-integration-now-ga/), which [accelerates your apps](https://redis.io/data-integration/) and provides data federation without needing to redesign your entire data strategy. RDI is coming soon to Redis Cloud and is GA on Redis Software.

Using automated data pipelines, RDI synchronizes data in existing databases with Redis with minimal setup. RDI provides the connection through a single API, so you can simplify development, and make your data more reliable. We’ve done the heavy lifting, so your apps run faster without investing significant time, effort, and money into building your own data pipeline.

[Learn more](https://redis.io/data-integration/) or [book a meeting](https://redis.io/meeting/) to get RDI.

### Build fast apps fast using our latest developments.

I’m very excited for Redis’ second act. We empower you to build GenAI apps while leveraging AI in our own products. It’s a new era of fast, where Redis is an essential part of the new stack for AI. Additionally, to help you get the latest innovations faster, we’ll be shipping smaller releases more frequently, so stay tuned. And most importantly, we’re not sacrificing the past to build this future. Whether you’re using Redis to power fast AI apps, as a high-availability database, or for caching, we’ll help you build fast apps — fast.

To get started, [try Redis here](https://redis.io/try-free/).

Links to resources:

- [Redis for AI](https://redis.io/redis-for-ai)
- [Redis Data Integration](https://redis.io/data-integration/)
- [Redis Insight](https://redis.io/insight/#insight-form)
