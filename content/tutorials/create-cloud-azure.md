---
title: "Create a database using Azure Cache for Redis"
linkTitle: "Create a database using Azure Cache for Redis"
url: "/tutorials/create/cloud/azure/"
description: "Azure Cache for Redis is a native fully-managed service on Microsoft Azure. Azure Cache for Redis offers both the Redis open-source (OSS Redis) and a commercial product from Redis (Redis Cloud) as..."
group: "For developers"
aliases:
- "/tutorials/create-cloud-azure/"
date: 2026-02-25
lastmod: 2026-02-26
hidden: true
---

*Published 25 February 2026 · updated 26 February 2026*

> **TL;DR:**
>
> Set up Azure Cache for Redis Enterprise by launching Redis Enterprise from the Azure Marketplace, configuring your subscription and cache settings in the Azure portal, and connecting with `redis-cli`. The Enterprise tier gives you access to advanced features like active geo-replication, Redis modules (RediSearch, RedisJSON, RedisBloom, RedisTimeSeries), and enterprise-grade SLAs.

Azure Cache for Redis is a native fully-managed service on Microsoft Azure. Azure Cache for Redis offers both the Redis open-source (OSS Redis) and a commercial product from Redis (Redis Cloud) as a managed service. It provides secure and dedicated Redis server instances and full Redis API compatibility. The service is operated by Microsoft, hosted on Azure, and accessible to any application within or outside of Azure.

## What will you learn?

- How to subscribe to Azure Cache for Redis Enterprise through the Azure Marketplace
- How to configure a new Redis Enterprise cache instance in the Azure portal
- How to connect to your Azure Redis Enterprise database using `redis-cli`

## Prerequisites

- An active [Microsoft Azure account](https://azure.microsoft.com/en-us/free/)
- Basic familiarity with the [Azure portal](https://portal.azure.com/)
- `redis-cli` installed locally (included with [Redis](https://redis.io/docs/latest/operate/oss_and_stack/install/install-redis/))

## How is Azure Cache for Redis Enterprise different from the basic tier?

Azure Cache for Redis Enterprise is the premium offering that provides features beyond the standard Azure Cache for Redis tiers. Enterprise tier benefits include:

- **Active geo-replication** for multi-region deployments
- **Redis modules** such as RediSearch, RedisJSON, RedisBloom, and RedisTimeSeries
- **Enterprise-grade SLAs** with 99.999% availability
- **Higher throughput and lower latency** compared to Basic and Standard tiers
- **Flash storage** support for cost-effective large datasets

If you're looking for the standard Azure Cache for Redis setup, see the [Azure portal basic tutorial](/tutorials/create/azure/portal/).

## How do you set up Azure Cache for Redis Enterprise?

### Step 1. Launch from the Azure Marketplace

Open the [Azure Cache for Redis Cloud & Flash](https://azuremarketplace.microsoft.com/en-us/marketplace/apps/garantiadata.redis_enterprise_1sp_public_preview?ocid=redisga_redislabs_cloudpartner_cta1) listing in the Azure Marketplace.

![Azure Marketplace listing page for Redis Enterprise Cloud and Flash showing subscription options](/images/site-mirror/1cc59dee17c2a8631b51754ce2a9a59e9c9dec9c-1038x659.webp)

### Step 2. Subscribe and configure your plan

Select your Azure subscription, resource group, and region. Choose the Enterprise tier that matches your workload requirements.

![Azure portal setup and subscribe page for configuring Redis Enterprise subscription details](/images/site-mirror/01768a6c6b999e9b31fd7a10327b05711e3c90c7-1038x709.webp)

### Step 3. Configure your Redis Enterprise cache

Set your cache name, select the desired capacity, and enable any Redis modules you need (such as RediSearch or RedisJSON). Configure networking and security settings based on your requirements.

![Azure portal configuration page for setting Redis Enterprise cache name, capacity, and module options](/images/site-mirror/06d5aa7f1da8521f83e9fd8cbe023887f69cf048-1038x801.webp)

### Step 4. Finalize and deploy

Review your configuration and click **Create** to deploy your Azure Cache for Redis Enterprise instance. Deployment typically takes a few minutes.

![Azure portal review and create page showing the final configuration summary before deploying Redis Enterprise](/images/site-mirror/2134506bb60d98956f9e134c02c59b5172f2b6f8-1038x576.webp)

## How do you connect to your Azure Redis Enterprise database?

Once your cache is deployed, retrieve the hostname and access key from the Azure portal. Then connect using `redis-cli`:

```bash
sudo redis-cli -h redislabs.redis.cache.windows.net -p 6379
redislabs.redis.cache.windows.net:6379>
```

Replace `redislabs.redis.cache.windows.net` with your actual cache hostname from the Azure portal.

## Next steps

- Follow the [Azure Cache for Redis portal tutorial](/tutorials/create/azure/portal/) for a walkthrough of the standard tier setup
- Learn how to [migrate from ElastiCache to Azure Managed Redis](/tutorials/learn/migration/elasti-cache-to-azure-managed-redis/)
- Learn how to [migrate from Memorystore to Azure Managed Redis](/tutorials/learn/migration/memorystore-to-azure-managed-redis/)
- Explore [using Azure Managed Redis to store LLM chat history](/tutorials/howtos/use-amr-store-llm-chat-history/)
- Build serverless apps with [Azure Functions and Redis](/tutorials/create/azurefunctions/)
- Review [Best Practices for Azure Cache for Redis](https://docs.microsoft.com/en-in/azure/azure-cache-for-redis/cache-best-practices)
- Get started with [Azure Cache for Redis in .NET Framework](https://docs.microsoft.com/en-us/azure/azure-cache-for-redis/cache-dotnet-how-to-use-azure-redis-cache)
