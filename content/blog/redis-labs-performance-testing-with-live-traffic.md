---
title: "Redis Labs Performance Testing With Live Traffic"
linkTitle: "Redis Labs Performance Testing With Live Traffic"
url: "/blog/redis-labs-performance-testing-with-live-traffic/"
description: "Originally published on bleacherreport.com"
date: 2014-07-16
blogCategories:
- "Company"
authors:
- "Tung Nguyen"
lastmod: 2025-03-27
hidden: true
---

*By Tung Nguyen · Published 16 July 2014 · updated 27 March 2025*

![Blog tile image](/images/blog/1da8c657f4d74067d8a342793a90b4143ac98cd6-800x320.webp)

Originally published on [bleacherreport.com](https://bleacherreport.com)

### Intro

Our API service uses Redis as it’s caching layer. The Redis set operations are extremely useful for the logic required in our API service. Unfortunately, we have had some issues scaling Redis. Redis is a single-threaded server that reads incoming connections using an event-based paradigm, thus uses only 1 CPU core. So you can scale Redis vertically but it is very challenging to scale Redis horizontally. We see this when our app calls heavier zset and zunionstore operations. Redis hits the CPU limit and it gets pegged at 100%.

We’ve also seen issues with the way Redis snapshots the data in memory to disk. Redis forks off another process to save the data and that process doubles the RAM footprint of the Redis. Once Redis runs out of memory on the box it gets painfully slow. This effectively reduces the memory you can use on the box to half of the total actually available. In our case we use Redis as a cache, so we’ve simply disabled saves so we could use all the memory on the box and we’ve been veritically scaling. However, vertically scaling will only get you so far. Our current bottleneck is that we’re approaching the upper bound of available CPU.

### Redis

We wanted try out Redis clustering, but the open source version is a still work in progress. [Redis](/), one of the top contributers to the open source Redis project, already has clustering working on their platform. [Redis](/) is engineered to scale up automatically and seamlessly. The Redis db will grow in capacity on a single shard and, when it needs to, automatically start to cluster across multiple shards. All of this happens behind the scenes transparently. Customers need only manage a simple single endpoint.

### Performance Testing

Beyond basic sanity tests and functional testing, we required quantitative measures and performance metrics to legitimize our move.

We used [em-proxy](https://github.com/igrigorik/em-proxy) to blue-green traffic in migrating our servers to a new cluster. This allows us to proxy a portion of traffic to [Redis](/), testing it, and reacting to changes with contained exposure.

After a few google searches that night, I ran into [it](https://www.codinginthecrease.com/news_article/show/153460), and then I did some testing that same night with a single instance. Then on the following night, I created an additional test cluster, which took about [5 minutes](https://gist.github.com/tongueroo/cd6a002771cde7db92a9), and then directed **ALL** of traffic from live production cluster to the test cluster and let it run through the night and following day. The powerful thing about this technique is that we are not guessing with input benchmark data, instead we’re actually using live production traffic. On top of that, we can compare the [New Relic](https://newrelic.com/) data sets against each other in real time.

The results were incredible.

The left graph is based on Redis servers that we maintain in-house. On the right is the test cluster connected to [Redis](/). The only difference between the clusters is that one uses open source Redis server and the other one uses [Redis](/). With the standard open source Redis server we see intermittent spikes in the response times up to 700ms and averaged 435ms; it’s all over the place. [Redis](/) brings our response times to a consistent and smooth average of 55ms! Whatever voodoo blackmagic Redis is conjuring up, it’s obviously working.

### Finding Issues Before Production

During our testing we found that [Redis](/) disables some Redis commands, thus were required to make some changes to our API code.

For instance, [Redis](/) disables the object command.

The next error is due to the fact that [Redis](/) was sharding, yet our app was not equipped to handle it.

To resolve this issue you need to name Redis keys such that Redis can manage the data shards. Keys need to be named with curly braces like so hello{dynamic}world. So the following keys map to separate shards:

- hello{123}world
- hello{456}world
- hello{789}world

It is explained in more detailed here: [/kb/redis-cloud-cluster](/kb/redis-cloud-cluster). We ended up deploying to a single shard, which is apples-to-apples with our prior environment, and will circle back to sharding at a later time.

This method of testing is extremely powerful. We found a lot of issues that we were able to fix **before** we actually rolled out [Redis](/) on production. Had we instead moved all traffic to [Redis](/), we would have been in a fire fighting situation and probably would have rolled back, not realizing the dramatic performance opportunities [Redis](/) offers.

### Conclusions

[Redis](/) is fast! If you’ve read closely, you’ve probably realized the kicker. We’re getting this performance increase from [Redis](/) without even sharding. We still have more follow up work to do, including sharding, which should improve our performance even more dramatically. If you are using Redis and are having issues scaling it beyond a single CPU or are getting memory bounded, [Redis](/) is a great option.
