---
title: "Multiplexing Explained"
linkTitle: "Multiplexing Explained"
url: "/blog/multiplexing-explained/"
description: "A critical, but important piece of your Redis-powered application is the client library. Client libraries are the glue between the software you are writing and Redis. They perform a few primary..."
date: 2020-02-12
blogCategories:
- "Tech"
authors:
- "Redis  "
lastmod: 2026-06-01
hidden: true
---

*By Redis   · Published 12 February 2020 · updated 1 June 2026*

![Blog tile image](/images/site-mirror/0073e867b4e64f59de9047fdcde04295ba647e5c-772x550.webp)

A critical, but important piece of your Redis-powered application is the client library. Client libraries are the glue between the software you are writing and Redis. They perform a few primary major duties:

1. **Parsing and encoding RESP (Redis Serialization Protocol)**
1. **Making Redis commands idiomatic to your language**
1. **Managing the connection(s) to Redis**

The first point is standardized—there is a specification for RESP and all clients must conform or, well, nothing works. The second point is unique to each library—this is what makes Redis feel natural to your programming language; even client libraries for the same language may implement this differently. It’s art rather than science. The third point, connection management, is where you see an oddly large variance among different libraries for such a technical point.

The Redis connections are persistent between the client (your app) and the Redis server. In contrast, many other APIs rely on a single-use connection that is used once then disposed. If you’ve ever used a REST interface, it follows this model. The persistent connection is fast because it doesn’t have to deal with overhead of creating and destroying connections. It does present some challenges, however: the client library needs to manage how the connection is reused (or not) and shared (or not). Opinions on this management as well as runtime characteristics of languages explain why the landscape remains fairly wide open on this point of client architecture.

There are three basic schools of thought regarding connection management:

1. **Unmanaged**
1. **Pooled**
1. **Multiplexed**

