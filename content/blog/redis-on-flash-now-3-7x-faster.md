---
title: "Redis on Flash: Now 3.7x Faster with New Data Engine and Amazon EC2 I4i Instances"
linkTitle: "Redis on Flash: Now 3.7x Faster with New Data Engine and Amazon EC2 I4i Instances"
url: "/blog/redis-on-flash-now-3-7x-faster/"
description: "Redis on Flash (RoF) has been one of our most popular enterprise functionalities, making in-memory computing cost-effective by storing up to 80% of the datasets in SSD rather than expensive DRAM,..."
date: 2022-05-03
blogCategories:
- "Company"
- "Product Releases"
authors:
- "Alon Magrafta"
- "Filipe Oliveira"
lastmod: 2025-07-03
hidden: true
---

*By Alon Magrafta, Filipe Oliveira · Published 3 May 2022 · updated 3 July 2025*

![Blog tile image](/images/blog/f64e4e2b5e596c17c9c33b3cf34524dde294e9b8-772x550.webp)

[Redis on Flash (RoF)](/redis-enterprise/technology/redis-on-flash/) has been one of our most popular enterprise functionalities, making in-memory computing cost-effective by storing up to 80% of the datasets in SSD rather than expensive DRAM, and while still keeping the sub-millisecond latency and high-throughput of Redis. In typical deployments, RoF provides up to 70% TCO discount.

