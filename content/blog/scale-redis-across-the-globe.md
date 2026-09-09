---
title: "Learn How to Scale Redis Across the Globe in 90 Seconds"
linkTitle: "Learn How to Scale Redis Across the Globe in 90 Seconds"
url: "/blog/scale-redis-across-the-globe/"
description: "We love technical articles that go deep. However, sometimes you’re on the go and need a quick summary to get the gist of something. This is why we’re continuing our “Redis in 90 Seconds” series..."
date: 2021-12-28
blogCategories:
- "Tech"
authors:
- "William Johnston"
lastmod: 2025-03-27
hidden: true
---

*By William Johnston, Head of Technical Marketing · Published 28 December 2021 · updated 27 March 2025*

![Blog tile image](/images/blog/a604f93a719583f870b14efeb765b4ddaef0db8b-772x550.webp)

We love technical articles that go deep. However, sometimes you’re on the go and need a quick summary to get the gist of something. This is why we’re continuing our “[Redis in 90 Seconds](/blog/learn-how-redis-simplifies-your-architecture-in-90-seconds/)” series with a short post about how to scale Redis.

## How to scale Redis with Active-Active Geo-Distribution using CRDTs

In today’s world, enterprise workloads can be very demanding. Enterprise customers demand low latency and fast failover with no data loss. Enterprise applications need to be distributed globally while minimizing latency.

You might think throwing Redis on top of your existing database might solve this problem. Unfortunately, it only solves part of the problem. This is because most Redis providers simply host Redis OSS. They provide Redis as a cache, but not as an enterprise-grade real-time database.

Redis Enterprise provides 99.999% uptime, sub-millisecond latency, [single-digit-seconds failover](/redis-enterprise/technology/highly-available-redis/), [Active-Active Geo-Replication](/active-active/), and [no data loss](/redis-enterprise/technology/durable-redis-2/). It’s the only Redis provider that can meet the demands of enterprise customers.

For example, with Redis Enterprise you can have multiple primaries spread across the globe and provide local, sub-millisecond latencies for both **reads and writes**. In order to avoid any write conflicts, Redis Enterprise uses the cutting edge Active-Active Geo-Replication feature that’s based on conflict-free replicated data types (CRDTs). Similarly, Redis Enterprise provides [enterprise clustering](/redis-enterprise/technology/redis-enterprise-cluster-architecture/), [Redis on Flash](/docs/benchmarking-redis-in-full-acid-configuration-on-emc-vmax-0-5-million-opssec/), and many other native functions that address the enterprise solutions you won’t find anywhere else.

Watch the video below to see Redis Enterprise in action:

[Click here to view video](https://www.youtube.com/embed/mCOX-2ez-m4)

## Next Steps
