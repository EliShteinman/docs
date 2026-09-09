---
title: "Recent Enhancements to Redis Enterprise VPC"
linkTitle: "Recent Enhancements to Redis Enterprise VPC"
url: "/blog/recent-enhancements-redis-enterprise-vpc/"
description: "In this blog post, we’d like to share some of the recent enhancements to Redis Enterprise VPC (also known as RV), one of Redis’ database-as-a-service solutions. RV provides a fully managed Redis..."
date: 2018-07-25
blogCategories:
- "Announcements"
- "New Product Announcements"
authors:
- "Aviad Abutbul"
lastmod: 2025-03-27
hidden: true
---

*By Aviad Abutbul, Senior Director of Product Management · Published 25 July 2018 · updated 27 March 2025*

![Blog tile image](/images/site-mirror/0073e867b4e64f59de9047fdcde04295ba647e5c-772x550.webp)

In this blog post, we’d like to share some of the recent enhancements to [Redis Enterprise VPC](/redis-enterprise/vpc/) (also known as RV), one of Redis’ database-as-a-service solutions. RV provides a fully managed Redis Enterprise on your virtual private cloud within major public clouds. It offers highly available, linearly scalable, high-performance, multi-model Redis, with intelligent tiered access to memory (both RAM and Flash).

Three of our latest major improvements to Redis Enterprise VPC provide:

- Support for Redis modules,
- Deployment inside an existing VPC and
- True linear scalability

## Redis Modules Support

[Redis modules](/community/redis-modules-hub/) are add-ons to Redis that extend it to cover most of the popular use cases for any industry. They seamlessly plug into Redis, are processed in-memory and benefit from Redis’ simplicity, super high-performance, scalability and high availability. New modules can be created by anyone, and we, at Redis, encourage the Redis ecosystem to extend Redis by developing new modules.

![RediSearch, ReJson, and ReBloom icons](/images/site-mirror/37a6dde6857ae6e90c4dbb74545d1a819e3384e3-1148x534.webp)

To set an example, we’ve developed several interesting modules ourselves, which we share with the community. The modules we now offer in RV are:

## RediSearch

[RediSearch](/redis-enterprise/technology/redis-search/) is a powerful text search and secondary indexing engine. Unlike Redis search libraries, it does not use Redis’ internal data structures. Using its own highly optimized data structures and algorithms, the RediSearch module delivers advanced search features with high performance and a low memory footprint. It can perform simple text searches as well as complex structured queries, such as filtering by numeric properties and geographical distances.

RediSearch supports continuous indexing with no performance degradation, maintaining concurrent loads of both querying and indexing. This makes it ideal for searching frequently updated databases without batch indexing or service interruptions. The [Enterprise version of RediSearch](/redis-enterprise/technology/redis-search/#sds) can scale across many servers, easily growing to billions of documents on hundreds of servers.

## ReJSON

[ReJSON](https://oss.redis.com/rejson/) is a Redis module that implements [ECMA-404 (the JSON Data Interchange Standard](http://json.org/)) as a native data type. It can store, update and fetch JSON values from Redis keys (documents). ReJSON’s primary features are:

- Full support of the JSON standard
- [JSONPath](http://goessner.net/articles/JsonPath/)-like syntax for selecting elements inside documents
- Document storage via binary data in a tree structure, allowing fast access to sub-elements
- Typed atomic operations for all JSON values types

## ReBloom

[ReBloom](https://oss.redis.com/rebloom/) extends Redis’ native data types and adds two new probabilistic data structures – a scalable [bloom filter](/blog/bloom-filter/) and a cuckoo filter. These data types are used to determine with a given degree of certainty whether an item is present in (or absent from) a collection.

Bloom/cuckoo filters are especially useful because they occupy very little space per element — typically counted in bits not bytes! Although there’s a controllable percentage of false positives, ReBloom provides excellent speed and (most importantly) excellent space efficiency for initial tests of whether a key exists in a set. More information is available in [this blog post](/blog/rebloom-bloom-filter-datatype-redis/).

To use one of these modules, simply select it when you create your subscription/database:

![Module selection in New Database creation tool](/images/site-mirror/c7a14e5f5bf74cfe9cae2e21f686d2cd13021d97-1999x795.webp)

## Deployment inside existing VPC

By default, whenever a new subscription is created, we’ve created a dedicated VPC and deployed Redis Enterprise within it. With this new feature, users now get to choose to have their subscription deployed inside an already existing VPC. This removes the need for peering between VPCs, saving you traffic charges from AWS and cutting some latency from your database.

![Redis Enterprise VPC deployment options](/images/site-mirror/5ab023125c8f89889e8ddd0257d00f20af8624eb-1228x1028.webp)

## True Linear Scalability

Linear scaling of database performance is critical for any application that needs to scale easily and cost-efficiently. Many cloud or on-premises databases claim to scale linearly but can rarely prove it in the manner Redis Enterprise has demonstrated. To achieve this, Redis Enterprise [leverages](/redis-enterprise/technology/linear-scaling-redis-enterprise/) the Redis open source (OSS) cluster API, which allows it to scale infinitely and in a linear manner by simply adding shards and nodes.

The OSS cluster API allows Redis clients to directly access the shard that holds a key/value object with no additional network hop. This, combined with the shared-nothing symmetric architecture of Redis Enterprise, ensures that data and control paths are separate, and that the control path does not impose non-linear overheads in a scaled-out environment.

Redis Enterprise has set a new industry performance record: delivering over **50 million** ops/second **under 1 millisecond**, in as little as **26 EC2 nodes**. You can read more about this in our [benchmark report](/docs/linear-scaling-benchmark-50m-ops-sec/).

![True Linear Scalability Graph](/images/site-mirror/2f3024a1f58ec2bf1999bd981523a0465d578763-1200x742.webp)

Try these new features out for free with our 14-day unlimited free trial (no credit card required). [Sign up now](https://app.redis.com/#/sign-up/vpc?direct=true).

For further information, feedback or suggestions, drop us a line at [pm.group@redis.com](mailto:pm.group@redis.com).
