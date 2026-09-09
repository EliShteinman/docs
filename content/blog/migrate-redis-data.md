---
title: "How to Migrate Data from Redis Open Source to Redis Enterprise in Under 5 Minutes"
linkTitle: "How to Migrate Data from Redis Open Source to Redis Enterprise in Under 5 Minutes"
url: "/blog/migrate-redis-data/"
description: "Migrating data from one data source to another creates a great risk for a business. There is a chance for a number of things to go wrong like data loss, dataset schema changes causing semantics..."
date: 2022-07-07
blogCategories:
- "How To and Tutorials"
- "Tech"
authors:
- "Talon Miller"
lastmod: 2025-03-27
hidden: true
---

*By Talon Miller, Principal Technical Marketer · Published 7 July 2022 · updated 27 March 2025*

![Blog tile image](/images/blog/718a9c399721c16ba227dc979d22959325852413-772x550.webp)

Migrating data from one data source to another creates a great risk for a business. There is a chance for a number of things to go wrong like data loss, dataset schema changes causing semantics risk, extended (unexpected) downtime, and data corruption, to name just a few. Regardless of the risks, businesses need to innovate to survive and that means taking data from old or legacy databases and putting some, if not all, data into new databases to take advantage of all of the new and necessary potential. Such is the case with the companies moving more of their data into in-memory solutions like Redis to take advantage of the power of real-time data.

![Migrate Data from Redis Open Source to Redis Enterprise blog image](/images/blog/3f6a14fa6e6696f877f3aa316bfefb1dcc21a6f4-1024x600.webp)

[Redis Open Source](https://redis.io/docs/getting-started/) is a really great way to incorporate real-time capabilities into your app. With [Redis Enterprise](/redis-enterprise/advantages/), you can bring all of the things you love about Redis on top of infinite [linear scalability](/docs/linear-scaling-benchmark-50m-ops-sec/), five 9s of true [high availability](/redis-enterprise/technology/highly-available-redis/), security built-in, and a way to keep the costs low with [Redis on Flash](/redis-enterprise/technology/redis-on-flash/). Once you start to outgrow Redis Open Source, the question becomes: how to safely and most efficiently migrate that Redis data to an enterprise-hardened Redis? The answer: Redis Enterprise.

## Why migrate from Redis Open Source to Redis Enterprise?

As an architect, your customers will want new capabilities and reliable performance that you simply cannot get in Redis Open Source without building them from the ground up. As an operator, you will want a simple set-up and a reliable and easy way to operate this critical data pipeline without all of the manual overhead and maintenance. Redis Enterprise is the easiest and most straightforward way to [migrate Redis data](/redis-enterprise-cloud/migrate/) from Redis Open Source to the version of Redis built for enterprise solutions. Let’s dive in.

## Redis Enterprise database migration: Zero-downtime deployment

In order to understand how we can perform a database migration with zero downtime deployment, we need to understand the features behind Redis Enterprise that help us execute this data migration. Redis Enterprise has the ability to provide [Active-Passive Geo-Distributed Replication](/redis-enterprise/technology/active-passive-geo-distribution/) to applications with read-only access to replicas from different geographical locations. We call this [Replica Of](https://docs.redis.com/latest/rs/databases/import-export/replica-of/).

![Migrate Data from Redis Open Source to Redis Enterprise blog image](/images/blog/08126353a730232fe36b49d0c2f2108aa6adc474-1024x600.webp)

In the configuration of a Redis Enterprise database, we can assign a database as a replica (destination) of one or more (max 32) databases (sources). After the initial load from source to destination is completed, all write commands are synchronized from the sources to the destination. This enables you to perform a database migration with zero downtime as the replication bridge between the destination database and the sources can stay connected for as long as needed, even indefinitely.

![Migrate Data from Redis Open Source to Redis Enterprise blog image](/images/blog/e5ff4dff1bfb8db03e00411ea133942ac1c86214-1024x600.webp)

Replica Of lets you distribute the read load of your application across multiple databases or synchronize the database, either within Redis Enterprise or external to Redis Enterprise, to another database.

## Redis Enterprise database migration: Active-Active Geo-Distribution

You might be wondering about write access – for that, Redis Enterprise has [Active-Active Geo-Distribution (CRDB)](/active-active/) that provides write access to all of the database replicas on top of the other benefits during database migrations.


Below, you will see a lightning demo of how we set this up in less than five minutes. But before you watch that, let’s cover the data [replication](/blog/what-is-data-replication/) process. When our database is defined as a replica of another database, all of its existing data is deleted and replaced by the data that is loaded from the source database. In our lightning demo, we will start with a fresh Redis Enterprise database with zero data so we don’t risk losing data. Once the initial load is completed, an ongoing synchronization process takes place to keep the destination database always synchronized with its source.

![Migrate Data from Redis Open Source to Redis Enterprise blog image](/images/blog/16f5288aa40d0bd87562b5025e3cce4c14dfdd82-1024x600.webp)

With security in mind, Replica Of supports encryption for a unidirectional replication between source and a destination Redis cluster utilizing TLS 1.2 encryption.

But what if your source database is sharded? The entire database is treated as a single source for the destination database. If your destination database is sharded then the destination database’s hashing function is executed to determine to which shard(s) the command refers.

Well, that covers what you need to know about migrating data from Redis Open Source to Redis Enterprise, so let’s jump into the lightning demo on how to do this with your Redis database in order to take advantage of not only real-time power but real-time power with enterprise-grade capabilities.

[Click here to view video](https://www.youtube.com/embed/6LYNegHRiRY)

---
