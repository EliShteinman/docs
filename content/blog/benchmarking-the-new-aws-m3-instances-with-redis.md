---
title: "Benchmarking the new AWS M3 instances with Redis"
linkTitle: "Benchmarking the new AWS M3 instances with Redis"
url: "/blog/benchmarking-the-new-aws-m3-instances-with-redis/"
description: "Two weeks ago, Amazon launched its next generation of standard instances (M3 instances), adding twice the computational capability/cores while providing customers with the same balanced set of CPU..."
date: 2012-11-15
blogCategories:
- "Tech"
authors:
- "Redis  "
lastmod: 2025-03-27
hidden: true
---

*By Redis   · Published 15 November 2012 · updated 27 March 2025*

![Blog tile image](/images/site-mirror/584fe8cc1f7f6798f6c888946e07c4abdce2036d-960x720.webp)

Two weeks ago, Amazon launched its next generation of standard instances (M3 instances), adding twice the computational capability/cores while providing customers with the same balanced set of CPU and memory resources as M1 instances. We don’t use the M1 instances in our Redis Cloud clusters (they can’t cope with the high throughput, low latency requirements of Redis as detailed [here](/blog/its-true-even-modest-datasets-can-enjoy-the-speediest-performance#.UKSQ1uPZ_7l)), but wanted to know whether the M3 double extra-large instance (m3.2xlarge) would really perform better than the m2.2xlarge high memory instance that we use in many of our clusters nodes. Both instances come with similar memory configuration and use the same type of vcores, so what intrigues us most is the fact that M3 instances can run in Xen hardware virtualized mode (HVM). Therefore, they should overcome the Xen fork time issues that significantly affect Redis performance (as described in detail [here](https://garantiadata.com/blog/testing-fork-time-on-awsxen-infrastructure)). In-addition, the m3.2xlarge instance has two times the number of vcores as an m2.2xlarge instance at less than 30% additional cost:

| Instance type | Memory size | vcore type | # of vcores | Cost/h (N.Virginia) | Cost vcore/h (N.Virginia) |
|---|---|---|---|---|---|
| m3.2xlarge | 30 GB | 3.25 ECU | 8 | $1.160 | $0.145 |
| m2.2xlarge | 34 GB | 3.25 ECU | 4 | $0.900 | $0.225 |

**Test scenarios** With all of that in mind, we conducted a test comparing Redis performance over m3.2xlarge and m2.2xlarge instances for the following:

- Fork time
- Throughput and latency of pure n-memory configuration
- Throughput and latency with AOF enabled and under normal conditions (with AOF rewrite disabled)
- Replication time

It was important to test replication time, because m3.2xlarge comes without ephemeral storage or, to be more accurate, with only 15GB of local disk size. That means it must be attached to an EBS volume even if no data persistence is required, because the Redis replication process involves writing the entire dataset to persistence storage twice (at the master and then at the slave). Since EBS is slow on sequential writes (see more details [here](/blog/is-amazon-piops-really-better-than-standard-ebs#.UKN9x-PZ_7k)), we wanted to see if and how Redis replication is affected by this configuration. Without further ado, here’s what we found: **Fork time**

| Instance type | Memory limit | Memory used | Memory usage(%) | Fork time | Fork time/GB |
|---|---|---|---|---|---|
| m3.2xlarge | 30 GB | 18.7 GB | 62.3 % | 0.25 sec | 0.01 sec |
| m2.2xlarge | 34 GB | 17.3 GB | 50.8 % | 5 sec | 0.29 sec |

As expected, fork time using the m3.2xlarge instance is significant lower than fork time on an m2.2xlarge instance, as it uses Xen’s full virtualization mode (HVM). Similar low fork time results are also seen over AWS Cluster Compute instances (see more info [here](/blog/testing-fork-time-on-awsxen-infrastructure#.UKOgKuPZ_7k)), but at a much higher instance cost. **Throughput and Latency** We compared the throughput and the latency of a single shard Redis on both instances, and this is what we got:


Our insight:

- m2.2xlarge had ~15% higher throughput and ~12% lower latency in every test. This what we expected, because fully virtualized guests (HVM) are usually slower than paravirtualized guests, given the emulation required.
- When we ran Redis over the m3.2xlarge instance with paravirtualized AMI, we saw equal single shard Redis performance, but no improvement in the fork time.
- In an environment with multiple Redis processes (i.e multiple dedicated Redis DBs or multi-shard Redis), we expect m3.2xlarge to run better when the number of active processes exceed the 4 vcores of the m2.2xlarge instance

**Replication time**

| Instance type | RDB file size | Replication time |
|---|---|---|
| m3.2xlarge | 0.6 GB (represents 8GB in-memory dataset) | 88 sec |
| m2.2xlarge | 0.6 GB (represents 8GB in-memory dataset) | 78 sec |

To measure replication time, we started measurement upon connecting the slave to the master, and stopped when the slave was synced. Although we configured the m2.2xlarge instance to use its local disk interface running at 80 MB/s (peak) and the m3.2xlarge to use an EBS interface running at 30 MB/s (peak), the overall replication time of the m2.2xlarge instance was better by only 13%. We believe this is because the population process is consuming most of the time at this size of RDB file. We assume the ratio of the population time to the entire replication process grows linearly to the size of the RDB file. Therefore, the larger a file is, the lower the effect of disk access throughput would be on the entire replication process. The replication of small RDB files is inherently fast, so it is safe to assume that a higher throughput storage interface does not significantly affect the full replication process. **Conclusions** AWS’ new M3 instances with HVM AMI completely eliminate the Xen fork time issues that significantly affected Redis performance during point-in-time snapshots or rewrite Append Only Files (AOFs) background save processes. On the other hand, the performance of a single threaded Redis server over m3.2xlarge instance was ~15% slower than over an m2.2xlarge instance in both pure in-memory and AOF tests. Replication time was also slower with the m2.3xlarge instance, though not significant as we expected. Our recommendation is to use Redis on m3.2xlarge rather than m2.2xlarge only if you run Redis without replication or if you need to run more than four Redis processes on the same instance. For all other cases, we still recommend using the m2.2xlarge instance. **Test setup** For those who want to know more details about our test, here are the resources we used:

- Redis Cloud on the following configurations:
  - 2x m3.2xlarge instances
  - 2x m2.2xlarge instances
- In both configuration we used Standard EBS volumes: 100GB (non-raided)

This was our setup for generating load: m2.2xlarge instance that ran our memtier_benchmark load generation tool (an advanced load generator tool we developed, which we will soon share in our[ github](https://github.com/GarantiaData) account). For testing fork time, we took the following steps:

- We populated the memory with various objects from different data types
- We enabled AOF and waited until the first rewrite operation completed
- We generated high-load on random keys using the memtier_benchmark in order to access as many memory pages as possible
- We performed [GBREWRITEAOF](https://redis.io/commands/bgrewriteaof)
- We read *latest_fork_usec* value of Redis [INFO](https://redis.io/commands/info)

For testing throughput and latency we ran 2 tests:

- With data persistence disabled
- With AOF “fsync every second”

We ran each test three times on each configuration, and calculated the average results using the following parameters:

- 100 connections
- Random 100B-1000B object size
- 1/1 GET/SET ratio

For testing replication, we:

- Disabled data persistence
- Populated the memory with various objects from different data types
- Disconnected the slave server
- Started measuring when reconnecting the slave to the master
- Stopped measuring when the slave was synced
- Simultaneously, we continued generating application load on the master server
