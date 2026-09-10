---
title: "Under the Hood: Redis Enterprise Flash Database Architecture"
linkTitle: "Under the Hood: Redis Enterprise Flash Database Architecture"
url: "/blog/hood-redis-enterprise-flash-database-architecture/"
description: "For many interactive applications, responsiveness is key to engaging and fluid experiences. However, RAM is expensive. Keeping a large amount of data with Redis can be costly. Given the..."
date: 2017-10-16
blogCategories:
- "Company"
- "Tech"
authors:
- "Cihan B"
lastmod: 2025-03-27
hidden: true
mirrored: true
---

*By Cihan B · Published 16 October 2017 · updated 27 March 2025*

![Blog tile image](/images/site-mirror/4f3ab4532ac918f5fcc94239bb30c809071f5eb9-270x230.webp)

For many interactive applications, responsiveness is key to engaging and fluid experiences. However, RAM is expensive. Keeping a large amount of data with Redis can be costly. Given the infrastructure cost, you end up choosing between the following 2 options;

**#1:** Pay a premium for storing sizable datasets in RAM with Redis OR
**#2:** Limit Redis database use to the most valuable data and augment Redis with disk-based relational or NoSQL databases.

Redis Enterprise Flash provides a better option **#3:** Redis Enterprise Flash technology combines RAM and flash to store large data sets in Redis with much lower cost per GB. With Redis Enterprise Flash, you can extend RAM onto Flash devices like NVMe and SATA based SSD drives and keep larger data sets in Redis, all without losing Redis’ performance advantage.

Let’s dig deeper into Redis Enterprise architecture to see how combining flash based SSD drives into the mix work in practice.

**Redis Enterprise Architecture Overview**

Let’s start with an overview of Redis Enterprise before we drill into the Flash architecture.

A Redis Enterprise cluster is composed of identical nodes that are deployed within a data center or stretched across local availability zones. Redise architecture is made up of a management path (depicted in the blue layer in Figure 1 below) and data access path (depicted in the red layer in Figure 1 below).

– The **Management path** is composed of proxy which helps scale connections and cluster manager which is responsible for orchestrating the cluster and the placement of database shards, as well as detecting and mitigating failures.
– The **Data Access path** is composed of master and slave Redis shards. Clients perform data operations on the master shard. Master shards maintain slave shards using the in-memory replication.

![](/images/site-mirror/6a397a28ed591aded729b311df62b9d287d7c09e-1319x517.webp)

*Figure 1*
*Redis Enterprise nodes, with blue tiles representing the management path and red tiles representing the data access path with Redis as the shards.*

**High Availability with Replication:** Redis Enterprise uses in-memory replication to maintain master and slave replicas stretched across nodes, racks and zones. Redis Enterprise comes with various watchdogs that detect and protect against many failure types. In node, network and process failures that render the master replica inaccessible, Redis Enterprise automatically promotes the slave replica to be a master replica and redirects the client connection transparently to the new master replica.

