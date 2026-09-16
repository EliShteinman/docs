---
title: "What’s new in two – November 2025 edition"
linkTitle: "What’s new in two – November 2025 edition"
url: "/blog/whats-new-in-two-november-2025-edition/"
description: "Click here to view video"
date: 2025-12-19
blogCategories:
- "Tech"
authors:
- "Talon Miller"
lastmod: 2026-06-01
hidden: true
mirrored: true
---

*By Talon Miller, Principal Technical Marketer · Published 19 December 2025 · updated 1 June 2026*

![What’s new in two – November 2025 edition](/images/site-mirror/0b14b14bf3288dadd637a8e56417744bd94071ba-1200x628.webp)

[Click here to view video](https://www.youtube.com/embed/oh_vNGnWRUQ?si=HYc8lvAPeyOTodth)

Welcome to “What’s new in two,” your quick hit of Redis releases you might have missed in the past month. If you blinked, you missed it—so here’s the recap. We’re covering the latest developments from November and expanding on what I covered in our latest video. Press play to watch it instead.

## Redis 8.4 is now GA in open source

Redis 8.4 is now generally available and introduces new levels of performance, memory efficiency, and developer simplicity. It also adds faster hybrid search for building smarter AI applications—and pushes Redis further as the context engine for real-time and agentic workloads.

###### Hybrid search for smarter retrieval

The new FT.HYBRID command combines full text and vector similarity search in one query. It merges meaning and match into a single ranked result, delivering faster, more relevant retrievals for AI use cases. The update also adds support for Reciprocal Rank Fusion (RRF), improving semantic accuracy when combining multiple ranking signals.

###### Performance and efficiency gains with JSON

Redis 8.4 delivers up to a 30% throughput boost for caching workloads and introduces multi-threaded I/O handling for distributed queries, improving performance by as much as 4.7x for large search operations. It also makes it more viable than ever to use JSON with vector search—now up to 92% more memory-efficient for numeric arrays and 37% for short string arrays—making it practical to persist vectors directly in JSON. Together with the Redis Query Engine, these enhancements bring efficient, memory-friendly semantic search to the core of Redis.

###### Smarter stream processing

Stream handling got a major upgrade. A new XREADGROUP extension lets you consume both idle pending and new messages in a single command, simplifying recovery logic and reducing operational overhead. That means faster, more resilient event-driven apps with less code to manage.

Together, these features reduce the need for scripts and client workarounds, making Redis more predictable in production.

Redis 8.4 is available now in Redis Open Source and will be coming soon to Redis Cloud and Redis Software.

## Redis 8.2 in Redis Cloud GA

Redis 8.2 is now generally available in Redis Cloud, bringing faster performance, smarter scaling, and native AI-ready data structures. This release delivers major gains in throughput and responsiveness while simplifying how developers build and manage cloud workloads.

###### Faster scaling and stability

Redis Cloud now delivers up to 45% higher throughput, 70% lower latency, and 30% faster scaling. Predictive scaling, quicker shard rebalancing, and improved cross-region replication keep workloads fast and stable under any demand.

###### Enhanced query engine

Complex queries now run up to twice as fast with improved indexing and vector compression for structured and vector data. These upgrades make Redis Cloud an even stronger foundation for retrieval-augmented generation and other AI-driven workloads.

###### Vector Set for AI

A new native Vector Set data type lets developers run semantic search, recommendations, and RAG pipelines using simple Redis commands. It is built for the cloud, with performance tuned for large-scale AI applications.

###### Everything included by default

All Redis modules, including Search, JSON, and Graph, are now bundled automatically in every Redis Cloud database. Developers can build with the full Redis toolkit right out of the box.

Redis 8.2 on Cloud reinforces Redis as the fastest, most complete managed platform for real-time and AI applications.

## Redis 8.0.2 in Redis Software GA

Redis Software 8.0.2 is now generally available, bringing faster performance, better reliability, and smarter scalability for enterprise customers running Redis in self-managed or on-prem environments.

###### Performance and reliability upgrades

This release delivers up to 40% faster scaling, 78% lower latency, and 35% less memory used during replication. The new replication mechanism reduces sync times and memory use for smoother failover and stability under load.

###### Redis Flex upgraded

The latest Redis Flex version boosts throughput by up to 30% and improves RAM and Flash utilization for large multi-terabyte datasets. It also introduces a more robust engine to handle complex enterprise workloads.

###### New Redis 8.2 engine

Redis Software 8.0.2 now includes the Redis 8.2 engine with all its upgrades. The Redis Query Engine brings up to 144% higher query rates with vector compression and improved reliability checks. The new Vector Set data type enables simple and fast semantic search operations using familiar Redis commands.

###### Enterprise-grade security

Enterprises can now use their own trusted certificates for internode encryption with support for customer-managed CAs. This gives full control over compliance and internal security requirements.

Redis Software 8.0.2 delivers blazing speed, stronger reliability, and AI-ready infrastructure for modern enterprise workloads.

## Smart client handoffs

Smart client handoffs coordinate reconnects and timeouts directly in the client libraries so your applications keep running through maintenance events and version upgrades. The feature automatically rebinds clients to the new endpoints and adjusts timeouts during transitions, avoiding disconnects, failed requests, and retry storms.

No special orchestration or application logic is required. Official Redis clients like redis-py, Lettuce, go-redis, and node-redis handle the entire process, keeping in-flight operations intact.

Smart client handoffs are enabled by default in Redis Cloud Essentials and Pro databases. They can also be activated in Redis Software 8.0.2 through the REST API.

This update makes routine maintenance truly routine, giving developers resilient, always-on applications with no extra code to manage. Learn more on the [docs](https://redis.io/docs/latest/develop/clients/sch/).

## New course: Semantic Caching for AI Agents on [DeepLearning.AI](http://deeplearning.ai)

In this new short course from Redis and deeplearning.ai, you’ll build a working semantic cache that measures hit rate, precision, and latency, then improve accuracy with techniques like fuzzy matching, LLM validation, and cross-encoders. You’ll also learn how to integrate caching directly into your AI agent so it gets faster and more efficient over time.

The course is led by [Tyler Hutcherson](https://www.linkedin.com/in/tyler-hutcherson/), Applied AI Engineering Lead, and [Iliya Zhechev](https://www.linkedin.com/in/iliya-zhechev/), Senior Research Engineer at Redis. [Enroll now](https://www.deeplearning.ai/short-courses/semantic-caching-for-ai-agents/?utm_campaign=29463680-redis-launch&utm_content=357865481&utm_medium=social&utm_source=linkedin&hss_channel=lcp-18246783) and get your feet wet with semantic caching.

That’s a wrap on November updates. And if you missed [last month’s update](https://youtu.be/eZgTtMguUPU), two minutes is all you need to catch up. Whether you prefer watching or reading, catch more valuable updates in my next two-minute episode. See you next time.
