---
title: "Redis 4.0 Now Available on Redis Enterprise"
linkTitle: "Redis 4.0 Now Available on Redis Enterprise"
url: "/blog/redis-4-0-availability-redis-enterprise/"
description: "The much-awaited Redis version 4.0 is here! Here at Redis we make an ongoing effort to ensure that our customers can enjoy all the latest and greatest features of Redis."
date: 2017-09-26
blogCategories:
- "Company"
- "Tech"
authors:
- "Aviad Abutbul"
lastmod: 2025-03-27
hidden: true
mirrored: true
---

*By Aviad Abutbul, Senior Director of Product Management · Published 26 September 2017 · updated 27 March 2025*

![Blog tile image](/images/site-mirror/3f32e3906bd6e8ac44fcac75dd08e2fba9cc3760-600x600.webp)

The much-awaited **Redis version 4.0** is here! Here at Redis we make an ongoing effort to ensure that our customers can enjoy all the latest and greatest features of Redis.

We are excited to announce that our latest version of **Redis Enterprise**, our core engine that powers **Redise Cloud** and **Redise Pack** products, now supports the latest release of Redis – version 4.0.

#### What’s new in Redis version 4.0

Redis 4.0 release adds several significant enhancements including:

- **Redis Modules** – the most talked about ability to extend Redis functionality by directly hooking into Redis core and extending it
- **Async non blocking delete operations** – new [**‘UNLINK’**](https://redis.io/commands/UNLINK) command is same as **‘DEL’** but working in a non-blocking way. To get the same with **‘FLUSHDB’** and **‘FLUSHALL’** use the new [**‘ASYNC’**](https://redis.io/commands/flushall) flag
- Improvements to existing eviction policies and a **brand new eviction policy** – **LFU** (Least Frequently Used)
- **Mixed RDB-AOF format** – this comes enabled by default in Redise. This allows faster rewrites and reloads when using the AOF persistence.
- **Active defrag** – this feature was contributed by our very own Oran Agra. Redis now actively defrag its allocated memory, freeing up unused ‘holes’ in RAM.
- Many more improvements about performance,memory usage and bug fixes

You can learn more about the release in this [blog post](/blog/redis-4-0-0-released/) and if you really want the full blown list you can always visit the [release notes](https://raw.githubusercontent.com/antirez/redis/4.0/00-RELEASENOTES).

#### Redis Enterprise now supports Redis 4.0!

Support for Redis 4.0 is available on [**Redise Cloud**](/products/redis-cloud/). You can start exploring the new version immediately using our **30MB free subscription,** just [**sign up**](https://app.redis.com/#/sign-up/tabs/redis-cloud?product=redis-cloud) here and you are good to go.

You can also experience Redis 4.0 and new certified modules with the **preview of Redise Pack 5.0**. Redise Pack 5.0 delivers rich functionality combined with the new capabilities in Redis 4.0 engine. Here it is a high level:

- The new **geo-distributed active-active deployments** powered by CRDBs (conflict free replicated databases)
- **Fast search and query** with real-time indexing using [**RediSearch**](http://redisearch.io/)
- Native and **high performance JSON processing** in Redis with [**ReJSON**](/blog/redis-as-a-json-store/)
- **Efficient indexing for “membership” queries** with bloom filters using [**Rebloom**](/blog/rebloom-bloom-filter-datatype-redis/) and
- Ability to upload your custom modules

You can find detailed information on Redise Pack version 5.0 preview program [**here**](/blog/announcing-private-preview-program-upcoming-redis-enterprise-pack-5-0/) and how you can signup for the program.
