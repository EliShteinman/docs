---
title: "What’s new in two – November edition"
linkTitle: "What’s new in two – November edition"
url: "/blog/whats-new-in-two-november-edition/"
description: "Click here to view video"
date: 2024-11-27
blogCategories:
- "Tech"
authors:
- "Talon Miller"
lastmod: 2025-07-03
hidden: true
---

*By Talon Miller, Principal Technical Marketer · Published 27 November 2024 · updated 3 July 2025*

![Blog tile image](/images/blog/ecfa1006ca666079c1d88d32291f590577f8223f-1544x1104.webp)

[Click here to view video](https://www.youtube.com/embed/F_sXNogoV_U?si=iyZ2_FgmcrrJ_kWf)

Welcome to “What’s new in two,” the place to catch up on Redis releases you might have missed in the past month. We’re covering the latest developments from November, expanding on what I covered in our latest video—press play above if you prefer to watch a recap of this month’s updates. Let’s get started.

## Redis 8.0-M02

We’re happy to announce [Redis 8.0-M02](/blog/redis-8-0-m02-the-fastest-redis-ever/). Now available in Community Edition, our second milestone builds on the new data structures introduced in M01 (JSON, time series, and probabilistic types) by delivering major performance gains and advanced scaling features. Commands like ZADD, SMEMBERS, and HGETALL show up to 36% lower latency, benefiting over 70% of Redis users.

Redis CE 8.0 now supports horizontal and vertical scaling for the Redis Query Engine. It powers high-throughput search and vector operations for datasets up to a billion vectors, with configurations fine-tuned for both precision and speed. Try Redis 8.0-M02 as a [Docker image](https://hub.docker.com/_/redis) on Alpine or Debian.

## Redis Software 7.8.2 release

Introducing the general availability of Redis Software 7.8.2! This new version comes with many new features and updates, like support for Redis Community Edition 7.4 with hash field expiration, significant memory reduction for the Redis Query Engine for vector use cases, and client-side caching. For administrators, this release comes with new compliance enhancements, new database management APIs, improved observability, expanded cluster manager UI functionality, and much more. Check out the [release notes](https://redis.io/docs/staging/release-rs-fuya-fuya/operate/rs/release-notes/rs-7-8-releases/rs-7-8-2-34/) to get started.

## Introducing Azure Managed Redis

On November 19, we announced Azure Managed Redis, a new, fully managed Redis solution developed in close collaboration with Microsoft Azure. Now available in public preview, Azure Managed Redis (AMR) provides Microsoft Azure customers with a licensed, multi-tiered Redis service—the first major cloud service provider to do so.

AMR now brings Redis 7.4, the latest and fastest version of Redis to Microsoft Azure. AMR includes all the powerful features of Redis Enterprise, such as 99.999% availability, top-tier security, and seamless integration with Azure AI and the Redis Vector Library, featuring 30+ ecosystem integrations like LlamaIndex and Langchain. It also offers the Redis Query Engine for full-text and vector search, Redis Insight for optimal management, and more than 30% cost savings over the previous Azure Cache for Redis option.

If you’re not an existing Azure Cache for Redis customer or a Microsoft Azure customer, reach out to us [here](https://redis.io/meeting/) to get started.

## New Redis Insight course at Redis University

Redis University has launched a new Redis Insight course. Participants will learn to explore and interact with their Redis data using Redis Insight’s powerful analysis tools, workbench, and intuitive data displays.

The course covers optimizing data with features like the slow log and profiler to monitor and troubleshoot performance, as well as boosting productivity with Redis Copilot for AI-driven assistance, bulk actions, and in-depth tutorials.

With engaging demos and hands-on labs, students will gain practical skills using Redis Insight’s tools to build and manage apps faster and with more confidence. Check out the [Redis University](https://university.redis.io/course/ibjgkshzhox41u) to learn more or go directly to this [Redis Insight course](https://university.redis.io/course/ibjgkshzhox41u).

## JSON and Search support for go-redis client library

The go-redis client library now supports advanced data modeling capabilities, including secondary indexing, JSON documents, and powerful search features. These updates bring it closer to providing the full suite of Redis Community Edition (Redis Stack and Redis 8), Redis Software, and Redis Cloud capabilities.

With JSON support, go-redis handles flexible data management for complex, hierarchical data structures. The Redis query engine adds indexing for both hash and JSON documents, making data retrieval faster and more efficient. To explore these new features, you can create a [free Redis Cloud](https://redis.io/try-free/) account or experiment with Redis 8 M02 on [Docker Hub](https://hub.docker.com/_/redis), or [install](https://redis.io/docs/latest/operate/oss_and_stack/install/install-stack/) it on your machine.

That wraps up this month’s “What’s new in two.” We’ve covered the latest Redis features and improvements from November. Whether you prefer watching or reading, catch more valuable updates in my next two-minute episode. December releases are just around the corner, so stay tuned. And if you missed [last month’s update](https://youtu.be/c5L1MQl6Ymo), two minutes is all you need to catch up.
