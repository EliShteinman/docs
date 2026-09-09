---
title: "How Intel’s persistent memory and Redis is a game changer in the Database industry"
linkTitle: "How Intel’s persistent memory and Redis is a game changer in the Database industry"
url: "/blog/how-intels-persistent-memory-and-redis-is-a-new-game-changer-in-the-database-industry/"
description: "Over the past decade, our customers have used Redis in some amazing ways—as a cache (of course!), session store, message broker, recommendation engine, secondary index, streaming platform, and,..."
date: 2019-04-02
blogCategories:
- "Benchmarks"
- "Company"
authors:
- "Priya Balakrishnan"
lastmod: 2025-03-27
hidden: true
---

*By Priya Balakrishnan, Sr. Director of Product and Partner Marketing · Published 2 April 2019 · updated 27 March 2025*

![Blog tile image](/images/site-mirror/9cfd4545e40037bd936f64d27531c54867a58bad-600x600.webp)

Over the past decade, our [customers](/customers/) have used Redis in some amazing ways—as a [cache](/solutions/caching/) (of course!), [session store](/solutions/session-management/), [message broker](/solutions/messaging/), recommendation engine, secondary index, streaming platform, and, increasingly, single source of truth database. Redis’ extreme versatility across countless scenarios is due to its ability (unlike any other database in the market) to process data and deliver insights at sub-millisecond speeds, irrespective of data volume.

The ability of Redis to instantaneously process data represents the future of all databases, but the performance efficiency gained by in-memory computing can sometimes come at a cost (literally!), especially if the volume of data needed for instant processing is substantially large and resides in DRAM. It was with this consideration that Redis introduced [Redis on Flash](/redis-enterprise/technology/redis-on-flash/) in 2016. Redis on Flash stores Redis keys, data dictionaries, and “hot” (frequently accessed) data in RAM, and “cold” data on Flash SSDs, all while still maintaining sub-millisecond performance. Many of our customers including Whitepages, Malwarebytes, Dynamic Yield, [BioCatch](/customers/biocatch/), Inovonics, and [Etermax](/customers/etermax/), all representing a variety of use cases with data sets in the terabytes, have achieved 40-80% savings on infrastructure costs with Redis on Flash.

But even with the incredible success of Redis on Flash, we have not remained complacent. Redis has been [working very closely with Intel](/blog/persistent-memory-and-redis-enterprise/) to ensure that their latest game-changing memory technology— Intel® OptaneTM DC persistent memory—is immediately available to Redis Enterprise users upon its general release with the second-generation Intel® Xeon® Scalable platforms. Which is happening now! And we’re ready!

### What is Intel Optane DC Persistent Memory?

[Intel Optane DC Persistent Memory](https://www.intel.com/content/www/us/en/products/docs/memory-storage/optane-persistent-memory/overview.html) delivers a new persistent memory tier between DRAM and SSD that can provide up to 6TBs of non-volatile memory capacity in a two-socket server plus up to 1.5TB of DRAM,—at a performance level comparable to traditional DRAM memory. More simply put, this new tier extends a standard machine’s memory capacity to up to 7.5TBs of byte-addressable memory (DRAM + persistent memory), while providing persistence. This technology comes in a DIMM form factor and is available as a 128, 256, and 512GB persistent memory module.

![](/images/site-mirror/942ca94b6c388ecc48b2a86a5fb2811f44986b6f-1024x606.webp)

*Reimagining the data center memory and storage hierarchy*

## Benchmark Testing Shows 43% Cost Savings

If you’ve been limiting your use of Redis because of memory costs, you no longer need to agonize over the trade-off. Intel Optane DC persistent memory allows you to keep more data per node, dramatically reducing your infrastructure costs while maintaining performance SLAs, keeping sub-millisecond latency at high throughputs of 1M ops/sec – a typical throughput for Redis Enterprise customers.

How do we know? We worked with [Intel to test Redis Enterprise](/blog/redis-intel-performance-testing/) on its new persistent memory tier:

|  | Test 1 | Test 2 |
|---|---|---|
| Memory configuration | 1.5TB DDR4 DRAM Memory | 192GB DDR4 DRAM Memory + 1.5TB Intel Optane DC Persistent Memory |
| Dataset | 6 billion keys, 100B values, 50/50 read/write ratio, and random access | 6 billion keys, 100B values, 50/50 read/write ratio, and random access |
| Dataset size | 1TB | 1TB |
| Throughput | 1 M ops/second | 1 M ops/second |
| Latency | <1 msec | <1 msec |
| Total savings in memory costs |  | ~ 43% less |

Over the multiple tests executed, we were able to consistently reproduce the same 1ms latency on these large data sets at high throughput. This equates to approximately 43% savings in hardware costs with little to no impact on performance—even on throughputs running into millions of operations per second!

## Ready. Set. Go!

You can see why this is a game-changer for Redis Enterprise users, who want more data closer to compute so they can use Redis Enterprise’s multi-model capabilities to their fullest and use it as a single source of truth database for its many [robust enterprise capabilities](/enterprise/).

There are two distinct operating modes available to customers of Intel’s persistent memory:

- **Memory Mode.** Memory mode extends the memory you have and uses your DDR4 memory as a cache. No specific persistent memory programming is required in the applications, and the data will not be saved in the event of a power loss.
- **App Direct Mode. **App direct mode delivers a tiered approach—one volatile and one persistent—that gives applications the option to optimize where data is placed. The applications and operating system are explicitly aware there are two types of direct load/store memory in the platform and have the ability to write directly to persistent memory.

Given that Redis is based on an in-memory engine (i.e. all its data structures are byte-addressable, with no special serialization/deserialization processes), it was relatively easy to adapt the Redis Enterprise stack and Redis on Flash to work with Intel’s new technology, which is also byte-addressable by design.

**Want to learn more?** If you’re in the bay area, join us at [RedisConf 2019](/redisconf/) in San Francisco (April 2-3). We’ll be talking about this technology in depth at the event and you’ll have direct access to both the Intel team and Redis experts. Even if you haven’t registered, show up and we’ll accommodate you! If you can’t make it to our conference, download our white paper, which delves into a good amount of detail on the persistent memory technology. Last but not least, you can always [reach out](/company/contact/) to the experts at our office for more information. We’re happy to inform and educate in any way that works for you!
