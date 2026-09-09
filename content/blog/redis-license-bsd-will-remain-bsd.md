---
title: "Redis’ License is BSD and will remain BSD"
linkTitle: "Redis’ License is BSD and will remain BSD"
url: "/blog/redis-license-bsd-will-remain-bsd/"
description: "Since the recent licensing change for our Redis modules, there’s been a lot of confusion and misinformation circulating about the implications of those changes. We want to address your questions..."
date: 2018-08-22
blogCategories:
- "Redis Modules"
authors:
- "Redis  "
lastmod: 2025-03-27
hidden: true
---

*By Redis   · Published 22 August 2018 · updated 27 March 2025*

![Blog tile image](/images/site-mirror/0073e867b4e64f59de9047fdcde04295ba647e5c-772x550.webp)

Since the recent licensing change for our Redis modules, there’s been a lot of confusion and misinformation circulating about the implications of those changes. We want to address your questions and be crystal clear: the license for open source Redis was never changed. It is BSD and will always remain BSD.

### So what has changed?

We recently did change the license for Redis modules developed by Redis from AGPL to Apache v2.0 *modified with* [Commons Clause](http://commonsclause.com). For those of you who are not familiar with Redis modules – these are add-ons on top of Redis core like [RediSearch](https://oss.redis.com/redisearch/), [RedisGraph](https://oss.redis.com/redisgraph/), [ReJSON](https://oss.redis.com/rejson/), [ReBloom](https://oss.redis.com/rebloom/) and [Redis-ML](https://oss.redis.com/redisml/).

### Why make that change?

Cloud providers have been taking advantage of the open source community for years by selling (for hundreds of millions of dollars) cloud services based on open source code they didn’t develop (e.g. Docker, Spark, Hadoop, Redis, Elasticsearch and others). This discourages the community from investing in developing open source code, because any potential benefit goes to cloud providers rather than the code developer or their sponsor.

### Why not AGPL?

There are two key reasons we decided to make the switch from AGPL:

1. AGPL does not prevent cloud providers (like AWS) from using AGPL-licensed code to build managed services.
1. We received requests from developers at large enterprises to move to a more permissive license, because the use of AGPL was against their company’s policy.

### Why Apache v2.0 modified with Commons Clause?

This new license allows full use of our Redis modules under the popular, liberal Apache v2.0 terms, but restricts the selling of the modules themselves. That means you can build internal, external and commercial products on top of our modules and sell those, but cannot directly sell the original modules. We believe this licensing supports the open and free use of modules, while still maintaining our rights over commercializing our assets.

### Why not a new license like Elastic or MariaDB?

Commons Clause was created by a coalition of several open source infrastructure companies, some of which use different open source licenses. In order to maintain a standard framework, we decided to piggyback the restriction (on cloud providers creating managed services) on an existing open source license.

### Questions?

We know some members in the community have had questions about this change, and we are happy to clarify any of the license details further to put your minds at ease. Please feel free to tweet me [@yiftachsh](https://twitter.com/Yiftachsh).
