---
title: "Bug Fix: Lua and MessagePack"
linkTitle: "Bug Fix: Lua and MessagePack"
url: "/blog/bug-fix-lua-messagepack/"
description: "Apple Vulnerability Research made us aware of a potentially exploitable bug in Redis during May 2018. We took this disclosure very seriously and devoted resources to properly fixing this issue. We..."
date: 2018-06-13
blogCategories:
- "Announcements"
- "Product Releases"
- "Tech"
authors:
- "Redis  "
lastmod: 2025-03-04
hidden: true
---

*By Redis   · Published 13 June 2018 · updated 4 March 2025*

![Blog tile image](/images/site-mirror/0073e867b4e64f59de9047fdcde04295ba647e5c-772x550.webp)

Apple Vulnerability Research made us aware of a potentially exploitable bug in Redis during May 2018. We took this disclosure very seriously and devoted resources to properly fixing this issue. We are happy to tell you that Salvatore Sanfilippo (the creator and Lead Developer of open source Redis) made the patch for open source users and contacted all major Redis providers. We have pushed the fix to all our Redis Enterprise offerings: Cloud, VPC and Software.

## What is the bug?

Background: Redis embeds Lua for database-level scripting. The Lua scripting engine has a number of libraries included that are relevant to Redis use-cases. The original bug found was related to the MsgPack library, an implementation of the MessagePack serialization format. MessagePack is similar to JSON, but is more space efficient because it relies on binary encoding for control and, where possible, values themselves.

A function that accepts a variable number of arguments (variadic) is available in Lua to “pack” a message using the MessagePack format. The implementation behind this variadic function does not properly check stack availability. Without this check, a very large number of arguments can be passed into this function and cause an overflow. Because of the nature of Redis, it’s possible that that data coming directly from an untrusted user is being accepted and processed in this way.

There are no known ‘in-the-wild’ exploits of this bug. Because of the nature of this bug, as with any overflow situation, it is theoretically possible to perform remote code execution, however this would have to target very specific versions of Redis in very specific scenarios. We have not been made aware of any proof-of-concept of this behavior. More likely, this bug could be exploited to cause instability or a Redis server crash.

## Are there any related bugs?

During the review process it is customary to review other parts of the codebase for related errors. During this process, Salvatore assisted by the OSS community found similar bugs in the Lua implementation of packing and unpacking other structures. Fixes have also been implemented to address these issues.

Apple Vulnerability Research has also raised an issue regarding Sentinel remote configuration as a security risk. We do not agree with this finding as Redis specifically and explicitly enables remote configuration with the understanding that Sentinel should not be accessible by a public facing address.

Furthermore, Redis Enterprise doesn’t use Sentinel for high availability but rather other internal mechanisms, so this finding has no effect on Redis Enterprise users.

## Am I vulnerable?

All un-patched versions of Redis after 2.8.18 are potentially affected. To be at risk, you would have to be using both Lua and directly allowing unrestricted user inputs to be passed into scripts in very specific ways. While we believe it is a very small fraction of users using these features together in this way, we still suggest everyone apply the patch to prevent future vectors of attack on unpatched systems.

## How does the patch work?

The patch adds the proper checking of stack availability and returns an error if a Lua script tries to pack a message that is too large. This guarantees that, at run time, this particular attack will be impossible.

## Additional follow-up

We have checked other parts of Redis for similar bugs and so far have not found any further bugs with the same risk profile.

## If I’m a Redis Enterprise user (Cloud/VPC/Software) what shall I do?

In general, as long as you use one of our access control (Cloud Security Group) and authentication (SSL, Password)/access control (SIP) mechanisms, your Redis should be secured. In addition, If your application doesn’t use Lua scripting, you should not experience any issue whatsoever. And even if your application uses Lua, this bug happens in extreme conditions and only if your application calls Lua with a very large number of arguments. As this bug existed since Lua support in Redis was announced (in 2014) we believe you probably haven’t experienced the issue before and unless your application is changed dramatically, the likelihood for this to affect your Redis deployment is extremely low. Furthermore, Redis Enterprise comes with built-in replication, auto-failover and data-persistence mechanisms that ensure high-availability and durability of your data in cases of a Redis failure.

If you use Redis Enterprise software in an on-premises deployment you can download the latest Redis Enterprise version that includes the vulnerability fix from [here](/redis-enterprise/software/downloads/#downloads).

Last but not least, make sure your Redis Enterprise database is [protected by password and the access control and authentication mechanisms](/redis-enterprise/technology/redis-security-reliability/).

## If I’m a Redis open source user, what shall I do?

We suggest open source users first ensure that any Redis instances are not unrestrictedly open to the internet and then to upgrade to the latest version of Redis (3.2.12, 4.0.10, or 5.0-rc2, at time of writing) which can be found on the [redis.io downloads page](https://redis.io/download).
