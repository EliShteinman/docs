---
title: "Understanding Redis for Cloud and Multicloud in 90 Seconds"
linkTitle: "Understanding Redis for Cloud and Multicloud in 90 Seconds"
url: "/blog/understanding-redis-for-cloud-and-multicloud-in-90-seconds/"
description: "Welcome back to our ongoing Redis in 90 seconds series. In this post, we’ll demonstrate how to use Redis with any major cloud providers, or in a hybrid cloud."
date: 2021-12-23
blogCategories:
- "How To and Tutorials"
- "Tech"
authors:
- "William Johnston"
lastmod: 2025-03-27
hidden: true
---

*By William Johnston, Head of Technical Marketing · Published 23 December 2021 · updated 27 March 2025*

![Blog tile image](/images/site-mirror/975cf42deae47f81d4134b523aed17f297b34f4b-772x520.webp)

Welcome back to our ongoing [Redis in 90 seconds](/blog/learn-how-redis-simplifies-your-architecture-in-90-seconds/) series. In this post, we’ll demonstrate how to use Redis with any major cloud providers, or in a hybrid cloud.

## How to use Redis in a multicloud environment

Most Redis providers simply host [open source Redis](https://redis.io/) and provide Redis as a cache. They don’t support Redis as a database. Not only that, they tend to lock your app into their cloud.

If you need to move to a different cloud provider for any reason, you’re often restricted. It’s because the rest of your data is stored in cloud-specific databases and services such as [DynamoDB](https://aws.amazon.com/dynamodb/), [Kinesis](https://aws.amazon.com/kinesis/), etc. If you use multiple clouds at the same time in place of a [multicloud](/redis-enterprise-cloud/multicloud/), often because of constraints on the region’s availability, or specific business needs, you can’t easily do that. Lastly, if you need a hybrid cloud capability to store some private data on-prem while still using the cloud for the rest, you’re in for a lot of trouble. When you use other Redis providers you lose all the flexibility and you’re “cloud locked-in”.

With Redis Enterprise, since all or most of your data is stored in a single system, you can easily move from one cloud to another. Redis Enterprise is available on all major cloud providers, such as [Amazon AWS](/cloud-partners/aws/), [Google Cloud](/cloud-partners/google/), [Microsoft Azure](/cloud-partners/microsoft-azure/), and even [Heroku](https://www.heroku.com/redis), making [multicloud deployments](/deployment/method/) a breeze. Redis Enterprise is available as [downloadable software](/enterprise/). Keep your private data in your private data center and keep the rest in the cloud, using Redis Enterprise’s hybrid deployment.

Watch the video below to see what we mean:

[Click here to view video](https://www.youtube.com/embed/GYhCTZhqB9U)

## Next Steps
