---
title: "Create Redis database on Azure Cache"
linkTitle: "Create Redis database on Azure Cache"
url: "/tutorials/create/azure/portal/"
description: "Azure Cache for Redis is a fully managed, in-memory data store on Microsoft Azure. It provides secure, dedicated Redis server instances with full Redis API compatibility. The service is operated by..."
group: "For developers"
aliases:
- "/tutorials/create-azure-portal/"
date: 2026-02-25
lastmod: 2026-02-25
hidden: true
mirrored: true
---

*Published 25 February 2026*

> **TL;DR:**
>
> Sign in to the [Azure portal](https://portal.azure.com/), search for **Azure Cache for Redis**, click **Create**, choose a resource group and pricing tier, then hit **Create** again. Your Redis instance is ready in a few minutes—grab the connection string from **Settings > Access keys**.

## Prerequisites

- An active [Microsoft Azure account](https://azure.microsoft.com/free/). A free-tier subscription works for testing.

## What is Azure Cache for Redis?

Azure Cache for Redis is a fully managed, in-memory data store on Microsoft Azure. It provides secure, dedicated Redis server instances with full Redis API compatibility. The service is operated by Microsoft, hosted on Azure, and accessible to any application within or outside of Azure.

Azure Cache for Redis supports both the Redis open-source engine (OSS Redis) and the commercial Redis offering. Use it as a primary database, cache, message broker, or session store with sub-millisecond response times.

### What can I monitor with Azure Cache for Redis?

Azure Cache for Redis integrates with [Azure Monitor](https://docs.microsoft.com/en-us/azure/azure-monitor/insights/redis-cache-insights-overview) to provide real-time observability for your cache instances:

- View metrics
- Pin metrics charts to the Startboard
- Customize the date and time range of monitoring charts
- Add and remove metrics from the charts
- Set alerts when certain conditions are met

## Step 1. Find Azure Cache for Redis in the portal

Search for "Azure Cache for Redis" in the Azure portal search bar and select the service.

![Searching for Azure Cache for Redis in the Azure portal search bar](images/inline-1-82d58fc06c0320ea904793ca98ee0edbe4f9c297-1968x1206.jpg)

## Step 2. Create a new Redis instance

Click **Create** to start a new Azure Cache for Redis resource. Fill in the required fields:

- **Resource group** – select an existing group or create a new one.
- **DNS name** – choose a globally unique name for your cache endpoint.
- **Pricing tier** – pick a tier (Basic, Standard, Premium, or Enterprise) based on your performance and availability needs.

After configuring the settings, click **Review + create** and then **Create**. Azure provisions the instance in a few minutes.

## How do I get my Azure Redis connection string?

Once the deployment finishes, navigate to your new cache resource. Under **Settings > Access keys** you will find the host name, port, and primary key. Use these values to connect from your application:

```bash
<cache-name>.redis.cache.windows.net:6380,password=<primary-key>,ssl=True,abortConnect=False
```

## Next steps

- [Create a database using Azure Cache for Redis](/tutorials/create/cloud/azure/) – provision an Enterprise-tier instance with advanced data structures and Active-Active geo-replication.
- [Getting Started with Azure Functions and Redis](/tutorials/create/azurefunctions/) – build serverless, event-driven applications powered by Redis triggers and bindings.
