---
title: "High Availability Architecture Demystified"
linkTitle: "High Availability Architecture Demystified"
url: "/blog/high-availability-architecture/"
description: "A high available architecture is when there are a number of different components, modules, or services that work together to maintain optimal performance, irrespective of peak-time loads."
date: 2022-07-01
blogCategories:
- "Tech"
authors:
- "John Noonan"
lastmod: 2026-06-01
hidden: true
---

*By John Noonan, Senior Product Marketing Manager · Published 1 July 2022 · updated 1 June 2026*

![Blog tile image](/images/site-mirror/4e2a56fcf3f8f0718bc00dd403d1e3d1a06aa7e6-772x550.webp)

## What is high availability architecture?

A high available architecture is when there are a number of different components, [modules](/modules/get-started/), or services that work together to maintain optimal performance, irrespective of peak-time loads.

![High Availability Architecture Demystified](/images/site-mirror/a74121ea8b1a323b3dd516662c9fa8d65a2ca83e-1024x484.webp)

In its purest sense, this system allows businesses to work continuously without failure over a given period of time. Many businesses can’t afford even a minute of downtime. Considering that data is the lifeblood of many businesses, even just a short period of downtime can be incredibly costly.

In certain real-life scenarios, lives may depend on a database built for [high availability](/redis-enterprise/technology/highly-available-redis/). When a patient arrives in the emergency room, medical professionals need instant access to their medical health records to understand what treatment decisions are best. Any delay in accessing this information could have a devastating impact.

