---
title: "A Redis Hosting Option for Heroku Users"
linkTitle: "A Redis Hosting Option for Heroku Users"
url: "/blog/redis-hosting-option-for-heroku-users/"
description: "Heroku may have discontinued its free platform support for Redis, which may discourage those who have depended on it. But not to worry! Redis has several ways to add continued support, including a..."
date: 2022-09-08
blogCategories:
- "Tech"
- "Uncategorized"
authors:
- "Raja Rao"
lastmod: 2025-03-27
hidden: true
---

*By Raja Rao, Head of Growth Marketing · Published 8 September 2022 · updated 27 March 2025*

![Blog tile image](/images/blog/e52cffc4ae0ae4a941d16aec9562a67df2a9536b-772x550.webp)

**Heroku may have discontinued its free platform support for Redis, which may discourage those who have depended on it. But not to worry! Redis has several ways to add continued support, including a starting plan far cheaper than Heroku Redis.**

Heroku is a fantastic product. For years, developers have praised this pioneer in the Platform as a Service (PaaS) category for the platform and the developer experience the tool provides. However, Heroku recently announced that it would discontinue its free platform tiers, Heroku Data for Redis and Heroku Postgres.

![](/images/blog/aeb41a25ac1abd1917e9d20c7f516feb645cbd78-1024x132.webp)

This is not the first time we’ve seen a third-party hosted provider that hosts Redis open source abruptly change or discontinue its service. For example, RedisToGo, which also offered a hosted Redis, recently announced its closure.

![](/images/blog/840297d684629cb3b7938fa5ecd0694a3035299b-1024x498.webp)

Now, imagine you are using Redis in production, an easy-to-imagine scenario. You’re suddenly given a rush project: purchase a new service, set up a new service, upgrade your server, migrate live production data, and so on. It can be a nightmare. You deserve a service you can depend on and one you can be confident will grow with you.

Here at Redis, we want to assure you that we have your back!

We are the driving force behind the popular Redis open source project and the ever-reliable, predictable platform for our customers with our commercial version, Redis Enterprise.

Our cloud offering, Redis Enterprise Cloud, includes free and paid plans. The latter has enhanced developers’ and DevOps capabilities and costs less than any other Redis provider.

Here is a quick comparison of Heroku Redis and Redis Enterprise:

| Free plan | No (Soon to be eliminated) | Yes |
|---|---|---|
| Paid plan starts at | $15/month for 50MB | Option 1: $5.25/month for 100MB w/ coupon through redis.com (i.e., 6X cheaper for 100MB)Option 2: $7/month for 100MB without coupon through redis.comOption 3: $10/month for 100MB through Heroku Marketplace |
| Type of Redis | Redis OSS | Redis Enterprise |
| Creators or maintainers of Redis? | No | Yes |
| Supports native JSON compatibility | No | Yes |
| Supports search and secondary indexing capability | No | Yes |
| Supports graph capability | No | Yes |
| Supports time series capability | No | Yes |
| Supports enhanced probabilistic data structures, including Bloom filter, Cuckoo filter, and others | No | Yes |
| Each Redis database (or cache) is highly available by default (with zero failover time) and durable (with data persistence and backups) | No | Yes |
| Supports globally distributed Active-Active Redis with 5 9’s uptime across regions, clouds, hybrid, and edge | No | Yes |
| Supports terabytes of datasets | No | Yes |
| Available on AWS, GCP, and Azure | No | Yes |

Whether you are a student who just wants to learn Redis, a startup that wants all the enterprise features at an affordable cost, or a large enterprise organization with terabytes of data and a multicloud strategy, look no further.

We have your back!

## A coupon to make it even sweeter

Unsure if this is a good deal for you? Try us out.

If you sign up directly, you can get the same plan for $7/month and get $200 in credit that you can use for up to three months.

Here’s how. After you sign up, choose a paid plan, and apply the coupon offered. Then, copy the endpoint URL and password to your application’s environment variables. It will look something like the one below. (If your environment variables are different, use them instead.)

REDIS_ENDPOINT_URL = "Redis server URI"

REDIS_PASSWORD = "Password to the server"

![](/images/blog/2012470ec980da194d80715330230fde7826f282-1452x318.webp)

Alternatively, to use the Redis Enterprise addon directly via Heroku, run the following:

heroku addons:create rediscloud:30 //30MB plan @ Free

heroku addons:create rediscloud:100 //100MB plan @ $10/month

## Looking for bigger discounts?

Are you a larger company with substantial custom Redis needs? Please contact us, and we’ll ensure you get the best Redis experience anywhere.
