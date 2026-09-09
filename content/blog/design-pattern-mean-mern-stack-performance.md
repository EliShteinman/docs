---
title: "Speed Up MEAN and MERN Stack Applications With This Effective Design Pattern "
linkTitle: "Speed Up MEAN and MERN Stack Applications With This Effective Design Pattern "
url: "/blog/design-pattern-mean-mern-stack-performance/"
description: "If you don’t design and build software with attention to performance, your applications can encounter significant bottlenecks when they go into production."
date: 2022-12-21
blogCategories:
- "Tech"
authors:
- "Prasan Rajpurohit"
lastmod: 2026-01-15
hidden: true
---

*By Prasan Rajpurohit, Technical Solutions Developer at Redis · Published 21 December 2022 · updated 15 January 2026*

**If you don’t design and build software with attention to performance, your applications can encounter significant bottlenecks when they go into production**.

Over time, the development community has learned common techniques that work as reliable **design patterns** to solve well-understood problems, including application performance.

So what are design patterns? They are recommended practices to solve recurring design problems in software systems. A design pattern has four parts: a name, a problem description (a particular set of conditions to which the pattern applies), a solution (the best general strategy for resolving the problem), and a set of consequences.

Two development stacks that have become popular ways to build [Node.js applications](/blog/redis-om-node-js/) are the **MEAN stack** and the **MERN stack.** The MEAN stack is made up of the MongoDB database, the Express and Angular.js frameworks, and Node.js. It is a pure JavaScript stack that helps developers create every part of a website or application. In contrast, the MERN stack is made up of MongoDB, the Express and ReactJS frameworks, and Node.js.

Both stacks work well, which accounts for their popularity. But it doesn’t mean the software generated runs as fast as it can—or as fast as it needs to.

In this post, we share one popular design pattern that developers use with Redis to improve application performance with MEAN and MERN stack applications: the **master data-lookup pattern**​. We explain the pattern in detail and accompany it with an overview, typical use cases, and a code example. Our intent is to help you understand when and how to use this particular pattern in your own [software development](https://launchpad.redis.com/).

## Building a movie application

For the purposes of this post, our demonstration application showcases a movie application that uses basic create, read, update, and delete (CRUD) operations.

![Movie application demo](/images/site-mirror/4c3e6d98c0e680f2d24b843c68b122ee263ed58c-624x322.webp)

The movie application dashboard contains a search section at the top and a list of movie cards in the middle. The floating plus icon displays a pop-up when the user selects it, permitting the user to enter new movie details. The search section has a text search bar and a toggle link between text search and basic (that is, form-based) search. Each movie card has edit and delete icons, which are displayed when a mouse hovers over the card.

This tutorial uses a GitHub sample demo that was built using the following tools:

- **Frontend:** ReactJS (18.2.0)
- **Backend: **Node.js (16.17.0)
- **Database: **MongoDB
- **Cache and database:** Redis stack (using Docker)

You can follow along with the details using [the code on GitHub](https://github.com/redis-developer/ebook-speed-mern-frontend.git).

## The master data-lookup pattern​

One ongoing developer challenge is to (swiftly) create, read, update, and (possibly) delete data that lives long, changes infrequently, and is regularly referenced by other data, directly or indirectly. That’s a working definition of master data, especially when it also represents the organization’s core data that is considered essential for its operations.

Master data generally changes infrequently. Country lists, genres, and movie languages usually stay the same. That presents an opportunity to speed things up. You can address access and manipulation operations so that [data consistency](/blog/database-consistency/) is preserved and data access happens quickly.

From a developer’s point of view, master data lookup refers to the process by which master data is accessed in business transactions, in application setup, and any other way that software retrieves the information. Examples of master data lookup include fetching data for user interface (UI) elements (such as drop-down dialogs, select values, multi-language labels), fetching constants, user access control, theme, and other product configuration. And you can do that even when you rely primarily on MongoDB as a [persistent data](/redis-enterprise/technology/durable-redis/) store.

![redis, mongodb, and application diagram](/images/site-mirror/d22b0d4041d39f0b0ad89bcc85fc2303fdc8d800-1163x285.webp)

*To serve master data from Redis, preload the data from MongoDB.*

1. Read the master data from MongoDB on application startup and store a copy of the data in Redis. This pre-caches the data for fast retrieval. Use a script or a cron job to repeatedly copy master data to Redis.
1. The application requests master data.
1. Instead of MongoDB serving the data, the master data will be served from Redis.

## Use cases

Consider this pattern when you need to

- **Serve master data at speed: **By definition, nearly every application requires access to master data. Pre-caching master data with Redis delivers it to users at high speed.
- **Support massive master tables: **Master tables often have millions of records. Searching through them can cause performance bottlenecks. Use Redis to perform [real-time search ](/search/)on the master data to increase performance with sub-millisecond response.
- **Postpone expensive hardware and software investments: **Defer costly infrastructure enhancements by using Redis. Get the performance and scaling benefits without asking the CFO to write a check.

## Demo

The image below illustrates a standard way to showcase a UI that is suitable for master data lookups. The developer responsible for this application would treat certain fields as master data, including movie language, country, genre, and ratings, because they are required for common application transactions.

Consider the pop-up dialog that appears when a user who wants to add a new movie clicks the movie application plus the icon. The pop-up includes drop-down menus for both country and language. In this demonstration, Redis loads the values.

![movie interface language selection](/images/site-mirror/25de617cf07f3ead866b1dd86b5c48703d48ddf2-1304x557.webp)

*Pop-up screen to add a new movie*

## Code

The two code blocks below display a fetch query of master data from both MongoDB and Redis that loads the country and language drop-down values.

Previously, if the application used MongoDB, it searched the static database to retrieve the movie’s country and language values. That can be time-consuming if it’s read from persistent storage—and is inefficient if the information is static.

Instead, the “after” views in the code blocks (on right) show that the master data can be accessed with only a few lines of code—and much faster response times.

![Query to fetch masters from MongoDB and Redis](/images/site-mirror/c66a6153d1ae9af1da30e9b8488f359900e8e428-624x266.webp)

*Query to fetch masters from MongoDB and Redis*

![Query to fetch masters from MongoDB Atlas and Redis](/images/site-mirror/92585081fd29559c9e3937475972b750bbd39752-624x380.webp)

*Query to fetch masters from MongoDB Atlas and Redis*

## Sensing a pattern here?

The master data-lookup pattern​ is not the only design pattern you can use to improve application performance.

To learn about other effective techniques when using Redis for performance improvement, including the “cache-aside” design pattern and the “[write-behind](/blog/three-ways-to-maintain-cache-consistency/)” design pattern, download our ebook, [**Three Design Patterns to Speed Up MEAN and MERN Stack Applications**](/docs/three-design-patterns-to-speed-up-mean-and-mern-stack-applications/)**.**
