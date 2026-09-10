---
title: "What’s New in Two with Redis – November Edition"
linkTitle: "What’s New in Two with Redis – November Edition"
url: "/blog/whats-new-in-two-with-redis-november-edition/"
description: "Click To Play Video"
date: 2023-12-13
blogCategories:
- "Tech"
- "Tech DE"
authors:
- "Talon Miller"
lastmod: 2025-06-11
hidden: true
mirrored: true
---

*By Talon Miller, Principal Technical Marketer · Published 13 December 2023 · updated 11 June 2025*

![Blog tile image](/images/site-mirror/a72d9eb984988837860d724e6428893a9ed22b3a-772x550.webp)

[Click To Play Video](https://www.youtube.com/embed/qYXtMZUgBQw?si=LcQPQwisHb0_Hwe8)

Are you a Redis enthusiast eager to stay ahead of the game with the latest releases? Welcome to my second episode of ‘What’s New in Two’, your go-to source for Redis updates. In this article, we’ll delve deeper into the exciting developments from the last month, expanding on what I covered in our latest video. I’ve included a video thumbnail above for those who prefer watching a quick recap of this month’s updates. Let’s dive in!

## Public Preview Support of Write-Behind for Redis Data Integration (RDI)

We’re thrilled to announce that in Public Preview, RDI now supports Write-Behind.

If you’re unfamiliar with the term, let’s break it down. Imagine managing a financial trading app dealing with a high volume of transactions every second. To maintain speed and efficiency, write-behind caching comes into play. Transactions first enter Redis, and then batches of transactions are written collectively to the database. This caching pattern prevents overloading the source database with each transaction, resulting in a smoother, faster, and more cost-effective process.

Look out for an upcoming demo that I’ll be building showcasing how this is done with a MySQL database as the source database.

### Redis Enterprise Cloud is Now Redis Cloud

![](/images/site-mirror/824ee5da07648ec78f8e91ff20fa18626eaa7c1f-1000x165.svg)

Shifting our focus to the cloud, Redis Enterprise Cloud has undergone a simplification – it’s now Redis Cloud. Despite the name change, Redis Cloud remains your only managed offering built and maintained by the experts behind Redis.

### New Low-Cost Fixed Plans for Redis Cloud

![](/images/site-mirror/b529c894d72f2d2e5587470e9a017a8a9cd05124-1920x1080.gif)

On the same note, we’re excited to introduce low-cost Fixed Plans, making Redis Cloud the most affordable per gig compared with other providers. Redis in the cloud has never been this cost-effective, providing a low-end entry point for those looking to get started with Redis in a cloud environment.

If you would like to try out our free tier or check out our new low-cost plans, check out our cloud page to get a first-hand look.

### Redis Cloud has Achieved PCI Compliance

![](/images/site-mirror/88aaa810bc995b74887ef0e5873cb20a39242563-1000x165.svg)

We’re very proud and excited to announce that Redis Cloud has achieved PCI compliance, a set of requirements established by the PCI Security Standards Council for protecting customer cardholder data. This certification ensures the utmost security across all AWS and Google Cloud regions. You can trust Redis Cloud to keep your data safe and compliant, meeting the stringent requirements for handling sensitive financial information.

Read more about PCI compliance to learn all the nitty-gritty details.

# RedisInsight🤝Redis Cloud

![redis insight cloud](/images/site-mirror/99ea5f1a0a33f5397b5f226a11094310659f7ce5-1920x1080.gif)

Let’s explore two exciting updates to RedisInsight. If you don’t know what RedisInsight is, check it out – it’s free and is my favorite Redis GUI out there.

RedisInsight now allows you to directly connect to your Redis Cloud databases from within the RedisInsight interface, offering enhanced insights into your cloud-based databases. It also contains cool hands-on guides such as how to create a vector index, CLI, the new Triggers and Functions, and more.

![](/images/site-mirror/bcfd8731c03bbb6ec82ad9412246bb69f29bbe05-1284x822.gif)

And if you’re already using RedisInsight but want to explore the new tiers in Redis Cloud, you can now create an account directly from RedisInsight with just a few clicks. This integration makes it easier than ever to expand your Redis experience. Download RedisInsight if you’d like to give it a test drive.

That’s a wrap for this month’s ‘What’s New in Two,’ where we’ve taken a closer look at Redis’ latest features and enhancements. Whether you prefer watching or reading, Redis has you covered. Stay tuned for more valuable updates in my next two-minute episode. And if you missed last month’s update, two minutes is all you need to catch up. Until next time!
