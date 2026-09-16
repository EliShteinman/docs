---
title: "Announcing Redis 8.10: Compact Hash, JSONPath extensions, performance improvements, & more"
linkTitle: "Announcing Redis 8.10: Compact Hash, JSONPath extensions, performance improvements, & more"
url: "/blog/announcing-redis-810-compact-hash-jsonpath-extensions-performance-improvements-and-more/"
description: "Redis 8.10 in Redis Open Source is now available, delivering improvements that make Redis more memory efficient, expressive, and easier to operate at scale."
date: 2026-09-14
blogCategories:
- "Tech"
authors:
- "Bosmat Tuvel"
- "Lior Kogan"
lastmod: 2026-09-15
hidden: true
mirrored: true
---

*By Bosmat Tuvel, Lior Kogan · Published 14 September 2026 · updated 15 September 2026*

![Announcing Redis 8.10: Compact Hash, JSONPath extensions, performance improvements, & more](/images/site-mirror/0d28d428a9cfcac4321833e6e008c2752ebab5f9-1200x628.webp)

Redis 8.10 in Redis Open Source is now available, delivering improvements that make Redis more memory efficient, expressive, and easier to operate at scale.

Highlights include compact hashes with up to 50% lower memory usage and 2× higher hash loading throughput, incremental backup and restore, JSONPath syntax extensions, more flexible Stream consumption, new Set cardinality operations, atomic movement of multiple List elements, and enhanced Time Series capabilities.

## Why Redis 8.10 matters

Redis 8.10 focuses on three areas: improving efficiency, expanding the capabilities of Redis data structures, and simplifying operations for production deployments.

On the performance side, compact hashes and stream optimizations reduce memory usage while increasing throughput, helping applications get more from existing infrastructure. Several new commands and enhancements across RedisJSON, Streams, Lists, Sets, and TimeSeries also make common operations more expressive, reducing application complexity and the number of round trips required to accomplish everyday tasks.

For operators, the introduction of incremental backup and restore makes it possible to create coordinated cluster backups with significantly lower impact on running workloads, improving reliability for large Redis deployments.

Let's take a closer look at each of these additions.

### Performance highlights

Beyond the new features, Redis 8.10 includes several performance optimizations that improve both throughput and memory efficiency across hashes and streams. The highlights are summarized below:

| Data type | Operations | Benefit |
|---|---|---|
| Hash | HSET, HMSET on wide, fresh hashes | Up to [[bold]]104% higher throughput[[/bold]] |
| Hash | Keys sharing field-name schemas | Up to [[bold]]50% lower memory usage[[/bold]] |
| Streams | XREADGROUP | Up to [[bold]]28% higher throughput[[/bold]] (COUNT 100) |
| Streams | Deep Streams | Up to [[bold]]26% lower memory usage[[/bold]] |

Beyond these performance gains, Redis 8.10 introduces several new capabilities across data structures, RedisJSON, RedisTimeSeries, Streams, and data management.

## What’s new in Redis 8.10

### Compact Hash

Applications commonly create large numbers of hashes with the same fields — for example, millions of user profiles containing `name`, `email`, `country`, and `last_login`. Traditionally, each hash stores its own copy of those field names.

Redis 8.10 introduces **hash templates**, a new internal encoding that allows hashes to share a common field-name set while keeping their values independent. For workloads with many similarly structured hashes, this can reduce memory usage by up to 50%.

Redis 8.10 also introduces `HIMPORT`, designed for efficient bulk ingestion of hashes with the same fields. A client prepares the field set once:

```
HIMPORT PREPARE user-profile name email country last_login
```

It can then load hashes by sending only their values:

```
HIMPORT SET user:1 user-profile "Alice" "alice@example.com" "UK" "2026-07-14"

HIMPORT SET user:2 user-profile "Bob" "bob@example.com" "US" "2026-07-14"
```

Because field names aren't repeatedly sent and parsed for every hash, `HIMPORT` reduces network and server-side processing overhead, enabling up to 2× higher hash loading throughput.

Existing hash commands continue to work with the same semantics. Operators can also opt in to automatic template conversion for eligible hashes without changing applications to use `HIMPORT`.

Hash templates work best when many hashes share a stable field set, making them particularly useful for user profiles, sessions, feature stores, bulk imports, and ETL workloads.

### JSON: More expressive JSONPath queries

Redis JSON uses JSONPath expressions to access and manipulate specific parts of JSON documents without retrieving the entire document.

Redis 8.10 significantly extends JSONPath syntax, allowing applications to perform more filtering, calculations, aggregation, and data processing directly in Redis.

New capabilities include:

- Arithmetic and comparison operators
- `in`, `nin`, and filter negation
- Operations on strings, arrays, objects, and nodelists
- String functions such as `match()`, `search()`, and `concat()`
- Array functions such as `first()`, `last()`, `append()`, and `index()`
- Aggregations including `min()`, `max()`, `avg()`, `sum()`, and `stddev()`
- Functions such as `length()`, `count()`, `keys()`, and `value()`

For example:

```
JSON.GET key '$.price * 0.8'

JSON.GET key '$.arr1.avg()'

JSON.GET key 'count($.items[?@.price > 10])'
```

This added expressivity allows applications to move more filtering and post-processing into Redis, reducing data transfer and simplifying application code.

### Streams: Control the total size of XREAD results

`XREAD` and `XREADGROUP` already support `COUNT`, but the limit applies independently to each Stream. When reading from many Streams—or Streams containing large entries—the overall response can still become very large.

Redis 8.10 adds two new options:

- `MAXCOUNT`: limits the total number of messages returned across all Streams.
- `MAXSIZE`: limits the overall reply size in bytes.

