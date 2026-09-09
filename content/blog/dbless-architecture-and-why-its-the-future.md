---
title: "What Databaseless (DBLess) Architecture Is—and Why It’s the Future"
linkTitle: "What Databaseless (DBLess) Architecture Is—and Why It’s the Future"
url: "/blog/dbless-architecture-and-why-its-the-future/"
description: "You may be wondering: Why is a database company like Redis talking about Databaseless (DBLess) architecture? And what is it? That’s natural, but before we get into the details, let’s look at the..."
date: 2021-07-08
blogCategories:
- "Company"
authors:
- "Raja Rao"
lastmod: 2025-03-27
hidden: true
---

*By Raja Rao, Head of Growth Marketing · Published 8 July 2021 · updated 27 March 2025*

![Blog tile image](/images/site-mirror/89835eab457fb43a2cd53773fbbcb6428a60743e-772x520.webp)

You may be wondering: Why is a database company like Redis talking about Databaseless (DBLess) architecture? And what is it? That’s natural, but before we get into the details, let’s look at the new way of thinking behind this brand new architecture.

To do that, I want to take a quick detour and talk about something called the [First Principles](https://fs.blog/2018/04/first-principles/) thinking. It forces you to [think for yourself ](https://jamesclear.com/first-principles)and not just follow the tradition, but to question everything.

The gist of First Principles is that unless you’re looking at a law of nature, such as the laws of gravity, every system or concept is man-made and can have inefficiencies. To add to that, the passage of time or technological innovation could have proven the concept obsolete. This means you should regularly question the traditional system or concepts and see if you can build something better.

To find those inefficiencies, you must take a systematic and scientific approach that breaks them into smaller pieces to get to the fundamental truths. Then, see if the passage of time or invention of new technology has made any of these pieces obsolete. If so, it appears you have a chance to build a newer and better system.

Fundamentally, whether people know it or not, the majority of the social, technical, and economic changes have happened because of people thinking with First Principles and challenging the tradition.

![](/images/site-mirror/aa61c4ab4d6bad665a323362d7b36336f48a108e-1024x558.webp)

*Source: See the reference links at the bottom*

In the above video, Elon Musk explains how he looked into the raw materials of a battery and was able to reduce the cost of it from $700 to $70.

Let’s take another example of the first principle of thinking because it’s easier to explain: Gasoline cars vs. Electric cars.

## Gasoline cars vs. Electric cars

We all know that you can use an electric battery to run a car.

But while a gasoline car, does have a battery, it’s not used for running the car. It uses batteries for starting the engine, A/C, audio systems, lights, sensors, locks, and so on, but not for running the car. Instead, it relies on an internal combustion engine (ICE) to run the car.

It turns out, ICE cars are highly inefficient. Only [16% to 25%](https://insideevs.com/features/392202/ice-vs-ev-inefficient-combustion-engine/) of the power that’s generated actually makes it into the wheels. On the other hand, electric vehicles provide about [90% power ](https://insideevs.com/features/392202/ice-vs-ev-inefficient-combustion-engine/)to the wheels! EVs also have major advantages when it comes to the environment, repair costs, and so on.

If you are looking at this from a First Principles perspective, even though most cars that are built even today are gasoline cars, the fundamental truth is that they use an inefficient system.

Now if you look at an electric car, it removes this inefficiency to build a new type of car. In this case, it simply gets rid of the complex and highly inefficient engine and replaces it with a large battery and a motor to directly spin the wheels.

![](/images/site-mirror/a22038cef528e75482674e5fa0e1918a5755eb91-1024x848.webp)

So you can see how First Principles thinking leads to identifying inefficiencies and creating a newer, better system.

Now looking at these ideas, if you were to start a new car company, would you build gasoline cars or electric cars?

Let’s shift gears and transition to the database world to see if we can apply the same First Principles thinking to that sector.

## Traditional architecture vs. DBLess architecture

Let’s first look at traditional architecture.

![](/images/site-mirror/b5eff7dd4e976e0f07deb477fefecdb9018aebc1-1024x441.webp)

In traditional architecture, you have a primary database (Postgres, MongoDB, etc.) and a secondary database or cache (e.g. Redis or Memcached). The primary DB is used to store all the data and support CRUD operations. The caching DB is used for caching, session storage, rate-limiting, IP-whitelisting, Pub/Sub, queuing, and many other things.

If you think about it, even when there’s a cache-hit, we’re also using the secondary DB for part of the CRUD operations. And yet we’re still not fully utilizing it as a primary database.

Does this remind you of the issue with gasoline cars? Just like they carry a battery to power numerous things except moving the car, the traditional architectures use things like Redis for everything except as the main DB.

Do you see the similarities?

What if we use the First Principles thinking to do what the electric car did? Similar to how EVs got rid of the engine, what if we get rid of the slow and inefficient primary database and simply use the cache DB as the main database?

Say hello to Databaseless (DBLess) architecture.

## The Databaseless (DBLess) architecture:

In this architecture, you get rid of the primary DB, hence the name DBLess. Instead, you use the formerly secondary/cache DB as the new primary database.

Let’s imagine that we started using Redis or other similar caching databases as a primary database and got rid of the primary DB (such as Postgres, Mysql, MongoDB, etc) completely.

![](/images/site-mirror/21d85ede7fe9b8740f9d279d25ed216bf50ca457-1024x471.webp)

**Important Note:** This is just an architectural discussion. The DBLess architecture is not a proprietary architecture that’s limited to Redis or Redis Enterprise, and it would work with any Redis-like system. Also, remember that Redis is an OSS project, so you can build this yourself or on any other Redis-hosted cloud provider.

### Is anyone using this architecture?

Yes, definitely. As you can imagine, we work with thousands of customers on a daily basis. And although Redis is still primarily used as a secondary database, we have started to see this new DBLess architecture emerge over the last couple of years. It started to get more momentum as Redis itself became more feature-rich, powerful, and as more people found success. Many who aren’t even our customers, like Request Metrics, [have built their entire startup on this architecture](https://www.youtube.com/watch?v=BHR_mvafOEc) and find it incredibly successful.

[Watch the video](https://www.youtube.com/watch?v=BHR_mvafOEc)

Now that you know it’s real, let’s see what makes this possible.

### Technically speaking, how does this compare to a traditional primary DB?

Let’s use Redis Enterprise as an example and compare it with the traditional primary DBs.

![](/images/site-mirror/fc0e5d955ce0281d50c2cf24df2b408163b5288f-631x503.webp)

As you can see, the short answer is that it fairs really well and, in fact, can even be better than some traditional Primary DBs.

**As a reminder,** you can use this architecture by simply using Redis OSS or other Redis competitors. You just need to come up with a similar comparison table to see how well it works.

### But, can Redis really do this? I thought it was just a cache?

You are correct. It started off as a cache store about a decade ago and is still great for that purpose.

However, Redis and Redis Enterprise have expanded significantly over the years by incorporating virtually all the features of traditional DBs—and by having a [module ecosystem](/modules/get-started/) that runs natively with core Redis.

Take [RedisJSON](/json/) ([10x faster](https://oss.redis.com/redisjson/performance/) than the market leader). You can use it and essentially have a real-time document-like database, or use the [RediSearch module](/search/) ([4x to 100x faster](/blog/search-benchmarking-redisearch-vs-elasticsearch/)) and implement real-time full-text searches like Elastic Search or Algolia.

And you can use any of these modules as part of Redis OSS and host it yourself.

### Is this really the future?

We strongly believe this architecture is the future in the same sense that electric cars are the future. And even though electric cars make up less than 1% of all cars, they are the future. We think that this is just a natural evolution of technology. Seeing the success of many of our customers, we think that the more people learn about it, the more people will try and adopt this.

### What’s in the name?

It’s called DBLess because we are getting rid of the primary DB and we think it’s a fun and quirky name along the lines of “[stateless](https://en.wikipedia.org/wiki/Service_statelessness_principle),” “[serverless](https://en.wikipedia.org/wiki/Serverless_computing),” “[NoSQL](https://en.wikipedia.org/wiki/NoSQL),” and “[No Software](https://www.forbes.com/sites/adrianbridgwater/2015/05/21/salesforce-no-software-we-mean-no-legacy-software/?sh=2af55d2826ec).”

### How to get started?

If you are one of the hundreds of thousands of Redis users, you’re in luck—you can do a quick proof-of-concept today! We aren’t asking you to add something new, but instead get rid of something that’s inefficient.

And here’s how to do it.

If you are building a new system or a new feature, then it’s straightforward just start using this architecture—or at least do a Proof-of-Concept and see if it works for you.

If you already have a primary DB, then do what many of our customers do and use a hybrid approach. They continue to use the traditional architecture, but migrate parts of the product into the newer architecture, such as places where they’re already relying heavily on Redis or newer features. And slowly but surely, they migrate all the features until they’re completely migrated over.

## Summary: Be a First Principles thinker

We’re asking you to be a First Principles thinker. Just because something is traditionally used, it doesn’t mean it’s perfect and that you should blindly follow it. We’re asking you to question traditional thinking, critically examine it, and try alternatives. And when you do, you may just invent something useful for yourself and others.

DBLess architecture provides an alternative to traditional thinking. Instead of wondering if it’ll work or not, try a Proof-of-Concept. It might just surprise you!

## References

1. [Elon Musk on First Principles](https://www.youtube.com/watch?v=bLv9MGsUt6g)
