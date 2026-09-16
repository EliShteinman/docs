---
title: "Redis Pack v4.4 Release"
linkTitle: "Redis Pack v4.4 Release"
url: "/blog/redis-pack-v4-4-release/"
description: "This content was written prior to a change in Redis’ naming convention – Redis Enterprise is now the moniker for all our products."
date: 2017-01-20
blogCategories:
- "Company"
- "Tech"
authors:
- "Kirk Kirkconnell"
lastmod: 2025-03-04
hidden: true
mirrored: true
---

*By Kirk Kirkconnell · Published 20 January 2017 · updated 4 March 2025*

![Blog tile image](/images/site-mirror/4bd7834c031c2231010bd6da0dbcc601c0296fc2-536x536.webp)

This content was written prior to a change in Redis’ naming convention – Redis Enterprise is now the moniker for all our products.

![](/images/site-mirror/4bd7834c031c2231010bd6da0dbcc601c0296fc2-536x536.webp)

We are very excited to announce the release of Redise Pack (RP) v4.4 (formerly Redis Enterprise Cluster or RLEC), which delivers several new features, improvements and bug fixes. RP 4.4 includes numerous functionality and performance enhancements that customers have been eagerly awaiting!

Redise Pack v4.4 features the following major enhancements:

- Richer Development
  - Advanced, tunable consistency and durability
  - New Redis commands for BIT and GEO operations
- Higher Performance and Scale
  - Multiple active proxies
  - Redis on Flash v2 (Preview)
- Improved Administration
  - Role-based Administration Control

Let’s get a quick overview of some of these major enhancements in version 4.4.

## Rich Development Experience

### Tunable Consistency and Durability

As a developer, you may want to utilize different consistency and durability levels for each call to the database. For example, for one call you might need to make 100% sure it gets to a replica and down to disk, so you are willing to wait for it. However, for the next call, you may need the speed and cannot wait for the cluster to do its part.

With the support of the WAIT command in RP v4.4, you can control consistency and durability guarantees, by operation even, for a replicated and persisted database across an RP cluster.

See “[Tunable Consistency and Durability](https://docs.redis.com/latest/rs/concepts/data-access/consistency-durability/)” in the RP documentation for more detailed information.

### New Redis Commands

Redise Pack v4.4 now supports the popular geo commands, making it easier for developers to use Redis for location-based data processing and analytics. It also supports BITFIELD, which allows for arbitrarily sized counters to be implemented with maximum memory efficiency, and is particularly useful for real-time analytics. These additional commands make it possible to develop richer applications with Redise Pack. RP v4.4 supports Redis 3.2 databases and the commands introduced in 3.2, specifically:

- [WAIT](https://redis.io/commands/wait)
- [BITFIELD](https://redis.io/commands/bitfield)
- The GEO Commands:
  - [GEOADD](https://redis.io/commands/geoadd)
  - [GEOHASH](https://redis.io/commands/geohash)
  - [GEOPOS](https://redis.io/commands/geopos)
  - [GEODIST](https://redis.io/commands/geodist)
  - [GEORADIUS](https://redis.io/commands/georadius)
  - [GEORADIUSBYMEMBER](https://redis.io/commands/georadiusbymember)
- [CLIENTREPLY](https://redis.io/commands/client-reply)
- [HSTRLEN](https://redis.io/commands/hstrlen)

## Higher Performance and Scale

### Multiple Active Proxies

We all need more uptime, fewer single points of failure and improved HA capabilities from our databases. Multiple Active Proxies can provide all three benefits by allowing your existing Redis clients to connect and use (on a round-robin basis) multiple RP proxies. This can improve throughput and HA capabilities for your database.

See “[Multiple Active Proxies](https://docs.redis.com/latest/rs/administering/designing-production/networking/multiple-active-proxy/)” in the RP documentation for more detailed information.

### Redis on Flash 2.0 (Preview)

For those using Redis for larger datasets, [Tunable Consistency and Durability](https://docs.redis.com/latest/rs/concepts/data-access/consistency-durability/) is a cost-effective tool that improves performance by spreading your Redis databases across both RAM and Flash Storage (e.g. SSD, FusionIO). Objects that are used frequently are kept in RAM by RP and objects used less frequently are relegated to Flash storage. You can tune hot-to-warm values in RAM to achieve your ideal application needs without requiring RAM for colder data. Version 2 of Redis on Flash improves performance and reliability and is provided as a preview to customers who want to try the new version of the product in test environments. Production ready version will be available in the next few months.

## Improved Administration

### Role-based Administration Control

With more and more companies making security and separation of duties a priority, RP 4.4 introduces Role-based Administration, allowing you to assign a role for each administrative user.

![Role-based Administration Control](/images/site-mirror/c4a5a46d978dee9fa23ccf1e337d804f09db52b3-1600x540.webp)

For example, you can give a user the ability to see and read database logs while prohibiting them from viewing cluster level resources or editing any settings.

See “Security Roles” in the RP documentation for more detailed information about this feature and what permissions can be granted.

You can download RP 4.4 today from our [Downloads](/downloads/) page and find more details on this release in the release notes and documentation.

- [4.4 Release Notes](https://docs.redis.com/latest/rs/release-notes/)
- [RP Documentation](https://docs.redis.com/latest/)
