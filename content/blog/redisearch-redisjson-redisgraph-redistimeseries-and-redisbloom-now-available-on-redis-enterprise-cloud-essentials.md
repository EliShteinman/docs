---
title: "RediSearch, RedisJSON, RedisGraph, RedisTimeSeries, and RedisBloom Now Available on Redis Enterprise Cloud Essentials"
linkTitle: "RediSearch, RedisJSON, RedisGraph, RedisTimeSeries, and RedisBloom Now Available on Redis Enterprise Cloud Essentials"
url: "/blog/redisearch-redisjson-redisgraph-redistimeseries-and-redisbloom-now-available-on-redis-enterprise-cloud-essentials/"
description: "We’re excited to announce the availability of our most popular modules on Redis Enterprise Cloud Essentials. Redis Enterprise Cloud Essentials databases are ideal for trying out new projects and..."
date: 2020-07-13
blogCategories:
- "Company"
- "Redis Modules"
authors:
- "Pieter Cailliau"
lastmod: 2025-03-04
hidden: true
---

*By Pieter Cailliau, Product Manager · Published 13 July 2020 · updated 4 March 2025*

![Blog tile image](/images/site-mirror/f0bb5cc303edaa86e77c556d6c42b34637041960-772x520.webp)

We’re excited to announce the availability of our most popular modules on [Redis Enterprise Cloud Essentials](/try-free/). Redis Enterprise Cloud Essentials databases are ideal for trying out new projects and can grow with you as you scale your application. Even better, Redis Enterprise Cloud Essentials offers a **free tier for databases up to 30MB**, which can be scaled to higher tiers at minimal cost.

[Click here to view video](https://www.youtube.com/embed/aNQeA8AQnsU)

We heard your requests for this feature and we agree that it’s an ideal playground to try out our technology for engineers who may have restricted laptops or would like to collaborate in a team. We are gradually rolling out the service, and as such it’s currently available only in the AWS/Mumbai (AWS/ap-south-1) region. We look forward to announcing a full rollout in the second half of 2020.

## How to create your Redis Enterprise Cloud Essentials database?

To get started, follow these three steps (you can also find them in the [Redis Modules Quickstart Guide](https://docs.redis.com/latest/modules/modules-quickstart/)):

**Step 1: Create a new subscription**

To create a new Redis Enterprise Cloud Essentials subscription:

1. In the Redis Enterprise Cloud menu, click **Subscriptions**
1. At the bottom of the page, click **Add**
1. Select your subscription configuration:
  1. For the cloud provider, select **Amazon AWS**
  1. For the region where you want to use the subscription, select **ap-south-1** or **us-west-2**
  1. In the Redis Enterprise Cloud service levels, select the **Redis Cloud Essentials 30MB/1 Database** level
  1. Enter a name for the subscription
1. Click **Create**

![](/images/site-mirror/0b68055a53ff943f427ddb599d9baa0b619738e5-1024x908.webp)

*How to subscribe to the free tier in Redis Enterprise Cloud Essentials*

**Step 2: Create a database with a module enabled**

After you create a subscription, you can create a database:

1. Enter a name for the database
1. Enable the modules and select the module you want to use
1. Click **Activate**

![](/images/site-mirror/1ecee7cb312342f2db4e26b539bc1be8ed419992-1024x731.webp)

*Creating a database in Redis Enterprise Cloud*

The database is in “Pending” status. When the database is created, you will be able to see the database settings, including:

- **Endpoint:** The address you use to connect to the database
- **Redis password:** The password you must use in your application connections to authenticate with the database

**Step 3: Connect to your database**

Now you can connect to the database with telnet, redis-cli, an application, or [RedisInsight](/insight/).

To get started with the modules, go to the quick-start guide for the module that you enabled:

- [RediSearch](https://docs.redis.com/latest/modules/redisearch/redisearch-quickstart/)
- [RedisJSON](https://docs.redis.com/latest/modules/redisjson/redisjson-quickstart/)
- [RedisGraph](https://docs.redis.com/latest/modules/redisgraph/redisgraph-quickstart/)
- [RedisBloom](https://docs.redis.com/latest/modules/redisbloom/redisbloom-quickstart/)
- [RedisTimeSeries](https://docs.redis.com/latest/modules/redistimeseries/redistimeseries-quickstart/)

## Getting started with RedisInsight

RedisInsight is an intuitive and efficient GUI for Redis, letting you interact with your databases and manage your data—with built-in support for most popular Redis modules. RedisInsight makes it easy to interact with your database hosted on Redis Enterprise Cloud Essentials, helping you get started with the rich data structures and providing the appropriate visualizations as well as interactive tools to help you iterate quickly when building your queries. (This is especially helpful when you are not yet familiar with the syntax.)

![](/images/site-mirror/f5c9d4ca5fa905eea50c3b4cb3e2b3aeb2afb2c6-1024x346.webp)

*A look at RedisInsight*

RedisInsight is free and available for Windows, Mac, and Linux:

- Learn more about RedisInsight’s the latest capabilities [in this blog post](/blog/redisinsight-1-6-brings-redisgears-support-and-redis-6-acl-compatibility/)
- [Download RedisInsight](/insight/) from the product webpage
- Browse [the RedisInsight documentation](https://docs.redis.com/latest/ri/)

## What’s next for Redis Enterprise Cloud Essentials?

In the following weeks, we plan to publish a series of tutorials to make it easier to experiment with Redis Enterprise Cloud Essentials and each of the modules. The tutorials will include guided flows and sample datasets to play with. You’ll discover new use cases you can address with the world’s most-loved database: Redis!

We’d love to hear from users, developers, and the entire Redis community interested in these new capabilities. Please feel free to ask a question on our [forums](https://forum.redis.com/) or use the support form from Redis Enterprise Cloud to request help and advice. We look forward to hearing from you!
