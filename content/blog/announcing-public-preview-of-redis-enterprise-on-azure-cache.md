---
title: "Announcing Public Preview of Redis Enterprise on Azure Cache"
linkTitle: "Announcing Public Preview of Redis Enterprise on Azure Cache"
url: "/blog/announcing-public-preview-of-redis-enterprise-on-azure-cache/"
description: "At RedisConf 2020 Takeaway in May, we announced our expanding partnership with Microsoft Azure and introduced Redis Enterprise as two new tiers on Azure Cache for Redis. We are humbled by the..."
date: 2020-11-09
blogCategories:
- "Company"
authors:
- "Cassie Zimmerman"
- "Amiram Mizne"
lastmod: 2025-07-03
hidden: true
mirrored: true
---

*By Cassie Zimmerman, Amiram Mizne · Published 9 November 2020 · updated 3 July 2025*

![Blog tile image](/images/site-mirror/4d83e305e3cb3bc38913c86da00917cf0e02d85b-772x550.webp)

## Delivering new features to Azure Cache for Redis

At [RedisConf 2020 ](https://events.redis.com/redisconf20/)[*Takeaway*](https://events.redis.com/redisconf20/) in May, we announced our expanding partnership with Microsoft Azure and introduced Redis Enterprise as two new tiers on [Azure Cache for Redis](https://azure.microsoft.com/en-us/services/cache/). We are humbled by the tremendous interest and positive feedback we have received from the Redis community and are excited to announce that the service is now available in public preview.

Today’s era presents new requirements for enterprise applications. Developers need the ability to iterate quickly with confidence in their underlying infrastructure and services. Consumers expect responsive and easy-to-use interfaces. Businesses require their applications to deliver sub-millisecond response time across millions of requests per second with the highest availability.

## What to expect in public preview

It’s for these reasons that we have partnered with Microsoft to expand upon the already popular Azure Cache for Redis service. Together we have integrated Redis Enterprise Software with Azure Cache for Redis, providing customers access to an enhanced feature set best suited for business-critical workloads. The service provides two new Enterprise tiers, which are powered by Redis’ technologies and aimed specifically at the needs of enterprise customers. These tiers are engineered jointly by Redis and Microsoft. Moreover, as part of a native Azure service, they are operated and supported by Microsoft. Now available in public preview, these new tiers enhance the open source based Azure product suite with new support for:

- **Open source **[**Redis 6.0**](https://redis.io/download)**:** the most secure version of Redis to date
- **Multi-AZ replication,** delivering an improved availability of up to 99.99%
- **Redis on Flash (RoF) **on Azure NVMe-enabled virtual machines
- **Enterprise modules** including
  - [RediSearch](/search/)
  - [RedisTimeSeries](/timeseries/)
  - [RedisBloom](/modules/redis-bloom/)
- **Scaling**
  - Datasets up to 15TB
  - Concurrent connections can be scaled up to 500K
- **Security**
  - Private Link support for network isolation
  - TLS (transport layer security) connectivity
- **Integrated billing **and Azure-commitment spend
- **Available in multiple Azure regions** including West US 2, South Central US, UK South, SE Asia, West Europe, East US, Australia East, East US 2, North Europe, and Central US
- **General availability coming soon**
  - [Active geo-replication](/active-active/) across multiple geographies and smooth failover, delivering improved availability of 99.999%

The public preview supports availability of up to 99.99% and is backed 24 x 7 x 365 by the Microsoft and Redis support teams. Public preview can be used for more than just testing and proof of concept purposes, and customers may consider it an option for staging, pre-production, or production workloads if the service meets your requirements.

## When to consider the Enterprise tiers

Redis Enterprise was built with enterprise developers in mind. Deciding whether the Enterprise tier is the right option for your organization is dependent on your business goals and application requirements. Here are a few key considerations:

1. **Expanding Redis use cases: **The Enterprise tiers extend beyond the native data structures of Redis, allowing developers to do more with Redis by leveraging Redis modules. This represents a huge advantage for developers by allowing them to use the [most-loved database](/blog/redis-is-the-most-loved-database-for-the-4th-year-in-a-row/) for more advanced use cases. The modules supported in public preview are:
  1. ***RediSearch***: A real-time search engine that runs your Redis dataset and allows you to query data that has just been indexed. Achieve the speed of Redis in your search engine.
  1. ***RedisBloom:*** TopK, CountMinSketch, and Bloom and Cuckoo filters are widely used to support data-membership queries, thanks to their space-efficiency and constant-time membership functionality. That said, fast and efficient probabilistic data-structure implementations aren’t easy to develop in the application layer. RedisBloom enjoys the linear scale, single-digit-seconds failover time, and durability of Redis Enterprise, with easy provisioning and built-in monitoring capabilities.
  1. ***RedisTimeSeries: ***Redis has been used for years to store time-series data. With RedisTimeSeries, capabilities like automatic downsampling, aggregations, labeling and search, compression, and enhanced multi-range queries are natively supported in Redis.
1. **Requiring the highest availability: **Customer requirements are getting tougher by the day. Meeting user expectations that an application must work seamlessly without delays or data loss is a must for businesses. Applications must be resilient enough to sustain even the toughest outages. Going from three-nines of availability to five-nines can mean the difference between ***more than eight hours of downtime*** per year, to ***less than five minutes of downtime ***per year. Depending on your business, this downtime difference could result in a substantial loss in revenue. The availability targeted in the Enterprise tiers for public preview is 99.99% with multi region AZ (availability zone) support enabled by default. With the future addition of active geo-distribution at GA, we expect availability to reach 99.999%.
1. **Scaling your data set: **The Enterprise tiers allow for creation of Redis on Flash (RoF) databases that extend your DRAM capacity with SSD and persistent memory to store significantly more data with fewer resources, significantly reducing cost per GB. While Redis on Flash is not designed to be used as an alternative mechanism for data persistence, AOF and snapshot data-persistence mechanisms are used with Redis on Flash, allowing you to run terabytes of data in Redis at significant cost savings.

## Genuine Redis, genuine Azure

Redis is the home of open source Redis and Azure is committed to the contribution and support of open source projects. With the Enterprise tiers, developers will have access to the most up to date version of Redis released by the community. Users will receive direct access to support from the professionals who build and maintain Redis through the Azure portal.

## Next steps

Customers and partners can now begin using Redis Enterprise on Azure Cache for Redis, in the same way they are used to with the existing Azure Cache tiers. We encourage you to explore the content available in the [Azure Cache for Redis documentation](https://docs.microsoft.com/en-us/azure/azure-cache-for-redis/) and on the [Azure Cache for Redis](https://azure.microsoft.com/en-us/services/cache/) product page. [Get started now with Azure Cache for Redis Enterprise](https://azuremarketplace.microsoft.com/en-us/marketplace/apps/garantiadata.redis_enterprise_1sp_public_preview?ocid=redispubprev_redis_blog_launch).
