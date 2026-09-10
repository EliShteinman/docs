---
title: "Multi-Tenancy in Redis Enterprise"
linkTitle: "Multi-Tenancy in Redis Enterprise"
url: "/blog/multi-tenancy-redis-enterprise/"
description: "In a multi-tenant architecture, a single software instance serves many distinct user groups (or “tenants”). Each tenant’s data is securely isolated, ensuring that it remains invisible and..."
date: 2024-05-14
blogCategories:
- "Company"
- "How To and Tutorials"
authors:
- "James Tessier"
- "John Noonan"
lastmod: 2026-06-01
hidden: true
mirrored: true
---

*By James Tessier, John Noonan · Published 14 May 2024 · updated 1 June 2026*

![Blog tile image](/images/site-mirror/ec9ba318b8d5c1330d0a39a48b1af491fab5ba28-772x552.webp)

In a multi-tenant architecture, a single software instance serves many distinct user groups (or “tenants”). Each tenant’s data is securely isolated, ensuring that it remains invisible and inaccessible to others. Think of it like an apartment building with people living in separate and isolated units of a shared building.

Within Redis, multi-tenancy refers to a single server efficiently managing the needs of various tenants, each maintaining their data securely and separately. Operational efficiency and cost-effectiveness are a few key advantages of this approach. This is because it provides maximum resource utilization without the need for additional physical infrastructure for each new tenant, resulting in simpler and more scalable business operations.

With Redis, you can create a multi-tenant environment on-prem or in any cloud infrastructure you control. This capability is particularly valuable if you’re developing in-house apps using microservices. By adopting a multi-tenant approach, you avoid the complexity and expense of building and maintaining separate infrastructure for each development, testing, or production environment. Meaning you can build and test in parallel—with significantly reduced effort.

## Redis in a multi-instance deployment

1. Multi-instance deployment

Multi-tenant and multi-instance architectures have notable differences. In a multi-instance architecture, you install a new software instance for each tenant. The picture below shows an example of multi-instance architecture for Redis. In this scenario, you deploy a new Redis instance for every tenant, accommodating the need for tenant data segregation. But as the number of your tenants grows, so does the complexity of deploying, monitoring, maintaining, and upgrading multiple software instances.

![multi-instance architecture](/images/site-mirror/fe9fa3ec42cbe110d78c5bacc2f83c5ad9bed3f6-1320x491.webp)

1. Multi-tenancy achieved through virtualization/containerization

In this scenario, Redis is deployed either as a container or a virtual machine, with the underlying management system responsible for launching new Redis instances as needed. Multi-tenancy is handled at the server or infrastructure level, ensuring that each tenant’s operations remain isolated and secure. This approach closely resembles a multi-instance setup, where despite the simplification in provisioning and launching new Redis services provided by the management layer, the number of Redis instances requiring monitoring and management is unchanged.

Many common services like Amazon ElastiCache employ this model. These services charge based on the number of Redis instances used. While this pricing model and the scalability of services like these often result in economies of scale and scope, these benefits tend to favor the service providers more than the end users.

![ElastiCache](/images/site-mirror/408cd358eb48be5d449a83b7613601b474a3c45a-1443x692.webp)

1. Multi-tenancy in Redis

Redis provides software multi-tenancy where a single deployment—typically a cluster of nodes—efficiently supports hundreds of tenants. Each tenant is assigned a distinct Redis endpoint, ensuring complete isolation from others. This maximizes efficiency while improving security and performance across the database setup.

![cluster of nodes](/images/site-mirror/3760a7245f4ffb23f36f10f2cd1855ed307a952a-1443x891.webp)

Deploying Redis in your data center, private cloud, or virtual private cloud leverages the economic advantages of our multi-tenant architecture. With just a single cluster of a few Redis nodes, you can support a range of activities from development and testing to full production. This setup allows you to efficiently accommodate the varying requirements of different tenants within the same infrastructure.

## How our multi-tenant architecture works

Our architecture layers on multiple levels of abstraction to achieve multi-tenancy, high availability, linear scaling, and high throughput, among other capabilities. Here’s a breakdown of the main components:

**Node**:

A node is the hardware foundation—be it a physical server, virtual machine, container, or cloud instance—where Redis Software runs.

**Data plane**:

**Shard**: At the heart of Redis is the shard, a core instance of Redis running on a single CPU core. It manages a subset of the total dataset, operating independently to enhance performance and scalability.

**Database**: Each database acts as a logical endpoint for a tenant’s data. You can allocate multiple shards to a database depending on your data size and throughput needs. Features like persistence, replication, eviction policies, and extending RAM with flash storage can be configured at the database level. Databases ensure high availability by distributing primary and secondary databases across different nodes. The types of databases include:

- **Simple database**: A single primary shard
- **Highly Available (HA) database**: A primary and one or more replica shards
- **Clustered database**: Multiple primary shards, each handling a segment of the dataset
- **HA clustered database**: Multiple pairs of primary and replica shards

![databases](/images/site-mirror/894c00e5c8d6613c30fb0b833d09dbef58828830-1102x536.webp)

**Control plane**:

**Zero latency proxy**: Integrated into each node, this multi-threaded proxy routes Redis operations from clients to the correct database shards. It ensures that requests are directed to the appropriate shard, maintaining efficient operation.

**Cluster manager**: This component consists of a set of distributed processes that manage the entire cluster lifecycle. Separated from the data-path components, the cluster manager is responsible for:

