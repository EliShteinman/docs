---
title: "The 6 Books New Redis Developers Should Read"
linkTitle: "The 6 Books New Redis Developers Should Read"
url: "/blog/6-books-new-redis-developers-should-read/"
description: "Just getting started with Redis? These books help you grasp the technical essentials and smooth the learning curve."
date: 2022-09-27
blogCategories:
- "Features"
authors:
- "Redis  "
lastmod: 2026-06-01
hidden: true
mirrored: true
---

*By Redis   · Published 27 September 2022 · updated 1 June 2026*

![Blog tile image](/images/site-mirror/ab705c72e2c437f970c3c92ffbacddcd0d5ebe40-772x550.webp)

**Just getting started with Redis? These books help you grasp the technical essentials and smooth the learning curve.**

Adopting any new-to-you technology can be daunting. There’s *a lot* to learn, from philosophical underpinnings to pragmatic how-to.

That’s true for [Redis newbies](/try-free/) too. So we asked Redis experts – inside the company and in the larger community – for the technology references they recommend for today’s developers. This curated book list can help you conquer the Redis learning curve and come up to speed swiftly.

## Seven Databases in Seven Weeks: A Guide to Modern Databases and the NoSQL Movement

Redis developer advocate Brian Sam Bodden recommends [*Seven Databases in Seven Weeks*](https://www.oreilly.com/library/view/seven-databases-in/9781680505962/), by Luc Perkins, as a starting point for beginners “to get a taste of the different data models and querying approaches.”

The book is also a top choice for Raja Rao, Redis’s vice president of growth marketing. “This book provides developers with an understanding of the modern database landscape by giving a good analysis of several databases and how they work.” And, he adds, you get an overview of the [NoSQL](/nosql/what-is-nosql/) community without leading you into a web of complexity.

![](/images/site-mirror/871b257e4d66ac9ce0de02997584fb8db6d32c87-853x1024.webp)

You need to integrate NoSQL databases into your architecture to store, process, and retrieve data efficiently. *Seven Databases in Seven Weeks* offers a thorough dissection of the NoSQL database ecosystem. Perkins presents conceptual introductions to seven databases – one of them being Redis – including how to deploy each one, when to use it, when not to use it, its benefits, its downsides, and how it relates to a real-life project.

It’s an extensive investigation that highlights the most important characteristics of each database without diving too deep into the technicalities. The book demystifies NoSQL and gives readers more confidence to navigate through the NoSQL space.

## Designing Data-Intensive Applications

Rao also recommends this book for programmers who want to design large, heavy systems. “It teaches you how to analyze situations and pick out the right solution,” he explains.

In [*Designing Data-Intensive Applications: The Big Ideas Behind Reliable, Scalable, and Maintainable Systems*](https://dataintensive.net/)*,* author Martin Kleppmann adds historical background to highlight how technical problems used to be solved, going back to the 1800s. That gives a problem-solving context, including the process of evaluating the pros and cons of different technologies.

For example, Kleppmann introduces MapReduce, then relates it to the technology that was created years before.

![](/images/site-mirror/cdad5b4465f121b78e0ca5098702458d250339f9-780x1024.webp)

Doing so reveals how we’ve progressed from batch-processing systems to technologies like MapReduce through to stream-based processing.

Perhaps the overarching benefit of *Designing Data-Intensive Applications* is that it teaches readers how to compare technologies and to become more analytical and efficient problem solvers.

## NoSQL Distilled

To wrap your head around SQL, Bodden recommends starting with[*NoSQL Distilled: A Brief Guide to the Emerging World of Polyglot Persistence*](https://martinfowler.com/books/nosql.html) by Pramod Sadalage and Martin Fowler. “It’s another great foundational book on data, data models, and how they’ve evolved with the advent of commodity hardware and horizontal scaling offerings,” he explains. Although the book is about ten years old, it gives developers a foundational awareness of NoSQL databases, accompanied by plenty of examples.

The authors adopt a conceptual approach and shun the coding aspect, going straight to the heart of [what NoSQL is about](/nosql/what-is-nosql/) and how NoSQL databases differ from relational databases.

![](/images/site-mirror/b99f73033c5ec55196482e2e20878b33c343b9dc-500x653.webp)

As [Fowler](https://twitter.com/martinfowler) wrote on his own website, the authors aimed to provide a background on how NoSQL databases work so that you can make those judgments yourself without having to trawl the whole web. “We’ve deliberately made this a small book (just 152 pages), so you can get this overview pretty quickly,” he wrote.

## Redis in Action

The books listed above introduce Redis newbies to underlying database concepts. At some point, you want to know more about Redis specifically.

Rao recommends [*Redis in Action*](https://www.manning.com/books/redis-in-action), by Josiah CarlsonHere, Carlson introduces the key value model and contextualizes its functionality with real-life use cases such as [caching](/solutions/caching/), distributed and targeting, and more.

Although the book is old, in tech terms – it’s from 2013 and has no mention of features released since then – Rao says this book helps new developers understand the basics of Redis through real-world examples.

![](/images/site-mirror/459c5d3ee45aac010ff6af6c5d31876045f382cb-817x1024.webp)

Carlson introduces the foundational topics, shedding light on important areas such as how to minimize the chances of data loss. Then it dives into common challenges, including how to model non-trivial data, deal with index data, and search, sort, and filter data. Scaling is covered in some depth, including techniques to help you scale read queries, write queries, total memory available, and suggestions for scaling complicated queries.

It’s a starting point – which is just what newbies need. You get a holistic understanding of Redis to help you navigate concepts and features, and you can build on that knowledge.

## Caching at Scale With Redis

Recommended by Henry Tam, Redis’s principal solutions marketing manager, you can view [*Caching at Scale*](https://www.leeatchison.com/book/caching-at-scale-with-redis) [*with Redis*](https://www.leeatchison.com/book/caching-at-scale-with-redis) by Lee Atchison as the [caching](/solutions/caching/) blueprint for Redis. “The book provides a really broad overview of caching the different patterns, and why Redis is the ideal fit for enterprises that need a caching solution,” Tam says.

![Caching at Scale With Redis book](/images/site-mirror/2bd824920e71d88c8af02ea4e61ddfc7898fda13-966x990.webp)

Atchison provides readers with a comprehensive insight into what caching is, why and when it’s needed, and how to maximize application performance through specific caching techniques.

## Redis Microservices for Dummies

The Wiley Dummies guides earned a reputation for no-nonsense instructions that are easy to understand and simple to follow, a template that began with [the surprise hit of ](https://slate.com/culture/2016/04/the-history-and-delights-of-the-for-dummies-how-to-books.html)[*DOS for Dummies*](https://slate.com/culture/2016/04/the-history-and-delights-of-the-for-dummies-how-to-books.html) in 1991.

The short [Redis Microservices for Dummies](/docs/redis-microservices-for-dummies/) book – which incidentally is free – teaches new Redis programmers how to develop and operate high-performance [microservices](/solutions/microservices/) with Redis architecture in the easiest possible way.

![Redis Microservices for Dummies](/images/site-mirror/761e6375b0d6edeb6540f27005995fc130426f9c-1024x842.webp)

Talon Miller, Redis Technical Product Manager, says, “Redis was somewhat of a complicated database for me to grasp, specifically because of all the variety of data structures. *Redis for Dummies* simply explained all of the core basics that I needed to know about Redis to get started using it.”

The book unravels microservice functionality, introduces the key Redis microservices terms and concepts, and shows how everything can be synchronized to optimize application performance.

## A final page

These books can help anyone new to Redis get to grips with important concepts in the Redis sphere and propel you forward to a new level of understanding.
