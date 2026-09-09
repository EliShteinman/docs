---
title: "Redis Enterprise for Kubernetes Now Supports Flash Memory"
linkTitle: "Redis Enterprise for Kubernetes Now Supports Flash Memory"
url: "/blog/redis-on-kubernetes-redis-on-flash/"
description: "Redis on Flash works with Redis Enterprise for Kubernetes. That’ll speed up your software – and save your company money."
date: 2022-11-03
blogCategories:
- "New Product Announcements"
- "Tech"
authors:
- "Brad Ascar"
lastmod: 2025-03-27
hidden: true
---

*By Brad Ascar, Contributor · Published 3 November 2022 · updated 27 March 2025*

![Blog tile image](/images/site-mirror/61093b5c4d24f242d211564632a31487b6a22bbf-772x550.webp)

**Redis on Flash works with Redis Enterprise for Kubernetes. That’ll speed up your software – and save your company money.**

One exciting feature in Redis Enterprise is called [Redis on Flash](/redis-enterprise/technology/redis-on-flash/) (RoF). RoF enables databases to extend DRAM capacity using [Flash memory](https://www.techtarget.com/searchstorage/definition/flash-memory) or [solid-state drives](https://www.symmetryelectronics.com/blog/the-development-and-history-of-solid-state-drives/) (SSDs).

Ordinarily, Redis Enterprise keeps an entire dataset in DRAM. That is good for most purposes, but it becomes an issue when a dataset is prohibitively large. However, when you use RoF, far less information is stored in DRAM: the keys, the Redis dictionary (the data structure behind the keys), and the dataset’s frequently accessed data (also called “hot data” or the working set). DRAM is still the faster tier, which is why it holds the critical data.

However, with RoF the inactive data (also called “the warm values”) are moved to the lower tier, the local Flash storage tier.

RoF is based on a multi-threaded asynchronous architecture that guarantees no blocking between a heavy caching request made to Flash and a light caching request made to DRAM. That avoids head-of-the-line blocking scenarios resulting from the single-threaded nature of Redis Enterprise.

Redis on Flash is not designed as an alternative mechanism for data persistence. The same Append Only File and snapshot data-persistence mechanisms, persisting data to disk, are used with RoF as with Redis Enterprise.

![](/images/site-mirror/c24d5ecd071f21b1ede0c8c0d2a4b2d669d1b930-767x294.webp)

So far, so good. We’ve had RoF for several years. Beyond its technical merit, [RoF has saved companies a lot of money](https://www.youtube.com/watch?v=hFQnhPstqLM).

## Redis on Flash is now available in Redis Enterprise for Kubernetes

However, RoF wasn’t part of our Kubernetes offering – until now.

RoF is now available for Redis Enterprise for Kubernetes, starting with version 6.2.12 (option to enable) and with 6.2.18 due in mid November – a boon for customers with large datasets. Even when a RAM-only solution works technically, it often is cost-prohibitive, and customers would prefer to use Flash.

Just as with RoF on non-Kubernetes clusters, there are, of course, storage prerequisites. The underlying hardware needs to be performant and directly attached to the Kubernetes cluster node. Kubernetes also has a particular way to use storage, so be sure to follow the setup guidelines to ensure a smooth installation.

After the prerequisites, the rest of what you do in Redis Enterprise for Kubernetes feels like any other operation. We extended the usual way you create and use [Redis Enterprise Cluster](/redis-enterprise/technology/redis-enterprise-cluster-architecture/) (REC) and Redis Enterprise Database (REDB) by adding YAML to express the configuration.

## RoF configuration basics

Getting started is remarkably easy. All you need is a simple configuration inside Kubernetes to use this powerful capability. Simple, fast, and efficient. What else could you ask for?

To turn on this feature, add these lines to a REC:

```yaml
redisOnFlashSpec:
   enabled: true
   flashStorageEngine: rocksdb
   storageClassName: local-scsi
   flashDiskSize: 100G

```

This code example turns on RoF for the cluster, then sets the storage engine, the Kubernetes storage class, and the amount on disk for this cluster node.

Similarly, you turn on RoF support for your database by adding these lines to the REDB spec:

```yaml
 isRof: true
 memorySize: 2GB
 rofRamSize: 0.5GB

```

With these instructions, you tell REDB to use RoF by turning it on, identifying how much memory to allocate for the database size, and how much you want in RAM.

Naturally, there are options, and some of them are mighty important. For instance, the setting here for how much data is in RAM directly impacts performance. Don’t merely copy the example above; there are configuration guidelines, so take the time to read the documentation for [Redis on Flash configuration](https://docs.redis.com/latest/rs/databases/redis-on-flash/) and the [Kubernetes-specific details](https://docs.redis.com/latest/kubernetes/re-clusters/redis-on-flash/).

Happy RoF-ing, and have a great day!

## Related resources

- [Deploy Redis Enterprise Software for Kubernetes](https://docs.redis.com/latest/kubernetes/deployment/quick-start/)
- [Redis Enterprise Software on Kubernetes Operator-based Architecture](https://docs.redis.com/latest/kubernetes/architecture/operator/)
- [Deploy Redis Enterprise Software for Kubernetes with OpenShift](https://docs.redis.com/latest/kubernetes/deployment/openshift/)
- [Redis Enterprise Software for Kubernetes](https://docs.redis.com/latest/kubernetes/)
- [Upgrade a Redis Enterprise cluster (REC) on Kubernetes](https://docs.redis.com/latest/kubernetes/re-clusters/upgrade-redis-cluster/)
