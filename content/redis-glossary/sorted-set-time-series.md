---
title: "Sorted Set Time Series"
linkTitle: "Sorted Set Time Series"
url: "/glossary/sorted-set-time-series/"
description: "Time series with Sorted Sets (zsets) are the typical way of modeling time series data in Redis. Sorted Sets are made up of unique members with a score all stored under a single key. Using this data..."
lastmod: 2025-06-30
mirrored: true
---

*updated 30 June 2025*

## Redis Sorted Set Time Series best practices

Time series with Sorted Sets (zsets) are the typical way of modeling time series data in Redis. Sorted Sets are made up of unique members with a score all stored under a single key. Using this data type for Sorted Sets means having the score act as some sort of indication of time (often a millisecond precision timestamp, although not always) and the member being the data recorded. The one catch is that, since this is a form of Set, only unique members are allowed and trying to record a time series entry with the same value as a previous member will result in only updating the score. To illustrate this problem, take the following example of recording temperature over time:

If you just added this directly as a Sorted Set using [ZADD](https://redis.io/commands/zadd), you would miss some data points:

**ANTI-PATTERN**

[**ZRANGEBYSCORE**](https://redis.io/commands/zrangebyscore)

**ANTI-PATTERN**

Notice how the third ZADD returns a 0 – this indicates that a new member was not added to the sorted set. Then, in the ZRANGEBYSCORE, we can see the that the sorted set only has two entries, …7001 and …6001, with …5001 missing. Why? In this case because both …7001 and …5001 share the same member (21) we only updated the score for the member. Not good!

There are several ways of approaching this problem. The first is to include some sort of random data with sufficient entropy to ensure uniqueness. Let’s examine this method. First, we’ll create a pseudo-random floating point number between 0 (inclusive) and 1 (exclusive) then we’ll add this to our timestamp. For our example, we’ll leave it in decimal form for readability (in a real workload, it would be smart to just convert it back to a raw 8 bytes to save storage space).

As you can see, all ZADDs are returning 1s indicating new additions and the ZRANGEBYSCORE returns all the values. This is workable method, however it is not very efficient with wasted bytes to ensure uniqueness which adds to storage overhead. For most use cases, the uniqueness will be just discarded by your application. It should be noted that adding uniqueness obviously would not be needed if your data would already be unique (for example, some data that includes a UUID).

With this method you have access to all the sorted set methods to allow for analysis and manipulation:

- ZRANGEBYSCORE allows you to get a specific slice between two timestamps
(ZREVRANGEBYSCORE for descending ordering)
- ZREMRANGEBYSCORE allows for removal of a specific range of timestamps
- [ZCOUNT](https://redis.io/commands/zcount) the number of items between a range of timestamps
- [ZINTERSTORE](https://redis.io/commands/zinterstore)‡ allows you to intersect two time-series data sets and save it in a new key
- [ZUNIONSTORE](https://redis.io/commands/zunionstore)‡ allows you to combine two time-series data sets and save it in a new key. It can also be used to duplicate a sorted set.

‡ ZINTERSTORE and ZUNIONSTORE are multi-key operations. Care should be taken when working in a sharded environment to make sure that your new key ends up on the same shard, otherwise these commands will end in an error.
