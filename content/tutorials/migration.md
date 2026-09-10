---
title: "Redis Cloud Migration"
linkTitle: "Redis Cloud Migration"
url: "/tutorials/migration/"
description: "Before migrating to Redis Cloud, you should evaluate the migration and consider the best option. This guide covers three strategies so you can pick the one that fits your workload, downtime..."
group: "For operators"
date: 2026-02-25
lastmod: 2026-02-27
hidden: true
mirrored: true
---

*Published 25 February 2026 · updated 27 February 2026*

> **TL;DR:** **What is the best way to migrate Redis?**
>
> Choose [**database replacement**](#database-replacement) if you use Redis only as a cache and can tolerate a cold start. Choose [**offline migration**](#offline-data-migration) (RDB export/import) when you need to preserve data but can accept a brief maintenance window. Choose [**live migration**](#live-data-migration) with [RIOT-X](https://github.com/redis/riotx-dist) when you need zero-downtime replication from a self-hosted or managed Redis instance to Redis Cloud.

Before migrating to Redis Cloud, you should evaluate the migration and consider the best option. This guide covers three strategies so you can pick the one that fits your workload, downtime tolerance, and data requirements.

## What you'll learn

- How to evaluate your migration requirements (data loss tolerance, downtime budget, dataset size)
- The trade-offs between the three migration strategies
- Which Redis migration tools to use for each strategy
- Where to go next for step-by-step instructions

## Strategy comparison

|                  | Database replacement | Offline (RDB) migration                  | Live migration (RIOT)                        |
| ---------------- | -------------------- | ---------------------------------------- | -------------------------------------------- |
| **Downtime**     | Minimal (cold cache) | Minutes (depends on dataset size)        | None                                         |
| **Data loss**    | All existing data    | None                                     | Possible for very large keys (100 MB+)       |
| **Complexity**   | Low                  | Low                                      | High                                         |
| **Best for**     | Cache-only workloads | Session stores, small-to-medium datasets | Production workloads requiring zero downtime |
| **Tools needed** | None                 | RDB export/import                        | RIOT                                         |

## Database replacement

If you can tolerate a flush of all your Redis data, there's no need to migrate the data at all. You can point your application to a new Redis Cloud database by configuring your client libraries and start working with a fresh, empty database. This can be a valid option if you use Redis as a cache and can restart without data. However, slow performance may impact your service while data is rehydrated, especially if Redis is used as a cache.

Pros:

- Simple to execute
- Little to no Redis downtime

Cons:

- Loss of all Redis data

## Offline data migration

If you use Redis for more than caching, such as session storage, you can't afford data loss or performance issues from a full data flush. For this, a durable persistence option is available. Next, consider if you can handle downtime, which might only last a few minutes, depending on the time needed to export and import your Redis data. If the downtime is acceptable, we recommend offline data migration. It's straightforward but will cause downtime during the data transfer from the source database to Redis Cloud.

Pros:

- Simple to execute
- Redis data is migrated from the source database to Redis Cloud
- Supported by other Redis based solutions such as ElastiCache and Redis Cloud
- Data consistency

Cons:

- Downtime during migration
- Might take some time for large datasets

## Live data migration

Live data migration can be done without downtime or data loss, but it is more complex and requires careful consideration. This method uses an external tool called RIOT, which was developed by Redis experts. The documentation provides guidance, and expert support is available if needed.

Pros:

- Migrates live data to Redis Cloud
- No downtime

Cons:

- More complex with potential issues
- Might require additional compute instance
- It may need tuning during testing
- It may not work for large key sizes (100MB+)
- Data consistency is not guaranteed
- High CPU usage
- It may require changes to source database
- RIOT support is the best effort

## How to migrate your data

Once you determine which migration strategy to use, follow the step-by-step guide for your source environment:

### Migrate to Redis Cloud

- [ElastiCache to Redis Cloud](/tutorials/migration/elasticache-to-redis-cloud/) — offline and live migration from AWS ElastiCache
- [Memorystore to Redis Cloud](/tutorials/migration/memorystore-to-redis-cloud/) — offline and live migration from Google Cloud Memorystore
- [Open source Redis to Redis Cloud](/tutorials/migration/redis-open-source-to-redis-cloud/) — migrate from a self-hosted Redis instance

### Migrate to Azure Managed Redis

- [ElastiCache to Azure Managed Redis (AMR)](/tutorials/learn/migration/elasti-cache-to-azure-managed-redis/) — move your workload from AWS to Azure
- [Memorystore to Azure Managed Redis (AMR)](/tutorials/learn/migration/memorystore-to-azure-managed-redis/) — move your workload from Google Cloud to Azure

## Next steps

- [Create a free Redis Cloud account](https://redis.io/try-free/) and provision your target database before starting the migration.
- Review the [Redis Cloud documentation](https://redis.io/docs/latest/operate/rc/) for configuration best practices.
- Explore the [RIOT-X migration tool](https://github.com/redis/riotx-dist) if you plan to use live migration.
