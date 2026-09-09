---
title: "A Developer’s Guide to RedisConf 2021"
linkTitle: "A Developer’s Guide to RedisConf 2021"
url: "/blog/developers-guide-redisconf-2021/"
description: "We just wrapped a successful RedisConf 2021, where thousands of Redis enthusiasts gathered to rediscover the power of real-time data. This year’s agenda included 60+ breakout sessions, four..."
date: 2021-05-12
blogCategories:
- "Tech"
authors:
- "Kyle Banker"
lastmod: 2025-03-27
hidden: true
---

*By Kyle Banker, Sr. Director, Field Engineering · Published 12 May 2021 · updated 27 March 2025*

![Blog tile image](/images/blog/8d56d5eb481a4f4efa9e69782776f09599601a68-772x520.webp)

We just wrapped a successful RedisConf 2021, where thousands of Redis enthusiasts gathered to rediscover the power of real-time data. This year’s agenda included 60+ breakout sessions, four comprehensive training courses, and several keynotes and interviews that explored Redis best practices, pro tips, and new features. Among the many great stories and presentations, we wanted to highlight a few that might be of interest to the developer community at large. Whether you’re brand new to Redis or already an expert, there’s something for everyone. Here’s our guide to RedisConf 2021:

## For brand-new Redis developers

