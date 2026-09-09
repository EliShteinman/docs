---
title: "Intro to Caching from the Caching at Scale Primer"
linkTitle: "Intro to Caching from the Caching at Scale Primer"
url: "/blog/intro-to-caching-at-scale-primer/"
description: "With over 34 years of experience architecting and building SaaS applications, Lee Atchison is a recognized thought leader and expert on application modernization, cloud migration, and DevOps..."
date: 2021-07-22
blogCategories:
- "Company"
authors:
- "Redis  "
lastmod: 2025-10-01
hidden: true
---

*By Redis   · Published 22 July 2021 · updated 1 October 2025*

![Blog tile image](/images/site-mirror/54ba91ad5fa926d984bbc9b39e770c0792692531-772x520.webp)

*With over 34 years of experience architecting and building SaaS applications, *[*Lee Atchison*](https://www.linkedin.com/in/leeatchison/)* is a recognized thought leader and expert on application modernization, cloud migration, and DevOps transformations. You can read or watch his expertise on display through any of his three books, 70+ published articles, or 100s of presentations, classes, and seminars.*

You and your team have developed an application worthy of people’s attention. Word of mouth spreads and it’s popularity soars, but then operation costs begin to skyrocket, the app continuously crashes, and a customer does the unthinkable—they tweet about super slow speeds.

As your customer base grows, how do you keep costs from rising? You welcome the challenge of scaling, but you also can’t sacrifice growth for higher failover rates and increased maintenance costs.

One thing is for certain: You need an application cache.

## What is a cache?

> “A cache is a data-storage component that can be accessed faster or more efficiently than the original source of data.”

Lee Atchison, Caching at Scale With Redis.

When there’s a request to fetch data, a cache provides a copy of that data in real-time. And as more and more customers begin using your app, you need an advanced application architecture that can handle those increased data requests without going back-and-forth between your primary data store.

Lee sums it up pretty simply: “Our modern world demands modern applications.”

It’s no secret that customers demand better and better performance. If your application isn’t performing up to customer expectations, those customers will leave and flock to your competitors.

And behind every fast, easy-to-use application is a ton of moving parts. As Lee says, “Today’s applications must be able to handle large quantities of data, perform complex operations, maintain numerous relationships among data elements, and operate on distinct and disparate states between transactions.”

Headaches happen within complex applications, and a cache is there to minimize them.

## Read Caching at Scale With Redis

In [*Caching at Scale With Redis*](/docs/caching-at-scale-with-redis/)*,* Lee introduces what caching is, why and when you need it, and caching practices that will help your application achieve the highest performance possible.

![](/images/site-mirror/0b43f3ad608f87d4fbcc4dad8235ea79f4e23114-1024x491.webp)

*A simple cache (p. 4)*

When a user requests data from a service, an operation is performed to acquire that data from a store, then relay that information back to the consumer. Yet, Lee notes that these operations can be very resource and time intensive—especially if the same data is being retrieved over and over again.

> “Instead, with a cache, the first time the complex operation is performed, the result is returned to the consumer, and a copy of the result is stored in the cache. The next time the data is needed, rather than performing the complex operation all over again, the result can be pulled directly out of the cache and returned to the consumer faster and using fewer resources.”

### What caching fixes—but why it’s not perfect

Caching isn’t a one-size-fits-all data store. Application architectures vary across the board, especially due to size of the app or even the industry use case. However, Lee says there are four primary features that caching will help improve:

- Performance
- Scaling
- Resource optimization
- Convenience and availability

This doesn’t mean implementing a cache will automatically provide these for you.

“In many cases, caching may not add value, and in a few cases, caching can actually degrade performance,” Lee says. He raises three potential problems:

1. Caching can cause the application to not execute desired side effects of targeted operations
1. Inconsistent data in a cache
1. Poor cache performance

Lee notes that certain variables must be true in order for a cache to be useful (see page 8 of the e-book for the list of rules). “For a cache to be effective, you need a really good understanding of the statistical distribution of data access from your application or data source,” Lee says.

## Prime yourself with the ultimate caching playbook

Now that you know you need a cache, this free e-book is the only primer you need to build and scale your cache with Redis.

From Lee himself: “This book describes what caching is, why it is a cornerstone of effective large-scale modern applications, and how [Redis](/try-free/) can help you meet these demanding caching needs.”

As you dive deeper into the e-book, *Caching at Scale With Redis* discusses the different types of caching strategies and offers practical explanations on how these strategies may fit for you—especially if you’re in the cloud.

“While there are many methods, processes, and techniques for making an application retain high availability at scale, caching is a central technique in almost all of them,” Lee says.

*For more information on the e-book, visit our *[*page*](/docs/caching-at-scale-with-redis/)*.*
