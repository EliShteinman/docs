---
title: "Azure Cache for Redis, Enterprise Tiers Are Now Generally Available"
linkTitle: "Azure Cache for Redis, Enterprise Tiers Are Now Generally Available"
url: "/blog/azure-cache-for-redis-enterprise-tiers-general-availability/"
description: "This morning, Microsoft and Redis jointly announced the general availability of Azure Cache for Redis, Enterprise tiers. The service has been in public preview since last October, and is already..."
date: 2021-03-02
blogCategories:
- "Company"
authors:
- "Amiram Mizne"
lastmod: 2025-03-27
hidden: true
mirrored: true
---

*By Amiram Mizne, Director of Product Management · Published 2 March 2021 · updated 27 March 2025*

![Blog tile image](/images/site-mirror/f9a3b0d4694e07e6d2757aa5d4287096c7272bab-772x520.webp)

This morning, Microsoft and Redis jointly announced the general availability of [Azure Cache for Redis, Enterprise tiers](https://azuremarketplace.microsoft.com/en-us/marketplace/apps/garantiadata.redis_enterprise_1sp_public_preview?ocid=redisga_redis_gablog_cta1). The service has been in public preview since last October, and is already serving customers with production Redis workloads. The GA release is now enhanced with previews of [active geo-replication](/active-active/) (with up to 99.999% availability), and [disk persistence with recovery](/redis-enterprise/technology/durable-redis/) while being rolled out to an increasing number of Azure regions.

## Azure Cache for Redis Enterprise highlights

The following Enterprise and Flash tier capabilities are now generally available:

- [**Open source Redis 6.0**](/blog/diving-into-redis-6/)**:** faster, more secure, and easier to use
- [**Zone redundancy**](https://docs.microsoft.com/en-us/azure/azure-cache-for-redis/cache-high-availability#zone-redundancy)**,** delivering improved availability of up to 99.99%
- [**Redis on Flash (RoF)**](/redis-enterprise/technology/redis-on-flash/)on Azure NVMe-equipped compute
- **Redis modules,** including
  - [RediSearch 2.0](/search/)
  - [RedisTimeSeries](/timeseries/)
  - [RedisBloom](/blog/redis-cache-vs-redis-primary-database-in-90-seconds/)
- **Scaling**
  - Datasets up to 13TB
  - Up to 2,000,000 concurrent client connections
  - More than 1,000,000 ops/sec
- **Security**
  - [Private Link support for network isolation](https://docs.microsoft.com/en-us/azure/azure-cache-for-redis/cache-private-link)
  - TLS (transport layer security) connectivity
- **Integrated billing **and the ability to apply Azure-commitment spend

### New features in this release

In addition to going GA, Azure Cache for Redis, Enterprise tiers now includes previews of powerful new features.

### Active geo-replication is available for preview

We’re excited to announce the public preview availability of active geo-replication. Enterprise tiers’ [CRDTs ](/blog/diving-into-crdts/)(conflict-free replicated data-types) based technology allows developers to create geo-distributed applications that enjoy local sub-millisecond Redis read/write latencies with much better resilience to failure.

Active geo-replication empowers operators to deploy Redis datasets across multiple Azure regions, with managed multi-primary replication across the Azure backbone network. Whether deploying a nationwide multi-region application or a globally distributed one, active geo-replication addresses key use-cases such as global [session management](/solutions/session-management/), world-wide [fraud detection](/solutions/fraud-detection/), geo-distributed search, and [real-time inventory management](/solutions/real-time-inventory/).

![](/images/site-mirror/89f7883a75a74ab678f106b9e1aa760af270b173-581x581.webp)

When it becomes generally available later this year, active geo-replication will provide up to 99.999% availability of service, enabling operators to bring the power of Redis to their organizations’ most mission-critical applications.

A demonstration of the active geo-replication capabilities will be available in the Azure Cache for Redis session at [Microsoft Ignite](https://ignite.microsoft.com/).

### Persistence

Another preview feature now available is persistence to disk and managed recovery from persistence.

Redis persistence to disk provides durability in the rare cases where data stored in RAM is lost due to underlying compute failure of both the primary and replica Redis servers, which are deployed on separate compute nodes by default.

Enterprise tiers provide two modes of persistence to disk storage attached to the Enterprise cluster nodes:

- **AOF** (append-only file) data persistence: logs every write operation or accumulates one second of write operations with minimal to non-effect on Redis performance. When used for recovery from multiple node failures, the append-only log will be played again at Redis startup, reconstructing the original dataset.
- **Snapshot (RDB) **data persistence: performs point-in-time snapshots of your dataset at specified intervals that can be used to rebuild your dataset if needed.

Head over to [Azure Cache for Redis documentation](https://docs.microsoft.com/en-us/azure/azure-cache-for-redis/cache-how-to-premium-persistence) to learn more about persistence.

## A unique joint solution

Azure Cache for Redis Enterprise tiers are powered by [Redis Enterprise Software](/enterprise/) and operated as a fully managed service by Azure. This unique integration lets developers and operators create, manage, and consume Enterprise tier featured Redis workloads natively in the Azure environment.

## Azure billing

The purchasing process is made seamless through integral billing, allowing customers to procure Enterprise-tier services as they do other Azure Cache for Redis tiers during the resource-creation process. Most importantly, for customers with a Microsoft Azure Commitment to Consume (MACC) agreement, their Redis Enterprise spend will automatically be [applied to consume their Azure commitment](https://docs.microsoft.com/en-us/azure/marketplace/azure-consumption-commitment-enrollment).

## Native Azure operations

Familiar Azure tools natively support database resources CRUD (Create, Read, Update, and Delete) operations. The Enterprise tiers’ entire lifecycle is manually managed through the [Az](http://.ms/redis/portal/EnterpriseCreate)[ure Portal](https://portal.azure.com/) or Azure CLI, and PowerShell. Automation of operations is achieved by employing the Azure [Terraform](https://registry.terraform.io/providers/hashicorp/azurerm/latest) provider, [ARM templates](https://docs.microsoft.com/en-us/azure/azure-cache-for-redis/cache-redis-cache-arm-provision), and [REST API](https://docs.microsoft.com/en-us/rest/api/redis/) while monitoring through [Azure Monitor](https://docs.microsoft.com/en-us/azure/azure-cache-for-redis/cache-how-to-monitor) or via the [Redis datasource for Grafana](https://itnext.io/an-easy-to-use-monitoring-solution-for-redis-5a8a73d56129).

### Complementing Azure services

Many Azure services are already pre-integrated with Azure Cache for Redis and with the Enterprise tiers.

A recent benchmark study conducted by Microsoft and GigaOm demonstrated a more than 800% throughput performance improvement and a more than 1,000% latency improvement to Azure SQL and PostgreSQL by deploying Azure Cache for Redis with your application. Read more about how Azure Cache for Redis can improve Azure SQL and Azure Database for PostgreSQL performance in the [Azure Cache for Redis Benchmarking Study](https://azure.microsoft.com/en-us/services/cache/#features).

Enterprise tiers also operate seamlessly with the [large ecosystem of clients and development frameworks](https://docs.microsoft.com/en-us/azure/azure-cache-for-redis/cache-development-faq), including [Azure Spring Cloud](https://github.com/Azure-Samples/brewdis).

### Beyond cache use cases with Redis modules

The Azure Cache for Redis Enterprise tiers extend beyond the native data structures of Redis, allowing developers to do more with Redis by leveraging [Redis modules](/modules/get-started/). This represents a huge advantage for developers by allowing them to address more advanced use cases. The modules supported in public preview are:

- [RediSearch 2.0](/search/): This powerful querying, indexing, and full-text search engine for Redis allows you to query and aggregate the data in a fully distributed manner in real-time, at the speed of Redis. It also supports full-text indexing and stemming-based query expansion in multiple languages and provides a rich query language that can perform text searches, as well as complex structured queries.
- [RedisBloom](/modules/redis-bloom/)*:* This probabilistic data structure is ideal for really large datasets and is designed to tell you, rapidly and memory-efficiently, whether an element is present in a set. It supports Top-K, Count-min sketch, and Bloom and Cuckoo filters. These structures allow for constant memory space and extremely fast processing while still maintaining a low error rate.
- [RedisTimeSeries](/timeseries/)*: *This module offers the ability to store and process time-series data in a fast, efficient, and scalable way. The most common use cases include DevOps and infrastructure monitoring on large scale deployments, IoT, and network monitoring, as well as vertical markets such as finance, energy, industrial IoT, aeronautics, and [healthcare](/industries/healthcare/). It lets you ingest and query millions of samples and events at the speed of Redis and natively supports capabilities like automatic downsampling, aggregations, labeling and search, compression, and enhanced multi-range queries.

## The Enterprise tier advantage

The Enterprise tiers create a natural progression of capabilities, extending the existing Azure Cache for Redis tiers with incremental features, novel use-cases, enhanced service availability, and higher performance.

This table compares the essential dimensions of each tier:

[Watch the video](/wp-content/uploads/2021/03/azure-GA-blog-5.3.png)

## Benchmarking

In a recent benchmark conducted the Enterprise tier (Redis on RAM) performed up to 70% more operations per second and provided up to 40% improved latency versus the Premium tier.

[Watch the video](/wp-content/uploads/2021/03/azure-GA-blog-3.2.png)

[Watch the video](/wp-content/uploads/2021/03/azure-GA-blog-4.2.png)

The benchmark compared E20 and E100 Enterprise tiers with their memory-size equivalent P3 and P5 tiers, using the [memtier-benchmark](https://github.com/RedisLabs/memtier_benchmark) tool, and the following key parameters:

- 100 concurrent client connections
- Pipeline size: 9
- Read:write ratio of 1:1
- Value size: 100B
- 1M keys for E20/P3 and 4M keys for E100/P5

The benchmark measured average latency as seen from the client including RTT (roundtrip time), and the overall maximum achievable throughput.

Note that this benchmark represents Azure Cache for Redis performance, across tiers, at scale 1x deployment. Users can expect up to Nx ops/sec improvement at each of the scale-out levels and up to 10x improvement at the current maximum scale of 10x.

## Enterprise tiers available now

Head over to the [Azure Marketplace](https://azuremarketplace.microsoft.com/en-us/marketplace/apps/garantiadata.redis_enterprise_1sp_public_preview?ocid=redisga_redis_gablog_cta2) to deploy the Azure Cache for Redis, Enterprise tiers and experience these exciting new capabilities first hand. You can also visit the [Azure page on Redis](/cloud-partners/microsoft-azure/) and share your information—a member of our team will contact you.

Learn more about the Azure Cache for Redis offering here:

- Read the [Microsoft blog](https://aka.ms/EnterpriseGABlog).
- Read the Redis [press release](/press/general-availability-of-azure-cache-for-redis-enterprise-tiers/).
- Pricing is available on the [Azure Cache for Redis pricing page.](https://azure.microsoft.com/en-us/pricing/details/cache/)
