---
title: "RedisInsight 1.6 Brings RedisGears Support and Redis 6 ACL Compatibility"
linkTitle: "RedisInsight 1.6 Brings RedisGears Support and Redis 6 ACL Compatibility"
url: "/blog/redisinsight-1-6-brings-redisgears-support-and-redis-6-acl-compatibility/"
description: "RedisInsight is an easy and intuitive GUI for Redis, allowing you to oversee all your databases and manage your data, with built-in support for the most popular Redis modules. It provides tools to..."
date: 2020-07-02
blogCategories:
- "Company"
- "Tech"
authors:
- "Stévan Le Meur"
lastmod: 2025-03-27
hidden: true
mirrored: true
---

*By Stévan Le Meur, Senior Product Manager · Published 2 July 2020 · updated 27 March 2025*

![Blog tile image](/images/site-mirror/0324f2cccf55ae10454911d833ea98f6219e2888-270x190.webp)

![](/images/site-mirror/894ccaeb22b4533384ff12e54959ba4d89d88a96-1024x345.webp)

[RedisInsight](/insight/) is an easy and intuitive GUI for Redis, allowing you to oversee all your databases and manage your data, with built-in support for the most popular Redis modules. It provides tools to analyze your database’s memory usage and profile its performance.

With the latest release, RedisInsight 1.6, RedisInsight hits another important milestone with new capabilities and enhancements designed to make your developer experience even more enjoyable. In this blog post, you’ll learn all the details about the latest developments in RedisInsight.

## Overview

Since the beginning of the year, we have released several new versions of RedisInsight. Each one included a mix of new capabilities, enhancements, and bug fixes. Key highlights include:

- **RedisGears beta**: Code, build, run, and manage RedisGears functions directly from RedisInsight.
- **Redis 6 and ACLs**: Support for the latest Redis release and its new access control lists (ACLs) capability.
- **Multi-line query editing**: Write and structure your queries using multiple lines for RediSearch, RedisGraph, and RedisTimeSeries.
- **Unleashing the command-line interface (CLI):** A faster and unrestricted redis-cli with cleaner output formatting.
- **TLS Support:** Connect to Redis databases requiring TLS authentication.
- **Auto-discovery of Redis databases: Quick configuration when using Redis Enterprise Cloud and Redis Enterprise Software.**
- **Full-screen mode:** Interact with your graphs, search queries, and time-series data without any distractions, greater detail, and maximum screen space.

## Quick start

The latest RedisInsight 1.6.0 is available for both local installation and as a Docker container. Here’s how:

**Local installation:**

[Download RedisInsight for Windows, Mac, and Linux](/insight/) from the Redis website.

**Docker installation:**

docker run -v redisinsight:/db -p 8001:8001 redis/redisinsight:latest

