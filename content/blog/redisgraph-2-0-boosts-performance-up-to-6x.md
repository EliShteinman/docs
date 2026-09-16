---
title: "RedisGraph 2.0 Boosts Performance Up to 6x"
linkTitle: "RedisGraph 2.0 Boosts Performance Up to 6x"
url: "/blog/redisgraph-2-0-boosts-performance-up-to-6x/"
description: "The newly announced RedisGraph 2.0 module brings a number of improvements, including increased Cypher support, full-text search, and it enables graph visualization. Just as important, however, the..."
date: 2020-04-07
blogCategories:
- "Product Releases"
- "Redis Modules"
authors:
- "Pieter Cailliau"
- "Filipe Oliveira"
lastmod: 2025-07-03
hidden: true
mirrored: true
---

*By Pieter Cailliau, Filipe Oliveira · Published 7 April 2020 · updated 3 July 2025*

![Blog tile image](/images/site-mirror/e16c4f6d29d0d217f605d83d1f54b42984a860c3-368x260.webp)

The newly announced RedisGraph 2.0 module brings a number of improvements, including increased Cypher support, full-text search, and it enables graph visualization. Just as important, however, the latest version of RedisGraph delivers significant performance improvements: **with latency improvements up to 6x and throughput improvements up to 5x**. Let’s take a look at those performance gains and the benchmarks used to demonstrate them.

