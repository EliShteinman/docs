---
title: "Redis 8 brings vector sets and is now in preview on Redis Cloud Essentials"
linkTitle: "Redis 8 brings vector sets and is now in preview on Redis Cloud Essentials"
url: "/blog/redis-8-brings-vector-sets-and-is-now-in-preview-on-redis-cloud-essentials/"
description: "Redis 8 is now available for preview on Redis Cloud Essentials. Starting today, you can create a Redis 8 database and experience the power of our most performant Redis version yet."
date: 2025-07-22
blogCategories:
- "Tech"
authors:
- "Bosmat Tuvel"
- "Noam Stern"
lastmod: 2025-10-01
hidden: true
---

*By Bosmat Tuvel, Noam Stern · Published 22 July 2025 · updated 1 October 2025*

![Redis 8 brings Vector Sets and is now in preview on Redis Cloud Essentials](/images/blog/7c0a4204a4f608bc83f022443460bdacf79fc3af-772x552.webp)

Redis 8 is now available for preview on [Redis Cloud Essentials](https://redis.io/docs/latest/operate/rc/subscriptions/view-essentials-subscription/essentials-plan-details/). Starting today, you can create a Redis 8 database and experience the power of our most performant Redis version yet.

Whether you're building AI agents, managing sessions, caching, or streaming events, Redis 8 delivers everything you need in one powerful release. The new vector sets data structure (beta) joins those previously part of Redis Stack—including JSON, time series, and five probabilistic data structures: bloom filter, cuckoo filter, count-min sketch, top-k, and t-digest. Plus, you get over 30 performance improvements and a Redis Query Engine with up to 16x more processing power to make your apps faster than ever.

## What’s new in Redis 8

Redis 8 is our biggest leap forward yet and is faster, more capable, and built for AI agents & apps with native vector support. This release focuses on what matters most: performance, flexibility, and making your life as a developer easier.

### Key Highlights

**Vector sets (beta):** A new data structure for AI workloads, created by Salvatore Sanfilippo, Redis's original creator. Vector sets enable native, fast vector similarity search using the HNSW (Hierarchical Navigable Small World) algorithm. By extending the sorted set data structure to store high-dimensional vector embeddings, you get simple commands to add and retrieve vectors that are most similar to another vector.

Think of it this way: You're building a music recommendation system where each song is a vector encoding its characteristics—tempo, key, genre, language, and listener preferences. With vector sets, you store these embeddings and instantly retrieve the most similar songs to a user's current favorite. The result? Highly personalized, vibe-based discovery that goes beyond basic genre matching.

Vector sets complement the Redis Query Engine, which continues to be the go-to for real-time full-text, numerical, vector, and hybrid queries over massive, scalable datasets.

Learn more about vector sets in our [documentation](https://redis.io/docs/latest/develop/data-types/vector-sets/) and in a [YouTube video](https://www.youtube.com/watch?v=kVApsFUeuEA) by Salvatore Sanfilippo, the creator of Redis.

**Massive performance gains:** Redis 8 includes 30+ performance enhancements across core operations, memory management, and internal optimizations. Many Redis Cloud customers will see meaningful performance gains by simply choosing Redis 8.

Check out some of these improvements from our benchmarking comparing Redis 8 to Redis 7.4 on Redis Cloud.

![Redis 8 brings Vector Sets](/images/blog/05591762f85ceeff251a8d533b855bc4d9cab987-1316x742.webp)

You see a latency reduction of up to 78% for bitmap, up to 66% for set, and up to 58% for sorted set command groups.

This is the largest performance boost in any Redis release—ever.

**Smarter resource management: **Redis 8 introduces int8 vector encoding in the Redis Query Engine so you can store and access high-dimensional vectors using 8-bit integer representation. Translation: lower infrastructure costs and better scalability.

**Granular data lifecycle control:** Redis 8 introduces new commands for hash field expiration so you can apply time-to-live (TTL) to individual fields within a hash.

The new commands introduced are:

- HGETEX – retrieve the value of one or more fields of a given hash key and set their expiration time or time-to-live (TTL).
- HSETEX – set the value of one or more fields of a given hash key, and optionally set their expiration time or time-to-live (TTL).
- HGETDEL – Get and delete the value of one or more fields of a given hash key.

## Ready to get started?

Redis Cloud delivers Redis 8 as a service with no provisioning headaches, no configuration puzzles, and no additional performance tuning required.

1. **Create a Redis 8 database** on the Essentials tier via [Cloud Console](https://app.redislabs.com/) or API
1. **Choose your memory size** - start for free with 30MB or scale up as needed
1. **Connect your app** and start building with new Redis 8 capabilities

Want to dive deeper? Check out the Redis 8 [documentation](https://redis.io/docs/latest/develop/whats-new/8-0/).

## What’s next

Redis 8 will soon be generally available on [Redis Cloud](https://redis.io/docs/latest/operate/rc/databases/create-database/create-pro-database-new/) including our Pro tier with support for larger datasets, advanced configuration options, replication, and service-level agreements (SLAs).

**Try Redis 8 out now on Redis Cloud Essentials and let us know what you build!**
