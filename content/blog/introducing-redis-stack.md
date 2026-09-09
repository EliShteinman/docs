---
title: "Hello, Redis Stack"
linkTitle: "Hello, Redis Stack"
url: "/blog/introducing-redis-stack/"
description: "Today we’re thrilled to announce Redis Stack. Redis Stack consolidates the capabilities of the leading Redis modules into a single product, making it easy for developers to build modern, real-time..."
date: 2022-03-23
blogCategories:
- "Company"
- "News"
- "Product Releases"
authors:
- "Redis  "
lastmod: 2026-09-01
hidden: true
---

*By Redis   · Published 23 March 2022 · updated 1 September 2026*

![Blog tile image](/images/blog/35b9ca6682093dbbd624172f666c7ef5fab6de53-772x550.webp)

Today we’re thrilled to announce Redis Stack. Redis Stack consolidates the capabilities of the leading Redis modules into a single product, making it easy for developers to [build modern, real-time applications](/try-free/) with the speed and stability of Redis.

## Prologue

At Redis, we’re building a real-time data layer to meet the universal demand for responsive, low-latency applications and services.

To build applications that provide real-time experiences, you need a database that can process any request, whether a simple object retrieval, a search, or a complex aggregation, with the fastest possible response times, preferably in less than a millisecond. The rationale is simple: in a typical application, every user interaction generates multiple calls to the database, which can result in significant overhead; if you add to that the round trip latency of the network between the end-user and the app, every extra millisecond spent in the database makes it more difficult to deliver a real-time end-user experience.

This holds no matter the data model, be it a key/value, document, stream, graph, time series, or probabilistic data structures.

## What have we done so far?

