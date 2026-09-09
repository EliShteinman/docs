---
title: "Redis Software 8.0.6: our fastest, most secure release yet"
linkTitle: "Redis Software 8.0.6: our fastest, most secure release yet"
url: "/blog/redis-software-806/"
description: "Redis Software 8.0.6 continues our commitment to making Redis the fastest, most reliable, and most secure data platform for enterprises. This release introduces a range of enhancements that improve..."
date: 2026-01-15
blogCategories:
- "Tech"
authors:
- "Yoav Peled"
- "Alon Magrafta"
- "Maayan Agranat"
lastmod: 2026-01-16
hidden: true
---

*By Yoav Peled, Alon Magrafta, Maayan Agranat · Published 15 January 2026 · updated 16 January 2026*

![Redis](/images/blog/557d090ba02ba737c1385c3eb50d0feb44e6ed09-1200x628.webp)

Redis Software 8.0.6 continues our commitment to making Redis the fastest, most reliable, and most secure data platform for enterprises. This release introduces a range of enhancements that improve performance, security, and observability for both Redis operators and developers.

Let’s take a look at what’s new in Redis Software 8.0.6.

### Redis 8.2 under the hood

Redis Software 8.0.6 brings Redis Software all the innovation and enhancements introduced to the Redis Open Source community in Redis 8.2.. Customers now benefit from improved performance, efficiency, and developer experience across core Redis operations. For a detailed overview, check out the [Redis 8.2 GA announcement](/blog/redis-82-ga/).

### Exceptional performance improvements

Redis Software 8.0.6 delivers measurable latency reductions across multiple Redis commands—pushing efficiency and responsiveness even further. In benchmark testing, median (p50) latency improvements reached up to **72%** when comparing Redis Software 8.0.6 (based on Redis Open Source version 8.2) against Redis Enterprise Software 7.8.6 (based on Redis Open Source version 7.4). These gains are driven by a powerful combination of Redis Open Source 8.2 performance optimizations and targeted enhancements in the Redis Enterprise proxy, which together deliver faster data processing and reduced command latency.

![Redis](/images/blog/27feaafdc0568f1b0a727b316beb4b8b70594975-512x271.webp)

This translates directly into customer value: you can now handle higher traffic, more users, and more demanding workloads on the same infrastructure. Higher efficiency means scaling thresholds are pushed further out, which saves money by reducing the need for infrastructure expansion. The most significant gains - seen in commands like BITCOUNT, SUNION, ZADD and HSCAN directly benefit use cases such as real-time analytics, recommendation engines, fraud detection, leaderboards, and large-scale metadata or session scans. This is another example of how Redis keeps improving. It keeps pushing the limits of performance so customers can move faster, scale smarter, and set new expectations for what real-time data platforms can do.

### Enterprise-grade Single Sign-On (SSO) for the Redis UI

Starting with Redis Software 8.0.6, customers can integrate their organization’s Identity Provider (IdP) to enable Single Sign-On (SSO) using the industry-standard SAML 2.0 protocol for the Redis UI. This allows users to log in to the Redis Software console using their existing corporate credentials, rather than managing separate local usernames and passwords. This simplifies access while improving security.

By centralizing authentication through trusted enterprise identity providers, organizations can apply company-wide security policies such as multi-factor authentication (MFA), password complexity enforcement, and session controls directly through their IdP. This approach enhances overall security posture, improves compliance and audit readiness, and ensures alignment with corporate identity governance frameworks.

### Trusted certificates for internode encryption

Up until now, internode encryption in Redis Software used self-signed certificates by default. This approach worked for many deployments, but did not meet stricter enterprise security and compliance requirements.

Redis Software 8.0.6 changes that by introducing full support for replacing self-signed internode encryption certificates with customer-provided trusted certificates. This enhancement ensures stronger alignment with organizational governance requirements and elevates overall cluster security.

### Advancing observability with new monitoring engine (V2)

Running a real-time, high-performance in-memory database like Redis requires observability that operates at the same speed and precision.

Redis introduced a new monitoring engine in Redis Software 7.8.2, and with this release it is now generally available. This new engine brings a streaming architecture that delivers more accurate and granular metrics, enabling smarter alerting, faster troubleshooting, and deeper visibility. It also lays the groundwork for unified observability experiences in Redis Cloud.

To ensure a smooth and straightforward transition, Redis offers updated best practices, a hands-on [tutorial](https://redis.io/learn/operate/observability/redis-software-prometheus-and-grafana), and prebuilt operational dashboards and alerts to help customers adopt V2 efficiently and with confidence.

### A revamped Redis Flex engine

Redis has long been the foundation for real-time apps, delivering sub-millisecond performance when speed matters most. But today’s systems operate at a very different scale.** **Datasets now span terabytes and support workloads like personalization, fraud detection, and machine learning feature stores. These use cases demand Redis-level speed without being constrained by memory limits. Redis Flex in Redis 8 addresses this shift by seamlessly combining RAM and Flash into a single data layer. Hot data remains in memory for low-latency access, while less active data is transparently stored on Flash and promoted automatically, all while preserving the Redis API and developer experience.

Redis 8.2 represents a significant step forward for Redis Flex. Earlier releases could offload values to Flash, but keys still consumed memory, limiting efficiency as databases grew. With Redis 8.2, both keys and values can be managed across RAM and Flash, freeing memory for truly hot data and smoothing performance as utilization increases. In real-world terms, this translates into higher cache hit rates, more predictable tail latency, and up to 2× higher effective throughput at the same RAM allocation, while keeping p99 latency in the single-digit milliseconds range for large, real-time workloads.

For customers upgrading from Redis 7, **Redis Flex is a practical and immediate reason to move to Redis 8**. It enables larger datasets, steadier performance at scale, and supports new real-time use cases—all without changing applications or operational models. Redis 8.2 doesn’t just extend Redis to bigger data; it makes Redis a stronger, more versatile foundation for the next generation of real-time systems.

### Experience Redis Software 8.0.6 Today

Redis Software 8.0.6 introduces a wealth of improvements—from significant performance boosts and enhanced security options to deeper observability.

You can experience all the benefits by [downloading the 8.0.6 release](https://redis.io/downloads/#Redis_Software) and [starting a free 30-day trial](https://redis.io/try-free/) today.
