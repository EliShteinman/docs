---
title: "Announcing Redis Enterprise Release with RedisGraph, Streams (Redis 5.0) and Popular Redis Java and Python Clients"
linkTitle: "Announcing Redis Enterprise Release with RedisGraph, Streams (Redis 5.0) and Popular Redis Java and Python Clients"
url: "/blog/announcing-redis-enterprise-release-redisgraph-streams-redis-5-0-popular-redis-java-python-clients/"
description: "As we gear up for 2019, we are very excited to announce the latest release of Redis Enterprise which marks a significant milestone in our journey towards a zero latency future, and comes packed..."
date: 2018-11-16
blogCategories:
- "Announcements"
- "New Product Announcements"
authors:
- "Madhukar Kumar"
lastmod: 2025-03-27
hidden: true
---

*By Madhukar Kumar, VP of Technical and Product Marketing · Published 16 November 2018 · updated 27 March 2025*

![Blog tile image](/images/blog/0073e867b4e64f59de9047fdcde04295ba647e5c-772x550.webp)

As we gear up for 2019, we are very excited to announce the latest release of Redis Enterprise which marks a significant milestone in our journey towards a zero latency future, and comes packed with all sorts of goodies. Let’s review three capabilities that make the new Redis Enterprise especially interesting.

### RedisGraph

[RedisGraph](https://oss.redis.com/redisgraph/) is a Redis module that represents connected data as [adjacency matrices](https://en.wikipedia.org/wiki/Adjacency_matrix) instead of the more common [adjacency lists](https://en.wikipedia.org/wiki/Adjacency_list) per data point representation. By using sparse matrices and employing the power of [GraphBLAS](http://graphblas.org/) (a highly optimized library for sparse matrix operations), RedisGraph delivers a fast and efficient way to store, manage and process graphs — we’re talking up to 600 times faster than other graph databases. RedisGraph is now part of a brand new Redis Enterprise module available for our [VPC](/redis-enterprise/vpc/) and [software](/redis-enterprise/software/) customers, and can also be used under our source available license. You can read about the benchmarks on our blog [here](/blog/new-redisgraph-1-0-achieves-600x-faster-performance-graph-databases/) and get more details about RedisGraph [here](/redis-enterprise/redis-modules/redis-enterprise-modules/redisgraph/).

## Streams

Streams is a new data structure that was [introduced with open source Redis 5.0](/blog/redis-5-0-is-here/) and is now available in the latest version of Redis Enterprise. Similar to the Lists data type, Streams has an ordered collection of elements called messages. Unlike Lists, however, messages are added exclusively to the end of Streams. In Streams, messages are stored using unique sub-second timestamp-based identifiers, and the order of the messages is immutable. With blocking read functionality, Stream provides a pub/sub like functionality but with fan out scaling ability. Streams has many interesting real-world uses like log aggregation, real-time sentiment analysis and more. We cannot wait to see how the community will put it to use to process data generated at incredible velocities. You can read more about Streams [here](/blog/redis-5-0-is-here/).

### Jedis and Redis-py

As part of the current Redis Enterprise release, we are also incredibly proud to collaborate with the creators of the two most popular Redis clients — [Jonathan Leibiusky](https://twitter.com/@xetorthio), the creator of [Jedis](https://github.com/xetorthio/jedis), and [Andy McCurdy, t](https://twitter.com/andymccurdy)he creator of [Redis-py.](https://github.com/andymccurdy/redis-py) We will continue to contribute to these projects as part of our commitment to the Redis community. We plan to ensure that all new features released as part of Redis will be supported in these clients, including Streams and modules. We believe it is important to make sure that these highly popular libraries will be constantly maintained and up to date with the latest capabilities of Redis.
