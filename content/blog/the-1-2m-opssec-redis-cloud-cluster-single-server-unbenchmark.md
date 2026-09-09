---
title: "The 1.2M Ops/Sec Redis Cloud Cluster Single Server Unbenchmark"
linkTitle: "The 1.2M Ops/Sec Redis Cloud Cluster Single Server Unbenchmark"
url: "/blog/the-1-2m-opssec-redis-cloud-cluster-single-server-unbenchmark/"
description: "While catching up with the world the other day, I read through the High Scalability guest post by Anshu and Rajkumar’s from Aerospike (great job btw). I really enjoyed the entire piece and was..."
date: 2014-09-04
blogCategories:
- "Tech"
authors:
- "Itamar Haber"
lastmod: 2025-03-27
hidden: true
---

*By Itamar Haber, Technology Evangelist · Published 4 September 2014 · updated 27 March 2025*

![Blog tile image](/images/site-mirror/0073e867b4e64f59de9047fdcde04295ba647e5c-772x550.webp)

![](/images/site-mirror/96eda390f3d1125f7f568efbef40a1d9c93ab6d3-635x200.webp)

While catching up with the world the other day, I read through the High Scalability guest post by[ Anshu and Rajkumar’s from Aerospike](https://highscalability.com/blog/2014/8/18/1-aerospike-server-x-1-amazon-ec2-instance-1-million-tps-for.html) (great job btw). I really enjoyed the entire piece and was impressed by the heavy tweaking that they did to their EC2 instance to get to the 1M mark, but I kept wondering – how would Redis do?

I could have done a full-blown benchmark. But doing a full-blown benchmark is a time- and resource-consuming ordeal. And that’s without taking into account the initial difficulties of comparing apples, oranges and other sorts of fruits. A real benchmark is a trap, for it is no more than an effort deemed from inception to be backlogged. But I wanted an answer, and I wanted it quick, so I was willing to make a few sacrifices to get it. That meant doing the next best thing – an unbenchmark.

An unbenchmark is, by (my very own) definition, nothing like a benchmark (hence the name). In it, you cut every corner and relax every assumption to get a quick ‘n dirty ballpark figure. Leaning heavily on the expertise of the guys in our labs, we measured the performance of our Redis Cloud software without any further optimizations. We ran our unbenchmark with the following setup:

- A sharded1 Redis Cloud in-memory NoSQL database server running on a single Amazon instance (see my notes on sharding and Redis Cloud clusters below).
- 3,000,000 objects, each of size 100 bytes.
- The [memtier_benchmark](https://github.com/RedisLabs/memtier_benchmark) tool client run on a non-server instance using the following command line arguments: `–ratio=1:1 -n 1000000 -d 100 -t 1 -c 50 –pipeline=75 –key-pattern=S:S`.
- A workload that mixes reads and writes in equal proportions (we have no particular bias towards one operation type over the other and feel this mix better reflects real life).
- An on-demand c3.8xlarge instance.

We didn’t have the time to set up a VPC and tune the placement groups for optimal performance, so we ran the entire thing in our standard service environment – i.e. on a noisy, crowded EC2 network. We also didn’t tune the CPU behavior or the number of threads or the shards’ configuration for this experiment – we let Redis Cloud use its defaults. We didn’t test multiple network configurations or add additional Elastic Network Interfaces (ENI). We simply took a freshly provisioned Redis Cloud server on HVM and did the unbenchmark against it…

You can find the raw output from our run [in this gist](https://gist.github.com/itamarhaber/9e7545258a7dddab0542), but the bottom line is that it scored a little over 1.2 million TPS (1228432 to be exact). Naturally, this amazing result really whetted my appetite and I immediately asked for a full-blown, all-optimizations-included, exhaustingly-exhaustive, fruit-and-vegetable-inclusive benchmark to really see how much we can push the limits with Redis! And guess what? It’s in the backlog 🙂

1 Some notes about sharding and Redis Cloud clusters (as promised):

By design, the Redis server is (mostly) a single-threaded process. That being the case, sharding is usually employed to scale a Redis database beyond the boundaries of a single CPU core or the RAM capacity of a single server. There are three generally-accepted approaches for implementing sharding: client-side, proxy or clustering. Since client-side and proxy-based solutions for sharding Redis are easier to implement independently of the actual underlying database engine, these (e.g., [Redis-rb](https://github.com/redis/redis-rb) and [nutcracker](https://github.com/twitter/twemproxy)) have been around for quite some time now. There are, however, only a few Redis cluster solutions today.

A sharded Redis cluster means a bunch of Redis servers (processes) deployed over one or more compute nodes across a network. The cluster runs Redis databases, each potentially spanning a number nodes and multiple cores, over an aggregated amount of RAM. A production-grade cluster should also meet challenges such as ensuring the database’s availability, as well as its performance and management of infrastructure and database resources.

The best known implementation of a Redis cluster is, naturally, that of the open source’s. [Redis cluster (v3)](https://github.com/antirez/redis/tree/3.0) is already in advanced stages of beta and it is expected to be production-ready within months. This upcoming version will provide excellent answers to many of the challenges I mentioned. Among its many new features, the new OSS version also includes the ability to [create](https://redis.io/topics/cluster-tutorial) [sharded](https://github.com/mattsta/redis-cluster-playground) [clusters](https://blog.marcgravell.com/2014/02/playing-with-redis-cluster-for-non.html). Speaking on behalf of the entire Redis community (my apologies if I have offended anyone by presuming :)), we expect Redis version 3 to be a major new version in every respect!

Besides the open source v3, there a few other Redis clusters already out there. Some folks went ahead and built their own clusters, each for her or his own reasons. I don’t want to namedrop anyone (like[Twitter](https://highscalability.com/blog/2013/7/8/the-architecture-twitter-uses-to-deal-with-150m-active-users.html), [Flickr](https://code.flickr.net/2014/07/31/redis-sentinel-at-flickr/) or [Pinterest](https://highscalability.com/blog/2013/4/15/scaling-pinterest-from-0-to-10s-of-billions-of-page-views-a.html)) but one company that has built a cluster is Redis. Our Redis Cloud service is powered by our own implementation of a Redis cluster and it has been in use in production for the better part of the last two years. During that period, we’ve been building and operating our clusters across multiple clouds and data regions. As a startup company, we’ve had to build our systems to scale both well and economically in order to accommodate the spectacular success that our commercial public service is having.

Redis is a contributor to the open source Redis project – most of our staff are amazing developers that live and breath Redis – but our users needed solutions that weren’t ready within the open source’s scope. In order to meet these business challenges, we’ve developed solutions that allow us to scale Redis databases on the fly from megabytes to terabytes. We deploy, scale and manage clusters over four different IaaS providers and across ~20 data centers. Our users have created tens of thousands of databases, and for each database we’ve maintained not only availability and performance, but also taken care of the operational and administrative tasks (all with a [tiny devops team](/blog/managing-50k-redis-databases-over-4-public-clouds-with-a-tiny-devops-team)).

To use our Redis Cloud clusters, just sign up to our service and create a database. You can set up a sharded database in seconds (although sharding isn’t included in our free tier). Redis Cloud instances can be sharded using the standard policy, i.e. per the [open source Redis Cluster Specification](https://redis.io/topics/cluster-spec), or with a powerful custom sharding policy that’s entirely configurable via a list of regular expression rules ([see the feature’s help page](/kb/redis-cloud-cluster) and future updates for more information).

As long as I’m on the subject, here’s one of the less-known facts about Redis’ clusters: you don’t have to change anything in your application to start using them. Yep, you can use your existing code and client library (whether cluster- and sharding-aware or not) and you’ll still get all the scalability, availability and operational benefits that the cluster offers. Our users need only create the database and configure its options (availability, data persistence, sharding, security and what not) and bazinga! They can just use the single Redis URL (hostname and port) that is the gateway to their database in a Redis Cluster. Sure, there are tweaks, best practices, optimizations, tips, tricks and a gazillion other things you could do on top, but (as shown in the unbenchmark), our cluster is a quite a performer even without them.

I had meant to keep these notes brief, but clustering is a rich and favorite topic of mine and I could go on and on for days (actually I promise that I will – more related announcements/technical/benchmarks/specs/comparisons to follow). To keep this a medium-sized post, I’d like to end here and invite you to follow [us](https://twitter.com/redis) and [shout](mailto:itamar@redis.com) at [me](https://twitter.com/itamarhaber) – I’m highly available 🙂

*This post was originally published at *[*HighScalability.com on August 27th, 2014*](https://highscalability.com/blog/2014/8/27/the-12m-opssec-redis-cloud-cluster-single-server-unbenchmark.html)[*.*](https://highscalability.com/blog/2014/8/27/the-12m-opssec-redis-cloud-cluster-single-server-unbenchmark.html)
