---
title: "Is Redis Enterprise susceptible to RedisWannaMine?"
linkTitle: "Is Redis Enterprise susceptible to RedisWannaMine?"
url: "/blog/redis-enterprise-susceptible-rediswannamine/"
description: "On March 8th, Imperva published a blog post about a new cryptojacking attack that incorporates Redis. From an engineering perspective, this attack isn’t so much a marvel as a complicated Rube..."
date: 2018-03-22
blogCategories:
- "Announcements"
- "Tech"
authors:
- "Redis  "
lastmod: 2025-03-04
hidden: true
---

*By Redis   · Published 22 March 2018 · updated 4 March 2025*

![Blog tile image](/images/blog/0073e867b4e64f59de9047fdcde04295ba647e5c-772x550.webp)

On March 8th, [Imperva published a blog post](https://www.imperva.com/blog/2018/03/rediswannamine-new-redis-nsa-powered-cryptojacking-attack/) about a new cryptojacking attack that incorporates Redis. From an engineering perspective, this attack isn’t so much a marvel as a complicated Rube Goldberg machine that happens to have Redis as one of the cogs. Good news though:

- If you’ve followed even the most basic configuration and security best practices, this won’t affect you.
- [**Redis Enterprise**](/redis-enterprise/)** is completely impervious to this attack.**

The Imperva blog post does a good job of explaining the exploit, so I won’t “reinvent the wheel” here, but I will briefly outline how Redis is involved:

1. In a previously exploited machine capable of remote code execution, a simple scanner probes for Redis servers at the default 6379 port.
1. Once it finds an open (with no AUTH) Redis server available to this exploited original machine, the exploit does the following:
  1. Sets a few keys to crontab configuration lines
  1. Uses CONFIG SET to alter the location of the *dir* / *dbfilename* directives to various paths that are key to executing the crontab
  1. Performs a synchronous save of the dataset with SAVE

Experienced Redis geeks are probably screaming right now. Let’s go over all the poor decisions related to Redis that need to be made to be vulnerable for this exploit:

1. You need to be running Redis on the open internet. Redis’ security model is layered – Redis should never be a completely open-to-the-wild service. Even a simple firewall would be sufficient to stop this attack. In fact, Redis tries to stop you from doing this with the redis.conf file – you have to go out of your way to bind to all network interfaces.
1. There is no password on the Redis server. Always set a password and use AUTH before sending commands. Even a single character password (which is a terrible idea) is sufficient to stop this attack. The protected mode is enabled by default, which will prevent a universally network interface-bound instance from not having a password. So again, someone would have to manually alter the configuration to turn off protected mode.
1. Redis is at port 6379. While this is not the worst offense in the world, changing the port number away from defaults on any service is a cheap defense against attacks like this. Even this small change would be sufficient to stop this attack.

In short, this attack targets those who manually altered settings to do dangerous things.

Redis Enterprise, on the other hand, is protected out-of-the-box against these types of attacks by providing a pure separation between the management / administrative plane and the data-path plane. For example, all CONFIG commands of the standard Redis API are disabled. Additionally, Redis Enterprise comes with a built-in multi-layer security control that includes an access control layer, authentication layer, authorization, forensics layer, encryption layer and available protection layer. A detailed description of all of these features can be found on the [Redis Enterprise Security Technology](/redis-enterprise/technology/redis-security-reliability/) page.

So, there you have it—a *very* ill-advised configuration is at the heart of this exploit. Don’t jump through hoops to make your open source Redis server less secure… or just use Redis Enterprise and you’re golden.
