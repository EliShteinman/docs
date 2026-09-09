---
title: "What’s New in Two with Redis – February Edition"
linkTitle: "What’s New in Two with Redis – February Edition"
url: "/blog/whats-new-in-two-with-redis-february-edition/"
description: "Click image to view video"
date: 2024-02-29
blogCategories:
- "Tech"
- "Uncategorized"
authors:
- "Talon Miller"
lastmod: 2025-06-11
hidden: true
---

*By Talon Miller, Principal Technical Marketer · Published 29 February 2024 · updated 11 June 2025*

![Blog tile image](/images/site-mirror/efe4da736ee275808c34c41247977dea4da3c6e9-772x550.webp)

[Click image to view video](https://www.youtube.com/embed/sQr16FVWCe4?si=SO3tWJ4rLXDEfC2n)

Welcome to ‘What’s New in Two’, the place to catch up on the Redis releases you might have missed from last month. In this article, we’ll delve deeper into developments from February, expanding on what I covered in our latest video. I’ve included a video thumbnail above for those who prefer watching a quick recap of this month’s updates. Let’s dive in!

First, an enhancement for Maintenance Mode for Redis Software is coming with our newest release of 7.4.2. This enhancement increases flexibility with different shard migration like offering a database ID to evict to preserve availability while keeping other replica shards on the node to save time and also offering the option to evict an active-active replica while keeping high availability replicas. You can also switch between the replica eviction and the database ID since it trumps whatever you provide, meaning, users can ask to avoid replica high availability eviction but supply database ID. For that database, we will evict primary and replica nodes. We are doing that so users can choose a general eviction rule while excluding some high-traffic or highly visible databases. This helps our Redis Software customers with maintenance activities while keeping operations online, available, and without data loss.

Plus improved indication of when maintenance is on or off. Something I know our customers have been asking for and it’s a great improvement.

Next, If you’ve been waiting to have all the great updates from 7.4.2 with your Redis Kubernetes deployment then your day has come. We’re happy to announce the latest release of Redis Software for Kubernetes version 7.4.2 which comes with many enhancements and updates.

That’s a wrap for this month’s ‘What’s New in Two,’ where we’ve taken a closer look at Redis’ latest features and enhancements in February. Whether you prefer watching or reading, Redis has you covered. Stay tuned for more valuable updates in my next two-minute episode. March is stacking up to be a very busy month for us here at Redis, so stay tuned! And if you missed last month’s update, two minutes is all you need to catch up. Until next time!
