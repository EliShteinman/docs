---
title: "Redis 8 is now GA, loaded with new features and more than 30 performance improvements"
linkTitle: "Redis 8 is now GA, loaded with new features and more than 30 performance improvements"
url: "/blog/redis-8-ga/"
description: "We’re excited to announce the general availability release of Redis 8."
date: 2025-05-01
blogCategories:
- "Company"
- "Product Releases"
- "Tech"
authors:
- "Pieter Cailliau"
- "Lior Kogan"
- "Charlie Wang"
lastmod: 2026-06-01
hidden: true
---

*By Pieter Cailliau, Lior Kogan, Charlie Wang · Published 1 May 2025 · updated 1 June 2026*

![Blog tile image](/images/blog/c2017dcedf5fb40bcda9736a84d8b19f9228804c-1544x1104.webp)

We’re excited to announce the general availability release of Redis 8.

Redis 8 is the most performant and scalable version of Redis yet. It has over 30 performance improvements, including up to 87% faster commands, up to 2x more operations per second throughput, up to 18% faster replication, and delivery of up to 16x more query processing power with Redis Query Engine.

This release adds 8 more data structures, including vector set (beta), JSON, time series, and five probabilistic structures, including Bloom filter, cuckoo filter, count-min sketch, top-k, and t-digest (some previously available as separate Redis modules). These new data structures help you solve your current use cases better and build for the next generation of fast and real-time apps.

Additionally, we’ve changed the name of our free product from Redis Community Edition to Redis Open Source to reflect the addition of AGPLv3 as a licensing option.

*(interactive chart, not available offline)*

## One Redis

Over the years, we have created new Redis modules that help you build real-time apps for web, mobile, and GenAI faster. However, we’ve heard from many of you how it often becomes confusing figuring out how to get started with modules, especially with matching the right module version to the Redis version. The introduction of Redis Stack helped and saw significant adoption but also introduced fragmentation in the community.

Today, we’re combining our Redis Stack and community offerings into a single Redis Open Source distribution. All the modules are already included in this package. Going forward, Redis Open Source delivers the same feature set to you everywhere. When you use Redis Open Source, you know you’re always getting the latest and best of Redis with the full suite of capabilities that are available to the community.

These are some of the features and capabilities that come packaged in Redis 8 in Redis Open Source.

**Vector set data structure [beta]**
We are excited to announce vector set, a new data type for vector similarity search. Developed by Salvatore Sanfilippo, the original creator of Redis, vector set takes inspiration from sorted set, another one of Redis’s fundamental data types known for its efficiency in handling ordered collections. Vector set extends the concept of sorted set to allow the storage and querying of high-dimensional vector embeddings, enhancing Redis for AI use cases that involve semantic search and recommendation systems. Vector set complements the existing vector search capability in the Redis Query Engine.

The vector set data type is available in beta. We may change, or even break, the features and the API in future versions. We are open to your feedback as you try out this new data type whilst we work towards general availability.

**JSON data structure**
The JSON data structure improves how you solve for traditional Redis use cases. It also lets you manage sessions more easily, like by using arrays and objects to model hierarchical session data. In Redis 8, the JSON data structure lets you store JSON documents as keys in Redis. Redis provides commands to retrieve and manipulate documents using the JSONPath language for more granular and efficient access to specific elements. Redis also supports atomic updates so you can make modifications to parts of a JSON document without having to retrieve the entire document first.

**Time series data structure**
The time series data structure simplifies how you tackle use cases with fast changing timestamped data such as those from IoT sensors, system telemetry, stock prices, commodity prices, foreign exchange rates, and crypto prices. In Redis 8, it’s very fast to get and use time series data. This is because Redis uses very efficient compression algorithms to keep the data memory footprint low. In addition, compaction (downsampling) rules can be defined for efficient long-term storage.

**Probabilistic data structures**
Probabilistic data structures let you answer common questions about your data streams and large datasets much faster. The significant advantages given in terms of efficiency in memory usage and processing speed is a trade-off with absolute accuracy. In Redis 8, in addition to **HyperLogLog**, which allows estimating the cardinality of a set, there are now 5 more probabilistic data structures:

- **Bloom** filter and **Cuckoo** filter—for checking if a given value has already appeared in a data stream
- **Count-min** **sketch**—for estimating how many times a given value appeared in a data stream
- **Top-k**—for finding the most frequent values in the data stream
- **t-digest**—for querying which fraction of the values in the data stream are smaller/larger than a given value.

