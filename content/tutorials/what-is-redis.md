---
title: "What is Redis?: An Overview"
linkTitle: "What is Redis?: An Overview"
url: "/tutorials/what-is-redis/"
description: "Redis is an open-source, in-memory data structure store that can be used as a database, cache, message broker, and streaming engine. It belongs to the class of NoSQL databases known as key/value..."
date: 2026-02-25
lastmod: 2026-09-01
hidden: true
---

*Published 25 February 2026 · updated 1 September 2026*

> **TL;DR:**
>
> Redis is an open-source, in-memory data structure store used as a database, cache, message broker, and streaming engine. It delivers sub-millisecond latency, supports rich data types (Strings, Hashes, Lists, Sets, Sorted Sets, Streams, JSON, vector sets), and scales horizontally with Redis Cluster. Redis also supports vector search for GenAI apps, including semantic search, RAG, and recommendation systems. Redis is free to use, runs anywhere, and offers a managed option through Redis Cloud.

**Redis is an open-source, in-memory data structure store that can be used as a database, cache, message broker, and streaming engine.** It belongs to the class of NoSQL databases known as key/value stores, where unique keys map to values of various data types. Redis is widely adopted for its sub-millisecond response times, rich data structures, and versatility across use cases from caching to real-time analytics.

> **Prerequisites:** No prior Redis experience is needed. This overview is designed for beginners who want to understand what Redis is and why devs choose it.

## How does Redis work?

Redis stores all data in memory as key/value pairs, where each key is a unique identifier mapped to a typed value. Each data type has its own set of commands for reading and writing data.

