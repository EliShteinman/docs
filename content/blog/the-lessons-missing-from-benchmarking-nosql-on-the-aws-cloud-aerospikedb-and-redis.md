---
title: "The Lessons Missing from Benchmarking NoSQL on the AWS Cloud (AerospikeDB and Redis)"
linkTitle: "The Lessons Missing from Benchmarking NoSQL on the AWS Cloud (AerospikeDB and Redis)"
url: "/blog/the-lessons-missing-from-benchmarking-nosql-on-the-aws-cloud-aerospikedb-and-redis/"
description: "Delivering on its promise from last week, Aerospike yesterday published the results of a benchmark done by Lynn Langit titled “Lessons Learned – Benchmarking NoSQL on the AWS Cloud (AerospikeDB and..."
date: 2015-01-29
blogCategories:
- "Company"
authors:
- "Itamar Haber"
lastmod: 2025-03-27
hidden: true
---

*By Itamar Haber, Technology Evangelist · Published 29 January 2015 · updated 27 March 2025*

![Blog tile image](/images/site-mirror/c5056d2b9ae7f4c27711115d5878549e3c5adec5-140x92.webp)

![](/images/site-mirror/acd1debe6aa31e22a6b140ed47dd1ef78cc70da6-635x300.webp)

Delivering on its [promise from last week](https://twitter.com/aerospikedb/status/558671732824113152), Aerospike yesterday published the results of a benchmark done by Lynn Langit titled “[Lessons Learned – Benchmarking NoSQL on the AWS Cloud (AerospikeDB and Redis)](http://lynnlangit.com/2015/01/28/lessons-learned-benchmarking-nosql-on-the-aws-cloud-aerospikedb-and-redis/).” Salvatore Sanfilippo, Redis’ creator, posted a response at “[Why we don’t have benchmarks comparing Redis with other DBs](http://antirez.com/news/85),” in which he describes some of the pitfalls of doing ‘comparative “advertising”‘ and provides several approaches for getting better results from Redis.

One thing the benchmark clearly shows is that in some read-write mixes, both Redis and AerospikeDB can be used as “dumb” key-value stores and essentially deliver the same value in terms of throughput per single server. So what is there besides comparable performance? Well, Aerospike rightfully boasts of a nice UI and friendly automations (and I’ve seen [the same for Redis](/redis-enterprise-downloads) :)), but yesterday’s benchmark still leaves some unanswered questions.

Why didn’t the benchmark use conventional, recommended Redis practices such as pipelining and multi-key operations? I imagine it’s because Aerospike doesn’t have the equivalent of these and has to resort to simple GET/SET operations, essentially measuring the network (and OS perhaps) rather than the technology’s true capabilities. Another missing piece is a 20%-80% read/write test (-w RU, 20) and a 100% write test (-w RU, 0). I suspect the results of such runs would not align with the benchmark’s message.

Regardless, why is it that some of the points simply don’t add up? Take, for example, Lynn’s results for the 100% read pattern against the sharded Redis from Test 1 and Test 2. In the first test, the configuration scored 928K TPS whereas in the 2nd test it only reached 860K – a decrease that is totally unexplained by the fact that she used AOF. Even with AOF enabled for Test 2, Redis only accesses the disk in response to changes to the data (a.k.a writes), so AOF should have exactly 0% impact for read-only traffic. That by itself is puzzling, but here’s another curiosity: her benchmark finds that an EBS-backed Redis actually performs better than a Redis server that’s RAM only – again, compare Test 2 and 1’s never-write scores for single shard Redis: 180K and 132K TPS, respectively.

Surprises continue if you compare single-shard Redis in Test 1 and 2 when writes are part of the traffic. In Test 1 (50% and 20% writes), single sharded Redis gets 128K and 129K TPS (respectively), whereas in Test 2 we see the same patterns’ performance improvement (yes, by turning AOF on) with scores of 150K and 164K TPS.

So while the multi-sharded Redis set up mysteriously gets hit by AOF activity (which shouldn’t have been happening in a read-only scenario anyway), the same AOF setting actually boosts performance of the single shard configuration, even with writes. That’s either a paradox, some foul witchcraftery or an act of divine intervention – and I don’t buy it.

Apropos the use of AOF, a common practice (that’s also employed in our Redis deployments) is to have a slave Redis instance deal with persistency considerations to lessen the master’s load. I can only assume that this best practice for Redis wasn’t used because an SSD-optimized, multi-threaded database does things differently.

Comparisons are as hard to do right as they are easy to do wrong, and the effort put into this one is notable. I respect Aerospike’s engineers for uncovering and sharing so many useful network tweaks, and I greatly appreciate the entire team’s attempt at sharding Redis. But in my opinion, the final outcome is somewhat lacking and simply leaves too many loose ends.
