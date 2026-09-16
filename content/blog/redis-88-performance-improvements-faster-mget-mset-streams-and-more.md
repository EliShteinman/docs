---
title: "Redis 8.8 performance improvements: Faster MGET, MSET, streams, & more"
linkTitle: "Redis 8.8 performance improvements: Faster MGET, MSET, streams, & more"
url: "/blog/redis-88-performance-improvements-faster-mget-mset-streams-and-more/"
description: "Every Redis release continues a simple commitment: the same command, on the same hardware, should do more work. Redis 8.6 delivered a step change for vector workloads, sorted sets, and GET-..."
date: 2026-06-02
blogCategories:
- "Tech"
authors:
- "Lior Kogan"
- "Filipe Oliveira"
- "Paulo Sousa"
lastmod: 2026-06-02
hidden: true
mirrored: true
---

*By Lior Kogan, Filipe Oliveira, Paulo Sousa · Published 2 June 2026*

![Redis 8.8 performance improvements Faster string, hash, streams, SCAN & more](/images/site-mirror/0ff729d19ee466bf1707c06bb2a06517d574ee5d-1200x628.webp)

Every Redis release continues a simple commitment: the same command, on the same hardware, should do more work. [Redis 8.6](/blog/announcing-redis-86-performance-improvements-streams/) delivered a step change for vector workloads, sorted sets, and GET-dominated caching paths. Redis 8.8 carries that cadence forward, with the biggest wins landing on the commands that carry most real-world traffic — MGET, MSET, HGETALL, and the SCAN family — alongside meaningful improvements in streams, sorted sets, bitmaps, and the persistence and replication paths.

This post is the performance-focused companion to the Redis 8.8 release announcement. Every number below compares Redis 8.8 to Redis 8.6, the previous stable release.