Besides the intra-cluster replication, Redis Enterprise also has built-in WAN-based replication for Redis deployments across multiple data centers. You can find additional details in the [references](https://docs.google.com/document/d/1dD-7pK108nBOp52LIsACpoNW_3skypCtnil1u1coyxw/edit?ts=59e52775#heading=h.vhdukms2tgac) section.

**Scaling & Performance with Sharding:** Each Redis Enterprise cluster can contain multiple databases. In Redis, databases represent data that belong to a single application, tenant or microservice. Redis Enterprise is built to scale to hundreds of databases per cluster to provide flexible and efficient multi-tenancy models.

Each database can contain few or many Redis shards. Sharding is transparent to Redis applications. Master shards in the database process data operations for a given subset of keys. The number of shards per database is configurable and depend on the throughput needs of the applications. Databases in Redis Enterprise can be resharded into more Redis shards to scale throughput while maintaining sub-millisecond latencies. Re-sharding is performed without downtime.

![](/images/site-mirror/d3bacd229aa5fd049cdaba22b7a01bc433c70847-2000x1125.webp)

*Figure 2*
*Redis Enterprise places master (M) and slave (S) replicas in separate nodes, racks and zones and use in-memory replication to protect data against failures.*

In Redis Enterprise, each database has a quota of RAM. The quota cannot exceed the limits of the RAM available on the node. However, with Redis Enterprise Flash, RAM is extended to the local flash drive (SATA, NVMe SSDs etc). The total quota of the database can take advantage of both RAM and flash drive. The administrator can choose the RAM vs Flash ratio using the slide seen in figure 3. This ratio can be updated at any moment in the lifetime of the database without downtime.

![](/images/site-mirror/74e55bffda948c3d00f7e6570d5c5831e06582c6-2000x1125.webp)

*Figure 3*
*Create Database dialog in Redis Enterprise Pack with the view of the RAM and Flash configuration.*

**Redis Enterprise Flash Architecture**

With Redis Enterprise Flash, you get an enhanced version of Redis as a shard. Besides other modifications, with this shard, instead of storing all keys and data in RAM, less frequently accessed values are pushed to flash. In figure 4, you can see the RAM and Flash combined together for storing data as 2 separate shades of gray.

![](/images/site-mirror/7b7221291508df237f583078d2e581f0b9c858d7-2000x1125.webp)


*Figure 4*
*Redis Enterprise Flash shards with process, memory and disk storage components. Redis Enterprise Flash uses both RAM and Flash for keeping data. RAM store all keys and some values. As the RAM fills up, less frequently used values are moved to flash (NVMe or SATA based SSDs).*

If applications need to access a value that is in flash, Redis Enterprise automatically brings the value into RAM. Depending on the flash hardware in use, applications experience slightly higher latency when bringing values back into RAM from flash. However subsequent accesses to the same value is fast, once the value is in RAM.

Using smart placement techniques, Redis Enterprise Flash adapts to changes in the workload over time. Redis Enterprise Flash has a background task that ejects less frequently used values to flash in order to adapt and maintain a healthy dose of free space for new incoming operations.

It is important to note that even though values get ejected to flash, all keys and metadata stay in RAM. Keys are typically smaller in size than values. Many Redis commands require access to keys without requiring access to the value. Keeping the full list of keys in RAM ensures many operations can be executed without any penalty of value retrieval from flash. Background services managing expiry, ensuring uniqueness of keys in the database are frequent operations in the database. With all keys stored in RAM, it is easy to check if the key already exists before inserting the new key or to run expiry checks.

**Durability:** Redis Enterprise Flash uses a flash drive as a RAM extension. At bootstrap of the database, Redis Enterprise Flash expects and ensures that both RAM and Flash drive are completely empty. Once the engine is started, RAM+flash is populated from the durable copy of data (disk or another replica). When using Redis Enterprise Flash, you can use either of Redis Enterprise’s two durability options:

– **Disk-based durability:** Redis Enterprise still maintains a durable copy on disk. Just like disk-based systems, this IO path is placed on a slower and more durable network-attached storage device. Redis databases provide tunable options to maintain this durable copy. You can read more about the durability options [here.](/redis-enterprise-documentation/concepts-architecture/concepts/database-persistence/)
– **Replication-based durability:** Redis Enterprise also maintain a replica–a slave shard–for durability. Replication-based durability protects against node, rack or zone failures and provides better write performance than network-attached storage writes. This means that in the event of an unplanned interruption, it is likely that your replica is more up to date than your durable copy on disk. To take full advantage of the replicated-durability, Redis provides the WAIT command. WAIT ensures that a write can wait for acknowledgement until multiple replicas confirm that write. This ensures that a write confirmed with WAIT on replicas will be durable even if a node catches on fire and never comes back to the cluster.

**“Buffer Cache” vs The “RAM Extension” Approach**

The smart data placement in Redis Enterprise Flash, which brings values from flash into RAM based on working set, is similar to disk-based database systems and the “Cache miss” on the buffer cache of the database. However, similarities between disk-based databases and the RAM extension method used in Redis Enterprise Flash end there. The IO patterns used in Redis Enterprise Flash are much more efficient than those of a disk-based system. Here are some of the differences between the two:

– **Hot Value Handling:** Many application workloads perform repeated writes to a set of “hot” keys in a short period of time, such as when the keys belong to an active piece of data. For example, imagine repeated updates by an app to its database, tracking a current shopper’s state on a site as the shopper views various products. Disk-based databases perform these writes both in RAM and on disk to persist the changes each time. However, updates to data in RAM are not sent to flash in Redis Enterprise Flash. The RAM extension approach used by Redis Enterprise Flash does not require any writes to flash under repeated writes to “hot” keys, unless the value gets ejected to flash. Remember that active values don’t get ejected to flash and mostly stay in RAM, so the repeated updates to the active shopper’s keys simply happen in RAM and do not require flash writes. This ensure that the IO bandwidth of the Flash drive is only used for ejections to Flash.
– **Exploiting Ephemeral Storage:** The cloud architecture in public or private clouds typically comes with two types of storage, faster ephemeral storage and slower durable network-attached storage. Disk-based databases require their writes to persist all the way to disk for every write. Thus you are required to use the persisted network-attached storage. However, Redis Enterprise Flash treats flash memory as a RAM extension, thus it can fully take advantage of local, fast ephemeral storage.
– **Write Amplification:** Disk-based databases depend on disk writes for durability. Each write to disk in disk-based databases is typically done through a redo-log (RL) or a write-ahead-log (WAL) before the actual values are updated on storage. Redis Enterprise Flash uses RocksDB to manage the flash drive access. The call sequence to RocksDB with Redis Enterprise Flash does not need to maintain these additional WALs. Write amplification measures the number of IO operations that any single read/write causes. Due to the logged writes, disk-based databases end up with much higher write amplification. You can read more about RocksDB and various IO amplification effects [here](https://github.com/facebook/rocksdb/wiki/RocksDB-Tuning-Guide#amplification-factors).
–** Advances in HW with Persistent Memory:** The techniques used in creating Redis Enterprise Flash are based on the new direction in memory technology. As persistent memory is introduced into the compute architecture such as [Intel’s 3DXPoint](/blog/redis-flash-double-performance-nvme/), the idea behind these technologies is to allow the application to decide which part of the data will be kept in RAM and which will use Flash/Nand in-order to maximize performance at the optimal cost. Redis Enterprise Flash was designed to exploit these benefits.

### Get Started and Try Redis Enterprise Flash!

It is easy to get started with Redis Enterprise Flash with Docker on Windows, Linux or Mac machine. You can find the steps here: [Redis Enterprise Flash Quick Start.](/redis-enterprise-documentation/getting-started/redis-enterprise-flash/)

### References

- Redis Enterprise Flash
  - [Overview](/redis-enterprise-documentation/concepts-architecture/concepts/redis-e-flash/)
  - [Best Practices and Considerations](/redis-enterprise-documentation/installing-and-upgrading/redis-flash-storage-memory-considerations/)
- Redis Enterprise Architecture
  - [Clustering Architecture](/redis-enterprise-documentation/concepts-architecture/architecture/database-clustering/)
  - [Replication Architecture](/redis-enterprise-documentation/concepts-architecture/architecture/database-replication/)
- [Documentation](/resources/redis-pack-documentation/)
- [How To Guides](https://docs.redis.com/latest/rs/installing-upgrading/quickstarts/redis-enterprise-software-quickstart/)
