---
title: "Redis 8.2 in Redis Open Source is GA and brings more performance, efficiency, and new commands"
linkTitle: "Redis 8.2 in Redis Open Source is GA and brings more performance, efficiency, and new commands"
url: "/blog/redis-82-ga/"
description: "We’re excited to announce the general availability release of Redis 8.2 in Redis Open Source, building on the momentum of Redis 8 with faster performance, more memory optimizations, and developer-..."
date: 2025-08-08
blogCategories:
- "Tech"
authors:
- "Lior Kogan"
- "Paulo Sousa"
- "Moti Cohen"
lastmod: 2026-06-01
hidden: true
---

*By Lior Kogan, Paulo Sousa, Moti Cohen · Published 8 August 2025 · updated 1 June 2026*

![Redis 8.2 in Redis Open Source is GA and brings more performance, efficiency, and new commands](/images/site-mirror/32002e84e88239d1d44bcd732c7c24bb696358e7-772x552.webp)

We’re excited to announce the general availability release of Redis 8.2 in Redis Open Source, building on the momentum of Redis 8 with faster performance, more memory optimizations, and developer-friendly enhancements that make Redis even better at what it does best–making data real time for AI agents & apps.

Redis 8.2 introduces over 14 new performance & efficiency improvements compared to Redis 8 including up to 35% faster commands, up to 49% more operations per second throughput, and a new internal implementation for storing keys and JSON that reduces memory footprint by up to 67%.

This release also simplifies your development workflows with new streams data structure commands that the community has been asking for and adds powerful new BITOP command operators that enable more sophisticated operations in a single command.

## Performance that pushes boundaries

### Up to 35% reduction in command latency

We've optimized over 70 commands in Redis 8.2 to run faster than in Redis 8.0. The BITCOUNT command now runs 35% faster, while list operations like LINSERT, LREM, and LPOS see more than 25% latency reduction each. An additional 17 commands show more than 5% improvement, and 52 more commands demonstrate over 2% latency reduction.

![Redis 8.2 Comparison Chart](/images/site-mirror/414d2351fc68b4e7f24fd24d2bd478e0af4b8eef-1530x954.webp)

These aren't just numbers—they translate to real-world performance gains for the vast majority of use cases.

### Up to 49% more throughput to exceed 1M ops/sec

Building on our I/O threading capability, we've further reimagined how Redis handles concurrent operations. With 8 I/O threads enabled, Redis 8.2 achieves up to 49% throughput improvement compared to Redis 8.0 for a typical caching workload ratio of 20% writes and 80% reads.

![Up to 49% more throughput to exceed 1M opssec](/images/site-mirror/a6e4d5b78377a7157577097fee909333750e963d-1600x995.webp)

We're exceeding 1 million operations per second on a single Redis 8.2 instance for mixed write and read workloads—a milestone that showcases how far we've pushed the boundaries of in-memory performance.

### Up to 37% memory reduction for short string keys

Redis 8.2 introduces a fundamental change to how we store key-value data. We now use a unified data structure called key-value object (kvobj) that tightly packs the key name, short values, and optional time-to-live (TTL) into a single memory allocation.

Instead of maintaining separate pointers for keys, values, and TTLs, Redis now uses a single pointer to the unified kvobj from both the values and TTL hash tables. For hash slots with a single key, we can even avoid allocating an entry entirely.

![Before 8.2 & Release 8.2](/images/site-mirror/3d788e41b23117f8a4a2b26d2fb813dc2d8f8e71-1033x427.webp)

This architectural change from multiple to single memory allocation per key delivers 25% to 37% memory reduction for short strings along with:

- Reduced pointer dereferences to improve performance
- Optimized cache line utilization
- Streamlined key expiration handling

### Up to 67% memory reduction for JSON numeric values

The JSON data structure, introduced in Redis 8, has a new memory optimization based on its underlying properties.