Note: [High availability](https://docs.redis.com/latest/rs/concepts/high-availability/) is often measured in the percentage of time that a service is available to users. According to the Microsoft Network Developer Glossary, for a server to be considered “highly available”, it needs to achieve 99.999% network uptime.

## What are high-availability clusters?

High availability clusters are a group of hosts that merge as a single system to prevent downtime. If one server in a high availability cluster goes down, the mission-critical app is immediately transferred to another server as soon as the fault has been detected.

No system is immune to failure, and high availability clusters ensure that optimal performance levels are maintained regardless of inevitable failures. As a result, these tend to be used for the most mission-critical applications, websites, and transaction processing systems.

## How does high availability clustering work?

[Click here to view video](https://www.youtube.com/embed/LLxWu27qQTI)

A high availability cluster will utilize multiple systems that are already integrated, so should a failure cause one system to fail, another can be efficiently leveraged to maintain the continuity of the service or application being used.

The high availability load balancing cluster plays a crucial role in preventing system failures. Having a load balancer in place essentially distributes traffic across different web nodes that are serving the same website or application users. This reduces the pressure on any one server, allowing each cluster to work more optimally while allowing traffic only to be sent to healthy servers.

## High availability cluster concepts

### Active-Passive cluster

The active/passive cluster is made up of at least two nodes. As the name implies, not all of the nodes will be active. If one node is active, the second is a read-only on standby. The passive server acts as a backup and will be utilized should the active server fail to work.

### Active-Active cluster

[Click here to view video](https://www.youtube.com/embed/mCOX-2ez-m4)

This type of cluster typically uses at least two nodes that execute the same service at the same time. In an active-active cluster, both nodes act as primary nodes, meaning either can accept reads or writes. Should one node fail, the user will automatically be connected to the other to ensure continuity of service. Once the first node has been replaced, users will then be split between the two original nodes.

The overarching benefit of the active/active cluster is that it allows you to accomplish node-network balance. If server failure instances are detected a load balancer will transmit user requests to the servers that are readily available and then analyze node-network activity. The load balancer will then push traffic to the nodes that are capable of serving that traffic allowing for greater levels of fault tolerance

This strategy follows a cyclical process, similar to the round-robin model, whereby users are spread randomly across available nodes, or conversely, may adhere to a weighing scheme where one node is prioritized over another based on a percentage.

### Shared-nothing vs. shared-disk clusters

[Click here to view video](https://www.youtube.com/embed/3WOfXRjYnGA)

A general rule that’s followed in distributed computing is to avoid single points of failure at all costs. This requires resources to be actively [replicated](https://docs.redis.com/latest/rs/administering/database-operations/replica-ha/) or replaceable, without a single factor being disrupted should the full service go down.

Imagine if you had fifty running nodes that were powered by one database. If one node fails, it will not have an impact on the persistent state of others, irrespective of the number of running nodes.

But should the database fail, the entire cluster will go down, making the database a single point of failure? This is referred to as a **shared disk cluster.**

On the other hand, should each node maintain its database, a node failure will not impact the entire cluster. This is referred to as a **shared nothing cluster.**

**Note: **If you want to discover more about high availability [clustering](/events/high-availability-with-redis-enterprise-clustering-technology/) technology then make sure to watch this [webinar](/events/high-availability-with-redis-enterprise-clustering-technology/). With over 20 years of experience in the software industry, George Carbonnel will unpack everything you need to know about how clustering technology with Redis Enterprise delivers high performance as well as high availability.

## Requirements of a highly available architecture

There are a number of different requirements that you’ll need to maximize [durability and high availability](https://docs.redis.com/latest/rs/databases/durability-ha/). These include:

### Load balancing

Load balancing is crucial to any [highly available](/docs/six-essential-features-for-highly-available-redis/) architecture. Its primary function is to distribute traffic across backend servers to transmit data more efficiently as well as prevent server overloads. A prerequisite of any load balancing system is to identify what failover process should be carried out when there’s a node failure.

### Data scalability

The ability to scale databases or disk storage units must be taken into account by all highly available architectures. There are two solutions you can pick between to achieve scalability:

- Utilizing the architecture’s main database and using [replication](https://docs.redis.com/latest/rc/databases/configuration/high-availability/) or partitioning to make it highly available; or
- Ensuring that individual application instances are capable of maintaining their own storage of data

### Geographical diversity

We live in a fast-paced digital world where being able to distribute highly available clusters across the globe is now mandatory. Doing so will ensure that if a natural disaster strikes a single location, the impact made will not hinder their ability to provide the service.

### Backup and recovery (disaster recovery)

For all its consistency, highly available architectures will always be susceptible to some sort of malfunction that can disrupt service. Therefore, should a service go down, businesses must have a recovery strategy available to get the entire system running again as quickly as possible.

This is often referred to as disaster recovery – a set of policies and procedures designed to return a service to full functionality in the event of a disruptive event.

## How to measure high availability

High availability is often measured in the percentage of time that a service is available to users. This is done by dividing the total uptime by the system period, which is then multiplied by 100 to get a percentage. According to the Microsoft Network Developer Glossary, for a server to be considered “highly available”, it needs to achieve 99.999% network uptime.

Quite often the percentage availability is referred to as the number of nines in the digits. So four nines would be 99.99%.

**Note:** 99.99% availability is considered the industry standard.

## Best practices for high availability

[Click here to view video](https://www.youtube.com/embed/tRk-LqyGfno)

There are a number of steps you can take to maximize high availability, ranging from the number of components you have to check through to replacing failed servers. Here are some practices that you can use to achieve high availability.

### Achieve geographic redundancy

Geo-redundancy is a crucial line of defense against the outbreak of natural disasters that can lead to service failures. This practice involves deploying numerous servers across different geographical locations, thereby spreading the risk and allowing the architecture to fall back on a different server should a natural disaster strike one region.

**Note:** You can easily achieve this with a database that has [Active-Active Geo-Distribution](/active-active/).

### Use failover solutions

High availability architectures usually involve numerous loosely coupled servers that provide failover capabilities. A failover is seen as a backup operational mode that is automatically utilized when the functions of a primary system go down.

### Implement load balancers

As mentioned previously, a load balancer will spread incoming traffic across different servers to mitigate the risk of any downtime. Be sure to configure your load balancer to utilize an algorithm that’s tailored to your needs to fully optimize this solution.

### Ensure that your data synchronization meets your Recovery Point Objective (RPO)

RPO is a marker for the maximum amount of data you can lose without causing harm to your organization. This highlights the data-loss tolerance of your business as a whole and it tends to be measured in time units, e.g. 1 minute or 1 day.

Setting your RPO to less or equal to 60 seconds will help you maintain [maximum availability](https://docs.redis.com/latest/rc/databases/configuration/high-availability/). Doing so will ensure that if there is a primary source failure, you won’t lose more than 60 seconds worth of data.

## Role of Redis in highly available architecture

Redis Enterprise is a powerful solution for any large corporation looking to achieve maximum availability. It’s a real-time data platform that ensures five-nines availability that provides elite automated database resilience while mitigating hardware failure and cloud outages risks.

Redis Enterprise meets the high availability needs of the most mission-critical enterprise applications. It offers industry-leading functionality to provide [99.999% availability](/events/high-availability-with-redis-enterprise/) using: [Active-Active Geo Distribution](/active-active/), automatic failover, intelligent clustering, a shared-nothing architecture, and global distribution.

Want to learn more about how to achieve high availability?

---
