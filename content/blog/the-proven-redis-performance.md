---
title: "The Proven Redis Performance"
linkTitle: "The Proven Redis Performance"
url: "/blog/the-proven-redis-performance/"
description: "Recently, a known NoSQL vendor announced the addition of in-memory capabilities to its database offering. The decision to take a hybrid approach with their database offering brings up a few serious..."
date: 2014-04-08
blogCategories:
- "Tech"
authors:
- "Redis  "
lastmod: 2025-03-04
hidden: true
mirrored: true
---

*By Redis   · Published 8 April 2014 · updated 4 March 2025*

![Blog tile image](/images/site-mirror/0073e867b4e64f59de9047fdcde04295ba647e5c-772x550.webp)

![](/images/site-mirror/973b1f79d5668280d37a9379c8dcda9f596db7b6-360x166.webp)

Recently, a known NoSQL vendor announced the addition of in-memory capabilities to its database offering. The decision to take a hybrid approach with their database offering brings up a few serious concerns. Redis, the in-memory, open-source, key-value store, has provided many insights into the world of modern applications. One particularly eye-catching observation is the inherent need for databases with in-memory capabilities. As a result, NoSQL vendors across the board have been working diligently to harness the benefits of both on-disk and in-memory databases.

At Redis, we believe this hybrid approach is wrong. Our concern stems from the fact that vendors using this approach cannot succeed in providing the advantages that databases such as Redis, with solely in-memory capabilities, have introduced to modern applications. In his [recent post](http://antirez.com/news/73), Salvatore Sanfilippo listed three important factors of database performance including latency, operation speed, and operation quality. The following real-life scenarios exemplify these three factors based on the experience we have gained from supporting tens of thousands of modern applications.

Before diving into each of these performance components, I would like to share the results of an in-house research study we did to compare the performance of a number of popular SQL and NoSQL databases. As seen below, there is no doubt that in-memory databases perform significantly better.

![](/images/site-mirror/ee2cb82a937206d6dbb3f76e4b26cc174ba4fcee-739x317.webp)

NoSQL and SQL Response Performance Comparison

### Three Principal Criteria

All in-memory systems can be measured by three main criteria: latency, throughput and efficiency. Similar to Sanfilippo’s three important factors of database performance, excelling at these criteria enables in-memory databases, such as Redis, to perform significantly better than their on-disk rivals. Because of this, in-memory databases have become critical for modern, scalable applications and real time processing.

1 – Latency: Modern applications require a latency of around 100 msec from the time a request reaches an application until it is processed and the application generates a response and returns it back to the user. In order to achieve this, the database level must perform at a consistent sub-millisecond latency, which is solely accomplished by an in-memory database that retrieves all data directly from RAM.

2 – Throughput: Nowadays, applications’ performance needs to scale instantly. Take a Twitter account with 1 million followers for example. A single tweet intended to reach 1 million people instantaneously generates 1 million simultaneous writes and requires immediate scaling. These types of events occur constantly without any prior warning, creating significant challenges for the system.

Scenarios such as this require infrastructure that can instantly scale out. Auto-scale will not do the job, as provisioning additional nodes to an existing cluster can take several minutes. And building an entire NoSQL infrastructure just to serve requests during peak times is very expensive. Accordingly, a growing number of developers are designing real-time apps entirely from scratch with Redis.

3 – Efficiency: While an in-memory database may be extremely fast, its performance will continue to be poor if it is constantly transferring large amounts of raw data between the database and an application. Redundant processing of raw data not only wastes resources, it increases latency. In addition, this raw data transfer can potentially block the entire network infrastructure, requiring node additions in order to maintain network speed.

Using Redis’ unique data types and commands, it is possible to build a schema in such a way that the database is tuned to serve application requests without any additional processing at the application level. This intelligent design significantly reduces the amount of transferred data.

![](/images/site-mirror/b4630d39649f0010f945487c0370eaefebc9f98b-383x230.webp)

The figure to the right illustrates an actual scenario from one of our customers. Without Redis, they would’ve needed to build a 150+ node cluster to support a network speed of 120 Gbps. In addition, they would’ve required increased work at the application level. Redis works using a six, in-memory, node cluster, 1.5 Gbps, and no extra work at the application level.

### Choosing the Appropriate Database

Attempting to fix problems that Redis has already solved by adding in-memory capabilities to an incompatible database is destined to fail.

At Redis, we believe in a best-of-breed approach. There is no reason to settle for just one type of database, whether it be in-memory or disk based. Modern, scalable applications ought to be designed in a way that ensures each component leverages the appropriate database.

(Author’s note: Many thanks to Salvatore Sanfilippo for the fruitful conversation that led to the ideas in this post.)
