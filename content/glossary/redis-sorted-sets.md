---
title: "Redis Sorted Sets"
linkTitle: "Redis Sorted Sets"
url: "/glossary/redis-sorted-sets/"
description: "Sorted sets in Redis are a powerful data structure that combines the features of sets and sorted lists. They allow you to store a collection of unique elements while assigning a score or rank to..."
lastmod: 2026-05-21
---

*updated 21 May 2026*

Sorted sets in Redis are a powerful data structure that combines the features of sets and sorted lists. They allow you to store a collection of unique elements while assigning a score or rank to each element. This score is used to determine the order of elements in the set, making sorted sets an excellent choice for applications that require ordered data.

In Redis, sorted sets are implemented using a combination of a hash table and a skip list data structure. The hash table provides fast access to elements based on their value, while the skip list maintains the sorted order of the elements based on their scores. This dual structure allows Redis to efficiently perform operations on sorted sets.

## Sorted Set Features

One of the key features of sorted sets is the ability to add, remove, or update elements dynamically while maintaining their sorted order. You can insert elements into a sorted set with an associated score, which can be a floating-point number. Redis uses the score to position the element in the sorted set. If an element with the same value already exists, its score is updated accordingly.

## Operations and Functionality of Sorted Sets in Redis

Sorted sets provide various operations for manipulating the data. You can retrieve elements within a specific range based on their scores, enabling efficient pagination or ranking functionality. Redis supports both inclusive and exclusive range queries, allowing you to fetch elements by their scores or their positions in the sorted set. Additionally, you can perform set operations like union, intersection, and difference on sorted sets, enabling you to combine or compare multiple sorted sets.

Redis also provides efficient methods to increment or decrement the score of an element in a sorted set. This feature is particularly useful in scenarios where you need to track rankings or keep a leaderboard. By incrementing or decrementing the score of an element, you can easily update its position in the sorted set without the need for complex operations.

## Sorted Set Benefits

Sorted sets in Redis offer several benefits. They provide fast access to elements based on their values, thanks to the underlying hash table structure. The skip list ensures efficient ordering and range queries based on scores. Sorted sets are widely used for various applications, including leaderboards, real-time analytics, job scheduling, and more.

## ZSET

Let’s look at some commonly used ZSET commands in table 3.9.Table 3.9 Some common ZSET commands

We’ve used some of these commands in chapters 1 and 2, so they should already be familiar to you. Let’s quickly revisit the use of some of our commands.Listing 3.9 A sample interaction showing some common ZSET commands in Redis>>> conn.zadd(‘zset-key’, ‘a’, 3, ‘b’, 2, ‘c’, 1) 3

Adding members to ZSETs in Python has the arguments reversed compared to standard Redis, which makes the order the same as HASHes.>>> conn.zcard(‘zset-key’) 3

Knowing how large a ZSET is can tell us in some cases if it’s necessary to trim our ZSET.>>> conn.zincrby(‘zset-key’, ‘c’, 3) 4.0

We can also increment members like we can with STRING and HASH values.>>> conn.zscore(‘zset-key’, ‘b’) 2.0

Fetching scores of individual members can be useful if we’ve been keeping counters or toplists.>>> conn.zrank(‘zset-key’, ‘c’) 2

By fetching the 0-indexed position of a member, we can then later use ZRANGE to fetch a range of the values easily.>>> conn.zcount(‘zset-key’, 0, 3) 2L

Counting the number of items with a given range of scores can be quite useful for some tasks.>>> conn.zrem(‘zset-key’, ‘b’) True

Removing members is as easy as adding them.>>> conn.zrange(‘zset-key’, 0, -1, withscores=True) [(‘a’, 3.0), (‘c’, 4.0)]

For debugging, we usually fetch the entire ZSET with this ZRANGE call, but real use cases will usually fetch items a relatively small group at a time.

You’ll likely remember our use of ZADD, ZREM, ZINCRBY, ZSCORE, and ZRANGE from chapters 1 and 2, so their semantics should come as no surprise. The ZCOUNT command is a little different than the others, primarily meant to let you discover the number of values whose scores are between the provided minimum and maximum scores.

Table 3.10 shows several more ZSET commands in Redis that you’ll find useful.Table 3.10 Commands for fetching and deleting ranges of data from ZSETs and offering SET-like intersections

