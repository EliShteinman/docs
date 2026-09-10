---
title: "Redis Open Source to Redis Cloud"
linkTitle: "Redis Open Source to Redis Cloud"
url: "/tutorials/migration/redis-open-source-to-redis-cloud/"
description: "Before migrating to Redis Cloud, you should evaluate the migration and consider the best option. Read this guide to determine which migration strategy is right for you."
group: "For developers"
aliases:
- "/tutorials/migration-redis-open-source-to-redis-cloud/"
date: 2026-02-25
lastmod: 2026-02-27
hidden: true
---

*Published 25 February 2026 · updated 27 February 2026*

> **TL;DR:**
>
> Export an RDB snapshot from your self-hosted Redis instance and import it into Redis Cloud (offline), or use the `REPLICAOF` command to replicate data in real time for a zero-downtime migration (live).

## What you'll learn

- How to choose between offline and live migration strategies
- How to import data into Redis Cloud from a self-hosted Redis server
- How to use `REPLICAOF` for live replication with minimal downtime
- How to validate your migration and cut over traffic

## Prerequisites

- A running self-hosted Redis Open Source instance with network accessibility
- A [Redis Cloud account](https://redis.io/try-free/) with a target database created
- Access to the [Redis Cloud console](https://cloud.redis.io/)
- For live migration: the source Redis instance must be reachable from the Redis Cloud service

Before migrating to Redis Cloud, you should evaluate the migration and consider the best option. Read this guide to [determine which migration strategy is right for you](/tutorials/migration).

## Why migrate to Redis Cloud?

Redis Cloud is a fully managed service that handles provisioning, patching, monitoring, and scaling so you can focus on your application instead of infrastructure. Key benefits include built-in high availability with automatic failover, instant scalability, and enterprise-grade security. Redis Cloud also offers a [free tier](https://redis.io/try-free/) so you can test your workload before committing.

## Offline data migration

Offline migration works best when you can tolerate a brief maintenance window. You export your dataset and import it directly into Redis Cloud.

To import a dataset from any publicly available Redis server:

1.  Select **Databases** from the Redis Cloud console menu and then select the target database from the database list.
2.  Select **Import**.
3.  Enter the source database details:
4.  Source type - Select **Redis**.
5.  Redis Hostname/IP Address - Enter the hostname or the public IP address of the source Redis server.
6.  Redis port - Enter the port of the source Redis server if it is not the default value of 6379.
7.  Password - Enter the password, if required by the source Redis database.
8.  Select **Import**.
9.  Validate your migration and redirect your application's traffic to the new Redis Cloud endpoint.

References:

- [Import data into a database | Redis Server](https://redis.io/docs/latest/operate/rc/databases/import-data/#redis-server)
- [Import data into a database | FTP or HTTP](https://redis.io/docs/latest/operate/rc/databases/import-data/#via-ftp-or-http)

## Live data migration

Live migration uses Redis replication to sync data continuously, allowing you to cut over with minimal downtime.

1.  Connect to your Redis Cloud Database
2.  Use **REPLICAOF** command to replicate the database

```bash
REPLICAOF 127.0.0.1 6799
```

3\. Use the **REPLICAOF** command with the **NO ONE** option to stop replication.

```bash
REPLICAOF NO ONE
```

4\. Validate your migration and redirect your application's traffic to the new Redis Cloud endpoint.

References:

- [ReplicaOf | Docs](https://redis.io/docs/latest/commands/replicaof/)
- [Important facts about Redis replication](https://redis.io/docs/latest/operate/oss_and_stack/management/replication/#important-facts-about-redis-replication)

## Is there downtime during migration?

With **offline migration**, there is a brief maintenance window while the import runs. Writes to the source instance during this window are not captured, so you should stop writes before exporting.

With **live migration** using `REPLICAOF`, data is replicated continuously. You can cut over traffic once the replica is fully synchronized, resulting in near-zero downtime. Monitor replication lag with the `INFO replication` command on the target to confirm the replica is up to date before switching.

## Next steps

- [Validate your data](/tutorials/migration) after migration to confirm key counts and sample values match
- [Configure your application](/tutorials/migration) to point to the new Redis Cloud endpoint
- Explore [Redis Cloud features](https://redis.io/cloud/) such as Active-Active geo-distribution, auto-scaling, and advanced monitoring