As the trend of the last 24 months at [DB-Engines](https://db-engines.com/) makes clear, the fastest-growing data models are key-value, search, document, graph, and time series. This trend also shows that fewer and fewer developers are choosing to model their applications with relational databases.

![](/images/blog/8d3fa55aa267596e25503c627bd91288bc388fbd-1024x484.webp)

As it turns out, we’ve spent the past four years building several dedicated data engines that extend the core key/value data-structure functionality of Redis with modern data models and data processing capabilities, such as search, document, graph, time series, and probabilistic data structures.

Implemented as Redis modules, we’ve built these engines from the ground up using the same design principles as open source Redis, with an in-memory architecture and an efficient codebase written in C or Rust, allowing developers to run a wide variety of data workloads with the lowest latency possible.

After listening to our community and customers, we realized that we needed to simplify the developer experience of the leading Redis modules and the capabilities they provide, along with their documentation and clients that support their functionality. We wanted to help developers be fully productive from the moment they started using Redis.

This is why we created Redis Stack.

## Redis Stack

Redis Stack unifies the leading Redis modules in a single product. This makes it easy to start building with our Redis-based search, document, graph, and time series capabilities.

Redis Stack is a suite of three components:

1. **Redis Stack Server** combines open source Redis with [RediSearch](http://redisearch.io), [RedisJSON](http://redisjson.io), [RedisGraph](http://redisgraph.io), [RedisTimeSeries](http://redistimeseries.io) and [RedisBloom](http://redisbloom.io)

1. **RedisInsight** is a powerful tool for visualizing and optimizing Redis data, making real-time application development easier and more fun than ever before

1. The **Redis Stack Client SDK** includes the leading official Redis clients in Java, JavaScript, and Python. These clients also include our new suite of object mapping libraries which offer developer-friendly abstractions that get you productive with just a few lines of code. Known as Redis OM for [.NET](https://github.com/redis/redis-om-dotnet), [Node.js](https://github.com/redis/redis-om-node), [Java](https://github.com/redis/redis-om-spring), and [Python](https://github.com/redis/redis-om-python), these libraries also make it easier than ever to integrate with major application frameworks such as Spring, ASP.NET Core, FastAPI, and Express.

![three redis stack icons](/images/blog/0c87796e72276c01f7f74d3901dc38b3aa6838c7-1024x432.webp)

## Getting started with Redis Stack

Redis Stack is now generally available for Redis 6.2, and we also have a release candidate for Redis 7.0.

We’re providing several ways to quickly get started with Redis Stack:

- Download Redis Stack directly from [redis.io](https://redis.io/download)
- Install using your [favorite package manager](https://redis.io/docs/stack/get-started/) or by simply launching the [Redis Stack docker image](https://redis.io/docs/stack/get-started/install/docker/)
- Deploy Redis Stack in the cloud by creating [a free database on Redis Enterprise Cloud](/try-free/) or by using one of our Fixed plans. We’re also providing Redis Stack’s capabilities in Redis Enterprise Software for anyone self-managing or deploying on-premises.

Once you have Redis Stack Server up and running, you can immediately leverage [RedisInsight](/insight/) to visualize, analyze and optimize your Redis data. RedisInsight includes a series of guides that walk you through several Redis Stack use cases.

On the client side, we’re supporting Redis Stack in several leading Redis clients — [Jedis](https://github.com/redis/jedis) (Java), [redis-py](https://github.com/redis/redis-py) (Python), and [node-redis](https://github.com/redis/node-redis) (JavaScript) — and with our new object mapping libraries ([redis-om-spring](https://github.com/redis/redis-om-spring), [redis-om-python](https://github.com/redis/redis-om-python), [redis-om-node](https://github.com/redis/redis-om-node), [redis-om-dotnet](https://github.com/redis/redis-om-dotnet)).
You can clone [an example repository for each language](https://redis.io/docs/stack/get-started/tutorials/) we support to start developing your freshly created database.

## Redis & Redis Stack

We’re excited about the universe of real-time applications that we believe Redis Stack will make possible. But we’d like to be very clear that Redis Stack is not a replacement for Redis.

Redis is a core, open source technology, and our focus on its continued development is not changing. You’ll always have the option to download, build, install, and run open source Redis.

When you’re ready to run Redis Stack, you can [easily migrate your data](/redis-enterprise-cloud/migrate/) using the Redis replication mechanism or by loading your RDB or AOF files.

![redis stack illustration](/images/blog/85ba0002eabf67d0b79061aa61748a14e3ccc66e-1024x323.webp)

## Licensing

All the codebase components of Redis Stack are open and free for everyone to use, but we still want to be very clear about the Redis Stack licensing model since we updated our licenses as mentioned in [this blog](/blog/rsalv2-sspl-announcement/):

- Redis Stack Server is provided under the [Redis Source Available License 2.0 (RSALv2)](/legal/licenses/) (the same license we’ve used with our Redis modules)
- We’re providing RedisInsight under its existing [Server Side Public License (SSPL)](https://en.wikipedia.org/wiki/Server_Side_Public_License)
- The leading Redis clients and our object mapping libraries have been released under an open source [MIT license](https://opensource.org/licenses/MIT)

![redis stack licensing icons](/images/blog/8a8b98f816600c2228313f9a8e96b6aa82bfc603-1024x435.webp)

## In summary

We’re committed to continuing to develop Redis as an open-source project, supporting one of the largest developer communities on earth, and cooperating with our growing number of active contributors to the project.

We will continue adding capabilities to Redis Stack, to allow developers to quickly and easily develop modern applications for the real-time era that are entirely based on Redis.

To learn more about Redis Stack and the capabilities it provides, tune into deep-dive sessions on Redis Stack delivered at our [RedisDays event](/redisdays/) available now on-demand.

We’ve also put together quick answers to anticipated questions – on the short FAQ section.
Finally, we’d love to get your feedback on Redis Stack. Send us a note on the [Redis mailing list](https://groups.google.com/g/redis-db?pli=1) or join the [Redis Discord server ](https://discord.com/invite/redis)to let us know what you think.

## FAQ

### What are the components of Redis Stack?

Redis Stack is a single package that includes open source Redis with the leading Redis modules (Redis Stack Server), and RedisInsight.

For the initial release of Redis Stack Server, we’re including five modules: RedisJSON, RedisSearch, RedisGraph, RedisTimeSeries, and RedisBloom.

Redis Stack is supported by official Redis client and object mapping libraries and allows developers to easily use the advanced Redis Stack capabilities with several application frameworks, including Spring, ASP.Net Core, Express, and FastAPI.

### What capabilities does Redis Stack provide for developers?

Redis Stack lets developers:

- Index and query Redis data, run aggregations, perform a full-text search
- Run advanced [vector similarity searches](https://redis.io/solutions/vector-database/) (KNN)
- Store and manipulate nested JSON documents efficiently
- Build and model relations as property graphs
- Store, query, and aggregate time-series data
- Take advantage of fast, space and compute efficient probabilistic data structures
- Easily visualize, debug, and analyze Redis data using RedisInsight

### Will you be adding more capabilities to Redis Stack?

We’ll consider adding new capabilities or even modules to Redis Stack if:

1. We see the demand from our community
1. The new capabilities comply with the Redis vision
1. The Redis Inc. engineering team can officially support the addition

### Why is RedisGears not part of the first Redis Stack release?

RedisGears adds database triggers, stream processing, distributed functions, and full programmability to Redis.

We will add RedisGears to Redis Stack once the support for JavaScript is GA, later this year.

### Can I self-manage Redis Stack for free?

Yes, you can!

### What are the Redis object-mapping libraries?

The Redis object-mapping libraries provide a level of abstraction above the Redis command API, much like an ORM does for a SQL database. Let’s distinguish the core Redis client libraries from Redis object mapping libraries.

#### Core Redis client libraries have the following responsibilities:

- Implement the Redis protocol (RESP, etc.).
- Manage connections (TCP, etc.), reconnect, server discovery, etc.
- Manage execution logic (threads, async io, etc.)
- Expose an API for executing arbitrary Redis commands
- Expose Redis commands in a language-idiomatic fashion
- Connect to any Redis deployment via connection string

#### Object-mapping libraries provide additional leverage:

- Allow developers to implement common Redis use cases in the fewest lines of code possible. Right now, this includes domain modeling and fluent query APIs. In the future, we’ll add support for other common Redis use cases including caching, session storage, rate limiting, [leaderboards](/solutions/leaderboards/), and de-duplicators.
- Expose a high-level API for the capabilities provided by the Redis Stack
- Provide the benefits of Redis without exposing the underlying Redis commands
- Integrate with major application frameworks (e.g., Spring, ASP.NET Core, FastAPI, Express)

These object-mapping libraries always depend on one or more core Redis libraries.

### Is there a .NET client available for Redis Stack?

Currently, the recommended client for .NET developers is [StackExchange](https://stackexchange.github.io/StackExchange.Redis/), which is not formally supported by Redis, Inc. You can extend the client with [NRediSearch](https://libraries.io/nuget/NRediSearch) for RediSearch, [NRedisGraph](https://github.com/tombatron/NRedisGraph) for RedisGraph, and [NRedisTimeSeries](https://github.com/RedisTimeSeries/NRedisTimeSeries/) for RedisTimeSeries. You can also use the [redis-om-dotnet](https://github.com/redis/redis-om-dotnet) library that builds on top of StackExchange.

### Can I work with RedisInsight on Redis Enterprise Cloud?

[RedisInsight](/insight/) is not yet available on Redis Enterprise Cloud. However, you can connect with the RedisInsight application to your cloud database. We plan to add RedisInsight to the cloud later this year.

### Can I migrate my Redis Stack database easily to Redis Enterprise Cloud?

Yes, you can leverage our [Replica-Of](https://docs.redis.com/latest/rs/administering/designing-production/active-passive/) solution to migrate your database to our fully managed cloud service without any downtime.

---
