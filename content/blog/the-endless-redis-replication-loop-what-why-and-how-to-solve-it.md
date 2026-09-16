---
title: "The Endless Redis Replication Loop: What, Why and How to Solve It"
linkTitle: "The Endless Redis Replication Loop: What, Why and How to Solve It"
url: "/blog/the-endless-redis-replication-loop-what-why-and-how-to-solve-it/"
description: "Redis’ replication is an indispensable tool – it can be used both to heighten the availability of your Redis setup (you can read more about Redis availability in this post) as well as to scale it..."
date: 2013-07-16
blogCategories:
- "Tech"
authors:
- "Redis  "
lastmod: 2026-08-14
hidden: true
mirrored: true
---

*By Redis   · Published 16 July 2013 · updated 14 August 2026*

![Blog tile image](/images/site-mirror/0073e867b4e64f59de9047fdcde04295ba647e5c-772x550.webp)

Redis’ replication is an indispensable tool – it can be used both to heighten the availability of your Redis setup (you can read more about Redis availability in [this post](/blog/available-now-redis-memcached-clouds-across-multiple-availability-zones)) as well as to scale it out by doing reads against read-only slaves.

In implementing replication, Redis capitalizes on its core functionalities – namely RDB files – to deliver a simple and elegant mechanism that’s effective in the majority of scenarios. Replication is widely adopted, including in our own Redis Cloud service, and is yet another useful, well-proven capability and of Redis’.

There are circumstances, however, when activating Redis’ replication can prove to be no simple feat. These are typically rare and extreme scenarios, such as when your dataset’s size grows significantly. But before getting into those details, let’s cover the basics of how Redis’ replication works.


*“In a Galaxy Far, Far Away”*

Replication in Redis is like to a dialog between a slave, (or an apprentice), and its master.
This conversation runs along the these lines:

1. Apprentice: *“I want to learn and to become like you.”*
1. Master: *“PATIENCE YOU MUST HAVE my young padawan. Hmmmmmm.”*
1. The Master forks itself, and…
  1. The forked process dumps the dataset to a disk file (RDB),
  1. The main process continues serving regular client requests, and
  1. Any changes made to the data are copied to a replication buffer on the main process.
1. Once the dump is done, the Master says: “*Come and get it while, hot, is it*.”
1. The apprentice reads the file over the network and writes it to its own disk.
1. Once it has the file stored locally, the apprentice loads it.
1. After loading is finished, the apprentice asks: “*Well, I finished my circle. I’m ready.*”
1. If there are any changes in the buffer, the Master says: “*Ready you are? What know you of ready? Feel the Force!*” and replays the stored changes to the slave.
1. After there are no changes left to replay from the buffer, the Master says: “*No more training do you require. Already know you, that which you need.*”
1. From that moment, any new change request that the master is given is then also replayed to the apprentice.

The above exchange essentially lets the slave synchronize the contents of the master’s dataset in two phases: firstly the full, albeit slightly-out-of-date, body of data is copied; then a partial subset consisting exclusively of updates is applied during a shorter catch-up period.

### “Size matters not. Look at me. Judge me by my size, do you?”

As mentioned above, some databases, depending on their use and purpose, grow significantly in size. Growth may be sudden or happen gradually over time, but regardless of how it got there, the fact remains – your database has gotten substantially bigger. And bigger isn’t always better, especially when trying to bootstrap a replication slave.

There are several problems that surface when a slave attempts to synchronize off a master that manages a large dataset (about 25GB or more). Firstly, the master server may require a lot of RAM, even up to 3X the size of the database, during the snapshotting. Although also true for small databases, this requirement becomes harder to fulfill the bigger the database grows. Secondly, the bigger the dataset is, the longer and harder it is to fork another process for snapshotting purposes, which directly affects the main server process.

