---
title: "Talking to Redis: Clients, Configuration, and Performance Tuning"
linkTitle: "Talking to Redis: Clients, Configuration, and Performance Tuning"
url: "/tutorials/operate/redis-at-scale/talking-to-redis/"
description: "This tutorial is part of the Running Redis at Scale course. You can jump to any section:"
aliases:
- "/tutorials/operate-redis-at-scale-talking-to-redis/"
date: 2026-02-25
lastmod: 2026-02-26
hidden: true
---

*Published 25 February 2026 · updated 26 February 2026*

> **TL;DR:**
>
> To optimize Redis client communication, use connection pooling to reduce overhead, pipeline commands to cut network round trips, tune `maxclients`, `maxmemory`, and TCP backlog settings for your workload, and choose a client library that supports these features natively.

## Course Structure

This tutorial is part of the **Running Redis at Scale** course. You can jump to any section:

1. [Introduction to Running Redis at Scale](/tutorials/operate/redis-at-scale/)
2. **Talking to Redis** ← You are here
3. [Persistence and Durability](/tutorials/operate/redis-at-scale/persistence-and-durability/) - RDB and AOF
4. [High Availability](/tutorials/operate/redis-at-scale/high-availability/) - Replication and Sentinel
5. [Scalability](/tutorials/operate/redis-at-scale/scalability/) - Redis Cluster
6. [Observability](/tutorials/operate/redis-at-scale/observability/) - Metrics and troubleshooting
7. [Course Conclusion](/tutorials/operate/redis-at-scale/course-wrap-up/)

---

In this tutorial, you'll learn how to communicate with Redis effectively. We cover the Redis server architecture, command-line tools, configuration options, client libraries, and performance tuning.

## What you'll learn

- How the Redis server processes requests and where multi-threaded I/O fits in
- How to use `redis-cli` productively with tab completion and command history
- How to configure Redis at startup and reconfigure it at runtime
- How connection pooling reduces connection overhead and boosts throughput
- How pipelining batches commands to minimize network round-trip latency
- Key tuning parameters (`maxclients`, `maxmemory`, TCP backlog, kernel settings) for running Redis at scale

---

