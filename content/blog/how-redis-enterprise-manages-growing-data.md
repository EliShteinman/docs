---
title: "How Redis Enterprise Manages Growing Data"
linkTitle: "How Redis Enterprise Manages Growing Data"
url: "/blog/how-redis-enterprise-manages-growing-data/"
description: "We recently surveyed our customers and received some great and interesting feedback. For instance, we found out that 71% of users increased their usage of Redis Enterprise because their business grew."
date: 2019-08-28
blogCategories:
- "Tech"
authors:
- "Roshan Kumar"
lastmod: 2025-03-27
hidden: true
---

*By Roshan Kumar, Senior Product Manager · Published 28 August 2019 · updated 27 March 2025*

![Blog tile image](/images/blog/8a1a2a8c41018fac3b33b81a982a7c006d9f1db0-5000x2590.webp)

We recently surveyed our customers and received some great and interesting feedback. For instance, we found out that 71% of users increased their usage of Redis Enterprise because their business grew.


*Figure 1. Redis customers increased their Redis usage.*

Across our customer base, we’ve seen how rapidly database size and throughput requirements can grow. Let’s say you launched a new app some time ago, and it stores data in Redis. Suppose your dataset size was about 1 GB when you launched, but your app became very popular. Your Redis dataset may have grown to over 20 GB, and be on track to reach about 50 GB in the next few days. In this type of scenario, a 100,000 operations/second launch throughput could now be inching towards a requirement of 1,000,000 operations/second – a challenge for any database.

[Redis Enterprise Cloud ](/redis-enterprise/pro/)users in this situation can easily increase their database size and throughput capacity by simply switching over to a higher limit in the Redis Enterprise Cloud console. This fully managed serverless DBaaS ([database-as-a-service](/blog/what-is-dbaas/)) is powered by the Redis Enterprise architecture, which lets you increase your dataset size and throughput in a completely transparent way.


*Figure 2. Redis Enterprise Cloud includes an administrator dashboard for increasing memory size and throughput.*

### What happens under the hood?

Behind the scenes, this all works seamlessly thanks to the [shared-nothing, symmetric architecture of Redis Enterprise](/redis-enterprise/technology/redis-enterprise-cluster-architecture/). This technology consists of a cluster and a set of physical or virtual nodes. Every node includes zero to a few hundred databases that could be configured as a simple database, a high availability (HA) database, a clustered database or an HA clustered database.


*Figure 3. Redis Enterprise databases can be configured in simple, HA, clustered and HA clustered modes.*

As depicted in figure four below, a Redis Enterprise node in the cluster contains Redis shards, a zero latency proxy, a cluster manager and a secure REST API. The proxy maintains the database endpoint and masks cluster complexity by hiding the details. For example, for a clustered database with a dataset spanning multiple shards, the proxy is the single endpoint and forwards each request to the appropriate shard.


*Figure 4. Redis Enterprise node components*

When you increase the memory or throughput size of your database, Redis Enterprise computes the extra number of shards and cluster nodes you need based on your requirements, adds new shards and nodes to the cluster, and rebalances the data for best performance. Redis Enterprise also optimizes your shard size to keep it small enough for fast replication, shard migration, backup and recovery. Figure five shows what happens when you add a new pair of master-replica shards to an existing database.


*Figure 5. Using Redis Enterprise to scale out with resharding.*

The proxy in Redis Enterprise plays a key role in this operation. Since it enables a single endpoint to your Redis database that spans multiple shards, even after a resharding, your application still connects with the same endpoint. This ensures you don’t have to make any changes to your application code as your database size increases.


*Figure 6. A Redis Enterprise database with the proxy front-ending master and replica shards*

### Resharding: the four-step process

For more on exactly how this works, let’s explore the four main steps Redis Enterprise performs during resharding.

**Step 1:** The platform builds two new replicas (R1 and R2), moves half of your dataset from the master to R1 and the other half of the (mutually exclusive) dataset from the replica to R2.


**Step 2:** Next, Redis Enterprise drains all outstanding requests before completing the resharding process. This guarantees consistency and avoids losing any ‘write’ operations.


**Step 3:** The third step includes converting the master to master 1, and the replica to master 2 and then stopping the draining process. Now, new requests are all processed by both master 1 and master 2, and the new shards that were introduced in step 1 (R1 and R2) will become replicas of the two new master shards.


**Step 4:** Finally, the platform trims master 1 and master 2, so that each shard holds a dataset associated with half of the Redis hash-slots.


As you can see, Redis Enterprise Cloud manages shards and proxies in a true serverless fashion. As a user, you don’t have to worry about nodes or clusters, and the scaling operation described above is completely transparent to you. If you are using Redis Enterprise software, the admin console provides all the tools you need to scale out linearly in a seamless manner.

### Scaling with Redis Enterprise to the next level

If your goal is to scale out even higher, you could configure multiple proxy servers in Redis Enterprise. With this configuration, you can leverage our cluster API to connect with all the proxy servers your application requires. Recently, we demonstrated how this unique shared-nothing architecture can scale to [200 million operations/second in ](/blog/redis-enterprise-extends-linear-scalability-200m-ops-sec/)a fully linear manner.

[Redis on Flash](/redis-enterprise/technology/redis-on-flash/) (RoF) is another way to scale your database, while saving over 70% in infrastructure costs. This option can be extremely cost effective when your dataset size gets over 100GB, and the average size of values in your dataset is higher than the average size of your keys. Furthermore, RoF is optimal when most database queries are targeted to a subset of your dataset, which allows RoF to keep a working dataset in memory (RAM) only.


*Figure 7. Redis on Flash’s multi-layered memory architecture*

Here at Redis, we strive to understand and meet our customers’ needs. When we heard about the pain points around managing growing data, we invested in building the right capabilities to overcome them. Today, over 7,400 enterprise customers benefit from the Redis Enterprise scaling features we described above.

Find out about the best scaling option for your situation. Call our experts today at (415) 930-9666. If you already know what size database you need, [contact us for pricing](/enterprise/pricing/).
