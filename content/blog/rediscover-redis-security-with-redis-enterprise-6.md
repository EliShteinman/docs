---
title: "Rediscover Redis Security with Redis Enterprise 6.0"
linkTitle: "Rediscover Redis Security with Redis Enterprise 6.0"
url: "/blog/rediscover-redis-security-with-redis-enterprise-6/"
description: "Based on high demand from the Redis community and users, the newly released open source Redis 6 dramatically improves Redis security and operational safety. We are excited to announce the general..."
date: 2020-04-30
blogCategories:
- "Product Releases"
- "Tech"
authors:
- "Alon Magrafta"
lastmod: 2026-09-01
hidden: true
mirrored: true
---

*By Alon Magrafta, Product Manager · Published 30 April 2020 · updated 1 September 2026*

![Blog tile image](/images/site-mirror/bbc53e468747e6300679ce8da02c3f7f26286bac-270x190.webp)

![](/images/site-mirror/57bbd453e954c0726b8214377225d61f9ceef0cc-300x294.webp)

Based on high demand from the Redis community and users, the [newly released open source Redis 6](/blog/diving-into-redis-6) dramatically improves Redis security and operational safety. We are excited to announce the general availability of [Redis Enterprise 6.0](/download-center/#downloads), which utilizes Redis 6’s important improvements, and takes Redis security to an even higher level. This release features access control lists (ACLs) and role-based access control (RBAC), allowing you to exercise fine-grained control over the security of your Redis Enterprise deployment. In addition, Redis Enterprise 6 incorporates many changes from open source Redis 6, and provides support for Redis Streams on Active-Active databases.

These new capabilities bring major security benefits to Redis users and make it easier to effectively scale Redis usage within your organization.

## Open source Redis 6

Redis, as the home of Redis, has invested countless hours working with the Redis community to take open source Redis to the next level. Let’s look at how Redis Enterprise 6.0 supports the newly released Redis 6 and takes advantage of many of its features:

## Access control lists (ACLs)

Access control lists allow you to control what level of access each user has in Redis. With ACLs, you can specify which **commands** specific users can execute and which **keys** they can access. This allows for much better security practices: you can now restrict any given user’s access to the [least level of privilege](https://en.wikipedia.org/wiki/Principle_of_least_privilege) needed.

**What are ACLs good for?**
Using ACLs lets you tailor access for specific users. Developers, administrators, and the applications themselves may be able to function without full access to the database itself, and have more limited access. For example, an application that only reads from Redis doesn’t need permissions to flush the database. It’s now possible to create a read-only user for such an application. Following the [principle of least privilege](https://kb.iu.edu/d/amsv) in this way, ACLs allow for a significant improvement in the security of Redis deployments.

**ACLs in Redis Enterprise**
Redis Enterprise has always provided a [centralized management](https://docs.redis.com/latest/rs/administering/cluster-operations/) platform for [multiple Redis databases](https://docs.redis.com/latest/rs/concepts/high-availability/clustering/). In Redis Enterprise 6.0, you manage ACLs for the entire cluster, so you can reuse ACL templates across users, accounts, and multiple databases to precisely scale complex security configurations with a few simple clicks.

## Role-based access control (RBAC)

In open source Redis, you define ACLs on a per-user basis. Redis Enterprise improves upon this by letting you create roles, each with a specific set of permissions. For example, you might have a role for read-only users and another role for your site reliability engineers. You can then associate these roles with the appropriate Redis users. This is known as role-based access control, or [RBAC](https://csrc.nist.gov/projects/role-based-access-control).

RBAC lets you set permissions for your databases and for the Redis Enterprise management console itself, providing a complete security-management solution for your cluster.

**What is RBAC good for**
Role-based access control lets you scale your Redis deployments while minimizing the overhead involved in managing a cluster with many databases, multiple users, and various access control lists. With RBAC, you can create a role once and then easily deploy it across multiple databases in the cluster.

**ACL roles**

![](/images/site-mirror/449dc6c15f84a33ad14d4c95cdc91e2cf5d64fce-1023x317.webp)

*In the diagram above, which represents Redis Enterprise 6.0, Bob, Sue, and Alice would receive access via the CachedReader role. In the diagram below, which represents OSS Redis 6.0, these users’ CachedReader permissions are set individually.*

**ACL open source**

![](/images/site-mirror/74e0d1a8354d498b5f214a2db915711161cb4a80-1024x340.webp)

## Redis Streams with Active-Active databases

Redis Enterprise 6.0 adds support for the Streams data type in Active-Active databases.

**What is Redis Streams?**
[Redis Streams](https://redis.io/docs/latest/develop/) is a Redis data structure that models an append-only log and enables you to use Redis Enterprise as a high-speed, in-memory, streaming database. [Redis Streams is often used](/docs/build-apps-using-redis-streams/) to collect and syndicate real-time data for internet of things (IoT) devices, complex event processing systems (such as fraud detection), and [messaging applications](/solutions/messaging/).

**What are Active-Active databases?**
[Active-Active](/active-active/) is a Redis Enterprise feature that synchronizes a database across two or more geographical regions. This allows you to build globally distributed applications while guaranteeing local-latency read and write performance.

**Redis Streams on Active-Active databases**
Using [conflict-free replicated data types (CRDTs)](https://en.wikipedia.org/wiki/Conflict-free_replicated_data_type), Redis Streams ensures both high availability and low latency while concurrently reading and writing to and from your stream in multiple data centers in multiple geographic locations. When used in a globally distributed Active-Active database, all Redis Streams data structures will be synchronized in a [strongly eventually consistent manner](https://en.wikipedia.org/wiki/Eventual_consistency#Strong_eventual_consistency) across all regions, so data or transactions are resistant to failure events.

You can use Streams with Active-Active in many situations, including:

- Managing multiple call centers around the globe in an enterprise hub-and-spoke configuration. By using Redis Streams with an Active-Active deployment, different customer calls can be handled by call centers in different regions, improving availability and making sure each call is handled appropriately.
- Managing and tracking inventory in real time across multiple regions, between stores and the enterprise hub, for example.

With the addition of Redis Streams, Active-Active Redis databases now support all major [Redis data types](https://docs.redis.com/latest/rs/developing/crdbs/#data-types), including Counters, Floats, Geospatial, Hashes, HyperLogLog, Integers, Lists, Sets, Sorted Sets, Strings, and, of course, Streams.

## Find out more

For more information, read our [deep dive into open source Redis 6.](/blog/diving-into-redis-6) You can also sign up for a free [1:1 Ask the Expert session](https://events.redis.com/redisconf20/ask-expert/) at RedisConf 2020 *Takeaway* on Tuesday, May 12.

Starting today, current customers can contact Redis for information on how to access Redis Enterprise 6.0—go to our [Download Center now](/download-center/?id=tab-2).