Benchmarks were run across the latest generation of Intel, AMD, and ARM hardware on AWS, comparing Redis 8.6 and Redis 8.8 with identical builds on both branches. Every gain reported below has been reproduced across multiple runs using our official [OSS SPEC](https://github.com/redis/redis-benchmarks-specification).

The table below summarizes the impact by data type and command family; the rest of the post explains what changed in each case.

## Summary of performance improvements in 8.8

Redis 8.8 introduces significant end-to-end throughput improvements:

| Data type | Operations | end-to-end throughput improvements |
|---|---|---|
| String | MGET  (pipelined, with I/O-threads) | Up to 68% |
|  | MGET  (pipelined, single thread) | Up to 50% |
|  | MSET | Up to 5% |
| Hash | HGETALL | Up to 25% (1K+ fields) |
| Streams | XREADGROUP | Up to 83% (COUNT 100) |
| Sorted set | ZADD, ZINCRBY, ZRANGEBYSCORE | Up to 74% |
| Bitmap | Bitmap operations | Up to 28% (x86) |
| (several) | SCAN, HSCAN, SSCAN, ZSCAN | Up to 40% |

In addition, persistence and replication (full synchronization) is now up to 60% faster.

## The performance improvements explained

### MGET and MSET: up to +68% on pipelined bulk string reads

MGET and MSET are the workhorses of caching. They are also the commands most sensitive to cache-miss latency: every key in a batch means another dict traversal, and the value pointers sit in cache lines that are almost never warm when the command arrives.

[In Redis 8.6](https://github.com/redis/redis/pull/14440) we introduced a memory prefetch framework that let single-key commands hide dict-traversal latency behind useful work. [In Redis 8.8](https://github.com/redis/redis/pull/14899), that framework has been extended to multi-key bulk reads. When a pipelined MGET batch arrives, Redis walks the dict buckets for every key in the batch ahead of time and issues prefetch hints — so by the time each key is looked up, its cache line is already on its way to the CPU. The same idea applies to writes:

MSET and MSETNX now do a batched dict bucket prefetch for groups of keys inside setKey.

Measured on m7i.metal-24xl (x86) vs Redis 8.6:

![Measured on m7i.metal-24xl (x86) vs Redis 8.6](/images/site-mirror/25159fb52bcc5cc700124896401fda68e58ecec9-1624x1004.webp)

The MGET gain is the largest. In pipelined deployments with io-threads, it moves the bottleneck out of Redis' dict traversal and into the network for all but the largest values. There is no new command, no new flag, and no protocol change — upgrading is the entire deliverable.

### HGETALL: up to +25% end-to-end on large hashes

HGETALL improved twice in Redis 8.8, and the improvements stack.

First, HGETALL benefits from a [broader infrastructure change](https://github.com/redis/redis/pull/14754) that extends cross-command prefetching from the pipeline header to the full pending batch — including the deferred-reply object list used by reply-heavy commands. On a 1,000-field hash, that alone lifts HGETALL by +4.6% on x86.

[Second](https://github.com/redis/redis/pull/14988), for hashes large enough to live in the hashtable encoding, a dedicated batched dict bucket prefetch has been added to the field-iteration loop itself. The same mechanism now covers HKEYS and HVALS.

On a 1,000-field hashtable-encoded hash, the two changes compound to approximately +15% to +25% vs Redis 8.6 on x86, depending on pipeline depth and hash field count.

![Improvements on Redis 8.8](/images/site-mirror/4fcaf3587c5d3a9e7a4c0a4c7d85d115c7c7a0bc-1744x1004.webp)

Small, listpack-encoded hashes see the +4.6% from the broader prefetch extension alone — listpack is already cache-resident and does not need the HGETALL-specific prefetch.

### SCAN family: up to +40% on pipelined cursor walks

On every SCAN, HSCAN, SSCAN, and ZSCAN call, the reply callback previously allocated a list-node per matching key — roughly 500 allocations and 500 frees per SCAN COUNT 500 command, all on the hot path. In Redis 8.8, [that linked list is replaced with a stack-allocated vector container](https://github.com/redis/redis/pull/15065), so typical COUNT values generate zero heap allocations on the reply path.

Measured vs current unstable, on both x86 m7i and ARM m8g: SCAN COUNT 500 pipeline-10 gains +38.0% on x86 and +39.7% on ARM.

![Measured vs 8.6, on both x86 m7i and ARM m8g](/images/site-mirror/5e55c458e3adaf94aa78bc39f268c1e58b0a9e1d-1744x1004.webp)

### Streams: up to +83% on large XREADGROUP

Streams see the [largest single improvement](https://github.com/redis/redis/pull/14885) in Redis 8.8. The underlying change rewrites rax — the radix tree Redis uses to index stream entries and consumer-group pending entries — with two specializations tuned for how streams are actually accessed:

- An O(1) append fast path for sequential inserts. Stream IDs are monotonically increasing, so every XADD takes the fast path.
- A last-child-first lookup on descent. For XREADGROUP and range scans, the child you want is almost always the most recently inserted one — walking the child list from the tail eliminates the per-node linear scan.

Measured on Redis 8.6 vs Redis 8.8:

![Measured on Redis 8.6 vs Redis 8.8](/images/site-mirror/4ad5ec5322c2d3c357de25ee72a8305383024483-1744x1004.webp)

## Sorted sets: up to +74% on score-parsing workloads

Redis 8.0 introduced the fast_float library ([#11884)](https://github.com/redis/redis/pull/11884) to accelerate ZADD, ZINCRBY, ZRANGEBYSCORE, GEOADD, and related double-parsing paths. Redis 8.8 goes further on two fronts: the fast_float C++ dependency is replaced with a pure-C implementation, simplifying the build (#14661), and the Clinger fast path has been widened to cover 17-to-19-significant-digit mantissas via a single 128-bit multiply (#15061).

On the canonical sorted-set-with-double-scores load benchmark:

![Redis 8.8](/images/site-mirror/660f74278e4a91e9079a3e72dfab88a63476840d-1744x1004.webp)

This matters for any ZADD, ZINCRBY, or ZRANGEBYSCORE workload with double-precision scores — leaderboards, time-series secondary indexes, and any pattern where scores come from timestamps or client-side float-to-string conversions.

## Bitmap operations: AVX-512 on modern x86

BITOP AND, OR, XOR, and NOT are now vectorized with AVX-512 on Ice Lake and newer Intel and AMD CPUs. Upstream measurements show up to +80% on value sizes of 10,000 bytes and above, with smaller gains on shorter values where the fixed dispatch overhead does not amortize.

![Bitmap operations: AVX-512 on modern x86](/images/site-mirror/d7ed5658bf741c24e84a5f1f31cf7663b9f1bc64-1744x1004.webp)

## Persistence and replication: Faster full sync, lower BGSAVE overhead

Redis 8.8 trims cost across several operational paths. [Diskless full sync is the most visible win](https://github.com/redis/redis/pull/14851): because the replication link already provides integrity, the RDB checksum computation and validation are no longer performed on diskless transfers, cutting a 12 GB full-sync on a c8g.2xlarge replica from 35 seconds to 11 seconds — a 68% reduction.

BGSAVE and full sync also pay less in the fork child. [Dict bucket arrays are now released back to the OS with MADV_DONTNEED](https://github.com/redis/redis/pull/14979), reducing the RSS spike and copy-on-write amplification during snapshotting, and memory tracking — which the child never used — [is now disabled there](https://github.com/redis/redis/pull/14928).

[Replication itself is lighter on the wire-feed path](https://github.com/redis/redis/pull/15003): the per-write bookkeeping in feedReplicationBuffer() has been reworked, so high-argument commands (HSET with many fields, MSET with many keys) pay less overhead on every replicated write. Pipelined SET, HSET, and ZADD with a replica attached measure between +3% and +26% faster. In addition, [primary and replica clients are now serviced inside I/O threads](https://github.com/redis/redis/pull/14335), shifting more of the replication path off the main thread.

## Getting started

All these enhancements are generally available on Redis 8.8 open source today. You can start using the new commands by [downloading Redis 8.8](https://redis.io/downloads/) and experimenting with them in your existing workflows.

Have feedback or questions? Join the discussion on our [Discord server](https://discord.gg/redis) or reach out to your account manager.
