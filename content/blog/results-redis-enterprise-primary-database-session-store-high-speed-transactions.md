---
title: "The Results Are In… Redis Enterprise for Primary Database, Session Store, High-Speed Transactions and More!"
linkTitle: "The Results Are In… Redis Enterprise for Primary Database, Session Store, High-Speed Transactions and More!"
url: "/blog/results-redis-enterprise-primary-database-session-store-high-speed-transactions/"
description: "Over the course of the last month, we surveyed 130 customers using a third-party validation service called TechValidate. Our goal was to better understand how organizations are using Redis..."
date: 2018-03-06
blogCategories:
- "Announcements"
authors:
- "Priya Balakrishnan"
lastmod: 2025-03-27
hidden: true
---

*By Priya Balakrishnan, Sr. Director of Product and Partner Marketing · Published 6 March 2018 · updated 27 March 2025*

![Blog tile image](/images/site-mirror/0073e867b4e64f59de9047fdcde04295ba647e5c-772x550.webp)

Over the course of the last month, we surveyed 130 customers using a third-party validation service called TechValidate. Our goal was to better understand how organizations are using [Redis Enterprise](/redis-enterprise/advantages/) and we were honored and humbled by what our customers had to say. In fact, nearly 80% of respondents said they intend to increase their usage of Redis Enterprise in order to serve growing business needs.

We’d like to thank all our customers who responded to the survey. We can’t post all the results here but I’ve cherry-picked some of our favorite findings that describe how Redis Enterprise is used in practice. If you’re interested in more details, Techvalidate has published a range of TechFacts, charts and over 51 customer case studies that you can read at your leisure.

Without further ado, let’s jump into a brief summary of the results…

1

We have always known that as our customers begin to use Redis Enterprise in their organization, there is often a viral effect and usage expands to beyond just caching. What is interesting in this latest poll is that the caching use case actually ranked lower than user session stores and high-speed transactions, which are now the top two most common uses for Redis Enterprise. This is validation that Redis Enterprise’s versatile data structures and sophisticated enterprise-class features make it a valuable database across a growing variety of [use cases](/solutions/caching/).

![](/images/site-mirror/eb6a78173c9baa59a6e8c4fbda30a7a150f42a92-717x771.webp)

Compared to [last year’s results](/blog/the-results-are-in-redis-usage-survey-2016/), we noticed a significant uptick in how organizations are using Redis Enterprise for high-speed transactions and messaging. And we’re seeing consistent usage across real-time analytics, notifications, time-series data and geospatial indexing as well. We believe that machine learning (ML) took a small dip in Redis adoption because the reality is there’s still ways to go when it comes to thoughtfully applying ML in many organizations — despite all the market buzz.


2

Redis Enterprise is well known for its [record-setting performance](/docs/linear-scaling-benchmark-50m-ops-sec/). That said, we were pleased to see the value our customers place on [high availability](/redis-enterprise/technology/highly-available-redis/) as well — nearly 80% said they most value the data persistence, auto-failover, cross-zone/multi-region/multi-data center in-memory replication that Redis Enterprise delivers.

![](/images/site-mirror/87649f082674920bb8cf0916245500fe3ea58d8f-734x661.webp)

For example, Serge Aube from ***Staples*** shared his love for Redis Enterprise’s impressive performance and availability:

![](/images/site-mirror/f2fd3d0160992fe5d3cc9746ff265e544968a497-703x396.webp)

Following fast performance and high availability (which were not surprising results), nearly 50% of our customers said they love our built-in [seamless scale and clustering](/redis-enterprise/technology/linear-scaling-redis-enterprise/) capabilities. For instance, at ***Microsoft***, Redis Enterprise was instrumental in handling election night traffic, seamlessly scaling to handle over two billion requests without any service interruption or performance degradation.

![](/images/site-mirror/37b8310ccd3e57fe2c0d0ff2bf7b6971d5098db2-728x476.webp)

3

As customers learn the shortfalls of their current database deployments, they are looking to move additional data from other databases into Redis Enterprise:

![](/images/site-mirror/14b7e01276b12e2605f1eca00e6dc2d9979d50c7-732x465.webp)

This migration is a result of common frustrations organizations face due to the limitations of their current databases. The chart below describes the top reasons why our customers choose Redis Enterprise over other databases.

![](/images/site-mirror/53d11a5692ef34caa7d5a5593a15036dacf012d1-727x543.webp)

Of course, Redis Enterprise solves all of these challenges around [scale](/redis-enterprise/technology/linear-scaling-redis-enterprise/), [speed](/docs/nosql-performance-benchmark/), [availability](/redis-enterprise/technology/highly-available-redis/), [durability](/redis-enterprise/technology/durable-redis/), [cross-geo-distribution](/active-active/) and future-proofs applications with a modern solution.

4

Lastly, but most noteworthy, we were delighted to learn that a staggering 67% of respondents use Redis Enterprise as their primary database, not storing data in any other system. What this means to us (and to you) is that companies are graduating from using Redis Enterprise as a caching service to using it as a full-fledged database.

![](/images/site-mirror/b33ff2ca5930c50ec62a964eed3dda3e5d60ed87-729x554.webp)

Since 2014, Redis Enterprise has trailblazed the database world, allowing organizations to solve complex problems and deliver modern applications at record-setting speeds, with reduced infrastructure footprint and greater simplicity. As its reputation and popularity continues to grow and new enterprise-class capabilities continue to be added, we’ve seen a significant acceleration in Redis Enterprise’s adoption amongst some of the largest companies in the world. We are delighted by the depth and breadth of Redis Enterprise usage across a variety of solutions including e-commerce, personalization, customer engagement and social, IoT, fraud mitigation and much more.

This April, many of these customers will share their Redis Enterprise experiences and best practices at our annual user conference, [RedisConf](/redisconf/). We’d love for you to take advantage of this great opportunity to meet with your peers and industry experts and have your questions directly answered by the Redis team.

These new Techvalidate results have further energized us, and we’re raring to execute on our exciting roadmap to serve your data needs. You’ll hear more from us in the coming months on the incredibly game-changing capabilities we’re working on. In the meanwhile, if you are interested in learning more, please [contact us](/meeting/).

Hope to see you at [Redisconf](/redisconf/)!
