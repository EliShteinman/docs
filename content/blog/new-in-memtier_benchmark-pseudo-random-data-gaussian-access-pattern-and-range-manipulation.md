---
title: "New in memtier_benchmark: Pseudo-Random Data, Gaussian Access Pattern and Range Manipulation"
linkTitle: "New in memtier_benchmark: Pseudo-Random Data, Gaussian Access Pattern and Range Manipulation"
url: "/blog/new-in-memtier_benchmark-pseudo-random-data-gaussian-access-pattern-and-range-manipulation/"
description: "Last year we open-sourced memtierbenchmark, a high-throughput benchmarking tool for Redis and Memcached resources. At Redis, we use this tool on a daily basis, and those of you who gave it a shot..."
date: 2014-07-08
blogCategories:
- "Tech"
authors:
- "Oran Agra"
lastmod: 2026-09-01
hidden: true
---

*By Oran Agra, Senior Software Architect at Redis Labs · Published 8 July 2014 · updated 1 September 2026*

![Blog tile image](/images/blog/0073e867b4e64f59de9047fdcde04295ba647e5c-772x550.webp)

![](/images/blog/2514d22fb5e530914e6cf102c0e8d8173b4aa393-250x158.webp)

Last year we [open-sourced memtier_benchmark](/blog/memtier_benchmark-a-high-throughput-benchmarking-tool-for-redis-memcached), a high-throughput benchmarking tool for Redis and Memcached resources. At Redis, we use this tool on a daily basis, and those of you who gave it a shot came back to us with great feedback. Based on these suggestions, we made several improvements to the project that I wanted to share with you today.

The first addition to our benchmarking tool is the generation of randomized data according to known size range. This is achieved by setting the new –data-size-pattern switch to the value ‘S’ (Sequential) and specifying its range with the –data-size-range switch. The following example will yield a benchmark keyspace whose values evenly range from 4 to 204 bytes values:

```
memtier-benchmark --random-data --data-size-range=4-204 --data-size-pattern=S --key-minimum=200 --key-maximum=400 <additional parameters>

```

In the example above, we’ve used the -–random-data switch to generate random data as well as the –key-minimum and –key-maximum switches to control the range of key name IDs, yielding a total of 200 keys. The first key, memtier-200, will hold 4 bytes of data, the next will have 5 bytes and so forth until the last key, memtier-400, which will store 204 bytes.

The next addition is the ability to use Gaussian (a.k.a normal) distribution to access the data. Before we made this change, you could specify a uniform random or sequential distribution for the benchmark’s access pattern. But to better mimic real-life use cases, this new option lets you conform the memtier_benchmark key access pattern to the familiar Gaussian distribution’s bell curve. When used, you can also control and set the standard deviation and median that the distribution will follow. For example, invoking the tool with the following arguments:

```
memtier-benchmark --random-data --data-size-range=4-204 --data-size-pattern=S --key-minimum=200 --key-maximum=400 --key-pattern=G:G --key-stddev=10 --key-median=300 <additional parameters>

```

will result in most read/write accesses being centered on the 100th (memtier-300) key.

Lastly, we’ve added the ability to use the [SETRANGE](https://redis.io/commands/setrange) and [GETRANGE](https://redis.io/commands/getrange) Redis commands in place of [SET](https://redis.io/docs/latest/commands/set/) and [GET](https://redis.io/docs/latest/commands/get/). This allows you to construct benchmarks that use significantly less network traffic while still using larger data sizes. For example, you can have key values of 1MB but only read and write the last byte with the following arguments:

```
memtier-benchmark --data-offset=1048575 --data-size=1 <additional parameters>

```

I hope you’ll find these new additions useful – if you want to share your memtier_benchmark input or war stories, feel free to do so directly in the project’s [GitHub repo](https://github.com/RedisLabs/memtier_benchmark).
