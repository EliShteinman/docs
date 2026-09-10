---
title: "HyperLogLog"
linkTitle: "HyperLogLog"
url: "/glossary/hyperloglog/"
description: "HyperLogLog is a probabilistic data structure that is used to estimate the number of distinct elements in a multiset or a stream of data. The basic idea is to count the number of distinct elements..."
lastmod: 2025-06-30
mirrored: true
---

*updated 30 June 2025*

## What is HyperLogLog

HyperLogLog is a probabilistic data structure that is used to estimate the number of distinct elements in a multiset or a stream of data. The basic idea is to count the number of distinct elements in large datasets. Imagine you have a jar full of candy of differing colors but you don’t know how many distinct colors are in the jar. If you wanted to estimate how many different colors were in the jar you could sample a small set of candies and extrapolate that information out to the full jar. This is similar to how HyperLogLog uses a set of hash functions and bins to estimate the number of distinct elements in a large dataset using a small amount of memory. HyperLogLog can estimate the number of distinct elements in a large dataset by analyzing unique hash values that map to different bins, just as you could estimate the number of distinct candy colors in the jar using a small sample.

## Redis HyperLogLog best practices

Unique items can be difficult to count. Usually this means storing every unique item then recalling this information somehow. With Redis, this can be accomplished by using a set and a single command, however both the storage and time complexity of this with very large sets is prohibitive. HyperLogLog provides a probabilistic alternative.

HyperLogLog is similar to a Bloom filter internally as it runs items through a non-cryptographic hash and sets bits in a form of a bitfield. Unlike a Bloom filter, HyperLogLog keeps a counter of items that is incremented when new items are added that have not been previously added. This provides a very low error rate when estimating the unique items (cardinality) of a set. HyperLogLog is built right into Redis.

There are three HyperLogLog commands in Redis: PFADD, PFCOUNT and PFMERGE. Let’s say you’re building a web crawler and you want to estimate the number of unique URLs the page has crawled during a given day. For every page you would run a command like this:

Each key above is indexed by day. To see how many pages were crawled on 2017-11-24, we would run the following command:

To see how many pages were crawled on 2017-11-24 and 2017-11-25, we would use PFMERGE to produce a new key of the union of the two counts. Note that since http://redis.io/ was added to both keys it isn’t counted twice:

This is a multi-key operation, so take care in sharded environments as to make sure your keys end up on the same shard.
