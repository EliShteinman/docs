---
title: "Enhancing Redis Slow Log"
linkTitle: "Enhancing Redis Slow Log"
url: "/blog/enhancing-redis-slow-log/"
description: "Redis Slow Log is one of the best tools for debugging and tracing your Redis database, especially if you experience high latency and high CPU usage with Redis operations. This online discussion in..."
date: 2013-01-17
blogCategories:
- "Tech"
authors:
- "Redis  "
lastmod: 2026-08-13
hidden: true
mirrored: true
---

*By Redis   · Published 17 January 2013 · updated 13 August 2026*

![Blog tile image](/images/site-mirror/0073e867b4e64f59de9047fdcde04295ba647e5c-772x550.webp)

[Redis Slow Log](https://redis.io/commands/slowlog) is one of the best tools for debugging and tracing your Redis database, especially if you experience high latency and high CPU usage with Redis operations. [This online discussion](https://groups.google.com/forum/?fromgroups=#!searchin/redis-db/Strange$20growing$20cpu$20usage$20in$202.6.7/redis-db/zY9FMEMBnJA/Eenw58zspe4J) in a Redis DB group is just one of many examples that show how efficient Redis Slow Log is. Because Redis is based on a single threaded architecture, Redis Slow Log can be much more useful than slow log mechanisms of multi-threaded database systems such as MySQL Slow Query Log.

Unlike tools that include the software locking overhead which makes the debugging process very complex, Redis Slow Log is highly effective at showing the actual processing time of each slow command. As a provider of [Redis Cloud](https://redis.io/cloud/), we use Redis Slow Log intensively for internal monitoring and to help our users solve latency issues related to their complex queries. And we often find ourselves struggling to understand the differences between two execution times of the same Redis command shown in the Slow Log – usually with complex commands such as [ZUNIONSTORE](https://redis.io/commands/zunionstore), [ZINTERSTORE](https://redis.io/commands/zinterstore), [ZRANGEBYSCORE](https://redis.io/commands/zrangebyscore). Based on our experience, we thought the Redis community could benefit from adding the time complexity parameters for each command stored in the Slow Log. With this enhancement, we expect users to get a better understanding of their Redis DB operations, including differences between execution times of the same command and spikes in CPU usage. So without further ado, here’s (bold) what we’ve contributed for the Enhanced Redis Slow Log:

| 33) 1) (integer) 468359   2) (integer) 1358158701 3) (integer) 132912 4) Complexity info: N:48362,M:38687 5)1) “ZUNIONSTORE” 2) “AAA” 3) “5” 4) “BBB” 5) “CCC” 6) “DDD” 7) “EEE” 8) “FFF” 9) “WEIGHTS” 10) “1” 11) “1” 12) “1” 13) “1” 14) “1” 15) “AGGREGATE” 16) “MIN” 34) 1) (integer) 61701 2) (integer) 1354754379 3) (integer) 15217 4) Complexity info: N:886,M:885 5) 1) “ZREVRANGE” 2) “XYZ” 3) ”1” 4) ”1000” 5) “WITHSCORES” 35) 1) (integer) 61700 2) (integer) 1354754379 3) (integer) 16067 4) Complexity info: N:897,K:2,M:897 5) 1) “ZINTERSTORE” 2) “XYZ” 3) ”2” 4) ”YZX” 5) “ZXY” |
|---|

For better understanding of the complexity, you may want to use the table below:

| Command | Value of interest | Complexity |
|---|---|---|
| LINSERT | N – list len | O(N) |
| LREM | N – list len | O(N) |
| LTRIM | N – number of removed elemnts | O(N) |
| PUBLISH | N – number of channel subscribersM – number of subscribed patterns | O(N+M) |
| PSUBSCRIBE | N – number of patterns client is subscribed toargc – number of arguments passed to the command | O(argc*N) |
| PUNSUBSCRIBE | N – number of patterns client is subscribed toM – total number of subscribed patternsargc – number of arguments passed to the command | O(argc*(N+M)) |
| SDIFF | N – total number of elements in all sets | O(N) |
| SDIFFSTORE | N – total number of elements in all sets | O(N) |
| SINTER | N – number of elements in smallest setargc – number of arguments passed to the command | O(argc*N) |
| SINTERSTORE | N – number of elements in smallest setargc – number of arguments passed to the command | O(argc*N) |
| SMEMBERS | N – number of elements in a set | O(N) |
| SORT | N – number of elements in the list/set/zsetM – number of elements in result | O(N+M*log(M))O(N) when no sorting |
| SUNION | N – total number of elements in all sets | O(N) |
| SUNIONSTORE | N – total number of elements in all sets | O(N) |
| UNSUBSCRIBE | N – total number of clients subscribed to all channels | O(N) |
| ZADD | N – number of elements in the zset | O(log(N)) |
| ZCOUNT | N – number of elements in the zsetM – number of elements between min and max | O(log(N)+M) |
| ZINCRBY | N – number of elements in the zset | O(log(N)) |
| ZINTERSTORE | N – number of elements in the smallest zsetK – number of zsetsM – number of elements in the results set | O(N*K)+O(M*log(M)) |
| ZRANGE | N – number of elements in the zsetM – number of results | O(log(N)+M) |
| ZRANGEBYSCORE | N – number of elements in the zsetM – number of results | O(log(N)+M) |
| ZRANK | N – number of elements in the zset | O(log(N)) |
| ZREM | N – number of elements in the zsetargc – number of arguments passed to the command | O(argc*log(N)) |
| ZREMRANGEBYRANK | N – number of elements in the zsetM – number of elements removed | O(log(N)+M) |
| ZREMRANGEBYSCORE | N – number of elements in the zsetM – number of elements removed | O(log(N)+M) |
| ZREVRANGE | N – number of elements in the zsetM – number of results | O(log(N)+M) |
| ZREVRANK | N – number of elements in the zset | O(log(N)) |
| ZUNIONSTORE | N – sum of element counts of all zsetsM – element count of result | O(N)+O(M*log(M)) |

For those who are interested, this enhancement is part of our extended Redis 2.6. version and can be found [here](https://github.com/Redis) in our GitHub account.