**Unmanaged connections** are those that defer the management of the connection to the application itself. A prime example would be the [node_redis library](https://github.com/NodeRedis/node-redis), which provides very little in terms of managing the connection aside from basic reconnection logic. The Node.js world is JavaScript, which is asynchronous by nature and single threaded, so much of the scaling of a Node.js applications occurs by running multiple instances of the application.

**Pooled connections** keep a series of connections to the Redis server ready at any given time and then allow for the application to pluck one of these connections from the pool, use it, and return it when done. [Jedis for Java](https://github.com/xetorthio/jedis) uses this technique as Java is threaded and it allows for a more logical sharing of the connections across threads.

Finally, we have **multiplexing**. In multiplexing, you take many threads and share a single connection. [StackExchange.Redis](https://github.com/StackExchange/StackExchange.Redis) for the .NET ecosystem uses this model. This may sound counter productive, but let’s look more closely at how it works and what it means for your application.

## Multiplexing pros

Visually, you can think of multiplexing a bit like a rope being braided. Many strands are arranged in a particular way to yield a single strand at the other end. In a multithreaded runtime, you’re not exclusively giving any thread full control over the communication with the Redis server. Instead, you’re letting the client library take communication from those threads and intelligently merge it into a single connection. Then, as communication is returned from the Redis server, you’re unwinding the responses back to each individual thread.

![](/images/site-mirror/d2cbc3c5c9ddd353ad53037016c183856f13e64e-300x152.webp)

This gives the client a few obvious advantages. Multiplexing can handle a large number of independent execution threads that get created and destroyed arbitrarily without having to create and destroy connections (which is expensive for both your application and Redis). Secondly, unlike a pooled interface, you don’t have to worry about getting and returning the connection from the pool.

Less apparently, there are other advantages. Multiplexing allows for a form of implicit pipelining. Pipelining, in the Redis sense, meaning sending commands to the server without regard for the response being received. If you’ve ever been through a drive-through window and rattled off your entire order into the speaker, this is like pipelining. You don’t wait for confirmation from the restaurant employee for each item, instead they just read back the entire order at the end. This is naturally just faster as it removes the latency between sending and awaiting the response to each item.

| Pipelined | Non-pipelined |
|---|---|
| SADD order cheeseburgerSADD order milkshakeSADD order large-frySADD order chicken-sandwichSADD order onion-ringsSADD order small-sprite111111 | SADD order cheeseburger(latency)1(latency)SADD order milkshake(latency)1(latency)SADD order large-fry(latency)1(latency)SADD order chicken-sandwich(latency)1(latency)SADD order onion-rings(latency)1(latency)SADD order small-sprite(latency)1 |

When using a multiplexer, all commands are pressed into the same connection at all times, so unrelated threads with unrelated Redis commands are sent immediately to the server, no waiting for a connection from the pool to be available or any responses to come back. And your application is none the wiser to all of this.

## Multiplexing woes

Like most things in computing, multiplexing does not come without a cost. Using a single connection is not always advantageous. Certain operations in Redis intentionally take a long time to respond: these are collectively known as client-blocking operations. Client-blocking operations withhold a response until a condition is met, usually until a new item is added to a structure or when a timeout elapses, whichever comes first. These commands are [BLPOP](https://redis.io/commands/blpop), [BRPOP](https://redis.io/commands/brpop), [BRPOPLPUSH](https://redis.io/commands/brpoplpush), [BZPOPMIN](https://redis.io/commands/bzpopmin), [BZPOPMAX](https://redis.io/commands/bzpopmax), [XREAD…BLOCK](https://redis.io/commands/xread), and [XREADGROUP…BLOCK](https://redis.io/commands/xreadgroup).

If you think about this from the perspective of multiplexing, as soon as one of these commands is issued, all traffic between all threads of your application and the Redis server are placed on hold until new data arrives or the timeout is met. Not good! For this reason StackExchange.Redis does not support these commands (and [according to the current documentation, will never support them](https://stackexchange.github.io/StackExchange.Redis/PipelinesMultiplexers#multiplexing)).

If you ever played with the Redis Pub/Sub command you’ll notice that the [SUBSCRIBE](https://redis.io/commands/subscribe) command works somewhat like this, so how does the multiplexer manage that? In effect, it creates a single dedicated subscription connection to Redis, then multiplexes any published messages out to the relevant threads as they come in.

Finally, the multiplexer has different dynamics than other clients when very large pieces of data are sent or received from Redis. Imagine sending a 500MB chunk of data to Redis. Redis itself, being single threaded, will be devoted to receiving this data, but your client application cannot continue to add to the pipeline until the entire 500MB is finished on that end as well. The same goes for receiving large pieces of data from Redis.

## Multiplexing: it’s complicated

StackExchange.Redis is a good client and multiplexing is an interesting architecture for a Redis client library. It is important to know what you are dealing with though: on one hand multiplexing solves a common problem (latency) and, on the other hand, it limits some functionality of Redis.

It’s also useful to understand how current and future variants in the Redis ecosystem will interact with this client architecture. Redis Enterprise is based on a zero-latency proxy process that does some automatic pipelining internally on the cluster side, which mutes some of multiplexing’s advantages.

Additionally, the upcoming release of [Redis 6](http://antirez.com/news/131) will raise two new challenges to the multiplexer model. In Redis 6, [ACLs will control what keys and commands individual users can use](/blog/getting-started-with-redis-6-access-control-lists-acls/), so a multiplexed connection will be counterproductive if it must constantly switch user contexts. Redis 6 also introduces threaded I/O, which means the processing delta between the single connection on the client side and multi-threaded server-side connections will likely grow.

On the other hand, there are many well-written existing applications and libraries in the .NET ecosystem that will automatically take advantage of optimization in Redis 6 and will continue to operate lightning fast without code changes. And be aware that the author of the StackExchange.Redis library, [Marc Gravell](https://twitter.com/marcgravell), [recently hinted in a tweet](https://twitter.com/marcgravell/status/1226442421715816448) that he’s considering some changes in the new version that may change the architecture of the library away from multiplexing.
