---
title: "Redis Enterprise Pack v4.5.0 Release"
linkTitle: "Redis Enterprise Pack v4.5.0 Release"
url: "/blog/redis-enterprise-pack-v4-5-0-release/"
description: "We are very excited to announce the release of Redise Pack 4.5.0. Along with many quality improvements and overall performance enhancements, this release ushers in two major capabilities;"
date: 2017-05-10
blogCategories:
- "Tech"
authors:
- "Kirk Kirkconnell"
lastmod: 2025-03-27
hidden: true
---

*By Kirk Kirkconnell · Published 10 May 2017 · updated 27 March 2025*

![Blog tile image](/images/site-mirror/4bd7834c031c2231010bd6da0dbcc601c0296fc2-536x536.webp)

# Redise Pack v4.5.0 Release

We are very excited to announce the release of Redise Pack 4.5.0. Along with many quality improvements and overall performance enhancements, this release ushers in two major capabilities;

- Redise Flash (RF) version 2 is now generally available for use in production.
- Simpler IP Based Connection Management with Discovery Service using the Redis Sentinel API.

## Building Large Databases with RAM and Flash Memory in Redise Flash v2.0

With Redise Pack 4.5.0, Redise Flash version 2 is production ready. The new version brings performance, reliability, and stability enhancements when building large high performance databases using Flash memory.

Redise Flash (RF) offers users of Redise Pack and Redise Cloud Private the unique ability to operate a Redis database that spans both RAM and flash memory (SSD), but remains separate from Redise Pack’s persistence mechanisms. Whilst keys are always stored in RAM, RF intelligently manages the location of their values (RAM vs Flash) in the database via a LRU-based (least-recently-used) mechanism. Hot, frequently used values will be in RAM while warm values will be ejected to flash memory. This enables you to have much larger datasets with RAM-like latency and performance, but at dramatically lower cost than an all-RAM database.

![](/images/site-mirror/c7c71f8dd73479413ee48603a08032bf512f79d1-600x328.webp)

You can get an introduction to building large scale databases with Redis using Redise Flash in this [short video](https://youtu.be/EUAGY5HTPYA) or read more about building large scale databases with Redis in [Redise Pack documentation](/redis-enterprise-documentation/concepts-architecture/concepts/redis-e-flash/).

## New Discovery Service with Support for Redis’ Sentinel API

The Discovery Service enables simple IP based connection for Redis applications. It is compliant with the Redis Sentinel API can be queried to discover the database endpoint (IP address). When used in conjunction with Redise Pack’s other high availability features, the Discovery Service assists an application cope with connectivity under cluster topology changes such as node failures or shard migrations.

The Discovery Service is a distributed service with a process running on each node in the cluster and can be the authoritative source for cluster discovery. To employ it, your application utilizes a Sentinel enabled Redis client to connect to the Discovery Service and query the endpoint for the given database. The Discovery Service replies with the database’s endpoint, either internal or external, for that database. In case of a node failure, the Discovery Service is updated by the cluster manager with the new endpoint.

You can [download Redise Pack 4.5.0](/redis-enterprise-downloads) today and find more details on this release in the release notes and documentation.

- [4.5.0 Release Notes](https://docs.redis.com/latest/rs/release-notes/legacy-release-notes/redis-pack-4-5-0-may-2017/?s=redis%20pack)
- [Redise Flash Documentation](https://docs.redis.com/latest/rs/concepts/memory-architecture/redis-flash/)
- [Discovery Service Documentation](https://docs.redis.com/latest/rs/concepts/data-access/discovery-service/)
- [Redise Pack Documentation](https://docs.redis.com/latest/rs/)
- [Discovery Service code examples](https://docs.redis.com/latest/rs/installing-upgrading/quickstarts/redis-enterprise-software-quickstart/)
