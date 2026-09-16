---
title: "What’s new in two: April 2025"
linkTitle: "What’s new in two: April 2025"
url: "/blog/whats-new-in-two-april-2025/"
description: "Click here to view video"
date: 2025-05-01
blogCategories:
- "Tech"
authors:
- "Talon Miller"
lastmod: 2025-10-01
hidden: true
mirrored: true
---

*By Talon Miller, Principal Technical Marketer · Published 1 May 2025 · updated 1 October 2025*

![Blog tile image](/images/site-mirror/f7036ad8ddfde50c979c0e40e7d1fea798ffc7b7-772x552.webp)

[Click here to view video](https://www.youtube.com/embed/xOx7-yKXCjg?si=BtyF4H-Ks5yjavLF)

Welcome to “What’s new in two,” your quick hit of Redis releases you might have missed in the past month. We’re covering the latest developments from April and expanding on what I covered in our latest video. Press play above if you’d rather watch than read. Let’s get started.

April was a huge month at Redis. Our Spring Release brings a new batch of tools and frameworks for Redis for AI, major updates to Redis Cloud, and the release candidate of Redis 8. There is a lot here, so I’ll brief you on the highlights, but if you want to go deeper, check out the [releas](/blog/spring-release-2025/)[e](/blog/spring-release-2025/)[ blog](/blog/spring-release-2025/). Let’s get into it.

## AI

### Redis LangCache

A fully managed semantic cache in private preview that cuts LLM latency and cost by reusing past responses via a simple REST API. No more juggling vector stores or cache invalidation—just plug in and speed up your GenAI apps. Sign up for the private preview [here](https://redis.io/langcache/).

### Vector sets

A new native data type that treats each element as a vector, making similarity search as easy as sorted sets—with hybrid and int8 quantized options for even faster, cleaner lookups. Try it out with the new [RedisVL 0.5.1 here](https://github.com/redis/redis-vl-python/blob/main/docs/user_guide/release_guide/0_5_0_release.ipynb).

### Smarter AI agents with LangGraph & agent memory

Redis now [integrates](https://github.com/redis-developer/langgraph-redis) directly into LangGraph’s memory architecture, using built-in checkpointers for short‑term state, a Store of persistent [vector embeddings](https://redis.io/glossary/vector-embeddings/) for long‑term knowledge, and LangCache for lightning‑fast LLM caching. This keeps your agents from losing context. The open‑source [Redis Agent Memory Server](https://github.com/redis-developer/agent-memory-server) layers on automatic topic extraction, entity recognition, and context summarization, eliminating custom code and letting you focus on building truly agentic workflows. And to orchestrate it all, the new [Redis Cloud Admin API MCP Server](https://github.com/redis/mcp-redis-cloud/) lets you manage your Redis Cloud subscription and agent infrastructure via natural language: spin up databases, adjust settings, or query usage straight from MCP‑compatible clients like Claude Desktop or Cursor.

## Redis Cloud

### Redis Flex

Now in public preview on Cloud Essentials: span RAM + SSD transparently to cache five times more data at the same cost, giving real‑time hits across months of history.

### Redis Data Integration (RDI)

Excited to finally talk about RDI in the cloud. Now in private preview on Redis Cloud Pro, RDI continuously captures every change in your primary database and streams it into Redis in milliseconds, making sure your cache and data store stay perfectly in sync. With built‑in scaling, failure recovery, and visibility, you get enterprise‑grade CDC–powered caching without architecting or operating the pipeline yourself.

### Redis Insight

This is another long-awaited release to the cloud. Now in public preview, Redis Insight on cloud brings your full Workbench experience straight to the browser: run queries, explore keys, and leverage dynamic query autocompletion. With built‑in dashboards, access controls, and automatic updates, you get centralized observability and collaboration for your Redis instances without installing or maintaining any client software.

### Redis Cloud BYOC (Bring Your Own Cloud)

Run Redis Cloud in your own VPC on AWS for full control over networking and data locality, with Redis expertise available.

## Redis 8

Download the fastest Redis ever, with over 30 performance boosts, eight new data types, a 16X faster query engine, and rock‑solid replication. Try the [release candidate](https://hub.docker.com/_/redis) now, with GA dropping in the coming weeks.

And that’s a wrap on one of the biggest months of 2025 for Redis updates. I highly recommend you read the [Spring Release blog](/blog/spring-release-2025/), which goes into more detail on everything we touched on here. Whether you prefer watching or reading, catch more valuable updates in my next two-minute episode. And if you missed [last month’s update](https://youtu.be/wqn1eCzgmXI), two minutes is all you need to catch up. See you next time.
