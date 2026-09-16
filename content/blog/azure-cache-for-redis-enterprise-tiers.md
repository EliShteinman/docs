---
title: "New Database Scaling and Security Features in Azure Cache for Redis Enterprise Tiers"
linkTitle: "New Database Scaling and Security Features in Azure Cache for Redis Enterprise Tiers"
url: "/blog/azure-cache-for-redis-enterprise-tiers/"
description: "As applications encounter rising data volumes and user counts, developers can struggle to scale their databases and maintain security. Database scaling can be a complex operation. When you get it..."
date: 2023-04-26
blogCategories:
- "Tech"
authors:
- "Shreya Verma"
lastmod: 2025-03-27
hidden: true
mirrored: true
---

*By Shreya Verma, Principal Product Manager · Published 26 April 2023 · updated 27 March 2025*

![Blog tile image](/images/site-mirror/c437db9e496faa71e5fafa57c58fa6b81afa5a62-772x550.webp)

**As applications encounter rising data volumes and user counts, developers can struggle to scale their databases and maintain security. Database scaling can be a complex operation. When you get it wrong, the result is downtime or service disruption, resulting in frustration for end users, embarrassment for the tech staff, and loss for the business.**

It isn’t just a matter of coping with user demand. Databases can become a target for cyberattacks or fraud, particularly as a company becomes more prominent and its data volumes increase. Maintaining database security can become a real challenge.

To help address these common challenges, we added some new preview features to the Azure Cache for Redis Enterprise tiers. Here’s what changed.

## Database scaling

Database scaling is always top of mind for application developers. Imagine that you launched a new game, and it went viral. Within a few days, the number of gamers grows from a few hundred to millions. Your database needs to handle the increased volume of data, connections, and user requests.

The new scaling feature in Azure Cache for Redis Enterprise tiers allows you to scale your Enterprise database with a click of a button. With the new in-place scale operation, you can both scale-up and scale-out a database. As this is an in-place operation, applications do not incur downtime. The scaling operation completes with minimal interruption to the database.

### Scaling-up

With Redis Enterprise software, you can scale up by moving your database to a larger virtual machine (VM) with more shards. This is useful when there is enough under-utilized (memory and CPU) capacity on the machine to host more database shards or Redis processes.

If you intend to scale a database, we recommend scaling-up to a higher cache type on Azure Cache for Redis Enterprise before you start to scale-out. With a larger cache, you get more memory and compute power. Unlike Redis Open Source, Redis Enterprise software uses the additional compute power to give an optimized shard placement for the database, which results in better overall performance and throughput.

![microsoft azure and redis enterprise instance capacity illustrations](/images/site-mirror/1676fbe845c2ede3e7b12ed6e1f0b8acecefe713-872x752.webp)

*When you scale-up from E10 (capacity 2) to E100 (capacity 2), the database moves to a larger VM and adds shards. Redis Enterprise software uses the additional compute power on the larger VM to optimize shard placement for the database.*

### Scaling-out

Scaling-out refers to adding nodes to the cluster followed by rebalancing, resharding, and then reoptimizing the shard placement within the database. This is useful if you are already using a larger cache type and need more physical resources to scale the database.

![diagram of microsoft azure and redis enterprise instance capacities](/images/site-mirror/15cb60f6528ab18f7dbc657ae5215ac044f5c85b-440x260.webp)

*This is the result when you scale-out from capacity 2 to capacity 4 on the E10 SKU. This adds nodes to the database.*

Microsoft offers documentation on how to scale-up or scale-out on Azure Cache for Redis Enterprise tiers. As it explains, the scaling feature is available in preview.

## Database security

It is crucial to monitor and prevent unauthorized access and to guard against data breaches. The following two preview features, introduced on Azure Cache for Redis Enterprise tiers, allow developers to put strong security measures in place.

### Customer-managed keys

One way to protect data from theft or interception is to use encryption. Azure Cache for Redis already offers Platform Managed Keys (PMKs), also known as Microsoft Managed Keys (MMKs), to encrypt the data on disk, and it does this by default. Additionally, the Enterprise and Enterprise Flash tiers support the ability to encrypt the operating system disk and persistent storage disk data using Customer Managed Keys (CMK). You can store keys in Azure Key Vault, which allows you to keep the keys used to encrypt the data separate from the data itself.

Azure Cache for Redis Enterprise tiers now supports customer-managed keys in preview. Here’s how to configure CMK encryption on Enterprise tiers.

### Connection auditing

Connection auditing is the process of monitoring database access. A real-time log captures who accessed the database, for how long, when the connection was established, and what authentication events were sent during that time. If someone gains unauthorized access to a database, the connection audit logs can provide an entire trail of events.

Azure Cache for Redis Enterprise tiers now supports connection auditing in preview. The connection auditing on the Enterprise tiers uses the built-in audit connection events functionality in the Redis Enterprise software.

Here’s how to enable connection auditing on the Enterprise tiers of Azure Cache for Redis.

Maintaining data requires both scalability and security. Businesses can ensure that their databases can handle rising data volumes and remain secure from cyberattacks by putting in place strong security measures and choosing the right scaling approach. To confirm that the organization’s data is kept safe and secure, use Azure Cache for Redis Enterprise tiers to stay current with the most recent trends in database security and scaling.

## Related links

- Best practices guide for Enterprise and Enterprise Flash tiers
- Developers Rejoice! Azure Cache for Redis Enterprise Features to Make Your Job Easier (Preview)
- Azure Cache for Redis Overview
- Azure Cache for Redis Pricing
- What’s New in Azure Cache for Redis
