---
title: "Redis Wins At the Polls!"
linkTitle: "Redis Wins At the Polls!"
url: "/blog/redis-wins-at-the-polls/"
description: "Last week, users of NoSQL databases worldwide crowned Redis champion in G2 Crowd’s Grid. The Grid℠ represents the democratic voice of real software users, rather than the subjective opinion of one..."
date: 2015-09-15
blogCategories:
- "Company"
authors:
- "Leena Joshi"
lastmod: 2025-03-04
hidden: true
mirrored: true
---

*By Leena Joshi, VP Product Marketing · Published 15 September 2015 · updated 4 March 2025*

![Blog tile image](/images/site-mirror/b1a22a1d1122e16d92cb59663a979e35112687e6-140x92.webp)

![](/images/site-mirror/2bb8aeb4d106583ed97e32edea9106d1be46d7bb-635x200.webp)

Last week, users of NoSQL databases worldwide crowned [Redis champion in G2 Crowd’s Grid](https://www.g2crowd.com/products/redis/reviews). The Grid℠ represents the democratic voice of real software users, rather than the subjective opinion of one analyst. G2 Crowd rates NoSQL databases algorithmically based on data sourced from product reviews shared by G2 Crowd users and data aggregated from online sources and social networks.

It was no surprise to us – Redis won hands down as the top scoring software in the NoSQL database category and # 4 overall among all databases.

Top 5 things that should come as no surprise to any Redis users:

- 100% of reviewers gave Redis 4 or 5 stars on user satisfaction
- 79% of reviewers think Redis is headed in the right direction – higher than all other software surveyed in this category.
- Average number of months to go live with Redis was 0.8 (3 weeks!) while everyone else needed months
- Feature-wise, Redis was rated higher than its peers on 5 out of 7 categories, including data manipulation, storage, availability, stability and security
- 92% of Redis users were likely to recommend Redis, higher than all its peers.

**Why does this matter?**

While RDBMS-es are well understood as a category, NoSQL technologies are still being digested by application developers, devops and operations. To make it even more confusing, vendors are adding multiple models to their databases, leaving customers confused about when to use which database technology.

![](/images/site-mirror/2fab6faf06ed388458906c837d77d9b5b3cdb306-635x398.webp)

Redis makes it simple. Blazingly fast, highly stable and persistent, it is the #1 choice of users for a variety of different applications and use cases. The unique data structures in Redis, 180 or so commands, Lua scripting language all endow it with a versatility and performance that can’t be beaten. Whether you need high speed analytic processing (example: leaderboards in gaming), in-app social functionality (example: who’s following who and who you also follow), online session management (example: what’s a user doing, clicking, purchasing etc), pub-sub functionality (example: inventory notification to thousands of web clients), geo-spatial lookups (example: who’s close by), unique user counts (example: ranking articles by unique page views), high speed transactions (example: price/currency notifications) – Redis not only delivers it, but delivers it with fewer lines of code, lower latencies and higher throughput than anyone else.

To quote the most read user review on G2 crowd:

*“I use Redis for a series of things, specifically a chat system and leaderboards for tracking site activity. I have also used Redis a ton in front of MySQL to serve as a more direct index in scenarios where queries are underperforming and the tables are so larger (50m+ rows) that trying to reindex means a chunk of downtime. I also use Redis for user sessions. I am also starting to migrate away from Memcached for basic key/value stores in front of MySQL.”*

The robust data structures that Redis offers are by far my favorite feature. It allows you to create hash tables to simulate more Mongo-like features as well as lists and sorted sets that can be used for queues, chat systems and leaderboards (basically anything you want sorted). Also, the option to flush to disk and have persistence is pretty awesome.

A recent benchmark outlines how much of a no-contest it is when you compare Redis’ performance to other technologies – get it[ here](/cbc-2015-15-nosql-benchmark)!
