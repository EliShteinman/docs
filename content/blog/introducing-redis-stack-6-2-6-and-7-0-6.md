---
title: "New Redis Stack Is Stuffed With Dozens of New Features"
linkTitle: "New Redis Stack Is Stuffed With Dozens of New Features"
url: "/blog/introducing-redis-stack-6-2-6-and-7-0-6/"
description: "Whether you are a long-time Redis developer or you are just getting started, Redis Stack represents the latest innovations we have to offer."
date: 2022-12-07
blogCategories:
- "New Product Announcements"
- "Tech"
authors:
- "Pieter Cailliau"
lastmod: 2025-03-27
hidden: true
---

*By Pieter Cailliau, Product Manager · Published 7 December 2022 · updated 27 March 2025*

![Blog tile image](/images/site-mirror/c21e544cd8c0a82599602320467a0f6c9e7379b9-772x550.webp)

**Whether you are a long-time Redis developer or you are just getting started, Redis Stack represents the latest innovations we have to offer.**

Today Redis is happy to announce the availability of the latest version of [Redis Stack](/blog/introducing-redis-stack/).

Redis Stack extends Redis Open Source (OSS) with data processing engines (such as query and search) and modern data models (such as document JSON, time series, and graph). The combination empowers developers to build real-time applications that are joyful to develop as well as easy to maintain and support.

This latest edition of Redis Stack provides a number of compelling features that developers have asked for. Here are the highlights:

