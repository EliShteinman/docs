---
title: "Scaling Out Redis: Read-Only Slaves or Cluster?"
linkTitle: "Scaling Out Redis: Read-Only Slaves or Cluster?"
url: "/blog/scaling-out-redis-read-only-slaves-or-cluster/"
description: "Instead, it uses asynchronous replication “for scalability … or simply for data redundancy.”"
date: 2013-10-01
blogCategories:
- "Tech"
authors:
- "Redis  "
lastmod: 2026-08-13
hidden: true
---

*By Redis   · Published 1 October 2013 · updated 13 August 2026*

![Blog tile image](/images/blog/1b7a2cc681b5b8abff3db9344d3ad13638b4e89d-635x200.webp)

![](/images/blog/1b7a2cc681b5b8abff3db9344d3ad13638b4e89d-635x200.webp)

### Thankfully, no humans are enslaved by Redis.

Instead, it uses [asynchronous replication](https://redis.io/topics/replication) “*for scalability … or simply for data redundancy.*”

Also, “*a [Redis] master can have multiple slaves … [that] are able to accept other slaves’ connections. Aside from connecting a number of slaves to the same master, slaves can also be connected to other slaves in a graph-like structure.*”

Setting up Redis replication is trivial and its flexibility provides great power.
Classic use cases for Redis’ replication are:

1. Scaling performance by using the replicas for intensive read operations.
1. Making data redundant in multiple locations.
1. Offloading data persistency costs from the master by delegating it to the slaves.

As a Redis Service provider, we are often asked why we do not provide access to our read-only replicas. It’s a valid question, and our answer relates to each of the use cases:

1. Scaling Our service scales by allocating resources to the databases that we manage. We deploy clusters on which we create database instances. Each database instance is sharded across the cluster’s members and each of the shards is split-able, highly available, relocatable and dynamically (re)sizable. To provide for more reads (or writes, RAM, CPUs, or bandwidth), we just reshard and rebalance as needed. Our cluster immediately and transparently provides access to the new shards, hence there is no need to access read-only replicas.
1. Redundancy We use replication for data redundancy at the shard level. Our redundancy is augmented with monitoring and auto-failover mechanisms that are internal to our service and do not require any user intervention.
1. Load Our replicas are configured to manage data persistency so the master shard is free to process requests.

Since replication is asynchronous, it can introduce inconsistencies when accessing stale data. Sharding, on the other hand, does not exhibit that property and is therefore a preferable approach to addressing read and write scaling challenges. Because our managed service addresses scalability (via sharding), redundancy (with auto-failover) and load management, there are only a handful of scenarios in which having access to the read replicas is of any value.

For example, a replica can be set up to give read-only database access to interested parties (e.g. development).

We are planning to support this functionality in the future, so if you have other use cases for read replicas we’d love to hear about them. Let us know if you are using replication for purposes other than scaling, redundancy or offloading – just drop us a line at [info@garantiadata.com](mailto:info@garantiadata.com) or contact [our support](/support/).
