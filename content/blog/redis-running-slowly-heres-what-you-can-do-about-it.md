---
title: "Redis Running Slowly? Here’s What You Can Do About it"
linkTitle: "Redis Running Slowly? Here’s What You Can Do About it"
url: "/blog/redis-running-slowly-heres-what-you-can-do-about-it/"
description: "Click here to get started with Redis Enterprise. Redis Enterprise lets you work with any real-time data, at any scale, anywhere."
date: 2014-10-02
blogCategories:
- "Tech"
authors:
- "Itamar Haber"
lastmod: 2026-08-13
hidden: true
mirrored: true
---

*By Itamar Haber, Technology Evangelist · Published 2 October 2014 · updated 13 August 2026*

![Blog tile image](/images/site-mirror/0073e867b4e64f59de9047fdcde04295ba647e5c-772x550.webp)

[*Click here to get started with Redis Enterprise. *](/try-free/)*Redis Enterprise lets you work with any real-time data, at any scale, anywhere.*

![](/images/site-mirror/c9ac6e4964b88ec417f80b0e98598c7d9b439c2a-635x200.webp)

Redis is blazing fast and can easily handle [hundreds of thousands](https://redis.io/topics/benchmarks) to [millions](/blog/the-1-2m-opssec-redis-cloud-cluster-single-server-unbenchmark) of operations per second (of course, YMMV depending on your setup), but there are cases in which you may feel that it is underperforming. This slowness of operations – or latency – can be caused by a variety of things, but once you’ve ruled out the usual suspects (i.e. the server’s hardware/virtualware, storage and network) you should also examine your Redis settings to see what can be optimized.

A good place to start is by verifying that the CPU load of your Redis server is indeed working at full throttle and not blocked somehow. If your Redis process is at a stable 100%, then your issue may be attributed to one or both of two things: your volume of queries and/or slow queries. The optimization of slow running queries (and in most cases the underlying data structures) is an art in itself, but there are still quite a few things that you can try before tryin other measures like upgrading your hardware or clustering Redis.

Review your Redis’ [SLOWLOG](https://redis.io/commands/slowlog) to ensure that there aren’t any particularly [slow queries](/blog/how-slow-queries-hurt-your-business/) in it – these should be easily identifiable by their high execution times (the third integer in each log entry). Higher execution times mean higher latency, but remember that some of Redis’ commands (such as Sorted Set operations) can take longer to complete, depending on their arguments and the size of data that they process. By using Redis Cloud’s [enhanced version of the SLOWLOG](/blog/enhancing-redis-slow-log) or doing the math in your head, you can further drill down to identify the troublemakers.

Next, take a look at the output of the [INFO ALL](https://redis.io/commands/info) command. Use your experience, keen judgment and cold logic to answer this question – does anything look weird? 🙂 When not tracking [persistent storage](/blog/5-tips-for-running-redis-over-aws#tip3), [networking](/blog/top-redis-headaches-for-devops-client-buffers) or [replication](/blog/top-redis-headaches-for-devops-replication-buffer) bottlenecks, you should focus on the **stats** and **commandstats** sections.

When the value of your **total_connections_received** in the stats section is absurdly high, it usually means that your application is opening and closing a connection for every request it makes. Opening a connection is an expensive operation that adds to both client and server latency. To rectify this, consult your Redis client’s documentation and configure it to use persistent connections.

Use the information in the commandstats section to hone in on the commands that occupy most of your server’s resources. Look for easy kills by replacing commands with their variadic counterparts. Some of Redis’ commands (e.g. GET, SET, HGET & HSET) sport a variadic version (i.e. MGET, MSET, HMGET & HMSET, respectively), whereas others have infinite arity built right into them (DEL, HDEL, LPUSH, SADD, ZADD, etc). By replacing multiple calls to the same command with a single call, you’ll be shaving off precious microseconds, while saving on both server and client resources.

If you’re managing big data structures in your Redis database and you’re fetching all their content (using HGETALL, SMEMBERS or ZRANGE, for example), consider using the respective [SCAN](https://redis.io/commands/scan) command instead. SCAN iterates through the Redis keys’ namespace and should always be used instead of the [“evil” KEYS command](/blog/5-key-takeaways-for-developing-with-redis#tip4). As an added bonus, SCAN’s variants for Hashes, Sets and Sorted Sets (HSCAN, SSCAN and ZSCAN) can also help you free up Redis just enough to reduce overall latencies.

Another way to reduce the latency of Redis queries is by using [pipelining](https://redis.io/topics/pipelining). When you pipeline a group of operations, they are sent in a single batch that, while bigger and slower to process, requires only a single request-response round trip. This consolidation of trips makes for substantial overall latency reductions. Note, however, that a pipeline operation could block your application if it is waiting for replies without sending the pipeline – Redis will provide all of the replies to the pipelined stream of commands only after the pipeline has been sent. Also bear in mind that when using pipelining, Redis caches all the responses in memory before returning them to the client in bulk, so pipelining thousands of queries (especially those that return a large amount of data) can be taxing to both the server and client. If that is the case, use smaller pipeline sizes.

When pipelining isn’t an option, you can still save big time on round-trip time (RTT) latency by taking the “moonlit” [scripting](https://redis.io/commands/EVAL) road. With [Lua scripting](/blog/5-key-takeaways-for-developing-with-redis#tip5) in Redis, you can use logic that interacts with the data locally, thus saving many potential client-server round trips. To further reduce bandwidth consumption, latency, and to avoid script recompilations, make sure to use [SCRIPT LOAD](https://redis.io/commands/script-load) and [EVALSHA](https://redis.io/commands/evalsha).

**Lua Tips:** Refrain from generating dynamic scripts, which can cause your Lua cache to grow and get out of control. If you have to use dynamic scripting, then just use plain [EVAL](https://redis.io/commands/eval), as there’s no point in loading them first. Also, remember to track your Lua memory consumption and flush the cache periodically with a [SCRIPT FLUSH](https://redis.io/commands/script-flush). Also, do not hardcode and/or programmatically generate key names in your Lua scripts, because doing so will render them useless in a clustered Redis setup.

These are just some of the ways that you can easily get more out of your Redis database without bringing in the heavy artillery. Adopting even one of these suggestions can make a world of difference and lower your latency substantially. Know more tricks of the trade? Have any questions or feedback? Feel free to [shout](https://twitter.com/itamarhaber) at [me](mailto:itamar@redis.com), I’m highly available 🙂
