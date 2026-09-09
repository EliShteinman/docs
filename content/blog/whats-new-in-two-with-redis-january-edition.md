---
title: "What’s New in Two with Redis – January Edition"
linkTitle: "What’s New in Two with Redis – January Edition"
url: "/blog/whats-new-in-two-with-redis-january-edition/"
description: "Click image to view session"
date: 2024-01-31
blogCategories:
- "Tech"
- "Tech DE"
authors:
- "Talon Miller"
lastmod: 2025-06-11
hidden: true
---

*By Talon Miller, Principal Technical Marketer · Published 31 January 2024 · updated 11 June 2025*

![Blog tile image](/images/site-mirror/0073e867b4e64f59de9047fdcde04295ba647e5c-772x550.webp)

[Click image to view session](https://www.youtube.com/embed/j3mlSPgzOmU?si=42W0PR8hMNcjR7fJ)

Welcome to ‘What’s New in Two’, the place to catch up on the Redis releases you might have missed from last month. And this month has a ton of great updates. In this article, we’ll delve deeper into developments from January, expanding on what I covered in our latest video. I’ve included a video thumbnail above for those who prefer watching a quick recap of this month’s updates. Let’s dive in!

![](/images/site-mirror/824ee5da07648ec78f8e91ff20fa18626eaa7c1f-1000x165.svg)

*Redis Cloud*

First, let’s jump into Redis Cloud and see what’s cooking there: eight new updates:

![active active Redis database](/images/site-mirror/175e4c2b35a64115890f42f64e1a075e66aa43c9-1920x1080.webp)

1. **JSON Support in Active-Active**

Redis Cloud now supports JSON in Active-Active deployment. Distribute your data globally in real-time with 99.999% high availability.

![ mTLS Certificates 
](/images/site-mirror/ce2394b98ec849bb3d26a3e8c7b687f762455655-1920x1080.webp)

1. **Support for multiple mTLS Certificates**

Adding support for multiple mTLS certificates for less downtime during maintenance windows – less worry about expirations and better separations of application instances connecting to the same database as well!

![Availability Zone Labeling](/images/site-mirror/56825ed568f0692ba241e989751e3314285ee15e-1920x1080.webp)

1. **Availability Zone Labeling**

Introducing a new availability zone labeling feature. This will give you more flexibility and more information when creating new subscriptions on what availability zones your cluster is deploying to.

![Database Tagging](/images/site-mirror/8f12d02fb9615f1d30616da94bc0e67b89532bd4-1920x1080.webp)

1. **Database Tagging (preview)**

Database tagging is here! Manage, organize, and track resources effortlessly with Redis Cloud’s fixed and flexible plans.

![New Billing Admin Role](/images/site-mirror/5654b3137ef57d69599160ef52eec9cfdec1560c-1920x1080.webp)

1. **New Billing Admin Role**

Finance can now pay the bills without access to your precious data. This new Billing Admin role ensures a smooth financial operation without compromising data privacy.

![Column Selector](/images/site-mirror/dc83d8ed10288ed473f02eac6e74403067519ce7-1920x1080.webp)

1. **New Column Selector for Databases**

A new selector, “Column” on the databases page makes diagnosing, identifying, or optimizing a breeze.

1. **AWS Transit Gateway Active-Active Support**

Did you see our AWS Transit Gateway announcement last week? Well, here’s another! We now have Active-Active support for Redis Cloud customers using AWS Transit Gateway in public preview.

![Confluent Cloud](/images/site-mirror/a091ff8079d5ff28af84b73e6d6a95947d350659-1920x1080.webp)

1. **Redis Cloud Integration with Confluent Cloud**

If you’ve logged into Redis Cloud recently, you may have seen a message pop-up that let you know about our new integration with Confluent! This integration will allow you to send data from Kafka or Confluent Cloud to your Redis databases. Go to **Account Settings **and then select the **Integrations **tab. Finally, start the setup by selecting the **Configure **button on the Confluent tile.

![whats-new-in-two-2-jan-blog-new-in-two](/images/site-mirror/a6f710527d12ead8e63fa5f92cebd3711e75dde6-772x550.webp)

Now, let’s talk about Redis Insight – the best Redis GUI out there.

![RedisInsight Click & Learn - Compressed](/images/site-mirror/5b7882840e24a40f1c9e2e541b6103bd76cb3f81-1920x1080.gif)

1. **New RedisInsight Enablement Area**

We’re introducing a dedicated developer enablement area for RedisInsight. Learn how to do more with Redis, even without a database connected. Dive into tutorials and level up your Redis game.

1. **RedisInsight is Now on Docker!**

Exciting News! Redis Insight is now on Docker. Check out our release there if that’s your preferred platform.

![](/images/site-mirror/8791ef8baf350829a49c656df7588acf7cfb3535-1200x628.webp)

But wait, there’s more! I told you January was going to be a busy month for our Redis developers. Our latest release, version 7.4.2 brings some firepower.

![Active-Active Setup](/images/site-mirror/3bebaca41156d9d37f2a97f80e4c76b6a8399fb2-1920x1080.webp)

1. **Active-Active Setup in Redis Enterprise Software UI**

Active-Active setup is now seamlessly integrated into our new Redis Enterprise Software UI. It’s easy to use and very time-efficient.

1. **Security Boost**

TLS 1.3 support and bidding farewell to old ciphers 3DES and RC4 as a nice add to security.

1. **IPv6 Support**

For those who prefer to use the IPv6 protocol, we now support IPv6 for new clusters.

1. **Search and Query Experience Simplified**

We’re wrapping it up with enhancements focused on improving the developer experience (DX). Upgraded integrations with AI and LLM ecosystems like Langchain. Debug your indices faster with richer error handling and build robust applications with new warnings at query time.

There’s more to announce with 7.2.4 but we’ll keep it there for now, come back to see the rest next month!

That’s a wrap for this month’s ‘What’s New in Two,’ where we’ve taken a closer look at Redis’ latest features and enhancements in January. Whether you prefer watching or reading, Redis has you covered. Stay tuned for more valuable updates in my next two-minute episode. And if you missed last month’s update, two minutes is all you need to catch up. Until next time!
