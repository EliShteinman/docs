---
title: "Top 9 Takeaways from RedisConf 2021"
linkTitle: "Top 9 Takeaways from RedisConf 2021"
url: "/blog/top-9-takeaways-from-redisconf-2021/"
description: "Every year Redis enthusiasts from around the world gather at RedisConf 2021, our annual real-time data conference. Last year was our first virtual RedisConf, and this year was bigger and..."
date: 2021-04-30
blogCategories:
- "Company"
authors:
- "Mike Anand"
lastmod: 2025-03-27
hidden: true
mirrored: true
---

*By Mike Anand, Former Chief Marketing Officer · Published 30 April 2021 · updated 27 March 2025*

![Blog tile image](/images/site-mirror/529e4704fbbf970043079e1dc032f1691735339d-772x520.webp)

Every year Redis enthusiasts from around the world gather at RedisConf 2021, our annual real-time data conference. Last year was our first virtual RedisConf, and this year was bigger and better—more than 12,000 developers, architects, and business and technology leaders from 122 countries registered for keynotes, fireside chats, 60+ breakout sessions, and training from April 20–21.

RedisConf 2021 was all about rediscovering the power of real-time data. We brought 10 keynote speakers to the stage to discuss how Redis has grown over the past year, what’s in store for the future, and how their businesses leverage real-time data to meet customer demands. You can get the full experience by watching the [**keynotes (and all breakout sessions!) on demand**](/redisconf/) for the next month, but here’s a quick digest on the key takeaways from RedisConf 2021:

## 1. The age of real-time is here

Across our keynotes, we consistently heard the same point: Real-time experiences are no longer nice-to-have, they’re an expectation in every digital business, with customer-facing front end apps. Redis as a real-time data platform offers more capabilities and choices for your needs—along with the high performance it’s known for. From strong consistency to integrated data models to artificial intelligence (more info on each below!), Redis has what you need to deliver the real-time, digital experiences that today’s customers expect.

## 2. Now you can index and query JSON documents at the speed of Redis

JSON is the lingua franca of the internet. With billions of JSON documents part of each and every digital service, being able to retrieve information from JSON at the speed of Redis and help deliver real-time experiences has been a project we’ve been working on for the past year—and the combination of RedisJSON with RediSearch is going to be in preview next month! This new capability allows indexing, querying, and search in JSON documents stored in Redis at a speed 3 to 37 times faster than other key document databases.

