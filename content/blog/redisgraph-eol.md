---
title: "RedisGraph End-of-Life Announcement"
linkTitle: "RedisGraph End-of-Life Announcement"
url: "/blog/redisgraph-eol/"
description: "Redis is phasing out RedisGraph. This blog post explains the motivation behind this decision and the implications for existing customers and community members."
date: 2023-07-05
blogCategories:
- "Uncategorized"
authors:
- "Lior Kogan"
lastmod: 2026-06-01
hidden: true
mirrored: true
---

*By Lior Kogan, Contributor · Published 5 July 2023 · updated 1 June 2026*

![Blog tile image](/images/site-mirror/d12eaa7d5f1f8289f7ae4c9f33dc3e2ea4fdd2b8-772x550.webp)

**Redis is phasing out RedisGraph. This blog post explains the motivation behind this decision and the implications for existing customers and community members.**

We introduced RedisGraph, a Redis module that extends Redis into a general-purpose property graph database, about five years ago. Since then, RedisGraph has gained tremendous interest and adoption, and it has been used widely in the commercial, academic, education, and other source-available communities.

RedisGraph was part of our commercial offerings for Redis Enterprise Software and Redis Enterprise Cloud customers. It was also part of Redis Stack. In addition, RedisGraph is licensed to the community under the Redis Source Available License 2.0 (RSALv2) or the Server Side Public License v1 (SSPLv1).

However, today we are announcing the end-of-life of RedisGraph. This blog post explains why we decided to take this action and the wind-down process.

## Our motivations

There are multiple reasons why we decided to end-of-life RedisGraph.

Many analyst reports predicted that graph databases would grow exponentially. However, based on our experience, companies often need help to develop software based on graph databases. It requires a lot of new technical skills, such as graph data modeling, query composition, and query optimization. As with any technology, graph databases have their limitations and disadvantages.

This learning curve is steep. Proof-of-concepts can take much longer than predicted and the success rate can be low relative to other database models. For customers and their development teams, this often means frustration. For database vendors like Redis, this means that the total pre-sales (as well as post-sales) investment is very high relative to other database models.

On the other hand, **we see impressive growth in the adoption of key Redis Enterprise features** like[**Search and Query**](/search/)**, **[**JSON**](/json/)**, and **[**Vector**](/solutions/vector-search/). We also see how much faster prospects complete proof-of-concepts, usually with a high success rate. Most customers build scalable solutions with minimal support.

This is how Redis is meant to be: simple and joyful. We have strong indications that [we are building things that developers love](https://survey.stackoverflow.co/2023/#section-admired-and-desired-databases). This is where we always aim to be.

We also need to respond to feedback where we miss the mark. We don’t always get it right. We are eager to continue to fulfill the brand promise of Redis by reducing complexity.

To be brutally honest, though our graph offering is unique and technically competitive in many aspects, the costs required to grow our technical, sales, and support capacity to address a larger segment of this market is significantly higher than we anticipated. Given the database market dynamics and the other opportunities in front of us, we decided to concentrate our efforts and put our attention on other segments.

## What does end-of-life mean?

For any company and any product, end-of-life is a process.

During the end-of-life process, there are two important steps:

- End of sale: the moment where we stop actively selling new licenses
- End of support: the moment the company no longer supports the product

End of sale for new customers is effective immediately. Existing RedisGraph customers can renew their subscriptions with an expiration date no later than January 31, 2025. Annual subscriptions can be renewed up till January 1, 2024.

End of support is scheduled for January 31, 2025.

After January 31, 2025, RedisGraph commands will be disabled on Redis Enterprise Cloud.

If you are an existing Redis Enterprise Cloud or Redis Enterprise Software customer, you can purchase RedisGraph with Redis Enterprise Software (on-premise or self-managed) annual subscriptions until January 31, 2024. After January 31, 2025, you can continue using RedisGraph on Redis Enterprise software indefinitely without needing to extend your RedisGraph subscription (though you still need to acquire a subscription for Redis Enterprise itself). No support will be provided for any Redis Enterprise database with RedisGraph after January 31, 2025.

### What happens to the source-available code of RedisGraph in GitHub?

The RedisGraph GitHub repository is now in “maintenance mode.” We will not develop any new features.

Until December 31, 2024, we will continue to monitor community-reported issues. We will consider releasing minor versions (patches) based on such reports. Any patches will be released on GitHub. Patch versions will remain aligned between GitHub and our commercial offerings.

On February 1, 2025, we will tag the RedisGraph GitHub repository as “deprecated.” No new patches will be released after that date.

### How does this impact Redis Stack?

Beginning with Redis Stack 7.2.x-y version onwards, we will no longer include graph capabilities (RedisGraph).

### Would RedisGraph support new versions of Redis? What about RESP3?

Our Redis Enterprise Software customers should *not* upgrade to a Redis Enterprise version greater than 6.4 unless otherwise requested. RESP3 support for RedisGraph is not planned.

### I have additional questions. Whom should I contact?

Community members can contact us via [Discord](https://discord.gg/redis) in the #redis-graph channel or via [Redis forums](https://forum.redis.com/c/modules/redisgraph).

## Last words

The RedisGraph team thanks both our customers and the community for its invaluable interest and feedback. It has been a challenging and fascinating journey, and we hope to serve our customers and community with many new and improved Redis capabilities in the upcoming years.
