---
title: "What’s new in two: April 2026 edition"
linkTitle: "What’s new in two: April 2026 edition"
url: "/blog/whats-new-in-two-april-2026-edition/"
description: "Click here to view video"
date: 2026-05-08
blogCategories:
- "Tech"
authors:
- "Talon Miller"
lastmod: 2026-05-09
hidden: true
---

*By Talon Miller, Principal Technical Marketer · Published 8 May 2026 · updated 9 May 2026*

![What’s new in two: April 2026 edition](/images/blog/c5cde963f98d658d1ec1dd56852aeaf66a9aefb1-1280x720.webp)

[Click here to view video](https://youtu.be/nepLRiTB-QA?si=yZ2MZrrtwbbg7GfH)

Welcome to “What’s new in two,” your quick hit of Redis releases you might have missed in the past month. If you blinked, you missed it—so here’s the recap. We’re covering the latest developments from April and expanding on what I covered in our latest video. Press play to watch it instead.

## Introducing Redis Feature Form

In mid April we released Redis Feature Form, a new enterprise-grade feature store for production ML, now generally available. It gives ML teams a managed system to define features, orchestrate pipelines, track lineage, and serve features with sub-millisecond latency, all while keeping training and inference in sync. If you’re running real workloads in fraud, risk, or recommendations, this is aimed at simplifying the hardest part of production ML, which is getting features into production reliably. Read more from TechTarget [here](https://www.techtarget.com/searchdatamanagement/news/366641958/Redis-unveils-Feature-Form-to-improve-AI-ML-workloads).

## Redis Cloud updates

Two security updates in Redis Cloud are now generally available, giving you tighter control over how your data is accessed in production environments. [PrivateLink resource endpoints](https://redis.io/docs/latest/operate/rc/security/aws-privatelink/) enable fully private connectivity at scale, keeping traffic off the public internet while supporting Redis Software clustered deployments. Support for PrivateLink for OSS clustering API will follow soon. Review the product limitations in our [docs](https://redis.io/docs/latest/operate/rc/security/aws-privatelink/).

In addition, the [block public endpoints](https://redis.io/docs/latest/operate/rc/security/database-security/block-public-endpoints/) capability, which reduces the risk of unintended exposure and simplifies network security posture, now supports disabling authentication. This lets customers conveniently and securely migrate Redis databases without authentication to Redis Cloud without the need to change their code and support authentication.

If you’re locking down access while still supporting distributed apps, these updates are worth digging into.

## OpenTelemetry observability for Redis clients

We’ve added OpenTelemetry-based observability across Redis clients to make it easier to understand what your apps are doing in production. With built-in tracing, you can track requests, debug latency issues, and get a clearer view into performance without stitching together custom instrumentation.

Python and Java clients are already supported, with node-redis coming next to complete the set. This gives you consistent visibility across the most widely used Redis client environments. Get started with the [docs](https://redis.io/docs/latest/develop/clients/observability/).

That’s a wrap on this month’s updates. Whether you prefer watching or reading, catch more valuable updates in my next two-minute episode. See you next time.
