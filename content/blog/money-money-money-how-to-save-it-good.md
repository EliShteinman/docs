---
title: "Money! Money! Money! – How to Save it Good!"
linkTitle: "Money! Money! Money! – How to Save it Good!"
url: "/blog/money-money-money-how-to-save-it-good/"
description: "Redis, as we know, is the world’s most popular in-memory NoSQL and rapidly becoming a default ingredient of most modern application stacks. Modern application architects use it to help their..."
date: 2016-04-25
blogCategories:
- "Company"
authors:
- "Rod Hamlin"
lastmod: 2025-03-04
hidden: true
---

*By Rod Hamlin · Published 25 April 2016 · updated 4 March 2025*

![Blog tile image](/images/blog/0073e867b4e64f59de9047fdcde04295ba647e5c-772x550.webp)

## Avnet rolls out IBM’s RapidBuild Program with Redis!

Redis, as we know, is the world’s most popular in-memory NoSQL and rapidly becoming a default ingredient of most modern application stacks. Modern application architects use it to help their applications scale to humungous volumes of traffic at sub-millisecond latencies –[with very little hardware](/blog/nosql-bar-datastax-aerospike-couchbase-redis-google-cloud-platform). This blog is about saving even more money with IBM’s RapidBuild Program for POWER8 systems. Today, Avnet announced that it is the first distributor to roll out this program, with pre-installed Redis Enterprise Cluster (RLEC) on IBM Power Systems.

So where’s the money savings part? Well, if you’re running Redis to accelerate your application, whether its processing high speed transactions or speeding up reporting and analytics, and you plan to extend it further to other uses, IBM POWER8 offers formidable horsepower, in terms of number of virtual cores per server, that allows you to run higher numbers of Redis instances on a single server. This helps increase throughput by 67% while keeping latencies under 1 ms. In fact in the below comparison of IBM POWER8 with standard x86 servers, you can see that the maximum throughput of RLEC on IBM POWER8 is so much higher, that on a per transaction basis, you end up with 67% higher throughput at 54% lower costs.

![Cost Savings with Redis in RAM and IBM Power ](/images/blog/6dcf9befc4156deaf1f85dd38681f65f4133cba9-541x354.webp)

With RLEC, you also get the capability to run Redis on Flash memory used as a RAM extender. Flash memory is 10 times cheaper than RAM, and with a judicious mix of RAM and Flash, you can still get hundreds of thousands of operations/min with sub-milllisecond latencies. IBM’s innovative CAPI interconnect, unique to POWER8, allows you to bypass I/O latencies by connecting flash memory directly to the main processors, resulting in a gain of 200% in terms of throughput at 70% lower costs. Not only will you gain increased performance and cost savings POWER8 technology, you can reduce your server footprint from 24 to 1 with POWER8 and CAPI.[1](#_ftn1)

[Watch the video](/wp-content/uploads/2016/04/RedisIBMPOWERcostsavingswithFlash.png)

Given these amazing numbers, of course, we are more than pleased to be included in IBM’s RapidBuild program, which aims to deliver POWER8 systems with pre-installed software that customers are most likely to need. As Avnet rolls this out today, we are delighted to be putting these cost savings and rapid time to value at the fingertips of Redis users worldwide.

---

[1](#_ftn1) 24:1 system consolidation ratio (12:1 rack density improvement) based on a single IBM S824, (24 cores, POWER8 3.5 GHz), 256GB RAM, AIX 7.1 with 40 TB memory based Flash replacing 24 HP DL380p, 24 cores, E5-2697 v2 2.7 GHz), 256GB RAM, SuSE Linux 11SP3 . Inbound network limits performance to 1M IOPs in both scenarios, equal capacity (#user, data) in both cases. x86 cost includes 10k$ for 2x 1U switches
