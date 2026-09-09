---
title: "Take #2 – Is Amazon SSD PIOPS Really Better?"
linkTitle: "Take #2 – Is Amazon SSD PIOPS Really Better?"
url: "/blog/take-2-is-amazon-ssd-piops-really-better/"
description: "For many of today’s applications, disk speed is extremely important, which is why some AWS users turn to the wide range of available Elastic Block Store (EBS) options. As an in-memory database,..."
date: 2014-11-03
blogCategories:
- "Tech"
authors:
- "Guy Lubovitch"
lastmod: 2026-08-13
hidden: true
---

*By Guy Lubovitch · Published 3 November 2014 · updated 13 August 2026*

![Blog tile image](/images/site-mirror/9354934247cd6901f97833ee9ab8fb067894a249-635x200.webp)

![](/images/site-mirror/d50aef6ad4e5f3f51359c31d5ef214af0b0d0443-635x200.webp)

For many of today’s applications, disk speed is extremely important, which is why some AWS users turn to the wide range of available Elastic Block Store (EBS) options. As an in-memory database, Redis relies mainly on memory, rendering disk speed less important, but – and this is a big ‘but’ – Redis is also persistent and uses disk for replication. So is it worth paying extra bucks to get a faster disk from AWS when you’re already running Redis servers?

Our initial assumption was “NO,” primarily because Redis uses sequential writes when creating AOF files, and when you perform replication it just dumps the memory into the disk. Neither of those operations exploit the fast allocation of SSD or the advantages of PIOPS. Two years ago we conducted some tests that [proved our hypothesis](/blog/is-amazon-piops-really-better-than-standard-ebs), and recently we tested it again to check whether the results have changed.

### The Tests

I created three benchmarks to compare EBS disk speeds against plain magnetic disk, EBS with SSD and EBS with SSD PIOPS. The benchmark was done on three nodes, each with its own EBS and our Redis Clouds service installed on top of it. I wanted to use the optimal configuration for PIOPS so I chose the c3.4xlarge instance type (more about that [here](https://aws.amazon.com/blogs/aws/enhanced-ebs-throughput/)). I configured Redis to write the its append-only file every second (i.e. appendfsync everysec), which is the default setting for AOF and is considered the common use case. Lastly, I did not use replication to avoid unneeded network noise, the focus of this benchmark being disk usage.

### The Setup

Our client machine’s instance type was c3.2xlarge and I used our home-grown [memtier_benchmark](/blog/memtier_benchmark-a-high-throughput-benchmarking-tool-for-redis-memcached) tool to simulate the workload.

The benchmark run had performed write operations exclusively . I used 10KB objects and had the benchmark use 50 concurrent connections and a pipeline size of 25. For your reference, here are the command line arguments that I used with memtier_benchmark:

–ratio=1:0 –test-time=120 -d 10000 -t 1 -c 50 –pipeline=25

The ratio was set for write (SET) operations only and the test’s time was 2 minutes. I ran each test twice, once with a single thread and once with 4 threads, because I wanted to examine the affect (if any) that the number of threads has.

### The Results

To my surprise, these benchmarks showed that running Redis on SSD and SSD PIOPS performs much better than it does with magnetic disk:

![](/images/site-mirror/5e5f37d78e0a63a800feca14137f2ec97c33c43b-710x632.webp)

The logic had remained the same and disk physics have not changed – by itself, magnetic EBS should provide similar throughput and latency to that of SSD EBS. But we found that using SSD EBS will get you better hardware and a faster network, which will **double** the performance. Note that increasing the number of memtier_benchmark client threads from 1 to 4 had caused performance to degrade, demonstrating that we’ve effectively saturated the EBS device.

If your durability requirements are stringent, it pays to pay more for faster disks. Additionally, you can increase the storage’s throughput by attaching multiple EBS volumes but this approach was not tested in this benchmark. Another approach for increasing the transactions per second (TPS) score from your Redis setup is to delegate persistence to a slave instance, thus freeing the master to do actual data processing. Note, however, that replication may add load to your network and may reduce the consistency of your database.

### Additional Findings

I’ve used Linux’s iostats to monitor the write throughput for each storage configuration during the benchmark’s run. Once each run was over, I’ve also triggered a manual snapshot (the [SAVE](https://redis.io/commands/save) command) and monitored its write throughput as well. Here are the results:

Analysis:

1. AOF is approximately twice as fast as snapshots with high-throughput EBS devices. This can be explained by the fact that by default the snapshot process performs on-the-fly compression to the RDB file that it creates, which delays the I/O write throughput. The more performant the EBS volume is (i.e. SSD), the throughput ratio becomes favorable for AOF activity since the bottleneck moves from EBS access to the CPU.
1. It is somewhat perplexing to note that while SSD PIOPS’ write throughput is x4.5 that of magnetic disk (96.2MB/sec vs 21.3MB/sec), it performs only x2 as fast in the end-to-end memtier_benchmark results (10484 writes/sec vs. 5214 writes/sec). This can be explained by the effects of file system caching as well as comments provided in [this post](http://oldblog.antirez.com/post/fsync-different-thread-useless.html) from Salvatore.

### Conclusion

Although SSD storage is optimized for random access rather append-only write patterns (the latter being Redis’ modus operandi), we were pleasantly surprised to find that it is in fact more performant than magnetic disks for our purposes. Furthermore, AWS’ SSD PIOPS indeed deliver better throughput compared to the regular SSD offer. The AWS team deserves a big kudos for this amazing service offering and our recommendation is: if you’re running Redis on EC2 and need data persistence, your money will be well spent on PIOPS SSD EBS volumes.
