---
title: "How Redis Fits with a Microservices Architecture"
linkTitle: "How Redis Fits with a Microservices Architecture"
url: "/blog/how-redis-fits-with-a-microservices-architecture/"
description: "This blog post was adapted from our new e-book, “Redis Microservices for Dummies” by Kyle Davis with Loris Cro. The excerpt was originally published on The New Stack on December 20, 2019. Download..."
date: 2020-01-09
blogCategories:
- "Company"
- "Tech"
authors:
- "Redis  "
lastmod: 2025-03-27
hidden: true
mirrored: true
---

*By Redis   · Published 9 January 2020 · updated 27 March 2025*

![Blog tile image](/images/site-mirror/0073e867b4e64f59de9047fdcde04295ba647e5c-772x550.webp)

*This blog post was adapted from our new e-book, “Redis Microservices for Dummies” by Kyle Davis with Loris Cro. The excerpt was *[*originally published on The New Stack on December 20, 2019*](https://thenewstack.io/how-redis-fits-with-a-microservices-architecture/)*. *[*Download the complete e-book here.*](/docs/redis-microservices-for-dummies/)

Many of today’s widely used database systems were developed in an era where a company adopted a single database across the entire enterprise. This single database system would store and run all the functions of the enterprise in one place. You can probably picture it: a room full of refrigerator-sized machines, many sporting oversize reel-to-reel tape drives.

![](/images/site-mirror/cd65d2a4a9c251417a73b540ac22800d8f8dbd16-300x184.webp)

But Redis evolved differently than many other popular database systems. Built in the NoSQL era, Redis is a flexible and versatile database specifically designed not to bother storing massive amounts of data that will be mostly idle. A microservices architecture has related goals: each service is designed to fit a particular use—not to run everything in the business.

Redis is designed to store active data that will change and move often, with an indefinite structure with no concept of relations. A Redis database has a small footprint and can serve massive throughput even with minimal resources. Similarly, an individual service in a microservices architecture concerns itself only with input and output and data private to that service, meaning that Redis databases can back a wide range of different microservices, each with their own individual data store. That’s important, because the very nature of having many services means that each service must perform as fast as possible to make up for the connection and latency overhead introduced by inter-service communication.

## Describing a Redis-powered microservices architecture

A key characteristic of a microservices architecture is that each individual service stands on its own—the service is not tightly coupled with another service. That means microservices must maintain their own state, and to maintain state you need a database.

Microservices architectures can comprise hundreds or even thousands of services, and overhead is the enemy of scale. An infrastructure that consumes lots of resources just to run would dilute the benefits of a microservices architecture.

Ideally the service data would be completely isolated from other data layers, allowing for uncoupled scaling and cross-service contention for slow resources. Since services are specifically designed to fill a single role (in terms of business processes), the state they store is inherently non-relational and well suited to NoSQL data models. Redis may not be a blanket solution for all data storage in a microservices architecture, but it certainly fits well with many of the requirements.

Once you have built a service, it needs to talk to other services. In a traditional microservices environment, this occurs over private HTTP endpoints using REST or similar conventions. Once a request is received, the service begins processing the request.

While the HTTP approach works and is widely used, there is an alternate method of communicating where services write to and read from log-like structures. In this case, that’s [Redis Streams](/blog/use-redis-streams-apps/), which allows for a completely asynchronous pattern where every service announces events on its own stream, and listens only to streams belonging to services it’s interested in. Bidirectional communication at that point is achieved by two services observing each other’s stream.

Even in services that do not use Redis for storage or communication, however, Redis can still play a vital role. To deliver a low-latency final response, each individual service must respond as fast as possible to its own requests, often outside the performance threshold of traditional databases. Redis, in this case, plays the role of a cache, where the developers of the service decide where data is not always required to be retrieved directly from the primary database, but instead can be pulled from Redis much more quickly.

Similarly, external data services that need to be accessed through an API will also likely be far too slow, and Redis can be used here to prevent unneeded and lengthy calls from impacting the system’s overall performance.

*For more detail on how Redis can help power your microservices architecture, *[*download your own copy of the “Redis Microservices for Dummies” e-book*](/docs/redis-microservices-for-dummies/)* and *[*listen to authors Kyle Davis and Loris Cro discuss the book on the The New Stack Context podcast.*](https://thenewstack.io/the-new-stack-context-microservices-for-dummies/)
