---
title: "RedisInsight Introduces Diagnostic Features and Support for Search Capabilities"
linkTitle: "RedisInsight Introduces Diagnostic Features and Support for Search Capabilities"
url: "/blog/redisinsight-new-diagnostic-and-support-features/"
description: "RedisInsight is an ideal tool for developers who build with any Redis deployments – including Redis Open Source, Redis Stack,Redis Enterprise Software, Redis Enterprise Cloud, and Amazon..."
date: 2023-01-25
blogCategories:
- "Tech"
authors:
- "Olga Lopaci"
lastmod: 2025-03-27
hidden: true
mirrored: true
---

*By Olga Lopaci · Published 25 January 2023 · updated 27 March 2025*

![Blog tile image](/images/site-mirror/c4f9dc68fe4479878f79a736685024b85b549388-772x550.webp)

[**RedisInsight**](/insight/)** is an ideal tool for developers who build with any Redis deployments – including **[**Redis Open Source**](https://redis.io/docs/about/)**, **[**Redis Stack,**](/blog/introducing-redis-stack/)[**Redis Enterprise Software**](/enterprise/)**, **[**Redis Enterprise Cloud**](/redis-enterprise-cloud/overview/)**, and **[**Amazon ElastiCache**](/redis-enterprise-cloud/compare-us-with-aws-elasticache/)** – and who want to optimize their development process. RedisInsight lets you visually browse and interact with data, take advantage of the advanced command line interface and diagnostic tools, and so much more. Best of all, RedisInsight is free for everyone.**

The latest version of RedisInsight has new UI controls to perform [full-text search](https://redis.io/docs/stack/search/) across your data, a new database analysis tool, data formatters, visual support for Redis streams, bulk deletion, and Slow Log tool. We’re excited about all of these, and we think they can help you a lot.

## Improved database analysis

Use the database analysis tool, its dashboards, and its recommendations to optimize the performance and memory usage of Redis databases. Among its features:

- It checks data type distribution and memory allocation, and the tool reviews the summary of key expiration time and memory to be freed over time.
- You can inspect keys and namespaces, sorted by consumed memory or key length and count of keys, respectively.
- You can capture and track database changes using historical analysis reports.

![redisinsight database interface](/images/site-mirror/8c98506cf1a52fed8b1031cc5ac631de399f7b33-624x380.webp)

*RedisInsight database analysis report*

## Support for Redis and Redis Stack search

If you’ve been using Redis for [indexing](https://redis.io/docs/manual/patterns/indexes/), try the [latest Redis Stack](/blog/introducing-redis-stack-6-2-6-and-7-0-6/), which includes – among other strengths – impressive [query and search capabilities](https://redis.io/docs/stack/search/).

We added more functionality in this release. RedisInsight now complements Redis Stack with UI controls to quickly and conveniently run [search](https://redis.io/docs/stack/search/) queries against a pre-selected index. You can also create a secondary index of your data in a dedicated pane.

![running search queries](/images/site-mirror/e560218bb6e4762bef4306e840b28d923ec3eeb8-1999x1208.webp)

*Run search queries and see results in the browser*

## Data formatters highlight your data

You can view, validate, and manage key values in a format suitable for humans, not just for computers. The Browser tool has new formatters to prettify and highlight data in different formats, including Unicode, JSON, MessagePack, HEX, and ASCII.

![json code](/images/site-mirror/0b1b6f405477cddbb0b8e9c32bc5ec7a51d4627b-1392x940.webp)

*Prettify your data using one of many supported formatters in the RedisInsight Browser*

## Redis Streams support

Take advantage of the visual support for [Redis streams](https://redis.io/docs/manual/data-types/streams/) to create and manage streams. You can add, remove, and filter entries per timestamp. You can see and work with new entries and enable and customize refresh rates.

That’s just the start; we expanded the number of ways to view and control the way you work with Redis Streams. You can view and manage [consumer groups](https://redis.io/docs/manual/data-types/streams/#consumer-groups). You can see existing consumers in a given consumer name as well as the last messages delivered to them. Plus, you can inspect pending messages, explicitly acknowledge processed items, or claim unprocessed messages.

![redis streams data](/images/site-mirror/82c113085664d56a5f6086158dd7d226dcbb029d-624x562.webp)

*Work with Redis Streams and Consumer Groups in the RedisInsight Browser*

## Perform bulk deletions

The new RedisInsight makes it fast and easy to clean up databases. You can delete multiple keys of the same type or with the same key name pattern in bulk.

![redisinsight browser](/images/site-mirror/2b2e55593ca85c4a572a65d81636bc58d23dd65c-1999x1215.webp)

*Set filters in the RedisInsight Browser and delete all relevant keys in bulk*

## Slow Log tool

One frustration in troubleshooting performance issues is determining which tasks are bogging down the system. The Slow Log tool displays the list of logs captured by the SLOWLOG command to analyze all commands that exceed a specified runtime. You can specify both the runtime and the maximum length of Slowlog to configure the list of commands logged. You also can set the auto-refresh interval to automatically update the list of commands displayed.

![redisinsight slow log](/images/site-mirror/04c3ff94351555fc012b37e59926356b0a631cae-624x380.webp)

*Use Slow Log to find out what is slowing things down*

## That’s just the beginning

Want to learn more? To get the latest version of RedisInsight:

- Follow these [instructions](https://redis.io/docs/stack/get-started/install/) to install [Redis Stack](https://redis.io/download/) with RedisInsight using Homebrew or Docker
- Download it from the [RedisInsight download page](/insight/#insight-form) for Windows, Mac, and Linux
- Download it from [Download Center](https://app.redislabs.com/#/rlec-downloads) if you are an existing Redis Enterprise customer
- Install it via [FlatHub](https://flathub.org/apps/details/com.redis.RedisInsight/) or [Snapcraft](https://snapcraft.io/redisinsight) for Linux

Learn more about the ways RedisInsight can help you from the latest [RedisInsight release notes](https://github.com/RedisInsight/RedisInsight/releases). We’d love to hear [your feedback](https://github.com/RedisInsight/RedisInsight/issues).
