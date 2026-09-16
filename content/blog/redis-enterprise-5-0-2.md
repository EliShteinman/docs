---
title: "Redis Enterprise 5.0.2"
linkTitle: "Redis Enterprise 5.0.2"
url: "/blog/redis-enterprise-5-0-2/"
description: "We, at Redis, are happy to announce the general availability of Redis Enterprise 5.0.2, the latest version of our high performance in-memory database platform. This new version is now available..."
date: 2018-04-03
blogCategories:
- "Announcements"
- "New Product Announcements"
- "Product Releases"
authors:
- "Paz Yanover"
lastmod: 2025-03-27
hidden: true
mirrored: true
---

*By Paz Yanover, Principal Product Manager · Published 3 April 2018 · updated 27 March 2025*

![Blog tile image](/images/site-mirror/0073e867b4e64f59de9047fdcde04295ba647e5c-772x550.webp)

We, at Redis, are happy to announce the general availability of ***Redis Enterprise 5.0.2***, the latest version of our high performance in-memory database platform. This new version is now available with each of our deployment options:

- Redis Enterprise Cloud (RC) – Fully managed, serverless and hosted Redis Enterprise database-as-a-service on major public clouds.
- Redis Enterprise VPC (RV) – Fully managed Redis Enterprise database-as-a-service in your virtual private cloud within major public clouds.
- Redis Enterprise Software (RS) – Downloadable in containers or as an AWS AMI.

The major enhancements of version 5.0.2 include:

**Redis Enterprise Software (RS)**

**Additional Active-Active (a.k.a. Redis-CRDT or CRDB – Conflict-Free Replicated Database) Capabilities**

– [Import a standard RDB](/redis-enterprise-documentation/administering/database-operations/administering-database-operations-importing-data/) file to a CRDB.
– Export a CRDB dataset from one of the CRDB instances (i.e. replicas) to a standard RDB.
– Dynamically and seamlessly [add or remove a CRDB instance](/redis-enterprise-documentation/administering/database-operations/updating-configurations) (replica) without affecting performance.
– Track new performance metrics on the bidirectional replication for CRDB.

**Improved Encryption Options for Data in Transit**
***RS 5.0.2***provides multiple encrypted communication options for various data flows, which help comply with regulatory requirements and can be easily and intuitively deployed. For example:

**Encrypted Communication Across Clusters Over the WAN**
For [active-active (CRDB)](/redis-enterprise-documentation/developing/crdbs/) and [active-passive (‘replica-of’)](/redis-enterprise-documentation/administering/intercluster-replication/replica-of/) deployments, **RS 5.0.2** adds the ability to encrypt data on-the-fly if an SSL handshake was established during the connection setup phase. This allows customers to run multiple types of connections between clusters (i.e. encrypted and unencrypted) without changing the configuration of database endpoints.

For more information about how to enable SSL, follow these links for [active-passive](/redis-enterprise-documentation/administering/intercluster-replication/replica-of/) and [active-active](/redis-enterprise-documentation/administering/database-operations/updating-configurations).

**Encrypted Communication for the Discovery Service (Sentinel API)**
[The Discovery Service](/redis-enterprise-documentation/concepts-architecture/data-access/discovery-service/) enables dynamic IP-based communication between your application and Redis using the Sentinel API. Starting with RS 5.0.2, the Discovery Service using Redis’ Sentinel API can require encryption (TLS/SSL-based) when the chosen Redis client library supports it.

**Redis Enterprise Modules Enhancements**
In ***RS 5.0.2***, [Redis Enterprise Modules](/redis-enterprise/redis-modules/redis-enterprise-modules/) were improved as follows:
– The [ReBloom](http://rebloom.io/) module was enhanced to support Cuckoo Indexes, along with [Bloom Filters](/redis-features/bloom-filter). Cuckoo Indexes are used for high-speed set membership tests, while supporting adding and removing items dynamically with even higher performance than Bloom Filters.

**Preview Release of Kubernetes Support**
The [initial integration of Redis Enterprise with Kubernetes](/blog/running-redis-enterprise-kubernetes-service/) is reflected in a native Redis Enterprise container that will take advantage of the new primitives introduced in Kubernetes (e.g. Kubernetes secrets and stateful sets). This allows Kubernetes customers to enjoy highly available, durable Redis Enterprise with high-throughput, low-latency, in-memory transactions.

**Redis Enterprise VPC (RV)**

**Integrated Redis Modules**
Our zero-touch **Redis Enterprise VPC service** now supports the following [Redis Modules](/redis-enterprise/redis-modules/redis-enterprise-modules/):

[RediSearch](http://redisearch.io/) – An extremely fast search and secondary index engine over Redis
[ReJSON](http://rejson.io/) – A JSON data type implementation for Redis
[ReBloom](http://rebloom.io/) – A scalable bloom filters as a new data type for Redis

Modules. This can be enabled when creating a new database, as illustrated below:

![](/images/site-mirror/0c2fc1f9e45004522795992b8fff07f254a53e85-1204x1070.webp)

Use [this table](/pricing/) for a full comparison between various Redis Enterprise deployments.

Of course, if you’re interested in a more detailed view of what’s new in ***Redis Enterprise 5.0.2***, please visit our [technical documentation](/resources/documentation/) or check out the [release notes](/redis-enterprise-documentation/release-notes/release-notes-redis-enterprise-software-v5-0-2/).

If you have any questions, drop us a line at: pm.group@redis.com