This phenomenon is called “latency due to fork” and is explained [here](/blog/testing-fork-time-on-awsxen-infrastructure) and at [redis.io](https://redis.io/topics/latency). Let us assume, however, that the latter are non-issues and that by throwing enough hardware at it, you’ve gotten the master server enough resources so that creating the snapshot and forking latency are negligible efforts. Remember that after all the forking is done, the file needs to be copied from the master by the slave.

Regrettably, this is carried over the same interconnect that clients are using to the access database from. A large database, in most cases, is used by a lot of clients that generate a lot of traffic. Furthermore, in a cloud setup, the same network may also be used to access EBS-like network-attached storage as well. Adding a 10GB-worth of file transfer traffic to that transport medium hardly lessens any existing congestion. Quite the opposite, actually. Even assuming the existence of optimal network conditions, there are still physical limits to just how fast a chubby RDB file can travel through the wires and get written to local disks.

The bottom line is that, given these factors and the compounded effects they have, it takes time for the slave to get the file ready and in place for loading. And once in place, it also takes time for the slave to load the file. You don’t need detailed models or elaborate mathematical proofs to intuitively grasp the fact that the bigger your dataset is, the longer it will take to fork, dump, copy and load it into the slave.

“*But what of it?*” you may say, “*It’s not like I need to set up a new slave every day. I have the time, I can wait it out.*” **“You must unlearn what you have learned”** and wait you will, ad infinitum et ultra.

The slave will never finish synchronization and replication will not start. That is because while the snapshot was being created, hauled and loaded into the slave, time had passed during which the master was busy serving requests (and probably a lot of them in a big and busy database). Updates were accumulated in the dedicated replication buffer, but that buffer’s size is ultimately finite and, once exhausted, it can no longer be used to bring the slave up to date.

Without a valid updates buffer to catch-up from, the slave cannot complete the cycle of preliminary synchronization that is required to actively begin replicating updates from the master in real time. To rectify the situation, Redis’ behavior under these circumstances is to restart the slave’s synchronization process from scratch.

And so, the Apprentice goes back to square one, forgetting all that was learned so far and returns to the Master with a single request: “*I want to learn and to become like you.*” However, since the basic circumstances remain unchanged, successive attempts to kickstart the replication are in all likelihood doomed to the same fate as that of the initial iteration.

### A New Hope

This scenario, while rare, is real and may occur as originally brought up [here](https://groups.google.com/d/searchin/redis-db/master-slave$20replication$20goes$20into$20a$20loop/redis-db/-1ge4cnzPhg/6jAfGvVHWjwJ) by Manohar. Upcoming v2.8 Redis will definitely improve on it and in the future it is near-certain that the open-source community will overcome it completely. In the meantime, if you are looking for an immediate solution for it, you can visit our [github](https://github.com/Redis) to download our version of Redis 2.6.14. In this version we’ve included a client-throttling mechanism to tactfully buy enough time for the slave to complete synchronization. Our throttling mechanism works by introducing a delay to the master server’s responses to application clients’ requests. While appearing counterintuitive at first glance, the added delay provides just enough “breathing room” for the slave to finish the transfer and replay the updates log before the latter runs out of space, thus allowing synchronization to complete and replication begin.

In implementing this mechanism we have added the new configuration variable

```
slave-output-buffer-throttling

```

that is set using the following syntax:

```
CONFIG SET slave-output-buffer-throttling <low> <high> <rate> <delay>

```

where:

- <low> is a threshold value in bytes for the buffer’s size that, once crossed, activates the throttling
- <high> is the maximal size in bytes that the buffer will be allowed to reach until replication is started
- <rate> is the estimated rate of replication in bytes per second
- <delay> is the maximum forced delay given in milliseconds

So, for example, the following setting:

```
CONFIG SET slave-output-buffer-throttling 32768 131072 102400 1000

```

will cause the the replication process to be played out as before with these changes:

1. The Master forks itself, and
  1. The forked process dumps the dataset to a disk file (RDB)
  1. The main process continues serving client requests, but:
    1. As long as the buffer’s size is less than the <low> (e.g. 32768 bytes or 32MB) value, requests are handled normally
    1. Once the buffer’s size <low> threshold is crossed, the master estimates the time to complete the replication cycle and may force client throttling by adding up to a <delay> (e.g. 1000 milliseconds) to its responses
  1. Any changes made to the data are copied to a replication buffer on the main process

### “…Difficult to see. Always in motion is the future.”

The master’s estimate of time to complete the replication cycle is done as follows:

- The replication cycle is considered done after the dump has been created, fetched & processed by the slave and it is ready for online streaming of new updates.
- The master relies on the provided <rate> parameter as the effective replication volume that can be processed within one second.

In our example, let us assume the dataset’s size is 25GB. Given the rate of 100MB/s (or 102400 bytes/s) that we provided the setting

```javascript
slave-output-buffer-throttling
```

the master will estimate that the replication cycle will finish in 250 seconds (= 25GB / 100MB/s).

It will then initiate throttling by delaying responses if the replication buffer grows too fast. The <high> parameter determines the maximum allowed buffer size by the end of the replication process so throttling is triggered and applied proportionally at any point. That means that, for example, 125 seconds into the cycle the master will assume that it is 50% done. At that point the master will apply delays if the replication buffer’s size exceeds the 64MB mark (which is 50% of the <high> 131072 bytes value).

The actual delay introduced is in itself proportional to how much the buffer exceeds the limit, and won’t exceed the <delay> setting of 1000 ms to maintain server responsiveness. For the same reason, the server will never throttle the first request of new connections.

Lastly,

```javascript
slave-output-buffer-throttling
```

and the standard Redis

```javascript
client-output-buffer-limit
```

(read more [here](https://raw.github.com/antirez/redis/2.6/redis.conf)) mechanisms may be used in conjunction, so you would want to make sure they do not conflict. You can prevent such conflicts by setting

```javascript
client-output-buffer-limit
```

higher than the

```javascript
slave-output-buffer-throttling
```

For example:

```javascript
CONFIG SET client-output-buffer-limit 262144 131072 60
```

In this example, if the throttling does not succeed in restraining the buffer’s size – perhaps as the result of requests to create huge keys – then the standard

```javascript
client-output-buffer-limit
```

mechanism will kick in and break the cycle once it reaches 256MB or remains over the <high> 128MB limit for over 60 seconds.

We hope this explanation and solution is of use to some of you! May the force be with you.
