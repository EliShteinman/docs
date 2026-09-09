---
title: "Redis 7.0 Is Out!"
linkTitle: "Redis 7.0 Is Out!"
url: "/blog/redis-7-generally-available/"
description: "Today we’re happy to tell the world about the general availability of Redis version 7.0, as announced at the Redis Days SF keynote earlier this year. The release has been under development for..."
date: 2022-04-27
blogCategories:
- "Announcements"
- "Company"
- "New Product Announcements"
- "Product Releases"
- "Tech"
authors:
- "Itamar Haber"
lastmod: 2026-05-26
hidden: true
---

*By Itamar Haber, Technology Evangelist · Published 27 April 2022 · updated 26 May 2026*

![Blog tile image](/images/blog/9e755fcc13280b99668203867278dc015a4389b7-772x550.webp)

Today we’re happy to tell the world about the general availability of [Redis](/try-free/) version 7.0, as announced at the [Redis Days SF keynote](/blog/redisdays-san-francisco-2022-overview/) earlier this year. The release has been under development for almost a year, and three release candidates preceded it, so we feel it is stable enough for use in production.

Upgrading from earlier versions is a relatively straightforward process, as backward compatibility has always been a design principle of the Redis project. However, before upgrading to Redis 7.0, please take a few minutes and get acquainted with the new version by reading the [release notes](https://github.com/redis/redis/blob/7.0/00-RELEASENOTES).

## Redis 7.0 Improvements and New Commands

In a nutshell,[ Redis 7.0](/blog/redis-7-first-release-candidate/) includes incremental improvements to almost every one of its aspects. Most notable are Redis Functions, ACLv2, command introspection, and Sharded Pub/Sub, which represent a significant evolution of existing features based on users’ feedback and lessons learned in production.

Version 7.0 adds almost 50 new commands and options to support this evolution and extend Redis’ existing capabilities. For example, the bitmap, list, set, sorted set, and stream data types have all been added with functionality that supports their use cases for data management. In addition, cache semantics have been extended to support existential and comparative modifiers.

While user-facing features are easy to boast of, the real “unsung heroes” in this version are efforts to make Redis more performant, stable, and lean. A large share of our developers’ brain cycles was invested in making the operation of Redis more effective by focusing on its performance vis-à-vis the resources that it uses. Redis 7.0 brings a number of improvements to almost every subsystem it manages, including memory, computing, network, and storage. Whereas some optimizations are enabled by default, others may require configuration. Please refer to the inline documentation in the [redis.conf](https://github.com/redis/redis/blob/7.0/redis.conf) file for details.

While the release of this new version is something for us to celebrate here at Redis, we are already busy working on making [Redis 7.2](https://github.com/redis/redis/projects/7) a reality. If you encounter any issues or have thoughts to share, we’d love to hear from you at the [Redis repository](https://github.com/redis/redis).
