---
title: "It’s True: Even Modest Datasets Can Enjoy the Speediest Performance"
linkTitle: "It’s True: Even Modest Datasets Can Enjoy the Speediest Performance"
url: "/blog/its-true-even-modest-datasets-can-enjoy-the-speediest-performance/"
description: "Those of us who use them know that Redis and Memcached were designed from the ground-up to achieve the highest throughput and the lowest latency for applications, and they are in fact the fastest..."
date: 2012-09-27
blogCategories:
- "Tech"
authors:
- "Redis  "
lastmod: 2025-03-27
hidden: true
---

*By Redis   · Published 27 September 2012 · updated 27 March 2025*

![Blog tile image](/images/site-mirror/0073e867b4e64f59de9047fdcde04295ba647e5c-772x550.webp)

Those of us who use them know that Redis and Memcached were designed from the ground-up to achieve the highest throughput and the lowest latency for applications, and they are in fact the fastest data store systems available today. They serve data from RAM, and execute all the simple operations (such as SET and GET) with O(1) complexity. However, when run over cloud infrastructure such as AWS, Redis or Memcached may experience significant performance variations across different instances and platforms, which can dramatically affect the performance of your application. As a provider of cloud services for hosting Redis and Memcached datasets, we at Garantia Data are always looking at best practices for optimizing performance, and so we recently conducted a benchmark test to compare small-to-medium size (<=12GB) Redis and Memcached datasets running over different AWS instances and platforms.

**Architectural considerations**

The first thing we looked at when putting together our benchmark was the various architectural alternatives we wanted to compare. Users typically choose the most economical AWS instance based on the initial size estimate of their dataset, however, it’s crucial to also keep in mind that other AWS users might share the same physical server that runs your data (as nicely explained by Adrian Cockcroft [here](https://bit.ly/Q5yKc8)). This is especially true if you have a small-to-medium dataset, because instances between m1.small and m1.large are much more likely to be shared on a physical server than large instances like m2.2xlarge and m2.4.xlarge, which typically run on a dedicated physical server. Your “neighbours” may become ”noisy” once they start consuming excess I/O and CPU resources from your physical server. In addition, small-to-medium instances are by nature weaker in processing power than large instances. Your instance selection may have a big effect on the performance of your Redis/Memcached, which typically uses an optimal number of code lines to run each command. Any slight interference of a “noisy neighbor” or lack of processing power that delays operations (such as memory access, network transmission or context switching) can significantly reduce throughput and increase latency. Because of this, it’s a fair assumption that apps using small-to-medium AWS instances for their Redis or Memcached data are more prone to performance degradation. Another way of running Redis or Memcached on AWS is to use a service, such as the AWS [Elasticache](https://aws.amazon.com/elasticache/) (for Memcached), or our own [Redis Cloud](/redis-enterprise-cloud/overview/) or [Memcached Cloud](/memcached). However, when using Elasticache, the user is still required to select instance size and therefore may suffer from the same performance issues. Garantia Data’s Redis Cloud and Memcached Cloud use a different approach: we run all cluster nodes on m2.2xlarge or m2.4xlarge instances to ensure the best performance, but we only charge users based on their actual dataset size (in GBs). For all the details about how we set up the benchmark, including resources, data sets and configuration, feel free to hop to the end of the post.

**Benchmark test results**

Without further ado, here’s what we found out about how the alternatives for running Redis and Memcached on AWS compare when it comes to performance.

**Throughput**

![](/images/site-mirror/db236eafdc3cbcae4ae8d71c08e6dbc01332d9fe-698x380.webp)

*Note: ElastiCache uses 2 Memcached threads on m1.large instance and 4 on m1.xlarge instance, while the Stand-alone Redis is based on a single threaded architecture* As seen above, the RPS of the Garantia Data Memcached/Redis Cloud was better in the range of 25-100% (depending on the instance type) than ElastiCache or Stand-alone Redis.

**Latency**

We also saw a better than average response time with our Memcached/Redis Cloud cluster in the range of 25-50% than ElastiCache or Stand-alone Redis, while its 99%-tile response time was significantly better, in the range of x6-x30, than ElastiCache or Stand-alone Redis.

*Note: Our response time measurement takes into account the network round-trip, the Redis/Memcached processing time, and the time it takes the memtier_benchmark tool to parse the result.*

**Conclusion**

This benchmark demonstrates that a different architectural approach can improve throughput and significantly reduce latency of Redis and Memcached in the cloud. We believe these findings are explained by the unique architecture of our Redis Cloud and Memcached Cloud services. We at Garantia Data have developed several technologies that run on each node of our clusters and guarantee minimal interference between users, i.e.:

- Migrating “noisy” datasets from one node to another
- Re-sharding “noisy” datasets for better performance and less interference

Behind the scenes we monitor each and every Redis or Memcached command and constantly compare its response time to what should be an optimal value. In addition, we reshard datasets on-the-fly in a non-intrusive manner, which is a very challenging operation with complex synchronization mechanisms between multiple distributed elements. This architecture allows users with any size dataset (including small-to-medium sizes) to run on the strongest instances and enjoy the highest performance, while paying only for their actual GB used on an hourly basis — so that our customers get the best of both worlds.

**Benchmark test setup**

We know you want to know about the nitty gritty details of our benchmark, so here are the resources we used:

- ElastiCache on m1.small, m1.large, m1.xlarge instances
- Stand-alone Redis on m1.small, m1.large, m1.xlarge instances
- A Garantia Data Redis/Memcached Cloud cluster (run on the same technological platform) on m2.4xlarge instances

This was our setup for generating load:

- For ElastiCache and the Stand-alone Redis tests — m2.2xlarge instance that ran our *memtier_benchmark* load generation tool (an advanced load generator tool we developed, which we will soon share in our [github](https://github.com/GarantiaData) account).
- For the Garantia Data Redis/Memcached Cloud tests — 2 x m2.2xlarge instances that ran the *memtier_benchmark* tool, one for simulating load and analysing results, and the other for creating background load that simulates noisy neighbors.

![](/images/site-mirror/04649e4dc4c1d24811ac540805344ac51c0206cb-851x379.webp)

We ran each of the tests 3 times on each configuration and calculated the average results using the following parameters:

1. 100 connections
1. 100B object size
1. 50/50 GET/SET ratio (for both Redis and Memcached)

Our dataset sizes included:

- 0.5GB for m1.small instance
- 5GB for m1.large instance
- 12GB for m1.xlarge instance
- Any combination of the above for the Garantia Data Redis/Memcached Cloud cluster
