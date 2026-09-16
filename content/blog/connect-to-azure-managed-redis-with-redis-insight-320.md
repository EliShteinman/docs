---
title: "Connect to Azure Managed Redis with Redis Insight 3.2.0 — Now with Entra ID Authentication"
linkTitle: "Connect to Azure Managed Redis with Redis Insight 3.2.0 — Now with Entra ID Authentication"
url: "/blog/connect-to-azure-managed-redis-with-redis-insight-320/"
description: "We're excited to highlight a key feature in the Redis Insight 3.2.0 release (February 2026): native support for connecting to Azure Managed Redis using Microsoft Entra ID authentication. This is a..."
date: 2026-04-27
blogCategories:
- "Tech"
authors:
- "Purna  Mehta"
lastmod: 2026-04-27
hidden: true
mirrored: true
---

*By Purna  Mehta, Senior Product Manager · Published 27 April 2026*

![Redis](/images/site-mirror/9ad6e30a66471e36398915fbf62560e08c184c86-1200x628.webp)

We're excited to highlight a key feature in the Redis Insight 3.2.0 release (February 2026): native support for connecting to Azure Managed Redis using Microsoft Entra ID authentication. This is a significant step forward for Azure-based teams who want a seamless, secure, and passwordless experience when working with their Azure Managed Redis resources directly from Redis Insight.

## What's new

Connecting to Azure Managed Redis resources previously required manual credential management. With Redis Insight 3.2.0, that experience is now dramatically simpler. The new release introduces:

**Entra ID authentication with automatic token refresh.** Connect to your Azure Managed Redis instances using Microsoft Entra ID - no passwords required. Redis Insight handles background token refresh automatically, so your sessions stay active without interruption.

**Auto-discovery across subscriptions.** Redis Insight can now scan across your Azure subscriptions and surface all your Azure Managed Redis resources automatically. A one-click import flow means you're connected in seconds, without manually entering connection strings.

**Multi-account support.** Easily switch between different Azure accounts within Redis Insight - useful for teams managing multiple environments or working across different Azure tenants.

## Getting started

To use Entra ID authentication with Azure Managed Redis in Redis Insight 3.2.0, you'll first need to configure the required Azure permissions. Follow the [Azure setup guide](https://github.com/redis/RedisInsight/blob/main/docs/azure-setup.md) to get your environment ready, then:

1. Download or update to [Redis Insight 3.2.0](https://redis.io/insight/)

2. Open the **Add Database** flow and select **Azure Managed Redis**

![Redis](/images/site-mirror/038badcf7f429e236d745f89e6e14de94406555e-1085x638.webp)

![Redis](/images/site-mirror/760e9568ba04656d03bfb007f011796b49417c14-885x693.webp)

3. Sign in with your Microsoft Entra ID credentials

![Redis](/images/site-mirror/a359ba8d1cf2cfbfdbe0fa42dd2d122b40186104-839x622.webp)

4. Let Redis Insight auto-discover your databases and connect with one click

![Redis](/images/site-mirror/1460d2c059a269143af102617856bbf204b0fe43-1912x1023.webp)

![Redis](/images/site-mirror/7b138f8a7f98df3e4d316d0e8e985608221e47a1-1912x1025.webp)

Note: While not the recommended approach, you have the option to connect Redis Insight to your Azure Managed Redis cache using Access Keys. This requires first enabling Access Keys on the cache, and then configuring the connection using the custom connection settings within Redis Insight.

## Share your feedback

This feature is now generally available, and we want to hear how it's working for you. Whether you're migrating from Azure Cache for Redis, managing multiple subscriptions, or simply exploring Azure Managed Redis for the first time - your experience matters.

**Tell us what you think:** open an issue or start a discussion in the [Redis Insight GitHub repository](https://github.com/redis/RedisInsight). Your feedback will directly influence how we continue to improve the Azure experience in Redis Insight.

[**Download Redis Insight 3.2.0 →**](https://redis.io/insight/)
