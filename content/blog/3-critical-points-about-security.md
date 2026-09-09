---
title: "3 Critical Points about Security"
linkTitle: "3 Critical Points about Security"
url: "/blog/3-critical-points-about-security/"
description: "Over the recent weeks there’s been an increase in the number of reports about NoSQL breaches in general, but also specifically in those relating to Redis. The latter is, in all likelihood, the..."
date: 2015-12-23
blogCategories:
- "Tech"
authors:
- "Itamar Haber"
lastmod: 2026-08-13
hidden: true
---

*By Itamar Haber, Technology Evangelist · Published 23 December 2015 · updated 13 August 2026*

![Blog tile image](/images/site-mirror/15dacb22ffd7d888b6b3c03026c9fa0c035001c3-140x92.webp)

![3 Critical Point about Security](/images/site-mirror/d791287c65015d1f451da0e544e515e616f9b4c0-635x200.webp)

Over the recent weeks there’s been an increase in the number of reports about [NoSQL breaches](https://krebsonsecurity.com/2015/12/13-million-mackeeper-users-exposed/) in [general](https://www.itworld.com/article/3016001/over-650-terabytes-of-data-up-for-grabs-due-to-publicly-exposed-mongodb-databases.html), but also specifically in [those](https://kevinchen.co/blog/postmortem-server-compromised/) relating to Redis. The latter is, in all likelihood, the aftermath of Salvatore Sanfilippo’s blog post “[A few things about Redis security](https://antirez.com/news/96).” That particular post was only the spark that lit the fire – I’d argue that the seeds for the breaches were laid in the ground long ago. And they’re still there unless you do something about it. But before continuing with the story, there are 3 critical points and 1 important note that I want you to take away from this:

1. Never leave an unprotected server open to the outside world
1. If your server has been compromised – burn it
1. Always read the documentation

**A note:** if you’re using the Redis Enterprise Cluster or Redis Cloud, then you can rest assured that the servers **have not been breached by this attack**. While it is possible to create an unprotected Redis database with our solutions, the overwhelming majority of our users’ databases, direct and from PaaS partners alike, are using at least one of the security measures we provide (such as password protection, source IP/Subnet whitelists and SSL). Furthermore, because our solutions provide separate operational and functional interfaces, even an unprotected database is not vulnerable to the full extent of this type of attack. That said, if your database is unprotected then your data is still at risk and you really should do something about it (hint: set a password).

Back to the origins of the breaches. In his blog post, Salvatore summarizes Redis’ security model with his typically brutal honesty: *“it’s totally insecure to let untrusted clients access the system, please protect it from the outside world yourself.”* To demonstrate how insecure “totally insecure” actually is, Salvatore shows how an unprotected Redis database can be used to gain access to the server running it.

The important thing here is that if you’re using Redis you **must not** ignore security. Once Redis isn’t run in a sandboxed environment, it is up to you (or your Redis provider) to take the steps needed to secure it properly. Redis databases can be made appropriately secure – here is a [documentation page](https://redis.io/topics/security) to get you started on doing just that. The first step to securing your Redis is reading the documentation. Redis has great official docs (it’s not just me saying that – check around) and [tons of other materials online](/redis-watch-archive).

Redis’ default password is set to none. Make sure to set it and set it to something non-trivial. Your security is only as good as the precautions you take.

The second step is really paying attention to the defaults. Trusting default values to work for you is like driving your car with your eyes closed and trusting the road to bend to your will. Unless the road is one that you fully control and have memorized, there’s little chance that you’ll get where you wanted to go. You would be wiser to keep your eyes open. When it comes to defaults, the only safe way to use them is know about them, which means – you guessed it – opening your eyes and reading their [documentation](https://download.redis.io/redis-stable/00-RELEASENOTES) or hiring a chauffeur.

Salvatore’s blog post was received only too well by the internets, initially inspiring “script kiddies” to crack unprotected servers for fun but eventually also being used for profit by professional cyber criminals. There also appears to be a [white hacker](https://gist.github.com/antirez/12d60c950fbfd8c8837e) ([artist’s rendition](https://twitter.com/itamarhaber/status/673803285883707392)) who sets passwords for unprotected servers. It is a shame that so much damage has been done but unless made public, this “vulnerability” would have stayed unnoticed by most and its consequences unknown. It wasn’t meant as a lesson, but we should learn from it not to take security for granted.

Future versions of Redis will include safer defaults (the release candidate for v3.2 that was released earlier today binds to 127.0.0.1 instead of 0.0.0.0 and [RC2 will have a new protected-mode](https://www.reddit.com/r/redis/comments/3zv85m/new_security_feature_redis_protected_mode/) enabled by default) and perhaps even [improved security mechanisms](https://github.com/redis/redis-rcp/blob/master/RCP1.md), but the responsibility for protecting the database will always be with the operator. If you’re operating your own Redis database in an environment that’s open to the outside world, you should review the security measures that you have in place and ensure that you’re protected. If you were using none, I recommended that you treat your server as suspect at the very least (nuke it and start from scratch if possible) – it is not unlikely that it was already breached.
