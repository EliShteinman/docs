---
title: "Let’s Play Master and Servant: Real Time Synchronization Tool for Redis Migration"
linkTitle: "Let’s Play Master and Servant: Real Time Synchronization Tool for Redis Migration"
url: "/blog/lets-play-master-and-servant-real-time-synchronization-tool-for-redis-migration/"
description: "Especially when orchestrating the migration of a sharded Redis backend with a strict requirement for minimal application downtime."
date: 2013-08-21
blogCategories:
- "Company"
authors:
- "Redis  "
lastmod: 2025-03-04
hidden: true
---

*By Redis   · Published 21 August 2013 · updated 4 March 2025*

![Blog tile image](/images/site-mirror/2707475b91218047674ff2dbdd84430b5226a28a-140x92.webp)

![Redis Replication in Action!](/images/site-mirror/c2409d7589e3e98e812bacdea0d6782c248db8e4-635x200.webp)

### Timing is everything…

Especially when orchestrating the migration of a sharded Redis backend with a strict requirement for minimal application downtime.

That is exactly the challenge we addressed with one of our users who wished to migrate to our Redis Cloud service from an existing setup, which is why we developed our own tool to ease this process (more details below). Many databases, Redis included, can be trivially moved from one place to another using built-in backup and restore mechanisms with a couple of file copy operations.

This approach, however, requires the database to be stopped and taken off-line during the move. In some cases you can optimize the process to reduce the database’s downtime (e.g. by completing the migration in two phases, the first for the bulk of the data body and the second for deltas), but a there are use cases where this approach is technically impossible (i.e. updates come too fast and in Redis’ case that could mean tens of thousands requests per second) or simply unacceptable (because of the application’s criticality).

An alternative approach uses [database replication](/blog/what-is-data-replication/), also supported by Redis, to create a copy from the original (a.k.a master) as an exact replica (a.k.a slave) at the destination. Then, once the replication is complete, you can switch to the replica.

The advantage of this method over the native backup-copy-recover approach is that application downtime can be kept to the absolute minimum because the database is not stopped during the migration.

Once the slave is ready, the application only needs to switch from using the master to using it instead – a change that takes practically no time and has no discernable effect with modern application architectures.

To successfully perform migration with replication, our recommended process is:

1. Set up replication
  1. Configure a node as the migration’s destination
  1. Start replication from the master to the slave
  1. Wait until replication is initialized (core data is replicated) and operational (updates are flowing from the master to the slave)
1. Make the switch
  1. Configure the replica to accept application write requests, if started in read-only mode
  1. Configure the application [instances] to use the slave instead of the master
  1. Wait for the master to stop getting write requests (and consequently updating the slave)
1. Housekeeping
  1. Stop the replication and promote the slave to be the master
  1. Take the ax to the old master

Replication as a means for migration is a great vehicle, but introduces some complexity. You need to know exactly when to proceed from one step to another, because all sorts of mishaps can happen if you prematurely switch to the slave.

Consider, for example, a case in which the rate of updates is high enough that the master’s replication buffer is never quite empty or even overflowing as described in [The Endless Redis Replication Loop](/blog/the-endless-redis-replication-loop-what-why-and-how-to-solve-it). With such cases, identifying the right point in time to make the switch between the master and slave can be a challenging task.

The process becomes even more complex if the migration’s scope consists of more than one server (e.g. in a sharded scenario). Regrettably, this has been somewhat of a constant issue for Redis users up until and including v2.6. The good news is that Redis v2.8 improved–[PSYNC](http://antirez.com/news/58) will introduce the lag information under the replication section of SHOW INFO’s output but this will not eliminate the timing challenge.

To quote the man himself:

- “Here the problem is to understand if there is a real desync. That is, if you stop the clients writing data to your master, is the key count and content exactly the same?” ([earlier today, Redis Creator Salvatore Sanfilippo, a.k.a antirez](https://groups.google.com/forum/?fromgroups#!topic/redis-db/23nQapMCwP8)).

The better news is that as of today, regardless which Redis version you use, you can use our home-grown **redis-migrate** tool to carry out the replicated migration of one or more Redis servers without even breaking a sweat.

Available [here](https://github.com/GarantiaData/redis-migrate) from our github, *redis-migrate* is an interactive Python script that displays real-time replication status information with top-like UI. The script accepts two N-sized lists of Redis URLs, via the the –src and –dst arguments, as input.

Once invoked, it first prompts you to let it continue (by entering ‘c’) after displaying the total size of data, number of keys and Redis servers that will be migrated. If you choose to continue, it then executes Step 1 of the above-described migration process by setting up and starting replication between the masters (src list) and their respective slaves (dst list). As Step 1 is executed, you are presented with up-to-date information regarding the progress of each master-slave replication link.

You can prompt the tool to continue to Step 2 once you have verified that everything is ready (i.e. initial sync completed and updates are flowing) by entering ‘e’. During Step 2, the tool waits for you to point your application to the replicated slaves. You can verify that your masters are no longer being used with the real-time information that the script outputs when replication buf is 0.

As before, the script waits for your permission to move to Step 3 – just say ‘m’. Once Step 3 has been executed – promoting the slaves to masters – the tool undramatically exits.
All you have to do now is attend to the old master.

Note: Ax not included