This is the first time that you’ve seen a few of these commands. If some of the ZREV* commands are confusing, remember that they work the same as their nonreversed counterparts, except that the ZSET behaves as if it were in reverse order (sorted by score from high to low). You can see a few examples of their use in the next listing.Listing 3.10 A sample interaction showing ZINTERSTORE and ZUNIONSTORE>>> conn.zadd(‘zset-1’, ‘a’, 1, ‘b’, 2, ‘c’, 3) 3 >>> conn.zadd(‘zset-2’, ‘b’, 4, ‘c’, 1, ‘d’, 0) 3

We’ll start out by creating a couple of ZSETs.>>> conn.zinterstore(‘zset-i’, [‘zset-1’, ‘zset-2’]) 2L >>> conn.zrange(‘zset-i’, 0, -1, withscores=True) [(‘c’, 4.0), (‘b’, 6.0)]

When performing ZINTERSTORE or ZUNIONSTORE, our default aggregate is sum, so scores of items that are in multiple ZSETs are added.>>> conn.zunionstore(‘zset-u’, [‘zset-1’, ‘zset-2′], aggregate=’min’) 4L >>> conn.zrange(‘zset-u’, 0, -1, withscores=True) [(‘d’, 0.0), (‘a’, 1.0), (‘c’, 1.0), (‘b’, 2.0)]

It’s easy to provide different aggregates, though we’re limited to sum, min, and max.>>> conn.sadd(‘set-1’, ‘a’, ‘d’) 2 >>> conn.zunionstore(‘zset-u2’, [‘zset-1’, ‘zset-2’, ‘set-1’]) 4L >>> conn.zrange(‘zset-u2’, 0, -1, withscores=True) [(‘d’, 1.0), (‘a’, 2.0), (‘c’, 4.0), (‘b’, 6.0)]

We can also pass SETs as inputs to ZINTERSTORE and ZUNIONSTORE; they behave as though they were ZSETs with all scores equal to 1.

ZSET union and intersection can be difficult to understand at first glance, so let’s look at some figures that show what happens during the processes of both intersection and union. Figure 3.1 shows the intersection of the two ZSETs and the final ZSET result. In this case, our aggregate is the default of sum, so scores are added.

Unlike intersection, when we perform a union operation, items that exist in at least one of the input ZSETs are included in the output. Figure 3.2 shows the result of performing a union operation with a different aggregate function, min, which takes the minimum score if a member is in multiple input ZSETs.

In chapter 1, we used the fact that we can include SETs as part of ZSET union and intersection operations. This feature allowed us to easily add and remove articles from groups without needing to propagate scoring and insertion times into additional ZSETs. Figure 3.3 shows a ZUNIONSTORE call that combines two ZSETs with one SET to produce a final ZSET.

![RIA Figure 3.1](/images/site-mirror/add86a280f987fcbef4e0cb7cf0bd93c7dc3f6ba-326x72.svg)

*Figure 3.1 What happens when calling conn.zinterstore(‘zset-i’, [‘zset-1’, ‘zset-2’]); elements that exist in both zset-1 and zset-2 are added together to get zset-i*

![RIA Figure 3.2](/images/site-mirror/535298d9381de0de2722650fbbade976b16e7e18-326x84.svg)

*Figure 3.2 What happens when calling conn.zunionstore(‘zset-u’, [‘zset-1’, ‘zset-2′], aggregate=’min’); elements that exist in either zset-1 or zset-2 are combined with the minimum function to get zset-u*

![RIA Figure 3.3](/images/site-mirror/ecebcffba7cac6417ded89f96f04976dba7399e2-371x83.svg)

*Figure 3.3 What happens when calling conn.zunionstore(‘zset-u2’, [‘zset-1’, ‘zset-2’, ‘set-1’]); elements that exist in any of zset-1, zset-2, or set-1 are combined via addition to get zset-u2*

In chapter 7, we’ll use ZINTERSTORE and ZUNIONSTORE as parts of a few different types of search. We’ll also talk about a few different ways to combine ZSET scores with the optional WEIGHTS parameter to further extend the types of problems that can be solved with SETs and ZSETs.

As you’re developing applications, you may have come upon a pattern known as publish/subscribe, also referred to as *pub/sub*. Redis includes this functionality, which we’ll cover next.

2 Scores are actually stored inside Redis as IEEE 754 floating-point doubles.
