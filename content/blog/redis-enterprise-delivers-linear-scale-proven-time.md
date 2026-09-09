---
title: "Redis Enterprise Delivers Linear Scale, Proven Time and Again!"
linkTitle: "Redis Enterprise Delivers Linear Scale, Proven Time and Again!"
url: "/blog/redis-enterprise-delivers-linear-scale-proven-time/"
description: "In Redis Enterprise 5.0, we introduced support for the Open Source (OSS) cluster API, which allows a Redis Enterprise cluster to scale infinitely and linearly by adding shards and nodes. This post..."
date: 2018-08-03
blogCategories:
- "Benchmarks"
- "Company"
authors:
- "David Maier"
lastmod: 2025-03-27
hidden: true
---

*By David Maier, Technical Enablement Mananger · Published 3 August 2018 · updated 27 March 2025*

![Blog tile image](/images/site-mirror/0073e867b4e64f59de9047fdcde04295ba647e5c-772x550.webp)

In [Redis Enterprise](/redis-enterprise/) 5.0, we introduced support for the Open Source (OSS) cluster API, which allows a Redis Enterprise cluster to scale infinitely and linearly by adding shards and nodes. [This post](/blog/10m-opssec-1msec-latency-6-ec2-nodes/) describes the first of our linear scaling benchmark tests and how Redis Enterprise works with the OSS cluster API and demonstrates infinite linear performance scalability.

Over the course of the last few months, we conducted tests that included additional benchmarking—n-shard database on a k-node Redis Enterprise cluster, as noted below:

![Table 1: Redis Enterprise scale linearly while delivering sub-millisecond performance](/images/site-mirror/dde1f7b2580f01f1c7bf8a4f42d155cecc2b3775-386x234.webp)

*Table 1: Redis Enterprise scale linearly while delivering sub-millisecond performance*

![Figure 1: Cluster throughput (@ 1 msec latency)](/images/site-mirror/7911717161c946cdf815ae9600712523697fe4e3-600x371.webp)

*Figure 1: Cluster throughput (@ 1 msec latency)*

This demonstrates that as throughput increases, there is a linear proportional increase in nodes, and Redis Enterprise is able to consistently deliver sub-millisecond latency across all data sizes and workloads. The details behind this analysis, as well as a complete write-up of the benchmark configuration, is available in [this whitepaper](/docs/linear-scaling-benchmark-50m-ops-sec/).

## So what is linear scale?

According to [Wikipedia](https://en.wikipedia.org/wiki/Scalability), a scalable database is one that can be upgraded to process more transactions by adding new processors and storage, and which can be upgraded easily and transparently without shutting it down. A database can scale out (by adding node(s) to the cluster, rebalancing, and then resharding your database) or scale up (by adding shards to your database without adding nodes to your cluster). Redis Enterprise is optimized to scale both out and up, simply by the virtue that it’s not bound to disk.

“Linear scaling” (when scaling out) means sequentially scaling your database by adding resources (in Redis terms, “resources” refers to nodes and shards) that correlate to the increased throughput. True linear scalability means that the amount of resources increases at the same proportion as your database throughput, and in a deterministic manner. For example, increasing your cluster resources by 50% will translate to 50% throughput increases.

## Linear scale matters!

Understanding the scalability of multi-node systems is crucial for resource planning; it’s important to know exactly how adding nodes and shards will impact performance. If a database can scale linearly, it minimizes operational overhead and allows you to grow your business without having to worry about size limits or performance bottlenecks in your database. However, very often there is an overhead associated with scaling out, which means when you increase your capacity by N, your database throughput often increases by a factor that’s less (or much less) than N.

A database delivers:

- Sub-linear scale – when the relative capacity is less than the number of resources
- Linear scale – when the relative capacity is equal to the relative number of added resources
- Super-linear scale – when the relative capacity increases due to adding resources

## Do other NoSQL databases scale linearly?

The simple answer is NO!

There have been many benchmarks and blogs published by other database vendors on their ability to scale, but truly, the results show that Redis Enterprise outperforms its NoSQL counterparts.

The chart below is the outcome of a benchmark that one of the other NoSQL vendors performed. It compares NoSQL databases such as Apache Cassandra, Hbase, MongoDB, and Couchbase.

![Table 2: Nodes and throughput by vendor](/images/site-mirror/04f311489349d160f777726058ec599ffb2a6690-860x275.webp)


*Table 2: Nodes and throughput by *vendor

![Cassandra: Linear vs. Actual Scale graph](/images/site-mirror/63cb0ad1f6f6c11607503c53cb611690aeb5cb04-420x260.webp)

![HBase: Linear vs. Actual Scale graph](/images/site-mirror/7a1a4f6d7cef86eb8a86a04262c793268ecb8f5c-420x260.webp)

![MongoDB: Linear vs. Actual Scale](/images/site-mirror/d0ab0ac7d26ff9c18783fd34cb70088855d64e38-420x260.webp)

![Couchbase: Linear vs. Actual Scale](/images/site-mirror/e96cbdadfbc8a080182dc0f6126df3bec01fcdad-420x260.webp)

As is obvious from the charts, all of these vendors deliver sub-linear scale. For instance, if we analyze Cassandra’s throughput by node, Cassandra can process ~18,700 ops/second (rounding up) with 1 node. Then, at 32 nodes, it should have been able to process ~600,000 ops/second. However, as illustrated above, it can only process about ~330,000 operations/second—only 55% of what a truly linearly scaling database should be able to process.

The same math and conclusion hold good for all other vendors in this table.

The fact that these databases are measuring tens of thousands of requests per second as their best-case scenario is rather appalling. Modern-day applications such as eCommerce, social networking, online gaming, messaging and collaboration, the Internet of Things, and many others need to be able to handle *millions* of operations per second. These databases are clearly not built for such volumes while delivering lower TCO.

With its [latest benchmark](/docs/linear-scaling-benchmark-50m-ops-sec/), Redis Enterprise has proven its ability to process millions of operations per second, even when using its most basic configuration. As demonstrated in the chart below, Redis Enterprise simply outperforms the other databases and delivers super-linear scale without any compromise to performance!

![Table 3: Redis Enterprise - Optimal vs. Actual Throughput by Node](/images/site-mirror/e76e9b268bc9612d1c5e13a912449a16d8423b88-634x139.webp)


*Table 3: Redis Enterprise – Optimal vs. Actual Throughput by Node*

![Redis Enterprise: Linear Scale vs. Actual Scale graph](/images/site-mirror/530d797633fd982896743f48ed4386ab37dd03ce-541x335.webp)

This new benchmark demonstrates Redis Enterprises’ ability to achieve true linear scalability, while delivering the predictable and fast performance with the most efficient use of your resources, helping you build scalable modern applications cost-effectively.
