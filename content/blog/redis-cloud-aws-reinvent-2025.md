---
title: "We’re bringing a bigger, better Redis Cloud to AWS re:Invent"
linkTitle: "We’re bringing a bigger, better Redis Cloud to AWS re:Invent"
url: "/blog/redis-cloud-aws-reinvent-2025/"
description: "Come see us at booth #1520 for live demos of everything new, as well as giveaways, and Redis swag. Also, don’t miss the Hallucination Hub, our happy hour where we’re bringing AI hallucinations to..."
date: 2025-12-01
blogCategories:
- "Company"
authors:
- "Jon Fritz"
lastmod: 2026-08-13
hidden: true
---

*By Jon Fritz, Chief Product Officer · Published 1 December 2025 · updated 13 August 2026*

![blog post thumbnail - bringing a bigger, better Redis Cloud to AWS re:invent](/images/site-mirror/7345a6bf8c818da9ead4f68a127c667ce209cf66-1200x628.webp)

Come see us at booth #1520 for live demos of everything new, as well as giveaways, and Redis swag. Also, don’t miss the Hallucination Hub, our happy hour where we’re bringing AI hallucinations to life (with food and drinks of course). Check out everything we’re doing at re:Invent [here](https://redis.io/aws-reinvent/).

Customers like Sky, Mercedes, Sephora, and NVIDIA rely on Redis Cloud for their mission critical workloads, and we’re keeping our foot on the gas in delivering new features to enable them. Here’s a summary of what’s new with Redis, with more details below:

- Redis Flex is now in GA in Redis Cloud Pro, giving you up to 75% lower cost on large caches and databases. Flex enables users to choose the mix of RAM and SSD for their database, customizing price and performance with minimal latency impact for many workloads.
- We’re showcasing everything we’ve added to Redis for AI, our integrated package of features and services that power our [performance-leading vector search](/blog/benchmarking-results-for-vector-databases/), semantic caching for lowering LLM costs and increasing agentic app speed, scalable feature store, and agent memory.
- Redis Data Integration (RDI) is now in Public Preview in Redis Cloud Pro (in AWS). It enables customers to sync databases to Redis, accelerating access to fresh data and exposing it via developer-loved Redis data structures.
- Redis Cloud now has several new features enabling faster database scaling and manageability, including smart client handoffs. This feature, which coordinates across Redis’ clients and cloud service, eliminates downtime during planned maintenance and scaling events.
- And we brought significant performance improvements, memory compression, hybrid search, and more to Redis 8.4 - the best version of Redis yet. It’s GA in Redis Open Source today, and will be available in Redis Cloud and Redis Enterprise Software soon.

## Run bigger workloads in Redis Cloud for less with an all-new Redis Flex

AI, machine learning, and database systems require real-time access to massive datasets, but delivering speed at scale is often too costly, driving many use cases out of reach.

Redis Flex introduces an intelligent hybrid memory layer to Redis Cloud that delivers real-time latency for the data that matters most at up to 75% lower cost, while seamlessly managing the rest on flash memory (SSD) with minimal performance impact.

The new Redis Flex:

- Maximizes efficiency, managing hot/warm data more intelligently, freeing additional room in RAM for hot data
- Lets you choose the ratio of RAM to SSD for your database, for the perfect price-to-performance balance for your workload. Select up to 90% SSD for your database, with a minimum size of 250 GB.
- Save up to 75% per GB, enabling new workloads at real-time speed.

Redis Flex provides sub-millisecond latency for hot data and millisecond access for warm data, powering real-time systems across tens of terabytes and is perfect for modern use cases with large datasets like feature stores, real-time personalization, recommendation systems, document databases, and other NoSQL workloads.