For example:

```
XREAD COUNT 100 MAXCOUNT 200 STREAMS stream:1 stream:2 stream:3 0 0 0
```

The command can read up to 100 messages from each Stream while returning no more than 200 messages overall.

These controls help applications bound network transfer and memory consumption and avoid unexpectedly large replies.

### Sets: Get union and difference cardinality without retrieving members

Applications frequently use Sets to represent groups such as user segments, permissions, product categories, or search filters. Often, they need to know **how many** elements match an operation without retrieving the elements themselves.

Redis already provides `SINTERCARD` for Set intersections. Redis 8.10 adds the equivalent operations for unions and differences:

```
SUNIONCARD numkeys key [key ...] [APPROX] [LIMIT limit]

SDIFFCARD numkeys key [key ...] [LIMIT limit]
```

`SUNIONCARD` returns the cardinality of a union, while `SDIFFCARD` returns the cardinality of the difference between the first Set and subsequent Sets.

This avoids returning potentially large collections to the client or creating temporary Sets simply to count their members. `SUNIONCARD` can also use `APPROX` for a fast HyperLogLog-based estimate with a 0.81% standard error.

### Lists: Move multiple elements atomically

Redis Lists are commonly used for queues, stacks, and processing pipelines. `LMOVE` and `BLMOVE` already allow applications to atomically move a single element between Lists, but many workflows need to claim or transfer multiple elements at once.

Redis 8.10 introduces:

```
LMOVEM source destination <LEFT|RIGHT> <LEFT|RIGHT>
       [<COUNT|EXACTLY> count <OBO|BULK>]

BLMOVEM source destination <LEFT|RIGHT> <LEFT|RIGHT> timeout
        [<COUNT|EXACTLY> count <OBO|BULK>]
```

The new commands atomically move multiple elements from one List to another.

`COUNT` moves up to the requested number of elements, while `EXACTLY` moves the batch only when the full requested number is available. Applications can also choose between one-by-one (`OBO`) ordering and `BULK` ordering, which preserves the relative order of the moved elements.

This is useful for batch job claiming, queue processing, pipeline handoffs, retry queues, and other workflows where groups of elements must move together.

### Time Series: Query multiple series by timestamp

Related Time Series are often stored separately even though they share timestamps. Financial OHLCV data, for example, may use separate series for open, high, low, close, and volume.

`TS.MRANGE` returns results grouped by Time Series, which means applications that need timestamp-aligned data often have to reorganize the results themselves.

Redis 8.10 introduces `TS.NRANGE` and `TS.NREVRANGE`, which query an explicit set of Time Series and return the results grouped by timestamp:

```
TS.NRANGE 5 {ACMZ}:open {ACMZ}:high {ACMZ}:low
            {ACMZ}:close {ACMZ}:volume
            <fromTimestamp> <toTimestamp>
```

Because the keys are specified explicitly, labels aren't required. In Redis Cluster, all specified keys must belong to the same hash slot.

The commands also support per-series aggregators, allowing applications to apply different aggregation functions to different Time Series in the same query.

This makes timestamp-aligned data easier to consume for financial applications, analytics pipelines, monitoring dashboards, and machine-learning feature extraction without requiring client-side pivoting.

### Time Series: Wait for new data with blocking reads

Applications that display live Time Series data often poll Redis repeatedly to determine whether new samples have arrived.

Redis 8.10 introduces `TS.READ`, an optionally blocking command that allows applications to wait for new samples:

```
TS.READ key timestamp
        [BLOCK milliseconds min_count]
        [MAX_COUNT max_count]
```

Instead of continuously issuing range queries, an application can block until a minimum number of samples becomes available or the specified timeout expires.

`TS.READ` is useful for live dashboards, monitoring systems, financial applications, alerting, and IoT workloads that continuously consume new Time Series data.

### Time Series: Exclude empty results

`TS.MRANGE` and `TS.MREVRANGE` can return Time Series that match a filter but contain no samples in the requested time range.

Redis 8.10 adds the `EXCLUDEEMPTY` flag:

```
TS.MRANGE - 500 WITHLABELS EXCLUDEEMPTY FILTER s=1
```

With `EXCLUDEEMPTY`, matching Time Series that have no samples in the requested range are omitted from the response, reducing unnecessary result data and client-side filtering.

### Incremental backup and restore

Backing up large Redis Cluster deployments can be resource intensive. Creating an RDB snapshot requires Redis to fork, and when multiple shards on the same node fork simultaneously, CPU and memory usage can spike, slowing workloads or causing backups to fail.

Redis 8.10 introduces **incremental backup and restore**, built around the new `BACKUP` command family.

Instead of requiring every shard to capture its snapshot simultaneously, snapshots can be staggered across shards while still producing a coordinated backup. Each backup begins with a point-in-time RDB snapshot (**BASE**). Redis then records subsequent writes in incremental (**INCR**) AOF files while the backup remains open.

When the backup is sealed, the RDB snapshot, incremental AOF files, and manifest form a complete backup representing the dataset at the end of the backup window. Sealing doesn't require another fork, allowing shards to be finalized together even when their snapshots were created at different times.

For restore, the new `preload-file` startup option can load either a sealed backup manifest or a standalone RDB file.

The result is a more scalable backup process with lower resource spikes, particularly for large deployments with multiple shards per node.

## Getting started

Redis 8.10 is generally available in Redis Open Source.

[Download Redis 8.10](https://redis.io/downloads/) to try the new capabilities in your applications.

Have feedback or questions? Join the discussion on our [Discord server](https://discord.gg/redis) or reach out to your account manager.
