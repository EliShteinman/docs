---
title: "Redis 8.0-M03 is out. Even more performance & new features."
linkTitle: "Redis 8.0-M03 is out. Even more performance & new features."
url: "/blog/redis-8-0-m03-is-out-even-more-performance-new-features/"
description: "We’re happy to announce the third milestone of Redis 8.0, our most advanced and performant offering yet."
date: 2025-02-11
blogCategories:
- "New Product Announcements"
- "Tech"
authors:
- "Lior Kogan"
- "Filipe Oliveira"
lastmod: 2026-08-13
hidden: true
---

*By Lior Kogan, Filipe Oliveira · Published 11 February 2025 · updated 13 August 2026*

![Blog tile image](/images/site-mirror/1f6efed12eb68491020d0ee12a4fbb0e3e4b4714-772x552.webp)

We’re happy to announce the third milestone of Redis 8.0, our most advanced and performant offering yet.

As we progress toward the general availability (GA) release, we’re committed to continuing to roll out new features and improve existing ones.

In the previous milestones, we [introduced](/blog/redis-8-0-m01-released-one-redis-for-every-use-case/) new data structures: JSON, time series, and 5 probabilistic data structures (previously available as separate Redis modules). We also [introduced](/blog/redis-8-0-m02-the-fastest-redis-ever/) significant performance improvements and added the capability to scale the Redis Query Engine both vertically and horizontally. To showcase this new achievement, we created a vector search benchmark with 1 billion [768-dimensions vectorsrunning on a Redis Community Edition cluster](/blog/redis-8-0-m02-the-fastest-redis-ever/).


Now, in CE 8.0 M03 (Milestone 3 pre-release), we’re introducing new additional performance improvements for both single-core and multi-core environments by using a new asynchronous I/O threading implementation along with an improved replication mechanism, delivering better performance and robustness than any previous Redis release.

## More performance improvements than any previous Redis release

In Milestone 3, we introduce additional latency improvements to PFCOUNT, PFMERGE, GET, EXISTS, LRANGE, HSET, LRANGE, and HGETALL. We also improved the performance of CRC64 calculations and commands with a large argument count. That makes Redis 8.0 the Redis release with both the most number of improvements and the absolute most performance increases compared to any previous Redis release.

We have further reduced the latency per command for an even wider set of commands compared to Redis 7.2.5. In our benchmark of 149 tests, 90 delivered latency reduction. The latency reduction ranges from 5.4% to 87.4% with a median of 16.7%.

![](/images/site-mirror/709a3eb9fcaa3b35c6fda9580c456f9d7240f225-2045x1220.webp)

For the complete list of performance improvements, please take a look at the “Performance and resource utilization improvements” sections in the [7.4 RC1](https://github.com/redis/redis/releases/tag/7.4-rc1), [8.0 M01](https://github.com/redis/redis/releases/tag/8.0-m01), [8.0-M02](https://github.com/redis/redis/releases/tag/8.0-m02), and [8.0-M03](https://github.com/redis/redis/releases/tag/8.0-m03) release notes.

## Better multithreading with a new asynchronous I/O threading implementation

Since 6.0, Redis has been able to use I/O threads to handle client requests, including socket reads, socket writes, and command parsing. However, the implementation didn’t capture the full performance benefits.

This release introduces our new I/O threading implementation. The way it works is the main thread assigns clients to specific I/O threads. Each I/O thread notifies the main thread after the client finishes reading and parsing queries. The main thread processes the queries from the I/O threads and generates replies. Then the I/O threads handle writing the replies to the clients.

You can enable this new I/O threading implementation by setting the io-threads configuration parameter. The default value is 1. When the parameter is set to 8 on a multi-core Intel CPU, we’ve measured from 37% to 112% improvement in throughput (contingent on the commands being executed). Additional improvements are expected as we further improve on this engineering effort.

## Replication on Redis clusters is now faster & more robust

When a full synchronization is conducted on a Redis cluster, a primary node is transferred to a replica node. However, while the transfer is taking place, clients can continue sending and getting replies to more commands.


Prior to this release, the primary node buffered commands executed while the Redis transfer took place. After the transfer, the second phase of transferring the stream of changes that occurred in the interim is started from the primary to the replica. This second phase introduces a new problem. The memory required to store the stream of changes on the primary node can often reach its maximum size, causing the replication process to abort and restart.

We’re introducing a completely new mechanism for the replication process. During replication, we initiate two replication streams simultaneously: one stream for transferring the primary node and the other for the stream of changes that happen in the interim. That also means the second phase is no longer blocked and needs to wait for the first phase to complete.

This new replication mechanism offers three major advantages. First, the primary node can handle operations at a higher rate during replication. Second, the size of the buffer required to keep the changes on the primary node is lower since memory demands are now divided between the primary and the replica. Third, replication can be completed faster.

With this new replication mechanism in place, full synchronizations are faster and more robust.

The following chart depicts a full synchronization of a 10 GB dataset where an additional stream of 26.84 million write operations yielded 25 GB of changes that were executed.

![](/images/site-mirror/71281db9c85c06188da49b725ff733a7c72534db-1280x797.webp)

The top chart depicts the execution rate of 26.84 million write operations over time. The blue line is the old replication mechanism pre-Milestone 3 while the red line is the new one introduced in Milestone 3. Observe that with the new mechanism, **the primary can handle write operations at a 7.5% higher average rate during replication **(471.9K versus 438.8K ops/sec).


The bottom chart depicts the replication buffer size over time. The solid purple line is the primary node in the old replication mechanism. The dashed lines are the results from the new mechanism, with purple standing in for the primary node and red for the replica node. In the new mechanism introduced in Milestone 3, **replication takes 18% less time **(101 vs. 123 seconds) and **the peak replication buffer size on the primary node is 35% lower **(15.16 vs. 23.24 GB).


## Redis 8.0-M03 is available now

We’re on an exciting path to the general availability (GA) release of Redis 8.0 and have more to share ahead. For now, you can start experimenting with this milestone by downloading an Alpine or a Debian Docker image from [Docker Hub](https://hub.docker.com/_/redis). Or you can install it by using [snap](https://snapcraft.io/redis) (latest/edge version – v7.9.226) or [brew](https://github.com/redis/homebrew-redis).