JSON documents often share a common schema so object member names are frequently repeated. A similar observation is also seen within a JSON document, such as with an array of objects. Redis only stores string values once and creates pointers for the other occurrences.

In Redis 8.2, we’ve found a more efficient way to store integers and floats in JSON, which saves 25% to 67% in memory.

| Numeric Type | Redis 8 - Memory consumed | Redis 8.2 - Memory consumed | Reduction in memory consumption |
|---|---|---|---|
| Small integer [-2^23, 2^23-1] | 12B | 8B | 25% |
| Integer [-2^60, 2^60-1] | 24B | 8B | 67% |
| Large integer [-2^63, 2^64-1] | 24B | 16B | 33% |
| 32-bit floating point | 24B | 8B | 67% |
| 64-bit floating point | 24B | 16B | 33% |

These optimizations are particularly impactful for JSON documents with many numeric fields. Financial records and analytics datasets can see dramatic memory reductions.

## New capabilities that simplify workflows

### Streams: simplifying working with multi-consumer groups

Managing Redis streams with multiple consumer groups has historically required complex app logic to ensure messages are only deleted after being acknowledged on all consumer groups. This logic can be quite complex to implement.

In Redis 8.2, we introduce a way to greatly simplify the application’s logic. We added 2 powerful new commands **XACKDEL** and **XDELEX** then also extended 2 existing commands that dramatically simplify this workflow.

You can learn more about these new stream commands [here](/blog/redis-82-streams-bitmap/).

### Bitmap: new logical operators for the BITOP command

Redis 8.2 adds 4 new logical operators to the BITOP command, enabling more sophisticated set operations in a single command:

- **DIFF**: Members of X but not in any of Y1, Y2, ...
- **DIFF1**: Members of one or more Y sets but not in X
- **ANDOR**: Members of X that are also in at least one Y set
- **ONE**: Members in exactly one of the given bitmaps

These new operators are particularly valuable for membership use cases, like whether a player is located within a specific segment of the map in a game or to store whether a person should be given an advertisement campaign.

You can learn more about these new logical operators for the BITOP command [here](/blog/redis-82-streams-bitmap/).

## Building on Redis 8.2

Redis 8.2 maintains full compatibility with all the client libraries you’re already using that’s supported by us. Whether you’re using [Jedis](https://github.com/redis/jedis), [Lettuce](https://github.com/redis/lettuce), [go-redis](https://github.com/redis/go-redis), [node-redis](https://github.com/redis/node-redis), [NRedisStack](https://github.com/redis/NRedisStack), or [redis-py](https://github.com/redis/redis-py), you can upgrade to Redis 8.2 and immediately benefit from these performance improvements and new features.

The Redis OM client libraries and [RedisVL](https://docs.redisvl.com/en/latest/) for AI apps are also fully compatible, ensuring your object mapping and vector search workflows continue to work seamlessly.

[Redis Insight](https://redis.io/insight/) and Redis for VS Code are also fully compatible with Redis 8.2.

## Getting started with Redis 8.2

Redis 8.2 in Redis Open Source is generally available through all standard distribution channels:

- Download an Alpine or a Debian Docker image from [Docker Hub](https://hub.docker.com/_/redis)
- Install using snap - [instructions](https://github.com/redis/redis-snap), [Snapcraft](https://snapcraft.io/redis)
- Install using brew - [instructions](https://github.com/redis/homebrew-redis)
- Install using RPM - [instructions](https://github.com/redis/redis-rpm)
- Install using Debian APT - [instructions](https://github.com/redis/redis-debian)

Redis 8.2 is coming to Redis Cloud and Redis Software soon as part of Redis Released in 18 cities. Join a Redis Released event near you to find us in-person and get an early preview by registering [here](https://redis.io/released/?utm_source=marketo&utm_medium=email&utm_campaign=2025-[%E2%80%A6]ross-promo&utm_content=ev-2025-fy26-redis_released_tier_1_events).

Ready to see how the fastest feels? Upgrade to Redis 8.2 today.
