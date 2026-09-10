---
title: "Native JSON Support on Azure Cache for Redis Enterprise Now Generally Available"
linkTitle: "Native JSON Support on Azure Cache for Redis Enterprise Now Generally Available"
url: "/blog/native-json-support-on-azure-cache-for-redis-enterprise/"
description: "Find new opportunities to help create a document database using native JSON support on Azure Cache for Redis Enterprise."
date: 2022-08-05
blogCategories:
- "Tech Redis Modules"
authors:
- "Shreya Verma"
lastmod: 2025-03-27
hidden: true
mirrored: true
---

*By Shreya Verma, Principal Product Manager · Published 5 August 2022 · updated 27 March 2025*

![Blog tile image](/images/site-mirror/a98878bd61760a63d5bec9fbf397bf9814af6c6f-772x550.webp)

**Find new opportunities to help create a document database using native JSON support on Azure Cache for Redis Enterprise.**

We are excited to announce that native JSON support on Azure Cache for Redis Enterprise and Enterprise Flash tiers is now generally available. The Enterprise tiers are developed in a joint partnership between Redis and Microsoft. They help you achieve the highest level of performance, availability, and functionality for your Redis cache databases.

With this release, we now provide a real-time document store on Azure Cache for Redis that allows you to build modern, high-performing, and scalable applications using a dynamic, hierarchical JSON document model. JSON-based keys can be accessed with a dedicated set of commands. RedisJSON supports the JSONPath syntax to atomically update, read, and project elements within your document.

This native support enables RedisJSON to combine with RediSearch, to secondary index, query, and full-text search JSON documents in real-time with ease. The result? Enhanced and scaled application customer experience supporting real-time use cases with low latency, JSON-oriented document database. With the addition of RedisJSON, Azure becomes the first Cloud Service Provider to offer the RSAL-licensed Document capability for their customers as a first-party service. This means that, unlike other services which claim Redis API compatibility, developers can seamlessly migrate applications built using Redis OSS or Redis Stack to Azure Cache for Redis Enterprise when they are ready to launch a fully Enterprise capable solution.

### Using JSON with Azure Cache for Redis Enterprise

With the RedisJSON module, Azure Cache for Redis Enterprise can now deliver a high-performance NoSQL document store that allows developers to build modern applications. It uses native APIs to ingest, index, and query JSON documents. RedisJSON with RediSearch provides a rich query language that can perform full-text searches, complex structured queries, and auto-complete suggestions using “fuzzy” searches.

Some common use cases where RedisJSON can help include Customer360, content management, mobile app development, session management, product catalogs, and more.

### Creating a RedisJSON database in Azure Cache for Redis

Below, you’ll find the steps for creating a database with RedisJSON using the Azure Portal:

1. On Azure Portal, go to the Azure Cache for Redis ‘create’ experience.
1. Select your subscription and resource group, and choose a name for your database.
1. Select an Enterprise or Enterprise Flash tier cache from the Cache type drop-down. Note that Redis Modules are only available on Enterprise or Enterprise Flash tiers.

![screen capture of creating a doc database with redisjson and redisearch](/images/site-mirror/165207bb1073d9c8bd36c36d79501523b6062ebc-750x817.webp)

4. In the **Advanced** tab, select RedisJSON from the Modules drop-down.

5. Click Review + create to create the JSON-enabled database.

![Screen capture for choosing RedisJSON to make document store](/images/site-mirror/1e20bebe44c50fd8d70a290d9ebdc25119ff38df-748x808.webp)

## Creating a document database: RedisJSON + RediSearch

1. Follow steps 1-3 described in the Creating a RedisJSON database in the “Azure Cache for Redis” section.
1. Go to the **Advanced **tab and select both RedisJSON and RediSearch from the Modules drop-down.
1. Click on Review + create to create your document database, that is, a RedisJSON database with RediSearch indexing and search capabilities.

![screen capture of creating a doc database with redisjson and redisearch](/images/site-mirror/165207bb1073d9c8bd36c36d79501523b6062ebc-750x817.webp)

### Creating a document database using Azure CLI – RediJSON + RediSearch

You can use the following AZ CLI command to create your RedisJSON database.

```powershell
az redisenterprise create 
--cluster-name "myjsondb" 
--location "West Europe" 
--minimum-tls-version "1.2" 
--sku "Enterprise_E10" 
--capacity 2 
--clustering-policy "EnterpriseCluster" 
--eviction-policy "NoEviction"  
--modules name="RedisJSON" 
--modules name="RediSearch"
--port 10000 
--resource-group "my_resource_group"

```

Want more detail? Consult the complete Azure CLI documentation for Azure Cache for Redis Enterprise.

### Using RedisInsight for your document database

RedisInsight provides built-in support for the RedisJSON, RediSearch, and RedisTimeSeries modules. With RedisInsight, you can flawlessly visualize, query, and edit your JSON data. You can also administer your Redis database using RedisInsight. For example, gain insights into real-time performance metrics, inspect slow commands, and manage Redis configuration directly through the interface.

RedisInsight comes with built-in tutorials for modules to get you started.

![image of redisinsight creating document database](/images/site-mirror/cddd45b4579a77f865db615199704a89cd74228d-1024x295.webp)

![image of redisinsight creating document database](/images/site-mirror/427a3b42a8d100ac330f0b70f4ac8828ef103057-1024x450.webp)

For details, please refer to this quick-start JSON tutorial.
