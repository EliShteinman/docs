---
title: "Expanded Microsoft Partnership Highlights RedisConf 2020 Takeaway"
linkTitle: "Expanded Microsoft Partnership Highlights RedisConf 2020 Takeaway"
url: "/blog/expanded-microsoft-partnership-highlights-redisconf-2020-takeaway/"
description: "RedisConf 2020 Takeaway is in the books. This innovative virtual event became a unique forum for sharing the latest Redis news, product previews, and technical insights with thousands of online..."
date: 2020-05-18
blogCategories:
- "Company"
authors:
- "Mike Anand"
lastmod: 2025-03-27
hidden: true
---

*By Mike Anand, Former Chief Marketing Officer · Published 18 May 2020 · updated 27 March 2025*

![Blog tile image](/images/site-mirror/ca94f1a7cc61b5d196fa2a20b4fc7c46bf27c3f1-2362x1604.webp)

[RedisConf 2020 ](https://redisconf.com)[*Takeaway*](https://redisconf.com) is in the books. This innovative virtual event became a unique forum for sharing the latest Redis news, product previews, and technical insights with thousands of online attendees, all in the context of rediscovering the wide range of things Redis can do, far beyond the most-common caching use case. Highlights include [Salvatore Sanfilippo](https://twitter.com/antirez?ref_src=twsrc%5Egoogle%7Ctwcamp%5Eserp%7Ctwgr%5Eauthor)’s demo of the new [Redis 6.0](/blog/diving-into-redis-6/), and the formal rollout of [Redis Enterprise 6.0](/blog/rediscover-redis-security-with-redis-enterprise-6/), as well as general availability of new technologies such as RedisGears 1.0 and RedisAI, a preview of RedisRaft, and an early-stage partnership around secure enclaves with Anjuna.

The one clear “takeaway,” if you will, is that Redis and Redis Enterprise continue to push boundaries and gain momentum. Redis Enterprise 6.0 is the most secure, easiest to deploy version of Redis ever, empowering developers to address a wider variety of enterprise use cases—including as a primary data store—than ever before. The new GA versions of RedisGears and RedisAI push the boundaries of what developers can do with Redis to achieve more with data.

More on that in a moment, but the biggest news, of course, was revealed in the opening keynote (watch the [video of the entire presentation below](https://youtu.be/TwhfBLwgTKI)). [Redis Co-Founder and CEO Ofer Bengal](/company/team/ofer-bengal/) shared many stories of our customers going beyond cache with Redis, and introduced [Microsoft Corporate Vice President of the Developer Division Julia Liuson](https://azure.microsoft.com/en-us/blog/microsoft-and-redis-labs-collaborate-to-give-developers-new-azure-cache-for-redis-capabilities/) to discuss the expanded partnership between the two companies, adding a pair of new Enterprise Tiers to the familiar and popular Azure Cache for Redis.

*To see the Microsoft Azure announcement, jump to *[*1:16:10*](https://youtu.be/TwhfBLwgTKI?t=4570)

## Redis and Microsoft empower developers

Microsoft is working to “empower every developer and every development team on the planet to build more applications,” Liuson told the online attendees. “We are also committed to building the most developer friendly cloud, bringing developer tools for development, productivity, and collaboration.”

She said that developers love the fully managed [Azure Cache for Redis](https://azure.microsoft.com/en-us/services/cache/) offering, which will be bolstered with [two new Enterprise Tiers](/blog/redis-enterprise-on-azure-cache-for-redis/). The Enterprise Tier will be an in-memory offer using Redis Enterprise, while the Enterprise SSD Tier will be built on top of the[ Redis on Flash](/redis-enterprise/technology/redis-on-flash/) technology, and deliver up to 10 times larger cache sizes and similar performance at a lower price per gigabyte.

“The new Azure Redis Enterprise provides significantly improved developer productivity,” Liuson said. “Developers can easily use the latest version of Redis and use all of its native data structures and modules,” including [RedisBloom](/modules/redis-bloom/), [RedisTimeSeries](/timeseries/), and [RediSearch](/search/).

“Developers can also deploy a Redis cluster within minutes, to scale without additional steps,” Liuson added. Developers who are already familiar with Azure Cache for Redis can leverage the same interface and management experience so they can immediately start working with the new service, she said.

**Resiliency, security, and compliance**

Because Redis is frequently used in mission-critical applications, resiliency, security, and compliance are not optional. Liuson promised to “deliver enterprise-grade SLAs offering additional uptime, through Redis Enterprise’s active geo-replication technology across Azure regions. With this joint partnership, the Enterprise Tier will support all of the most stringent requirements on security and compliance that is demanded by our most security-minded customers.”

It’s not just a technology partnership, though. “We want to make it easy for customers to acquire and use open source technologies directly in Azure,” Liuson said, “and deliver deep integration around identity, security, and unified billing.” Liuson emphasized that this will significantly increase both operational efficiency and developer productivity.

**A simplified user experience**

The new tiers will also provide a simplified administration and billing experience, as well as streamlined support. Customers can set Redis cache size in real-time based on their needs, potentially delivering cost savings with Azure’s consumption-based pricing model. “Redis Enterprise usage will simply show up in customers’ monthly Azure bill,” Liuson promised. The companies will also deliver a simplified and streamlined support experience—customers will contact Microsoft, which will then pull Redis in for any software questions.

For more on how it works, watch the [video demo of Azure Cache Redis Enterprise](https://youtu.be/TwhfBLwgTKI?t=5151) from the keynote. The new tiers are available now in [private preview](/redis-enterprise-microsoft-azure/). “We are working hard for public preview this fall,” Liuson concluded, “and general availability by winter.”

## Redis 6.0 takes center stage

An appearance by Salvatore Sanfilippo, the original creator of Redis, is always a RedisConf highlight, and this year he was able to demo the brand-new [Redis 6.0](/blog/diving-into-redis-6/), released just two weeks ago.

Sanfilippo noted many fixes and powerful new features like access control lists (ACLs), client-side caching, cluster manager in the Redis CLI, replication improvements, and even a Gopher implementation, among others. He also showed off the longest common subsequence algorithm, which is often used to compare and visualize genetic sequences, of the RNA of viruses, for example.

With all that, Sanfilippo wondered, “is Redis becoming too complex?” He did a quick check of the number of lines of code in the system. The answer: “I think we are still small! … What I want to stress is that Redis is still the simple thing … it looks like a toy … but it can actually solve really interesting problems when developers apply their creativity.”

Sanfilippo also took an in-depth look at tracking. “It’s just 300 lines of code and a bit more comments,” he noted, “but it could be the most significant feature of Redis 6.0, perhaps because it can change a lot of things.” Watch his live-coding explanation and demo of tracking—basically the server-side support for the client-side caching protocol—in the video below:

[Watch the video](https://www.youtube.com/watch?v=TwhfBLwgTKI&feature=youtu.be&t=987)

## From Redis 6.0 to Redis Enterprise 6

After Sanfilippo discussed what’s new in Redis 6, [Redis Chief Product Officer Alvin Richards](https://twitter.com/jonnyeight?lang=en) took the virtual stage to talk about how Redis Enterprise 6.0, which extends the open source version in a number of key ways for enterprise customers to increasingly use it as a powerful primary database, not just as a cache. It’s no secret that Redis is often used as a cache to speed up other database systems, but over the years Redis has come a long way toward becoming an increasingly credible database option, adding a number of critical enterprise-grade features. Redis Enterprise 6.0 highlights the security and management side of things, giving customers better control of user and enterprise access and security.

Specifically, that means ACLs with role-based access control (RBAC) to simplify administration at scale. Richards also noted that Redis Enterprise 6 includes TLS 1.3 support and Mutual TLS Authentication.

Meanwhile, as data volume and velocity keep growing, customers increasingly need to work with event-based streams, and Redis Enterprise 6 extends Active-Active to support Redis Streams to take advantage of that trend.

Much remains to be done of course, and Richards also discussed new security initiatives with Intel and Anjuna around secure enclaves, which bring hardware and software together into an integrated security approach to encryption in use. (For more on this, see our blog post on [Secure Enclaves Could Be the Future of Security](/blog/secure-enclaves-future-of-data-security/).)

Finally, he touched on our work on a new RedisRaft module to support strong consistency for large-scale enterprise applications, based on the popular Raft consensus-based algorithm for replicating state across many machines. “We are announcing that sometime early this summer, we will be open sourcing RedisRaft,” he said.

Of course, as Chief Product Officer, Richards couldn’t sign off without offering a peek at what’s coming next:

[Watch the video](https://www.youtube.com/watch?v=TwhfBLwgTKI&feature=youtu.be&t=1895)

“Now that we’ve got role-based access control,” Richards said, “many people will want to configure them through external identity providers. So Active Directory or LDAP. The next step is to be able to configure those roles, not just within a Redis Enterprise cluster, but from outside the Redis Enterprise cluster. Again, this simplifies the administration burden.”

Richards concluded that we’re also adding TLS 1.3 support so we get the latest ciphers, and we’re adding mutual TLS authentication. And, finally, we’re extending Active-Active to support RediSearch, which lets you do full-text search, stemming, fuzzy matching, and much more.

## Doing more with data

Much of the keynote focused on doing more with your applications, but Redis Co-Founder and CTO [Yiftach Shoolman](/company/team/yiftach-shoolman/) addressed the issue of “doing more with data.” For one thing, he said, “it’s about time to take AI to production,” and move beyond AI training to AI inferencing. Shoolman noted that analysts estimate that revenue associated with AI inferencing will soon surpass the revenue associated with AI training. That’s because the AI training model is complex, he said, while inference lets you tweak existing AI models using your own reference data and get to production much faster.

[Watch the video](https://www.youtube.com/watch?v=TwhfBLwgTKI&feature=youtu.be&t=3347)

That’s where the [new Redis AI module](/modules/redis-ai/) (co-developed by Redis and [Tensorwerk](https://tensorwerk.com/)) comes in. By placing the AI serving engine inside Redis, RedisAI reduces the time spent on external processes and can deliver up to 10x more inferences than other AI serving platforms at a much lower latency. This increased performance can help drive better business outcomes for leading AI-driven applications such as fraud detection, transaction scoring, ad serving, recommendation engines, image recognition, autonomous vehicles, and game monetization.

**Learn more about** [**RedisAI**](/modules/redis-ai/)**.**

Finally, to orchestrate the flow in this new data architecture, Shoolman said, “you need to have a fully programmable serverless engine that runs in a fully distributed manner, closer to where your data lives, preferably inside the database.” Redis needs serverless to enable cluster-wide data processing, reliable event processing, and to orchestrate your AI transactions—at the speed of Redis.

RedisGears, announced a year ago, is a serverless engine for infinite programmability in Redis, and Yiftach announced that RedisGears is now generally available. RedisGears lets you program everything you want in Redis, deploy functions to every environment, simplify your architecture and reduce deployment costs, and run your serverless engine where your data lives.

**Learn more about **[**RedisGears**](/modules/redis-gears/)**.**

## Rediscover Redis: More than a cache

![](/images/site-mirror/340e1ea1ff0a5a41c80a9db297bd6bd0363cbe51-369x211.webp)

Put it all together and once thing is clear: While many people know that Redis is an awesome caching system, that’s only the beginning of what Redis can do. According to Ofer Bengal, maybe that’s because running in-memory may still be perceived as not robust enough for a primary database, or perhaps we need to do more to expose the Redis community to the enhanced capabilities added to Redis over the years.

Whatever the cause, Bengal said, “with so many embedded tools and capabilities, Redis can serve as your primary database for many of your modern apps and complex use cases, while guaranteeing the best performance. … We hope you will rediscover Redis and its unique capabilities as a database.”

**More on RedisConf 2020 *****Takeaway***

For more on everything that went down at the event, check out this press coverage:

- **TechCrunch:** [**Microsoft Partners with Redis to Improve Its Azure Cache for Redis**](https://techcrunch.com/2020/05/12/microsoft-partners-with-redis-labs-to-improve-its-azure-cache-for-redis/)
- **ZDNet Database Week: Database Week: **[**Microsoft OEMs Redis Enterprise for Azure**](https://www.zdnet.com/article/database-week-microsoft-oems-redis-enterprise-for-azure/)
- **Channel Buzz: **[**Redis Urges Users to Rediscover Redis as a Database at Their Virtualized Conference**](https://channelbuzz.ca/2020/05/redis-labs-urges-users-to-rediscover-redis-as-a-database-at-their-virtualized-conference-33849/)
- RedisConf keynote [video demo of Azure Cache Redis Enterprise](https://youtu.be/TwhfBLwgTKI?t=5151)

**You can also watch many of the presentations from **RedisConf 2020 *Takeaway *[on the conference site](https://redisconf.com/).