- **Database provisioning and de-provisioning**: Ensuring optimal resource utilization
- **Automatic scaling**: Adjusts resources to handle peak workloads
- **Automatic resharding: **Ensures high-throughput and low-latency performance
- **Automatic rebalancing:** Maintains high-throughput and real-time performance
- **Resource management:** Monitors the health of the entire system
- **Node watchdog: **Oversees processes on each Redis node, triggering shard failure events when necessary
- **Cluster watchdog:** Ensures the health of Redis cluster nodes, triggering node failure events as needed

![cluster paths](/images/site-mirror/c345f737169710b0d30e1d2a4ba985fc6eddb6fa-2048x762.webp)

There are a ton of deployment capabilities, with the only limitation being the total memory available across the cluster. Each database endpoint is assigned a fully qualified domain name (FQDN), and zero-latency proxies on all nodes efficiently redirect client requests to the correct primary shard.

## Cut costs and work more efficiently with multi-tenancy

Redis’s multi-tenant solution brings some serious value:

**Reduced infrastructure costs**: Redis maximizes infrastructure utilization by allowing you to run multiple Redis database endpoints in a single cluster. For instance, you could run hundreds of database endpoints on a simple three-node cluster. The number of database instances you run can be many more than the available cores because of underlying time-slicing. Redis utilizes all available physical resources before signaling the need to add more resources. In contrast, other solutions like ElastiCache provide only one database endpoint per node or cluster—which leads to significant [additional costs vs. our approach](https://redis.io/tco/).

**Seamless scaling**: You can scale a Redis database by adding more shards and expanding it over multiple nodes if needed. The Redis architecture makes sure other tenants—databases in this case—aren’t affected during this process.

**Fine-tuning for HA, persistence, eviction, and data size**: Not all apps have the same requirements for data durability and high availability. In Redis, you can tune your database to meet your app requirements, independent of the other databases running on the same node.

**Agility in dev, testing, and prod environments**: Once a Redis cluster is set up, app devs can provision Redis database endpoints on demand without worrying about the underlying physical or cloud infrastructure.

Redis, a market-proven multi-tenant solution, powers Redis Cloud. This makes sure all databases meet their performance requirements while remaining isolated from “noisy neighbors” and maintaining HA in distributed environments. Redis is easily scalable, operating over 50,000 database endpoints across major cloud platforms like AWS, Azure, and Google Cloud—with nearly 10,000 enterprises trusting us with their most important apps.

## How you benefit from our shared-nothing architecture

Redis uses a shared-nothing architecture, which clearly separates the data-path components (such as proxies and shards) from control and management components (like cluster management processes).

This architecture offers significant advantages and addresses key multi-tenancy challenges:

**Performance**: Our architecture allows data-path entities to focus exclusively on processing user requests, improving overall performance. Each shard functions independently, akin to a standalone Redis instance, without the burden of monitoring other instances or managing network partitions—this isolation minimizes the “noise” from other tenants.

**Availability**: Apps maintain consistent access to data during sharding, resharding, and rebalancing activities. This seamless data availability is managed automatically, eliminating the need for manual intervention and ensuring operations are uninterrupted despite background activities.

**Security and data privacy**: Redis bolsters security by limiting configuration commands to a secure CLI, UI, or API interface with role-based authorization. Our proxy-based architecture makes sure each shard connects only with authenticated entities and processes verified requests, safeguarding against unauthorized access, and enhancing data privacy among tenants.

**Manageability**: Management tasks like database provisioning, configuration changes, and software updates are streamlined through a single command, executed via the UI or API. These tasks are performed across the cluster without disrupting user traffic, ensuring smooth operations and effective resource allocation.

**Scalability and resource allocation**: The architecture supports horizontal scalability, distributing data sets effectively across multiple nodes, servers, and clusters. This method not only accommodates growth but also strategically allocates resources to prevent any single tenant from monopolizing system capabilities. The result? Equitable resource distribution among all tenants.

## Real-world applications

Redis has been successfully deployed in numerous organizations. For instance, a large e-commerce company uses multi-tenancy in Redis to handle data for different departments like sales, marketing, and inventory, each acting as a different tenant.

Similarly, a software-as-a-service (SaaS) provider deployed Redis to manage data for each client. Each client is a different tenant, with their data isolated from others. In these scenarios, Redis’s multi-tenancy helps maintain data privacy while ensuring efficient resource utilization. This approach is commonly used by companies deploying Redis-as-a-Service (RaaS) internally to offer a standardized and centrally-managed Redis for use by the various teams across their organization.

## Multi-tenancy, secured

Security is a top concern in any multi-tenant environment. Redis is designed with several security measures in place. Data isolation between tenants is strictly enforced, ensuring that each tenant’s data is invisible and inaccessible to others.

Redis also deploys security measures to protect against potential breaches. This includes strong access controls, regular security audits, and the latest encryption standards to secure data both in transit and at rest. This provides an extra layer of assurance for businesses and helps maintain trust in the multi-tenant setup.

## In conclusion…

Our multi-tenant architecture offers big benefits, improving performance, scalability, and security. It efficiently manages resource allocation and data isolation, ensuring operational continuity and high availability.

For enterprises looking for robust data management across various environments, Redis is a strong cost-effective solution.

[Explore the many ways Redis provides lower costs and bigger business impacts](https://redis.io/tco/)
