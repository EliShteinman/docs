---
title: "Bringing The Latest Persistent Memory Technology to Redis Enterprise"
linkTitle: "Bringing The Latest Persistent Memory Technology to Redis Enterprise"
url: "/blog/persistent-memory-and-redis-enterprise/"
description: "It’s amazing to think that in the last 50-60 years, the tech industry has only produced around 6-7 classes of memory technology. Even so, each of those memory classes brought different attributes..."
date: 2018-04-25
blogCategories:
- "Announcements"
- "New Product Announcements"
authors:
- "Priya Balakrishnan"
lastmod: 2025-03-27
hidden: true
---

*By Priya Balakrishnan, Sr. Director of Product and Partner Marketing · Published 25 April 2018 · updated 27 March 2025*

![Blog tile image](/images/blog/0073e867b4e64f59de9047fdcde04295ba647e5c-772x550.webp)

## Redis on Flash with Intel® persistent memory based on 3D Xpoint™ NVDIMM — more data per server and better performance than ever before!

It’s amazing to think that in the last 50-60 years, the tech industry has only produced around 6-7 classes of memory technology. Even so, each of those memory classes brought different attributes to the way we store and retrieve data. From RAM in the early days to SRAM, DRAM, NAND Flash, and now to solid-state drives (SSD) and NVMe (Non-Volatile Memory Express), we’ve seen significant improvements to the speed, density, and stability of our data storage options.

[Redis on Flash](/redis-enterprise/technology/redis-on-flash/) (RoF) takes advantage of the increasing availability of high-speed storage in the form of Flash SSDs, resetting existing price/performance expectations. By extending Redis from RAM to Flash, and using intelligent tiering to always keep hot values in RAM, RoF reached [new levels of throughput](/docs/redis-on-flash-with-intel-nvme-benchmark/) while still retaining sub-millisecond latencies. With this innovation, the economics of data stored in Redis changes completely.

We’ve seen many of our customers benefit from this approach. For instance, Whitepages uses our Redis on Flash solution to store and query several terabytes of data – with hot values and keys in RAM, and cold values in cost-effective, flash-based SSDs. This architecture lets them keep only 30% of their dataset in RAM and still achieve less than sub-millisecond latency from Redis (on Flash). In fact, they’re maintaining end-to-end application latencies of <100ms. This substantial reduction in RAM consumption saved Whitepages hundreds of thousands of dollars in infrastructure costs each year.

In the last few years, Intel and Micron have been working on a completely new class of storage and memory technology that is faster, denser and non-volatile, based on 3D XPoint™. Their goal is to improve overall system performance and lower latencies by putting more data closer to the processor on nonvolatile media. At Redis, we’ve been working very closely with Intel to ensure our solutions run optimally with this new technology. We started by benchmarking RoF over Intel Optane, an NVMe SSD card based on the 3D XPoint™ technology, and saw[ significant performance increases ](/blog/redis-enterprise-flash-intel-optane/)over the standard NVMe-based SSD solution. In the past few months, we have been tuning and benchmarking RoF to work with the new form factor of 3D XPoint technology based on NVDIMM.

Intel’s persistent memory based on 3D XPoint technology delivers a new tier between DRAM and SSD that can provide up to 6TB of capacity in a two-socket server at performance comparable to traditional DRAM memory. In addition, Intel has been working with the industry to create a new programming language model for Linux and Windows environments, which would allow applications to directly and persistently engage with data in memory. This means that applications like RoF can decide which part of the dataset will remain purely in DRAM and which part can be hosted on both DRAM and 3D XPoint™. As part of this effort, we’ve redesigned our RoF code path to maximize performance gains from the new technology. We use the embedded storage engine in the main Redis thread and [Intel’s DAX](https://www.kernel.org/doc/Documentation/filesystems/dax.txt) to access the NVDIMM. This helps reduce internal bottlenecks and eliminates the overhead associated with context switching between the Redis main thread and the I/O threads that are used to run the storage engine.

*The end result – Redis on Flash users may see performance comparable to DRAM, even if over 80% of the dataset is stored on NVDIMM. This translates to a significantly lower total cost of ownership.*

**Why is this important to users of Redis?**

Persistent memory allows you to think of memory as the main storage tier for your data. Operating at the speeds promised by the new Intel NVDIMM technology will be a game changer for Redis users. When this starts shipping with servers, customers won’t just gain a fast, persistent data store that’s closer to the CPU and memory. With RoF, they’ll also gain the ability to extend their “memory.”

Additionally, if Redis users have limited themselves because of the cost of memory, that thinking is about to change. Keeping data in memory is about to get even cheaper. The new persistent memory tier allows you to keep more data per node, delivering a significant reduction in infrastructure costs while maintaining performance.

**Does this mean that not only Redis but every other DBMS can now enjoy the new speed introduced by 3D XPoint™ technology?**

Actually, this is a misconception, because your DBMS must be optimized to work with the new technology. In fact, when we first started to work with 3D XPoint™, we saw zero impact on performance versus the tests we’d done over Intel Optane™ (NVMe-based SSD card based on 3D XPoint™). That was due to the fact that our entire software stack and storage engine were not designed to work with this level of speed of persistent memory. That said, since Redis is based on an in-memory engine (all its data structures are byte-addressable, with no special serialization/deserialization processes), it was relatively easy to adapt the RoF stack to work with NVDIMM (which is also byte-addressable by design).

Existing disk-based databases built their entire engines on storage engines that were not designed to be byte-addressable. Their serialization/deserialization overheads and the long access time to their internal disk-based data-structures will prevent them from achieving the expected performance boosts when running on this revolutionary technology.

Moving the majority of processing infrastructures to 3D Xpoint™ technology won’t happen overnight, but it is an event you need to be prepared for. We believe that once 3D Xpoint™ technology becomes mainstream, the majority of the database market will have to move to being in-memory. There will simply be no more reason to continue using disk-based databases. As a developer or software architect, you should start thinking about moving your application code to work natively with in-memory databases, like Redis. The sooner you do, the better you’ll position yourself against your competitors.
