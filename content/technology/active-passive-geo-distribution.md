---
title: "Active-Passive geo-distribution"
linkTitle: "Active-Passive geo-distribution"
url: "/technology/active-passive-geo-distribution/"
description: "With Redis Enterprise you can create Active-Passive Geo-Distributed deployments using the “replica-of” capability. This unidirectional replication capability allows you to synchronize data between..."
lastmod: 2026-02-20
mirrored: true
---

*updated 20 February 2026*

With Redis Enterprise you can create Active-Passive Geo-Distributed deployments using the “replica-of” capability. This unidirectional replication capability allows you to synchronize data between source and destination databases, placing the data physically closer to the user for low-latency read access. All writes to the source database are replicated to destination databases. However, writes to the destination databases are *not* replicated back to source databases.

“Replica-of” provides great flexibility for creating complex geo-distribution topologies:

- Each source database can replicate to many destination databases.
- Each destination database can replicate from many source databases.
- Each destination database can also be a source database (cascading replication).
- Each database source or destination, participating in the replica-of setup can independently choose database settings including shard count, local replication, and persistence settings. The replication itself is done at the database endpoint level while behind the scenes Redis Enterprise handles the population of the shards across replicas.
- Each cluster-hosting databases participating in the replica-of setup can have a different number of nodes.
- The data transfer between the source and the destination replicas is automatically compressed and can be encrypted on demand.

It is possible to achieve the following Active-Passive Geo-Distributed topologies using the replica-of capability:

- Multi-region deployment in the same cloud
- Multi-cloud deployment
- Hybrid on-premises and cloud deployment

This figure illustrates Active-Passive Geo-Distributed topology using replica-of:

![Redis](/images/site-mirror/ebc597e02b1ac359c5b8279d023e3de566c50731-800x468.webp)

## Want to learn more?

Watch our recent Lightning Demo on how to use active-passive (Replica Of) to migrate Redis data in under 5 minutes.

[Watch the video](https://www.youtube.com/embed/6LYNegHRiRY)