Now with two new, exciting collaborations, we’re proud to announce RoF can now **deliver up to 3.7x the performance** while maintaining the same attractive total cost of ownership for running large datasets on Redis. First, AWS has announced the general availability of a new generation of instances, [Amazon EC2 I4i](https://aws.amazon.com/ec2/instance-types/i4i/), powered by 3rd generation Intel Xeon Scalable processors (code-named Ice Lake) and AWS Nitro SSD NVMe-based storage. This new generation promises to deliver a remarkable increase in performance for data-intensive Redis customers. Additionally, we’re pleased to share our plans to open the data engine for RoF to any RocksDB compatible database, with the newly announced technology from Speedb, as the first option.

We believe the combination of the new I4i instances and providing customers a choice for their data engine will make RoF even more attractive for massive datasets, as the need for real-time experiences increases for companies building modern applications or low latency microservice architectures.

## What do Amazon EC2 I4i and Speedb bring to Redis on Flash?

Let’s dive into what’s new on RoF. AWS is offering the [new Amazon EC2 I4i (the ‘i’ is for Intel) instances](https://aws.amazon.com/ec2/instance-types/i4i/) across 4 regions. The I4i instances use the latest technology, Intel Ice Lake processors and AWS Nitro SSD, which improves IOPS and reduces latencies compared to the previous generation of I3 instances.

Separately from the hardware, we’ve been looking for ways that RoF can deliver even greater performance and identified an opportunity to open the data engine to innovation by customers and entrepreneurs. We’re pleased to announce that RoF is now open to any [RocksDB](http://rocksdb.org/)-compatible data engine and Speedb is the first alternative to be offered by Redis. Working with us, the team at Speedb has redesigned the RocksDB internal data structure which impressively increases both performance and scale while reducing CPU resources.

In this blog post, we share how Speedb provides a significant performance boost of almost 50% at our sub-millisecond tests compared to RocksDB, regardless of which AWS EC2 instance we were using, the I4i or the I3.

RoF with Speedb is currently available in private preview. Redis customers can contact their account team for additional information or to trial the new service.

## Benchmarking the new Redis on Flash

Our performance engineers couldn’t wait to get their hands on the AWS’ I4i instances and test them with RoF’s new Speedb data engine. We are pleased to be the first AWS partner to thoroughly test the Amazon EC2 I4i instances. As a reminder, RoF intelligently tiers large datasets and was designed to take advantage of lower-priced per GiB of NVMe SSDs compared to DRAM. This enables us to deliver Redis-grade performance, now even faster with the I4i instances, at 30% total cost-of-ownership of DRAM-based instances.

Before getting to benchmark results and numbers, let’s review when a customer should consider RoF. We developed RoF for use cases where the working dataset is smaller than the total dataset and moving to additional DRAM is cost-prohibitive. Another common RoF use case is batch data processing, where huge amounts of data need to be processed for business-critical applications, that require steady low latency and high throughput over time.

Now to the fun part, the benchmark results.

## What we benchmarked

### We compared the performance of Redis on Flash over four AWS instances:

i3.8xlarge – 244GB RAM, 4xNVMe SSD drives, for a total 7.6TB
I4i.4xlarge – 128GB RAM, 1xNVMe SSD drives, for a total 3.75TB
I4i.8xlarge – 256GB RAM, 2xNVMe SSD drives, for a total 7.5TB
I4i.16xlarge – 512GB RAM, 4xNVMe SSD drives for a total 15TB

### We compared the performance of two data engines

- RocksDB
- Speedb

### Test parameters

We used 1KiB value sizes, covering most standard Redis use cases
We tested 50% and 85% RAM hit ratios (i.e. many requests served directly from RAM)
We tested 20:80 RAM:Flash ratio
We benchmarked various read:write ratios: 1:1, 4:1 and 1:4
All tests were done using two servers
The following are the database sizes that we run according to the instances types:

- I4i.4xlarge: 500GB + replication. 5 Primary shards + 5 Replica shards
- i3.8xlarge: 1TB + replication. 10 Primary shards + 10 Replica shards
- I4i.8xlarge: 1TB + replication. 10 Primary shards + 10 Replica shards
- I4i.16xlarge: 2TB + replication. 20 Primary shards + 20 Replica shards

In each configuration, we tested how many ops/sec could be achieved while keeping sub-millisecond client latency (not including the network)

### What we found

The graph below shows the i3 vs the I4i and RocksDB vs Speedb:

![](/images/blog/7dccb8cad5c5f17299bfb5f15c532bc603973b5a-600x371.webp)

We can see the following improvements:

| From | to | Speedup factor |
|---|---|---|
| i3.8xlarge rocksdb | i3.8xlarge speedb | 1.3x |
| I4i.8xlarge rocksdb | I4i.8xlarge speedb | 1.46x |
| i3.8xlarge rocksdb | I4i.8xlarge rocksdb | 1.94x |
| i3.8xlarge speedb | I4i.8xlarge speedb | 2.16x |
| i3.8xlarge rocksdb | I4i.8xlarge speedb | 2.83x |

The graph below shows scaling with I4i on Speedb and different read:write ratios:

![](/images/blog/55634bd27da8df0bf2516ce1747be4ad65e13b1c-782x483.webp)

We can see the following results and improvements:

Scaling wise, we can see that RoF on I4i with Speedb scales almost linearly.

4xlarge → 8xlarge has a factor of ~1.55x-1.8x
8xlarge → 16xlarge has a scaling factor of ~1.85x-1.95x

A second notable result is that RoF on I4i with Speedb is very agnostic to the application access pattern (the read:write ratio). That means performance stays steady and is predictable. That can be useful when working with multiple different applications or when the access pattern varies over time.

The graph below shows the overall 3.7x performance improvement:

![](/images/blog/51dcbec5a8163f7cc2ca739a94be21070ade40ba-600x371.webp)

**Appendix:**
**Benchmark setup**

Redis Enterprise version: v. 6.2.8-39 on Ubuntu 18.04
Redis on Flash database: see details per instance above
Client machine: EC2 m5.8xlarge (32 VCPUs, 128 GB RAM)
Load Generation tool: memtier benchmark

Memtier sample command for 85% ram hit ratio:
memtier_benchmark -s <database host IP> -p <database port>
–hide-histogram –pipeline=1 -c 4 -t 256 -d 1000
–key-maximum=771141855 –key-pattern=G:G –key-stddev=50358491
–ratio=1:1 –distinct-client-seed –randomize –test-time=1200

Setup illustration:

![](/images/blog/11057be57e247f70c5319a5e08b6a2214ba82898-1024x653.webp)

---
