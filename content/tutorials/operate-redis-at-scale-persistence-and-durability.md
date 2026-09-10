---
title: "Redis Persistence and Durability: RDB Snapshots & AOF"
linkTitle: "Redis Persistence and Durability: RDB Snapshots & AOF"
url: "/tutorials/operate/redis-at-scale/persistence-and-durability/"
description: "This tutorial is part of the Running Redis at Scale course. You can jump to any section:"
group: "For operators"
aliases:
- "/tutorials/operate-redis-at-scale-persistence-and-durability/"
date: 2026-02-25
lastmod: 2026-02-26
hidden: true
---

*Published 25 February 2026 · updated 26 February 2026*

> **TL;DR:**
>
> Redis stores data in memory but can persist it to disk using two mechanisms: **RDB snapshots** (periodic point-in-time dumps) and **AOF** (append-only log of every write command). RDB is compact and fast for backups but risks losing recent writes; AOF is more durable but produces larger files. You can combine both for a hybrid persistence strategy that balances performance with data safety.

## Course Structure

This tutorial is part of the **Running Redis at Scale** course. You can jump to any section:

1. [Introduction to Running Redis at Scale](/tutorials/operate/redis-at-scale/)
2. [Talking to Redis](/tutorials/operate/redis-at-scale/talking-to-redis/) - CLI, clients, and tuning
3. **Persistence and Durability** ← You are here
4. [High Availability](/tutorials/operate/redis-at-scale/high-availability/) - Replication and Sentinel
5. [Scalability](/tutorials/operate/redis-at-scale/scalability/) - Redis Cluster
6. [Observability](/tutorials/operate/redis-at-scale/observability/) - Metrics and troubleshooting
7. [Course Conclusion](/tutorials/operate/redis-at-scale/course-wrap-up/)

---

## What you'll learn

- How RDB snapshots and AOF persistence work under the hood
- The durability trade-offs between RDB, AOF, and hybrid persistence
- How to configure Redis persistence using `redis.conf` and live `CONFIG SET` commands
- How to verify that your data survives a server restart
- When to choose RDB vs AOF based on your backup strategy and recovery requirements

---

