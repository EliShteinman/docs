---
title: "Redis Enterprise Flash on Intel Optane"
linkTitle: "Redis Enterprise Flash on Intel Optane"
url: "/blog/redis-enterprise-flash-intel-optane/"
description: "Our partners at Intel have recently announced the availability of Optane, an NVMe-based SSD device built on top of the new persistent memory technology from Intel and Micron, 3D XPoint (3DXP)."
date: 2017-08-08
blogCategories:
- "Company"
- "Tech"
authors:
- "Redis  "
lastmod: 2025-03-27
hidden: true
mirrored: true
---

*By Redis   · Published 8 August 2017 · updated 27 March 2025*

![Blog tile image](/images/site-mirror/150d3c2cc7560f1147b5b859fd87441ca00ede70-528x257.webp)

### Overview

Our partners at Intel have recently [announced the availability of Optane](https://download.intel.com/newsroom/2021/archive/2017-08-01-news-xps-alienware-systems-dell-intel-optane-memory.pdf), an NVMe-based SSD device built on top of the new persistent memory technology from Intel and Micron, 3D XPoint (3DXP).

### Intel Optane Technology

![](/images/site-mirror/150d3c2cc7560f1147b5b859fd87441ca00ede70-528x257.webp)

![](/images/site-mirror/8d9e52a2397cd2cc5eea6df50cf20bb845f4e15d-514x260.webp)

One of the main advantages of 3DXP is that it gives the application a way to decide which part of the dataset should be stored on fast memory, e.g. DRAM, and which part on a slower memory, e.g. Flash/Nand. Our Redis Enterprise Flash (RF) product was built from the ground-up with the same approach in mind.
We therefore decided to conduct an RF benchmark using Optane drives and compare the results with the benchmark we ran using the previous generation of Intel’s NVMe-based SSD, the [P3700](https://www.intel.com/content/www/us/en/products/memory-storage/solid-state-drives/data-center-ssds/dc-p3700-series.html). We knew that achieving better results with Optane would be challenging, as [RF had performed impressively with P3700](/docs/redis-on-flash-with-intel-nvme-benchmark/).

Before I get into the results of our benchmark, I’ll first cover some quick background about Redis and [Redis Enterprise Flash](/products/redis-pack/flash-memory/). Redis is known for its extremely fast performance, mainly because it serves datasets entirely from RAM. However, RAM prices have remained flat during recent years, and even deploying a dataset with only a few hundreds gigabytes can be very expensive (not to mention the cases wherein one or more replicas are needed for high-availability).

RF solves this problem by storing Redis’ keys, dictionary (the main data structure behind the keys) and “hot” values (the most accessible values) in RAM, while “cold” values (the less accessed part of the dataset) identified by the LRU algorithm are kept on Flash (the technology behind SSDs). Distributing the data this way guarantees that ongoing operations are executed almost as quickly as Redis on RAM.

This architecture is mainly designed for use cases in which the working dataset is smaller than the total dataset (which is the most common scenario), as it allows RF to maintain performance similar to that of RAM, while dramatically reducing the server’s infrastructure costs. RF is fully compatible with open-source Redis and incorporates the entire set of Redis commands and features. Flash is treated as a RAM extender and does not replace the existing data-persistence mechanism of Redis. With all of this in mind, let’s look into our latest performance tests on AWS.

### Test setup

We benchmarked the performance of Redis(e) Flash using the following setup:

1. 1000B **value (item) size**, covering most standard Redis use cases
1. 50%, 85% and 95% **RAM hit ratios** (i.e. the amount of requests served directly from RAM)
1. For each configuration we tested how many ops/sec could be achieved while maintaining **sub-millisecond** server latency (not including the network)

### Benchmark Results

The graph below show the 1000B results respectively for 50%, 85% and 95% RAM hit ratio.

![](/images/site-mirror/019520daea373a09196637e5719bf3044bffdd4e-980x566.webp)

### Performance Improvement

The table below summarizes the average improvement factor of the Intel Optane SSD compared to the Intel P3700 across all tests:

|  | 1000B |
|---|---|
| 50% RAM hit ratio | x9.2 |
| 85% RAM hit ratio | x9.7 |
| 95% RAM hit ratio | x2.8 |

#### Web UI of the throughput on 95% RAM hit ratio

![](/images/site-mirror/402db8bcd319edfb6a13531bdde17197271865cf-926x392.webp)

### Summary

The new Intel Optane SSD is a major improvement over the P3700 (especially for items larger than 1000B), delivering more than nine times the throughput using our RF product.

### Appendix

#### Hardware Server side

Intel(R) Xeon(R) CPU E5-2699 v4 @ 2.20GHz
2-sockets, 88 hardware threads, 44 cores (22 cores/socket)
128GB of memory (8GB DDR4 DIMMs at 2133 MHz)
4x Intel® Optane
Network: 10Gbps Ethernet

#### Software

OS – RHEL 7.0
[memtier_benchmark](https://github.com/RedisLabs/memtier_benchmark) version 1.2.6
Redis Enterprise version 4.5

Memtier command:
*./memtier_benchmark -s 192.168.22.14 -p 12320 –pipeline=20 -c 10 -t 20 -d 1000 –key-maximum=42949673 –key-pattern=G:G –key-stddev=1177484 –ratio=1:1 –distinct-client-seed –randomize –test-time=120 –run-count=1 –hide-histogram*
