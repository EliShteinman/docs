---
title: "Announcing a New Technology Collaboration with AMD"
linkTitle: "Announcing a New Technology Collaboration with AMD"
url: "/blog/announcing-a-new-technology-collaboration-with-amd/"
description: "We’re excited to announce a new technology collaboration with AMD, which is using Redis Enterprise to benchmark Redis database on publicly launched and available AMD EPYCTM 7002 series processor..."
date: 2020-08-21
blogCategories:
- "Company"
authors:
- "Filipe Oliveira"
- "Yiftach Shoolman"
lastmod: 2025-07-03
hidden: true
---

*By Filipe Oliveira, Yiftach Shoolman · Published 21 August 2020 · updated 3 July 2025*

![Blog tile image](/images/blog/938429530ed9b5ea28b6290156e64af19a2e4ff9-1201x628.webp)

We’re excited to announce a new technology collaboration with[ AMD](https://www.amd.com/en), which is using Redis Enterprise to benchmark Redis database on publicly launched and available AMD EPYCTM 7002 series processor powered systems, and instances in the cloud. The first series of cloud instances tested in this collaboration are[ the AWS EC2 C5a instances](https://aws.amazon.com/ec2/amd/), which are powered by 2nd generation AMD EPYCTM processors. The 2nd generation AMD EPYCTM processors used in the AWS C5a instances run at frequencies up to 3.3 GHz[i] and are available in eight virtualized sizes—ranging from 2 vCPUs to 96 vCPUs—and offer up to 192GB of memory. These C5a instances provide customers with options to optimize cost and performance for a variety of compute-intensive workloads and can be up to[ 10% less expensive than comparable instances](https://aws.amazon.com/ec2/amd/).

“We’re excited to be working with AMD to benchmark the Amazon EC2 C5a instances, and pleased the results clearly demonstrate cost and performance advantages for our customers while highlighting how Redis can contribute to benchmarking the next-generation cloud infrastructure. We are looking forward to continuing this collaboration with the next in line AMD EPYC processor-based cloud instances as well as with other infrastructure innovations from AMD,” said Yiftach Shoolman, Co-Founder and CTO at Redis.

“We are thrilled to team with Redis to showcase how AMD EPYC processors can deliver high performance for the Redis database solutions used by a variety of demanding enterprise applications. The core density and large memory capacity of AMD EPYC™ processors can optimally scale and serve the growing needs of multi-model based NoSQL databases in real-time,” said Raghu Nambiar, Corporate Vice President, Data Center Ecosystems and Applications, AMD. “By collaborating with Redis we want to showcase how enterprises can get breakthrough database performance by optimizing Redis and Redis Enterprise to take advantage of innovations in AMD EPYC™ processors.”

## Adding AMD to a prestigious list of partners

The AMD and Redis collaboration agreement adds AMD to the list of prestigious tech companies—including Intel and Samsung, as well as the major cloud service providers and many innovative startups—that utilize Redis Enterprise for testing and benchmarking next-generation infrastructure products in the areas of persistent memory, SSDs, storage engines, and network adaptors.

For this first engagement, AMD engineers used the[ memtier_benchmark](https://github.com/RedisLabs/memtier_benchmark), an open source load-generation tool developed by Redis, for benchmarking NoSQL datastores like Redis and Memcached.

The goal of this benchmark was to see how many operations per second a single C5a instance, across multiple instance sizes, can perform while keeping latency at sub-millisecond levels. Redis Enterprise’s shared-nothing architecture allows running a Redis cluster across all cores of a cloud instance, for achieving maximum throughput at a linear scale. That is, the throughput grows linearly as more cores are added and without affecting the sub-millisecond latency.

To validate this level of performance and scalability with the new C5a instance, AMD engineers set-up memtier_benchmark with five runs on each C5a instance under test, and the scores reflect the medians of all runs, as shown in the chart below:

![Redis](/images/blog/fff8fcca391ec674e90c773e0a1736d0b64fb15c-998x660.webp)

These results demonstrate the exceptional throughput performance and linear scalability among the different instances, making it clear that Redis running on AWS C5a instances can help boost application performance and can easily scale with application growth.

## What’s next for AMD and Redis Enterprise?

Going forward, AMD engineers plan to perform a scale-out benchmark to demonstrate that linear scalability can also be achieved by adding more instances to the cluster, not just by scaling up the instances. Stay tuned: We look forward to sharing the results as they become available.

To learn more, visit:

- [AMD EPYC™ 7002 Series Processors in the Cloud: RedisTM on AWS C5a Instances](https://www.amd.com/system/files/documents/epyc7002-awsc5a-redis.pdf) (benchmark results)
- [Amazon EC2 Instances Featuring AMD EPYC™ Processors Solution Brief](https://d1.awsstatic.com/diagrams/AMD_SolutionBrief_Final.pdf)
- [AMD EPYC™ Tech Docs and White Papers – AWS](http://www.amd.com/cloud/aws/solutions)
- [AMD EPYC™ Tech Docs and White Papers – All](https://www.amd.com/en/processors/server-tech-docs/search)
- [Amazon EC2 Instances Featuring AMD EPYC Processors](https://aws.amazon.com/ec2/amd/) (AWS website)

[i] Max boost for AMD EPYC processors is the maximum frequency achievable by any single core on the processor under normal operating conditions for server systems. EPYC-18

AMD, the AMD logo, EPYC, and combinations thereof are trademarks of Advanced Micro Devices, Inc.
