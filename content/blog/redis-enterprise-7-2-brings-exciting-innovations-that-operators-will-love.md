---
title: "Redis Enterprise 7.2 Brings Exciting Innovations That Operators Will Love"
linkTitle: "Redis Enterprise 7.2 Brings Exciting Innovations That Operators Will Love"
url: "/blog/redis-enterprise-7-2-brings-exciting-innovations-that-operators-will-love/"
description: "Among the highlights for operators are better access control, troubleshooting features, and maintenance capabilities."
date: 2023-08-17
blogCategories:
- "Uncategorized"
authors:
- "Esther Schindler"
lastmod: 2025-03-27
hidden: true
---

*By Esther Schindler · Published 17 August 2023 · updated 27 March 2025*

![Blog tile image](/images/blog/41e908c63f8217ca4d9f176ae726d4738b86135c-772x550.webp)

**Among the highlights for operators are better access control, troubleshooting features, and maintenance capabilities.**

The Redis 7.2 release has a lot of new features that matter to developers, and [we go into many of the details elsewhere](/blog/introducing-redis-7-2/). But the new version has many new capabilities that make life easier for operators and system administrators–from better access control to troubleshooting in multi-tenant environments–and we expect these features to make you smile.

To begin with, the new Redis Enterprise Cluster Manager makes your life easier.

## Troubleshooting in a multi-tenant environment

Imagine this scenario: You are on-call. You receive a phone call notifying you of a problem with an application or database. Your priority is to identify the source of the issue. That’s rarely fun.

When browsing to the Cluster Manager user interface (UI), the default page shows the database list. You see all your databases. Databases whose status is different from “active” are listed at the top, followed by databases with alerts, sorted by the number of alerts.

![](/images/blog/467250024834dda0868d168598b0f5ee744cc716-1000x286.webp)

To help you further investigate the problem, the new Redis Enterprise Cluster Manager has an expanded view for each row in the database view. That gives you quick access to crucial information in a user-friendly manner.

The main databases’ view when one of the databases is an expanded view looks like this:

![The Redis Enterprise Cluster Manager, expanded view](/images/blog/3fbfb1f366e1c6562b0fe11b31785a3a5383996e-1000x439.webp)

The expanded view provides key matrices, updated status and alerts, along with configuration. The expanded view lets you retain the context without disruptions. And you can compare metrics and data across multiple databases.

## Better ways to maintain clusters

The new Redis Enterprise Cluster Manager makes it easier to perform maintenance operations.

### License management

The new release prominently displays shards consumption (out of the total entitled by the license) on the main cluster configuration screen. This helps you stay on top of your license usage. When your license nears expiration, the new UI makes it easier to replace it.

![General Cluster information view](/images/blog/7e51c915d53ae5703164695ff8791e0c59b50380-1000x515.webp)

### Identifying the primary node

We added an indication for the primary node, so each node is displayed along with its role in the cluster. That makes it easier to plan maintenance or cluster upgrades.


![Cluster nodes view](/images/blog/dce347f6c43527ca224fadee8067f08b9f350590-1000x221.webp)

### Certificate management

New in version 7.2, the Redis Enterprise Cluster Manager helps you manage certificates by displaying essential information (such as expiration dates) and providing a convenient way to upload new certificates directly from the UI.

![Cluster certificates view ](/images/blog/f756c61770d5a78213b3d462fdd0d11be25a77ab-1000x607.webp)

## Integrated modules to add functionality

When you create a database in the new Redis Enterprise Cluster Manager UI, you now can easily access and highlight the option to add additional capabilities, also known as modules.

![Create a database with advanced capabilities](/images/blog/22be5d3d2d2cf0eb63fa7ee042d080a4573f1582-1000x554.webp)

Redis Enterprise 7.2 adds more functionality. To simplify maintenance, the Cluster Manager UI specifies the minimum Redis database version required for each module. The modules management screen provides visibility to the databases that use a given functionality so you can highlight any version dependencies.

![Manage databases with modules](/images/blog/20ba3d279741196fbf51a0b3599fe13f6e5599df-1000x408.webp)

Redis Enterprise 7.2 offers a host of exciting new features and improvements, including [auto tiering](/blog/introducing-auto-tiering/), support for [triggers and functions](/blog/introducing-triggers-and-functions/), expanded [JavaScript and client support](/blog/five-official-redis-clients/), and a lot of other enhancements. You can experience all the benefits by [downloading the 7.2 release ](/downloads/)and starting a free 30-day trial today.
