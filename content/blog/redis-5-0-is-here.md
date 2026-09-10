---
title: "Redis 5.0 is here!"
linkTitle: "Redis 5.0 is here!"
url: "/blog/redis-5-0-is-here/"
description: "Last week, Redis reached a major milestone with the release of 5.0, which includes a variety of advancements and improvements. The big story here is the introduction of Streams as part of the..."
date: 2018-10-22
blogCategories:
- "Announcements"
- "New Product Announcements"
- "Product Releases"
- "Redis Open Source"
authors:
- "Redis  "
lastmod: 2026-06-01
hidden: true
mirrored: true
---

*By Redis   · Published 22 October 2018 · updated 1 June 2026*

![Blog tile image](/images/site-mirror/0073e867b4e64f59de9047fdcde04295ba647e5c-772x550.webp)

Last week, Redis reached a major milestone with the release of 5.0, which includes a variety of advancements and improvements. The big story here is the introduction of Streams as part of the release. Streams is the first entirely new data structure in Redis since HyperLogLog was introduced as part of 2.8.9 back in April 2014 (over four years ago)!

## Streams

So what is Redis Streams, you may ask? A Redis Stream is a log-like data structure that allows you to store multiple fields and string values with an automatic, time-based sequence at a single key. In many ways, Streams resembles other Redis data structures — it orders data in a manner reminiscent of Lists, it stores fields and values similar to Hashes, it enables you to read ranges of values like you can with Sorted Sets, and it can behave somewhat like Pub/Sub (or Lists) with blocking behavior that waits for items to arrive, allowing for real-time reactions to the stream.

All that said, a Redis Stream is quite distinctly its own thing. It’s not exactly fair to say they are like structure *foo* but with feature *bar*. There is a unique capability of Redis Streams that sets it apart from any other existing data structure: consumer groups that allow various clients to consume a stream with their own position. This enables a whole new collection of uses for Redis; tasks like event sourcing or unified log architecture are now not only possible but also optimal. As with any Redis data structure, there are also numerous commands (13, in fact) that allow you to interact with the structure — you can find a list of these commands at [redis.io](https://redis.io/commands#stream).

## ZPOP and friends

With the latest release, sorted sets have now gained a few new commands that allow you to remove the highest- (ZPOPMAX) or lowest- (ZPOPMIN) scoring member of a sorted set. An oft-requested feature, this enables some new patterns that were previously only accessible with Lua scripting.

Accompanying ZPOPMIN and ZPOPMAX are the blocking variants (BZPOPMIN/BZPOPMAX) that wait for a value to arrive, similar to the blocking behavior of lists (BLPOP, as an example). So not only can you now remove the highest or lowest values, but also you can wait for members to arrive.

## Other improvements

Aside from new commands and data structures, the 5.0 release includes many refinements to existing internals including:

- New Modules API capabilities
- Improvements in HyperLogLog implementation
- HELP for many sub-commands
- Enhancements to memory management and reporting
- RDB storing frequency and recency information about keys (i.e. LFU, LRU)
- Lua replica and AOF refinements
- Networking and client connection management improvements
- Client identification and blocking management between clients

For a bit of fun, we have also added the useless [yet entertaining](http://antirez.com/news/123) LOLWUT command, which generates some computer art using random elements and command arguments. It doesn’t have a significant technical purpose, but it might be a nice thing to test to see if Redis 5.0 is running properly when connecting to an instance of an unknown version.

![Art inside a database command](/images/site-mirror/9b83976685f93af7afcd4b50d7ea3e706dd8081f-456x536.webp)

(From [LOLWUT: a piece of art inside a database command](http://antirez.com/news/123))

For more details or background on the improvements, you are welcome to take a look at the [release notes](https://raw.githubusercontent.com/antirez/redis/5.0/00-RELEASENOTES).

## Redis Enterprise

If you’re itching to try Redis 5.0 in Enterprise — especially Streams — you can download [Redis Enterprise Software 5.4](/blog/redis-enterprise-5-4-supports-redis-streams-ga/), which includes Redis 5.0. And you want to run it on our fully managed [VPC](/redis-enterprise/vpc/) offering.

Happy Streaming!
