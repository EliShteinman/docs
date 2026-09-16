---
title: "Lettuce Joins Redis’ Official Client Family"
linkTitle: "Lettuce Joins Redis’ Official Client Family"
url: "/blog/lettuce-joins-redis-official-client-family/"
description: "Lettuce joins the family of officially supported clients under the Redis umbrella."
date: 2024-03-26
blogCategories:
- "Announcements"
- "Company"
- "Uncategorized"
authors:
- "Pieter Cailliau"
lastmod: 2025-07-03
hidden: true
mirrored: true
---

*By Pieter Cailliau, Product Manager · Published 26 March 2024 · updated 3 July 2025*

![Blog tile image](/images/site-mirror/659ae4df42ab89b3720dc2b3381a2dc873d443da-772x552.webp)

Lettuce joins the family of officially supported clients under the Redis umbrella.

With the [Redis 7.2 release](/blog/introducing-redis-7-2/), we’re committed to supporting the key client libraries that the developer community uses. These official client libraries complement the latest Redis functionality, security features, and are optimized for performance, with consistent docs and user interfaces. Lettuce joins the other five [official client libraries](/blog/five-official-redis-clients)––[Jedis](https://github.com/redis/jedis) (Java), [node-redis (NodeJS)](https://github.com/redis/node-redis), [redis-py](https://github.com/redis/redis-py) (Python), [NRedisStack](https://github.com/redis/NRedisStack) (.Net), and [Go-Redis](https://github.com/redis/go-redis) (Go).

[Lettuce](https://github.com/lettuce-io/lettuce-core) is an advanced and non-blocking Java Redis driver that allows for various app arrangements. [Mark Paluch](https://github.com/mp911de) developed it over 10 years with a community of users and contributors. Today, we’re happy to announce that Lettuce has found a new home at Redis. This move marks a pivotal moment for Lettuce and the broader Redis open-source community.

Lettuce is an ideal choice when using the Spring Framework or if you need an asynchronous Redis client for Java. The growing community of users and contributors is a testament to its reliability and effectiveness. This strong foundation has paved the way for Lettuce to take a significant step forward.

The transition under the umbrella of official Redis clients comes with a change in licensing. Lettuce now operates under the more permissive MIT license, moving away from the Apache 2.0 license. Despite this change, Lettuce remains Open Source, and its namespace and package names are unchanged. This means that existing users can continue using Lettuce without modifying their apps.

Redis will offer support for both Jedis, our current Java client, and Lettuce, ensuring that devs don’t need to migrate existing codebases from Lettuce to Jedis or vice versa. Devs should continue to use Jedis for apps that need a fast, synchronous client, and select Lettuce for those apps that require real-time, asynchronous, and reactive capabilities or tight integration with the Spring Framework‌.

We’re thankful for [Mark Paluch](https://github.com/mp911de) and everyone who’s participated in this project. And we’re excited to work with the wider Redis community to make Lettuce and Jedis the best clients for devs within the Java ecosystem.

## Additional Resources

![Introducing Redis 7.2](/images/site-mirror/6f4d1774f0717e849708d1ebc64665473c7c337c-772x550.webp)

Redis 7.2 Sets New Experience Standards Across Redis Products

Learn More

![vector-db-101-blog-card-772x552 (1)](/images/site-mirror/e9391fc69c7ee617640e64892c4b8448ab82cc59-772x550.webp)

Five New Official Redis Clients

Redis is committed to making using our software a delight to use.

Learn More

![](/images/site-mirror/676300a03c67ab78fd62ea92003ec1ad5a4c4c59-772x552.webp)

The best Redis GUI

**REDISINSIGHT** Take your productivity to the next level

Try free
