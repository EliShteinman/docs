---
title: "What’s new in two: August 2025 edition"
linkTitle: "What’s new in two: August 2025 edition"
url: "/blog/whats-new-in-two-august-2025-edition/"
description: "Click here to view video"
date: 2025-09-10
blogCategories:
- "Tech"
authors:
- "Talon Miller"
lastmod: 2025-09-10
hidden: true
---

*By Talon Miller, Principal Technical Marketer · Published 10 September 2025*

![Redis](/images/blog/870188c648a0df252c650ba7c6fb9c954b5aab84-772x552.webp)

[Click here to view video](https://www.youtube.com/embed/nKVN8ZuL1bM)

Welcome to “What’s new in two,” your quick hit of Redis releases you might have missed in the past month. We’re covering the latest developments from August and expanding on what I covered in our latest video. Press play above if you’d rather watch than read. Let’s get started.

## Redis Cloud

There were a number of Redis Cloud updates in August that are worth looking into. I’ll highlight them here in this section.

## Redis 8 on Redis Cloud for Essentials tier in Public Preview

Redis 8 is now in public preview on the Cloud Essentials tier, bringing up to 78% lower latency, faster replication, and native vector sets for similarity search.

This early release lets customers spin up new databases to test Redis 8’s performance, query engine upgrades, and new data structure capabilities ahead of GA. Check out [the docs](https://redis.io/docs/latest/develop/whats-new/8-0/).

## Other Redis Cloud Previews

### Customer Managed Keys

Enterprise customers can now bring their own encryption keys for persistent storage, giving them greater control over data security and compliance inside Redis Cloud.

### PrivateLink Resource Endpoints

With PrivateLink support, you can now connect to your Redis Cloud databases without exposing your application VPC, keeping latency and cost low.

### Active-Active support on Bring Your Own Cloud

Bring Your Own Cloud (BYOC) deployments now support Active-Active geo-replication, enabling globally distributed Redis deployments with local latency and seamless failover.

## Redis for AI Updates

Redis continues to invest heavily in the AI ecosystem, and August proves that with the updates below.

## LangGraph Redis Checkpoint 0.1.0

[LangGraph Redis Checkpoint](https://github.com/redis-developer/langgraph-redis) 0.1.0 is here with a performance-driven redesign. By denormalizing storage, adopting sorted sets, and aggressive pipelining, checkpoint retrieval is now up to 12x faster and listing checkpoints is 30x faster, making Redis the high-performance backbone for production AI agents.

## New RedisVL Integrations with Cognee, AutoGen, and A2A

[Cognee now uses RedisVL](/blog/build-faster-ai-memory-with-cognee-and-redis/) to power vector-backed long-term memory for AI assistants, while AutoGen and A2A integrate Redis for reliable task queues, event streams, and push notification management. Together, these integrations make Redis the go-to infrastructure for agent memory and coordination. Check out [the integration](https://github.com/topoteretes/cognee-community/tree/main/packages/vector/redis).

AutoGen now supports RedisMemory, letting agents store and retrieve context directly from Redis. That means faster, consistent answers with Redis as the unified memory layer for RAG and long-running agents. Check out an [example notebook](https://github.com/microsoft/autogen/blob/c715876a9599453037a9ba1dd01b5335fb2118fd/python/docs/src/user-guide/agentchat-user-guide/memory.ipynb#L228).

Lastly, [a2a-redis](https://github.com/redis-developer/a2a-redis), a package that plugs Redis into the Agent-to-Agent (A2A) Python SDK. It brings persistent task storage, reliable event queues with Streams, low-latency broadcasting with Pub/Sub, and push notification configuration—all backed by Redis. With built-in consumer group strategies, developers can now build agents that coordinate, recover from failures, and share work seamlessly, powered by Redis.

## Redis and LMCache

LMCache is an open-source KV cache library that accelerates LLM serving by reusing precomputed attention chunks. With Redis as its default backend, LMCache delivers faster inference, lower GPU costs, and scalable chunk reuse—a huge win for RAG, chatbots, and multi-turn applications. Check out the [LMCache docs](https://docs.lmcache.ai/kv_cache/redis.html) or [Repo](https://github.com/LMCache/LMCache).

## Redis Open Source 8.2 Generally Available

Redis 8.2 is now generally available, delivering up to 49% higher throughput, 35% lower command latency, and major memory savings of up to 67% for JSON and integer data. New stream commands (XACKDEL, XDELEX) simplify consumer group logic, while four new bitmap operators enable more powerful targeting and analytics use cases. Check out [the release](https://github.com/redis/redis/releases/tag/8.2.0).

That’s a wrap on August updates. Whether you prefer watching or reading, catch more valuable updates in my next two-minute episode. See you next time.
