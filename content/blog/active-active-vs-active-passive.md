---
title: "Active-Active vs Active-Passive database architecture"
linkTitle: "Active-Active vs Active-Passive database architecture"
url: "/blog/active-active-vs-active-passive/"
description: "Your database is down. Users are hitting errors, revenue is bleeding, and the on-call engineer is staring at a promotion sequence that's taking too long. The architecture decision you made six..."
date: 2026-04-29
blogCategories:
- "Tech DE"
authors:
- "Jim Allen Wallace"
lastmod: 2026-04-29
hidden: true
mirrored: true
---

*By Jim Allen Wallace, Sr. Product Marketing Manager · Published 29 April 2026*

![Active-active vs active-passive: Choosing the right database architecture](/images/site-mirror/21b6c27a9f39a9243833cd3ccc54f9b0756d3129-2400x1256.webp)

Your database is down. Users are hitting errors, revenue is bleeding, and the on-call engineer is staring at a promotion sequence that's taking too long. The architecture decision you made six months ago is now the difference between a brief blip and a full-blown incident.

Active-active and active-passive are two fundamentally different approaches to keeping your database available when things go wrong. This guide covers how each architecture works, the key tradeoffs, and how Redis approaches active-active.

## What "high availability" really means for your database

[High availability](https://csrc.nist.gov/glossary/term/high_availability) means a database keeps serving requests even when individual components fail. It comes from how you engineer the system: redundancy, alternate equipment, and deliberate failover design. [Contingency planning](https://nvlpubs.nist.gov/nistpubs/legacy/sp/nistspecialpublication800-34r1.pdf) ties these pieces together into a plan for keeping systems resilient and recovering quickly when disruptions hit.

The industry measures availability in "nines," and each one costs more than the last.

| Availability level | Max downtime per year | Max downtime per month |
|---|---|---|
| 99% (two nines) | ~87.6 hours | ~7.2 hours |
| 99.9% (three nines) | ~8.76 hours | ~43.8 minutes |
| 99.99% (four nines) | ~52.6 minutes | ~4.4 minutes |
| 99.999% (five nines) | ~5.26 minutes | ~26 seconds |

Here's the thing most teams overlook: [diminishing returns](https://queue.acm.org/detail.cfm?id=3374665). Going from 99.99% to 99.999% is exponentially more expensive to engineer than going from 99% to 99.9%. There's no universally correct tier, only the tier that makes economic sense for your workload.

Two metrics define what recovery looks like for your system. Recovery Time Objective (RTO) is [maximum downtime](https://csrc.nist.gov/glossary/term/recovery_time_objective) before it causes unacceptable business impact. Recovery Point Objective (RPO) is the [recovery point](https://csrc.nist.gov/glossary/term/recovery_point_objective) after an outage, or how much data loss you can handle.

Both RTO and RPO are shaped by your replication architecture. [Replication tradeoffs](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-209.pdf) connect these metrics to a core tradeoff: synchronous replication can help ensure near-zero RPO but adds write latency, while asynchronous replication reduces latency but creates an RPO gap equal to the replication lag at the moment of failure. This is what makes the active-active vs active-passive decision non-trivial.

## What is an active-active database architecture?

One way to push RTO toward zero is to remove the promotion step entirely. Active-active is a database architecture where multiple nodes run at the same time, each accepting reads and writes. There's no single primary, so if one node goes down, the others keep handling traffic without waiting for a standby to take over. It's sometimes called multi-master or bi-directional replication.

The payoff shows up during failures. Every node is already live, so traffic shifts to a healthy node without any promotion step. That's why active-active can reach [much lower RTO](https://www.infoq.com/articles/apache-kafka-stretch-cluster-failures/) than active-passive setups in well-designed deployments.

### Handling concurrent writes

The one thing active-active has to get right is concurrent writes. When multiple nodes accept writes at the same time, two nodes can modify the same record simultaneously, and reverse-order processing can leave the nodes inconsistent if there's no resolution strategy in place.

Two well-understood strategies handle this. Last Writer Wins (LWW) is the simplest: the operation with the most recent timestamp survives. It works for some use cases, but not when both updates carry meaningful information. Conflict-free Replicated Data Types (CRDTs) are more durable: they make operations commutative by construction, so the same set of updates converges to the same final state regardless of application order, with no conflicts to resolve at the application layer.

## What is an active-passive database architecture?

Active-passive takes the opposite approach. It's the traditional high-availability pattern: one primary handles all writes while replicas stand by. If the primary fails, a replica gets promoted to take its place. Some teams call it active-standby or primary-replica.

The appeal is simplicity. One writer at a time means no concurrent-write conflicts to resolve and a straightforward consistency model.

### Easier to rehearse

Active-passive is easier to rehearse. The failover path is fixed (one promotion event and one traffic reroute), so teams can script it, run drills, and document recovery procedures for compliance reviews without much ambiguity about what happens when.

### Failover isn't instant

The cost of that simplicity is downtime during failover. [One practitioner reports](https://www.infoq.com/podcasts/distributed-database-architecture-deepthi-sigireddi/) under 10 seconds for planned failovers with request buffering, and under 30 seconds for unplanned failures. Apps see errors during the unplanned window.

Standbys can also fail when called on. During a [2012 incident](https://queue.acm.org/detail.cfm?id=2655736), high primary load at GitHub triggered a failover to a secondary with a cold cache. It couldn't handle production traffic, and the cluster failed back. The standby had never been exercised under production load.

The failover machinery itself can fail too. The same report found 2.5% of multi-availability-zone databases in U.S. East failed to failover during one protocol bug. Small percentage, complete outage for the teams hit.

## Active-active vs active-passive: key differences & fit

With those failure modes in mind, the choice comes down to your consistency requirements, geographic distribution, and tolerance for downtime.

| Dimension | Active-passive | Active-active |
|---|---|---|
| Write nodes | Primary only | Multiple write-capable nodes |
| Failover mechanism | Heartbeat → promotion → reroute | Traffic rerouting without promotion in some designs |
| RTO | Seconds to minutes in well-tuned hot-standby systems; minutes to hours more generally | Lower than active-passive in well-designed deployments; promotion step removed |
| RPO (async) | Lag-dependent (seconds to minutes) | Can be near-zero in some well-designed deployments; replication-model and network-dependent |
| Write conflicts | None by design | Requires explicit resolution strategy |
| Consistency model | Single-writer by design; consistency depends on replication and read path | Eventual or strong eventual |
| Write scalability | Vertical only | Can scale horizontally, depending on workload, conflict patterns, and implementation |
| Standby utilization | Idle under normal operation | Fully active |
| Resource utilization & cost | Pay for standby capacity that sits idle; lower cost-per-request only if the primary runs below capacity | All nodes serve traffic, so infrastructure investment is used continuously; higher upfront footprint but better cost-per-request at scale |
| Operational complexity | Low | Higher (conflict resolution, topology design) |

### A simple decision framework

Start with your RTO and RPO targets, then layer in geography and budget. A few common scenarios:

- Tight RTO and RPO requirements: Active-active is worth evaluating, especially if a promotion sequence isn't acceptable.
- Seconds-to-minutes RTO acceptable: Active-passive usually works, provided your standby is hot and regularly exercised.
- Users in one region: [Single-writer consistency](/blog/database-consistency/) often tips toward active-passive.
- Users globally distributed: Active-active reduces cross-region write latency.
- Constrained budget, moderate load: Active-passive can be cost-effective when one primary handles typical demand.

One important nuance: these architectures aren't mutually exclusive. A common production pattern is active-active between regions with active-passive within each region.

## Redis Active-Active

When the decision lands on active-active, the implementation choice still matters. [Active-Active Geo Distribution](https://redis.io/active-active), available in Redis Software and Redis Cloud (not Redis Open Source), is built on a Conflict-free Replicated Database (CRDB). A global database in Redis spans clusters where each cluster hosts a CRDB instance, and every write replicates to all other instances via bi-directional mesh replication.

Conflict resolution is where the implementation differs from simpler approaches. Rather than relying on LWW for everything, Redis maps each supported data type to a purpose-built CRDT with [conflict resolution](https://redis.io/docs/latest/operate/rs/databases/active-active/develop/) based on the data type's intent. For example:

- Counters use commutative increment operations that are inherently conflict-free, so concurrent increments from two regions both count.
- Sets use add-wins semantics, where concurrent adds survive concurrent removes.
- Hashes resolve updates to different fields independently, so concurrent updates to different fields in different regions don't create a conflict.

Where these built-in resolutions apply, the CRDT layer handles conflict resolution at the data layer, reducing how much conflict logic the app has to carry.

Redis Active-Active runs on [Strong Eventual Consistency (SEC)](https://redis.io/docs/latest/operate/rs/databases/active-active/causal-consistency/), where every replica reaches the same state once it has seen the same set of updates, with no consensus protocol required. For workloads that need ordering guarantees on specific keys, Redis also supports causal consistency as an optional feature, though enabling it adds network and memory overhead.

For local operations, Redis docs describe [sub-millisecond latency](https://redis.io/docs/latest/operate/rs/databases/active-active/) for reads and writes within each region under typical conditions.

## The right architecture depends on what you can't afford to lose

The choice comes down to what matters most for your workload. Active-passive gives you simplicity and a single-writer model, with brief failover gaps as the tradeoff. Active-active is designed for low RTO, fuller resource utilization, and local write latency in each region.

If brief failover interruptions are acceptable and your users are concentrated in one region, active-passive works. If your users are global, your uptime targets are five nines, or you want to avoid the promotion sequence entirely, active-active is the architecture to evaluate.

Redis builds active-active around CRDTs at the data type level, so the conflict-resolution work most teams hand to application code lives in the data layer instead. That fits teams running real-time workloads where downtime and data loss aren't options.

[Try Redis free](https://redis.io/try-free/) to test Active-Active Geo Distribution with your workload, or [talk to Redis](https://redis.io/meeting/) about architecting high availability for your infrastructure.

## FAQ

### What's the main difference between active-active & active-passive?

Active-active uses multiple write-capable nodes at the same time, while active-passive sends writes to one primary and keeps standby nodes ready for failover.

### Which architecture has faster failover?

In well-designed deployments, active-active can reach much lower RTO than active-passive because traffic can be rerouted without promoting a standby. Active-passive recovery often takes seconds to minutes, depending on how failover is designed.

### Does active-active always mean conflict resolution?

If multiple nodes accept writes at the same time, you need a conflict-resolution strategy. Common approaches include Last Writer Wins (LWW) and CRDTs.

### Can you use active-active & active-passive together?

Yes. A common production pattern is active-active between regions for global availability, with active-passive within each region for local high availability.

### Which is more cost-effective?

It depends on load. Active-passive often wins on cost for workloads where a single primary handles typical demand, since the standby is insurance rather than capacity. Active-active tends to be more cost-effective per request at scale, because every node you pay for is actively serving traffic.

### When is active-passive a better fit?

Active-passive is often a good fit when single-writer consistency on the primary matters most, users are concentrated in one region, and brief failover interruptions are acceptable.

### Does Redis Active-Active remove all application conflict logic?

Not for every workload. Redis can reduce application-side conflict handling for supported data types, but CRDT boundaries still matter for cross-object transactions and unsupported patterns.
