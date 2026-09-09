---
title: "Managing 50K+ Redis Databases Over 4 Public Clouds with a Tiny Devops Team"
linkTitle: "Managing 50K+ Redis Databases Over 4 Public Clouds with a Tiny Devops Team"
url: "/blog/managing-50k-redis-databases-over-4-public-clouds-with-a-tiny-devops-team/"
description: "Modern applications have a general list of needs in order to not only survive, but thrive in today’s fast paced cloud environment. These include low response times (less than 100 milliseconds),..."
date: 2014-07-31
blogCategories:
- "Tech"
authors:
- "Redis  "
lastmod: 2025-03-27
hidden: true
---

*By Redis   · Published 31 July 2014 · updated 27 March 2025*

![Blog tile image](/images/blog/0073e867b4e64f59de9047fdcde04295ba647e5c-772x550.webp)

![](/images/blog/c4255191f38b9c3948d682a280b0f46a63049dd2-635x200.webp)

Modern applications have a general list of needs in order to not only survive, but thrive in today’s fast paced cloud environment. These include low response times (less than 100 milliseconds), limitless scalability, high availability, and optimal performance, to name a few. With a selection of modern database options available, Redis has proven to be one of the most popular. Redis has aided in the creation of over 50,000 databases by over 2,500 paying customers, with more than 100 new databases created daily. Being a major contributor to [Redis’ open source project](https://github.com/antirez/redis), many of the use cases that we see using Redis include social applications, online advertising companies, and gaming companies. Our experience running Redis services across the four major clouds (AWS, Azure, GCP and SoftLayer) has made us aware of a number of challenges that users encounter, which consequently led to our thoroughly tested solutions, a few of which we have shared below.

*(interactive chart, not available offline)*

### Challenge #1: Stable Top Performance

While Redis is very fast, with the ability to respond to requests in less than 1 millisecond, running it in the cloud can cause performance to degrade significantly. However, with Redis, all operations are performed behind the scenes, incorporating as many Redis instances as possible into a cluster to enable pure multi-tenancy architecture without degraded performance. Redis databases on our platform use master-slave replication, where the master is located on one node while the slave is located on another, with as many instances as possible on every node. Additionally, the cluster is built around an odd number of nodes in order to have a quorum in case of a failure. Our zero-latency proxy hides everything from the user’s perspective, so that users only see a single-end point, with the ability to add proxy to receive more throughput, without visibility of shards, clusters or nodes.

### Challenge #2: Data Center Selection

When we began our journey with Redis, our primary challenge was understanding which data center would be optimal for each application. It is important that every Redis database be run on the same data center as its respective application so as to avoid network latency. Data centers are selected by users when they create an instance inside a region, however, an issue arises when selecting a zone or data center from AWS, because they are mapped out differently between accounts. For example, Redis’ ‘us-east-1a’ can be signified as ‘us-east-1c’ for other users. While these are completely different data centers, AWS set up this method to ensure stable load balancing for its internal architecture. Otherwise, since most users have no preference regarding a specific data center, most will choose the first one, thus creating an unbalanced level of demand. To deliver Redis’ multi-cloud, multi-region service from the closest location possible to the user’s application, we developed a code that performs mapping between our zones and those of our users. Applying that to our example, we found that the code for ‘us-east-1a’ matched that of ‘us-east-1c’. This tells us that when a user chooses to create a database in ‘us-east-1c’, it should be mapped to our ‘us-east-1a’ to ensure minimal network latency.

### Challenge #3: Instance Selection

Deciding which instance to select when creating a node can be confusing. Consequently, we decided that any type of instance can be used in Redis’ clusters. Though each instance type has a predefined set, there is no limitation to the range of sizes that can exist within a cluster, whether it be 30GB or 200GB. This kind of flexibility is key. We want to be able to cope with high memory usage as well as high CPU usage. Additionally, we want to run everything on dedicated infrastructure to avoid ‘noisy neighbors’ and be as cost effective as possible. Using large instances automatically provides dedicated instances by design. These large instances are then used in creating our own controlled multi-tenant infrastructure. In order to create a solid infrastructure for any architecture, it is advised to use specific instances across the clouds: c3 (for performance) and r3 (for memory) in AWS; a4, a5, a6, and a7 in Azure; the standard high memory and high CPU in GCP; base clusters over bare metal servers in SoftLayer with added virtual machines to scale out.

### Challenge #4: Data Persistence

With users who run 1 million operations per second, 50% of which being write requests, data persistence is extremely significant with Redis. The question is, how can this be performed over AWS’ EBS infrastructure? First of all, you need to understand the details behind the storage architecture of the cloud: local ephemeral storage is relatively fast and network attached storage, such as EBS, is persistent. The largest EBS volumes on AWS provide dedicated EBS disk storage (the same goes for GCP). Unfortunately, this is not enough to cope with Redis’ performance. As a result, we hybridized the two, using ephemeral for some storage needs, incorporated with EBS for persistence. Accordingly, we have fine tuned Redis to enhance its speed when accessing a disk, and use slaves to perform data persistence activities when using replication, freeing up the master.

### Challenge #5: Monitoring

How is everything monitored? [Zabbix](http://www.zabbix.com/) is used to monitor nodes, and as far as monitoring database metrics goes, we searched for an open source project to no avail, which led us to build our own monitoring system – Limbic – that is based on Python, [RRD](http://oss.oetiker.ch/rrdtool/) and Redis. With this platform we are able to monitor 50,000 databases, each with 100 metrics, and keeping 10,000 time resolutions. In due time, it will be available on open source for everyone to enjoy.

*(interactive chart, not available offline)*

### How We Manage the Service

We are able to handle these complex infrastructures at the hand of our strong DevOps team that, while humble in size, is backed up by the devs who know the system inside and out, and can be dragged into resolving production issues in real time. We also use a ‘baby steps’ approach when moving to production. As a result, we always begin with manual configuration, then slowly make our way to automation. We’ve found that this practical approach always wins.

Overall, Redis has taken the necessary steps to ensure quality Redis performance for our customers. Our solutions to the challenges mentioned above have provided the peace of mind our customers need in order to successfully focus on their own core capabilities. For more information, check out the full [video](https://www.youtube.com/watch?v=eymqHZaUOH4) that explores the challenges above as well as the corresponding [slide show](http://www.slideshare.net/Redis/redis-labs-igt-0714).
