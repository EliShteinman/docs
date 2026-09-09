---
title: "Top Redis Headaches for Devops – Replication Timeouts"
linkTitle: "Top Redis Headaches for Devops – Replication Timeouts"
url: "/blog/top-redis-headaches-for-devops-replication-timeouts/"
description: "Redis provides a wide variety of tools directed at improving and maintaining efficient in-memory database usage. While its unique data types and commands fine-tune databases to serve application..."
date: 2014-07-21
blogCategories:
- "Tech"
authors:
- "Yaron Dolev"
lastmod: 2025-03-27
hidden: true
---

*By Yaron Dolev · Published 21 July 2014 · updated 27 March 2025*

![Blog tile image](/images/blog/0073e867b4e64f59de9047fdcde04295ba647e5c-772x550.webp)

![](/images/blog/15393ef4ce1521d1d5325adbb1a884d0802b7601-250x168.webp)

Redis provides a wide variety of tools directed at improving and maintaining efficient in-memory database usage. While its unique data types and commands fine-tune databases to serve application requests without any additional processing at the application level, misconfiguration, or rather, using out-of-the-box configuration, can (and does) lead to operational challenges and performance issues. Despite the setbacks that have been the cause of quite a few headaches, solutions do exist, and may be even simpler than anticipated. This series of installments will highlight some of the most irritating issues that come up when using Redis, along with tips on how to solve them. They are based on our real-life experience of running thousands of Redis database instances.

Following our previous installment in the series, [the Replication Buffer](/blog/top-redis-headaches-for-devops-replication-buffer), the next headache on our list will carry on with the topic of master-slave replication. In particular, we will look a bit deeper at the length of time needed to complete the process as well as some configuration issues that can cause major inconveniences.

## Replication Timeouts

As we’ve previously discussed in the [Endless Replication Loop post](/blog/the-endless-redis-replication-loop-what-why-and-how-to-solve-it), Redis’ replication process is made up of two synchronization stages: initial and ongoing. While the ongoing stage is fairly stable (as long as the link between the master and slave is kept), the initial phase is somewhat trickier to complete. Successful completion of the initial synchronization is dependent not only on the amount of memory that’s allocated for the replication buffer (see [previous headache](/blog/top-redis-headaches-for-devops-replication-buffer)) but also on the amount of time that this step takes.

You may recall that the initial synchronization step consists of a background save and the transmission of the entire database from the master to the slave. Depending on the dataset’s size and the quality of the network connection, this may prove to be a lengthy process to complete. If that phase takes too long, Redis’ replication timeout setting may be reached, thus causing the initial phase to be repeated over and over, ad nauseam. In such cases, you will find your slave’s Redis log riddled with messages such as:

```
[28618] 21 Jul 00:33:36.031 * Connecting to MASTER 10.60.228.106:25994
[28618] 21 Jul 00:33:36.032 * MASTER <-> SLAVE sync started
[28618] 21 Jul 00:33:36.032 * Non blocking connect for SYNC fired the event.
[28618] 21 Jul 00:33:36.032 * Master replied to PING, replication can continue...
[28618] 21 Jul 00:33:36.032 * Partial resynchronization not possible (no cached master)
[28618] 21 Jul 00:33:36.032 * Full resync from master: 549907b03661629665eb90846ea921f23de6c961:2537453


```

Redis’ replication timeout is set to 60 seconds by default (see the repl-timeout directive in your [redis.conf file](https://download.redis.io/redis-stable/redis.conf) or do a config get repl-timeout using redis-cli). This period of time may be far too short, especially when you have:

- **Slow storage:** if the master and/or the slave are attached to a slow-performing storage, this will cause the background saving process to take a significant amount of time in the master’s case. In slave’s case, writing and loading the data from disk may be prolonged.
- **Big dataset:** the bigger the dataset’s size is, the more time it will require time to save and transfer.
- **Network performance:** when network link between the master and slave has limited bandwidth and/or high latency, it directly affects the rate of data transfer.

You can rectify this by setting the replication timeout to a more appropriate value. Start by working on an acceptable estimate of the time needed to replicate the database. First, check how long it takes Redis to perform a background save by executing the [BGSAVE](https://redis.io/commands/bgsave) command and examining the log file for the relevant lines (i.e. * Background saving started by pid nnn * indicates that the process started, whereas * Background saving terminated with success * indicates its termination). Next, time how long it takes you to copy the resulting RDB file from the master to the slave’s disk. Lastly, you’ll need to time how long it takes to actually load the data from disk (e.g. by restarting Redis and looking for the * DB loaded from disk line in the log file). The sum of these measurements can serve as a rough estimate of your desired replication timeout value, but you’d probably want to add 10-20% to it for safety.

Once you’ve set up the timeout based on the estimate, you can test how long replication actually takes by having the slave do a full synchronization a few times and examining the log file. If possible, try repeating this exercise at different times throughout the day to better gauge the system’s behavior under different loads. Lastly, keep in mind that the timeout setting’s value should be reviewed periodically based on your database’s growth.

This concludes our review of Redis’ replication headaches. Replication is a powerful tool for keeping your database available and scaling its read throughput, but mind the default settings and make sure you’ve configured the database to your use case.

If you’ve finished reading this article and want to dive into the next common cause for Devops’ headaches then continue reading about [the client buffers](/blog/top-redis-headaches-for-devops-client-buffers).