You can find more information on installing RedisInsight in the [documentation](https://docs.redis.com/latest/ri/installing/).

**Upgrades:**

Since Version 1.2.2, RedisInsight notifies you when a new update is available. Alternatively, you can upgrade RedisInsight by simply uninstalling and reinstalling the application from your operating system. *Note that updating persists all your preferences, and especially all the database connection details.*

## What’s new in RedisInsight 1.6

**RedisGears beta support in RedisInsight**

RedisGears is a dynamic framework that enables developers to write and execute [functions](https://oss.redis.com/redisgears/functions.html) that implement data flows in Redis, while abstracting away the data’s distribution and deployment. You can use [RedisGears](/modules/redis-gears/) to improve application performance and process data in real time. RedisGears lets you program in Redis, deploy functions, and run your serverless engine where your data lives. (You can learn more about RedisGears in this blog post: [Announcing RedisGears 1.0: A Serverless Engine for Redis](/blog/redisgears-serverless-engine-for-redis/).)

![](/images/site-mirror/edecbbe371797423bb0d953e8aece55e93765b69-275x274.webp)

RedisInsight 1.6 includes a new tool—accessible from the application’s main menu—that lets you interact with the RedisGears serverless engine. With this new tool, you can explore the history of the latest executed functions and analyze the results (and eventually the errors) of those functions. You’ll get a summary of the execution, as well as the result data, depending on what your function is actually doing.

With RedisGears, you can also register functions to be triggered by specific events on your data. Within RedisInsight, you can manage and explore the registered functions—the UI displays all the functions running in Redis at a quick glance.

Finally, we also added a simple code editor. Obviously, we’re not trying to replace your favorite IDE or development tool, but an integrated editor lets you quickly write a script to process data in real time or capture when a particular event is happening with your data.

[Watch the video](/wp-content/uploads/2020/08/image3-resized-1.gif)

This new capability is currently in beta, so we’re excited to hear your feedback and thoughts on the [Redis Community Forum](https://forum.redis.com/c/RedisInsight/65).

**Redis 6 and access control lists (ACLs) support**

RedisInsight is now fully compatible with Redis 6—they work seamlessly and transparently together.

[One of the key new capabilities introduced with Redis 6 is access control lists](/blog/diving-into-redis-6/). ACLs bring the concept of “users” to Redis, which lets you control what level of Redis access each user has. You can configure which **commands** specific users can execute and which **keys** they can access. This allows for much better security practices: you can now restrict any given user’s access to the[ least level of privilege](https://en.wikipedia.org/wiki/Principle_of_least_privilege) needed. This is particularly helpful if you are building different services in your application: You can create dedicated users to grant only a specific set of commands on the database. ACLs allow users access to only particular commands, keys, or even patterns of keys based on user-based specified permissions.

Each defined user can have its own password. Now, when you connect to Redis from RedisInsight, you can specify the user you want to connect with, as well as the password, as shown here:

![](/images/site-mirror/9eda9af4305c550341600ba5dcd5b3af1c6065d1-1024x769.webp)

***Note: ****In order to use RedisInsight, a user must have at least the permissions to run the following commands: INFO and PING. Those commands are used for properly configuring RedisInsight with Redis.*

**Unleashed CLI**

RedisInsight provides most capabilities with an easy UI, but in certain cases you might still need to run some advanced commands. For those purposes, we have integrated a web CLI into RedisInsight, so you have it handy and always ready to interact with your database. In the latest version of RedisInsight, the CLI has been improved by removing most command restrictions and providing better support for output formatting.

We initially limited the list of commands that a RedisInsight user could execute on the database. But we heard from our users that those limitations were not always helpful and that most of you would just like to run all commands as you do with redis-cli. That’s why RedisInsight’s integrated CLI can now run all non-blocking commands supported in the redis-cli.

If you are already familiar with how the redis-cli lets you interact with data and renders the data structures, we are now rendering them exactly the same way in RedisInsight 1.6. You’ll feel at home when switching between them.

[Watch the video](/wp-content/uploads/2020/06/image8.png)

Last but not least, the escape-string inputs and outputs are also rendered the same way as in redis-cli.

***Note:**** The RedisInsight CLI does not currently support a few blocking commands, as well as some commands that do not return standard streaming responses: MONITOR, SUBSCRIBE, PSUBSCRIBE, SYNC, PSYNC, SCRIPT DEBUG*

**Multi-line query editing**

We’ve made it easier to build and edit queries for RediSearch, RedisGraph, or RedisTimeSeries as you can now better structure them by using the multi-line editor. Often, however, your queries will need multiple lines, either because it’s a long query, or because you would like to structure it for easier understanding. So we improved the query editor to allow using multiple lines:

[Watch the video](/wp-content/uploads/2020/08/image4-resized-1-1.gif)

In order to use the multi-line query editor, just:

1. Use Shift+Enter to enter the multi-line mode
1. Then type “Enter” to add a new line
1. Use Ctrl+Enter to execute your query

You’ll notice that the formatting of your queries is protected in the history of your queries (when navigating using the Down Arrow or Up Arrow keys to see your previously executed queries).

**Secure connection: TLS support**

To prevent unauthorized access to your data and to encrypt the communication between the database and the clients, you can enable the Transport Layer Security (TLS) protocol on your Redis Enterprise databases. (To learn more about configuring TLS on your Redis Enterprise databases, refer to the [Configuring TLS Authentication and Encryption](https://docs.redis.com/latest/rs/administering/designing-production/security/tls-configuration/) in the Redis Enterprise documentation.)

When TLS is enabled, Redis Enterprise sends its client certificate to the database for authentication. To configure your database with TLS enabled, use the choices shown in the screenshot below:

[Watch the video](/wp-content/uploads/2020/06/image2-1.png)

If your database requires client authentication for mutual authentication, just select “Require TLS Client Authentication” in the “Add Redis Database” form—you’ll have the ability to provide the certificate-key pair as shown here:

![](/images/site-mirror/3663d424980f94e348bac19cd9f5fe8844e87ef7-1024x513.webp)

**Auto-discovery of Redis databases**

The latest version of RedisInsight makes it possible to configure connection details of your Redis Enterprise Software or Redis Enterprise Cloud databases with a single-click. Click on the “ADD REDIS DATABASE” button to search for databases from different locations, as shown here:

![](/images/site-mirror/83e4e4a081a7f09236dd6ed37f641138b85923c1-1024x528.webp)

In **Redis Enterprise**, you can explore databases on a particular cluster. Just provide the [connection details](https://docs.redis.com/latest/ri/using-redisinsight/auto-discover-databases/) and your databases will be listed, which lets you select and configure them in RedisInsight:

[Watch the video](/wp-content/uploads/2020/06/image7.png)

Configuration is even easier in **Redis Cloud Enterprise **(Pro Subscriptions only), as you have to provide only your [account key](https://docs.redis.com/latest/rc/api/concepts/authentication-and-authorization/#account-key) and [secret key](https://docs.redis.com/latest/rc/api/concepts/authentication-and-authorization/#secret-key) to connect your Redis Enterprise Cloud account and get the list of all your databases, as shown here:

![](/images/site-mirror/066d0d54fc2567c64e9285ffa2e9d470d6c87029-1024x524.webp)

[Watch the video](/wp-content/uploads/2020/06/image5.png)

If you have multiple subscriptions, you can choose from which ones you want to connect the databases:

[Watch the video](/wp-content/uploads/2020/06/image1-2.png)

***Note:**** You can learn more in the *[*Automatically Discovering Databases*](https://docs.redis.com/latest/ri/using-redisinsight/auto-discover-databases/) *section of the RedisInsight documentation.*

**Full-screen mode in RedisGraph, RedisTimeSeries, and RediSearch**

Integrated in the latest version of RedisInsight is the ability to maximize the space used for interacting with graphs or with the data from RediSearch or RedisTimeSeries. This is convenient when you need to explore a large set of data. You can also use this capability when you are screensharing or showcasing your models.

[Watch the video](/wp-content/uploads/2020/08/image15-resized-1.gif)

## Other notable enhancements and bug fixes

You can find the other notable enhancements and all bug fixes in the [Release Notes](https://docs.redis.com/latest/ri/release-notes/) section of the RedisInsight documentation.
