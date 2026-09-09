---
title: "Redis: the Lightweight and Scalable Database"
linkTitle: "Redis: the Lightweight and Scalable Database"
url: "/blog/redis-lightweight-scalable-database/"
description: "We are FreeWheel, a Comcast company providing solutions to the Media Advertising industry to enable efficiency and insight into all aspects of campaign workflows, across media for media buyers and..."
date: 2018-04-27
blogCategories:
- "Company"
- "How To and Tutorials"
authors:
- "Daniel Jones"
lastmod: 2025-03-04
hidden: true
---

*By Daniel Jones · Published 27 April 2018 · updated 4 March 2025*

![Blog tile image](/images/blog/0073e867b4e64f59de9047fdcde04295ba647e5c-772x550.webp)

We are [FreeWheel](https://freewheel2018.tv/), a Comcast company providing solutions to the Media Advertising industry to enable efficiency and insight into all aspects of campaign workflows, across media for media buyers and publishers.

Our system is based on a [microservices architecture](/solutions/microservices/). The ecosystem of products that support the workflow has had to evolve significantly over the last 15 to 20 years in terms of tech stack and infrastructure. Part of that evolution was ensuring a robust and quick-caching mechanism to support shared data storage within our ecosystem and across environments.

A few years ago, our system’s caching mechanism was a simple per-server-per-application store, utilising the built-in technologies available on Microsoft IIS and running .NET web applications. This was sufficient for isolated domain data with no shared concerns outside of a single request. But as the ecosystem grew, so did the need to share that data with processes running in a different application or a different server pool. Problems with stale caches surfaced. Rolling out our own orchestrations that attempted to ensure an up-to-date store resulted in unmaintainable and hard-to-scale code. We looked at many solutions, including memcache and various derivatives such as Couchbase, but in the end we settled on [Redis](https://redis.io/).

![](/images/blog/3c1a42bfc9898e42cd2489cedea380a2269ee0b5-466x416.webp)

## Old Model

Redis brought with it a growing reputation as the standard bearer in lightweight data storage, performance and reliability. In short, it just worked, and we weren’t required to waste time troubleshooting the underlying technology. Instead, our time was spent fine tuning a clean implementation, which ensured failover support and handling of flexible [cache invalidation](/glossary/cache-invalidation/) policies (depending on the use case). We could also be sure that the data we stored in Redis persisted quickly to a farm of servers and was available to many different deployed applications so that users were always getting the correct data.

![](/images/blog/3537ed96e9d8a4c5b36f4cb4b833b2e9ef58babf-464x501.webp)

## Fine Tuning With Redis

Moreover, there is good community support and documentation for Redis development, with supporting libraries such as StackExchange. Redis gave us the right amount of abstraction to achieve what we need. We were also able to easily integrate Redis to address concerns such as health monitoring against our existing stack. This was a fundamental plus point, as we have a mature yet quickly growing product with new releases every two weeks. We now deploy [Redis Enterprise](/redis-enterprise/) to our production servers, both bare metal and cloud based, supporting users in Europe, US and APAC.

The transition to Redis Enterprise has been a positive experience. Using Redis Enterprise has made the system more stable and most importantly, we have identified more use cases where Redis can be utilized, which will improve the user experience further. It will allow us to achieve things that may have otherwise been more challenging. Right now, we are designing the infrastructure needed for automation of some internal processes that will facilitate Continuous Integration scenarios, which are key to our success and allow us to move quickly. Building these solutions around Redis will allow us to be more sophisticated in our approach and give us more scalable results.

*This is a guest post by Daniel Jones, a Technical Architect at FreeWheel. He can be reached through his LinkedIn page https://www.linkedin.com/in/daniel-jones-5b93774/*
