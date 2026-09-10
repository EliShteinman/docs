---
title: "5 Things You Didn’t Know You Could Do With Redis"
linkTitle: "5 Things You Didn’t Know You Could Do With Redis"
url: "/blog/5-things-you-didnt-know-you-could-do-with-redis/"
description: "You certainly know Redis as a cache and primary database. It’s earned an excellent reputation among developers worldwide. But Redis also provides a lot of underlying technology to solve lots of..."
date: 2022-09-28
blogCategories:
- "Company"
authors:
- "Alex Patino"
lastmod: 2025-03-27
hidden: true
mirrored: true
---

*By Alex Patino · Published 28 September 2022 · updated 27 March 2025*

![Blog tile image](/images/site-mirror/a98878bd61760a63d5bec9fbf397bf9814af6c6f-772x550.webp)

**You certainly know Redis as a **[**cache**](/solutions/caching/)** and primary database. It’s earned an excellent reputation among developers worldwide. But Redis also provides a lot of underlying technology to solve lots of business problems, and you might not realize how it might help in your own IT shop.**

As with any technology, its value is measured purely on the accomplishments it enables. As you see in the five mini-case studies that follow, Redis lets you achieve more than pure database functions.

Speeding up [financial transactions](/industries/financial-services/)? Making video [game cloud service](/industries/gaming/) insanely fast? Enabling instant online purchases? Let’s start with those and explore a few other examples of what’s possible with Redis.

## Make better decisions based on real-time analytics and inventory management

