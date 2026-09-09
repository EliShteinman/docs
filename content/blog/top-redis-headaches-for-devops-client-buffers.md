---
title: "Top Redis Headaches for Devops – Client Buffers"
linkTitle: "Top Redis Headaches for Devops – Client Buffers"
url: "/blog/top-redis-headaches-for-devops-client-buffers/"
description: "Despite the setbacks that have been the cause of quite a few headaches, solutions do exist, and may be even simpler than anticipated."
date: 2014-07-28
blogCategories:
- "Tech"
authors:
- "Yaron Dolev"
lastmod: 2025-03-27
hidden: true
---

*By Yaron Dolev · Published 28 July 2014 · updated 27 March 2025*

![Blog tile image](/images/blog/0073e867b4e64f59de9047fdcde04295ba647e5c-772x550.webp)

Despite the setbacks that have been the cause of quite a few headaches, solutions do exist, and may be even simpler than anticipated.

This series of installments will highlight some of the most irritating issues that come up when using Redis, along with tips on how to solve them. They are based on our real-life experience of running thousands of Redis database instances.

Our previous installments in this series had discussed Redis’ replication [buffer](/blog/top-redis-headaches-for-devops-replication-buffer) and [timeouts](/blog/top-redis-headaches-for-devops-replication-timeouts). In this post we’ll fill you in on yet another type of buffer that Redis maintains, the client buffer. In some cases, this bugger may prove to be the cause of many headaches when left untamed.

## Client Buffers

You probably already know that Redis is an in-memory database, which means that all data is managed and served directly from RAM. This allows Redis to deliver unparalleled performance, serving tens and hundreds of thousands of requests at sub-millisecond latencies. RAM is by far the fastest means of storage that technology offers today – to get a sense of latency numbers, have a look at the following:

```python
Latency Comparison Numbers (~2012)
----------------------------------
L1 cache reference                           0.5 ns
Branch mispredict                            5   ns
L2 cache reference                           7   ns                      14x L1 cache
Mutex lock/unlock                           25   ns
Main memory reference                      100   ns                      20x L2 cache, 200x L1 cache
Compress 1K bytes with Zippy             3,000   ns        3 us
Send 1K bytes over 1 Gbps network       10,000   ns       10 us
Read 4K randomly from SSD*             150,000   ns      150 us          ~1GB/sec SSD
Read 1 MB sequentially from memory     250,000   ns      250 us
Round trip within same datacenter      500,000   ns      500 us
Read 1 MB sequentially from SSD*     1,000,000   ns    1,000 us    1 ms  ~1GB/sec SSD, 4X memory
Disk seek                           10,000,000   ns   10,000 us   10 ms  20x datacenter roundtrip
Read 1 MB sequentially from disk    20,000,000   ns   20,000 us   20 ms  80x memory, 20X SSD
Send packet CA->Netherlands->CA    150,000,000   ns  150,000 us  150 ms

Notes
-----
1 ns = 10^-9 seconds
1 us = 10^-6 seconds = 1,000 ns
1 ms = 10^-3 seconds = 1,000 us = 1,000,000 ns

Credit
------
By Jeff Dean:               http://research.google.com/people/jeff/
Originally by Peter Norvig: http://norvig.com/21-days.html#answers

Contributions
-------------
'Humanized' comparison:  https://gist.github.com/hellerbarde/2843375
Visual comparison chart: http://i.imgur.com/k0t1e.png

```

Redis, by name and design, is a remote server and that means that clients (usually) connect to it over a network. That being the case, a client’s request will take significantly more time to return to the client than the actual fetching of data from RAM by Redis’ CPU. The direct implication of this order of magnitude difference is that Redis would have been tied up serving the request for the duration of that time, had it not been for client buffers.

Client buffers make up a memory space that is allocated for serving client requests and every connection to Redis is allocated with its own buffer space. After processing a request, Redis copies the response data to the client buffer and proceeds to process subsequent requests, while the requesting client reads the data back over that connection at its own network-dictated pace. Redis’ client buffers are configured in the [redis.conf](https://download.redis.io/redis-stable/redis.conf) file by the client-output-buffer-limit normal directive (you can obtain this setting in runtime with a config get client-output-buffer-limit). The default redis.conf file defines it as follows:

```
client-output-buffer-limit normal 0 0 0

```

These values represent a buffer’s soft limit, hard limit, and timeout in seconds, respectively (similar to the behavior of [replication buffers](/blog/top-redis-headaches-for-devops-replication-buffer)). They serve as protection, where Redis will terminate the connection – without allowing the client to read the reply – when the buffer’s size reaches a) the soft limit and stays there until the timeout expires or b) the hard limit. Setting these limits to 0 means disabling that protection.

However, unlike replication buffers, memory allocation for client buffers is taken from Redis’ data memory space. The total amount of memory that Redis can use is set by the maxmemory directive and, once reached, Redis will employ its configured eviction policy (defined by the maxmemory-policy directive). This effectively means that slow performing clients and/or a large number of concurrent connections may cause your Redis instance to evict keys prematurely or deny updates with an out of memory message (OOM) because its memory usage, primarily being the sum of the dataset’s size and client buffers, had reached the memory’s limit.

Due to life’s relativity, a client doesn’t necessarily have to be slow to trigger this behavior. Because of the immense speed difference between accessing RAM and reading from the network, exhausting Redis’ memory with bloated client buffers is actually very easy to accomplish, even with top-performing clients and network links. Consider the (evil) [KEYS](https://redis.io/commands/keys) command, for example, once issued, Redis will copy the entire keys’ namespace to the client buffer. If your database has a significant number of keys, this alone would be sufficient to trigger eviction.

**Warning:** use KEYS with extreme caution and never on a production environment. Besides the possibility of triggering eviction as described above, by using it you risk blocking Redis for a significant period of time.

KEYS is not the only command that can cause this scenario, however. Similarly, Redis’ [SMEMBERS](https://redis.io/commands/smembers), [HGETALL](https://redis.io/commands/hgetall), [LRANGE](https://redis.io/commands/lrange) and [ZRANGE](https://redis.io/commands/zrange/) (and associated commands) may have the same effect if your values (and ranges) are large enough or, since every connection requires a separate buffer, if you have multiple open connections.

It is highly recommended, therefore, to refrain from using these commands irresponsibly. In their place the [SCAN](https://redis.io/commands/scan) family of commands is preferred, that have been available since v2.8. These commands not only allow Redis to continue processing requests between subsequent SCAN calls, but also reduce the chance of exhausting the client buffers.

Client buffers are an often overlooked aspect of Redis’ memory requirements and management. Their default setting of being disabled is quite risky, as it can quickly lead to running out of memory. By setting the buffers’ thresholds accordingly – taking the ’maxmemory’ setting into consideration, along with existing and predicted memory usage, and the application’s traffic patterns. Responsibly using the aforementioned commands can prevent unpleasant situations that will leave you with a throbbing headache. Stay tuned for our next installment in the Top Redis Headaches for Devops!
