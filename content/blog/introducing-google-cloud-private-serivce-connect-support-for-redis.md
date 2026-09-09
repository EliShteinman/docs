---
title: "Introducing Google Cloud Private Service Connect Support for Redis Cloud"
linkTitle: "Introducing Google Cloud Private Service Connect Support for Redis Cloud"
url: "/blog/introducing-google-cloud-private-serivce-connect-support-for-redis/"
description: "Redis Cloud enhances security and reliability with its new support for Google Cloud Private Service Connect."
date: 2023-09-11
blogCategories:
- "Uncategorized"
authors:
- "Redis  "
lastmod: 2025-03-27
hidden: true
---

*By Redis   · Published 11 September 2023 · updated 27 March 2025*

![Blog tile image](/images/blog/dd1c6d60a3a1196a9ba945c44cf28c2e5c5f5d8c-772x550.webp)

**Redis Cloud enhances security and reliability with its new support for Google Cloud Private Service Connect.**

At its annual Google Cloud Next conference, the company shared several [exciting innovations underway](https://www.reuters.com/technology/google-unveils-enterprise-ai-tools-new-ai-chip-2023-08-29/). Networking and infrastructure optimization earned particular attention.

We were excited that Redis was featured as an ecosystem partner in Google’s [cloud networking session](https://cloud.withgoogle.com/next/session-library?session=ARC201#architects-it-professionals). As part of this partnership, we’re announcing our support for Google Cloud Private Service Connect on Redis Cloud.

## What is Google Cloud Private Service Connect?

Google Cloud Private Service Connect allows organizations to connect applications securely to specific cloud services. Doing so bypasses the public internet and limits network exposure. This provides a safer and more reliable way for applications to communicate with cloud services without exposing entire networks over the web.

There are a few reasons why you might want to use Private Service Connect:

- **Enhanced security**: All data moving between your Google Cloud resources and Redis instances travels through a private, secure, and dedicated connection. This significantly reduces potential attack vectors.
- **Reliability**: The connection is optimized for high availability and low latency. This ensures that applications always have swift and consistent access to your Redis data.
- **Simplified network architecture**: You can easily connect your Virtual Private Cloud (VPC) to Redis Cloud without managing IP address ranges or firewall rules.

Redis Cloud can now connect to all of your Google Cloud applications and services through Private Service Connect as a hosted SaaS service.

![](/images/blog/e27e3369c6b5838831ac8ea017ad29472df8932e-1466x983.svg)

## How to get started

Set up and configure Private Service Connect [through the Redis Cloud admin console](https://docs.redis.com/latest/rc/security/private-service-connect/). Or, if you are new to Redis Cloud, [start today through the Google Cloud Marketplace.](https://console.cloud.google.com/marketplace/product/redis-marketplace-isaas/redis-enterprise-cloud-flexible-plan?pli=1)

We thank our hardworking development team for making this integration a reality and the Google Cloud team for its support throughout the process.