Plus, later this year you will be able to deploy and run a fully managed RedisJSON+RediSearch database across multiple regions/clouds or hybrid deployment—closer to where your users are—using Active-Active Redis Enterprise. Check out [Yiftach Shoolman’s day one keynote](https://redisconf.com/redisconf21/modules/79868/agenda/session/257171) to see our brand new retail demo application, *RedisMart*, with all those new capabilities in action!

## 3. Getting real-time apps to market faster with Redis

Redis has established its reputation as one of the most developer friendly databases—with the set of supported data structures packaged with Redis, developers can spend less time on data manipulations and more time on app logic. With the set of Redis modules—RedisGraph, RedisBloom and RedisTimeSeries—developers can add more advanced use-cases while using the same set of familiar Redis interfaces, and get more code developed faster! We’ve seen strong adoption trends for its Redis modules with a YoY increase of 60%—and for the first part of this year, the increase has been 120% compared to the same time last year.

Be sure to check out the [developer (Build with Redis) track sessions](https://redisconf.com/redisconf21/modules/85405/agenda/list?filterMode=additive&&&tracksOpen=false&activeTab=1&activeView=1&activeDate=1618815600000) and the *RedisMart* demo retail app we introduced in [Yiftach Shoolman’s day one keynote](https://redisconf.com/redisconf21/modules/79868/agenda/session/257171), all available on demand for the next month!

## 4. We stay committed to our open source roots

Last year we introduced our new [community governance model](/blog/new-governance-for-redis/)—made of a core team from Redis, AWS, and Alibaba—taking his place. The team announced the release of [Redis 6.2](/blog/redis-6-2-the-community-edition-is-now-available/) earlier this year, and they plan to increase the cadence of major Redis releases to two per year, with Redis 7.0 planned for Q3 of this year. Learn more about these releases in [Yiftach Shoolman’s day one keynote](https://redisconf.com/redisconf21/modules/79868/agenda/session/257171) and the breakout sessions on [Redis 6.2](https://redisconf.com/redisconf21/modules/85405/agenda/session/265310) and [7.0](https://redisconf.com/redisconf21/modules/85405/agenda/session/265311).

## 5. Redis expands to strong consistency database support

Redis adoption as a primary database is on the rise with more than 66% of Redis customers relying on Redis as their main database, and we want to extend the functionality and make Redis suitable for use cases where strong consistency is a requirement.

[RedisRaft](/blog/redisraft-new-strong-consistency-deployment-option/)—a new strong-consistency deployment option first introduced at RedisConf 2020—will be generally available with Redis 7.0.

## 6. Redis is critical in building AI-based real-time applications

There’s no question that real-time capabilities are becoming increasingly important for supporting AI use cases in application stacks. At the heart of AI reference architectures is the [feature store](/solutions/feature-store/), the bridge between your data and machine learning models. In the past year companies such as Netflix, Uber, Doordash, Airbnb, and Spotify have published their AI stack architecture, where Redis consistently serves as the online feature store, and combined with a model store and RedisAI inference engine, addresses the need to deliver real-time AI services.

We’ll be gradually releasing RedisAI online [feature store](/solutions/feature-store/) specific capabilities on Redis Enterprise Cloud, our fully managed cloud service, in the second half of 2021.

## 7. Accelerating Redis cloud deployments with GKE on Anthos

In addition to the existing Google Cloud offering of Redis Enterprise as a fully managed Database-as-a-Service ([DBaaS](/blog/what-is-dbaas/)), we’re now adding a self-managed option of Redis Enterprise with Anthos on GKE. Anthos extends the use of GKE to other platforms outside the Google Cloud and allows standardized and rapid deployment on other clouds and on premises. To learn more about this newly announced support, [tune in to Jeff Reed’s day two keynote](https://redisconf.com/redisconf21/modules/79868/agenda/session/257187) or visit our [Google Cloud page](/cloud-partners/google/).

## 8. Redis Enterprise Cloud is now available in AWS Marketplace

Last September Redis was named an Advanced Technology Partner of AWS. Now there’s even greater support for Redis customers on AWS, with the availability of all Redis Enterprise Cloud in AWS Marketplace. AWS customers will be able to find Redis Enterprise Cloud on AWS’ public listing, use AWS credits towards Redis Enterprise on top of AWS, and benefit from simplified and consolidated billing. Check out our [AWS page](/cloud-partners/aws/) to learn more about this announcement.

## 9. Our customer shared perspectives on what real-time data means to them

Real-time experiences are now a part of every digital business. This year we hosted three key Redis customers on the main stage and asked them to share how they make real-time services a reality in their respective businesses. Mike Lee, Head of Enterprise Payment Architecture at Capital One, took the audience through the transformation taking place in the payments space with fintech disruptors, crypto currencies, and new regulations and how he built an architecture to deal with today’s and tomorrow’s real-time needs. You can tune into Mike’s segment on our [day one keynote](https://redisconf.com/redisconf21/modules/79868/agenda/session/257171). Dave Anderson from Genesys, a contact center solutions provider, gave perspective on the criticality of real-time experience in the voice application in the call center, and Alex Curtin from Unity—one of the largest technology providers for the gaming industry—shared his story on accelerating gaming developers onboarding with Redis Enterprise on GKE. Tune into Dave’s and Alex’s segments on our [day two keynote](https://redisconf.com/redisconf21/modules/79868/agenda/session/257187).

*Get the full story on these takeaways by checking out the entire keynotes, available to view on demand for the next month on the RedisConf platform. If you’d like share your feedback on the event or the keynotes, don’t hesitate to reach out to us on *[*Twitter*](https://twitter.com/Redis)* with the hashtag #RedisConf2021.*
