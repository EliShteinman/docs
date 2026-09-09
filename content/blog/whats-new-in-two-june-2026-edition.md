---
title: "What’s new in two: June 2026 edition"
linkTitle: "What’s new in two: June 2026 edition"
url: "/blog/whats-new-in-two-june-2026-edition/"
description: "Click here to view video"
date: 2026-07-06
blogCategories:
- "Tech"
authors:
- "Talon Miller"
lastmod: 2026-07-06
hidden: true
---

*By Talon Miller, Principal Technical Marketer · Published 6 July 2026*

![What’s new in two: June 2026 edition](/images/blog/2697060446aca394f1a252c820023ff9f7d5c6c0-1200x628.webp)

[Click here to view video](https://youtu.be/f_i7C-yJYgE?si=fUcZWNc9KqNwA1Wo)

Welcome back to “What’s new in two,” your quick hit of Redis releases you might’ve missed over the last month. Summer might be here, but product releases apparently don't take vacations. We're covering the biggest updates from June and expanding on what I covered in the latest video. Prefer the faster version? Hit play and watch instead.

## Redis Data Integration arrives in Redis Cloud

One of the biggest updates this month is the general availability of [Redis Data Integration](https://redis.io/data-integration/) (RDI) in Redis Cloud on AWS.

Keeping app data fresh sounds simple until you're stitching together ETL jobs, change data capture tools, message brokers, and enough custom code to make future-you question every life decision that led to this architecture.

RDI gives you a simpler path. It continuously syncs data from operational systems into Redis, keeping apps, services, and AI workloads working from current business data instead of yesterday's snapshot.

That's especially important for AI agents. As part of Redis Iris, our context engine for AI agents, RDI helps keep the operational context inside Redis up to date so agents can retrieve current information, make better decisions, and act on what's happening right now, not what happened three hours ago.

The GA release includes faster pipeline provisioning, improved pipeline visibility, better error reporting, higher sync performance, advanced source configuration options, and management through the Redis Cloud REST API.

We also added support for MongoDB and preview support for Snowflake. That opens up two especially useful patterns.

The first is MongoDB application acceleration. Many customer-facing apps depend on MongoDB, but scaling reads can get expensive fast. RDI continuously syncs operational data into Redis so apps can serve hot data from Redis while reducing pressure on the primary database.

The second is real-time decisioning with Snowflake. Teams already generating features and business signals in Snowflake can move that data into Redis and serve it with sub-millisecond latency for personalization, recommendations, fraud detection, and AI-driven workflows.

During preview, customers used RDI to simplify data movement, reduce database load, eliminate stale cache problems, and support production workloads without introducing additional infrastructure layers. Check out the [docs](https://redis.io/docs/latest/operate/rc/rdi/) to learn more.

## More control over cost & performance with Flex

We also introduced a major update to [Flex](https://redis.io/solutions/flex/).

Flex already helps you reduce infrastructure costs by automatically keeping hot data in RAM while storing warm data on flash. The result is a larger effective dataset size without paying all-RAM prices.

Now we're giving customers more control over how that balance works.

New Flex subscriptions can choose a tunable RAM-to-Flash ratio ranging from 10% to 50% RAM. Need maximum throughput? Increase the RAM allocation. Looking to optimize cost for larger datasets? Shift more capacity toward flash.

Instead of forcing every workload into the same memory profile, customers can tune Flex to match the performance and economics their application needs.

The update also extends Flex pricing to BYOC deployments for the first time, giving organizations more deployment flexibility while maintaining the same cost optimization benefits.

For teams managing large datasets, growing AI workloads, or cost-sensitive production environments, Flex now offers more ways to find the right balance between performance and spend. [Try Redis Cloud for free](https://redis.io/try-free/) or learn how to set up a Flex database on Redis Cloud on the [docs](https://redis.io/docs/latest/operate/rc/databases/create-database/create-flex-database/).

That's a wrap on this month's updates. Whether you prefer watching or reading, catch more valuable updates in my next two-minute episode. See you next time.
