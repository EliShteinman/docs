---
title: "Say Hi to Redis’ New-Old Friends"
linkTitle: "Say Hi to Redis’ New-Old Friends"
url: "/blog/say-hi-to-redis-new-old-friends/"
description: "One of the most amazing things a first-time Redis user might notice is a 42-page long list of clients, all developed by the great open source community of Redis. Currently, it consists of 218..."
date: 2021-11-04
blogCategories:
- "Redis Open Source"
- "Tech"
authors:
- "Guy Korland"
lastmod: 2026-09-01
hidden: true
---

*By Guy Korland · Published 4 November 2021 · updated 1 September 2026*

![Blog tile image](/images/site-mirror/f2757e486f26feabe53f3a5071977a5d05b8d102-772x520.webp)

## Idiomatic Python, Java, and Node clients
join the Redis organization

One of the most amazing things a first-time [Redis](https://redis.io) user might notice is a [42-page long list](https://redis.io/docs/latest/) of clients, all developed by the great open source community of Redis. Currently, it consists of **218** different clients!

![](/images/site-mirror/4f46aef3bf15195962a08d646e359a2cd31c00aa-1024x537.webp)

That list not only covers all the major programming languages, but also languages that I, at least, didn’t hear about until I set out to write this blog, like [Racket](https://redis.io/clients#racket), [Rebol](https://redis.io/clients#rebol), and [Lasso](https://redis.io/clients#lasso). To be technically correct, the list covers **36** different programming languages! (I guess you already got the point. Perhaps I can drop the “!” from now on…)

At a first glance, writing a Redis client sounds like a simple task. All you have to do is read the [Redis Protocol (RESP)](https://redis.io/topics/protocol), which is pretty simple and text based, then just follow the [Redis Commands](https://redis.io/docs/latest/commands/) documentation and implement these commands one by one. To be accurate, the list contains **264** different commands! (Sorry, I couldn’t help myself—had to add another “!”)

## But why am I telling you all of that?

Well, these 264 commands are just the tip of the iceberg. If you really want to harness the full power of Redis, covering only these commands won’t do Redis justice. On top of these “simple” commands Redis also supports what is expected from any NoSQL database these days: [High-Availability](https://redis.io/topics/replication), [Sharding](https://redis.io/topics/cluster-tutorial), [Transactions](https://redis.io/topics/transactions), [Access-Control list (ACL)](https://redis.io/topics/acl), [Notifications](https://redis.io/topics/notifications), and [Extensibility](https://redis.io/docs/latest/develop/reference/modules/).

In order to keep Redis simple and stable, chunks of processing are offloaded to the client. For example, in order to support [Redis Transactions](https://redis.io/topics/transactions), the client has to promise all the operations are done on the same exact socket and can’t multiplex this socket as long as the transaction wasn’t “[executed](https://redis.io/commands/exec).” Such nuances should be taken into consideration when one starts to develop a new Redis client, and it gets even trickier when it comes to supporting High-Availability and [Clustering](https://redis.io/topics/cluster-spec).

![](/images/site-mirror/4613cb169ebda4c7b5198a94cc2ca6f71daac5d9-1024x561.webp)

## We want to make it even better!

About two years ago, a few months before the move of Redis code to the[ Redis organization](https://github.com/Redis),we started to think: How can we make sure Redis users not only get the best Redis server, but also get the best development experience while being able to use all the latest and greatest Redis can offer?

We started to approach the different clients used by the vast Redis community, setting our target at helping client maintainers be up to speed with the vast Redis feature set. First, we formed a forum with many of the maintainers, providing them a platform to share their experience and dilemmas, but also to get the Redis core team their direct feedback.

Then, we mapped the gaps and missing features in the more adopted clients in the 10 leading programming languages. We realized that while some of the clients have millions of downloads a week, they’re still missing valuable features (like Redis Cluster or Pipeline) which many users can’t utilize, so we immediately started to contribute code to these clients.

Last, after interviewing many Redis users, we realized the amazing variety of clients users can pick from suggests bootstrapping a Redis client is amazingly simple, but maintaining an up-to-date client is full-time work, and users find it hard to decide which client to pick and which client they can rely on for long runs.

## New Redis organization members

In the last year, we started to suggest some of the more adopted clients to join the Redis organization, so we are happy to welcome three new members [Jedis](https://github.com/redis/jedis), [node-redis](https://github.com/redis/node-redis), and [redis-py](https://github.com/redis/redis-py). These three clients join the old timer members [Hiredis](https://github.com/redis/hiredis) and [redis-rb](https://github.com/redis/redis-rb). We hope that it will reduce confusion among users, increase their assurance about the clients road map, and help us make sure these clients provide the complete Redis experience.

The last couple of months were pretty hectic, and the three clients got a complete face lift. A long list of missing features were added to make sure the clients support all the goodies Redis has to offer, while also being refactored to provide a more “modern” experience (these clients are 10+ years old). The result of this hard work is a new 4th version for each one of them. You’re more than welcome to download the new client release candidates [Jedis@v4](https://mvnrepository.com/artifact/redis.clients/jedis), [node-redis @v4](https://www.npmjs.com/package/redis/v/next), and [redis-py@v4](https://pypi.org/project/redis/4.0.0b3/). Please share your feedback.

## What’s next?

The work has just started and the road map holds a couple of interesting features, so expect more to come in the near future. Some of them are adding native support for the most adopted Redis Modules like [RediSearch](https://redisearch.io) and [RedisJSON](https://redisjson.io), which should simplify the developer experience. Also, some complete other long-awaited features, such as [client side caching](https://redis.io/topics/client-side-caching) support, new Redis protocol ([RESP3](https://github.com/redis/redis-specifications/blob/master/protocol/RESP3.md)) added in Redis 6, new Stream APIs, and Redis Functions upcoming in Redis 7.
