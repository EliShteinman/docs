---
title: "How Mutualink Uses Redis to Support a Life-Saving Microservices Architecture"
linkTitle: "How Mutualink Uses Redis to Support a Life-Saving Microservices Architecture"
url: "/blog/how-mutualink-uses-redis-to-support-a-life-saving-microservices-architecture/"
description: "(As organizations look to modernize their applications, many are turning to a microservices architecture to deconstruct their legacy apps into collections of loosely coupled services. This profound..."
date: 2020-01-15
blogCategories:
- "Company"
authors:
- "Sheryl Sage"
lastmod: 2025-03-27
hidden: true
---

*By Sheryl Sage, Director of Partner Marketing · Published 15 January 2020 · updated 27 March 2025*

![Blog tile image](/images/blog/98923d2ca8e84b52306450f3658e454a2a964c7d-2000x1405.webp)

*(As organizations look to modernize their applications, many are turning to a microservices architecture to deconstruct their legacy apps into collections of loosely coupled services. This profound change inspired us to reach out to Redis customers in various stages of this journey to microservice architectures. We will be telling their microservices stories in a series of blog posts in the coming weeks.)*

When Mutualink looked to modernize its [Interoperable Response and Preparedness Platform (IRAPP)](https://mutualink.net/our-solution/), the company’s IT team turned to a microservices architecture to enable dozens of technology components to work seamlessly together. That’s important, because [Mutualink](https://mutualink.net/)’s mission is to facilitate collaboration between Federal, state, and local agencies and private entities to resolve dangerous incidents.

Paul Kurmas, Director of Strategic Product Development at Mutualink, shared what a microservices model means to him: “It allows us to design components that do one thing and do it well, and the payoff is simpler software that is faster, more reliable, and easily supportable. Our microservices architecture maximizes availability and minimizes the scope of any software, system, or communications failure, while also helping us scale because we can load-balance work from various clients or internal services across a large pool of instances.”

All of this requires a flexible and efficient central data store with top performance, effortless scalability, and high availability. That’s why the Mutualink team turned to Redis Enterprise to power the data layer in its microservices architecture.

## Achieving top performance in an environment where low latency saves lives

Mutualink’s tens of thousands users expect instant response every time they use the system to track and report location data during an incident; send and receive text, audio, or video messages; share files; and more. So IRAPP’s latency must be as low as possible, and the architecture has to maintain its performance even as clients’ needs scale. At any given time, the platform might contain hundreds of active collaborations between agencies, each of which feeds an event stream with data on who’s online where and what new content is available for subscribers.

Mutualink runs Redis Enterprise on virtual machines that store upwards of 32 terabytes of data, including both user records and subscriptions to these various streams. Thanks to Redis’ ability to automatically scale data across servers, the IRAPP can maintain consistently high performance and scale dynamically by adding servers or availability zones as these collaboration volumes expand. This lets Mutualink handle a large number of concurrent data requests with sub-millisecond latency.

## Active-Active replication ensures high availability and data resiliency

From the beginning, Mutualink worked to enable high availability so the platform could survive the loss of a software instance, compute node, or even an entire data center. One way the team accomplishes this is through [Redis Enterprise’s Active-Active replication](/active-active/), in which data is automatically synchronized between multiple data centers for geographic redundancy. “Our focus on instant access to data is critical. It’s what made Redis an attractive solution to be the central data store to our application,” Paul noted. “The Active-Active functionality was our deciding factor in using Redis Enterprise, and it saved my team many, many staff years’ of time trying to invent a cross-data site synchronization model.”

![](/images/blog/bf273442b64d8e1f623c6183d6574a9b76aefe81-1024x590.webp)

Mutualink’s Redis data model supports near real-time, eventual consistency—if an event triggers a change to data on the company’s server in its Boston region, for example, the response to the event-triggering client is immediate, while the data is reflected on its server in its Dallas region in near real-time. Additional clients can subscribe to events in Redis in whichever region is closest.

Taking a closer look, the microservice that handles signaling for voice over IP (VoIP) has to maintain thousands of telephony connections even if there’s a software failure. Mutualink exports each call state from the platform and stores it in Redis in multiple regions, so that the platform remains stateless. Then, when the next message in that session is ready, it can be delivered efficiently to any instance of the service. Thanks to Redis Enterprise’s conflict-free replicated datatypes (CRDT), the VoIP service provides uninterrupted availability even when some data centers are completely unavailable. With this kind of resiliency, the overall application can continue to perform reads and writes even if one or more of the individual microservices fails.

## Establishing team autonomy by minimizing interdependence between services

While Mutualink originally planned to use Redis for just one central component of its microservices architecture, the team quickly learned how easy it was to plug other services into Redis and use its simple APIs to maintain their own data. Rather than having one service (which they called “the World”) act as the gatekeeper to all of the platform’s data, Mutualink now has 15 – 20 different services directly using Redis Enterprise to serve various needs.

![](/images/blog/7df7094971f69f0860635ee4283c353add9f4129-1024x311.webp)

Redis’s extensibility and data model diversity help the Mutualink team avoid vendor sprawl, since its data structures can support a wide range of business capabilities. Features Mutualink has built with Redis include:

- Buffering text messages for asynchronous transmission in a content cache
- Maintaining client device location, presence, and time with [Redis’ Geospatial indexing](/glossary/geospatial-indexing/)
- Managing authentication stores and search trees with Redis Strings, Sets, and Lists
- Supporting inter-service communications (HTTP, POST, PATCH, GET, and DELETE) by using [Redis as a simple message queue](/solutions/messaging/).

![](/images/blog/061b43a20f376d08922c8926b66ff80cab2bf888-642x333.webp)

Redis helps each of these microservices transform data without requiring changes to the back-end stores. Mutualink benefits from a common, yet decentralized, data layer in Redis that all services can access. Plus, each service can use the right language, database, or other developer tools for the job at hand. Since Redis supports multiple data formats, individual services can employ key-value, graph, hierarchical, JSON, streams, search, or other data models as needed.

## Supporting efficient legacy migration and modernization

By enabling Mutualink to cache frequently used content and evict unnecessary data (such as expired authentication tokens or aging data surrounding subscriptions, text messaging, and HTTP live-streaming services), Redis Enterprise also ensures optimal use of the company’s compute resources. For instance, Redis stores frequent location status updates and OAuth2 tokens, which are kept on a short timeout. When a client stops reporting, Redis automatically removes its subscriptions and presence reports to free memory.

By using Redis as both a caching layer and primary data store, Mutualink can more quickly phase out its legacy architecture and replace it with more efficient access to data. “We have a 3 – 6 month window to move thousands of users over to our new microservices-based system,” Paul said. “Since Redis and microservices remove the constraints of our old architecture, it will increase our speed of deployment 2x – 3x within the first year.”

## Future-proofing the architecture with Redis Enterprise and microservices

Now that Mutualink has laid the groundwork for its modern microservices architecture, Paul looks forward to building out even more purpose-built software components. He expects Redis Enterprise to remain a key asset as his team scales to more instances, mitigates the impact of failures, and performs upgrades to individual services.

Learn more about how [Mutualink is taking full advantage of Redis Enterprise](/customers/mutualink/).

[***Join us:***](https://dzone.com/webinars/adopting-a-microservices-architecture-dont-forget)Hear more about Mutualink’s journey to a microservices architecture and how Redis Enterprise is used to solve several key problems with distributed systems in our January 22 webinar.

*Featured image by Nicholas Jeffries, Unsplash*
