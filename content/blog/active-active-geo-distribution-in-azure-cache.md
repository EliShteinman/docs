---
title: "Active-Active Geo-Distribution Now Generally Available in Azure Cache for Redis Enterprise"
linkTitle: "Active-Active Geo-Distribution Now Generally Available in Azure Cache for Redis Enterprise"
url: "/blog/active-active-geo-distribution-in-azure-cache/"
description: "We’re excited to announce the general availability of Active-Active Geo-Distribution from Redis in Azure Cache for Redis’ Enterprise and Enterprise Flash tiers. Azure Cache for Redis customers can..."
date: 2022-02-02
blogCategories:
- "Company"
- "Product Releases"
- "Uncategorized"
authors:
- "Shreya Verma"
lastmod: 2025-03-27
hidden: true
---

*By Shreya Verma, Principal Product Manager · Published 2 February 2022 · updated 27 March 2025*

![Blog tile image](/images/blog/34ebd5ff9f40e03d38da3b0f67cd729c744ab45f-772x550.webp)

We’re excited to announce the general availability of Active-Active Geo-Distribution from Redis in Azure Cache for Redis’ Enterprise and Enterprise Flash tiers. Azure Cache for Redis customers can now have up to five Enterprise tier cache database instances in different Azure regions to form an active geo-replicated cache using [conflict-free replicated ](/blog/diving-into-crdts/)data types. An Enterprise tier active-active deployment allows businesses to create global applications that provide local sub-millisecond read/write latencies with considerably better resilience to failure, [covered by 99.999% Azure availability SLA](https://azure.microsoft.com/en-us/support/legal/sla/cache/v1_1/). In addition, Active-Active Geo-Distribution provides [strong eventual consistency](https://en.wikipedia.org/wiki/Eventual_consistency#:~:text=Whereas%20eventual%20consistency%20is%20only,be%20in%20the%20same%20state.), supporting writes to multiple Redis instances across the globe, and takes care of merging local changes while predictably resolving conflicts.

[*Active-Active Geo-Distribution*](/active-active/) known as [active geo-replication](https://docs.microsoft.com/en-us/azure/azure-cache-for-redis/cache-high-availability#enterprise-tiers-1) in Azure enables several key scenarios for enterprise applications:

1. Business continuity with up to 99.999% service availability
1. Global application scaling with **local** read and writelatency
1. Protection against Azure regional outages
1. Data consistency across the globe.

## How to setup active geo-replication on Enterprise Tiers

*Note that Active-Active Geo-Distribution, known as active geo-replication in Azure, is only available on Azure Cache for Redis Enterprise and Enterprise Flash tiers.*

Active geo-replication must be initially set up when creating the Redis instance. You can setup active geo-replication for your instance in the Azure Portal as follows:

1. Create a new Redis Enterprise instance.

![Image of Azure Cache for Redis](/images/blog/6abbd41626261d891daa412d02f981b85ebf4a6e-1024x895.webp)

2. Click on the ‘Advanced’ tab in the create experience.

3. Then click ‘Configure’ in the active geo-replication section to set up active geo-replication.

4. Select an existing replication group, to add a new cache instance to the existing group. Or create a new replication group, by providing a new replication group name.

![Image of Azure Cache for Redis](/images/blog/6abbd41626261d891daa412d02f981b85ebf4a6e-1024x895.webp)

Detailed steps to create and set up active geo-replication on enterprise and enterprise flash tiers can be found [in Azure Cache for Redis documentation.](https://docs.microsoft.com/en-us/azure/azure-cache-for-redis/cache-how-to-active-geo-replication)

## Key features

### Business continuity with up to 99.999% service availability

![image showing regional Azure outages](/images/blog/2eaaa2f1cb26306e2e817876ff3386d142a3df68-856x789.webp)

Active-Active in the Enterprise tier is designed to provide **business continuity**, enabling quick disaster recovery in the event of regional Azure outages. With Active-Active, cache instances can be configured in two or more Azure regions (up to five). It gives you the flexibility to either deploy the application nationwide in multiple regions within the national boundaries or distribute the application across the globe.

When an Azure region experiences a large-scale event or an outage, other cache instances participating in the replication group continue to take the read and write requests. Even if the majority of instances in the replication group are down (3 out of 5) the remaining instances are uninterrupted. The application needs to monitor the cache instances and switch to another region when an instance becomes unavailable.

### Global application scaling with local read and write latencies

![image of reads and writes via active-active geo-replication](/images/blog/4b3033a115f8e05596f55adfcdf236cd9c8f7dfc-786x785.webp)

An application connecting to an Active-Active instance can connect to the geographically closest instance. Bi-directional replication is used between all instances participating in Active-Active in a mesh-like topology to replicate all the writes. All writes made by the application to the local instance are automatically replicated to all other instances. The offers local latency on read and write operations, regardless of the number of geo-distributed regions and their distance from each other.

A globally distributed application can send all their read and write requests to the closest or local instance and enjoy single digit (ms) Redis read/write latencies.

### Data consistency across the globe – Follow the sun!

![image of seamless conflict resolution with active-active](/images/blog/7c380b1e201496ab351975d95fcf3287f1b4d1fd-697x681.webp)

Active-Active enables seamless conflict resolution between two or more geo-distributed cache instances. You can write to multiple cache instances and changes are automatically merged by the underlying replication technology, which is based on the principles of conflict-free replicated data types.

This is useful for applications deployed globally or nationally in multiple regions that must keep data in sync on all instances. For example, a multi-national bank. This can also be used for applications with a ‘follow the sun’ model. For example, source code control systems, DevOps or customer care, where work from one location is handed over to another location that may be many time zones away.

## Conclusion

Active-Active on Azure Cache for Redis Enterprise unlocks critical capabilities for enterprise applications, which need to be highly available anywhere at any time. Whether deploying a nationwide multi-region application or a globally distributed one, Active-Active is essential to use-cases like global [session management](/solutions/session-management/), world-wide [fraud detection](/solutions/fraud-detection/), geo-distributed search, and [real-time inventory management](/solutions/real-time-inventory/).

And we’re excited to announce that this functionality is now generally available in the Azure Cache for Redis Enterprise Tiers! Find links to documentation and demos below. Please give it a try and leave feedback. We look forward to hearing from you.

### Read next:

Microsoft’s documentation on [Azure Cache for Redis geo-replication](https://docs.microsoft.com/en-us/azure/azure-cache-for-redis/cache-high-availability#geo-replication)

Create your own Azure Cache for Redis Enterprise: [Azure Cache for Redis – Microsoft Azure](https://portal.azure.com/#blade/HubsExtension/BrowseResource/resourceType/Microsoft.Cache%2FRedis)

[Overview of the Enterprise Tiers and the MIcrosoft/Redis partnership](https://www.youtube.com/watch?v=rhAjhkE7RVY&t=638s)

[See a demo of active geo-replication in action](https://www.youtube.com/watch?v=LGm4wyWVXFc)
