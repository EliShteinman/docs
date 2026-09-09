---
title: "Rising NoSQL Star: Aerospike, Cassandra, Couchbase or Redis?"
linkTitle: "Rising NoSQL Star: Aerospike, Cassandra, Couchbase or Redis?"
url: "/blog/rising-nosql-star-aerospike-cassandra-couchbase-or-redis/"
description: "A new NoSQL benchmark was just released by Avalon Consulting, LLC, and I couldn’t be happier to brag that Redis out-performed its competitors by a landslide. With more than double the throughput..."
date: 2015-06-04
blogCategories:
- "Tech"
authors:
- "Itamar Haber"
lastmod: 2025-03-27
hidden: true
---

*By Itamar Haber, Technology Evangelist · Published 4 June 2015 · updated 27 March 2025*

![Blog tile image](/images/site-mirror/f13b02ddbd943e99efdae5855f6190818e266d33-152x152.webp)

![](/images/site-mirror/09c7d666a72220f3f7b1eae9a698b30da795ac11-635x200.webp)

> “I always knew I was a star, and now the rest of the world seems to agree with me.” — Freddie Mercury

A new NoSQL benchmark was just released by [Avalon Consulting, LLC](http://www.avalonconsult.com/), and I couldn’t be happier to brag that Redis out-performed its competitors by a landslide. With more than double the throughput and half the latency of other NoSQL databases, our Redis Enterprise Cluster dominated in a real-world application scenario. The Avalon benchmark report is [freely available here](/cbc-2015-15-nosql-benchmark) and the results speak for themselves.

[Watch the video](/cbc-2015-15-nosql-benchmark)

But before we get into all the fun background on this particular test, let’s acknowledge a few things about benchmarks. There’s no way around it – performing meaningful comparisons between NoSQL solutions is a hard task. That is because of benchmarking’s “original sin” — results from any benchmark are truly relevant only to the specific application that was used for the test (see [Haber’s Benchmarking Theorem](https://gist.github.com/itamarhaber/2dad94e3bdd2980bce73)). This fact is compounded by the diverse capabilities of all the different NoSQL databases. Typical benchmark models tend to generalize a specific use case, and in the process they distance themselves from the underlying data management system and fail to leverage its strengths.

This by itself is hardly news and the past is riddled with attempts at [comparing apples to oranges](/blog/nosql-bar-datastax-aerospike-couchbase-redis-google-cloud-platform). I gave an entire presentation at RedisConf 20Fifteen on this subject ( [“Benchmarking Redis By Itself and Versus Other NoSQL Databases”](https://www.youtube.com/watch?v=aotCPUtahDU)). If you’ve watched it then you already know I believe that the only way to compare apples with oranges is through an applicative benchmark, in which the test application is optimized independently for each DBMS. That RedisConf talk, it turns out, was only the warm-up act for a session by Lahav Savir, CEO of Emind, who presented a real life benchmark using that exact approach ([“Real-Time Vote Platform Benchmark”](https://www.youtube.com/watch?v=aotCPUtahDU&t=20m02s)).

Emind’s use case is a great example of how Redis is put to use in tackling some of the hairier challenges that real-time analytics presents in the context of Big Data and the IoT. The story behind Emind’s benchmark brings together all my passions: data, people, technology and the cloud. It is a brilliant experiment designed to identify the best-performing NoSQL database for a real-time voting platform. The voting platform supports large events such as televised talent shows (think “American Idol” or “Rising Star”), where the audience is actively involved and directs the course of the show by voting. The volume and velocity of votes that must be tallied as they come in is staggering, so the platform’s performance must have superstar qualities (much like the shows’ participants) to support that kind of traffic.

Emind’s team identified several NoSQL technologies that could potential power their platform: Aerospike, Cassandra, Couchbase and Redis. While all candidates seemed promising, Emind needed to be sure that it chose the database that would best meet its requirements. To do that, Emind’s engineers built a [mock application](https://github.com/emind-systems/real_time_vote_benchmark) (“mockapp”) in Go that simulated the voting process and tailored it to use each of the different candidates.

Emind then solicited the services of Avalon Consulting, LLC to ensure the benchmark was executed optimally and impartially. Avalon reviewed and optimized the mockapp’s source code, approached each database vendor (Aerospike, Datastax, Couchbase and Redis) for guidance and certification of its respective solution’s deployment, executed the benchmark and compiled a [comprehensive report](/cbc-2015-15-nosql-benchmark) with the results. Check out the full write-up to find out more about how my favorite performer is a rocking superstar. Questions? Feedback? [Email](mailto:itamar@redis.com) or [tweet](https://twitter.com/itamarhaber) me – I’m highly available 🙂
