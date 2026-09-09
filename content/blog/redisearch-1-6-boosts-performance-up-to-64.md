---
title: "RediSearch 1.6 Boosts Performance Up to 64%"
linkTitle: "RediSearch 1.6 Boosts Performance Up to 64%"
url: "/blog/redisearch-1-6-boosts-performance-up-to-64/"
description: "The newly introduced RediSearch 1.6 adds some important new functionality, including aliasing, a low-level API, and improved query validation, as well as making Fork garbage collection the module’s..."
date: 2020-03-12
blogCategories:
- "Product Releases"
authors:
- "Pieter Cailliau"
- "Filipe Oliveira"
lastmod: 2025-07-03
hidden: true
---

*By Pieter Cailliau, Filipe Oliveira · Published 12 March 2020 · updated 3 July 2025*

![Blog tile image](/images/blog/46e7a4e823913ad78c8d439125b1610e047aebf7-368x260.webp)

The newly introduced RediSearch 1.6 adds some important new functionality, including aliasing, a low-level API, and improved query validation, as well as making Fork garbage collection the module’s default. Even more important, though, the original code in RediSearch 1.6 has been refactored to significantly boost performance. The improved performance leads to a better user experience as applications can be more reactive than ever with search.

***(For more on the new features in RediSearch 1.6, see our blog post on ***[***Announcing RediSearch Version 1.6***](/blog/redisearch-version-1-6-adds-features-improves-performance)***.)***

Just how big is the performance bump in RediSearch 1.6? That’s what this post is all about, and we’ll get to the results in a moment. But in order to fully understand the performance issues, we needed a way to properly compare database search speed.

To compare RediSearch version 1.6 against the previous 1.4 release, we created a full-text search benchmark. [FTSB](https://github.com/RediSearch/ftsb) (licensed under [MIT](https://github.com/RediSearch/ftsb/blob/master/LICENSE)) was designed specifically to help developers, system architects, and DevOps practitioners find the best search engine for their workloads. It allows us to generate datasets and then benchmark read and write performance on common search queries. It supports [two data sets](https://github.com/RediSearch/ftsb#current-use-cases) with different characteristics:

- **enwiki-abstract:** From [English-language Wikipedia:Database](https://en.wikipedia.org/wiki/Wikipedia:Database_download) page abstracts. This use case generates 5.9 million documents, with 3 TEXT fields per document, and an expected average document size of ~250 bytes.
- **enwiki-pages:** From [English-language Wikipedia:Database](https://en.wikipedia.org/wiki/Wikipedia:Database_download) last page revisions, containing processed metadata extracted from the full Wikipedia XML dump. This use case generates 4 TEXT fields (2 sortable), 1 sortable TAG field, and 6 sortable NUMERIC fields per document, and an expected average document size of ~400 bytes.

To achieve reproducible results, the data to be inserted and the queries to be run are pre-generated, and native Go clients are used wherever possible to connect to each database. In order to design a common benchmarking suite, all latency results include the network round-trip time (RTT) to measure duration to and from the client, so that we can properly compare additional databases.

We encourage you to run these benchmarks for yourself to independently verify the results on your hardware and datasets of choice. More importantly, we’re looking for feedback and extension requests to the tool with further use cases (e.g. ecommerce, JSON data, geodata, etc.) and problem domains. If you are the developer of a full-text search engine and want to include your database in the [FTSB](https://github.com/RediSearch/ftsb), feel free to open an issue or a pull request to add it.

## Testing infrastructure

We ran the performance benchmarks on Amazon Web Services instances, provisioned through our benchmark testing infrastructure. Both the benchmarking client and database servers were running on separate c5.24xlarge instances. The tests were executed on a single node Redis Enterprise cluster setup, version 5.4.10-22, with data distributed across 10 master shards.

In addition to this primary benchmark/performance analysis scenario, we also enabled running baseline benchmarks on network, memory, CPU, and I/O, in order to understand the underlying network and virtual machine characteristics. We represent our benchmarking infrastructure as code so that it is easily replicable and stable.

## Dataset and insertion rate

The table below displays the size of the datasets we used in this benchmark. It also shows the overall indexing rate for each dataset. You can see that RediSearch 1.6 did not degrade performance on ingestion:

![Redis](/images/blog/5c35d69912b936f0383c58bedf509a7c11d9be33-977x299.webp)

FSTB currently supports three full-text search queries, as shown in the chart below (remember that the latency results include RTT). Note that we plan to extend this benchmark suite with a more diversified set of [read queries](https://github.com/RediSearch/ftsb#appendix-ii---english-language-wikipediadatabase-page-abstracts).

![Redis](/images/blog/1ec44fa2b97238ae0c8d8ad291198db55306d6b0-974x339.webp)

We can observe in the table above that RediSearch 1.6’s improved q99 makes it more predictable, with fewer latency peaks.The chart below shows that compared to RediSearch 1.4, **RediSearch 1.6 increases throughput by 48% to 63%.**

![Redis](/images/blog/7b6f8832e4391f1d5c7a0d6c6ffa5d685ca5cf78-1024x640.webp)

![Redis](/images/blog/c4ddcc099c4c25cc5bc1d9cfea14c511fde595f6-1024x640.webp)

Similarly, the** latency (q50) drops by 51% to 64%.**

## Aggregation queries

In addition to the simple search queries, we also added a set of aggregation queries. The full details of what each query does can be found in our [benchmark repository](https://github.com/RediSearch/ftsb#aggregate-queries-1) (again, remember that the latency results include RTT):

![Redis](/images/blog/72764d860001160808c46ac5d5f8964b2cd94695-970x515.webp)

Here too, RediSearch 1.6 improves performance compared to RediSearch 1.4. **The throughput increases by 15% to 64%:**

![](/images/blog/98c590dedcce96afafc8d2d0d979924f7a76d8a3-1024x630.webp)

Similarly, the **latency (q50) decreases by 17% to 73%**:

![Redis](/images/blog/f56efd6b543835d445ecd772c50bce683b08d912-1024x639.webp)

## RediSearch 1.6 by the numbers

Put it all together, and you can see that RediSearch 1.6 brings significant performance advantages compared to version 1.4. Specifically, **RediSearch 1.6 increased simple full-text search throughput by up to 63% while cutting latency (q50) by up to 64%. For aggregate queries, throughput increased from 15% to 64%.**

Almost as important, the introduction of full-text search benchmarking helped us to constantly monitor the performance between different versions of RediSearch and it has proven to be of extreme value in eliminating performance bottlenecks and hardening our solution.
