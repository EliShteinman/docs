---
title: "Benchmarking  Redis Enterprise 5.2.0  vs. Hazelcast 3.9"
linkTitle: "Benchmarking  Redis Enterprise 5.2.0  vs. Hazelcast 3.9"
url: "/blog/benchmarking-redis-enterprise-5-2-0-vs-hazelcast-3-9/"
description: "Hazelcast has published two benchmarks comparing its system against the Redis open source database:"
date: 2018-08-30
blogCategories:
- "Benchmarks"
- "Company"
authors:
- "Redis  "
lastmod: 2025-03-27
hidden: true
---

*By Redis   · Published 30 August 2018 · updated 27 March 2025*

![Blog tile image](/images/blog/0073e867b4e64f59de9047fdcde04295ba647e5c-772x550.webp)

## Background

Hazelcast has published two benchmarks comparing its system against the Redis open source database:

- [The first](https://hazelcast.com/resources/benchmark-redis-vs-hazelcast/) (released on May 20, 2016) unfairly compared four standalone instances of open source Redis 3.0.7 running over the network with a Hazelcast IMDG 3.6 4-node cluster running in a near-cache mode.
- The second (released on April 4, 2017) compared Redis open source cluster version 3.2.8 (with 48 master and 48 slave instances running over a 3-node cluster) with a Hazelcast IMDG 3.8 3-node cluster, both running over the network.

Recently, multiple prospects and customers have asked us to run a similar benchmark (over the network) between Redis Enterprise and Hazelcast. Given that Redis Enterprise clusters are based on a different architecture than open source clusters (as further explained [here](/redis-enterprise/technology/redis-enterprise-cluster-architecture/)), we wanted to see if there would be any differences in these results.

## Benchmark setup

At first, we aimed to reproduce the exact same benchmark setup used by [Hazelcast](/comparisons/redis-enterprise-vs-hazelcast/), but they apparently used proprietary hardware. As a company born in the cloud, here at Redis we do not host a single server in-house, and thus decided to look for a similar server configuration on AWS. Here is the setup we used:

## Hardware Configuration

| Parameter | Value |
|---|---|
| Server & client machines | EC2 instance of type m4.10xlarge: Intel E5 160GB RAM 10Gb Xeon E5-2676 RAM: 160GB of memory Network: 10Gbps Ethernet |
| Number of server machines | 3 |
| Number of client machines | 3 |

## Software and Cluster Configuration

|  | Redis Enterprise | Hazelcast |
|---|---|---|
| OS version | Ubuntu 16.04 |  |
| Cluster version | 5.2.0 | 3.9 |
| Cluster configuration | 48 masters + 48 slaves (16 + 16 on each node) 16 proxy threads on each cluster node | 3 members |

## Load generation tool

In its benchmarks, Hazelcast used [*RadarGun*](https://github.com/radargun/radargun) to orchestrate the load generated against both Hazelcast and Redis. In the Redis case, *RadarGun* launched a [Jedis cluster](https://github.com/radargun/radargun/blob/master/plugins/redis32/src/main/java/org/radargun/service/RedisClientService.java) and used a configuration file similar to [this](https://github.com/radargun/radargun/blob/master/extensions/cache/src/main/resources/benchmark-redis.xml) (although we couldn’t find the exact setup in [this](https://github.com/GhostInAMachine/radargun/tree/redis) fork that Hazelcast listed).

Using the right tool to test a product is crucial for running a successful benchmark. For instance, most experts would prefer to test Redis with a [pipelining technique](https://redis.io/topics/pipelining), as this speeds up Redis and is used by a large portion of Redis users. However, we didn’t find a pipeline configuration in the Hazelcast benchmarks.

We therefore opted for the following approach:

- Use the *RadarGun* orchestrator to test Hazelcast (we made the assumption that since it was selected by Hazelcast, the company was probably satisfied with the benchmark results it produced for its system).
- Use [*memtier_benchmark*](https://github.com/RedisLabs/memtier_benchmark) (an open source load generation tool for Redis and Memcached) to test Redis, with the Redis Cluster API.

## Load generation configuration

|  | Redis Enterprise | Hazelcast |
|---|---|---|
| Version | memtier_benchmark version 1.2.8 | RadarGun version 3.0.0 |
| Number of threads per client | 64 |  |
| Read:Write ratio | 80:20 |  |
| Number of objects | 4 million |  |
| Object size | Strings with a random distribution of lengths between 100 bytes and 10,000 bytes |  |
| Total dataset size | 42GB |  |
| Command line used | memtier_benchmark –cluster-mode -s <ip_address> -p <port_number> –key-maximum=4000000 –test-time=900 –data-size-range=100-10000 -c 1 -t 64 –pipeline=5 –key-pattern=P:P –ratio=1:4 –distinct-client-seed | dist.sh -c benchmark-hazelcast-server.xml -t -u ubuntu -o `pwd` -m ip-radargun:2103 ip-server-1 ip-server-2 ip-server-3 ip-client-1 ip-client-2 ip-client |

## Benchmark results

The results of our benchmark are presented below:

![](/images/blog/8bda5e31a0ce8c0e51031b68715e3163ce517043-1231x761.webp)

![](/images/blog/c93a3a5aea22fa3ea8d1e11cc811a18c363acb63-1243x768.webp)

## Summary

We re-ran the benchmark comparing Hazelcast against Redis over the network with two major changes:

1. This time, we tested a Redis Enterprise cluster as opposed to the open source version of Redis.
1. We used the *memtier_benchmark* load generation tool rather than *RadarGun *to test Redis Enterprise with the open source Redis Cluster API.

We found the results for Hazelcast’s performance to be very similar to (or better than) what the company published [here](https://hazelcast.com/resources/benchmark-redis-vs-hazelcast/). Therefore, we tend to believe the Hazelcast cluster and the *RadarGun* orchestrator were configured correctly.

On the other hand, our findings reached a much better throughput (over 3.5X) and latency (~3X) for the Redis Enterprise cluster than those from Hazelcast. We think these differences were related to:

1. Hazelcast using an inappropriate tool to benchmark Redis (we also think that if their team had used the right load generation tool, Hazelcast’s open source benchmark would have shown much better results for Redis); and
1. Redis Enterprise being designed to work well with a combination of pipelining and the open source cluster API.

## Appendix

#### Redis Enterprise results

![](/images/blog/564cda307902da49da9fb331d85d9931d3f81c15-1004x783.webp)

#### Hazelcast results

![](/images/blog/761a833edb013941b72b5ef8675d36126996aae9-606x736.webp)

![](/images/blog/e1972939879c224c2eff972e4be5b3de5f534eca-606x730.webp)

#### 

#### RadarGun benchmark orchestrator


If you have questions related to this benchmark, please feel free to email me: *keren at redis.com*. If you would like to find out more about Redis Enterprise, visit [here](/redis-enterprise/) or email *product at redis.com*.
