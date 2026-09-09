---
title: "What’s new in two: May 2025"
linkTitle: "What’s new in two: May 2025"
url: "/blog/whats-new-in-two-may-2025/"
description: "Click here to view video"
date: 2025-05-30
blogCategories:
- "Tech"
authors:
- "Talon Miller"
lastmod: 2025-06-10
hidden: true
---

*By Talon Miller, Principal Technical Marketer · Published 30 May 2025 · updated 10 June 2025*

![Redis](/images/site-mirror/b6a07218f79ae330bdcb6b5316512dc927d2c929-500x358.webp)

[Click here to view video](https://www.youtube.com/watch?v=t1XWnbPNCUY)

Welcome to “What’s new in two,” your quick hit of Redis releases you might have missed in the past month. We’re covering the latest developments from May and expanding on what I covered in our latest video. Press play above if you’d rather watch than read. Let’s get started.

## General availability of Redis 8

I’m thrilled to announce the general availability of Redis 8, the fastest Redis yet. It has over 30 performance improvements, including 87% faster commands, 2x more operations per second throughput, 18% faster replication, and 16x more query processing power with Redis Query Engine.

Plus, we’ve changed the name of our free product from Redis Community Edition to Redis Open Source to reflect the addition of AGPLv3 as a licensing option. That’s right, it’s the copyleft license that brings the flexibility devs love.

Download the fastest Redis ever. You can get started here with the [Docker image](https://hub.docker.com/_/redis), [install using snap](https://github.com/redis/redis-snap), [install using brew](https://github.com/redis/homebrew-redis), [install using RPM](https://github.com/redis/redis-rpm), or [install using Debian APT](https://github.com/redis/redis-debian). Or if you’re just looking to upgrade to Redis 8 from version 7.x, then here are the [docs to upgrade](https://redis.io/docs/latest/operate/oss_and_stack/install/upgrade/).

## General availability of Azure Managed Redis

In case you missed it, we announced the public preview of Azure Managed Redis (AMR) back in November last year, and now another huge milestone happened in May—the general availability of this fully-managed, first-party Redis offering co-engineered in partnership with Microsoft Azure.

The GA release of AMR comes with 7.4, and users will soon have access to Redis 8. This makes AMR the most advanced Redis offering on Azure to date, supporting both traditional caching and caching for AI apps and workloads.

Existing Azure Cache for Redis customers can easily migrate to AMR, and if you aren’t a Microsoft Azure customer and want to see how it could work for your solution, [reach out](https://redis.io/meeting-4/?utm_campaign=&utm_source=&utm_medium=&utm_term=&utm_content=&gclid=) to our team. 

## Release of Redis Software 7.22

Another major milestone release in May was for our on-prem offering, 7.22 for Redis Software. This release delivers boosts in performance, making it the most performant version to date. For example, it improved performance by up to x3.4 on plain text benchmarks and x4.6 on TLS-enabled benchmarks, both compared to 7.2.4.

This release also includes multiple feature improvements like faster issue resolution and proactive support with new built-in diagnostics and structured logs, higher availability for mission-critical workloads with two-dimensional rack-zone awareness, and enterprise-grade control and scalability with enhanced tracking of management operations. Want to learn more? Check out the [release notes](https://redis.io/docs/latest/operate/rs/release-notes/rs-7-22-releases/rs-7-22-0-95/).

## Database version selection for Pro subscriptions

Next, a quality of life improvement is rolling out to our customers using Redis Cloud with a Pro subscription. You can now select Redis versions per database and perform [self-serve database upgrades](https://redis.io/docs/latest/operate/rc/databases/upgrade-version/) instantly, without needing to open a request. You can do this through the UI or [API](https://redis.io/docs/latest/operate/rc/api/), so this gives our customers complete control over upgrading.

## Private Service Connect for Pro subscriptions on GCP

Another update for our customers using [Private Service Connect](https://redis.io/docs/latest/operate/rc/security/private-service-connect/) (PSC) to connect to their databases with a Pro subscription on GCP. We’ve reduced the number of PSC endpoints required on the consumer side from 40 to one. This will help our customers enjoy the benefits of this private connectivity method without needing to allocate a larger number of IPs in their application subnets. 

## Redis Data Integration (RDI) lab

Lastly, I wanted to share a cool opportunity for those who want to get their hands on RDI. We talk about RDI a lot on this monthly series, and for good reason—it’s an amazing tool for syncing external databases to your Redis databases in real-time. We just released a new lab that will make you an expert in RDI in an hour or so. Check it out [here](https://university.redis.io/course/2qa1u1ss21vsy5?tab=details) to get started.