When we released RedisGraph 1.0 back in November 2018, we shared [benchmark](/blog/new-redisgraph-1-0-achieves-600x-faster-performance-graph-databases/) results based on the *k-hop neighborhood count query*. The new [RedisGraph 2.0](/blog/introducing-redisgraph-2-0/) includes new features and functionalities that support more-comprehensive test suites, like the ones provided by the[ Linked Data Benchmark Council (LDBC)—more on that below](http://ldbcouncil.org/). But we still rely on the k-hop benchmark in order to compare RedisGraph 2.0 to v1.2.

The K-hop neighborhood count query is a graph local query that counts the number of nodes a single start node (seed) is connected to at a certain depth, and counts only nodes that are* k*-hops away, as shown here:

![](/images/site-mirror/fa7237bc59eced2198bafe373ffdd6aa226cc7ee-720x777.gif)

K-hop neighborhoods queries are very useful in analytic tasks on large-scale graphs, like finding relations in a social network, or recommending friends or advertising links according to common properties.

## Dataset

We’ve kept the previous benchmark Graph 500 dataset with scale 22, with the following graph characteristics:

[Watch the video](http://graph500.org)

To gain deeper insight and coverage of the database performance, we extended the seed coverage of the benchmark to 100,000 random deterministic seeds instead of 300. To make it easy for anyone to replicate our results, here is a [public link to the persistent store graph 500 dataset with scale 22 on RDB format](https://performance-cto-group-public.s3.amazonaws.com/benchmarks/redisgraph/khop/graph500-22/rdb/GRAPH500_S22_dump.rdb).

## The methodology of k-hop benchmark

For each tested version, we performed:

- 1-Hop 22M queries
- 2-Hop 220K queries
- 3-Hop 22K queries
- 6-Hop 22K queries

All queries were under a concurrent parallel load of 22 clients. We reported the median (q50) and achievable throughput.

To get steady-state results, we discarded the previous Python benchmark client in favor of the [memtier_benchmark](https://github.com/RedisLabs/memtier_benchmark), which provides low overhead and full-latency-spectrum latency metrics.

## Testing infrastructure

All benchmark variations were run on Amazon Web Services instances, provisioned through our benchmark-testing infrastructure. Both the benchmarking client and database servers were running on separate c5.12xlarge instances. The tests were executed on a single-shard setup, with RedisGraph versions 1.2 and 2.0.5.

In addition to the primary benchmark/performance analysis scenarios described above, we also enable running baseline benchmarks on network, memory, CPU, and I/O, in order to understand the underlying network and virtual machine characteristics. We represent our benchmarking infrastructure as code so that it is stable and easily reproducible.

## Benchmark results

The RedisGraph 1.2 vs 2.0 benchmark values point towards significant improvements on parallel workloads (multiple clients). We’ve measured** latency improvements up to 6x** and **throughput improvements up to 5x** when performing graph traversals. The more parallel and computationally expensive the workload, the better RedisGraph 2.0 performs when compared to the previous version.

![](/images/site-mirror/1093fed5d93166c36be17fb7765fa3768ca5d07d-1024x588.webp)

![](/images/site-mirror/2120a5997c00f8ced58ec2e1a86c89fc08187bca-1024x588.webp)

## OpenMP effect

RedisGraph 2.0 incorporates the latest version 3.2.0 of SuiteSparse:GraphBLAS —[SuiteSparse](https://github.com/DrTimothyAldenDavis/GraphBLAS)’s implementation of GraphBLAS— which RedisGraph uses for sparse matrix operations. With this version it is now possible to exploit shared-memory parallelism by recurring to OpenMP in order to gain significant performance advantages.

Internal testing on CPU intensive queries showed that RedisGraph spends around 75% of its total CPU time on SuiteSparse:GraphBLAS. To demonstrate the performance gains of SuiteSparse:GraphBLAS parallel OpenMP-based implementation in RedisGraph, we tested the 6-hop query neighborhood count due to it being computationally expensive.

As visible below, using a single-threaded SuiteSparse:GraphBLAS translated into q50 latencies of 537ms, and 175ms with 22 OpenMP threads, with latency reductions of up to 6x, at no extra cost for RedisGraph. The improvements are even more noticeable in the higher-latency spectrum (high-quantile values like q99):

![](/images/site-mirror/dd9e14235e9a3240fdbc30b0f10299d4ad1477bd-619x171.webp)

![](/images/site-mirror/042f982fea9c702b2372d2bc24c83fb7b9c070f4-1024x633.webp)

## Embracing LDBC

Because RedisGraph 2.0 supports many more Cypher features, we decided to start to embrace the [Linked Data Benchmark Council](http://ldbcouncil.org/) (LDBC) benchmarks. LDBC has gathered strong industrial participation for its mission to standardize the evaluation of graph data management systems. In this section we wanted to give an update on the progress we’ve made.

The LDBC Social Network Benchmark (SNB) in the LDBC is a logical choice for RedisGraph since it enables complex read queries that touch a significant amount of data, have complex graph dependencies, and require the graph database to support complex and innovative query patterns and algorithms.

In the LDBC SNB benchmark, the nodes and edges distribution are guided by a degree-distribution function similar to the one found in [Facebook](https://arxiv.org/abs/1111.4503). This benchmark accounts for an important aspect of simulating social networks, the fact that persons with similar interests and behaviors tend to be connected (known as the [Homophily principle)](https://www.annualreviews.org/doi/abs/10.1146/annurev.soc.27.1.415?journalCode=soc).

Concurrent with the SNB’s read queries is a write workload, which reproduces real-world social network scenarios such as adding a friendship among persons or liking and commenting on a post.

Currently from the LDBC SNB benchmark queries we support 100% of the write queries and 52% of the read queries, as seen in the following table:

![](/images/site-mirror/72b836ee4fef977e6994d8381ce7d4bb114d9785-356x344.webp)

The soon-to-be-supported Cypher features: OPTIONAL MATCH (the equivalent of outer join in SQL), shortestPath (an implementation of the well-known [Shortest path problem](https://en.wikipedia.org/wiki/Shortest_path_problem)), and list and pattern comprehensions will enable us to support 100% of the SNB’s complex read queries.

## Conclusion

RedisGraph 2.0 brings significant performance gains compared to version 1.2, which can lead to 6X faster queries. Not only did the sequential performance improve, RedisGraph is also able to exploit shared-memory parallelism with the inclusion of the latest versions of SuiteSparse:GraphBLAS, leading to even further performance gains.

In conjunction with the performance improvements, the work we did to increase the Cypher support gets us close to supporting the richer, community-driven LDBC benchmark, which we are excited to be part of and use to improve and harden our solution.
