---
title: "How Conflict-free Replicated Data Types power active-active database replication"
linkTitle: "How Conflict-free Replicated Data Types power active-active database replication"
url: "/blog/how-crdts-power-active-active-database-replication/"
description: "Your application runs in three regions. A customer in Tokyo buys the last unit of a product at the exact moment a customer in Frankfurt buys the same SKU. Both writes succeed locally. Both replicas..."
date: 2026-05-27
blogCategories:
- "Tech DE"
authors:
- "Jim Allen Wallace"
lastmod: 2026-05-27
hidden: true
---

*By Jim Allen Wallace, Sr. Product Marketing Manager · Published 27 May 2026*

![How CRDTs power active-active database replication](/images/site-mirror/6f142e344b96307882f7f112eaacabe7cf46ed8e-2400x1256.webp)

Your application runs in three regions. A customer in Tokyo buys the last unit of a product at the exact moment a customer in Frankfurt buys the same SKU. Both writes succeed locally. Both replicas decrement inventory. Which region's view is correct, and what happens to the order that "lost"?

That question sits at the heart of active-active replication, and for most distributed database architectures, the answer involves painful trade-offs: higher write latency, silent data loss, or brittle application-level reconciliation. Conflict-free Replicated Data Types (CRDTs) offer a different approach: data structures designed to [merge automatically](https://crdt.tech/) for supported data types, without special conflict-resolution code or human intervention.

This article explains why active-active replication creates conflicts in the first place, how CRDTs merge concurrent updates into a consistent state, and what kinds of workloads they fit (and don't).

## Why active-active replication is hard

Active-active replication is hard because two regions can accept conflicting writes to the same data at the same time, and there's no universally safe way to resolve them after the fact. Every architectural choice trades off write latency, availability, or data integrity, and the wrong choice can silently lose committed data.

Here's why. During a network partition, you can't have both strong consistency and full availability, so you have to choose. A single-leader (primary-replica) setup chooses consistency by routing every write through one node, which makes conflicts impossible by design but creates a bottleneck and a single point of failure. Active-active gives up that guarantee so every region can write locally, which means two nodes can update the same key at the same time without either one knowing about the other's change until replication catches up.

That leaves two ways to keep the data sane. The first is to coordinate every write globally using a consensus protocol like Paxos or [Raft](https://www.usenix.org/conference/atc14/technical-sessions/presentation/ongaro). The protocol elects a leader, funnels writes through it, and confirms each commit with a quorum of replicas before acknowledging the client. That's safe, but slow at global scale. [Spanner's cross-region docs](https://cloud.google.com/spanner/docs/replication) report about 100 ms strong-read latency between us-east1 and a leader in europe-west4, almost all of it round-trip network time. Every write pays that toll.

The second option is to skip coordination and reconcile later, usually with Last Write Wins (LWW). When two regions update the same key, the write with the later timestamp survives and the other is [silently discarded](https://www.infoq.com/presentations/architecture-multi-region-storage). It's fast, but the data loss is invisible. Your application thinks both writes succeeded. Only one actually did.

Real-world replication architectures come in many flavors, and most production systems blend patterns. But the broad design choices reduce to a small set of trade-offs, summarized below:

| Architecture | Write latency | Failure mode at global scale |
|---|---|---|
| Primary-replica | High (all writes to single primary) | Geographic read-write latency; single point of failure on promotion |
| Active-passive | Medium (primary only) | Failover gap: unavailable for writes until promotion completes |
| Active-active (synchronous) | High (inter-region quorum) | Latency tied to slowest quorum member |
| Active-active (asynchronous) | Low (local only) | Write conflicts, split-brain, silent data loss |

The bottom row is where most globally distributed applications want to live. Active-active with asynchronous replication gives you the best write latency, but the worst conflict story. CRDTs are what make that approach safer to operate, by changing how conflicts are handled for data types whose semantics fit the model.

## What CRDTs are

CRDTs make this work by moving conflict resolution out of the application layer. A CRDT is a [data structure](https://redis.io/glossary/data-structures/) whose merge rules are built into the data type itself. Independent copies on different nodes can be updated separately and still converge to the same consistent state without coordination, because the rule for combining concurrent updates is part of the data type's definition rather than something the application layer has to figure out at runtime.

That's the shift. Conflict resolution stops being a hard problem the application owns and becomes a property of the data structure. Developers no longer have to reason about clocks, ordering, retries, replication lag, and partial failures every time they update shared state. The math handles it, as long as two replicas eventually exchange state.

For active-active replication, that's a strong fit. Each region accepts local writes at local speed, replicas exchange updates asynchronously, and the data converges without forcing every operation through global coordination.

## How merge behavior changes the problem

CRDTs don't eliminate conflicts. They change the question from "which region wins?" to "what should this data structure preserve when concurrent updates arrive?" and answer it at the data-type level.

For supported operations, the data type already defines what a valid merge looks like:

- **Counters**: Both increments survive, and the final value is the sum of all updates across regions.
- **Sets**: Each region's additions are preserved as separate operations, so the merged set contains the union of all additions.
- **Maps and structures with independent fields**: Concurrent updates to different fields merge cleanly because the operations don't actually conflict.

For data shaped like membership, flags, or accumulated state, those merge rules sit much closer to business intent than discarding one side with Last Write Wins. CRDTs aren't a single technique. They're a family of merge-safe data structures, each with its own conflict rules. That's the layer Active-Active Geo Distribution builds on. Available on [Redis Cloud](https://redis.io/cloud/) and [Redis Software](https://redis.io/software/), it provides multi-region writes with automatic conflict resolution via CRDTs, so local writes happen in multiple regions and replicas converge without application-layer reconciliation.

## A concrete example: the inventory counter problem

Shared inventory counters are one of the clearest ways to see why overwrite-based conflict handling can be dangerous. Picture the SKU from the opening scenario: one unit left, replicated to both regions. The Tokyo customer's order arrives first locally, so the Tokyo region's count drops to 0 and the order proceeds. At nearly the same moment, the Frankfurt region still shows 1 unit (replication hasn't caught up), so the Frankfurt customer's order proceeds there too, dropping Frankfurt's count to 0.

In an overwrite model like Last Write Wins, both regions wrote the same value (0), so the merged count looks completely consistent. The system has no idea anything went wrong. Both orders show up in the database as accepted, the inventory reads zero, and everything looks correct from the application's perspective. But the warehouse only has one unit, so one of those orders won't ship. The data lies cleanly, and the oversell stays invisible until a customer complains.

A CRDT-oriented merge model treats this differently. Instead of writing a new value, each region records its operation: Tokyo issued one decrement, Frankfurt issued one decrement. When the regions exchange state, the math applies both: 1 + (-1) + (-1) = -1. The inventory converges to -1, which is impossible in physical reality, and that impossibility is exactly the point. The negative count is a signal in the data that something needs attention. The application can flag the Frankfurt order, refund the customer, route the order to backorder, or whatever the business rule calls for. The bug doesn't have to wait for a complaint.

That doesn't mean every inventory rule is automatically solved. If your business logic depends on reserving stock before charging a card, or on routing orders to specific fulfillment centers, the application still owns those rules. But for the underlying replication problem, the difference is substantial: supported updates converge by design instead of colliding and waiting for one side to lose.

## Where CRDTs fit (and where they don't)

The inventory counter is one example. The same logic applies anywhere multiple regions independently update something that has a sensible "combine" rule. Stock counts, vote tallies, like buttons, tag sets, audit logs, presence lists, telemetry counters. If the right answer to "what happens when two regions write at once?" is something other than "throw one away," CRDTs probably fit.

That's a strong fit for many real-time application patterns. Redis Cloud and Redis Software apply CRDT semantics [in Active-Active](https://redis.io/active-active/) for strings, hashes, lists, sets, sorted sets, streams, JSON, and HyperLogLog. The merge behavior varies by type: counters and sets converge through commutative operations, hashes merge at the field level, and strings fall back to LWW. The more naturally your workload maps to one of those mergeable types, the more naturally a CRDT-based replication model fits.

It isn't a universal answer, though. Data types outside that list don't get CRDT semantics in Active-Active, so a workload built around them may need a different replication strategy. Some workloads are also about preserving invariants that need tighter coordination, such as financial transfers or uniqueness constraints, where one update has to block, validate, or reject another before commit. Automatic convergence isn't the whole problem there, because the application cares about rules that exist above the level of the data structure. CRDTs don't replace consensus protocols. They're a fit for the subset of problems where merge semantics match the shape of the data.

## Run active-active workloads on Redis

Active-active replication forces trade-offs between write latency, availability, and how you handle conflicting writes when two regions write to the same key. CRDTs change that calculus for supported data types by making convergence a property of the data structure itself. For workloads that fit the model, that's often a better path than naive Last Write Wins or paying inter-region coordination cost on every commit.

[Active-Active Geo Distribution](https://redis.io/active-active/) on Redis Cloud and Redis Software is built on CRDTs, with sub-millisecond local data operations and up to 99.999% uptime when deployed across multiple regions. If you're evaluating active-active replication for a globally distributed app, [try Redis free](https://redis.io/try-free/) to test multi-region writes in your own environment, or [talk to our team](https://redis.io/meeting/) about your architecture.
