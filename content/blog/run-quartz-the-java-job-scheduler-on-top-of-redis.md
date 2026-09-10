---
title: "Run Quartz, The Java Job Scheduler, On Top of Redis"
linkTitle: "Run Quartz, The Java Job Scheduler, On Top of Redis"
url: "/blog/run-quartz-the-java-job-scheduler-on-top-of-redis/"
description: "Job scheduler programs have grown to become very popular in today’s web application world. Most commonly used to automatically run asynchronous and heavy jobs, schedulers have been utilizing Redis..."
date: 2014-04-30
blogCategories:
- "Tech"
authors:
- "Matan Kehat"
lastmod: 2025-03-27
hidden: true
mirrored: true
---

*By Matan Kehat · Published 30 April 2014 · updated 27 March 2025*

![Blog tile image](/images/site-mirror/0073e867b4e64f59de9047fdcde04295ba647e5c-772x550.webp)

Job scheduler programs have grown to become very popular in today’s web application world. Most commonly used to automatically run asynchronous and heavy jobs, schedulers have been utilizing Redis as a go-to backend host for some time now. This stands true for popular job management systems, such as [Resque](https://github.com/resque/resque), written in Ruby to create background jobs; [Sidekiq](https://github.com/mperham/sidekiq), which provides efficient background processing for Ruby; and Python users who mainly use[ Celery](https://github.com/celery/celery) with a Redis backend option. Based on requests by the community, we recently implemented Redis to support Quartz, the popular Java job scheduler.

### The Redis Advantage

Quartz is a mature and robust solution that can use almost any type of database as a backend for storing its data. As most relational databases feature a JDBC driver, it isn’t surprising that Quartz’s JDBC JobStore is quite popular. Relational databases, however, can be slow and difficult to manage. In fact, the Quartz FAQ has several suggestions on how to improve performance while using JDBC, ranging from throwing money at the problem and buying better hardware/network/software to traditional DBA wisdom (e.g. adding indexes on tables).

It is no surprise that Redis has many advantages as a backend for job schedulers, due to the efficiency and convenient data types it provides as an in-memory database. As noted in [The Proven Redis Performance](/blog/the-proven-redis-performance), Redis’ unique data types and commands enable schema building in such a way that the database is tuned to serve application requests without any additional processing at the application level. Additionally, given that an application is deployed in the same region as a Redis dataset, the result in latency will be a mere few milliseconds.

Large web applications, such as Facebook or Twitter, rely on job schedulers to perform a vast amount of background jobs. These range from heavy jobs (i.e. image processing) to light ones (i.e. sending emails). Applications these days require quality performance without the hassles of database setup and script writing. Fortunately, Redis provides the efficiency and level of performance these applications require, with an added motivation of simplicity. Moreover, using our [Redis Cloud Platform](/redis-cloud), with a single click, a database can be instantly configured with Quartz.

### The Quartz Job Scheduler

[Quartz](http://quartz-scheduler.org) is an open source job scheduling and management library that can be integrated within any Java application. As the informal standard job management system in the Java world, Quartz has gained popularity, serving tens of thousands of applications. By utilizing Redis as persistent storage, Quartz users are granted the Redis advantages of efficiency, low latency, and simple integration with PaaS providers, such as Heroku.

### Redis JobStore for Quartz

Redis JobStore was implemented for Quartz utilization, can now be downloaded from our [Github repository](https://github.com/Redis), and simply added to a given Quartz project’s library. Redis JobStore utilizes sorted sets in which triggers and their respective trigger fire times are stored, making the retrieval of specific jobs and their execution quick and efficient. A sorted set value is provided with a score that is used for the job’s fire time, accelerating the entire process.

An additional element used in Redis JobStore is global locking with Redis’ publish and subscribe mechanism (Pub/Sub), in which JobStore listens to an ‘unlock’ message.

[Download the Quartz Scheduler JobStore that uses Redis for persistent storage.](https://github.com/RedisLabs/redis-quartz)

Redis JobStore supports multiple schedulers with two handy mechanisms. One releases the locked triggers of a previously run scheduler, and the second monitors live schedulers. The live schedulers’ IDs are stored in Redis, and inactive scheduler triggers are released after a given amount of time.

To better understand the workflow and the behavior of a Quartz Scheduler using Redis JobStore, I invite you to review the [Redis schema](https://github.com/RedisLabs/redis-quartz/blob/master/schema/schema.txt) that it uses.

[Check out the readme](https://github.com/RedisLabs/redis-quartz) or [contact me](mailto:matan@redis.com?subject=Redis%20JobStore%20for%20Quartz) to learn more about how to get started, as well as current limitations and issues. This is a good starting point and we plan on continuing to enhance this package based on community requests.
