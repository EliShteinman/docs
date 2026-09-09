---
title: "AWS I3 instances are x2.6 faster and 80% cheaper with Redis Flash"
linkTitle: "AWS I3 instances are x2.6 faster and 80% cheaper with Redis Flash"
url: "/blog/redis-flash-double-performance-nvme/"
description: "Recently, AWS announced the availability of I3 instances across 15 different regions. We were happy to be a part of their I3 instances beta program and used our own Redis Enterprise Flash (Redise..."
date: 2017-04-05
blogCategories:
- "Company"
- "Tech"
authors:
- "Redis  "
lastmod: 2025-03-27
hidden: true
---

*By Redis   · Published 5 April 2017 · updated 27 March 2025*

![Blog tile image](/images/blog/eb513320eb68e9cda9d3d86406e81fc846ad9901-950x369.webp)

Recently, AWS announced the availability of I3 instances across 15 different regions. We were happy to be a part of their [I3 instances](https://aws.amazon.com/blogs/aws/now-available-i3-instances-for-demanding-io-intensive-applications/) beta program and used our own Redis Enterprise Flash (Redise Flash) technology to extensively test and benchmark the new instances before they were formally launched. The I3 SSD storage is based on [NVMe](https://en.wikipedia.org/wiki/NVM_Express) technology, which theoretically should provide significantly higher throughput and much lower latency than the previous generation I2 instances (which are based on SATA SSDs).

Before I get into the results of our benchmark, I’ll first cover some quick background about Redis and [Redise Flash](/products/redis-pack/flash-memory/). Redis is known for its extremely fast performance serving datasets entirely from RAM. However, RAM prices have remained flat during recent years, and deploying large datasets may prove to be expensive and may not fit all business models and economics (not to mention the cases where one or more replicas are needed for high-availability).

[Redise Flash](/products/redis-pack/flash-memory/) solves this problem by storing Redis’ keys, dictionary (the main data structure behind the keys), and “hot” values (the most accessed values) in RAM, while “cold” values (the least accessed part of the dataset as identified by the LRU algorithm) are kept on Flash (the technology behind SSDs). Distributing the data this way guarantees that ongoing operations are executed almost as quickly as Redis running entirely on RAM.

This architecture is mainly designed for use cases where the working dataset is smaller than the total dataset (which is the most common scenario), as it allows Redise Flash to maintain a similar performance to that of RAM while dramatically reducing the server infrastructure costs. Redise Flash is fully compatible with open-source Redis and incorporates the entire set of Redis commands and features. Flash is treated as a RAM extender, and does not replace the existing data-persistence mechanism of Redis. With all of this in mind, let’s look into our latest performance tests on AWS.

**What We Benchmarked**
We compared the performance of Redise Flash over three AWS instances:

1. i2.8xlarge – 244GB RAM, 8xSATA SSD drives and total 6.4TB, with 365K/315K read/write IOPS
1. i3.8xlarge – 244GB RAM, 4xNVMe SSD drives and total 7.6TB, with 1.65M/150K read/write IOPS
1. i3.16xlarge – 488GB RAM, 8xNVMe SSD drives and total 15.2TB, with 3.3M/300K read/write IOPS

Test Parameters

- We used 100B and 1000B value sizes, covering most standard Redis use cases
- We tested 50% and 85% RAM hit ratios (i.e. a number of requests served directly from RAM)
- We benchmarked our customers’ most commonly used read/write ratios: 1:1 and 4:1. All tests were done on a single server
- In each configuration, we tested how many ops/sec could be achieved while keeping sub-millisecond server latency (not including the network)

**What We Found**
The two graphs below show the 100B and 1000B test results:



**Performance Improvement**
The table below summarizes the average improvement factor of the i3 over i2 instances across all tests:

|  | 100B | 1000B |
|---|---|---|
| i3.8xlarge vs. i2.8xlarge | x1.98 | x1.66 |
| i3.16xlarge vs. i2.8xlarge | x2.59 | x1.92 |

The results above show that the new I3 instances are truly an improvement over I2 as demonstrated by Redis’ Redise Flash technology.

Savings Per Operation
AWS I3 instances are not only faster than AWS I2 instances, they are also much cheaper. For example, the cost of an on-demand Linux i3.8xlarge instance in US East North Virginia region is $2.496/hr versus $6.820/hr of i2.8xlarge, **that’s 73% cheaper**!

When we calculated the savings per RoF operation on an i3.8xlarge instance, we found the following:

| i3.8xlarge savings per 100B operations | i3.8xlarge savings per 1000B operations |
|---|---|
| 81.47%(or each operation is x5.4 cheaper) | 77.88%(or each operation is x4.5 cheaper) |

Note: We only compared the i3.8xlarge and i2.8xlarge instances as both have similar RAM and SSD capacity.

**Summary**
As expected, we found that Redise Flash runs **up to 2.6 times faster** on AWS I3 instance than it does on AWS I2 instance. We also found that due to the relatively attractive cost of I3 instances, each Redise Flash operation is **up to 5.4 times cheaper** on an I3 instance than it is on an I2 instance.

**Appendix:**

**Benchmark setup**

- Redise Pack Redise Flash version: v. 4.5.0
- Redise Flash database: 20 shards
- Client machine: EC2 C4.8xlarge
- AMI: ami-f4cc1de2 (xenial)
- Load Generation tool: [memtier benchmark](https://github.com/RedisLabs/memtier_benchmark/blob/master/README.md)
- An example of the memtier command line:
*memtier_benchmark -s 172.31.9.63 -p 12345 –pipeline=20 -c 10 -t 15 -d 100 –key-maximum=42949673 –key-pattern=G:G –key-stddev=1197484 –ratio=1:1 –distinct-client-seed –randomize –test-time=600 –run-count=1 –hide-histogram*

**AWS I3 and I2 instances configurations:**

![](/images/blog/81481967a068516032a4da224055d0a7487cec77-296x151.webp)

![](/images/blog/39a0ea3f7482b5a9ebbf35397dacd9f7a85fd44b-386x176.webp)

Detailed pricing can be found on the AWS website.
