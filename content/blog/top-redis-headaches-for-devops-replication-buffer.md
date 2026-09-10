---
title: "Top Redis Headaches for Devops – Replication Buffer"
linkTitle: "Top Redis Headaches for Devops – Replication Buffer"
url: "/blog/top-redis-headaches-for-devops-replication-buffer/"
description: "Redis provides a wide variety of tools directed at improving and maintaining efficient in-memory database usage. While its unique data types and commands fine-tune databases to serve application..."
date: 2014-06-26
blogCategories:
- "Tech"
authors:
- "Yaron Dolev"
lastmod: 2025-03-04
hidden: true
mirrored: true
---

*By Yaron Dolev · Published 26 June 2014 · updated 4 March 2025*

![Blog tile image](/images/site-mirror/0073e867b4e64f59de9047fdcde04295ba647e5c-772x550.webp)

![](/images/site-mirror/1086a17a951d9939adb048467240ba0051d2c6fa-635x200.webp)

Redis provides a wide variety of tools directed at improving and maintaining efficient in-memory database usage. While its unique data types and commands fine-tune databases to serve application requests without any additional processing at the application level, misconfiguration, or rather, using out-of-the-box configuration, can (and does) lead to operational challenges and performance issues. Despite the setbacks that have been the cause of quite a few headaches, solutions do exist, and may be even simpler than anticipated.

This series of installments will highlight some of the most irritating issues that come up when using Redis, along with tips on how to solve them. They are based on our real-life experience of running thousands of Redis database instances.

## The Replication Buffer Limit

Replication buffers are memory buffers that hold data while a slave Redis server synchronizes with the master server. In a full master-slave synchronization, changes performed to the data during the initial phase of the synchronization are held in the replication buffer by the master server. After the completion of the initial phase, the contents of the buffer are sent to the slave. There is a limitation to the size of the buffer that can be used in this procedure, causing replication to start from the beginning when the maximum is reached, as mentioned in our post on [endless Redis replication loops](/blog/the-endless-redis-replication-loop-what-why-and-how-to-solve-it). In order to prevent this from happening, an initial configuration of the buffer needs to take place according to the amount and types of changes expected to be made during the replication process. For example, a low volume of changes and/or smaller data in the changes can get by with a smaller buffer, whereas if there are a lot of changes and/or the changes are big, a large buffer is needed. A more comprehensive solution entails setting the buffers to a very high level to offset the possibility of a lengthy or heavy replication process that will eventually exhaust the buffer (if the latter is too small). Ultimately, this solution requires fine-tuning the specific database at hand.

Redis Default Setting:

```
> config get client-output-buffer-limit
1) "client-output-buffer-limit"
2) "normal 1073741824 536870912 30 slave 268435456 67108864 60 pubsub 33554432 8388608 60"

```

As explained [here](https://download.redis.io/redis-stable/redis.conf), this default configuration replication link will be broken (causing the synchronization to start from the beginning) once the 256MB hard limit is reached, or if a soft limit of 67MB is reached and held for a continuous 60 seconds. In many cases, especially with a high ‘write’ load and insufficient bandwidth to the slave server, the replication process will never finish. This can lead to an infinite loop situation where the master Redis is constantly forking and snapshotting the entire dataset to disk, which can cause up to triple the amount of extra memory to be used together with a high rate of I/O operations. Additionally, this infinite loop situation results in the slave never being able to catch up and fully synchronize with the master Redis server.

A simple solution that offers an immediate improvement results from increasing the size of the output slave buffer by setting both the hard and soft limits to 512MB:

```
> config set client-output-buffer-limit "slave 536870912 536870912 0"

```

As with many reconfigurations, it is important to understand that:

1. Before increasing the size of the replication buffers you must make sure you have enough memory on your machine.
1. The Redis memory usage calculation does not take the replication buffer size into account.

That brings us to the end of our first installment of the top Redis operational headaches. As pointed out above, in terms of replication buffer limits, proper configuration can go a long way. Be sure to keep an eye out for the next post in this compilation covering replication timeouts and how to handle them accordingly.