For example, you can store a name in a Redis String and associate it with the key "myname" using the [SET command](https://redis.io/docs/latest/commands/set/), then retrieve it using [GET](https://redis.io/docs/latest/commands/get/):

```bash
127.0.0.1:6379> SET myname "Will Johnston"
OK
127.0.0.1:6379> GET myname
"Will Johnston"
```

Keys in a Redis database are distributed in a flat keyspace. Redis does not enforce a schema or naming policy for keys, giving developers full flexibility over how to organize their data.

## What are Redis data types?

Redis goes far beyond simple key/value string storage. It supports a rich set of data types, each optimized for specific access patterns:

| Data type                                                                   | Description                                                          | Example use                                  |
| --------------------------------------------------------------------------- | -------------------------------------------------------------------- | -------------------------------------------- |
| [Strings](https://redis.io/docs/latest/develop/data-types/strings/)         | The simplest type; stores text, numbers, or binary data up to 512 MB | Counters, cached values, session tokens      |
| [Lists](https://redis.io/docs/latest/develop/data-types/lists/)             | Ordered collections of strings (linked lists)                        | Activity feeds, message queues               |
| [Sets](https://redis.io/docs/latest/develop/data-types/sets/)               | Unordered collections of unique strings                              | Tags, unique visitors, set operations        |
| [Hashes](https://redis.io/docs/latest/develop/data-types/hashes/)           | Maps of field-value pairs, similar to objects                        | User profiles, product details               |
| [Sorted Sets](https://redis.io/docs/latest/develop/data-types/sorted-sets/) | Sets ordered by a numeric score                                      | Leaderboards, priority queues, rate limiters |
| [Streams](https://redis.io/docs/latest/develop/data-types/streams/)         | Append-only log data structures                                      | Event sourcing, activity logs                |
| [JSON](https://redis.io/docs/latest/develop/data-types/json/)               | Native JSON document storage and querying                            | Complex nested data, API response caching    |
| [Vector sets](https://redis.io/docs/latest/develop/data-types/vector-sets/) | Elements associated with vector embeddings for similarity search     | Semantic search, recommendations, RAG        |

Redis also supports specialized types like Bitmaps, Bitfields, HyperLogLog, and Geospatial indexes for advanced use cases.

## What is Redis used for?

Redis is used across industries wherever fast data access matters. Common use cases include:

- **Caching:** Store frequently accessed data in memory to reduce database load and speed up response times.
- **Session management:** Maintain user session data across distributed web applications with built-in expiration.
- **Leaderboards and ranking:** Use Sorted Sets to build real-time leaderboards with automatic ordering by score.
- **Real-time analytics:** Track metrics, counts, and time-series data with sub-millisecond writes.
- **Pub/Sub messaging:** Broadcast messages to multiple subscribers for real-time notifications and chat systems.
- **Rate limiting:** Control API usage and prevent abuse using counters with expiration.
- **Queues and background jobs:** Use Lists or Streams as lightweight, high-performance task queues.
- **GenAI and vector search:** Store vector embeddings and run similarity searches for semantic search, context retrieval, agent memory, retrieval-augmented generation (RAG), and recommendation systems.

## What are the advantages of Redis?

Redis combines in-memory speed with rich data structures, persistence, and horizontal scalability. Key advantages include:

- **Sub-millisecond latency:** All data lives in RAM, so reads and writes complete in microseconds rather than milliseconds.
- **Rich data structures:** Go beyond simple key/value strings with Lists, Sets, Hashes, Sorted Sets, Streams, JSON, and more.
- **Built-in persistence:** RDB snapshots and AOF logs keep your data durable without sacrificing performance.
- **Horizontal scalability:** Redis Cluster distributes data across multiple nodes with automatic sharding and failover.
- **Broad language support:** Official client libraries exist for Python, Node.js, Java, Go, .NET, and many other languages.
- **Vector search and GenAI:** Native support for vector embeddings, similarity search, and hybrid queries makes Redis a strong fit for GenAI apps.
- **Versatile use cases:** Use Redis as a cache, primary database, message broker, vector database, streaming engine, or all of the above in a single deployment.
- **Active ecosystem:** A large open-source community, comprehensive docs, and Redis University courses make it easy to learn and adopt.

## Is Redis a NoSQL database?

Yes, Redis is a NoSQL database. Unlike relational databases that store data in tables with rigid schemas, Redis uses flexible key/value pairs with typed data structures. This makes Redis well suited for use cases where speed, flexibility, and horizontal scalability matter more than complex relational queries.

Redis differs from other NoSQL databases like MongoDB or Cassandra in that it primarily operates in-memory, making it significantly faster for read and write operations.

## How fast is Redis?

Redis is one of the fastest databases available. Because it stores and serves all data from RAM rather than disk, typical operations complete in **under one millisecond**—often in the range of single-digit microseconds. A single Redis instance can handle over 100,000 operations per second on modest hardware, and benchmarks on optimized configurations regularly exceed 1 million ops/sec.

This speed makes Redis an excellent choice for apps that require real-time data access, such as gaming leaderboards, financial trading platforms, and ad-tech bidding systems.

## How does Redis persist data?

Redis persists data to disk so it survives restarts, even though all reads and writes happen in memory. It provides multiple persistence options to ensure durability:

- **RDB (Redis Database):** Takes point-in-time snapshots of your data at configured intervals.
- **AOF (Append Only File):** Logs every write operation, providing stronger durability guarantees.
- **RDB + AOF:** Combines both methods for a balance of performance and data safety.

This means your data is durable even though all reads are served from an in-memory copy, giving you both speed and reliability.

## Is Redis single-threaded?

Redis uses a single-threaded event loop for command processing, which avoids locking overhead and keeps every operation atomic. This design is a deliberate choice—by processing commands sequentially on one thread, Redis eliminates race conditions and delivers predictable, low-latency performance.

Starting with Redis 6.0, I/O threading offloads network read/write work to background threads while the main thread still handles command execution. This means Redis can saturate modern multi-core network interfaces without changing its single-threaded execution model. For workloads that need multi-core parallelism, you can run multiple Redis instances or use Redis Cluster to shard data across nodes.

## Is Redis free?

Yes, Redis is free and open-source software. As of Redis 8, Redis source code is available under the RSALv2, SSPLv1, and AGPLv3 licenses which means you can use, modify, and deploy Redis at no cost. Redis 7.2 and prior releases remain subject to the BSDv3 clause license.

For managed deployments, [Redis Cloud](https://redis.io/cloud/) offers a free tier that includes 30 MB of storage—enough to prototype, learn, and run small workloads without a credit card. Paid tiers scale with your usage and include features like Auto Tiering, Active-Active Geo Distribution, and automated backups.

## Can Redis replace a traditional database?

Redis can serve as a primary database for many apps, especially when combined with its persistence options and rich data structures. Unlike a traditional relational database, Redis keeps all data in memory for fast access while persisting it to disk for durability.

Redis works well as a primary database when your app needs:

- **Fast reads and writes** with sub-millisecond latency
- **Flexible data modeling** using Hashes, JSON, Sorted Sets, and other types instead of rigid table schemas
- **Horizontal scaling** through Redis Cluster
- **Built-in expiration** for data that has a natural time-to-live

For apps that require complex joins, foreign key constraints, or ACID transactions across multiple keys, a relational database may still be a better fit—or you can use Redis alongside a relational database, with Redis handling the hot path and the relational database managing the rest.

## How does Redis support AI apps?

Redis provides built-in vector search and vector sets, making it a fast, general-purpose data layer for GenAI apps. Instead of adding a separate vector database to your stack, you can store embeddings, run similarity searches, and manage your app's operational data in a single Redis deployment.

Key AI capabilities in Redis:

- **Vector sets:** A native data type that associates elements with vector embeddings. Use the [VADD](https://redis.io/docs/latest/commands/vadd/) command to insert items with embeddings and [VSIM](https://redis.io/docs/latest/commands/vsim/) to find the nearest neighbors by similarity.
- **Vector search with indexing:** Store embeddings in Hash or JSON fields, create an index with [FT.CREATE](https://redis.io/docs/latest/commands/ft.create/), and query with [FT.SEARCH](https://redis.io/docs/latest/commands/ft.search/) using KNN or range-based vector queries. Redis supports FLAT and HNSW indexing algorithms with L2, cosine, and inner product distance metrics.
- **Hybrid search:** Combine vector similarity with traditional filters (numeric ranges, tags, full-text) in a single query. This lets you find semantically similar results while applying business logic—for example, "find similar products under $50."
- **Semantic caching:** Cache LLM responses keyed by embedding similarity rather than exact string match, so semantically similar questions return cached answers without another API call.
- **Agent memory:** Store short-term chat history, long-term memory, and session state in Redis so AI agents maintain context across interactions. The [Redis Agent Memory Server](https://github.com/redis/agent-memory-server) provides a ready-made memory layer with a REST API and MCP server, two-tier memory (session-scoped working memory and persistent long-term memory), semantic search, and automatic topic extraction—available as a Docker image or Python SDK.
- **RAG (retrieval-augmented generation):** Chunk documents, index their embeddings, and retrieve relevant context at query time to ground LLM responses in your own data.

Redis handles these AI workloads at the same sub-millisecond latency it provides for caching and session management, so your GenAI app doesn't need a separate infrastructure layer for vector operations.

## Redis vs Memcached

Redis is the more capable choice for most apps. Both Redis and Memcached are in-memory stores, but Redis goes beyond simple string caching with rich data structures, built-in persistence, and clustering:

- **Rich data structures** beyond simple strings (Lists, Sets, Hashes, Sorted Sets, Streams, JSON)
- **Built-in persistence** so data survives restarts
- **Pub/Sub messaging** for real-time communication
- **Lua scripting** for server-side logic
- **Cluster mode** for horizontal scaling with automatic sharding

Memcached is simpler and may be sufficient for basic string caching, but Redis is the more versatile choice for most apps.

## Redis vs MongoDB

Redis and MongoDB are both NoSQL databases, but they solve different problems. Redis is an in-memory data store optimized for speed, while MongoDB is a document database that stores JSON-like documents on disk.

| Feature        | Redis                                                     | MongoDB                                       |
| -------------- | --------------------------------------------------------- | --------------------------------------------- |
| Storage model  | In-memory with disk persistence                           | Disk-based with in-memory caching             |
| Data format    | Key/value with typed data structures                      | JSON-like documents (BSON)                    |
| Query language | Command-based (GET, SET, HSET, etc.)                      | Rich query language with aggregation          |
| Latency        | Sub-millisecond                                           | Single-digit milliseconds                     |
| Scaling        | Redis Cluster (sharding)                                  | Replica sets and sharding                     |
| Best for       | Caching, real-time data, leaderboards, session management | Content management, catalogs, complex queries |
| Schema         | Schema-free                                               | Schema-free (optional validation)             |

Many teams use Redis and MongoDB together—MongoDB as the primary data store for complex documents and queries, and Redis as a caching or real-time processing layer in front of it.

## Redis vs DynamoDB

Redis and Amazon DynamoDB are both key/value stores, but they differ in architecture, pricing, and performance characteristics. Redis runs in-memory for the lowest possible latency, while DynamoDB is a fully managed, disk-based service on AWS.

| Feature         | Redis                                                              | DynamoDB                                          |
| --------------- | ------------------------------------------------------------------ | ------------------------------------------------- |
| Deployment      | Self-managed, Docker, or Redis Cloud                               | AWS-managed only                                  |
| Storage model   | In-memory with disk persistence                                    | Disk-based with DAX caching option                |
| Latency         | Sub-millisecond                                                    | Single-digit milliseconds (microseconds with DAX) |
| Data structures | Strings, Lists, Sets, Hashes, Sorted Sets, Streams, JSON, and more | Key/value and document items                      |
| Pricing         | Open source (free) or Redis Cloud usage-based                      | Pay-per-request or provisioned capacity           |
| Querying        | Commands per data type                                             | Primary key, secondary indexes, PartiQL           |
| Best for        | Real-time apps, caching, low-latency workloads                     | Serverless apps, AWS-native architectures         |

Choose Redis when you need the lowest possible latency and rich data structures. Choose DynamoDB when you want a fully managed, serverless database tightly integrated with the AWS ecosystem.

## Frequently asked questions

### What language is Redis written in?

Redis is written in C. This contributes to its minimal overhead and high performance, giving it direct control over memory management and system-level optimizations.

### Does Redis support transactions?

Yes, Redis supports transactions through the MULTI/EXEC command block. Commands between MULTI and EXEC run sequentially and atomically—no other client command runs in between. Redis also supports optimistic locking with the WATCH command.

### How much data can Redis store?

Redis can store up to 2^32 keys (over 4 billion), and each String value can hold up to 512 MB. The practical limit depends on available memory. Redis Cloud and Redis Cluster let you scale beyond a single node's memory by sharding data across multiple instances.

### What is Redis Pub/Sub?

Redis Pub/Sub is a messaging pattern where publishers send messages to channels and subscribers receive them in real time. It enables decoupled communication between services—useful for real-time notifications, chat apps, and event-driven architectures. Redis also supports Redis Streams for persistent, consumer-group-based messaging.

### Is Redis ACID-compliant?

Redis provides atomicity for individual commands and MULTI/EXEC transaction blocks, but it does not support full ACID transactions with rollback across multiple keys in the way a relational database does. For most use cases, Redis's atomic operations and Lua scripting provide sufficient consistency guarantees.

### What companies use Redis?

Thousands of companies across every industry use Redis, including technology companies, financial institutions, gaming platforms, e-commerce sites, and healthcare organizations. Redis is one of the most popular databases in the world, consistently ranking among the most-loved technologies in developer surveys.

### Can Redis be used as a vector database?

Yes. Redis supports vector search natively through vector sets and indexed vector fields in Hash or JSON documents. You can store embeddings, run KNN and range-based similarity queries, and combine vector search with filters on structured fields (hybrid search)—all without a separate vector database.

### What are Redis client libraries?

Redis client libraries let you interact with Redis from your app's programming language. Official and community-maintained clients exist for Python (redis-py), Node.js (node-redis), Java (Jedis, Lettuce), Go (go-redis), .NET (StackExchange.Redis), and many other languages. See the full list on the [Redis clients page](https://redis.io/docs/latest/develop/clients/).

## How do I get started with Redis?

The fastest way to start using Redis:

1. **Try Redis Cloud free:** Sign up for a [free Redis Cloud account](https://redis.io/try-free/) — no installation required.
2. **Run Redis locally with Docker:**

    ```bash
    docker run -d --name redis -p 6379:6379 -p 8001:8001 redis:latest
    ```

3. **Follow the quick-start tutorial:** Walk through the [Redis quick start guide](/tutorials/howtos-quick-start/) to learn basic commands and data types hands-on.

## Next steps

Ready to dive deeper? Explore these tutorials and resources:

- [Quick start guide](/tutorials/howtos-quick-start/) — set up Redis and learn the basic commands.
- [Quick start cheat sheet](/tutorials/howtos-quick-start-cheat-sheet/) — a handy reference for common Redis commands.
- [Get started with Redis course](https://university.redis.io/learningpath/14q8m6gilfwltm?tab=details) — a free, comprehensive course at Redis University covering data structures and real-world applications.
- [Vector sets basics](/tutorials/howtos-vector-sets-basics/) — learn how to store and query vector embeddings with Redis vector sets.
- [Getting started with vector search](/tutorials/howtos-solutions-vector-getting-started-vector/) — build vector similarity search with Redis indexing.
- [Redis Agent Memory Server](https://github.com/redis/agent-memory-server) — a ready-made memory layer for AI agents with semantic search, long-term memory, and MCP support.
- [Redis Cloud](https://redis.io/cloud/) — a fully managed cloud database with a free tier.