[See an interactive demo →](https://redis.io/demo-center/#redis-flex-pro-interactive-demo)

## Build AI apps simply and efficiently on Redis Cloud

Redis Cloud expands its AI offerings with the introduction of LangCache, our fully managed semantic caching service. LangCache caches vector embeddings and LLM responses to reduce inference costs by up to 70% while delivering instant responses.

We’ve also expanded our ML capabilities through the acquisition of FeatureForm and the launch of Redis’s first end-to-end feature store, providing a real-time ML feature pipeline with built-in versioning and governance for faster model iteration and lower infrastructure overhead. Learn more about [LangCache](https://redis.io/langcache/) and Redis’ feature store offering.

As a vector database, Redis helps companies like [Relevance AI](https://redis.io/customers/relevance-ai/) build and scale agentic AI applications up to 99.5% faster. And we’ve continued to expand our vector search capabilities with vector sets: A native Redis data type optimized for high-performance similarity search. Vector sets make it faster and simpler to store and query high-dimensional embeddings, enabling developers to build more efficient AI applications without added complexity.

## Easily sync data into Redis Cloud with RDI

[Redis Data Integration (RDI)](https://redis.io/data-integration/) is now in Public Preview in Redis Cloud Pro (in AWS). RDI makes it easier than ever to bring your data into Redis. It accelerates access to fresh data and exposes it via developer-loved Redis data structures. Developers can more easily build apps with data stored in databases across the enterprise with high performance.

With RDI, you can also modernize your caching architecture. You can stop writing cache invalidation code - every Redis dev knows all too well what it’s like to write:

```python
# Update database
db.update_product(product_id, new_data)
# Transform for cache
cache_data = {
'name': new_data['product_name'],
'price': float(new_data['price']),
'in_stock': new_data['stock_count'] > 0,
'category_rank': calculate_rank(new_data)
}
# Update cache
redis.hset(f"product:{product_id}", mapping=cache_data)
# Update sorted sets, lists, etc…
redis.zadd(f"category:{new_data['category']}", 
{product_id: new_data['price']})
# TODO: Fix this later once outdated prices are served to customers
```

RDI eliminates this. With RDI you can connect your PostgreSQL or MongoDB directly to Redis Cloud, and data syncs automatically so you can avoid cache misses and stale data. It does this by capturing changes, transforming them into Redis data types, and instantly ingesting changed data into Redis.

![rdi-diagram](/images/site-mirror/201bff6a249075763a101c8b7f5c5aab17601552-1457x579.webp)

With the public preview of RDI, Redis Cloud Pro customers can now accelerate their applications by over 75% and realize substantial cost savings. For instance, [Axis Bank](https://redis.io/customers/axis-bank/) saw 4.25x better performance while saving over $80K.

## A more scalable and resilient Redis Cloud with hosted compute or in your VPC

Recent updates make Redis Cloud more resilient, performant, and easier to manage.

- New smart client handoffs keeps Redis apps running smoothly through planned maintenance, upgrades, and scaling by coordinating reconnects directly with the official Redis client libraries. Get the best of Redis reliability, upgrading without disruption to critical workloads.
- Faster and smoother database scaling powered by underlying innovations in our cloud fabric. And, even more to come driven by Redis’ atomic slot migration feature set in Redis 8.4.
- Redis Cloud now utilizes AWS Graviton-based hardware, offering improve performance and memory efficiency.

The result: faster scaling, smoother upgrades, and no application interruptions, even during large-scale cluster changes.

Redis Cloud also offers flexible deployment options. You can use Redis Cloud’s hosted compute, or [Bring Your Own Cloud (BYOC)](https://redis.io/docs/latest/operate/rc/subscriptions/bring-your-own-cloud/) which launches and manages the Redis platform on EC2 instances in your Amazon VPC. With BYOC, data never leaves your VPC, and you can also leverage your Amazon EC2 discounts directly.

Redis gives flexibility beyond AWS, too. You can also run the Redis platform anywhere—[fully managed ](https://redis.io/cloud/)or [self-managed](https://redis.io/software/), cloud or hybrid—without lock-in. Redis is available across [AWS](https://redis.io/partners/aws/) (EKS, EC2), [Azure](https://redis.io/partners/azure/), [Google Cloud](https://redis.io/partners/google/), and on-premises, giving you the freedom to deploy Redis where you want it.

## Redis 8.4, our most advanced version yet, GA in Redis Open Source

Built to streamline scaling, boost performance, and power new AI use cases, Redis 8.4 is now available in Redis Open Source and coming soon to Redis Cloud, with major new enhancements, including:

- **Performance improvements: **With multi-threaded I/O, improved memory handling, and smarter JSON storage that deliver over 30% higher throughput and up to 91% lower memory use.
- **Atomic Slot Migration (ASM):** Enables easier, more reliable cluster scaling.
- **Hybrid Search:** Combines full-text and vector results in one query, powering more accurate AI, RAG, and semantic search experiences.
- **Atomic key operations**: Provide safer, script-free key updates and expirations.
- **Stream enhancements**: Allow clients to process new and pending messages in a single step.

Read more about Redis 8.4 in our deep dive here.

## Catch up on the latest from Redis

In case you couldn't tell, we’ve been busy innovating. If you missed the latest announcements at Redis Released and would like to learn more, check out [redis.io/new](https://redis.io/new).

And if you’ll be in Las Vegas for re:Invent, don’t forget to visit us at booth #1520 for live demos, theater sessions, swag, and a whole lot of fun. Learn more [here](https://redis.io/aws-reinvent/).
