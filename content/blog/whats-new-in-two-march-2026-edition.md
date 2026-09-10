---
title: "What’s new in two: March 2026 edition"
linkTitle: "What’s new in two: March 2026 edition"
url: "/blog/whats-new-in-two-march-2026-edition/"
description: "Click here to view video"
date: 2026-03-31
blogCategories:
- "Tech"
authors:
- "Talon Miller"
lastmod: 2026-03-31
hidden: true
mirrored: true
---

*By Talon Miller, Principal Technical Marketer · Published 31 March 2026*

![What’s new in two – March 2026 edition](/images/site-mirror/ec70110fb6de0b599bbbd23dd6e0e62b249b006c-1200x628.webp)

[Click here to view video](https://youtu.be/sAEh2n5Puec)

Welcome to “What’s new in two,” your quick hit of Redis releases you might have missed in the past month. If you blinked, you missed it—so here’s the recap. We’re covering the latest developments from February and March and expanding on what I covered in our latest video. Press play to watch it instead.

## Redis 8.6 is now GA in open source

Redis 8.6 is now generally available in Redis Open Source, delivering major gains in performance, operational visibility, and event-stream reliability. This release strengthens Redis as the fastest real-time data platform and introduces new capabilities that will flow into Redis Cloud and Redis Software.

### Performance at scale

Redis 8.6 delivers significant improvements in throughput, latency, and memory efficiency—making it the fastest in-memory database in its class.

These optimizations translate directly into:

- Lower latencies on the same hardware
- Higher throughput per node
- Reduced infrastructure costs through improved memory efficiency

For teams running large-scale caching, AI inference pipelines, and real-time systems, 8.6 means more performance headroom without adding hardware.

### Stronger, production-ready Streams

Streams continue to mature in Redis 8.6, reducing operational complexity and edge-case failure modes in event-driven architectures.

Improvements make it easier to:

- Operate resilient consumer groups
- Recover from failure scenarios
- Run real-time pipelines with fewer workarounds

The result is simpler, more reliable event-driven systems for financial services, media streaming, and AI-driven workflows.

### Easier to operate in production

Redis 8.6 improves visibility into runtime behavior with better tooling to identify and diagnose hot key issues—one of the most common real-world scaling challenges.

New eviction policies also make memory behavior more predictable for modern workloads, helping teams manage growth without surprise performance degradation.

### Cleaner time series handling

Redis 8.6 introduces native support for missing time series values, preventing broken aggregations and simplifying analytics pipelines. This makes Redis even more reliable for financial systems, observability platforms, and telemetry-heavy workloads.

Redis 8.6 is [available now](https://redis.io/downloads/) in Redis Open Source and will roll into Redis Cloud and Redis Software in upcoming releases. Dive deeper into all that’s in Redis 8.6 [here](/blog/announcing-redis-86-performance-improvements-streams/).

## Redis 8.4 is now GA in Redis Cloud

Redis 8.4 is now available on Redis Cloud Essentials and Pro, bringing a fully unified Redis experience where capabilities like Search, JSON, TimeSeries, Bloom, and vector data types are built in—no modules required. This release introduces powerful improvements across cluster operations, search and vector ranking, and performance, including hybrid search with FT.HYBRID, atomic cluster slot migration for zero-downtime scaling, and SIMD-driven optimizations for faster workloads.

### Developer & Operational Enhancements:

Redis 8.4 adds new primitives for building safer and more efficient applications, including native compare-and-set semantics, multi-key TTL operations with MSETEX, and improved stream processing for consumer groups. Combined with automatic AOF repair and smarter query scoring, these updates make Redis Cloud more resilient, performant, and easier to operate at scale.

## New Redis Agent Skills

We’ve introduced [Redis Agent Skills](https://github.com/redis/agent-skills), a growing set of pre-built capabilities that make it easier for AI agents to interact with Redis for memory, retrieval, and real-time data workflows. These skills help developers quickly integrate Redis into agent frameworks, reducing setup time and making Redis a natural default for stateful AI applications.

## New Redis Cursor Plugin

The new [Redis plugin for Cursor](https://cursor.com/marketplace/redis) brings Redis directly into the AI coding workflow, enabling developers to seamlessly generate, connect, and build with Redis from within their editor. By embedding Redis into code generation and development flows, it becomes faster and more intuitive to incorporate Redis into modern AI-powered applications.

## Cloud metrics resolution update

Redis Cloud now dynamically adjusts metric resolution based on the selected time range, delivering high-fidelity data for short-term analysis and aggregated views for long-term trends. This update simplifies the monitoring experience while ensuring charts remain clear, actionable, and aligned with modern observability best practices. Set up a free tier of Redis Cloud [here](https://redis.io/try-free/).

## New health report in Redis Software

The new Consolidated Health Report provides a clear, read-only snapshot of your Redis Enterprise cluster and database health directly in the Admin Console, eliminating the need for SSH or CLI access. With real-time visibility into alerts, node health, memory usage, and ongoing actions, teams can quickly understand system status and make more confident operational decisions. Find the latest release of Redis Software [here](https://redis.io/downloads/#Redis_Software).

## Redis Insight comes to Azure users

The release of Redis Insight 3.2.0 brings the ability to connect Azure Managed Redis with ease. Auto-discover databases across subscriptions with one-click import and connect using Entra ID and Azure passwordless (OAuth) authentication. Check it out [here](https://github.com/RedisInsight/RedisInsight/blob/main/docs/azure-setup.md).

## New Lab: Context Engineering for AI Applications

We’ve launched a new hands-on lab focused on one of the most important emerging disciplines in AI development: context engineering.

In this lab, you’ll build a course advisor agent that recommends courses by intelligently searching structured catalogs, reasoning through complex requirements, and maintaining conversational memory across sessions. You’ll start with baseline Retrieval-Augmented Generation (RAG) and progressively evolve the system into a more advanced, production-ready agent architecture.

Along the way, you’ll:

- Engineer system, retrieved, conversational, and user context
- Implement progressive RAG strategies and the ReAct framework
- Integrate Redis Agent Memory Server for working and long-term memory

Using Redis as both a retrieval engine and memory layer, this lab demonstrates how Redis serves as the context engine for modern AI applications. Get started [here](https://university.redis.io/course/vsgabnbkd3f5cd?tab=details)!

That’s a wrap on this months’ updates. Whether you prefer watching or reading, catch more valuable updates in my next two-minute episode. See you next time.
