---
title: "Refreshing and Extending Redis.io"
linkTitle: "Refreshing and Extending Redis.io"
url: "/blog/redis-io-refresh/"
description: "Today we’re pleased to announce the relaunch of Redis.io. Redis.io has always been the home of Redis and the entry point for new Redis users. With this launch, we’ve revised the core Redis..."
date: 2022-03-23
blogCategories:
- "Product Releases"
authors:
- "Kyle Banker"
- "Itamar Haber"
lastmod: 2025-07-03
hidden: true
mirrored: true
---

*By Kyle Banker, Itamar Haber · Published 23 March 2022 · updated 3 July 2025*

![Blog tile image](/images/site-mirror/bf06bd62eb0cdad539214994a4674468e34b0d73-772x550.webp)

Today we’re pleased to announce the relaunch of [Redis.io](https://redis.io). Redis.io has always been the home of Redis and the entry point for new Redis users. With this launch, we’ve revised the core Redis documentation while modernizing the site’s design and updating its infrastructure.

In this post, we’d like to explain our motivations for the site relaunch, share the principles we’ve adopted in revising [the Redis.io site](https://redis.io), and preview what’s next.

## Refreshing Redis.io

![](/images/site-mirror/55a4e632fc2cb655a51cc820c6ec09caa570db8f-914x361.webp)

*Screenshots of the new Redis.io documentation page, home page, and commands page*

Redis has come a long way in the thirteen years since [its first commit](https://github.com/redis/redis/commit/ed9b544e10b84cd43348ddfab7068b610a5df1f7). Now established as a foundational database technology, deployed widely across data centers and clouds the world over, and reliably processing untold billions of requests every second, the Redis open source project continues to advance.

All the while, redis.io has served as the home and core documentation site for Redis. But this site [has remained largely unchanged](https://web.archive.org/web/20130502072652/http://redis.io/commands) since its unveiling back in 2012. When we started asking ourselves how we could improve upon redis.io to reflect the importance of the Redis open source project and to better serve the Redis community, we discovered several glaring issues worth addressing.

The first of these issues concerned the Redis documentation itself. Modern software documentation should be well organized, navigable, and up to date. For this first major update, we’ve reorganized the Redis docs, added site navigation, removed a lot of legacy content, and completed a light, first-pass copyedit. In doing so, we’ve significantly improved the user experience of the Redis docs while also setting the stage for the many longer-term improvements we and the larger Redis community need to make.

Our next concern was with the site’s design. We wanted to create a fresh, navigable, and modern design for the site while maintaining certain elements from the original design. We hope that the final result speaks for itself.

Finally, we wanted to update the site’s infrastructure. The site had been running on a bespoke Ruby application, written eleven years ago, that was getting hard to maintain. Now, redis.io runs on Hugo, a well-known and widely deployed static site generator.

## Redis open source principles

As the sponsors of Redis, we strongly believe in the importance of open source for the health and continued growth of the Redis project. We’re committed to keeping Redis open source, as it’s been since day one. We are the driving force behind the [project’s governance](https://redis.io/topics/governance), contributing the majority of its code, and mentoring and educating hundreds of developers around the world on how to become Redis contributors. We have never asked anyone to sign a [Contributor License Agreement](https://en.wikipedia.org/wiki/Contributor_License_Agreement), and we don’t plan to do so in the future. The bottom line is that we take our stewardship of Redis seriously, and we’re explicitly committed to Redis remaining open source.

## Extending the developer experience

At the same time, redis.io has always been focused on helping developers build with Redis. We’re now taking this further by also introducing [Redis Stack](/blog/introducing-redis-stack) on redis.io. Licensed under the [Redis Source Available License (or RSAL)](/legal/licenses/), Redis Stack unites the capabilities of the leading Redis modules (RediSearch, RedisJSON, RedisGraph, RedisTimeSeries, and RedisBloom) under a single product. We believe that Redis Stack represents an important progression for any developer wanting to take the speed and stability of Redis into new domains and problem spaces.

And, while we are now hosting both OSS and RSAL-licensed projects on redis.io, we’re also taking great pains to ensure that the line between these projects is clear. For example, the documentation for open source Redis will always be maintained with [its current license](https://github.com/redis/redis-doc/blob/master/LICENSE) and [in its own repository](https://github.com/redis/redis-doc). We’re also explicitly calling out the portions of the site that apply to RSAL-licensed projects.

## Final thoughts and next steps

At the end of the day, we believe that we can effectively sponsor and promote open source Redis while also providing an onramp to the RSAL-licensed Redis Stack. This new redis.io represents a significant and long-needed improvement to the core Redis docs; to the look, feel, and usability of the site; and to the future development of redis.io for the benefit of Redis developers everywhere. We welcome your comments and contributions, and we look forward to continuing to improve the home of Redis.

---
