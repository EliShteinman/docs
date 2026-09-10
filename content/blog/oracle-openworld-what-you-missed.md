---
title: "6 Things You Missed If You Didn’t Visit Redis Labs at Oracle OpenWorld"
linkTitle: "6 Things You Missed If You Didn’t Visit Redis Labs at Oracle OpenWorld"
url: "/blog/oracle-openworld-what-you-missed/"
description: "As you are probably aware, tens of thousands of database professionals and other tech leaders and practitioners converged on San Francisco last week for Oracle OpenWorld. And you may have heard..."
date: 2019-09-26
blogCategories:
- "Company"
authors:
- "Fredric Paul"
lastmod: 2025-03-27
hidden: true
mirrored: true
---

*By Fredric Paul, Director of Content · Published 26 September 2019 · updated 27 March 2025*

![Blog tile image](/images/site-mirror/0073e867b4e64f59de9047fdcde04295ba647e5c-772x550.webp)

As you are probably aware, tens of thousands of database professionals and other tech leaders and practitioners converged on San Francisco last week for [Oracle OpenWorld](https://www.oracle.com/openworld/). And you may have heard some of the news coming out of the event, ranging from another batch of [controversial statements from Oracle chief Larry Ellison](https://www.crn.com/slide-shows/cloud/larry-ellison-s-15-boldest-statements-at-oracle-openworld) to the annual [raft of new announcements](https://www.forbes.com/sites/oracle/2019/09/17/larry-ellison-details-4-database-innovations-including-a-new-free-version/#1ef0a44054ef), this time centering around [Exadata](https://www.networkworld.com/article/3439538/oracle-updates-exadata-big-iron-and-its-cloud-commitment.html), [AutoML and data security](https://www.informationweek.com/cloud/oracle-touts-autonomous-cloud-for-data-security), cloud infrastructure, and even a [new mission statement](https://www.businessinsider.com/oracle-larry-ellison-mission-statement-bright-red-brand-2019-9#for-many-years-oracle-has-been-closely-associated-with-a-particularly-bright-shade-of-red-1)!

But unless you were there, you might have missed a golden opportunity to learn more about Redis and Redis Enterprise. Let’s take a quick look at what went down in and around the Redis booth at Oracle OpenWorld:

## 1. Kyle Davis explains “Everything You Need to Know About Redis”

In an exclusive sit-down with TFIR at Oracle Open World, Kyle Davis, Head of Developer Advocacy at Redis, covers all the basics about Redis and Redis Enterprise in just 10 minutes! It’s a great way to get up to speed on what we’re up to, and fortunately, you can watch the video even if you weren’t at the show:

[Click here to view video](https://www.youtube.com/embed/t_Dlg3S8skE)

## 2. Dave Nielsen on “Why MySQL Needs Redis”

MySQL has definitely earned its popularity, Redis’ Head of Ecosystem Programs Dave Nielsen told a standing-room-only crowd, but as a fast and lightweight in-memory database, Redis specializes in things that MySQL doesn’t always do well, making them perfect complements to each other. In particular, users of MySQL databases may face challenges in areas such as:

- Minimizing the cost of data management while scaling your application
- Speeding time-to-market
- Keeping applications responsive for users
- Overcoming the physical limits of database capacity

Fortunately, he said, there are several ways adding Redis can help, including:

- Using Redis as a cache when you have frequent reads and infrequent writes, especially when data is shared among multiple users
- Using Redis as a user session store for session-based apps
- Using Redis for metering to limit the peak load on your legacy database by limiting the number of queries per second
- Using [Redis for fast data ingest](/solutions/fast-data-ingest/) for real-time analytics, the Internet of Things, log collection, and time-series applications

## 3. Madhukar Kumar shared “5 Things You Didn’t Know Redis Could Do”

![](/images/site-mirror/5981f42b1a08ba765f023bcf28c7076566ad0d80-300x149.webp)

Redis is known for its performance, simplicity, and extensibility, but [Madhukar Kumar](/author/mkumar/), Redis’ Vice President of Technical and Product Marketing, explained that Redis supports a surprising variety of high-performance operational, analytics, and hybrid use cases. He specifically called out using:

1. **Redis for rate limiting,** so your APIs don’t get overloaded.
1. **Redis for super-fast search** at the speed of silicon, not spinning discs, with no-lag (re)indexing, and intuitive search syntax.
1. **Redis for finding unique views with HyperLogLog, **such as how many unique logins has your website registered.
1. **Redis for message brokering **with Redis Streams and Pub/Sub so that you can build an event based architecture for your microservices.
1. **Redis to store, retrieve, and manipulate JSON** to deal with large JSON objects that need only small changes or to work with only portions of complex JSON objects.

## 4. Mikhail Volkov on linear scalability to 200M ops/sec @ <1msec latency

![](/images/site-mirror/9e26322e0c1d0b140972a63c357f05a376a5d297-300x161.webp)

Earlier this year, [Redis Enterprise delivered more than 200 million ops/sec](/blog/redis-enterprise-extends-linear-scalability-200m-ops-sec/), with less than 1 millisecond latency, on as few as 40 AWS instances. This represented a 2.6X scalability improvement in less than 15 months. And at Oracle OpenWorld, Enterprise Customer Success Team Lead [Mikhail Volkov](https://www.linkedin.com/in/mikhailvolkov) showed attendees just how we keep breaking our own speed records by maintaining close to optimal scalability (94%).

## 5. Kyle Davis on “Serving AI Deep Learning Modules in Real Time”

![](/images/site-mirror/ead6bb791e2a25812a468ff69c523a45a97f931d-300x187.webp)

Kyle talked about “how the AI sausage is made” and reminded attendees that “production is hard,” especially when it comes to serving complex artificial intelligence models. “When running AI across many services, there are lots of places for potential failure and you run the risk of losing important data. To ensure that AI predictions are properly recorded, the prediction needs to be on the same instance as the storage … Enter RedisAI!” RedisAI implements an AI serving layer as a module in Redis that’s no more complicated than a simple caching operation in Redis. You don’t have to know anything about AI, you just need to know these four commands: AI.MODELSET, AI.TENSORSET, AI.MODELRUN, and AI.TENSORGET. And RedisAI has another superpower: the ability to swap models at will to enable A/B testing, user-level configuration, interval model replacement, and optimizing models for peak periods.

## 6. Awesome swag

![](/images/site-mirror/fc07e16795006d5f1e5d5dd8a5fd4e02bcc34aeb-233x300.webp)

It wouldn’t be a trade show without t-shirts, but few pieces of swag are as cool as the jet-black GOT Redis? t-shirt our booth staff was handing out to folks who attended our informative lightning talks. But that’s not all. We also had stickers to adorn your laptop and chances fun door prizes ranging from drones to smart speakers to Star Wars LEGO kits! The only catch? You had to be present to win!

Of course, these highlights represent only a small fraction of the many lightning talks, product demos, one-on-one conversations with Redis experts, and other Redis activities at the event.

But don’t worry too much if you didn’t make it to Oracle OpenWorld this year. There are plenty of upcoming opportunities to connect with the Redis team at events around the world, from Chief Data Officer Day in Madrid, Spain, this Thursday, September 26 to [AWS re:Invent in Las Vegas,](/aws-reinvent/) December 2 – 6, and many more.

*(To stay up to date on Redis events and find the best ones to attend, subscribe to our events page now!)*
