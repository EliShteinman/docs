---
title: "What’s new in two – October edition"
linkTitle: "What’s new in two – October edition"
url: "/blog/whats-new-in-two-october-edition/"
description: "Click here to view video"
date: 2024-11-01
blogCategories:
- "Tech"
authors:
- "Talon Miller"
lastmod: 2025-07-03
hidden: true
---

*By Talon Miller, Principal Technical Marketer · Published 1 November 2024 · updated 3 July 2025*

![Blog tile image](/images/blog/c1e398bf2fb1b5c299410f1123d20c5d0ea4867d-772x552.webp)

[Click here to view video](https://www.youtube.com/embed/c5L1MQl6Ymo?si=K7DbN9Zp_fj-QBJl)

Welcome to “What’s new in two,” the place to catch up on Redis releases you might have missed in the past month. Before we get started this month, I wanted to take a moment to celebrate our 12th edition. We’ve been putting together this monthly update now for a year and are grateful to everyone who’s helped put this update together, and to you for following along.

We’re covering the latest developments from October, expanding on what I covered in our latest video—press play above if you prefer to watch a recap of this month’s updates. Let’s get started.

First, let’s start with some great updates coming to the latest version of Redis Insight.

New buttons for [Redis Data Integration (RDI)](https://redis.io/docs/latest/integrate/redis-data-integration/) are now available, including ‘Reset Pipeline’ and ‘Start / Stop Pipeline’. These buttons let you do a full sync reset, or stop and start your data pipeline again, without needing to switch over to the CLI.

The [latest Redis Insight update](https://redis.io/docs/latest/operate/redisinsight/install/) now lets you add multiple elements to list data types at once. Before this update, developers had to add elements one at a time using commands like RPUSH, LPUSH, or LINSERT, so this is a welcomed enhancement.

The last update for Redis Insight is a cool one and one that I know will save us a lot of time developing with Redis! [Redis Query Engine](https://redis.io/docs/latest/develop/interact/search-and-query/) is getting syntax auto-completion with index names, fields, etc. in the workbench for Redis Insight. So now, along with auto-complete for Redis commands, like FT.CREATE and its associated parameters, you can also access existing indexes and fields. This is going to be huge for writing new queries for full-text, semantic, and vector search.

Next, a new update for Redis Data Integration 1.4 brings support for helm charts for our Kubernetes customers, so if that’s you, make sure you [download the latest version ](https://redis.io/docs/latest/integrate/redis-data-integration/installation/)of RDI 1.4.

Redis Cloud users, we’ve got an update for you! The [cloud API](https://redis.io/docs/latest/operate/rc/api/) now supports a new “viewer” role. Before this, the cloud API ran as an owner role, which added some governance challenges. This new role will be a useful addition, and more roles are coming to the cloud API soon.

Finally—saving the best for last: Java and Python clients for client-side caching are now available. Jedis and redis-py client libraries are two of our most popular client libraries for our users so this is a monumental enhancement, especially as client-side caching is one of the most efficient ways to increase the performance of your apps and help reduce network traffic and costs. Get the latest [Jedis](https://github.com/redis/jedis/releases/tag/v5.2.0) or [redis-py](https://github.com/redis/redis-py/releases/tag/v5.1.1) libraries.

Last but not least, our final Redis Released stop was in NYC on October 17, where we continued to speak on the future of fast via our new releases: Redis 8, Redis Data Integration, Redis for AI, and more. And if you couldn’t make it in person, join us for [Redis Released Worldwide](https://redis.io/released/worldwide/), our virtual event from November 6 to 7.

That wraps up this month’s “What’s new in two.” We’ve covered the latest Redis features and improvements from October. Whether you prefer watching or reading, catch more valuable updates in my next two-minute episode. November releases are just around the corner, so stay tuned. And if you missed [last month’s update](https://youtu.be/L3ZQ1oboruw), two minutes is all you need to catch up.
