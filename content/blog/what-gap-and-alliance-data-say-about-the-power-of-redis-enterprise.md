---
title: "What Gap and Alliance Data Say About the Power of Redis Enterprise"
linkTitle: "What Gap and Alliance Data Say About the Power of Redis Enterprise"
url: "/blog/what-gap-and-alliance-data-say-about-the-power-of-redis-enterprise/"
description: "You probably already know Redis as the most launched, most used, and most loved database in the world. What you may not know is that Redis has evolved from a caching and session-storage solution..."
date: 2019-12-12
blogCategories:
- "Company"
authors:
- "Redis  "
lastmod: 2025-03-27
hidden: true
---

*By Redis   · Published 12 December 2019 · updated 27 March 2025*

![Blog tile image](/images/blog/02cc2b544d7836ffab5d6684b0f8d05577c20583-1999x1500.webp)

You probably already know Redis as the [most launched](/press/redis-establishes-new-industry-benchmark-one-billion-downloads-docker/), [most used](https://www.sumologic.com/brief/continuous-intelligence-report/), and [most loved](https://insights.stackoverflow.com/survey/2019) database in the world. What you may not know is that Redis has evolved from a caching and session-storage solution into the primary database for high-performance stateful applications.

At [AWS re:Invent 2019](/blog/redis-labs-at-aws-reinvent-2019/), our friends Junaid Fakhruddin and Bhilhanan Jeyaram from [Gap](https://www.gap.com/) and Brandon Mahoney of [Alliance Data](https://www.alliancedata.com/home/default.aspx) joined Redis Chief Product Officer Alvin Richards on the stage in a breakout session—[Using Redis Beyond Caching](https://www.youtube.com/watch?time_continue=18&v=HoBFic0OONE&feature=emb_logo)—sharing their Redis journeys and how their organizations went from using Redis for simple use cases to powering business-critical applications with it. You can watch the entire session below, but let’s dive deeper into a few of the lessons they learned along the way.

[Click here to view video](https://www.youtube.com/embed/HoBFic0OONE)

## Redis Enterprise powers modern applications

Gap and Alliance Data were looking for a new level of database sophistication in order to successfully implement real-time applications at enterprise scale. Gap needed an [online inventory management platform](/solutions/real-time-inventory/) that could quickly display store inventory and instantly calculate shipping dates as shoppers purchased items. But its existing inventory platform—which was a single monolithic application backed by a relational database—could run its order fulfillment algorithms only asynchronously. Similarly, Alliance Data worried that it wouldn’t be able to update its slow and unreliable legacy content management system quickly enough to keep up with newly released features from nimbler competitors.

Both organizations focused on the value of [performance](/docs/linear-scaling-benchmark-50m-ops-sec/) and [high availability](/redis-enterprise/technology/highly-available-redis/) when building an application meant to serve millions of customers, and the importance of choosing the fastest possible database, not only compared to relational databases, but also to other non-relational (NoSQL) databases.

![](/images/blog/c17b9795adc88f54d614ad22006c58cbd6084c36-1024x506.webp)

Redis Enterprise provides a fast database that helps everyone more efficiently build and operate applications. Redis’ easy-to-learn [data structures](/redis-enterprise/data-structures/) and [modules](/modules/) are flexible enough to cover a variety of use cases—and Redis Enterprise features such as [persistent-memory storage](/redis-enterprise/technology/redis-on-flash/) and [shared-nothing cluster architecture](/redis-enterprise/technology/redis-enterprise-cluster-architecture/) help reduce operational burden.

## Release velocity delivers a competitive edge

But database performance is far from the only place where it’s critical to go fast. Organizations are increasingly turning to microservices and event-driven architectures to increase the speed at which they can respond to customer requests, and the need for real-time response is only boosting the pressure to cut end-to-end latency.

![](/images/blog/acf5ba6a60d6f0cdd364f18f4df6f97a20f15ee4-1024x553.webp)

Redis was a natural fit for caching in Alliance Data’s new microservices architecture, explained Brandon Mahoney, because it provided incredible database speed while remaining stable and predictable. For Gap’s real-time inventory management platform, meanwhile, Redis Enterprise’s [RedisSearch module](/search/) was the key to providing incredibly fast search queries and secondary indexing.

![](/images/blog/175d1f5dbdae60672743ae877f0c14ab2b80c0f0-872x613.webp)

Of course, speed that’s hard to harness isn’t always useful, which is why Redis Enterprise’s ease of use and operational simplicity across multiple [data structures](/redis-enterprise/data-structures/) and [modules](/modules/) is so important. Instead of spending time on repetitive maintenance or other forms of undifferentiated heavy lifting, Redis Enterprise helped the Gap and Alliance Data teams to quickly onboard developers and focus on building application logic and new features that deliver a competitive advantage.

## Database performance drives business outcomes—and happy customers

![](/images/blog/9099b18eff739f64bc91e505b903406cb4622aae-961x653.webp)

Conversations around digital transformation tend to revolve largely around development agility—the move to cloud infrastructure, DevOps practices, continuous integration and continuous deployment (CI/CD), containerization, and open source software components. But it’s easy to forget that all of this work is intended to deliver better software to *people*.

![](/images/blog/e475d5ddf88ff566ed5853609e157ee0e14ac7a1-960x540.webp)

Both Gap and Alliance Data want to deliver faster, more personalized, and more innovative experiences to their customers. Gap, for example, knew that in order to provide its more than 3 million customers with the best possible online shopping experience, it had to optimize fulfillment and shipping of online orders: Using Redis to power inventory searches resulted in a 100x improvement in query response!

Alliance Data, meanwhile, quadrupled throughput and boosted application uptime from 70% to 99%. It was even able to onboard customers its systems could not previously support.

## Growth happens. Grow better with Redis Enterprise

Our theme for AWS re:Invent this year was “growth happens. Put simply, that means Redis Enterprise delivers the super-fast database you love, at the scale you need to cope with ballooning web traffic, increasing customer orders, and heightened demand for “instant” experiences. For Gap, that means building an online inventory management platform to display store inventory and calculate shipping dates in real time. For Alliance Data, it’s all about modernizing its legacy content management system fast enough to stay ahead of its competitors.

To learn more about how *your* organization can leverage Redis Enterprise to successfully implement real-time applications at enterprise scale, visit the Redis Growth Happens page now!