[YouTube: https://www.youtube.com/watch?v=GnVvrLF7oeE](https://www.youtube.com/watch?v=GnVvrLF7oeE)

## Redis Server Overview

As you might already know, Redis is an open source data structure server written in C. You can store multiple data types, like strings, hashes, and streams and access them by a unique key name.

For example, if you have a string value "Hello World" saved under the key name "greeting", you can access it by running the **GET** command followed by the key name - greeting. All keys in a Redis database are stored in a flat keyspace. There is no enforced schema or naming policy, and the responsibility for organizing the keyspace is left to the developer.

The speed Redis is famous for is mostly due to the fact that Redis stores and serves data entirely from RAM instead of disk, as most other databases do. Another contributing factor is its predominantly single-threaded nature: single-threading avoids race conditions and CPU-heavy context switching associated with threads.

Indeed, this means that open source Redis can't take advantage of the processing power of multiple CPU cores, although CPU is rarely the bottleneck with Redis. You are more likely to bump up against memory or network limitations before hitting any CPU limitations. That said, Redis Cloud does let you take advantage of all of the cores on a single machine.

Let's now look at exactly what happens behind the scenes with every Redis request. When a client sends a request to a Redis server, the request is first read from the socket, then parsed and processed and finally, the response is written back to the socket and sent to the user. The reading and especially writing to a socket are expensive operations, so in Redis version 6.0 multi-threaded I/O was introduced. When this feature is enabled, Redis can delegate the time spent reading and writing to I/O sockets over to other threads, freeing up cycles for storing and retrieving data and boosting overall performance by up to a factor of two for some workloads.

---

## The Redis Command Line Tool

[YouTube: https://www.youtube.com/watch?v=VenGyryG4OE&t=1s](https://www.youtube.com/watch?v=VenGyryG4OE&t=1s)

Redis-cli is a command line tool used to interact with the Redis server. Most package managers include redis-cli as part of the redis package. It can also be compiled from source, and you'll find the source code in the Redis repository on GitHub.

There are two ways to use redis-cli:

- an interactive mode where the user types commands and sees the replies;
- a command mode where the command is provided as an argument to redis-cli, executed, and results sent to the standard output.

Let's use the CLI to connect to a Redis server running at 172.22.0.3 and port 7000. The arguments -h and -p are used to specify the host and port to connect to. They can be omitted if your server is running on the default host "localhost" port 6379.

The redis-cli provides some useful productivity features. For example, you can scroll through your command history by pressing the up and down arrow keys. You can also use the TAB key to autocomplete a command, saving even more keystrokes. Just type the first few letters of a command and keep pressing TAB until the command you want appears on screen.

Once you have the command name you want, the CLI will display syntax hints about the arguments so you don't have to remember all of them, or open up the Redis command documentation.

These three tips can save you a lot of time and take you a step closer to being a power user.

You can do much more with redis-cli, like sending output to a file, scanning for big keys, get continuous stats, monitor commands and so on. For a much more detailed explanation refer to the [documentation](https://redis.io/docs/latest/develop/tools/cli/).

---

## Configuring a Redis Server

The self-documented Redis configuration file called `redis.conf` has been mentioned many times as an example of well written documentation. In this file you can find all possible Redis configuration directives, together with a detailed description of what they do and their default values.

You should always adjust the `redis.conf` file to your needs and instruct Redis to run based on it's parameters when running Redis in production.

The way to do that is by providing the path to the file when starting up your server:

```bash
redis-server ./path/to/redis.conf
```

When you're only starting a Redis server instance for testing purposes you can pass configuration directives directly on the command line:

```bash
redis-server --port 7000 --replicaof 127.0.0.1:6379
```

The format of the arguments passed via the command line is exactly the same as the one used in the redis.conf file, with the exception that the keyword is prefixed with `--`.

Note that internally this generates an in-memory temporary config file where arguments are translated into the format of `redis.conf`.

It is possible to reconfigure a running Redis server without stopping or restarting it by using the special commands `CONFIG SET` and `CONFIG GET`.

```bash
127.0.0.1:6379> CONFIG GET *

127.0.0.1:6379> CONFIG SET something

127.0.0.1:6379> CONFIG REWRITE
```

Not all the configuration directives are supported in this way, but you can check the output of the command `CONFIG GET *` first for a list of all the supported ones.

> **TIP**
>
> Modifying the configuration on the fly has no effect on the `redis.conf` file. At the next restart of Redis the old configuration will be used instead. If you want to force update the `redis.conf` file with your current configuration settings you can run the `CONFIG REWRITE` command, which will automatically scan your `redis.conf` file and update the fields which don't match the current configuration value.

---

## Redis Clients

[YouTube: https://www.youtube.com/watch?v=2LRXM6ELhFw&t=2s](https://www.youtube.com/watch?v=2LRXM6ELhFw&t=2s)

Redis has a client-server architecture and uses a request-response model. Apps send requests to the Redis server, which processes them and returns responses for each. The role of a Redis client library is to act as an intermediary between your app and the Redis server.

Client libraries perform the following duties:

- Implement the Redis wire protocol - the format used to send requests to and receive responses from the Redis server
- Provide an idiomatic API for using Redis commands from a particular programming language

### Managing the Connection to Redis

Redis clients communicate with the Redis server over TCP, using a protocol called [RESP](https://redis.io/docs/latest/develop/reference/protocol-spec/) (REdis Serialization Protocol) designed specifically for Redis.

The RESP protocol is simple and text-based, so it is easily read by humans, as well as machines. A common request/response would look something like this. Note that we're using netcat here to send raw protocol:

This simple, well documented protocol has resulted in Redis clients for almost every language you can think of. The [redis.io](https://redis.io/docs/latest/develop/clients/) client page lists over 200 client libraries for more than 50 programming languages.

To get started with a specific language, see these tutorials:

- [Getting Started with Node.js and Redis](/tutorials/develop/node/gettingstarted/)
- [Getting Started with Java and Redis](/tutorials/develop/java/getting-started/)

---

## Client Performance Improvements

### How does connection pooling work in Redis?

Redis clients are responsible for managing connections to the Redis server. Creating and recreating new connections over and over again, creates a lot of unnecessary load on the server. A good client library will offer some way of optimizing connection management, by setting up a connection pool, for example. With connection pooling, the client library will instantiate a series of (persistent) connections to the Redis server and keep them open. When the app needs to send a request, the current thread will get one of these connections from the pool, use it, and return it when done.

![Diagram showing connection pooling between an application and Redis](/images/site-mirror/11f851c5752b3777aec1b5a912c0066db4195644-817x386.webp)

So if possible, always try to choose a client library that supports pooling connections, because that decision alone can have a huge influence on your system's performance.

### What is Redis pipelining?

As in any client-server app, Redis can handle many clients simultaneously. Each client does a (typically blocking) read on a socket and waits for the server response. The server reads the request from the socket, parses it, processes it, and writes the response to the socket. The time the data packets take to travel from the client to the server, and then back again, is called network round trip time, or **RTT**. If, for example, you needed to execute 50 commands, you would have to send a request and wait for the response 50 times, paying the **RTT** cost every single time. To tackle this problem, Redis can process new requests even if the client hasn't already read the old responses. This way, you can send multiple commands to the server without waiting for the replies at all; the replies are read in the end, in a single step.

![Diagram explaining Redis pipelining to reduce round-trip time](/images/site-mirror/9fe996c7062ecc38ba13b4dc4bcdbdbf8951e18e-993x649.webp)

This technique is called pipelining and is another good way to improve the performance of your system. Most Redis libraries support this technique out of the box.

#### Supplemental reading about Redis pipelining

- [Redis Pipelining](https://redis.io/topics/pipelining)
- [Redis Client Handling](https://redis.io/topics/clients)
- [Connection Pools for Serverless Functions and Backend Services](https://redislabs.com/blog/connection-pools-for-serverless-functions-and-backend-services/)

---

## Initial Tuning

We love Redis because it's fast (and fun!), so as we begin to consider scaling out Redis, we first want to make sure we've done everything we can to maximize its performance.

Let's start by looking at some important tuning parameters.

### Max Clients

Redis has a default of max of 10,000 clients; after that maximum has been reached, Redis will respond to all new connections with an error. If you have a lot of connections (or a lot of app instances), then you may need to go higher. You can set the max number of simultaneous clients in the Redis config file:

```bash
maxclients 20000
```

### Max Memory

By default, Redis has no max memory limit, so it will use all available system memory. If you are using replication, you will want to limit the memory usage in order to have overhead for replica output buffers. It's also a good idea to leave memory for the system. Something like 25% overhead. You can update this setting in Redis config file:

```bash
# memory size in bytes
maxmemory 1288490188
```

### Set TCP-BACKLOG

The Redis server uses the value of `tcp-backlog` to specify the size of the complete connection queue.

Redis passes this configuration as the second parameter of the `listen(int s, int backlog)` call.

If you have many connections, you will need to set this higher than the default of 511. You can update this in Redis config file:

```bash
# TCP listen() backlog.
#
# In high requests-per-second environments you need an high backlog in order
# to avoid slow clients connections issues. Note that the Linux kernel
# will silently truncate it to the value of /proc/sys/net/core/somaxconn so
# make sure to raise both the value of somaxconn and tcp_max_syn_backlog
# in order to get the desired effect.
tcp-backlog 65536
```

As the comment in `redis.conf` indicates, the value of `somaxconn` and `tcp_max_syn_backlog` may need to be increased at the OS level as well.

### Set Read Replica Configurations

One simple way to scale Redis is to add read replicas and take load off of the primary. This is most effective when you have a read-heavy (as opposed to write-heavy) workload. You will probably want to have the replica available and still serving stale data, even if the replication is not completed. You can update this in the Redis config:

```bash
slave-serve-stale-data yes
```

You will also want to prevent any writes from happening on the replicas. You can update this in the Redis config:

```bash
slave-read-only yes
```

### Kernel Memory

Under high load, occasional performance dips can occur due to memory allocation. This is something Salvatore, the creator of Redis, blogged about in the past. The performance issue is related to transparent hugepages, which you can disable at the OS level if needed.

```bash
echo 'never' > /sys/kernel/mm/transparent_hugepage/enabled
```

### Kernel Network Stack

If you plan on handling a large number of connections in a high performance environment, we recommend tuning the following kernel parameters:

```bash
vm.swappiness=0                       # turn off swapping
net.ipv4.tcp_sack=1                   # enable selective acknowledgements
net.ipv4.tcp_timestamps=1             # needed for selective acknowledgements
net.ipv4.tcp_window_scaling=1         # scale the network window
net.ipv4.tcp_congestion_control=cubic # better congestion algorithm
net.ipv4.tcp_syncookies=1             # enable syn cookies
net.ipv4.tcp_tw_recycle=1             # recycle sockets quickly
net.ipv4.tcp_max_syn_backlog=NUMBER   # backlog setting
net.core.somaxconn=NUMBER             # up the number of connections per port
net.core.rmem_max=NUMBER              # up the receive buffer size
net.core.wmem_max=NUMBER              # up the buffer size for all connections
```

### File Descriptor Limits

If you do not set the correct number of file descriptors for the Redis user, you will see errors indicating that "Redis can't set maximum open files.." You can increase the file descriptor limit at the OS level.

Here's an example on Ubuntu using systemd:

```bash
/etc/systemd/system/redis.service
[Service]
...
User=redis
Group=redis
...
LimitNOFILE=65536
...
```

You will then need to reload the daemon and restart the redis service.

### Enabling RPS (Receive Packet Steering) and CPU Preferences

One way we can improve performance is to prevent Redis from running on the same CPUs as those handling any network traffic. This can be accomplished by enabling RPS for our network interfaces and creating some CPU affinity for our Redis process.

Here is an example. First we can enable RPS on CPUs 0-1:

```bash
echo '3' > /sys/class/net/eth1/queues/rx-0/rps_cpus
```

Then we can set the CPU affinity for redis to CPUs 2-8:

```bash
# config is set to write pid to /var/run/redis.pid
$ taskset -pc 2-8 `cat /var/run/redis.pid`
pid 8946's current affinity list: 0-8
pid 8946's new affinity list: 2-8
```

---

## Next steps

Now that you understand how to communicate with Redis and tune client performance, continue with the course or explore related topics:

- **Next in this course:** [Persistence and Durability](/tutorials/operate/redis-at-scale/persistence-and-durability/) — learn about RDB snapshots and AOF for data safety
- **Dive deeper into clients:** [Getting Started with Node.js and Redis](/tutorials/develop/node/gettingstarted/) or [Getting Started with Java and Redis](/tutorials/develop/java/getting-started/)
- **Redis CLI reference:** [redis-cli documentation](https://redis.io/docs/latest/develop/tools/cli/)
- **Pipelining deep-dive:** [Redis Pipelining](https://redis.io/docs/latest/develop/use/pipelining/)
