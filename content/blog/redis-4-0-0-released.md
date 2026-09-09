---
title: "Redis 4.0.0 is Released"
linkTitle: "Redis 4.0.0 is Released"
url: "/blog/redis-4-0-0-released/"
description: "On July 14, Salvatore Sanfilippo (@antirez) announced the availability of the much anticipated Redis 4.0.0 GA release. Redis 4 contains a number of new features including the Modules API, the..."
date: 2017-07-14
blogCategories:
- "Company"
- "Tech"
authors:
- "Tague Griffith"
lastmod: 2025-10-01
hidden: true
---

*By Tague Griffith, Head of Developer Advocacy · Published 14 July 2017 · updated 1 October 2025*

![Blog tile image](/images/site-mirror/d75b51f6d811874093f54bfd83f6615b7f728a6b-91x78.webp)

> Redis 4.0.0 GA is out! My notes here: [https://t.co/1YAiQM98cn](https://t.co/1YAiQM98cn)
— Salvatore Sanfilippo (@antirez) [July 14, 2017](https://twitter.com/antirez/status/885858901564018688)


On July 14, Salvatore Sanfilippo (@antirez) [announced](https://groups.google.com/forum/#!msg/redis-db/5Kh3viziYGQ/58TKLwX0AAAJ) the availability of the much anticipated Redis 4.0.0 GA release. Redis 4 contains a number of new features including the Modules API, the PSYNC2 (improved replication mechanism) engine,, new caching policies, asynchronous deletion operations, microcontroller support, Redis Cluster improvements, memory management improvements and a [host of additional changes and bug fixes](https://raw.githubusercontent.com/antirez/redis/4.0/00-RELEASENOTES).

**Modules**

One of the biggest features in Redis 4.0.0 is the long awaited modules system & Redis memory docker that was announced at RedisConf 2016. The modules system provides an API for extending Redis with dynamically loaded modules primarily in C. The modules API provides multiple levels of API for developers to add new features and functionality to Redis.

With Redis Modules, developers can add new operations to existing data types, introduce new data types, such as [JSON](http://rejson.io/), or extend Redis with new processes like [Search](http://redisearch.io/) or [Neural Network](https://github.com/antirez/neural-redis).

The new API enables developers to build extensions that were either impractical or not performant enough when built with Lua. As mentioned in the [documentation for modules](https://redis.io/docs/latest/develop/reference/modules/) on Redis.io, “Redis modules make [it] possible to extend Redis functionality using external modules, implementing new Redis commands at a speed and with features similar to what can be done inside the core itself.”

**Caching Improvements**

For many Redis users, caching is their introduction to working with Redis and the 4.0.0 release introduces new features to improve the performance of Redis when used for caching. The 4.0.0 release adds least-frequently-used (LFU) maxmemory policies giving users another algorithm for evicting keys when Redis hits the maxmemory threshold. LFU caching provides a better hit to miss ratio than least-recently-used (LRU) caching for many applications.

The implementation of LFU caching in Redis is done through an approximated algorithm to provide accurate estimation of the frequency of a key access without adding a significant amount of memory overhead to track the access counts. Like the current LRU caching policies, LFU caching can be applied only to volatile keys (expire set) or to all keys.

Details of the Redis caching policies can be found in the [Using Redis as an LRU Cache](https://redis.io/topics/lru-cache) article on Redis.io.

**Memory Features**

Two useful features related to memory consumption were also highlighted in Salvatore’s release announcement. They are the addition of a new command for memory introspection and the addition of active memory defragmentation.

The new MEMORY command gives users information into the memory consumption of a Redis instance. The MEMORY USAGE command provides users with the precise amount of memory being used by a given key, while MEMORY DOCTOR provides a framework (similar to the LATENCY DOCTOR command) for observing the overall memory consumption of an instance.

Congratulations to Salvatore (@antirez) for getting the 4.0.0 release to GA. Also thank you to [all of the contributors](https://raw.githubusercontent.com/antirez/redis/4.0/00-RELEASENOTES) involved in the project for their hard work and perseverance.
