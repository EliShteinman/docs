---
title: "Is Amazon PIOPS Really Better than Standard EBS?"
linkTitle: "Is Amazon PIOPS Really Better than Standard EBS?"
url: "/blog/is-amazon-piops-really-better-than-standard-ebs/"
description: "UPDATE: read our followup post Take #2 – Is Amazon SSD PIOPS Really Better?"
date: 2012-10-04
blogCategories:
- "Tech"
authors:
- "Redis  "
lastmod: 2025-03-27
hidden: true
---

*By Redis   · Published 4 October 2012 · updated 27 March 2025*

![Blog tile image](/images/blog/0073e867b4e64f59de9047fdcde04295ba647e5c-772x550.webp)

**UPDATE:** read our followup post [Take #2 – Is Amazon SSD PIOPS Really Better?](/blog/take-2-is-amazon-ssd-piops-really-better)

Two months ago, Amazon launched its EBS Provisioned IOPS (PIOPS) for running high performance databases in the cloud, and introduced EBS-Optimized instances to deliver dedicated throughput between EC2 and EBS. As the provider of the [Redis Cloud](http://redis-cloud.com) service, we wanted to know whether the PIOPS EBS with EBS-Optimized instances would really perform better than Standard EBS with non-optimized instances for Redis. Note – recently, Amazon released their new RDS Provisioned IOPS. However, it is not applicable to Redis and is therefore not addressed in this post.

Running Redis on AWS has been [a challenge](https://groups.google.com/forum/?fromgroups=#!searchin/redis-db/Amazon/redis-db/c8NI6gVy4Fk/ZJLsczoVGicJ) for Redis users, mainly due to EBS’ slow and unpredictable network and I/O throughput. Though Redis is a pure in-memory datastore system and serves everything from RAM, it also has two [persistent-storage mechanisms](http://antirez.com/post/redis-persistence-demystified.html) for better durability: AOF (Append Only File) and Snapshotting. These mechanisms are very efficient when interfacing with persistent storage, as they only use sequential writes with no seek time. As a result, Redis can run pretty well with data-persistence even on non-SSD hardware.

That being said, we decided to conduct some benchmarks for Amazon’s EBS PIOPS because slow storage devices can still be very painful for Redis. We see this when the AOF “fsync every second” policy blocks an entire Redis operation due to slow disk I/O. In addition, background saving for point-in-time snapshots or AOF rewrites takes longer, and therefore more memory is used for copy-on-write — leaving less memory available for your app. You may have seen the [detailed post](http://www.stratalux.com/?p=1511) from [Strattalux](http://www.stratalux.com/) comparing the performance of PIOPS EBS vs. Standard EBS using EBS-Optimized and non-Optimized instances. While their tests were interesting, we thought we’d dig a little deeper and examine whether the performance of a simple Redis application is influenced by different storage architecture. Therefore, we were very specific and only tested the performance of sequential writes, ignoring other scenarios like random read/write and sequential read.

For our benchmark, we also reviewed cost implications, and used what we believe is a more optimal performance configuration of Standard EBS (1 x 1TB EBS volume vs. 10 x 100 GB RAID0 EBS, per a very educational blog about [Standard EBS performance](http://perfcap.blogspot.co.il/2011/03/understanding-and-using-amazon-ebs.html) by Adrian Cockcroft from Netflix). So, without further ado, here are the details of our tests…

**Benchmark Setup** We used the following setup: PIOPS EBS with Optimized-Instance (i.e. m2.4xlarge with EBS-Optimized attribute set to true) vs. Standard EBS with non-Optimized Instance (m2.4xlarge with EBS-Optimized attribute set to false). We also tested another setup in which we compared PIOPS EBS vs. Standard EBS on a non Optimized-Instance (m2.2xlarge). Our intention was to see whether AWS users who cannot use the EBS Optimized-Instance for various reasons (such as cost) can get benefit from the new PIOPS EBS. Those results were very similar to the setup described above. For all tests, we used 2 x m1.xlarge instances that run our memtier_benchmark load generation tool (memtier_benchmark is an advanced load generator tool we developed for testing Redis and Memcached datastores, which we will soon share in our [github](https://github.com/GarantiaData) account). We ran 8 tests on each configuration to simulate a Redis application, then ran each of these tests 3 times and calculated the average results. Our tests combinations included:

1. 100 and 500 connections on each load-generator machine (200 and 1000 connections total)
1. 100B and 1KB object size
1. 50%/50% read/write scenario, and 100% write scenario (for imposing load on EBS)

![](/images/blog/395fa9ebdeb9f523ab539be4cf896ef4c0cd3c8f-573x370.webp)

**Benchmark Results **Note – we have chosen to show the results from the 1KB object size tests, which impose higher load on the EBS. **RPS (Requests Per Seconds)** **Latency** The RPS and Latency results aggregated from our two memteir_benchmark tools are shown above. Our latency tests take into account the network round-trip, the Redis processing time, and the time it takes for the memtier_benchmark tool to parse the result. As you can see, RPS and latency are approximately the same on all tests, though there are some differences which might be due to the fluctuations in the AWS infrastructure during the test time. Needless to say, Redis runs better with fewer disk accesses. **iostats**

The results above are taken from iostats commands executed while the tests were running (here’s a useful [AWS forum post](https://forums.aws.amazon.com/thread.jspa?messageID=124044#124044) that explains how to interpret Linux iostats). We ran iostats every 2.5 seconds and aggregated results from both EBS volumes. These charts only present relevant performance parameters for Redis — “read” parameters were not presented as they were constantly zero during these tests. As you can see, except from few glitches here and there, iostats show approximately the same results for both EBS configurations. **Set-up cost** As mentioned earlier, we wanted to understand the cost implications of the Standard vs. PIOPS EBS options, so we compared the monthly setup costs using Amazon EC2 on-demand prices in us-east-1 (N. Virginia):

|  | Instance Cost | EBS Cost | Total | Comment |
|---|---|---|---|---|
| Setup#1 |  |  |  |  |
| Standard EBS | $648 | $200 + $0.01 (per 1 million I/O) | $848 + $0.01 (per 1 million I/O) | Standard will cost less than PIOPS for up to 37.5K writes/sec (assuming an average of 40 merged requests per I/O with average size of 1KB) |
| PIOPS EBS | $648 | $225 | $873 |  |
| Setup# 2 |  |  |  |  |
| Standard EBS | $1,296 | $200 + $0.01 (per 1 million I/O) | $1,496 + $0.01 (per 1 million I/O) | Standard will cost less than PIOPS for up to 91.5K writes/sec (assuming an average of 40 merged requests per I/O with average size of 1KB) |
| PIOPS EBS | $1,296 + $36 (ebs-optimized) = $1332 | $225 | $1,557 |  |

**Conclusion** After 32 intensive tests with Redis on AWS (each run in 3 iterations for a total of 96 test iterations), we found that neither the non-optimized EBS instances nor the optimized-EBS instances worked better with Amazon’s PIOPS EBS for Redis. According to our results, using the right standard EBS configuration can provide equal if not better performance than PIOPS EBS, and should actually save you money. Keep in mind that these findings represent a specific storage usage pattern (sequential write only), so if you have different storage access patterns, you may want to review the [Stratalux](http://www.stratalux.com/?p=1511) test results (while taking into account the different Standard EBS configuration we suggest). Given these results, we plan to continue running Garantia Data’s clusters on a Standard EBS configuration. We welcome comments from the Amazon EBS Team on our benchmark, and will be sure to share any new information we discover.
