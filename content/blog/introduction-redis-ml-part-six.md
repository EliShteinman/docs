---
title: "An Introduction to Redis-ML (Part Six)"
linkTitle: "An Introduction to Redis-ML (Part Six)"
url: "/blog/introduction-redis-ml-part-six/"
description: "This post is the final post in a series delving into the features of the Redis-ML module. The first post in the series can be found here."
date: 2017-09-20
blogCategories:
- "Company"
- "Tech"
authors:
- "Tague Griffith"
lastmod: 2025-03-27
hidden: true
mirrored: true
---

*By Tague Griffith, Head of Developer Advocacy · Published 20 September 2017 · updated 27 March 2025*

![Blog tile image](/images/site-mirror/820efa0b01ff2e45d586426137638edcb6a436ed-6400x3600.webp)

*This post is the final post in a series delving into the features of the *[*Redis-ML*](/modules/machine-learning/)* module. The first post in the series can be found *[*here*](/blog/introduction-redis-ml/)*.*

In previous posts we learned how to use [Redis](https://redis.io) and [scikit-learn](http://scikit-learn.org) to build a real-time classification and regression engine, how to use [linear regression to predict housing prices](/blog/introduction-redis-ml/) and how to use [decision trees to predict survival rates](/blog/introduction-redis-ml-part-five/). We even took a [small detour into R](/blog/introduction-redis-ml-part-two/) to demonstrate ML toolkit independence, but one question we haven’t focused on is, “Why?” Why would we want to use Redis for a real-time predictive engine?

If we look at the landscape of machine-learning toolkits, most focus on the learning side of ML, leaving the problem of *building* a predictive engine to the reader. This is where Redis fills a gap; instead of trying to build a custom server, developers can rely on a familiar, full-featured data store to build their applications. Simple and powerful data management, reduced overhead, and minimal latency are just three of the major advantages of building your machine-learning models with Redis.

**Data Management Functionality**

Although Redis-ML data types like *linear regression object* and *random forests* are very different from the built-in 4.0 types like *sets* and *hashes*, it’s important to understand that the Redis-ML keys are still Redis keys. All of the Redis features for managing, persisting and replicating keys work equally well with Redis-ML keys.

Redis already provides developers with a managed keyspace for storing data. Additional statistical models can be added to an application with a simple SET command, allowing developers to maintain multiple versions of models for cases in which data needs to be reprocessed. A Redis-ML key, like any Redis key, can be maintained using the [Redis key management commands](https://redis.io/commands#generic).

To scale up a Redis-based predictive engine, you simply deploy more Redis nodes and [create a replication topology](https://redis.io/topics/replication) with a single master node and multiple replica nodes. Updates to your statistical models are written to the master node and automatically distributed to the replicas, so you don’t have to write any additional code (as you would with a custom application).

**Reduced Operational Complexity**

Redis is already a part of most companies’ tech stack. Your operations staff already understand how to scale, manage and monitor Redis instances–they may even have automated many deployment tasks. So employing Redis for your ML needs requires considerably less overhead than adding operational support for a new, homegrown service that will take a while to implement and address the operational issues of.

**Fast Throughput**

Finally, Redis maintains all data in memory, which makes it extremely fast. It also has a highly tuned, optimized networking stack and sophisticated memory and buffer management, all of which would need to be replicated in order for a home grown service to match the performance of Redis. In benchmarks, we’ve seen Redis perform [thirteen times faster](/modules/machine-learning/) than homegrown Java applications in predictive operations.
Redis is a great way to accelerate the performance of your existing data pipelines and with the Redis-ML module you can speed up prediction operations. Hopefully you’ve enjoyed this series on the Redis-ML module. If you’re still curious and want to learn more, remember that the module is open-source software and you can find the source here on [Github](https://github.com/RedisLabsModules/redisml). The Redis-ML team is actively soliciting contributions.
