---
title: "AWS and Open Source: It’s Complicated"
linkTitle: "AWS and Open Source: It’s Complicated"
url: "/blog/aws-vs-open-source/"
description: "It’s that time of the year again. No, I’m not referring to the winter holidays, but to the reverberations of the announcements coming out of AWS re:Invent. Oftentimes when AWS makes a big move, IT..."
date: 2019-12-17
blogCategories:
- "Company"
authors:
- "Redis  "
lastmod: 2026-09-01
hidden: true
mirrored: true
---

*By Redis   · Published 17 December 2019 · updated 1 September 2026*

![Blog tile image](/images/site-mirror/78bca5b3928c071769472013b199b0e5a8af1bed-386x259.webp)

It’s that time of the year again. No, I’m not referring to the winter holidays, but to the reverberations of the announcements coming out of [AWS re:Invent](https://reinvent.awsevents.com/). Oftentimes when AWS makes a big move, IT ecosystems get shaken. In the database space, this year the effect focused on [Apache Cassandra](http://cassandra.apache.org/), after AWS announced a Cassandra-compatible serverless managed solution.

Along with the [announcement](https://aws.amazon.com/blogs/aws/new-amazon-managed-apache-cassandra-service-mcs/), AWS also released a [blog post](https://aws.amazon.com/blogs/opensource/contributing-cassandra-community/) explaining how its offering is going to help the Cassandra ecosystem by increasing the demand for Cassandra-like solutions and by allowing AWS to contribute back improvements to the open source community.

This is not the first time AWS has done something like this. Back in March, [AWS announced Open Distro](https://aws.amazon.com/blogs/aws/new-open-distro-for-elasticsearch/), a [hostile fork](http://meatballwiki.org/wiki/HostileFork) of [Elasticsearch](https://www.elastic.co/products/elasticsearch), and published a [similar blog post](https://aws.amazon.com/blogs/opensource/keeping-open-source-open-open-distro-for-elasticsearch/) where the company argued its actions were aimed at stopping [Elastic](https://www.elastic.co/) from tainting the open source project with proprietary extensions.

Now, with the Cassandra announcement, I’m getting a feeling of deja vu. I’m not here to address any business implications, but from the developer-community perspective, it seems that every time AWS announces a new database offering based on an open source project, it feels the need to restate how the company is a great OSS citizen—but the repeated effort just makes me feel more skeptical about the overall effect on open source projects in the cloud era. To be fair, at least in the case of Redis, AWS did contribute something back to the main project. The upcoming addition of SSL support to Redis 6 is the result of a collaboration between software engineers from both AWS and Redis (plus Alibaba, and more), as [antirez](https://twitter.com/antirez) himself tweeted:

> I just merged SSL support into Redis unstable. This feature has an interesting story that I want to tell you. It was kinda of a "process" to reach the right solution, or at least a solution that looks a lot better than the alternatives.
— antirez (@antirez) [October 16, 2019](https://twitter.com/antirez/status/1184496866618150912?ref_src=twsrc%5Etfw)

## Not so AWSome when it comes to OSS

While legions of AWS employees [storm Twitter](https://twitter.com/_msw_/status/1203019261502869504?s=20) to assure everybody they’re the good guys, other people in the community think differently. In particular, the people at [ScyllaDB](https://www.scylladb.com/) (a C++14 implementation of Cassandra) seem very concerned (learn more about the company’s take in this [blog post](https://www.scylladb.com/2019/12/04/managed-cassandra-on-aws-our-take/)). Long story short the AWS offering is based on [Amazon DynamoDB](https://aws.amazon.com/dynamodb/) and uses only some of the original Cassandra code as a form of translation layer to allow Cassandra clients to connect ***almost*** transparently.

“Almost transparently” because some original Cassandra features are not supported by this implementation. Quoting the Cassandra experts from ScyllaDB:

> Looking deeper, the functional differences are significant. There is no multi-region support, no UDT, no ALTER TABLE, no counters—all pretty fundamental for Cassandra users.

This is the inevitable result of offering a hybrid solution. In my opinion, it’s not OK because it’s likely to cause a split in the Cassandra community. I saw it happen with Redis. AWS offers a managed Redis solution called [ElastiCache](https://aws.amazon.com/elasticache/). As the name implies, it’s heavily geared towards caching workloads and it doesn’t include support for some key features that make Redis a viable persistent message broker or even a primary database.

The situation is complicated, and not as straightforward as it sounds. At AWS re:Invent, I lost count of the number of attendees who showed up at [the Redis booth](https://www.youtube.com/watch?v=CQ5tWMyzvU4) who didn’t know that in Redis [you can indeed tune persistence](https://redis.io/topics/persistence) to achieve durability guarantees comparable with any other operational or analytical database. Once they learned that, they would ask what else they could do with Redis, and we’d talk about the different data types, [Redis Streams](https://redis.io/docs/latest/develop/) (which are supported by ElastiCache, but become much more useful with strong persistence settings), and how [Redis modules](/redis-enterprise/modules/) let you add new data types to Redis, such as [full-text search indexes](https://redisearch.io). We’d also cover the [many additional modules](https://redis.io/modules) written by the Redis open source community (including [redis-cell](https://github.com/brandur/redis-cell), [redis-cuckoofilter](https://github.com/kristoff-it/redis-cuckoofilter), and [cthulhu](https://github.com/sklivvz/cthulhu)).

As you might have guessed, ElastiCache doesn’t support any modules, even those from the community:

![](/images/site-mirror/6ba7234be0d388f6d13c9983aa98913a11151db5-974x616.webp)

The prevalence of ElastiCache has created a split in the community of Redis users. The people who experience Redis only via AWS are seeing an incomplete vision of the open source project’s direction and benefits. I feel the broader community would benefit if they knew that, Yes, Redis is a great caching solution, but you can do so much more with it.

## How AWS affects the open source community

We’ve now seen AWS fork and carve out features from several open source databases. In addition to Cassandra and Elasticsearch, AWS also has a MongoDB-compatible offering that [is also not feature complete](https://docs.aws.amazon.com/documentdb/latest/developerguide/mongo-apis.html). Feature disparity might seem a minor technical detail, but as a Developer Advocate for Redis I can see the impact it can have on the community. In the case of Redis, the feature disparity effectively relegates [the most loved database by developers worldwide](/blog/redis-named-loved-database-third-consecutive-year/) to being primarily a caching front-end for the databases that AWS wants its customers to use.

When it comes to open source, the real question is not whether or not AWS will contribute code back, but rather what will be the overall impact of its actions on the open source community. Frankly, all these blog posts, tweets, and metal pins just look like red herrings to me.
