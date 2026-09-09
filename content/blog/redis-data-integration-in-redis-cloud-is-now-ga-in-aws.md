---
title: "Redis Data Integration in Redis Cloud is now GA in AWS"
linkTitle: "Redis Data Integration in Redis Cloud is now GA in AWS"
url: "/blog/redis-data-integration-in-redis-cloud-is-now-ga-in-aws/"
description: "Today, we’re announcing the general availability of Redis Data Integration (RDI) in Redis Cloud on AWS."
date: 2026-06-08
blogCategories:
- "Tech"
authors:
- "Pieter Cailliau"
- "Mirko Ortensi"
lastmod: 2026-06-08
hidden: true
---

*By Pieter Cailliau, Mirko Ortensi · Published 8 June 2026*

![Redis Data Integration in Redis Cloud is now GA in AWS](/images/blog/ad672731ed83408d2919f3d3137c55e45532d7f6-1200x628.webp)

Today, we’re announcing the general availability of Redis Data Integration (RDI) in Redis Cloud on AWS.

RDI in Redis Cloud is our fully-managed service for moving operational and analytical data into Redis in near real time and keeping Redis continuously in sync with your source databases and data warehouses.

Many of those source systems can't deliver the scale or latency that real-time apps, APIs, models, and agents need. RDI is purpose-built for that path: it continuously streams updates from the source into Redis and applies native transformations that convert source records into Redis data structures optimized for sub-millisecond reads and high-scale throughput.

Over the last several months since our [Redis Cloud preview](/blog/redis-cloud-aws-reinvent-2025/), customers have validated that this is the product they want when they need a simpler, Redis-native path from systems of record to fast and linearly scalable read workloads in Redis Cloud.

That matters because RDI is more than “data ingestion.” It is how customers transform slow operational and analytical data into a fast data layer for modern apps, real-time decisioning, and AI workloads.

## How RDI makes source data Redis-fast

RDI implements the two phases of the pipeline lifecycle: an initial bulk hydration that loads the source into Redis, and ongoing near-real-time CDC that keeps Redis continuously in sync as the source changes. That gives customers a consolidated Redis product for the job they actually need done: define, validate, run, and monitor source-to-Redis pipelines without managing the underlying integration infrastructure themselves.

![How RDI makes source data Redis-fast](/images/blog/83d362c70e1363a33a8fd3f7be7aa680b8474327-1022x600.webp)

Redis becomes the low-latency serving layer for data that lives in your system of record, decoupling read traffic from the source database. That means no cache misses, fresher data, less pressure on source databases, a lower total cost of ownership, and a much simpler path to building real-time apps on top of Redis Cloud.

## Bringing key RDI advances to Redis Cloud

RDI in Redis Cloud GA brings many of the key improvements introduced with [RDI 1.18](https://redis.io/docs/latest/integrate/redis-data-integration/release-notes/rdi-1-18-0/) into the managed Redis Cloud experience, making the service fast, easy to operate, and aligned with production data pipeline needs.

Highlights include:

- **Better CDC latency and throughput**, plus faster full hydration throughput through a new processor that improves full-sync performance.
- **Fast, self-service pipeline management** with early validation of source connectivity, secrets, and source readiness. Includes actionable error messages during pipeline creation, private connectivity setup, and monitoring, along with clearer pipeline states and more accurate status reporting.
- **Advanced source and processor configuration** for pipelines that need more control.
- **Support for snapshot SQL statements**, so users can ingest only part of the source data when they need a more selective initial load.
- **New source support for Snowflake** (in preview) **and** **MongoDB** in Redis Cloud.
- **CAPI support**, so users can provision RDI infrastructure through API and Terraform and automate it like other Redis Cloud services.

In short, RDI in Redis Cloud GA introduces the latest performance and user experience improvements, and is aligned with how cloud teams want to build and operate production data paths.

## New source support: MongoDB & Snowflake

A key highlight of this GA release is that RDI in Redis Cloud builds on established support for relational sources including MySQL, MariaDB, Oracle, SQL Server, and PostgreSQL, while also expanding beyond relational databases with especially strong support for Snowflake (in preview) and MongoDB.

Snowflake expands RDI into reverse ETL and feature-store style use cases, where precomputed data can be synced into Redis Cloud for low-latency serving. MongoDB is a natural fit for app acceleration because JSON data often maps cleanly into Redis, avoiding the joins and denormalization work that can limit the use cases from relational sources.

Together, they show that RDI in Redis Cloud is not limited to traditional relational ingestion. It now supports a broader set of operational and analytical sources for app modernization and real-time decisioning.

## Why RDI matters for agents

[Redis Iris](/blog/context-is-all-you-need/) is our real-time context engine for agents, and RDI is one of its foundational building blocks. In Iris, RDI continuously syncs data from your source databases and data warehouses into Redis, so agents retrieve context in real time while systems of record stay where they are. Without that sync, agents act on stale reads— yesterday's account state, last hour's order status — not the current state of the business.

RDI is especially crucial for feature store and reverse ETL scenarios. A feature store only delivers value if the serving layer has fresh features at decision time. A reverse ETL flow only helps if the data arrives in the operational path quickly enough to influence what the app, model, or agent does next.

![Redis Data Integration Blog](/images/blog/4031646c421b5532400980d5854113c96e3b05f6-1339x855.webp)

RDI is what turns data that lives elsewhere into live, actionable context inside Redis. That live context is the difference between systems that are simply connected and systems powering real-time apps and agents.

## Learn more

RDI is available today in Redis Cloud on AWS, bringing Redis-native, managed data pipelines to the same platform teams already use for fast, reliable, production Redis services.

If you want to learn more about Redis Data Integration, visit the [RDI overview page](https://redis.io/data-integration/), read the [Redis Cloud quick start](https://redis.io/docs/latest/rc/rdi/), and explore how it fits into the [Redis Iris](https://redis.io/iris/) vision for real-time context.
