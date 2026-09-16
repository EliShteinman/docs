---
title: "Redis Labs Dominates Independent Redis-as-a-Service (RaaS) Benchmark"
linkTitle: "Redis Labs Dominates Independent Redis-as-a-Service (RaaS) Benchmark"
url: "/blog/redis-labs-dominates-independent-redis-as-a-service-raas-benchmark/"
description: "Making the right Redis decision isn’t easy. Should I build out my own Redis environment or pay a consultant or service to manage it for me? When is the right time to start using Redis? Is my..."
date: 2015-01-27
blogCategories:
- "Company"
authors:
- "Leena Joshi"
lastmod: 2025-03-04
hidden: true
mirrored: true
---

*By Leena Joshi, VP Product Marketing · Published 27 January 2015 · updated 4 March 2025*

![Blog tile image](/images/site-mirror/4bbc40ee7a42c6f1ee8302191a8e1d69e537de81-140x92.webp)

![](/images/site-mirror/3006e929cd5cfe48cece4bc555a7c75e940be641-635x200.webp)

Making the right Redis decision isn’t easy. Should I build out my own Redis environment or pay a consultant or service to manage it for me? When is the right time to start using Redis? Is my current solution scalable and available?

With the explosive growth of Redis, we asked the Altoros team to conduct the first wide-scale benchmark test of popular Redis-as-a-Service (RaaS) offerings that you can use on IaaS and PaaS solutions like Amazon Web Services and Heroku.

Get the full benchmark results for free [here](https://lp.redislabs.com/2015-Q1-Redis-Cloud-Service-Benchmark-Lander01.html).

Altoros’ findings were impressive, with Redis achieving the highest throughput and the lowest latency across all the tested workloads (tests were conducted over a single AWS EC2 instance):

- **Simple workload.** Redis Cloud reached 1.14 million operations per second (ops/sec), while runners up ElastiCache and RedisGreen hit 611 thousand and 536 thousand ops/sec, respectively. Redis Cloud also led the RaaS industry in latency, clocking in at .18 milliseconds, which was 45 percent faster than the nearest comparison, ElastiCache.
- **Complex workload.** Redis Cloud continued to dominate the competition with 253 percent more throughput and over 70 percent lower latency compared to ElastiCache and Redis Green.

Our CEO and co-founder, Ofer Bengal had this to say about our success in the benchmark: “Developers love the speed and open source nature of Redis, yet are challenged by many demanding facets of scaling their cloud architecture. Redis Cloud is a perfect fit at this point, because it allows the developer to enjoy the benefits of Redis without having to do any heavy lifting.”

“While most Redis benchmarks focus on simple GET/SET operations, we were interested in better utilization of built-in data types and server-side operations,” said Vladimir Starostenkov, Senior R&D Engineer at Altoros. “For this reason, we designed a combined workload, embodying two different types of queries running concurrently and imitating a real-life Redis use case.”

Get the full benchmark results for free [here](https://lp.redislabs.com/2015-Q1-Redis-Cloud-Service-Benchmark-Lander01.html).

For this benchmark, Altoros used a single AWS EC2 instance in the same region. In addition, it used two AWS EC2 instances to run memtier_benchmark, an open source traffic generator written in C++, and a Java-based stress tool that simulates a more complex workload. The benchmark consisted of three workloads: simple, complex and combined.
