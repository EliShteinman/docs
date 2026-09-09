---
title: "Overcoming Microservices Adoption Challenges"
linkTitle: "Overcoming Microservices Adoption Challenges"
url: "/blog/overcoming-microservice-challenges/"
description: "Concerns about complexity, eventual consistency, and latency: all these can generate reservations from those who are new to adopting microservices. Our solution brief, Cache and Message Broker for..."
date: 2023-03-09
blogCategories:
- "Tech"
authors:
- "Henry Tam"
lastmod: 2025-03-27
hidden: true
---

*By Henry Tam · Published 9 March 2023 · updated 27 March 2025*

![Blog tile image](/images/blog/6d8ea508ce03795ed157cc164cd3820c4a4961af-772x550.webp)

**Concerns about complexity, eventual consistency, and latency: all these can generate reservations from those who are new to adopting microservices. Our solution brief, *****Cache and Message Broker for Microservices, *****highlights the design patterns that can help you work around such common obstacles.**

Microservice architecture can be a game-changer that helps organizations reduce barriers for organizations’ application modernization and [cloud](/redis-enterprise-cloud/overview/) migration journey – and lets them beat their competition to market. A [microservice architecture](/solutions/microservices/) decouples business domains into their own respective services, dependent on use case or function, while keeping the line of communication open between all services through APIs. Each domain typically has its own autonomous development team who creates, manages, tests, and deploys services independent of all other domains. This provides faster time to market as each service has its own release cycles.

Here’s a real-world example:

Consider the airline industry, where real-time data is exchanged through numerous applications by various business domains. The business domains – you might think of them as departments – might include the reservations system, baggage handling, and passenger check-in systems. If Joe Smith buys a ticket from Atlanta to Miami, that information goes into a reservation system. That data can be readily retrieved once Joe Smith checks in at an airport kiosk on the day of his flight. When Joe hands over his luggage to the airline, a whole other division (separate from reservations and check-in services) ensures that Joe’s luggage arrives in Miami when he does.

Each domain has its own enterprise tools and resources, and it might use a unique tech stack or database platform. One microservice might use Java and a NoSQL [JSON document store](/json/); another service may use a legacy mainframe system that runs on COBOL and a relational database. All these distributed services are connected via an API gateway which enables the airline to build applications that call on data from several sources, such as airport kiosks, booking sites, and baggage handling. The point is: the same data can be accessed in real-time by all these decoupled services through APIs.

## Microservices challenges

What are the challenges preventing the wider adoption of microservices? Despite the many benefits of a decoupled architecture, why aren’t all companies making the switch?

**Complexity**: In the end, dispersing each viable domain from a monolithic architecture into microservices almost always creates a more complex system. As someone commented in our [5 Microservices Misconceptions](/blog/5-microservices-misconceptions/) post, “Companies think they can make the complexity go away with microservices. But you don’t really make it go away; you just move it to a different layer of abstraction.”

When functionality is splintered into hundreds or thousands of isolated domains, team autonomy can introduce a host of different SLAs, tools, and various headcounts to troubleshoot and properly manage each domain at the data tier.

How to untangle all these disparate tools in one distributed system without breaking isolation? The answer lies in the efficient use of one data platform for caching that supports the optimal data models and provides a lightweight message broker for inter-service communication. This enhances developer productivity, provides faster time to market, and generally streamlines the architecture of your application.

**Eventual consistency: **Maintaining strong consistency is extremely difficult within a distributed system. Though domains in a microservice architecture must be decoupled, teams need to maintain up-to-date data, even with far-flung instances halfway across the globe.

It’s essential for all services to maintain optimal consistency with shared data, whether you’re dealing with a system of record write-optimized database in one microservice and a read-optimized cache in another service. You will need to implement the Command Query Responsibility Segregation ([CQRS](/solutions/microservices/cqrs/)) pattern to improve cross-domain data access with sub-millisecond query latency. And if microservice instances are distributed to multiple data centers around the world, Active-Active Geo-Replication of the read data is required to scale and maintain availability.

**Latency:** Latency can come from all angles. Each new domain or component can elevate the risk of performance failure, as the growing number of API calls between services can escalate and grow into unwanted latencies.

Ideally, if you follow the domain-driven design principle of using an optimal database for each microservice, latency wouldn’t be an issue. However, [legacy databases](/blog/legacy-database-migration/) need to be used in a specific microservice in some industries due to technical debt constraints or regulatory reasons. However, those applications can’t meet the performance SLAs. Caching can provide those query response times, though, and setting it up requires minimal development time.

A single bottleneck in the data flow in one microservice can cascade into a system-wide collapse, especially if it’s global data at the API gateway. The API gateway cannot be the single point of failure that leads to system downtime, user crankiness, and news headlines that you truly did not want to see.

To optimize durability, consistency, and read performance, your application needs a powerful cache and rate-limiting solution for the API gateway.

## Explore our microservices solution brief

Learn in detail about Redis Enterprise solutions that can minimize the cost and complexity of microservice applications with [Cache and Message Broker for Microservices](/docs/caching-for-microservices/).