[YouTube: https://www.youtube.com/watch?v=FzXp4CkxgzU](https://www.youtube.com/watch?v=FzXp4CkxgzU)

As you know, Redis serves all data directly from memory. But Redis is also capable of persisting data to disk. Persistence preserves data in the event of a server restart.

In this tutorial, we'll look at the options for persisting data to disk. You'll learn about RDB snapshots and AOF (Append-Only File), and then do a hands-on exercise setting up persistence for your Redis instance.

---

## How does Redis persist data?

[YouTube: https://www.youtube.com/watch?v=08V8KeXhZY4](https://www.youtube.com/watch?v=08V8KeXhZY4)

If a Redis server that only stores data in RAM is restarted, all data is lost. To prevent such data loss, there needs to be some mechanism for persisting the data to disk; Redis provides two of them: **RDB snapshotting** and an **append-only file (AOF)**. You can configure your Redis instances to use either of the two, or a combination of both (hybrid persistence).

### RDB vs AOF comparison

| Feature             | RDB Snapshots                                   | AOF (Append-Only File)                      |
| ------------------- | ----------------------------------------------- | ------------------------------------------- |
| **How it works**    | Periodic point-in-time dump of the full dataset | Logs every write command as it happens      |
| **File format**     | Compact binary `.rdb` file                      | Human-readable command log                  |
| **Data loss risk**  | All writes since last snapshot                  | Depends on fsync policy (none to ~1 second) |
| **Restart speed**   | Fast (load a single binary file)                | Slower (replay all logged commands)         |
| **Disk I/O impact** | High during snapshot (fork + write)             | Continuous but smaller writes               |
| **File size**       | Smaller (compressed)                            | Larger (grows until rewrite)                |
| **Best for**        | Backups, disaster recovery, cloning             | Maximum durability, audit trails            |

### What are RDB snapshots?

When a snapshot is created, the entire point-in-time view of the dataset is written to persistent storage in a compact **.rdb** file. You can set up recurring backups, for example every 1, 12, or 24 hours and use these backups to easily restore different versions of the data set in case of disasters. You can also use these snapshots to create a clone of the server, or simply leave them in place for a future restart.

Creating a .rdb file requires a lot of disk I/O. If performed in the main Redis process, this would reduce the server's performance. That's why this work is done by a forked child process. But even forking can be time-consuming if the dataset is large. This may result in decreased performance or in Redis failing to serve clients for a few milliseconds or even up to a second for very large datasets. Understanding this should help you decide whether this solution makes sense for your requirements.

You can configure the name and location of the .rdb file with the **dbfilename** and **dir** configuration directives, either through the **redis.conf** file, or through the redis-cli as explained in [Talking to Redis](/tutorials/operate/redis-at-scale/talking-to-redis/). And of course you can configure how often you want to create a snapshot.

As an example, this configuration will make Redis automatically dump the dataset to disk every 60 seconds if at least 1000 keys changed in that period. While snapshotting is a great strategy for the use cases explained above, it leaves a huge possibility for data loss. You can configure snapshots to run every few minutes, or after X writes against the database, but if the server crashes you lose all the writes since the last snapshot was taken. In many use cases, that kind of data loss can be acceptable, but in many others it is absolutely not. For all of those other use cases Redis offers the AOF persistence option.

### What is the Append-Only File (AOF)?

AOF, or append-only file works by logging every incoming write command to disk as it happens. These commands can then be replayed at server startup, to reconstruct the original dataset. Commands are logged using the same format as the Redis protocol itself, in an append-only fashion. The AOF approach provides greater durability than snapshotting, and allows you to configure how often file syncs happen.

### Which AOF fsync policy should you use?

Depending on your durability requirements (or how much data you can afford to lose), you can choose which fsync policy is the best for your use case:

- **fsync every write** (`appendfsync always`): The safest policy: The write is acknowledged to the client only after it has been written to the AOF file and flushed to disk. Since in this approach we are writing to disk synchronously, we can expect a much higher latency than usual.
- **fsync every second** (`appendfsync everysec`): The default policy. Fsync is performed asynchronously, in a background thread, so write performance is still high. Choose this option if you need high performance and can afford to lose up to one second worth of writes.
- **no fsync** (`appendfsync no`): In this case Redis will log the command to the file descriptor, but will not force the OS to flush the data to disk. If the OS crashes we can lose a few seconds of data (Normally Linux will flush data every 30 seconds with this configuration, but it's up to the kernel's exact tuning.).

The relevant configuration directives for AOF are shown on the screen. AOF contains a log of all the operations that modified the database in a format that's easy to understand and parse. When the file gets too big, Redis can automatically rewrite it in the background, compacting it in a way that only the latest state of the data is preserved.

### Can you use both RDB and AOF together?

Yes. Redis supports **hybrid persistence**, where both RDB and AOF are enabled simultaneously. In this configuration, Redis uses the AOF for durability during normal operation and can still produce RDB snapshots for backups and faster restarts. When both are present at startup, Redis loads the AOF because it is typically more complete. This hybrid approach gives you the best of both worlds: the fast recovery of RDB combined with the write-by-write durability of AOF. For most production deployments, enabling both is the recommended Redis backup strategy.

---

## Exercise: Configuring Persistence

By default, Redis will save a snapshot of your database every hour if at least one key has changed, every five minutes if at least 100 keys have changed, or every 60 seconds if at least 10000 keys have changed.

Let's update this to a simplified hypothetical scenario where we want to save a snapshot if three keys have been modified in 20 seconds.

### Step 1: Create a Configuration File

Create a directory named 2.2 and in it prepare a `redis.conf` file.

```bash
mkdir 2.2
cd 2.2
vim redis.conf
```

The `redis.conf` file should specify a filename that will be used for the rdb file and a directive that will trigger the creation of a snapshot if 3 keys have been modified in 20 seconds, as described above.

```bash
dbfilename my_backup_file.rdb
save 20 3
```

### Step 2: Start Redis with RDB Snapshots

In the 2.2 directory, start a Redis server - passing it the `redis.conf` configuration file you just created.

```bash
redis-server ./redis.conf
```

In a separate terminal tab use the `redis-cli` to create three random keys, one after the other. For example:

```bash
127.0.0.1:6379> SET a 1
127.0.0.1:6379> SET b 2
127.0.0.1:6379> SET c 3
```

Run the `ls` command in the first terminal to list all the files in the 2.2 directory. What changed?

### Step 3: Enable AOF Persistence

Now we're ready to take our persistence a level higher and set up an `AOF` file. Modify your `redis.conf` file so that the server will log every new write command and force writing it to disk.

Be careful! We have a running server and we want this configuration to be applied without restarting it.

```bash
127.0.0.1:6379> CONFIG SET appendonly yes
127.0.0.1:6379> CONFIG SET appendfsync always
```

In order for these settings to be persisted to the `redis.conf` file we need to save them:

```bash
127.0.0.1:6379> CONFIG REWRITE
```

### Step 4: Verify AOF is Working

Create a few random keys through `redis-cli`. Check the contents of the directory 2.2 again. What changed?

### Step 5: Test Persistence After Restart

As a final step, restart the Redis server process (you can press Ctrl+C in the terminal to stop the process and re-run it again). If you run the `SCAN 0` command you will see that all the keys you created are still in the database, even though we restarted the process.

---

## Next steps

Now that you understand how to protect your data with Redis persistence, the next step is ensuring your Redis deployment stays available even when servers fail.

- **[High Availability →](/tutorials/operate/redis-at-scale/high-availability/)**: Learn how replication and Redis Sentinel provide automatic failover so your data remains accessible even if the primary server goes down.
- **[Scalability](/tutorials/operate/redis-at-scale/scalability/)**: Explore Redis Cluster to distribute data across multiple nodes and scale beyond the limits of a single server.
- **[Observability](/tutorials/operate/redis-at-scale/observability/)**: Monitor your Redis instances to catch persistence issues, replication lag, and memory pressure before they impact your users.
