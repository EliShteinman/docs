---
title: "Redis 6.2—the “Community Edition”—Is Now Available"
linkTitle: "Redis 6.2—the “Community Edition”—Is Now Available"
url: "/blog/redis-6-2-the-community-edition-is-now-available/"
description: "Not long ago—just four days before the project’s 12th birthday—we published the general availability release of Redis 6.2. Despite being “just” another minor open source Redis release, version 6.2..."
date: 2021-03-09
blogCategories:
- "Tech"
authors:
- "Itamar Haber"
lastmod: 2025-03-27
hidden: true
---

*By Itamar Haber, Technology Evangelist · Published 9 March 2021 · updated 27 March 2025*

![Blog tile image](/images/site-mirror/af94fb5ef8faeb869d3d86aac411e1686c0c276f-773x521.webp)

Not long ago—just four days before the project’s 12th birthday—we published the general availability release of [Redis 6.2](https://github.com/redis/redis/releases/tag/6.2.0). Despite being “just” another minor open source Redis release, version 6.2 represents a major milestone for the Redis open source software project.

The new version introducesdozens of new commands and extensions to existing ones. Along with performance and memory optimizations, it is also supported by older operating systems. And it demonstrates the new management principles of the Redis project’s development and also reverts several historical decisions. While all these improvements are great, they’re not enough to make Redis 6.2 a major event. Yet the new version of Redis is actually a really big deal.

That’s true because of the **intense involvement of the Redis community**, which is why I like referring to Redis 6.2 as the “Community Edition,” albeit not in the term’s usual sense.

Allow me to explain.

Unless you’ve been living under a rock, you probably already know that last year [antirez (Redis creator Salvatore Sanfilippo) ](http://antirez.com/news/133)stepped back from maintaining the project and that we’ve adopted a new [governance model](/blog/new-governance-for-redis/). The project is now led by the [Redis core team](/blog/redis-core-team-update/), which consists of Madelyn Olson from Amazon Web Services, Zhao Zhao from Alibaba Cloud, and Redis’ Yossi Gottlieb, Oran Agra, and myself.

## Community is Redis’ most important asset

Following a brief period of reorientation, the core team unanimously agreed that the project’s community is Redis’ most important asset. Our collective awesomeness as Redis’ maintainers will only be as useful as the value we provide our members. The team firmly believes that the project’s long-term value and sustainability depend on open, transparent, and full-duplex communication and cooperation between the developers and the users. After all, the users are also developers and technical folks from all walks of life who care deeply about Redis.

So the team sat down together online (even pre-pandemic, because we are distributed all over the world) and started to plan our next steps. There were a myriad of tasks that needed attention: issues to triage, bugs to reproduce and squash, improvements and optimizations to implement, pull requests to review and merge, features to design and develop, wishes to grant and fulfill, and more. The TODO list was and is long and ambitious.

To have a real chance to move Redis forward, we needed help from the larger Redis community. I am happy to report that more than 35 developers (not counting the core team) contributed their brain-cycles in the making of Redis 6.2. While it seems like we’re doing something right, we would love to have even more community members contribute to Redis.

## Basic principles for Redis

To help make the most of Redis community participation, we also spent time setting principles to guide our activities. The updated definition of the [Redis release cycle](https://redis.io/topics/releases) captures some of these principles and sets the guidelines for release schedules, backward compatibility, and support. To adhere to this “formal obligation” and effectuate it, we assembled the contents of Redis 6.2 based on several criteria.

From a technical standpoint, a minor release like this allows us to add new functionality as well as modify existing behaviors. So Redis 6.2 was the perfect vehicle to make these changes before we set out to work in earnest on Redis 7. The 6.2 release also gave us the opportunity to address issues important to the community, regardless of their date of creation and open/closed status. The [release notes](https://github.com/redis/redis/blob/6.2/00-RELEASENOTES) detail all the changes, so I’ll focus on a few key examples:

One place where the community’s voice was heard loud and clear is the relaxation of requirements for compiling Redis (see [PR #7707](https://github.com/redis/redis/pull/7707)). In this regard, Redis 6.0 made a big change by requiring compiler support for C11 and atomics. Because these are available only with newer versions of operating systems, the move left many community members frustrated and unable to use Redis. The backlash feedback from the community (see [issue #7509](https://github.com/redis/redis/issues/7509) and its duplicates) was all the motivation we needed to resolve it. Even better, it was the community, and specifically Wang Yuan ([@ShooterIT](https://twitter.com/shooter_it) on Twitter) in this case, who contributed the fix. Those kinds of community contributions led to much of what’s new Redis 6.2.

## What else is new in Redis 6.2?

Besides the usual fixes and optimizations, Redis 6.2 brings more than 25 new commands. These are mostly small-ish features requested over the years by a substantial number of members in order to improve the project’s usability. For one reason or another, these extensions never made it into Redis despite offering real value. For example, the oldest issue addressed by this release is the [11-year-long absence of ZUNION and ZINTER](https://code.google.com/archive/p/redis/issues/328) from Redis. In that case, resolving the issue wasn’t merely about API-completeness but mainly to address the itch that only these commands can scratch, namely returning the results rather than storing them (which is what the new commands’ existing counterparts, ZUNIONSTORE and ZINTERSTORE, do).

There’s also the [GETEX](https://redis.io/commands/getex) command, first requested in [2015](https://github.com/redis/redis/issues/2762), which reads a value while setting its time-to-live; the how-come-they-were-never-there-from-the-beginning [HRANDFIELD](https://redis.io/commands/hrandfield) and [ZRANDMEMBER](https://redis.io/commands/zrandmember) commands, which return random values from the Hash and Sorted Set data structures; the [SMISMEMBER](https://redis.io/commands/smismember) and [ZMSCORE](https://redis.io/commands/zmscore) commands are for variadic aficionados who want to query multiple values with one call; the generic [LMOVE](https://redis.io/commands/lmove) command is designed to succeed [RPOPLPUSH](https://redis.io/commands/rpoplpush) and complement the functionality with all conceivable manners of moving elements between the ends of two List data structures; and bounding box [GEOSEARCH](https://redis.io/commands/rpoplpush) queries; to name but a few.

The Streams API, which was introduced in Redis 5.0, also received attention and improvements. The new additions make it simpler and easier to use streams and range from [exclusive range queries](https://redis.io/commands/xrange#exclusive-ranges), through filtering[ pending messages by idle time](https://redis.io/commands/xpending#idle-time-filter), to [trimming by minimal ID (the MINID strategy](https://redis.io/commands/xtrim)) and the [XAUTOCLAIM](https://redis.io/commands/xautoclaim) command, which should bring joy to any consumer group user’s heart by allowing users to reclaim messages lost in processing with a single command.

## Thanks for all the hard work

There’s no need for this post to be a walkthrough to [Redis 6.2’s release notes](https://github.com/redis/redis/blob/6.2/00-RELEASENOTES). More importantly, this release speaks volumes about the Redis community’s commitment to the project and about the momentum of Redis’ development. As an optimist-turned-pessimist, I was cautious about predicting how the Redis community would respond to all the changes to the project over the past year. So I was pleasantly surprised to witness the level of community participation and the number of useful improvements that we were able to put into Redis 6.2.

Big thanks for all the hard work put in by the community’s developers and the entire global Redis community. Now it is time to move on to creating the next release!

*Interested in learning more about Redis 6.2? We’ll be discussing the release and all things Redis at *[*RedisConf 2021*](/redisconf/)*, our annual real-time data conference taking place**** virtually on April 20-21****.*
