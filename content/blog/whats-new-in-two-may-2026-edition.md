---
title: "What’s new in two: May 2026 edition"
linkTitle: "What’s new in two: May 2026 edition"
url: "/blog/whats-new-in-two-may-2026-edition/"
description: "Click here to view video"
date: 2026-05-29
blogCategories:
- "Tech"
authors:
- "Talon Miller"
lastmod: 2026-05-29
hidden: true
mirrored: true
---

*By Talon Miller, Principal Technical Marketer · Published 29 May 2026*

![What’s new in two: May 2026 edition](/images/site-mirror/15f9a02d10140df4da60515dcde5a11094c1602a-1200x628.webp)

[Click here to view video](https://youtu.be/nK--hUZC6N8?si=EypY7yI_T_bNjkBh)

Welcome back to “What’s new in two,” your quick hit of Redis releases you might’ve missed over the last month. If your backlog has been winning lately, no worries—we’ve got the recap. We’re covering the biggest updates from May and expanding on what I covered in the latest video. Prefer the faster version? Hit play and watch instead.

## Introducing Redis Iris

This month we launched Redis Iris, our new context engine built for AI agents. Because agents don’t have an intelligence problem, they have a [context problem](/blog/context-is-all-you-need/).

Redis Iris sits between your agents and your enterprise data, giving them fast, live, agent-ready context instead of stale prompts and brittle integrations. It combines Redis Context Retriever, Redis Agent Memory, Redis Data Integration, Redis LangCache, and Redis Search into a single system designed to help agents retrieve the right data, maintain memory across tasks, and act in real time.

Two new capabilities are included in the preview: Context Retriever, which makes external data sources navigable by agents, and Agent Memory, which preserves short- and long-term memory across workflows and sessions.

If you’re building AI agents that need to reason across operational systems, customer data, documents, and real-time events without falling apart halfway through the workflow, [Redis Iris](https://redis.io/iris/) is worth a look.

## Redis Open Source 8.8 now generally available

[Redis 8.8](https://redis.io/docs/latest/develop/whats-new/8-8/) brings major performance improvements across core workloads, new native data structures, more resilient stream processing for AI agents, and lower infrastructure costs for vector-heavy apps.

Performance gains including up to 83% higher throughput for Streams workloads and up to 74% improvements for Sorted Sets. Vector storage in JSON also gets dramatically more memory efficient, with new floating-point precision controls enabling up to 92% memory savings for AI workloads.

We’re also introducing Array, a new native data structure written by Salvatore Sanfilippo, designed for indexed data patterns like rolling windows, random access, and range aggregations with better performance and memory efficiency.

On the operational side, Redis 8.8 adds built-in window-counter rate limiting with the new INCREX command, reducing the need for Lua-based implementations and custom workarounds. Stream processing also gets more resilient with the new XNACK command for explicit failure handling in consumer groups, making recovery behavior more predictable for agent workflows and event-driven systems.

Hash subkey notifications and multi-aggregation time series commands round out the release, giving teams more granular event visibility and faster analytics queries with fewer network round-trips.

Redis 8.8 capabilities are expected to land in Redis Cloud and Redis Software late summer so follow this series to keep up to date on when that lands.

## RDI 1.18 brings faster ingestion & Snowflake support

[Redis Data Integration 1.18](https://redis.io/docs/latest/integrate/redis-data-integration/release-notes/rdi-1-18-0/) shipped with two major additions: a new Flink-based processor and preview support for Snowflake as a source.

The [new Flink processor](https://redis.io/docs/latest/integrate/redis-data-integration/architecture/classic-vs-flink/) dramatically increases ingestion throughput for large data sets and trivial transformations, delivering up to 3.4x higher throughput in some scenarios. Streaming CDC throughput also jumps from 10k/s to 20k/s, giving teams more headroom for high-volume pipelines.

We also added preview support for Snowflake sources in Helm-based deployments, including multi-schema capture in a single pipeline. That opens the door for more reverse ETL workflows, where data and features generated in the warehouse can move directly into Redis to power real-time apps, personalization, fraud detection, and operational workflows.

RDI 1.18 also includes new API v2 capabilities for DLQ inspection, target flush operations, and CDC-readiness validation, plus reliability and security updates across the platform.

## Redis Software adds certificate-based authentication with LDAP authorization

Redis Software now supports certificate-based authentication with centralized LDAP/AD authorization, giving organizations a passwordless way to manage access through their existing identity systems.

That means no local Redis user management for human access, faster onboarding and deprovisioning, and permissions that stay aligned with LDAP or Active Directory automatically at login. In other words, fewer manual sync processes and fewer chances for someone to keep access longer than they should.

The update also helps security teams tighten governance with centralized access policies, stronger auditability, and support for modern certificate-based workflows. Organizations using platforms like Teleport can also support short-lived certificates to reduce long-term credential exposure. Want to learn more? [Check the docs](https://redis.io/docs/latest/operate/rs/release-notes/rs-8-0-releases/rs-8-0-20-19/).

## PrivateLink is now fully GA

[AWS PrivateLink](https://redis.io/docs/latest/operate/rc/security/aws-privatelink/) resource endpoints are now fully generally available across Redis Cloud Pro deployments, including both Redis Enterprise and OSS clustering support, plus Smart Client Handoffs for smoother maintenance and upgrades.

For most deployments, PrivateLink is now the recommended default connectivity model. It keeps Redis traffic off the public internet while providing scoped, directional access to specific Redis resources instead of exposing entire VPCs to each other. It also works with overlapping CIDR ranges, which saves a lot of networking pain once environments start getting complicated.

Most apps won’t see a noticeable performance difference, which makes PrivateLink the easier default choice for teams that care about security, compliance, and simpler network management.

## Dynamic endpoints arrive in Redis Cloud

We also introduced [dynamic endpoints](/blog/dynamic-endpoints-migrate-databases-without-changing-your-endpoint/) for Redis Cloud in public preview.

Most database migrations aren’t technically difficult. Coordinating endpoint changes across dozens of apps, services, jobs, and owners is the part everyone dreads.

Dynamic endpoints solve that by giving you a stable hostname that can redirect traffic between Redis databases. Instead of updating app configs every time you move from Essentials to Pro, migrate regions, switch clouds, or handle disaster recovery, you redirect the endpoint once and keep your apps connected to the same hostname throughout the move. Learn more on the [docs](https://redis.io/docs/latest/operate/rc/databases/redirect-endpoints/).

That’s a wrap on this months’ updates. Whether you prefer watching or reading, catch more valuable updates in my next two-minute episode. See you next time.
