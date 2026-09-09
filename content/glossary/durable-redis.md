---
title: "Durable Redis"
linkTitle: "Durable Redis"
url: "/glossary/durable-redis/"
description: "When something persists, it lasts. In the context of databases, that means you intend for a piece of information that is going to be saved in some way (in memory or on disk) for some period of..."
lastmod: 2025-07-11
---

*updated 11 July 2025*

### What is data persistence?

When something persists, it lasts. In the context of databases, that means you intend for a piece of information that is going to be saved in some way (in memory or on disk) for some period of time, so that it can be recovered even if a computer process is killed. With data persistence, existing data from an application stays intact between sessions, preserving it for use in a following application session without suffering data loss. Data persistence is particularly essential in the event of a server restart, because data stored only in-memory is gone when the power flickers.

### Data persistence options

Redis Enterprise is a fully durable database that serves all data directly from memory, using either RAM or [Redis on Flash](https://redis.io/auto-tiering/). With regards to persistent data, Redis only reads this data when both the primary and secondary shards in a high-availability database are lost.

Redis supports append-only file data persistence (AOF) as well as snapshotting. It is also possible to use both RDB and AOF together, known as “hybrid persistence” to take advantage of the strengths of both options. Lets dive into to each of the Redis data persistence options below with further explanation and more detailed information about the strengths and weaknesses of each.

### Append-only file data persistence for data durability

Append-only file (AOF) is a logging mechanism that writes to a log file on disk every write operation performed on a Redis database. The log file is used to reconstruct the database in the event of a crash or failure.

AOF works by appending each database write operation to the end of the log file, hence the name append-only file. When Redis restarts, it reads the log file and re-executes the write operations preserved in the file to restore the database to its previous state.

AOF provides better data durability than the snapshot persistence option, creating only point-in-time data snapshots.

Redis uses a multi-part AOF mechanism, wherein the original AOF splits into base and incremental files. The base file represents an initial snapshot of the data present when the AOF is written. The incremental files contain changes since the last base AOF was created.

You can configure AOFs to be rewritten in the background when it gets too large, using a process called AOF fsync. The fsync configuration directive controls how often the AOF log file is synchronized to disk.

The latest AOF mechanism implementation reduces the memory consumption and the amount of I/O operations that are performed during an AOF rewrite.

### Snapshot

A snapshot is a point-in-time copy of the Redis data stored in memory. Snapshots are created using the Redis DataBase (RDB) persistence option, which allows the state of the Redis database to be saved to disk at specified intervals.When an RDB snapshot is taken, Redis creates a child process to perform the snapshotting, allowing the main process to continue serving requests.

Snapshots are useful for creating backups of the Redis database, as well as for migrating data between Redis instances. They can be created manually using the ‘SAVE’ or ‘BGSAVE’ command, or automatically using the ‘save’ configuration directive in the Redis configuration file.

It is important to note that while snapshots allow the data in Redis to be persisted to disk, they do not provide the same level of data durability as the AOF persistence option. AOF writes every write operation performed on the Redis database to a log file on disk, which can be used to reconstruct the database in the event of a crash or failure.

### Snapshots vs. backups

Snapshots and backup are designed for two different things. While snapshot supports data durability (i.e. to automatically recover data when there is no copy of the dataset in memory), [backup](https://redis.io/redis-enterprise/technology/backup-disaster-recovery/) supports disaster recovery (i.e. when the entire cluster needs to be rebuilt from scratch).

### Data availability vs. durability

Data durability refers to the ability of data to remain stored and accessible over a period of time, even in the face of various types of failures or disasters. Data availability, on the other hand, refers to the ability of users to access and use the data when needed.

Data availability involves designing systems and processes that allow users to access and use the data when needed. This can involve desinging systems with high uptime and fast response times, as well as implementing failover and load balancing mechanisms to ensure that the data is alaways available to users, even if some of the systems fail.

For a data center, availability is an important metric as is durability. A data center will support persistence by using redundant storage systems, such as storage are networks (SANs) or network-attached storage (NAS) systems. These systems provide multiple copies of data, so that if one copy becomes unavailable, there are other copies that can be accessed.

See our blog [Data Durability and Availability](/blog/data-durability-vs-availability/) for more information on this topic.

### Ephemeral vs. persistent storage

In cloud native deployments such as a public cloud, private cloud, or virtual private cloud, ephemeral (instance) storage cannot be used for data durability purposes.

### What is ephemeral storage?

Ephemeral storage, or volatile temporary storage, disposes of data once its corresponding container reaches the end of its lifespan.

Instead, a network-attached storage (NAS) like [Amazon Elastic Block Store](https://aws.amazon.com/ebs/) (EBS), [Microsoft](https://azure.microsoft.com/en-us/services/storage/disks/) Azure Disk Storage[,](https://azure.microsoft.com/en-us/services/managed-disks/) or [Google Cloud Platform Persistent Disk](https://cloud.google.com/persistent-disk/) is required. That’s because, just as it sounds, ephemeral storage is ephemeral! When a cloud instance fails (which is relatively common), the contents of its local disk are also lost.

### What is persistent storage?

Persistent storage, also known as non-volatile storage, refers to any storage device capable of keeping data intact and available when it is no longer powered on.

Persistent storage is useful for maintaining critical data and making it available for later use. A hard disk drive is a common example of a persistent storage device.

The Redis Enterprise cluster is designed to work with network-attached storage for persistent data. By default, every node in the cluster is connected to a network-attached storage resource, making the cluster immune to data-loss events such as multiple node failures with no copies of the dataset left in DRAM. This data durability-proven architecture is illustrated here:

![Durable Redis](/images/site-mirror/8c5ec09fba20e22367cbc8da41239d4cdb347d1b-1395x805.svg)

As illustrated above, in cases where there is no copy of the dataset left in DRAM, Redis Enterprise will find the most recent copy of the dataset in the network-attached devices that were connected to the failed node, and use that to populate the Redis shard on the new cloud instance.

### Data-persistence at the primary or at the replica level?

By default, when data persistence is enabled Redis Enterprise sets data persistence at the replica of each shard of the database. In this configuration there is no impact on performance, as the primary shard is not affected by the slowness of the disk; on the other hand, replication adds latencies that may break the data persistence SLA. Therefore, Redis Enterprise allows you to enable data persistence on both the primary and replica shards. This is a more reliable configuration that doesn’t infringe on your data persistence SLA, but if the disk speed cannot cope with the throughput of ‘writes,’ it will affect the latency of your database, as Redis delays its processing when it cannot commit to disk. If you use Redis Enterprise DBaaS deployments (Cloud or VPC) you will automatically be tuned to work with a storage engine and the right shards configuration to support your persistent storage load; in an on-premises deployment, we recommend you consult with Redis solutions architects regarding your sizing. Data persistence options are shown here:

![Durable Redis](/images/site-mirror/d6772c3ec3160b10f2b0373d5325f07a670474b5-1214x658.svg)

### Enhanced storage engine

Redis Enterprise enhances the Redis storage engine to increase the throughput of the Redis core with data persistence enabled, and to better utilize cluster resources by allowing multiple Redis instances to run on the same cluster node without affecting performance:

1. When AOF is used as a mechanism for data persistence, the size of the append-only file grows with every ‘write’ operation. An AOF rewrite process is then triggered to control the size of the file and reduce the recovery time from disk. By default (and configurable), the OSS Redis triggers a rewrite operation when the size of the AOF has doubled since the size of the previous rewrite operation. In a ‘write’ intensive scenario, the rewrite operation can block the main loop of Redis (as well as other Redis instances that are running on the same cluster node) from executing ongoing requests to disk. Redis Enterprise uses a greedy AOF rewrite algorithm that attempts to both postpone AOF rewrite operations as much as possible without infringing the SLA for recovery time (a configurable parameter) as well as prevent the rewrite from reaching the disk space limits. Though optimal use of the rewrite process, the overall throughput of a persistent Redis instance is much higher than it otherwise would be.
1. The Redis Enterprise storage layer allows multiple Redis instances to write to the same persistent storage in a non-blocking way, i.e. a busy shard that is constantly writing to disk (during an AOF rewrite) will not block other shards from executing durable operations.

A storage engine benchmark performed by Dell-EMC and Redis showed that when using Redis Enterprise’s enhanced storage engine with Dell-EMC VMAX, Redis performance is nearly unaffected by AOF every-write operation, as shown here:

![Single Node Redis Enterprise ACID](/images/site-mirror/7afbf194fffc52625c6ec23aa7e93d51d32e788e-960x400.webp)

More information on this benchmark can be found here:

- [Your cloud can’t do that: 0.5M ops + ACID @<1ms latency!](/blog/your-cloud-cant-do-that-0-5m-ops-acid-1msec-latency/)
- [Benchmarking Redis Enterprise in full ACID configuration on EMC VMAX at over 0.5 Million ops/sec @ <1 ms latency](/blog/your-cloud-cant-do-that-0-5m-ops-acid-1msec-latency/)
