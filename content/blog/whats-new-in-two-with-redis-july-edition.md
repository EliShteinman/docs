---
title: "What’s new in two with Redis – July edition"
linkTitle: "What’s new in two with Redis – July edition"
url: "/blog/whats-new-in-two-with-redis-july-edition/"
description: "Click here to view video"
date: 2024-07-31
blogCategories:
- "Tech"
authors:
- "Talon Miller"
lastmod: 2025-06-11
hidden: true
---

*By Talon Miller, Principal Technical Marketer · Published 31 July 2024 · updated 11 June 2025*

![Blog tile image](/images/blog/94691f9972e12fa104e04ef204cd183fa8174109-772x552.webp)

[Click here to view video](https://www.youtube.com/embed/_k31XzZKYJo?si=sMW5sY-eMOXdIcqY)

Welcome to “What’s new in two,” the place to catch up on Redis releases you might have missed from last month. This time, we’re covering the latest developments from July, expanding on what I covered in our latest video. Press play above if you prefer watching a recap of this month’s updates. Let’s get started.

## Release of 7.4 for Community Edition

The big news in July was the release of Redis 7.4 for [Redis Community Edition](https://redis.io/docs/latest/get-started/) and [Redis Stack](https://redis.io/about/about-stack/) as a release candidate.. This release comes with bug squashes and highly anticipated features including hash field expiration, new vector data types for reduced memory usage, and time series insertion filters. Redis 7.4 Community Edition is also the first dual-licensed under RSALv2 and SSPLv1, providing devs more flexibility. 

### Hash field expiration

The ability to set expiration times for individual hash fields is here. This enhancement caters to the long-standing request from the community for better control over hashes, which are widely used for representing data objects and storing session data. Before this enhancement, Redis only supported key expiration. Now, with hash field expiration, users can set a time-to-live (TTL) for individual fields within a hash. This feature increases precision in apps like [fraud detection](https://redis.io/solutions/fraud-detection/), where event counters can be strategically set to expire.

### Memory optimization

The new data types for vectors include bfloat16 and float16, which allow for significant reductions in memory consumption without sacrificing accuracy. These new data types are especially beneficial for apps that rely on large-scale vector databases, such as semantic caches and real-time data retrieval systems. Benchmarks show that using bfloat16 and float16 yields higher query per second (QPS) rates, lower latency, and faster indexing times compared to float32 and float64. This makes Redis more efficient for memory-intensive operations.

### Enhanced dev experience

Redis 7.4 also enhances the dev experience with improved secondary indexing and simplified querying of special characters in TAG fields. The new release makes it easier to [index and query empty and missing fields](https://redis.io/docs/latest/develop/interact/search-and-query/indexing/#index-missing-or-empty-values), supporting more dynamic data models. Geospatial search capabilities have been expanded with new operators, [INTERSECT and DISJOINT](https://redis.io/docs/latest/develop/interact/search-and-query/query/geo-spatial/). And time series size has been improved by introducing insertion filters that ignore negligible changes. These enhancements aim to streamline Redis and provide devs with a more robust and efficient tool. If you want to learn more about these updates and get even deeper into the 7.4 release, check out our [Redis 7.4 announcement blog](/blog/announcing-redis-community-edition-and-redis-stack-74/).

## Enhanced tagging for Redis Cloud

Two really helpful enhancements are coming to Redis Cloud for tagging. First, [database tagging](https://redis.io/docs/latest/operate/rc/databases/tag-database/) in cost reports are now downloadable through the Redis Cloud console. This allows users to see their database costs for specific tag keys or values. The cost report is available in the “Usage Report” and “Billing and Payment” tabs. Second, with tagging capabilities via the Cloud API, customers can manage their database tags using dedicated APIs. This includes adding, updating, getting, and deleting tags. 

## Introducing a 14-day trial of Redis Cloud on Google Cloud

We’re very excited to announce a new 14-day trial for Google Cloud customers who want to try out Redis Cloud. This new trial also includes $500 of usage. It’s never been easier than today to try out [Redis Cloud on the Google Cloud marketplace](https://console.cloud.google.com/marketplace/product/redis-marketplace-isaas/redis-enterprise-cloud-flexible-plan?project=redis-marketplace-isaas).


That’s it for this month’s “What’s new in two.” We’ve taken a closer look at the latest Redis features and enhancements from July. Whether you prefer watching or reading, keep an eye out for more valuable updates in my next two-minute episode. August releases are just around the corner, so stay tuned. And if you missed [last month’s update](https://www.youtube.com/watch?v=iJHMFYDlkc8), two minutes is all you need to catch up.