**Redis Query Engine**
The Redis Query Engine unlocks fast data access beyond a key lookup. With Redis 8 you can create a secondary index of data that resides in hashes and JSON data structures. Some of the most common ways to use the Redis Query Engine include for vector search, data queries that return exact matches by a criteria or tag, and search queries that return the best matches by keywords or semantic meaning. The query engine also supports features like stemming, synonym expansion, and fuzzy matching for more comprehensive search results. Vector embeddings that represent data points within hashes or JSON documents can also be stored so the query engine in Redis 8 can be leveraged for vector similarity search.

**Access Control Lists (ACLs)**
While Redis 8 is secure by default, Access Control Lists (ACLs) allow more fine-grained security control. With ACLs, you can define which users can connect, what commands they can perform, and which keys they can access. This helps you restrict unauthorized access and maintain data integrity in your Redis environment**. **In Redis 8, we introduce new ACL categories for the new data structures. Existing ACL categories such as @read and @write now include commands that support the newly included data structures.

**New commands building on Redis 7.4**
When you build on Redis 8, you also get all the new features and capabilities that came in Redis 7.4, including our [introduction](/blog/announcing-redis-community-edition-and-redis-stack-74/) of hash field expiration. One of the most frequently requested feature (e.g., [#13345](https://github.com/redis/redis/issues/13345), [#13459](https://github.com/redis/redis/issues/13459), [#13577](https://github.com/redis/redis/pull/13577)), you can find 3 new hash commands in Redis 8:

- HGETDEL – Get hash fields and delete them
- HGETEX – Get hash fields and optionally set their expiration time
- HSETEX – Set hash fields and optionally set their expiration time

## AGPL is now a licensing option

Redis 8 is available in Redis Open Source under the open source [AGPLv3](https://www.gnu.org/licenses/agpl-3.0.en.html) license in addition to the [dual RSALv2 and SSPLv1 licenses](/blog/redis-adopts-dual-source-available-licensing/) we moved to last year. We heard from some customers that it is easier for them to operate under an OSI-approved license, so we’ve added that option. [Read more here](/blog/agplv3/), or visit [redis.io/legal/licenses/](https://redis.io/legal/licenses/).

## Significant performance improvements

Redis 8 introduces over 30 performance improvements for both single-core and multi-core environments, delivering the greatest leap in performance in a single new Redis version.

Based on anonymized statistics from our tens of thousands of existing customers and users, we’ve invested in what we’ve seen you use the most. That means for many of you, you will see improvements in performance that provide the greatest uplift and value in how you use Redis when upgrading to Redis 8.

**Up to 87% reduction in command latency**
We have reduced the latency per command in Redis 8 for a large set of commands compared to Redis 7.2.5. In our benchmark of 149 tests, 90 commands run faster with less latency. The p50 latency reduction ranges from 5.4% to 87.4%. The vast majority of apps built with Redis 8 will see significant performance improvements.

![Redis 8.0 Blog Post Graph](/images/blog/66f490792b7b9fc89fa9afe24fcbdc2ad850911b-1116x676.webp)

More details are available on the [8.0-M02 blog post](/blog/redis-8-0-m02-the-fastest-redis-ever/).

**2x more ops per second throughput by enabling multithreading**
Since Redis 6, we have supported I/O threads to handle client requests, including socket reads/writes and command parsing. However, the previous implementation does not fully capture the performance potential.

In Redis 8, we introduce our new I/O threading implementation. You can enable it by setting the io-threads configuration parameter. The default value is 1. When the parameter is set to 8 on a multi-core Intel CPU, we’ve measured up to 112% improvement in throughput. Exact throughput improvements will vary, contingent on the commands being executed.

**Up to 35% less memory used for replication**
In Redis 8, we are introducing a new replication mechanism. During replication, we initiate two replication streams simultaneously: one stream for transferring the primary node and the other for the stream of changes that happen in the interim. The second phase is no longer blocked waiting for the first phase to complete.

![Redis 8.0 Blog Image](/images/blog/91ce9076c6cbafea5a8b8d3ab29166de6bc7933a-1600x898.webp)

In our tests, we conducted a full synchronization of a 10 GB dataset with an additional stream of 26.84 million write operations that yields 25 GB of changes during the replication. With the new replication mechanism, **the primary can handle write operations at a 7.5% higher average rate during replication**. Replication also takes 18% less time and the **peak replication buffer size on the primary node is 35% lower**.

More details are available on the [8.0-M03 blog post](/blog/redis-8-0-m03-is-out-even-more-performance-new-features/).

**Up to 16x more query processing power with horizontal & vertical scaling**
Redis 8 comes with a Redis Query Engine that can scale in two new ways that were previously exclusive to Redis Cloud and Redis Software. The first way enables querying in clustered databases, allowing you to manage very large data sets with indices and support for higher throughput of reads and writes by scaling out to more Redis processes. The second way allows you to add more processing power to scale your query throughput vertically, unlocking up to 16 times more throughput than before.

When both ways to scale are enabled, Redis 8 is the fastest vector database on the market, and you have access to it for free through Redis Open Source. We [demonstrate](/blog/redis-8-0-m02-the-fastest-redis-ever/) this scale and how you can perform vector search queries at real time on 1 billion 768-dimensional vector embeddings at high precision.

![Redis 8.0 Chart](/images/blog/c1b68f3dd7f58714ebd99bb754e196827b289856-1600x976.webp)

At a billion-vector scale, with real-time indexing, Redis 8 can sustain 66,000 vector insertions per second for an indexing configuration that allows precision of at least 95%. For indexing configurations that result in lower precisions, Redis 8 can sustain higher ingestion rates of 160,000 vector insertions per second. Throughput can be increased further by using more servers. For high precision queries, we can see that larger HNSW indices improves the search quality at the expense of latency. We reach 90% precision with a median latency including RTT of 200ms, and 95% precision with a median latency including RTT of 1.3 seconds for the top 100 nearest neighbors, while executing 50 search queries concurrently.

## Building on Redis 8

**Open source client libraries**
Redis 8 is easy to start building your app on and is fully supported by the most performant and reliable open source client libraries that you are using today. To learn more, please reference our [documentation](https://redis.io/docs/latest/develop/clients/) for quick start guides for your favorite programming languages:

- [Jedis](https://github.com/redis/jedis), for Java synchronous programming
- [Lettuce](https://github.com/redis/lettuce), for Java asynchronous programming
- [go-redis](https://github.com/redis/go-redis), for Golang users
- [node-redis](https://github.com/redis/node-redis), the reference library for Node.js
- [NRedisStack](https://github.com/redis/NRedisStack), the C# library that offers the stability of StackExchange.Redis and supports for new data structures in Redis 8
- [redis-py](https://github.com/redis/redis-py), for the Python programming language

**Object mapping libraries**
If you want to map your data with object mapping techniques, the [Redis OM client libraries](https://redis.io/docs/latest/develop/clients/om-clients/) are available to help you. They will help you model your objects, add schema validation, and store them in Redis 8.

**GenAI use cases**
For the GenAI apps and use cases you’re building, we make it easier by offering [Redis vector library (RedisVL)](https://redis.io/docs/latest/integrate/redisvl/) together with Redis 8 as a simple yet powerful solution to work with vectors. With easy integrations to LLMs for your AI apps or to perform semantic search, RedisVL includes many capabilities that make new GenAI features fast and possible, such as semantic caching, vectorizers, and semantic routing.

**Developer environment**
Redis Insight and Redis for VS Code are visual tools that let you explore data, design, develop, and optimize your applications while also serving as a platform for Redis education and onboarding. Redis Insight specifically integrates Redis Copilot, a natural language AI assistant that improves the experience when working with data and commands. Redis 8 is fully compatible with Redis Insight and Redis for VS Code.

## Upgrading to Redis 8

If you are running on an older version such as Redis 6 and Redis 7, we encourage you to upgrade to Redis 8 to take advantage of new performance improvements and capabilities. We’re committed to keeping Redis 8 in Redis Open Source free so you can uplevel how you solve for use cases including caching, session management, leaderboards, and matchmaking.

More information on how to upgrade to Redis 8 is available [here](https://redis.io/docs/latest/operate/oss_and_stack/install/upgrade/).

If you are a current user of Redis Stack, currently supported features and capabilities that were exclusive to Redis Stack can be found on Redis Open Source. We also encourage you to upgrade to Redis Open Source as we will stop releasing patches for Redis Stack 6.2, 7.2, and 7.4 on September 15, 2025.

New features found in Redis Open Source will be fully coming to our other offerings later this year.

## Getting started with Redis 8 today

Redis 8 is generally available on Redis Open Source and can be installed through the following channels as they become available in the coming days:

- Download an Alpine or a Debian Docker image from [Docker Hub](https://hub.docker.com/_/redis)
- Install using snap – [instructions](https://github.com/redis/redis-snap), [Snapcraft](https://snapcraft.io/redis)
- Install using brew – [instructions](https://github.com/redis/homebrew-redis)
- Install using RPM – [instructions](https://github.com/redis/redis-rpm)
- Install using Debian APT – [instructions](https://github.com/redis/redis-debian)