Like many other brick-and-mortar retail businesses, the pandemic had a huge effect on Ulta Beauty, from swift adoption of [curbside delivery](https://www.economist.com/business/2021/03/06/how-to-get-hybrid-shopping-right/) service (which ballooned six-fold in the final quarter of 2020, industry-wide) and greater dependence on digital sales. A solid e-commerce infrastructure became a non-negotiable requirement. Digital businesses that strengthened, modernized, and scaled their tech stack reaped enormous benefits – [or at least survived](https://www.trade.gov/impact-covid-pandemic-ecommerce).

Ulta Beauty was among the retailers that acted quickly, moving to [Redis Enterprise Cloud](/redis-enterprise-cloud/overview/) for its data and e-commerce strategy and execution. The results? A 40% increase in revenue to the sound of $8.6 billion.

In the end, using Redis for predictive analytics, Ulta Beauty surpassed all quarterly expectations. Doing so lets them identify trends and use benchmarking to help them stay ahead of the curve. Redis also provides Ulta Beauty with [retail inventory management](/industries/retail/) and facilitates modern customer personalizations, experiences, and virtual product testing through [machine learning](/modules/redis-ai/).

“Data was the key to help us make the right decision,” explained Omar Koncobo, Ulta Beauty’s IT director of e-commerce and digital systems. Data helps the company make suitable investments. “With data, we can be sure that we are actually delivering what our customers are looking for. And so now it is such an important piece of everything we do. And we make sure that all of our decisions and everything we do is backed by data.”

Watch the fireside chat with Koncobo and Redis’ Udi Gotlieb as they cover how database innovation fuels the beauty industry.

[Click here to view video](https://www.youtube.com/embed/GqCfkBBppYo)

## Stream data and video at peak performance

The COVID-19 pandemic accelerated the streaming space to unprecedented levels (of which you probably were a part). The growth hasn’t ceased since, with global streaming viewing time up by 14%, according to Conviva’s Q2 2022 [State of Streaming report](https://www.conviva.com/the-state-of-streaming-in-2022-thank-you-page/).

For [TELUS](/customers/telus/), a Canadian telecommunications company, that means maintaining a faultless delivery of constant streaming entertainment to over 1.5 million customers across Western Canada and Quebec through their Optik TV product (think YouTube TV meets Apple TV). The company’s technology strategy team oversees third-party integrations with Optik TV, such as Amazon Prime, Netflix, and other streaming services.

TELUS built [*Showcase*](https://www.showcase.ca/), Optik TV’s all-in-one local and streaming content hub on Redis Open Source. But with a market accelerating at breakneck speed, the demand called for enterprise-level support with real-time performance. “It wasn’t a simple dollars and cents business case,” explained Steve Allen, manager of Showcase’s development team. “It was the operational availability of having enterprise customer support and the fact that Redis Enterprise offered high availability without manual intervention.”

In this [TELUS case study](/customers/telus/), read about TELUS’s journey from Redis Open Source to Redis Enterprise, including how TELUS used Redis Enterprise as a cache to deliver instant content to millions of customers with [Active-Active Geo-Distribution](/active-active/).

## Provide failover services for critical data

[Plivo](/customers/plivo/) is a Communication Platform as a Service (CPaaS) that provides cloud communication services with an integrated messaging platform and a cloud-based carrier network. The company serves over one billion API requests per month in more than 190 countries. Its Voice API platform is used by thousands of businesses across the globe.

Plivo’s engineers built its communications stack on Amazon Elasticache, but they were unsure Elasticache could keep customer operations afloat in the event of a failover. They needed to account for cross-region optimization and fault tolerance. The system needs to kick in so fast that users don’t notice anything changed.

According to Rajat Dwivedi, Plivo’s director of API engineering, “We wanted to ensure we could meet uptime and scalability requirements through Active-Active Redis. We tried to simulate these capabilities with Amazon ElastiCache, but realized this is something we didn’t want to solve ourselves.” The company chose Redis Enterprise Cloud, which delivered this functionality within a fully managed solution that could handle all of Plivo’s Voice API requirements. The [Plivo case study](/customers/plivo/) details how Plivo has sustained volume and scaled its architecture worldwide.

## Get digital payments approved in real-time

The founders of Kipp set out to be the bridge between credit issuers and merchants in the digital payment approval process, helping to deliver a great online shopping experience for any customer.

A credit card transaction that stalls or makes you repeat the payment details is annoying to consumers but a larger issue for businesses: It’s another moment to reconsider the purchase. Nobody wants to nudge anyone to consider a competitor.


Kipp turned to Redis Enterprise Cloud on AWS to save this potentially enormous market from continuing to fall through the cracks in the digital payment process. Because Redis is a widely-approved and used data platform across the financial industry, the IT team didn’t need to learn to validate the system with banks and credit issuers. For more on how Redis helps Kipp deliver a modern e-commerce experience, read [Kipp Eyes E-commerce Opportunity Through Real-Time Payment Approval](/blog/kipp-eyes-e-commerce-opportunity-through-real-time-payment-approval/).

## Speed up database search

Knowledge management firm [Yext](https://www.yext.com/) offers a data and AI Search platform that uses machine learning to ingest, structure, and deliver data in the form of answers, largely for support-related content. For over 15 years, thousands of companies worldwide have trusted Yext to create seamless content-driven experiences at scale across search engines, websites, mobile apps, and hundreds of other digital touchpoints.

With databases such a core part of the Yext platform, findability and discoverability are paramount. To have millions of answers at the ready, Yext uses the hosted version of [RediSearch](/search/), one of our core [modules](/modules/). Because both Yext and Redis are [multicloud](/redis-enterprise-cloud/multicloud/), Redis can serve as a back-end system for Yext anywhere it has a point of presence.

In [Yext & Redis Help Companies Wrangle Public Data Across Multiple Clouds, Third-Party Sites & Owned Experiences](https://accelerationeconomy.com/cloud-wars/yext-redis-help-wrangle-public-data-multiple-clouds-third-party-websites/), you can learn how Redis helps Plivo’s mission to always have the right answer, at any time, anywhere the customer may be.

## Cache, database, and beyond

In this digital-first, real-time data landscape, Redis is helping many businesses to find solutions that go well beyond [caching](/solutions/caching/) and database storage. Industries ranging from [financial services](/industries/financial-services/), [retail](/industries/retail/), [gaming](/industries/gaming/), and [healthcare](/industries/healthcare/) have turned to Redis for speed, scale, and reliability and, in the process, found new ways to cultivate modern customer experiences.
