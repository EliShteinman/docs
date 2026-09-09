---
title: "Announcing Redis Enterprise Pack 5.0 GA"
linkTitle: "Announcing Redis Enterprise Pack 5.0 GA"
url: "/blog/annoucing-redis-enterprise-pack-5-0-ga/"
description: "This content was written prior to a change in Redis’ naming convention – Redis Enterprise is now the moniker for all our products."
date: 2017-11-27
blogCategories:
- "Company"
- "Tech"
authors:
- "Cihan B"
lastmod: 2025-03-27
hidden: true
---

*By Cihan B · Published 27 November 2017 · updated 27 March 2025*

![Blog tile image](/images/site-mirror/724d91083e1b650d172bc4bc9b8f5bfe48cd6212-2000x1125.webp)

This content was written prior to a change in Redis’ naming convention – Redis Enterprise is now the moniker for all our products.

We are super excited to announce the general availability of Redis Enterprise 5.0 today. This latest software pack is now available with new modules on our [downloads page.](/products/redis-pack/downloads/#downloads)

With the 5.0 release, Redis Enterprise provides higher availability, scaling, performance and unmatched cost efficiency over open source Redis.

Here’s what’s new:

**Active-Active Geo-Distributed Deployments Based on CRDTs**

Developing globally distributed applications can be challenging, as developers have to think about race conditions on concurrent writes across regions and complex combinations of events under geo-failovers. New Redis CRDTs (conflict-free replicated data types) simplify this task by using built-in smarts that handle conflicting writes based on the data type in use. Instead of depending on simplistic “last-writer-wins” conflict resolution, geo-distributed Redis Enterprise combines techniques defined in [CRDT](/docs/active-active-datasheet/) research with Redis data types to automatically resolve conflicts based on each data type’s intent.

Visit [Getting Started](/redis-enterprise-documentation/getting-started/creating-database/crdbs/) in our Redis Enterprise Pack documentation to learn more. And for information on how to develop applications with Redis CRDTs, check out our [Developing with Redis CRDTs](/redis-enterprise-documentation/developing/crdbs/) page.

![](/images/site-mirror/724d91083e1b650d172bc4bc9b8f5bfe48cd6212-2000x1125.webp)

**Fulltext Search with RediSearch**

Low latency search results are critical for engaging users. The RediSearch module extends Redis with a fast, distributed, in-memory index for Text, Numeric and Geo search queries. RediSearch with Redis Enterprise scales easily to billions of documents and can instantly index many tens of thousands of updates per second while providing search results at the speed of Redis.

Visit “[Getting Started with RediSearch](/redis-enterprise-documentation/getting-started/creating-database/redisearch/)” in our Redis Enterprise documentation for more information. To learn about developing applications with RediSearch, visit [Developing with RediSearch](http://redisearch.io/Commands/).

**Enhanced JSON Data Handling with ReJSON**

ReJSON is another module that simply makes JSON processing in Redis faster. Native JSON data handling reads and writes subdocument elements with Redis Commands. This eliminates the need to transfer an entire JSON document when doing sub-document updates.

Visit [Getting Started with ReJSON](/redis-enterprise-documentation/getting-started/creating-database/rejson-quick-start/) in our Redis Enterprise Pack documentation for the basics. And for more information on how to develop applications with ReJSON, go to [Developing with ReJSON](http://rejson.io/commands/).

**Bloom Filters with ReBloom**

ReBloom is a command that enables a scalable [bloom filter](/blog/rebloom-bloom-filter-datatype-redis/) as a data type. Similar to hyperloglog, bloom filters are probabilistic data structures. They power “existence search” or “membership search” with a super efficient index that uses just a fraction of the space of a structured or text index.

For more information on how to develop applications with ReBloom, visit [Developing with ReBloom.](http://rebloom.io/Commands/)

**Custom Redis Modules**

In addition, Redis Enterprise 5.0 allows you to install custom modules, enabling you to further extend the functionality of Redis. For example, you can add new data types, capabilities, etc. to tailor the cluster to a specific use case or needs. Once installed, these modules benefit from the high performance, scalability, and availability that Redis Enterprise is known for.

The list of Redis modules is growing every day. You can build your own or explore modules built by the Redis community by visiting [Redismodules.com](http://redismodules.com/).

**Redis 4.0 Support**

Redis Enterprise databases use Redis instances as the shard and each Redis Enterprise database can contain one or many shards for scale throughput and data size for Redis applications. Redis Enterprise 5.0 includes the Redis 4.0 engine as the default version for Redis Enterprise databases. Redis 4.0 improves memory management and powers the modules discussed above.

**Redis Cluster API Support**

Redis Enterprise 5.0 supports the [Redis Cluster](/lp/redis-cluster-database/) API for lower latency operations. This API, along with the zero latency proxy in Redis Enterprise, together deliver efficient connection management and lower latency at higher throughputs.

**Docker in Production**

Your Redis Enterprise Pack cluster can now officially be deployed and run on Docker containers in production. This means you can easily and quickly deploy several containers to start running the scalable and highly available clusters Redis Enterprise is famous for.

To get started with Redis Enterprise 5.0 on Windows, macOS or Linux using Docker, please visit [Quick Start with Redis Enterprise Pack on Docker](/redis-enterprise-documentation/getting-started/docker/).

**LDAP Integration**

With Redis Enterprise 5.0, administrator accounts can now use either built-in authentication or authenticate externally via an LDAP store. These accounts can be used to manage resources on the cluster via command line, Rest API or web interfaces.

For more information, visit [LDAP Integration.](/redis-enterprise-documentation/administering/security/ldap-integration/)

Of course, if you’re interested in a more detailed view of what’s new in Redis Enterprise Pack 5.0, please visit our [technical documentation.](/redis-enterprise-documentation/overview/new-features-redis-enterprise/) You can also check out the [release notes](/redis-enterprise-documentation/release-notes/redis-enterprise-5/) for full details on the improvements we’ve made over our previous 4.5 version of Redis Enterprise.
