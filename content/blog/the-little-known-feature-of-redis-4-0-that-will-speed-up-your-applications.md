---
title: "The little-known feature of Redis 4.0 that will speed up your applications"
linkTitle: "The little-known feature of Redis 4.0 that will speed up your applications"
url: "/blog/the-little-known-feature-of-redis-4-0-that-will-speed-up-your-applications/"
description: "Redis 4.0 brought an amazing feature to the Redis ecosystem: Modules. Modules are a big shift in Redis — suddenly, it is an open landscape of custom data types and full-speed computation right..."
date: 2018-02-22
blogCategories:
- "Company"
- "Tech"
authors:
- "Redis  "
lastmod: 2025-03-27
hidden: true
---

*By Redis   · Published 22 February 2018 · updated 27 March 2025*

![Blog tile image](/images/blog/0073e867b4e64f59de9047fdcde04295ba647e5c-772x550.webp)

Redis 4.0 brought an amazing feature to the Redis ecosystem: Modules. [Modules](/community/redis-modules-hub/) are a big shift in Redis — suddenly, it is an open landscape of custom data types and full-speed computation right inside Redis. But while most of the fanfare over this release focused on Modules, the new version also introduced a super important command that is a game changer in its own right: [UNLINK](https://redis.io/commands/unlink).

To find out if you can use the UNLINK command, run INFO from redis-cli. The response will tell you all about your server. In the first section (#Server) there should be a line called *redis_version.* If this value is greater than 4.0, you’re ready to use the UNLINK command. All versions of [Redis Enterprise](/) 5.0+ and all new subscriptions of Redis Enterprise Cloud should be able to use the UNLINK command. Not all providers of Redis keep up-to-date, so it’s good to check the version before you change any code.

Let’s review one of the key architectural features of Redis: single threadedness. Redis is, for the most part, a single-threaded application. It does one thing at a time and it does those things super fast. Multi-threading is complicated and introduces locking and other gremlins that, counterintuitively, can slow down an application. While Redis (up to 4.0) did a small number of things multi-threadedly, it generally completes one command before starting another.

Deleting a key (with [DEL](https://redis.io/commands/del)) is normally a command that you probably don’t think much about. High speed writing and reading are things to brag about, but in many cases, removing your data is just as important. Like most other commands in Redis, the DEL command operates in a single thread. This is no big deal if you’ve got a key with a value that is a few kilobytes — it will probably take far less than a millisecond. What happens when your key has a value that is a megabyte ? 100 megabytes? 500 megabytes? Hashes, Sorted Sets, Lists, or Sets are often built by adding items over time, which can result in a multi-gigabyte key. What happens when you delete one of these large keys with DEL? Since Redis is single threaded, your whole server is tied up for… well, a while. Compounding this situation, data held in these keys may have been built over thousands or millions of tiny requests, so the application or operator may have no real understanding of how long it will take for the data to be deleted.

Sanity would tell us not to run a command like this on a Sorted Set with a million members:

```javascript
> ZRANGE some-zset 0 -1
```

However, DEL on *some-zset *will take a similar amount of time — there is no transmission overhead, but there is memory de-allocation that really adds up and all the while you’re dead in the water with your CPU pegged. Prior to UNLINK, you might have resorted to the un-atomic method of doing little deletions in conjunction with SCAN to avoid this de-allocation nightmare. Either way, it’s no fun!

As you might have guessed, it’s UNLINK to the rescue! UNLINK is syntactically the same as DEL but provides a much more ideal solution. First it removes the key from the overall keyspace. Then, in a different thread it starts reclaiming the memory. This is a safe operation from a multithreaded perspective since it (in the main thread) removes the item from the keyspace and thus makes it inaccessible from any Redis command.

If you have big values the speed increase is dramatic — UNLINK is a O(1) operation (per key; in the main thread) regardless of the size of the value held at the key. Whereas a big value could take a few hundred milliseconds or more to delete with DEL, UNLINK will finish in less than a millisecond (including the network round trip). Of course, your server will still need to spend cycles reallocating the value’s memory in another thread (in which the work is O(N), where N is the number of allocations of the deleted value), but your main thread performance is unlikely to be heavily impacted by the operations going on in the other thread.

So, should you just replace all the DELs in your code with UNLINKs? Probably. There are a few small edge cases where DEL is exactly what you want. Here are two I can come up with:

- In a [MULTI](https://redis.io/commands/multi)/[EXEC](https://redis.io/commands/exec) or pipeline, DEL is ideal when adding and deleting large values. In this case, UNLINK wouldn’t free up the space immediately and in heavy traffic scenarios when running up to your memory limit, you could be in trouble.
- When it’s more critical that you can write without eviction over responding quickly.

In a green field environment without extreme memory constraints, it’s really hard to fathom situations where you wouldn’t want UNLINK. UNLINK will provide more consistent behavior and overall better performance and it’s a very small code change (or no-change, if you have the ability to rename commands in your client). If UNLINK is right for your application, go ahead and change your DELs over to UNLINKs and see the improvement.
