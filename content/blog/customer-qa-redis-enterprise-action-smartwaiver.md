---
title: "Customer Q&A: Redis Enterprise in Action at Smartwaiver"
linkTitle: "Customer Q&A: Redis Enterprise in Action at Smartwaiver"
url: "/blog/customer-qa-redis-enterprise-action-smartwaiver/"
description: "As one of the most-loved databases by developers, the list of popular applications that rely on Redis today is mind-boggling, and we always appreciate first-person perspectives from our customers..."
date: 2017-04-26
blogCategories:
- "Company"
- "Tech"
authors:
- "Saman Moayeri"
lastmod: 2025-03-04
hidden: true
---

*By Saman Moayeri · Published 26 April 2017 · updated 4 March 2025*

![Blog tile image](/images/site-mirror/a638111c7920ae29e416a9185c4f62e9bacbf04a-436x317.webp)

As one of the most-loved databases by developers, the list of popular applications that rely on Redis today is mind-boggling, and we always appreciate first-person perspectives from our customers who are on the front lines of implementing Redis in their application stack. So, we recently sat down with Ted Knudsen, CTO at [Smartwaiver](https://www.smartwaiver.com/) (and a long time fan of Redis databases). Smartwaiver is an online waiver solution that converts release-of-liability waivers into interactive, digital documents. Thousands of businesses rely on Smartwaiver to streamline their operations and make the waiver signing process secure, simple, fast and as painless as possible. Ted is a pragmatic technologist who’s savvy enough to use the best tools at his disposal and practical enough to pick the ones that make the most business sense. He is also happy to share his ideas on how to use Redis as a primary data store and as a system of engagement for his use case.

Here are some excerpts from our conversation:

**Can you summarize how Smartwaiver uses Redis Enterprise in its stack today?**

**Ted**: At Smartwaiver, we use the Redis database in a variety of different ways throughout our application infrastructure. Thousands of kiosks call home into redis, to see if they have any special commands to run locally (such as autofill information). Redis also fills a variety of other roles for us — from underpinning interactive reporting to maintaining daily statistics and dashboards.

What are your favorite Redis Enterprise database capabilities?

We’ve found that Redis’ data structures (like List, Hash, Sets and Sorted Sets) are great for implementing complex functionality with simplicity. We use Redis to power command and control functionality within our kiosk application, which allows it to accomplish things like autofill, registration and more with lightning fast speeds and with very few resources. There’s really no other database that beats Redis’ pure ease of use.

**Can you elaborate on how Smartwaiver uses Redis Enterprise to power complex analytics?**

We run several internal dashboards out of our Redis database. These use Redis Lists to maintain and display the most recent waivers, and Hashes and Sorted Sets to display more complex graphs that compare “counts per hour” to “top customer counts per hour.” We also leverage Redis to maintain counters on transactions saved to our backend MySQL database, such as “completed waivers” per minute, per hour and to-date (and many more).

**Does Redis also support any caching use cases for your application?**

Yes, we also use Redis Enterprise to cache information about Smartwaiver kiosks and implement webhooks to integrate it with other services.

![](/images/site-mirror/a638111c7920ae29e416a9185c4f62e9bacbf04a-436x317.webp)

In addition, our interactive reporting relies on the Redis cache for rapid load times. It would just be too slow to use data out of MySQL for our millions of waivers across thousands of customers.

**Have you compared Redis with other in-memory databases?**

We tried ElastiCache before but found it really has no viable high availability. Now, we run Redis Enterprise Pack databases within our VPC to maximize performance, availability and minimize our resource costs. Because network bandwidth and sharding vs. not sharding are big considerations for us, Redis Enterprise Pack provides the cost-efficiency and high performance we need within our VPC, making it a perfect choice!

[**Read more testimonials**](/customers/)** from Redis customers.**