If you don’t know much about Redis and just want to know what it’s capable of, you should hear from Spleet Software Engineer [Michael Owolabi](https://www.linkedin.com/in/imichaelowolabi/) in his session, [Yes! Redis can do that](https://redisconf.com/redisconf21/modules/85405/agenda/session/265320). Michael provides an enthusiastic take on Redis, starting with caching before moving on to full-text search use cases and the ins and outs of persistence.

With an in-depth guide to how he found Redis, Michael’s examination of Redis helped him realize its capabilities beyond the cache, and ultimately how it can be used as a general, high-performance in-memory data store.

## For the Redis community

Redis remains committed to the development of open source Redis. And while we directly employ many of the core Redis contributors, we’re also encouraging the larger community to contribute more and more to core Redis.

[Itamar Haber](https://www.linkedin.com/in/itamarhaber/), Technology Evangelist for Redis and a Redis core team member, presented [Redis 6.2: For the community, by the community](https://redisconf.com/redisconf21/modules/85405/agenda/session/265310). This talk covers Redis’ new community-driven governance model and [the formation of the core team](/blog/redis-core-team-update/). Now the emphasis is on **community**—since July 2020, we’ve seen an 86% increase in unique contributors!

Itamar’s talk also covers the new features in Redis 6.2. These include ACLs for Pub/Sub, incremental eviction, and numerous improvements to the core Redis data structures (e.g., auto-claiming pending entries in streams and setting expiration on GET).

If you want to know about the future of Redis, then you should check out [Redis 7.0 and beyond](https://redisconf.com/redisconf21/modules/85405/agenda/session/265311). In this session, [Meir ](https://www.google.com/url?q=https://www.linkedin.com/in/meir-shpilraien-501469104/&sa=D&source=editors&ust=1620854711255000&usg=AOvVaw0Z43CijfULuJbrTwyWCa7z)[Shpilraien](https://www.linkedin.com/in/meir-shpilraien-501469104/), Software Architect at Redis, discusses the design of Redis Functions, which will provide a **language-agnostic programmable interface **(i.e., JavaScript support!) to Redis. [Yossi Gottlieb](https://www.linkedin.com/in/yossi-gottlieb-40842/), a Redis core team member and longtime Redis Chief Architect, also presents the latest on [RedisRaft](https://github.com/RedisLabs/redisraft), a dual-licensed Redis module that provides **strong consistency** for Redis.

Another core team member, AWS Senior Software Development Engineer [Madelyn Olson](https://www.linkedin.com/in/madelyn-olson-6a5053b6/), presented [Better together: How AWS is helping build a stronger open source community](https://redisconf.com/redisconf21/modules/85407/agenda/session/265370). In this session, Madelyn reflects with her colleagues Carl Lerche and Matt Asay on their work with core Redis and on the strategic importance of open source Redis to AWS and its customers.

## For Node.js developers

RedisConf 2021 had Node.js developers covered. If you’re new to Redis, or just want to see how to build a complete and highly responsive application with it, see [The Node.js Redis ](https://redisconf.com/redisconf21/modules/83900/info-page)[Crash Course](https://www.google.com/url?q=https://redisconf.com/redisconf21/modules/83900/info-page&sa=D&source=editors&ust=1620854711260000&usg=AOvVaw0Q6yLOGA2TIptnmIbSLPuo). In this new course, built specifically for RedisConf, Senior Curriculum Software Engineer [Simon Prickett](https://www.linkedin.com/in/simonprickett/) teaches you how to build a social check-in app using Express, Redis, and the Redis modules. Not to be missed!

For an enlightening take on enhancing the performance of Node.js apps on Redis, see [Solving Head-Of-Line blocking with auto pipelining](https://redisconf.com/redisconf21/modules/85405/agenda/session/265327). In this session, NearForm Technical Director [Matteo Collina](https://www.linkedin.com/in/matteocollina/) describes the new auto-pipelining features of [ioredis](https://github.com/luin/ioredis) and how it improved some of his team’s benchmarks by 35-50%.

## For Spring developers

This year, one of our goals for RedisConf was to meaningfully support the Spring and Java community, and for that, we could not have found a better expert than [Josh Long](https://www.linkedin.com/in/joshlong/), Spring Developer Advocate at VMWare.

In his talk, [An application framework worthy of Redis](https://redisconf.com/redisconf21/modules/85405/agenda/session/265312), Josh quickly takes you through the process of building a **Spring Boot** application powered entirely by Redis. [Brian Sam-Bodden](https://www.linkedin.com/in/sambodden/), Developer Advocate for Java at Redis, joins Josh in this whirlwind talk to add support for RediSearch to the stack.

If you want something more comprehensive, see Brian’s course, [Redis and Spring: Building High Performance REST APIs](https://redisconf.com/redisconf21/modules/83977/info-page). This training course covers everything you need to know to be successful with Redis and **Spring Boot and Spring Data Redis**. Brian teaches the basics of domain modeling and caching, but quickly progresses to implementing:

- full-text search, faceted search, and auto-complete with RediSearch
- a recommendation service with RedisGraph
- Redis Streams, and, well, quite a lot more.

## For running Redis at scale

This year, we put together a brand new training course called [Running Redis at Scale](https://redisconf.com/redisconf21/modules/84081/info-page). This course considers scaling broadly, including discussions of security and observability. But the course focuses primarily on classic scaling concerns such as **high availability** and **sharding**. Our technical enablement architects, [Elena Kolevska](https://www.linkedin.com/in/ekolevska/) and [Kurt Moeller](https://www.linkedin.com/in/kurtfm/), present these topics for open source Redis and include numerous examples and labs using **Redis Sentinel** and **Redis cluster**.

Elena and Kurt also briefly discuss **Redis Enterprise Software** and how it contrasts with the features of open source Redis.

If you just want a Redis at scale war story, check out [Martin Perez’s](https://www.linkedin.com/in/mpermar/) session [Look ma, no database!](https://redisconf.com/redisconf21/modules/85406/agenda/session/265351) Here, Martin explains how Cisco Webex uses Redis as a backend to a **billion-request-per-week service**.

## For data scientists and MLOps

More and more, Redis is coming to the fore as a high-performance online feature store. In [Redis as an online feature store](https://redisconf.com/redisconf21/modules/85405/agenda/session/265324), Redis’ Chief Business Development Officer [Taimur Rashid](https://www.linkedin.com/in/taimurrashid/) and Software Engineer [Dvir Dukhan](https://www.linkedin.com/in/dvir-dukhan-73548244/) show how you can use Redis to manage features and increase performance at the model building and inferencing stages.

And for a real world example, see [Redis as a scalable feature store](https://redisconf.com/redisconf21/modules/85406/agenda/session/265358). In this session, ML Platform Engineer [Arbaz Khan](https://www.linkedin.com/in/arbazkhan002/) and Technical Lead Manager [Zohaib Hassan](https://www.linkedin.com/in/zohaibsibtehassan/) of DoorDash discuss how they use Redis to manage billions of features and serve them with ultra-low latency.

## The community growth continues

RedisConf 2021 demonstrated the continued growth of Redis as a core component in every developer’s toolset. If you haven’t had a chance to check out [this year’s 60+ sessions](/redisconf/sessions/), we hope that the recommendations here provide a useful entry point. All content is available on-demand until May 20, so there’s still time to [log in](/redisconf/)!

As always, we love hearing your stories and helping where we can. If you have any thoughts, ideas, or questions about Redis today, consider stopping by our [Redis Discord server](https://discord.gg/redis) and saying hello! And thanks again to the many speakers, community members, and Redis employees who made this year’s conference one of the best yet.
