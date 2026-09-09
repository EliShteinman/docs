---
title: "New Governance for Redis"
linkTitle: "New Governance for Redis"
url: "/blog/new-governance-for-redis/"
description: "Today Salvatore Sanfilippo (a.k.a. antirez) announced that he’s stepping back from being the maintainer of the Redis project. We are honored and humbled that he requested us to succeed him as Redis..."
date: 2020-06-30
blogCategories:
- "Company"
authors:
- "Yossi Gottlieb"
- "Oran Agra"
lastmod: 2025-07-03
hidden: true
---

*By Yossi Gottlieb, Oran Agra · Published 30 June 2020 · updated 3 July 2025*

![Blog tile image](/images/blog/2ea9fb274df6ebe096c1a9a31088188d1d71bdf2-270x190.webp)

Today Salvatore Sanfilippo (a.k.a. [antirez](https://twitter.com/antirez)) [announced that he’s stepping back](http://antirez.com/news/133) from being the maintainer of the Redis project. We are honored and humbled that he requested us to succeed him as Redis project leads. With this change, we are excited to offer a new “community-driven” governing structure. Let’s look inside this new approach and see how we arrived at this decision.

## A big deal for Salvatore, for Redis, and for us

In the 11 years since Salvatore created Redis, it has become extremely popular and a standard tool in practically every modern application stack. During this time Salvatore has been, for the most part, the [BDFL](https://en.wikipedia.org/wiki/Benevolent_dictator_for_life) of the Redis project.

It was Salvatore’s final call on what went into or stayed out of Redis, how bugs should be fixed, what features were added, and what design tradeoffs were accepted. Basically, he was the only one to commit or, occasionally, press “Merge.” So, as you can imagine, his stepping back is a big deal for Redis.

The change in Salvatore’s role is also a very big deal for the two of us, because he has asked us to pick up Redis and take it forward.

## Deep experience with Redis

Fortunately, Redis is well-charted territory for us. Together, our journey with Redis development spans more than 15 years. Some of this time we’ve been busy creating Redis Enterprise and its unique features like [Redis on Flash](/redis-enterprise/technology/redis-on-flash/) and [CRDTs-based Active-Active replication](/landing/active-active/#:~:text=CRDT%2Dbased%20Active%2DActive%20Redis,data%20centers%20to%20remote%20geographies.&text=Redis%20CRDTs%20do%20all%20the,commands%20used%20by%20the%20applications.). Building these capabilities required in-depth involvement with the Redis core and working closely with Salvatore.

We’ve also been collaborating with Salvatore on many other core open source Redis initiatives: the modules API, diskless replicas, active memory defragmentation, TLS support, and many other optimizations, bug fixes, and general design discussions. Most recently, we’ve been busy with [RedisRaft](/blog/redisraft-new-strong-consistency-deployment-option/), a new open source project that is part of the Redis ecosystem.

## A new light-governance model for Redis

But having a good knowledge of the code base is not enough. When it comes to the dynamics of how the project is going to run in its new settings, that’s a new thing for us and for the Redis community in general.

When faced with such a big change, we feel it is important to clearly identify two main things: the qualities of the project we want to preserve and the opportunities to change and improve as the community continues to grow.

Redis has its own unique DNA. It’s hard to define or quantify, but it involves ideas like striving for simplicity, solving fewer problems but in a better way, and doing the right thing by default. All in the pursuit of speed and efficiency. Preserving and refining Redis’s unique DNA, even as Redis continues to evolve, will remain a priority for us.

As Salvatore steps back from maintaining Redis, the project’s scale can no longer be managed as a BDFL-style project. We see this as an opportunity for Redis to adopt a new model that, hopefully, will promote more teamwork and structure and let us scale up its development and maintenance processes.

Salvatore has always been very open and collaborative with the Redis community. It was a common practice for him to listen to what users are asking, and to share his thoughts and ask for user feedback. This is something we’re going to work hard to preserve. Taking it a step further, we want to make Redis more approachable, and make it easier for community members to become effective contributors taking a more active and significant part in its development.

To facilitate this vision we are proposing a new light-governance model for Redis, which is described [on the project’s site](https://redis.io/topics/governance). The new model is based around forming a small core team of developers—individuals we will gather based on their demonstrated Redis familiarity, contributions, and commitment.

The first person to join the team will be [Itamar Haber](https://github.com/itamarhaber), who is known to many in the Redis community. In the coming days and weeks, we’ll be working to make this core team a reality and reflect the community’s contributions to Redis. We look forward to announcing more core team members soon.

We wish to thank Redis for supporting us in this process and for its ongoing commitment to the open source Redis project.

Last and definitely not least, we wish to thank Salvatore for all his hard work, for his wonderful company on this Redis journey, and for his trust.
