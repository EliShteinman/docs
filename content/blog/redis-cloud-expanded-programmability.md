---
title: "Expanding Programmability With Redis Cloud"
linkTitle: "Expanding Programmability With Redis Cloud"
url: "/blog/redis-cloud-expanded-programmability/"
description: "We updated Redis Cloud with Redis Open Source 7.0 compatible features, including Redis functions and Pub/Sub ACL changes, in a limited release."
date: 2023-03-29
blogCategories:
- "Tech"
authors:
- "Redis  "
lastmod: 2025-03-27
hidden: true
---

*By Redis   · Published 29 March 2023 · updated 27 March 2025*

![Blog tile image](/images/blog/3241aff147643c864e2728d8786ae4dd83521920-772x550.webp)

**We updated Redis Cloud with Redis Open Source 7.0 compatible features, including Redis functions and Pub/Sub ACL changes, in a limited release.**

Developers love Redis’ simplicity and ease of use, and we are eager to continue extending server-side processing functionality for their applications. Redis Open Source version 7.0 was made generally available nearly a year ago, and it was the first major release of Redis since 2019. One significant change to improve server-side programmability is Redis functions.

Today, we are announcing the availability of Redis functions within [Redis Cloud](/cloud/).

This first phase is a limited release. These updates are only available on [Amazon Web Services](/cloud-partners/aws/) (AWS) and [Google Cloud Platform](/cloud-partners/google/) (GCP) for Fixed and Free subscriptions. The regions supported, as of today, are GCP Tokyo and AWS Singapore.

## Adding support for Redis functions

The most significant new feature that was introduced is Redis functions, an API for managing code to be executed on the server. This feature, which became available in Redis OSS 7.0, superseded the use of EVAL in prior Redis versions.

As part of this limited release, we now support Redis functions in Redis Cloud.

Redis functions have several advantages over [scripting with Lua](https://redis.io/docs/manual/programmability/eval-intro/). As our developers know, Lua has limitations.

First, with Lua, all client application instances must maintain a copy of all scripts in order to guarantee consistency. That means that the developer needs to create some mechanism that applies script updates to all of the application’s instances.

Second, scripts are ephemeral, and a script can’t call another script. This makes it nearly impossible to share or reuse code between scripts, short of client-side preprocessing.

Functions solve these problems. They serve as a single source of truth of the executable logic and they operate as first-class citizens in Redis. Functions are also persisted to the append-only file (AOF) and replicated from primary (formerly known as ‘master’) to replicas, so they are as [durable](/redis-enterprise/technology/durable-redis/) as the data itself.

To learn more about Redis functions and how you can take advantage of them, consult the [documentation](https://redis.io/docs/manual/programmability/functions-intro/).

## Pub/Sub ACL changes

Another important change is the default ACL access to Pub/Sub channels.

ACLs for Pub/Sub channels were originally introduced as part of Redis OSS 6.2, with permissive access by default. That meant that if you didn’t *explicitly block* access in your Pub/Sub ACL, the Pub/Sub channel remained accessible.

Starting with Redis OSS 7.0, the default access is more restrictive in response to developer feedback. Unless you *explicitly allow* access in your Pub/Sub ACL, the Pub/Sub channel is not accessible.

To ease the upgrade process from version 6.x to 7.x, Redis Cloud continues to support the permissive approach by default. We provide additional support within the ACL Rule Builder UI to allow you to adapt to this change at your own pace.

![Rule builder interface for creating REdis ACL rules](/images/blog/21b9bf0a72712af3ac0db8b08d9019c708cc72b9-694x777.webp)

You are not required to take immediate action when upgrading your applications from Redis 6.x to Redis 7.x. However, if you use ACLs and Pub/Sub channels, we recommend that you make your Pub/Sub ACL rules explicit for increased security. For more, see the Redis Cloud [ACLs documentation](https://docs.redis.com/latest/rc/security/database-security/passwords-users-roles/#define-permissions).

We have additional information about the [Redis OSS 7.0 changes that are relevant to Redis Cloud](https://docs.redis.com/latest/rc/changelog/march-2023/#redis-70-breaking-changes), and you may want to consult the complete [Redis OSS 7.0 release notes](https://raw.githubusercontent.com/redis/redis/7.0/00-RELEASENOTES).

## How to get started

If you already have an account with Redis Cloud, create a new Fixed subscription.

![](/images/blog/b68a4a23f7c1e086b0a869bda4ef11c1438fd23f-1999x898.webp)

When you get to the vendor/region selection section, you’ll notice a new toggle for **Redis 7.0 preview**. Selecting it narrows the region list to regions that support Redis 7.0. (We will gradually add more regions to the list.)

![](/images/blog/b3a252e783000383f131ea984fefe5d2e29a738e-1660x664.webp)

All the databases you create with this subscription will be compatible with the features and capabilities of Redis OSS 7.0.

Don’t have an account yet? No worries! Create a [new free account](/try-free/), and you can choose Redis 7.0 there as well.

![](/images/blog/201c97c0734b3b46b6f9a95035804888aefcc63a-1035x628.webp)

## What’s next?

We will expand the rollout and availability of Redis 7.0 commands, functions, and capabilities to new regions.

We also plan to continue programmability improvements for Redis OSS, Redis Enterprise, and Redis Cloud. Specifically, we are exploring [triggered functions](/blog/database-trigger-features/) and you can catch up on the [latest innovations here](/blog/database-trigger-features/). We want to support the development of JavaScript-based functions that can be invoked, triggered, or scheduled based on events (keyspace notifications) driven by changes to underlying data. Expect triggered functions to be included as a preview within Redis Cloud later this year, as well as efforts to gather feedback from developers on the ease of use across development, debugging, and provisioning.

We are excited about what possibilities this unlocks for developers! Stay tuned.
