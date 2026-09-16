---
title: "5 Basic Steps to Secure Redis Deployments"
linkTitle: "5 Basic Steps to Secure Redis Deployments"
url: "/blog/5-basic-steps-to-secure-redis-deployments/"
description: "Recent security reports identified the risk of attacks on misconfigured Redis databases. Here are five basic steps to secure your Redis deployments."
date: 2023-02-02
blogCategories:
- "Announcements"
- "Company"
authors:
- "Quincy Castro"
lastmod: 2025-03-27
hidden: true
mirrored: true
---

*By Quincy Castro, Contributor · Published 2 February 2023 · updated 27 March 2025*

![Blog tile image](/images/site-mirror/dd803210e9ea43497bf6c58b9d070cd550956aed-772x550.webp)

**Recent security reports identified the risk of attacks on misconfigured Redis databases. Here are five basic steps to secure your Redis deployments.**

Recently the cyber research community highlighted how attackers have been abusing insecurely configured Redis databases. As one of the world’s most used NoSQL databases, the huge installation footprint of Redis––both open source and commercial––makes it a natural target for attackers.

However, there are a number of basic steps Redis users can take to reduce the risk of attacks like the recent HeadCrab malware campaign identified by [AquaSec](https://blog.aquasec.com/headcrab-attacks-servers-worldwide-with-novel-state-of-art-redis-malware).

We should note that there are no signs that Redis Enterprise software or Redis Cloud services have been impacted by these attacks.

Since version 3.2.0, Redis Open Source (Redis OSS) enters a special mode called protected mode when it is executed with the default configuration and without any password required to access it. In this mode, Redis only replies to queries from the loopback interfaces. When clients connect from other addresses, Redis OSS replies with an error that explains the problem and how to configure Redis properly.

We expected protected mode to decrease the security issues caused by unprotected Redis instances executed without proper administration. But system administrators can ignore the error emitted by Redis; those administrators can disable protected mode or manually bind all the interfaces. It appears that there are plenty of these kinds of deployments which are being targeted by attacks such as HeadCrab.

Here are some basic recommendations for how to begin securing your Redis deployments:

- Deploy Redis inside a trusted network. Where possible, administrators should avoid exposing Redis directly to the public internet. Configure controls such as security groups and IP whitelisting to expose only the services that are necessary.
- Ensure you properly configure user access controls. This includes separating accounts for database users and administrators, enforcing strong passwords, disabling default user accounts, and implementing role-based access controls (RBAC). Redis Enterprise software customers have the option to enable LDAP authentication, while Redis Cloud customers can control access with their [corporate SSO systems](https://docs.redis.com/latest/rc/security/single-sign-on/saml-sso/).
- Enforce Redis TLS encryption and authentication for communication where possible. While Redis supports self-signed certificates, we highly recommend that you use certificates with a valid public chain of trust.
- Make sure that you send Redis logs to a remote logging service and that you monitor them for signs of abnormal usage or behavior.
- Finally, take our free [Redis University course](https://university.redis.com/courses/ru330/) to get educated on how to securely configure and deploy Redis. This course provides a straightforward walkthrough of the capabilities and best practices.

For more details on how to securely configure, deploy, and use Redis, visit our [open source](https://redis.io/docs/management/security/) and [commercial software](https://docs.redis.com/latest/rs/security/) documentation sites.
