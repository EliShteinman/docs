---
title: "Diving Into Redis 6.0"
linkTitle: "Diving Into Redis 6.0"
url: "/blog/diving-into-redis-6/"
description: "Download the latest version by clicking here."
date: 2020-04-30
blogCategories:
- "Product Releases"
- "Tech"
authors:
- "Redis  "
lastmod: 2026-06-01
hidden: true
mirrored: true
---

*By Redis   · Published 30 April 2020 · updated 1 June 2026*

![Blog tile image](/images/site-mirror/e11a23ca2757d57e1a7c0a8ac428b0e8f9b1685c-772x520.webp)

[*Download the latest version by clicking here*](https://redis.io/download?_ga=2.182771878.1286583108.1662571050-1570724325.1643248711).

You know the warning on the shallow end of the pool where it says “NO DIVING”? Well, the new Redis 6 is no shallow update to the world’s most-loved database—it’s so deep you can dive right in. Now that Salvatore Sanfilippo has made Redis 6 generally available, let’s take a dip in the new changes and features.

The new stuff can be divided into a few different categories: security, performance, ease-of-use, and even some entirely new functionality. Each category holds a number of improvements, so read carefully to learn how they can fundamentally change how you use Redis.

## Redis 6 brings news security features

Perhaps the biggest, most game-changing feature of Redis 6 are access control lists (ACLs). ACLs bring the concept of “users” to Redis. Each user can have a defined set of capabilities that dictate which commands they can run and on what keys. If you’ve been using Redis for a while, you’ve probably put this feature on your wish list—it reduces the need for oopsy moves like running [FLUSHDB](https://redis.io/commands/flushdb) on production servers, and lets you do more sophisticated tasks like creating specific users for specific actions so that every action operates with the [least required privilege](https://en.wikipedia.org/wiki/Principle_of_least_privilege).

Redis clients in [Java](https://github.com/xetorthio/jedis), [Node.js](https://github.com/luin/ioredis), [Python](https://github.com/andymccurdy/redis-py) and [.NET](https://github.com/StackExchange/StackExchange.Redis) already support ACLs, and we expect support to rapidly expand to more languages and libraries now that Redis 6 is generally available.

![](/images/site-mirror/3dfaea8b0ea5d321a505354c56c26d4ec936204d-1024x576.webp)

*ACLs will allow users access to only particular commands, keys, or even patterns of keys based on user-based specified permissions.*

In addition to ACLs, Redis 6 brings the ability to encrypt traffic over SSL. Up until this version, encryption in Redis was deferred outside the process, meaning it required other applications to provide encryption and that many instances were left unencrypted. This is an important step forward for Redis, allowing for use in more environments where encryption is a critical requirement.

## Redis 6 is faster

Despite Redis’ well-deserved reputation for high performance, its single-threaded architecture has been controversial among engineers who wondered if Redis could be even faster. Redis 6 rings in a new era: while it retains a core single-threaded data-access interface, I/O is now threaded.

By delegating the time spent reading and writing to I/O sockets over to other threads, the Redis process can devote more cycles to manipulating, storing, and retrieving data—boosting overall performance. This improvement retains the transactional characteristics of previous versions, so you don’t have to rethink your applications to take advantage of the increased performance. Similarly, Redis’ single-threaded DEL command can now be configured to behave like the multi-thread UNLINK command that has been available since Redis version 4.

The performance of a local variable is almost always unbeatable, Finally, even a database as high performance as Redis will be much slower than accessing something from the stack or heap. Redis 6 adds a new technique for sophisticated client libraries to implement a client-side caching layer to store a subset of data in your own process. This implementation is smart enough to manage multiple updates to the same data and keep your data as in-sync as possible—while retaining the advantages of Redis with the speed of local variables.

## Redis 6 is easier to use

For years, the second version of the Redis protocol (RESP2) has proven to be remarkably flexible. It supports not only Redis’ built-in data structures but also [Redis ](/redis-enterprise/modules/)features and the new commands and data that those bring along. Redis 6 starts support for a new version of the protocol, RESP3. This new protocol is an evolution of the previous version that adds richness to results, which let interfacing libraries better map Redis responses with variable types in the host language. Additionally, this version of the protocol paves the way for thinner client libraries with less code and will eventually allow for more-rapid adoption of new commands and features. RESP2 will be with us for quite a while as it will take the community some time to migrate software, tools, and client libraries to the new protocol. But if you want to dive in headfirst, you can try out RESP3 on Redis 6 now—just understand that RESP3 is still in an early phase of development.

Redis Cluster greatly expands the variety of Redis uses, but it does require a more complex client library. In smaller language communities, the client libraries to support cluster never fully emerged. Thankfully, Redis 6.0 comes complete with a cluster proxy to assist language platforms that do not support the Redis Cluster API to connect to Redis clusters. This masks the complexity, so only a simple single-instance library implementation is required.

Since Redis 1.0, developers have been able to set keys to expire after a given time, a feature indispensable for caching. This expiration has always relied on sampling techniques to avoid unpredictable delays when many keys expire at the same time. The expiration cycle has been rewritten in Redis 6.0 to allow for much faster expirations that more closely match the time-to-live (TTL) property. Additionally, you can now tune expirations to zero in on the accuracy required for your particular situation.

## Meet the longest common subsequence family

And now for something completely different. In a recent surprise for the community, Salvatore, the author of Redis, released a new command *family *for version 6*. *The [longest common subsequence (LCS) commands](https://twitter.com/antirez/status/1245377579034517506) can be used to find non-contiguous sequences among strings. If you’ve ever used a diff, then you’ve indirectly used this algorithm. In Salvatore’s own eponymic example:

STRALGO LCS STRINGS salvatore sanfilippo

"salo"

How did this command come up with that result?

**salvato**re **sa**nfi**l**ipp**o**

As you can see, the STRALGO LCS STRINGS command is skipping over a number of bytes—and that can be a different number for each argument trying to find the longest sequence of common bytes.

That’s only the beginning, there is a lot more to this new capability of Redis. Since the LCS family of commands works on binary data—like almost everything else in Redis—just think about the possibilities outside of text processing. [Salvatore has mentioned the possibilities of using it for RNA and DNA analysis](https://twitter.com/antirez/status/1245377580880060422). Pretty neat, but keep in mind this is a very new command that you may want to treat like a sandbox—the command name changed as of last week, so don’t be surprised if it isn’t supported everywhere.

## Get started with Redis 6

Redis 6 opens up vast new possibilities for the Redis community. It brings everything from better security to incremental performance improvements, not to mention being easier to use and introducing new ways to use Redis. If you’re ready to get started, you can[ download the brand new version right now from redis.io](https://redis.io/download)! To learn more about general availability of Redis Enterprise 6.0, which utilizes Redis 6’s improvements and takes Redis security to an even higher level, see our post on [Rediscover Redis Security with Redis Enterprise 6.0](/blog/rediscover-redis-security-with-redis-enterprise-6/).
