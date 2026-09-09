---
title: "Making the Fast, Faster! Methodically Improving Redis Performance"
linkTitle: "Making the Fast, Faster! Methodically Improving Redis Performance"
url: "/blog/improving-redis-performance/"
description: "Redis is developed with a great emphasis on performance. We do our best with every release to ensure you’ll experience a very stable and fast product."
date: 2022-06-15
blogCategories:
- "Tech"
authors:
- "Filipe Oliveira"
lastmod: 2025-03-27
hidden: true
---

*By Filipe Oliveira, Performance Engineer · Published 15 June 2022 · updated 27 March 2025*

![Blog tile image](/images/site-mirror/0c00ac98ca37b5685d8b50c3598220bc71ec360d-772x550.webp)

Redis is developed with a great emphasis on performance. We do our best with every release to ensure you’ll experience a very stable and fast product.

Nevertheless, if you’re finding room to improve the efficiency of Redis or are pursuing a performance regression investigation, you will need a concise methodical way of monitoring and analyzing Redis’ performance. This is the story of one of those optimizations.

In the end, we’ve improved [stream’s ingest performance](https://github.com/redis/redis/pull/10574) by around 20%, an improvement you can already take advantage of on the [Redis v7.0](https://github.com/redis/redis/releases/tag/7.0.0).

## A standard SPEC

Before jumping into the optimization, we want to give you a high-level idea of how we got to it.

As stated before, we want to identify Redis performance regressions and/or potential on-CPU performance improvements. To do so, we felt the need to foster a set of cross-company and cross-community [standards](https://github.com/redis/redis-benchmarks-specification/) on all matters related to performance and observability requirements and expectations.

In a nutshell, we constantly run the SPEC’s benchmarks by breaking them down by branch/tag and interpret the resulting performance data that includes profiling tools/probers outputs and client outputs in a “zero-touch” fully automated mode.

The used instruments are all open source and rely on tools/popular frameworks like memtier_benchmark, redis-benchmark, [Linux perf_events](https://man7.org/linux/man-pages/man1/),[ bcc/BPF tracing tools](https://github.com/iovisor/bcc), and Brendan Greg’s[ FlameGraph repo](https://github.com/brendangregg/FlameGraph).

If you’re interested in further details on how we use profilers with Redis, we recommend taking a look at our extremely detailed *“*[*Performance engineering guide for on-CPU profiling and tracing*](https://redis.io/docs/latest/operate/oss_and_stack/management/optimization/cpu-profiling/)*.”*

## Avoid duplicate computation to improve performance

As soon as this first step was given, we started interpreting the profiling tools/probers’ outputs. One of the benchmarks that presented an interesting pattern was the Streams’ ingested benchmark which simply ingests data into a stream with a command similar to the one below:

**`XADD key * field value`.**

We’ve observed that when adding to a stream without an ID, it creates duplicate work on SDS creation/freeing/sdslen that costs about 10% of the CPU cycles, as showcased in detail in the next two perf report prints.

![redis performance breakdown of on-cpu time for the XADD command](/images/site-mirror/2b2ba8244b4223fd5592af82155bd5ef05a396e9-1024x662.webp)

*Breakdown of on-CPU time for the XADD command*

For the same inputs, sdscatfmt and _sdsnewlen were being called twice:

![](/images/site-mirror/67a5c212856a553bf5002504ce028e9147f9635d-1024x156.webp)

*sdscatfmt and _sdsnewlen duplicate computation overhead detail*

This allowed us to optimize Streams ingestion in around 9-10% as confirmed following benchmark results:

**Baseline on unstable branch (**[**6b403f5**](https://github.com/redis/redis/commit/6b403f56a523480a08b1143c676ce174d0d0251c)**) :**

**First commit of this PR (avoid dup work):**

![github stats results](/images/site-mirror/3c7cbbc9b91508cfaaab0b5e84e9c9410e946b1a-894x170.webp)

## Avoiding duplicate allocations to improve performance

The initial focus of this use-case improvement lead to further analysis from Oran (one of the core-team members) that noticed yet another waste of CPU cycles. This time, it was due to non-optimal memory management within the same code block. We were allocating an empty SDS, and then re-allocating it. Reducing the number of calls will give us yet another speed improvement, as shown below.

Second commit (avoid reallocs):

![github second commit stats](/images/site-mirror/190523533e5bb2eaae5a848fb9f9c828409ba32a-889x168.webp)

## Measured improvement

![](/images/site-mirror/f16f2923318b70944492918bb4da7bb156e62b65-795x491.webp)

As expected, by simply reusing intermediate computation and consequently reducing the redundant computation and allocations within the internally called functions, we’ve measured a reduction in the overall CPU time of ~= 20% of [Redis Streams](https://redis.io/docs/manual/data-types/streams/).

We believe this is an example of how methodical simple improvements can lead to significant bumps in performance, even for already deeply optimized code like Redis.

Our goal is to expand the performance visibility we have of Redis, and members from both industry and academia, including organizations and individuals, are encouraged to contribute. If we don’t measure it, we can’t improve it.

---
