---
title: "Diving into Conflict-Free Replicated Data Types (CRDTs)"
linkTitle: "Diving into Conflict-Free Replicated Data Types (CRDTs)"
url: "/blog/diving-into-crdts/"
description: "Active-Active Geo-Distribution allows you to place your Redis database cluster instances and data centers close to your users, no matter where they are. Placing read replicas closer to your users..."
date: 2022-03-17
blogCategories:
- "Tech"
authors:
- "Redis  "
lastmod: 2026-06-01
hidden: true
---

*By Redis   · Published 17 March 2022 · updated 1 June 2026*

![Blog tile image](/images/blog/d9e8f500a5594c4321f53cfae252d9aa60e426d5-300x300.webp)

[Active-Active Geo-Distribution](/active-active/) allows you to place your Redis database cluster instances and data centers close to your users, no matter where they are. Placing read replicas closer to your users is the right thing to enable real-time response. For write-heavy applications, that’s not enough. So how do you develop an Active-Active geo-distributed cluster?

## Introduction to Conflict-Free Replicated Data Types (CRDTs)

[Conflict-free replicated data types (CRDTs)](https://www.infoworld.com/article/3305321/when-to-use-a-crdt-based-database.html) (aka convergent replicated data type or commutative replicated data type) are a family of replicated data types with a common set of properties that enable operations to always converge to a final state consistent among all replicas. To ensure that conflicts never happen (there is no concept of conflict resolution) and cause problems in your applications, operations on CRDT data types have to respect a specific set of algebraic properties.

CRDTs work in Redis Enterprise when you create a CRDT-enabled database because standard commands get swapped with an equivalent CRDT implementation. Let’s look at a Redis data structure with a CRDT equivalent and the nuances that Active-Active geo-distributed replication adds.

## Sets in Redis

Redis Sets are similar to what your favorite programming language offers in the standard library, offering specialized operations to add and remove elements, check if an element is part of the set, and perform set intersection, union, and difference. Here’s how it looks like when calling actual Redis commands:

// Create a set:

> SADD fruits apple pear banana

3

// Test if it contains apple:

> SISMEMBER fruits apple

1

// Remove a fruit:
> SREM fruits banana
1

// Test if it’s still present:

> SISMEMBER fruits banana

0

Running the same commands in a CRDT-enabled Redis Enterprise database would display the same behavior, but what’s happening behind the scenes is completely different.

In a CRDT database, all replica nodes can independently apply changes to the “fruits” key. This enables you to write genuinely geo-distributed applications. The downside is that the “replication lag” is also experienced when writing to a value. This approach offers significant advantages for geo-distributed applications and achieving data consistency.

**CRDT Sets & Redis Enterprise**

In a Redis Enterprise CRDT-enabled database, sets operations work under a few additional rules, the two most important of which get applied when merging operations coming from different nodes:

1. Adding wins over deleting.
1. Deleting works only on elements that the replica executing the command has already seen.

The second rule is sometimes referred to as the “observed remove” rule, meaning that you can delete only items that you were able to observe when the command was issued.

**A note on replication lag and consistency model**

While eventually all replica nodes will converge to the same final state, in the short term a command sent to ReplicaEU may not have yet been propagated to ReplicaUS, for example. This situation, albeit normally brief, is the reason why CRDT data structures must hardcode conflict-resolution strategies. All replicas in the same CRDT database will constantly sync their state to provide as consistent a view of the dataset as possible, but keep in mind that CRDTs are also useful for [ensuring high availability](/redis-enterprise/technology/highly-available-redis/) in case of network partitions.

This means that to implement better resilience in your system you will need to account for the possibility of prolonged moments where the system has not yet been not fully synchronized. This makes CRDTs a form of eventual consistency. This is usually described as **strong eventual consistency** because it’s much more efficient than the more common types of replication based on quorum quotas. (For more information, see the [Redis page on Active-Active Geo-Distribution](/active-active/).)

## Why Use CRDTs?

CRDTs perform replication as commutative operations. This has the desirable quality (for a distributed system) that the order of replication does not matter. Replication in an arbitrary order fundamentally reframes many distributed system race conditions, and its usefulness increases as asynchrony (e.g., distribution) increases. In many systems, copies of some data need to be stored on replicas. Examples of such systems include

- Mobile apps that store data on the local device and that need to sync that data to other devices belonging to the same user (such as calendars, notes, contacts, or reminders);
- Distributed databases, which maintain multiple replicas of the data (in the same data center or different locations) so that the system continues working correctly if some of the replicas are offline;
- Collaboration software, such as Google Docs, Trello, Figma, or many others, in which several users can concurrently make changes to the same file or data;
- Large-scale data storage and processing systems that replicate data to achieve global scalability.
- Use cases for CRDTs include:
  - Distributed caching
  - Shared sessions
  - Multi-region IoT data ingest

**More CRDT data structures**

For a complete list of the CRDT data structures that Redis Enterprise supports, [take a look at the official documentation](https://docs.redis.com/latest/rs/databases/active-active/develop/develop-for-aa/).

## Developing for CRDTs

What are the practical requirements for developing an Active-Active application?

Let’s look at the main development aspects that could raise questions.

Client libraries for CRDT databases

One question is whether you need a special type of Redis client to interact with a CRDT database. The answer is no—any normal Redis client can connect to a CRDT database and execute commands directly. As mentioned earlier, the commands don’t change, it’s the underlying mechanics that do. The only thing that clients don’t offer out-of-the-box is the ability to connect to a different geo-distributed replica in case the one closest to the service instance becomes unavailable. We’re working on this issue, but in the meantime, in the event of a network split, you will have to decide at the application level when it’s appropriate to connect to a replica in a different region.

CRDT Application architecture

The advantage of Active-Active geo-distribution is the ability to share some state across service instances distributed globally, all while experiencing local latencies when manipulating that state. To fully exploit this capability, your services need to rely on CRDTs’ semantics as much as possible and, as such, avoid keeping an internal state that would get lost (or become un-mergeable) in the event of failures. CRDT-based databases are available even when the distributed database replicas cannot exchange the data.

CRDTs can’t solve all problems because they hardcode specific merge rules that might not be appropriate for your particular problem. Counters are a typical example: CRDT counters are great, but they can’t be used to model a bank account balance because merges could allow the counter to go negative-and there is no way at the application level to prevent this from happening. In other words, CRDTs are an efficient but nuanced form of eventual consistency that doesn’t apply properly to inherently transactional problems.

**Testing Active-Active Geo-distributed CRDT Applications**

It might seem that testing an Active-Active geo-distributed application must be much more complicated than testing normal single-master ones. While CRDTs certainly are a complex component of your data model, their behavior is fully deterministic in terms of results. You have to account for the primary situation when the cluster is partitioned. As mentioned above, it’s OK to continue sending updates to a replica that has been disconnected from the rest of the cluster because the updates will eventually be merged successfully when the connection is reestablished. You need to ensure that your service can still operate correctly when disconnected from the whole Active-Active geo-distributed CRDT database cluster.

In other words, the only non-obvious extra testing required on your part should be about how the application behaves in the event of a network partition.

## Local latencies to global users

CRDTs allow you to create geo-distributed applications that can offer local latencies to your entire user base, all the while rendering your entire application more resilient to failure. While not all problems can be solved by CRDTs, there is a vast space of improvements that most companies can benefit from. As an example, please take a look at [this recent blog post by Kyle Davis](/blog/redis-game-mechanics-scoring/), where he shows how to implement a leaderboard using Sorted Sets—and hints at the benefits of a CRDT version.

To learn more about writing Active-Active applications with Redis Enterprise, take a look at our [Under the Hood: CRDTs](/resources/under-the-hood/) whitepaper and the [official documentation](https://docs.redis.com/latest/rs/databases/active-active/develop/develop-for-aa/).

## How does eventual consistency compare to strong consistency?

Strong consistency is propagating any update to all copies of data. In the most simple case, a series of updates to the data come from a single source, and all other entities that hold a replica of the data are guaranteed to receive those updates in the same order.

When multiple copies of the data need to be updated simultaneously, there needs to be a way to agree upon the correct version of the data. With strong consistency, once one entity makes any updates, all other replicas are locked to eliminate the need for conflict resolution until they’ve been updated to the same new version. The source of truth pushes updates to all entities in the same order to keep them ‘in step.’

The locking mechanism used in strong consistency is inconsistent with the need for real-time performance. This is where eventual consistency and CRDTs come into play. Every cluster or node can potentially make and receive updates, so there is no way to ensure that each replica gets the same sequence of updates. Eventual consistency is the property where the state of the data is eventually reconciled, regardless of the order of update events that reach each replica. CRDTs can resolve replication conflicts that arise from concurrent updates or concurrent inserts on replicas existing in a decentralized environment.
