---
title: "Redis Enterprise 5.4 supports Redis Streams GA!"
linkTitle: "Redis Enterprise 5.4 supports Redis Streams GA!"
url: "/blog/redis-enterprise-5-4-supports-redis-streams-ga/"
description: "We are happy to announce the launch of Redis Enterprise 5.4, the latest version of our high performance, in-memory database platform."
date: 2018-12-14
blogCategories:
- "Announcements"
- "New Product Announcements"
- "Product Releases"
authors:
- "Paz Yanover"
lastmod: 2026-09-01
hidden: true
---

*By Paz Yanover, Principal Product Manager · Published 14 December 2018 · updated 1 September 2026*

![Blog tile image](/images/site-mirror/0073e867b4e64f59de9047fdcde04295ba647e5c-772x550.webp)

# Redis Enterprise 5.4 supports Redis Streams GA!

We are happy to announce the launch of [Redis Enterprise 5.4](/redis-enterprise/software/downloads/), the latest version of our high performance, in-memory database platform.

The new version contains the following major enhancements:

### Redis 5.0 GA — Redis Streams

[Redis Streams](https://redis.io/docs/latest/develop/), introduced in Redis 5.0, is one of the most popular products today in the Redis ecosystem. Redis Streams is a new data type that models a log data structure in-memory and implements additional powerful operations, such as:

- A set of blocking operations allowing consumers to wait for new data added to a stream by producers.
- A concept called Consumer Groups that enables a group of clients to cooperate while consuming a different portion of the same stream of messages.

**Redis Enterprise 5.4** adds support for Redis 5.0 (GA version 5.0.2) and allows our customers to enjoy the highly available, high-performance and secure database with the new Redis Streams data type.

### Redis Graph Module

Redis Enterprise Modules are installed with Redis Enterprise by default so that it is easy for you to deploy and use these powerful modules. With the release of Redis Enterprise 5.4, [Redis Graph](https://oss.redis.com/redisgraph/) — a new Redis Enterprise Module that introduces the world’s fastest graph database — is an integral part of the Redis Enterprise package.

[**Redis Graph**](/blog/new-redisgraph-1-0-achieves-600x-faster-performance-graph-databases/) joins the previous popular Redis Enterprise Modules:

- [**RediSearch**](https://oss.redis.com/redisearch/)— An extremely fast search and secondary index engine over Redis
- [**ReJSON**](https://oss.redis.com/rejson/)— A JSON data type implementation for Redis
- [**ReBloom**](https://oss.redis.com/rebloom/) — A scalable bloom filters as a new data type for Redis

Redis Enterprise Modules are only available in Redis Enterprise Software and Redis Enterprise VPC deployments.

### Active-Active Redis (CRDB) – Creation in non-clustering mode

Redis Enterprise 5.4 increases the flexibility of [Active-Active database (CRDB) creation ](https://docs.redis.com/latest/rs/administering/database-operations/create-crdb/)with the following creation options:

1. **Clustering mode** — Creates a CRDB that consists of any number of shards in a clustering mode and that is subject to [multi-key commands limitations](https://docs.redis.com/latest/rs/concepts/high-availability/clustering/).
1. **Non-clustering mode** — Creates a CRDB that consists of one shard only in a non-clustering mode so multi-key commands limitations do not apply.

### High Availability for Replica (Slave)* Shards

When a master shard fails, a replica shard is automatically promoted to a master shard to maintain data availability. This creates a single point of failure until a new replica shard is manually created.

**Redis Enterprise 5.4** [expands the high availability capabilities](https://docs.redis.com/latest/rs/administering/database-operations/slave-ha/) by adding the ability to automatically avoid this single point of failure, thereby configuring the cluster to [automatically migrate](/redis-enterprise-cloud/migrate/) the replica shard to another available node. In practice, replica migration creates a new replica shard and replicates the data from the master shard to the new replica shard.

******Please note**** that just as is the case with the Redis open-source project, Redis is in the process of changing the “master-slave” terminology to “master-replica” everywhere, including within our documentation.*

### Support for Ubuntu 18.04

In addition to all of the above updates, **Redis Enterprise Software (RS) 5.4** also adds support for a new operating system — Ubuntu 18.04 64-bit.

If you’re interested in a more detailed view of what else is new in **Redis Enterprise 5.4**, please take a look at our [technical documentation](https://docs.redis.com/latest/index.html) or check out our [release notes](https://docs.redis.com/latest/rs/release-notes/legacy-release-notes/rs-5-4-december-2018/).

If you have any questions, don’t hesitate to drop us a line at [pm.group@redis.com](mailto:pm.group@redis.com)!
