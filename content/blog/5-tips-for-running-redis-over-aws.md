---
title: "5 Tips for Running Redis over AWS"
linkTitle: "5 Tips for Running Redis over AWS"
url: "/blog/5-tips-for-running-redis-over-aws/"
description: "Cloud computing can help host an application in a way that is both scalable and cost effective. The leading vendor in the infrastructure as a service (IaaS) arena is Amazon Web Services (AWS),..."
date: 2014-08-06
blogCategories:
- "Tech"
authors:
- "Itamar Haber"
lastmod: 2025-03-27
hidden: true
---

*By Itamar Haber, Technology Evangelist · Published 6 August 2014 · updated 27 March 2025*

![Blog tile image](/images/site-mirror/0073e867b4e64f59de9047fdcde04295ba647e5c-772x550.webp)

![redis aws 5 tips](/images/site-mirror/90010520753602d9c42095adac1c2aeea0ee7bfa-800x252.webp)

Cloud computing can help host an application in a way that is both scalable and cost effective. The leading vendor in the infrastructure as a service (IaaS) arena is Amazon Web Services (AWS), which offers scalable, highly available and secure cloud hosting with Redis. If your application uses Redis for caching or data storage, below are a few tips which will help you save time, money, and achieve better performace with redis on aws with AWS Redis.

### Tip #1: Choosing an EC2 Instance with Redis AWS

When applicable, [hardware virtual machine (HVM) enabled instances](/blog/benchmarking-the-new-aws-m3-instances-with-redis) (e.g., second generation M3 instances and R3 memory-optimized instances) should be used to reduce latency issues due to fork times and in order to run multiple Redis servers on different cores.

Non-HVM EC2 instances use the Xen hypervisor, which is [much slower](/blog/testing-fork-time-on-awsxen-infrastructure) when it comes to forking large processes. Redis’ persistence options, RDB and AOF, both fork the main thread and launch background rewrite or save processes. When forking involves a large amount of memory, it can increase Redis’ latency significantly.

Multiple cores on the same machine can also be used to deploy a number of Redis instances. In this set up, since each Redis instance manages a smaller dataset, per-database forking times can be further mitigated.

### Tip #2: Disable Swapping with Redis AWS

Swapping is an operating system mechanism that attempts to efficiently use RAM. However, seeing as Redis AWS is an in-memory database, in order to provide top performance, all data must be kept in RAM.

With swapping enabled, Redis on aws may attempt to access memory pages that are on disk. This will cause Redis’ process to be blocked by the I/O operation of the disk, which can be a slow process since it involves random I/Os. By chaining Redis to disk performance, your are likely to experience a latency increase. To mitigate this, you can configure the following options in Linux in /etc/sysctl.conf:

```javascript
vm.swappiness=0
vm.overcommit_memory=1
```

For Redis AWS, this means that when the memory is almost full, the kernel will try to steal pages from cache instead of swapping out of program to memory. Use these settings, along with Redis’ maxmemory and maxmemory-policy directives, to prevent Redis AWS from denying writes or the kernel’s out of memory manager (OOM) from terminating Redis.

### Tip #3: Redis AWS Persistence with Elastic Block Store

EC2 instances are equipped with ephemeral storage, with EBS as the de facto standard storage for persistent data in AWS. Keep in mind that EBS is network-attached storage. Therefore, if you are persisting data to the volumes, EBS competes with Redis over network bandwidth. There is a chance that extra I/O and limited bandwidth may affect [Redis’ performance when using EBS](/blog/does-amazon-ebs-affect-redis-performance). Nonetheless, this, too, can be reduced in a number of ways, including:

- Using large EBS volumes for dedicated-like performance.
- Using RAID over EBS configuration.
- Delegating persistence to a replicated slave (be careful of [replication loops](/blog/the-endless-redis-replication-loop-what-why-and-how-to-solve-it) and mind [these](/blog/top-redis-headaches-for-devops-replication-buffer) [tips](/blog/top-redis-headaches-for-devops-replication-timeouts)).
- Using EBS-optimized instances to improve performance as a result of dedicated bandwidth between EC2 instances and EBS.
- Last but not least – reviewing your application’s persistency requirements and tuning Redis’ persistency to fit them.

### Tip #4: For Datasets < 4GB, Use 32-Bit Instances with Redis AWS

If your data’s maximum size is less than 4GB per instance, by saving bits, you can also save money. When compiling and running Redis on a 32 bit target, it uses less memory per key, since the pointers are smaller.

If you are unsure of the size of your dataset, use the [INFO](https://redis.io/commands/info) command to get the relevant numbers (e.g. used_memory). You can also use a benchmarking tool, such as [redis-benchmark](https://redis.io/topics/benchmarks) or [memtier-benchmark](https://github.com/RedisLabs/memtier_benchmark), to generate random datasets for guesstimations.

Remember that the size of your dataset is not the only consideration when planning the overall RAM for a Redis AWS server. For example, in case you have enabled persistence or replication, a background memory thread will periodically create a copy of the data, which will be in-memory at that point. Any data then remains in-memory until the operation is complete and therefore, any update operation on the data/key being copied requires extra memory in the form of memory pages and [buffers](/blog/top-redis-headaches-for-devops-replication-buffer). A “worst case” scenario, where all keys are updated during this period, may require twice or more memory than what would have been required without persistence and/or replication. To provision against running out of memory in such a scenario, **use a factor of 2 at the very least** on the actual dataset’s size.

### Tip #5: Use Sharding to Properly Utilize Multi-Core EC2 Instances

The final tip comes full circle, picking up from where tip #1 left off. Redis is a (mostly) single-threaded process, which means that each Redis process can use a single core, at the very most. To make better use of EC2 instances with multiple cores, you can start one Redis process for each core of a server and efficiently utilize the extra cores. These extra servers can act as independent Redis servers. For example, one can be utilized to manage user session data while another one can be used to cache user profiles. An alternative approach for harnessing these multiple cores is to shard the data between servers.

Sharding is a big topic, in and of itself, and we’ll dedicate more time to it in the upcoming weeks. Prepare yourself for the drama associated with choosing between the application-side, client-assisted, by proxy or via cluster sharding. Learn the horrible truths about sharding for yourself and how to battle them bravely. Understand how to take Redis to the next step. Have questions about Redis on AWS? Feedback on Redis AWS? [Email](mailto:itamar@redis.com) or [tweet](https://twitter.com/itamarhaber) me – I’m highly available 🙂