- **Real-time query and search**: Multi-value support for indexing and querying a list of values within a nested JSON document. We added support for suffix and infix wildcard searches. Plus, the query and search capabilities with JSON can now be deployed in an [Active-Active geo-distributed](https://docs.redis.com/latest/rs/databases/active-active/) manner with Redis Enterprise with local read and write latencieswhen[ manipulating nested data](https://docs.redis.com/latest/modules/redisjson/active-active/).
- ***t*****-digest**: A new probabilistic data structure to estimate quantiles in streaming data.
- **Graph**: New tweakable path-finding algorithms and language constructs let you more easily manipulate labels on nodes and better support resource management use cases. Plus, more than 20 new functions address type conversion, trigonometric, and logarithmic functions.
- **Time series**: Enhanced compaction and aggregation functionality significantly reduces the client-side logic required to query time series data.
- **Developer tools**: [RedisInsight](/insight/) is updated with new diagnostic tools, including memory usage, data distribution, slow log analysis, and support for encoded data (such as protobuff, php unserialize, and Java serialized objects), all of which speed up development cycles.

All of these Redis Stack capabilities are also available on Redis Enterprise Cloud and Redis Enterprise Software.

Need more information? Here’s some additional details about the enhancements.

## Real-time query and search

Redis Stack allows you to [index, query, and perform full-text searches](https://redis.io/docs/stack/search/) on data residing in Redis hashes or in nested [JSON](https://redis.io/docs/stack/json/) documents. This latest release adds several frequently requested improvements that let developers use infix and suffix wildcards in search queries, such as `*vatore` and `ant?rez`.

Developers can create multi-value indexing and query attributes irrespective of type ([TEXT](https://redis.io/docs/stack/search/indexing_json/#index-json-arrays-as-text), [TAG](https://redis.io/docs/stack/search/indexing_json/#index-json-arrays-as-tag), [NUMERIC](https://redis.io/docs/stack/search/indexing_json/#index-json-arrays-as-numeric), [GEO](https://redis.io/docs/stack/search/indexing_json/#index-json-arrays-as-geo), and [VECTOR](https://redis.io/docs/stack/search/indexing_json/#index-json-arrays-as-vector)), defined by a [JSONPath](https://redis.io/docs/stack/json/path/) leading to an array or to multiple scalar values. Previously, you could only index scalar attributes.

For example, imagine the following document representing a bicycle:

```python
{ 
    …
    "color": "silver",
    …
    "components": [
       { "name": "seatpost", "color": "blue" },
       …
   ]
}

```

Now, with a single JSONPath `$..color`, you can index all color fields in the document, irrespective of their location in the document. (See the [RedisSearch release notes](https://github.com/RediSearch/RediSearch/releases/tag/v2.6.3).)

We also updated the JSONPath parser with improved performance and bug fixes.

## t-digest

Redis Stack contains a set of useful [probabilistic data structures](https://redis.io/docs/stack/bloom/). Probabilistic data structures allow developers to control the accuracy of returned results whilst gaining performance and reducing memory. These data structures are ideal for analyzing streaming data and large datasets.

Within this latest release, Redis Stack now includes a new probabilistic data structure, [t-digest](https://www.sciencedirect.com/science/article/pii/S2665963820300403), for estimating quantiles based on a data stream or a large dataset of floating-point values. You can use it to answer questions such as:

- What fraction of the values in the data stream are smaller than a given value?
- Which value is smaller than *p* percent of the values in the data stream? (That is, what is the *p*-percentile value?)
- What is the mean value between the *p1*-percentile value and the *p2*-percentile value?
- What is the value of the *n*-th smallest / largest value in the data stream? (What is the value with [reverse] rank *n*)?
- What is [the airspeed of an unladen swallow](https://interestingengineering.com/science/monty-python-and-the-holy-grail-airspeed-velocity-of-an-unladen-swallow)? Okay, maybe not that one.

## Graph and time series

Redis Stack also has dedicated data structures for [time series](https://redis.io/docs/stack/timeseries/) data and highly connected data ([graph](https://redis.io/docs/stack/graph/)), each with its own powerful query engine.

Many users are using our graph capabilities for resource, identity, and access management use cases. Modeling your data as a graph can help you ensure that the right entities have the right access to the right resources at the right time, where both entities and resources can be members of hierarchical groups.

This latest Redis Stack release enhances that experience further. We added new path algorithms for finding minimal-weight, optionally bounded by cost or length paths between a given pair of nodes or starting at a given node. We also added language constructs for adding and removing node labels, changing node properties and edge properties, and deleting paths. We have 29 new functions covering type conversion, trigonometric, and logarithmic functions. Lastly, all write queries are now executed atomically. ([*Atomicity*](https://en.wikipedia.org/wiki/ACID#Atomicity) is the guarantee that each query either succeeds or fails with no side effects. Whenever a failure occurs, the query effect is rolled back from an undo log.) (See the [graph release notes](https://github.com/RedisGraph/RedisGraph/releases/tag/v2.10.4) for more details.)

In terms of the advancement of our [time series](https://redis.io/docs/stack/timeseries/) capabilities, we added the ability to retrieve aggregation results for the latest (still open) bucket of compactions. We introduced a new aggregator: time-weighted average, for estimating more accurately average-over-time when samples of a continuous signal are available at non-constant intervals. A new gap-filling capability allows interpolating or repeating the last value for empty buckets. In addition, you can now control how bucket timestamps are reported (the bucket’s start time, mid-time, or end-time) as well as controls for alignment for compaction rules. A set of new reducers is introduced as well. (See the [time series release notes](https://github.com/RedisTimeSeries/RedisTimeSeries/releases/tag/v1.8.3).)

## Developer tools

[RedisInsight](/insight/) is the ideal developer companion for Redis and Redis Stack. It allows you to visualize and optimize Redis data. RedisInsight also helps you learn about our latest innovations as they are introduced, using guided tutorials.

The [latest RedisInsight](https://github.com/RedisInsight/RedisInsight/releases/tag/2.14.0) enhances diagnostic capabilities. A database analysis feature helps you optimize performance and memory usage. It shows data type distribution, memory allocation, and top keys and namespaces, sorted by consumed memory or key length and count of keys, respectively. The new slow log tool makes it easier to troubleshoot performance issues. You can also validate your data with the help of newly added formatters (JSON, HEX, MessagePack, ASCII, and so on).

## ​​Getting started with Redis Stack

The latest release of Redis Stack is available in two versions: Redis Stack [6.2.6](https://github.com/redis-stack/redis-stack/releases/tag/v6.2.6-v0), built on top of Redis 6.2; and Redis Stack [7.0.6](https://github.com/redis-stack/redis-stack/releases/tag/v7.0.6-rc2), a release candidate, built on top of Redis 7.0.

You can choose one of the following ways to install and get started with Redis Stack:

- Download Redis Stack from [redis.io](https://redis.io/download)
- Use your [favorite package manager](https://redis.io/docs/stack/get-started/) or launch the [Redis Stack docker image](https://redis.io/docs/stack/get-started/install/docker/)
- Create [a free database on Redis Enterprise Cloud](/try-free/), which contains all the latest features of Redis Stack

The new Redis Stack features are also available today on Redis Enterprise Cloud and Redis Enterprise Software.

Once you have Redis Stack Server up and running, you can instantly leverage RedisInsight to visualize, analyze, and optimize your Redis data.

Choose the client library in [the language of your choice](https://redis.io/docs/stack/get-started/clients/), and consult our [tutorials](https://redis.io/docs/stack/get-started/tutorials/) for .NET, Node.js, Python, and Spring to get started coding. For a deep dive into the query and search capabilities of Redis Stack, enroll in our free course, [RU204: Storing, Indexing, and Querying JSON at Speed](https://university.redis.com/courses/ru204/).

## What’s next for Redis Stack?

In the next Redis Stack release, we plan to introduce additional mechanisms for triggered functions. Specifically, we plan to include an embedded JavaScript engine. Functions written in JavaScript can be triggered by an event arriving in a stream, synchronously with a Create/Update/Delete operation, or can be scheduled at a given time. This will allow you to execute business logic within the database in combination with Redis Stack capabilities such as query and search. By manipulating data server-side, triggered functions can significantly lower the latency of updates and reduce stale data.

The next Redis Stack release is planned for Spring 2023, but you can preview its programmability capabilities now. In our [Expanding the Database Trigger Features in Redis](/blog/database-trigger-features/) [blog post](/blog/database-trigger-features/), we show how to write functions that react to data changes in Redis.

Note: To offer the Redis community more freedom and clarity, Redis Stack is now provided under [a new dual license](/blog/rsalv2-sspl-announcement/): a new version of our Redis Source Available License ([RSALv2](/legal/rsalv2-agreement/)) and the Server Side Public License ([SSPLv1](https://www.mongodb.com/licensing/server-side-public-license)).
