---
title: "Introducing Redis Enterprise 5.6: Customized Installation, HyperLogLog on Active-Active, and more!"
linkTitle: "Introducing Redis Enterprise 5.6: Customized Installation, HyperLogLog on Active-Active, and more!"
url: "/blog/introducing-redis-enterprise-5-6-customized-installation-hyperloglog-on-active-active-and-more/"
description: "As we continue to enhance Redis Enterprise by adding new exciting features for our customers, we are happy to announce general availability of the latest major version: Redis Enterprise Software..."
date: 2020-04-16
blogCategories:
- "Announcements"
- "Product Releases"
authors:
- "Alon Magrafta"
lastmod: 2026-09-01
hidden: true
mirrored: true
---

*By Alon Magrafta, Product Manager · Published 16 April 2020 · updated 1 September 2026*

![Blog tile image](/images/site-mirror/4865ef10a1417b15577c777cf2080d67e3136861-1200x1000.webp)

As we continue to enhance Redis Enterprise by adding new exciting features for our customers, we are happy to announce general availability of the latest major version: [Redis Enterprise Software 5.6.0](/download-center/#downloads). This release includes:

- A more customized installation process
- HyperLogLog support in Active-Active databases
- RedisJSON support in Redis on Flash databases
- Redis open source software cluster API support for Active-Active and Replica Of databases

These important new capabilities bring big benefits to a wide variety of Redis users. For a complete list of new features and changes, check out the [RS 5.6.0 Release Notes](https://docs.redis.com/latest/rs/release-notes/rs-5-6-0-april-2020/).

## Redis Enterprise Software Installer

The Redis Enterprise Software installer now allows you to specify custom installation paths and a custom installation user, group, or both. This provides the flexibility customers require to align with their companies’ security best practices and internal processes and procedures.

When running the installer, you can specify the installation, configuration, and *var* directories, as well as the operating system user and group. Remote users (such as LDAP, etc.) are also supported. To install Redis Enterprise with these new customizations, run:

sudo ./install.sh --install-dir <path> --config-dir <path> --var-dir <path> --os-user <user> --os-group <group>

You can find all the details in the [Redis Enterprise Software installer documentation](https://docs.redis.com/latest/rs/installing-upgrading/).

## HyperLogLog for Active-Active

Redis Enterprise Software 5.6.0 adds support for [HyperLogLog](http://www.antirez.com/news/75) in [Active-Active Redis](https://docs.redis.com/latest/rs/administering/active-active/) databases.

**What is HyperLogLog?**

HyperLogLog is a data structure that probabilistically solves the count-distinct problem. [Hyperloglog is available as a Redis data structure](/blog/streaming-analytics-with-probabilistic-data-structures/), and you use it when you need to count many distinct elements and you’re willing to sacrifice some accuracy (it has a standard error of 0.81%) in exchange for significant memory savings.

The HyperLogLog data structure has three main operations:

- [PFADD](https://redis.io/commands/pfadd): add a new element to the set
- [PFCOUNT](https://redis.io/commands/pfcount): get the cardinality of the set
- [PFMERGE](https://redis.io/commands/pfmerge): write the union of two HyperLogLog data structures to a new Redis key

**Data types on Active-Active**

With Active-Active Redis databases, your applications can read and write to the same data set from different geographical locations seamlessly and with latency less than 1 millisecond, without changing the way the application connects to the database. With the addition of HyperLogLog, Active-Active databases now support ten[ Redis data types](https://docs.redis.com/latest/rs/developing/crdbs/#data-types): Floats, Geospatial, Hashes, HyperLogLog, Integers, Counters, Lists, Sets, Strings and Sorted Sets. (Stay tuned: In Redis Enterprise 6.0, Active-Active will also support [Streams](https://redis.io/docs/latest/develop/)!)

For more information, check out the [HyperLogLog on Active-Active documentation](https://docs.redis.com/latest/rs/developing/crdbs/developing-hll-crdb/).

## RedisJSON for Redis on Flash

Redis Enterprise Software 5.6.0 adds support for [Redis on Flash](https://docs.redis.com/latest/rs/concepts/memory-architecture/redis-flash/) (RoF) databases with [Redis modules](https://docs.redis.com/latest/modules/). [RedisJSON](https://docs.redis.com/latest/modules/redisjson/) is the first module to run on a RoF database.

Redis on Flash offers users major cost savings to users with especially large Redis databases. Where standard Redis databases are held entirely in DRAM, Redis on Flash enables your Redis databases to span both DRAM and dedicated solid-state Flash memory drives (SSDs). This enables you to affordably run much larger datasets with DRAM-like latency and performance.

[RedisJSON](https://oss.redis.com/redisjson/) is a Redis module that implements the [JSON Data Interchange Standard ](http://json.org/)as a native data type. It allows storing, updating, and fetching JSON values from Redis keys (documents). Using RedisJSON on Redis on Flash allows you to benefit from the high-performance of Redis with high data volumes at a much lower cost. Once again, please stay tuned—we’re working on making more Redis modules support Redis on Flash.

## Cluster API support with Active-Active and Replica Of

The Redis OSS cluster API ensures the fastest possible response times by allowing clients to connect directly to each shard in a cluster. Redis Enterprise databases have long supported the Redis OSS cluster API. Today, we’re announcing cluster API support for Active-Active and Replica Of databases! This increased local performance may be of special interest to customers who need a very high number of operations per second and very low latency, even beyond “regular” Redis’ exceptional performance.

#### Support for Active-Active and Replica Of databases

Working in OSS Cluster mode improves the performance of client operations against your database, whether it’s a standard database, an Active-Active database, or a Replica Of database. You can create or modify an Active-Active Redis database in OSS cluster mode using the web UI (see below) or using the crdb-cli tool with the –oss-cluster option. Using the crdb-cli tool will affect all the database’s instances.

For more information, check out the [Redis OSS cluster API documentation](https://docs.redis.com/staging/next/rs/administering/designing-production/networking/using-oss-cluster-api/).

**Create and edit databases via the web UI**

Starting with Redis Enterprise Software 5.6.0, you can configure databases with the OSS cluster API using the web UI. (Note that for standard or Replica Of databases, this configuration applies only to the local database). Here is what the UI looks like for standard or Replica Of databases:

[Watch the video](/wp-content/uploads/2020/04/image1-3.png)

When creating new Active-Active databases this configuration will apply to all its instances. When editing a database via the configuration page, it will apply only to the local instance. Here is what the UI looks like for Active-Active databases:

[Watch the video](/wp-content/uploads/2020/04/image2-3.png)

These independent enhancements and new features add up to important new capabilities for a wide variety of Redis users. Try them out and see which ones make the biggest difference to you.
