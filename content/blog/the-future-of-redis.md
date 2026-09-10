---
title: "The Future of Redis"
linkTitle: "The Future of Redis"
url: "/blog/the-future-of-redis/"
description: "Following yesterday’s announcement of the Redis licensing change, we want to provide a wider view of our future for our customers, partners, and the developer community."
date: 2024-03-21
blogCategories:
- "Uncategorized"
authors:
- "Rowan Trollope"
- "Yiftach Shoolman"
lastmod: 2025-07-03
hidden: true
mirrored: true
---

*By Rowan Trollope, Yiftach Shoolman · Published 21 March 2024 · updated 3 July 2025*

![Blog tile image](/images/site-mirror/fa552eae80b9c38b5e33ffdc39b0844b5c209160-772x552.webp)

Following yesterday’s announcement of the Redis licensing change, we want to provide a wider view of our future for our customers, partners, and the developer community.

Redis has been a tremendous success, thanks to the support of our developer community and the hard work of the entire Redis team. The principles outlined in the Redis manifesto continue to guide our approach to building software. As a company built by developers for developers, we constantly seek feedback from our ecosystem on how we can improve and add new capabilities.

So, what have we heard and where are we investing?

**Simplifying the Redis Experience**

First, we’re focusing on simplicity and the developer experience – both in the core and in our developer experience. Starting with Redis 8, we’re integrating Redis Stack capabilities including query and search, vector search, JSON document support, time series and probabilistic structures into the Community Edition, providing a single, comprehensive Redis that offers all the latest features without the need for separate downloads or packages. Simplicity is key, and this change is driven by the overwhelmingly positive feedback we’ve received about Redis Stack and the fact that in CY’23 Redis Stack represented over 50% of the download volume of Redis 6.x.

We’ve also worked with various community members to consolidate and officially support the most popular language-specific client libraries used with Redis. We are taking action to ensure that every client library we support is updated and tested on the latest Redis release and that capabilities are delivered consistently across versions. For example, Redis has had support for client-side caching for quite some time, but it does not appear in the vast majority of client libraries. Our goal is to provide client-side caching support for all the client libraries under Redis’ responsibility in a way that provides consistent behavior across Redis Community Edition and our commercial offerings. Further, all client libraries under Redis’ responsibility are open source.

**Making Redis the Go-To for Generative AI**

Next, we’re staying at the forefront of the GenAI wave. We were among the first to recognize the need for vector search functionality in a database, even before ChatGPT and LLMs were household names. By leveraging real-time Vector Search, Semantic Caching, and personal Chat History, Redis allows you to develop real-time GenAI applications in a cost-effective and efficient manner. Furthermore, we recently launched Redis Vector Library (RedisVL) to allow developers to easily build these applications with some of the leading GenAI frameworks, such as Azure Open AI, AWS Bedrock, LangChain, OpenGPTs, and LlamaIndex.

RedisInsight, our companion tool for developers recently surpassed 100,000 monthly active users and will soon feature an AI-powered assistant called Redis CoPilot to allow developers to directly interact with their data using language and translate that into code.Going further, our plans for the near future include making Redis even more cost-efficient for RAG use cases by leveraging product quantization and further improving vector processing performance with the latest hardware and GPU advancements.

**Community-Inspired Development**

As a company guided by our developer community, we’re working to release the most requested features and enhancements. A prime example is hash field expiration, a highly requested capability that will be part of Redis Community Edition 7.4. We’re eager to tackle other long-standing feature requests in the coming months.

We also want to address the struggle that many companies have launching modern web/mobile apps that use data scattered across multiple sources, usually hosted on non real-time relational or NoSQL databases. To do this, we’re launching Redis Data Integration (RDI), a new product that lets architects and developers seamlessly and continuously transform data from multiple data sources into Redis using Change Data Capture (CDC) technology. RDI can also automatically write back data changes using a write-behind technique when existing databases still need to be maintained. RDI is currently in public preview and being deployed into production by our early adopter customers. We expect to make it generally available in the coming months. By using a single API to access data, Redis becomes the front-end database for modern real-time applications.

**Doubling Down on Speed with the Acquisition of Speedb**

Finally, we’re going back to our roots as the world’s fastest real-time data platform and are proud to announce the acquisition of Speedb, the world’s fastest data storage engine.

Over the past two years, we’ve been working directly with Speedb, integrating it as the default storage engine in the Redis Enterprise auto-tiering functionality launched recently in version 7.2. Our close collaboration with Speedb and encouraging developer feedback on our integrated releases led us to an easy decision: join forces to advance the Redis core with a fully integrated storage engine.

In doing so, we open up many new use cases for Redis without sacrificing end-to-end performance. Now is the time to take full advantage of innovations and advancements in SSD storage and transfer rates, which are two orders of magnitude faster than when Redis originally launched (10GB/s vs 100MB/s). As a result, we’ll be able to deliver lightning-fast speed with greater price performance without compromising application performance.

The recipe is simple and revolves around speed. We’re pairing Redis’s unmatched simplicity and blistering speed, best suited for applications with intense latency requirements, with Speedb’s speed and cost-efficiency for all other use cases.

In summary, Redis is evolving based on community feedback and staying true to our manifesto. We’re focusing on simplicity, the developer experience, and staying at the forefront of the GenAI wave. Guided by our developer community, we’re releasing highly requested features and introducing new approaches to enable real-time applications. With the acquisition of Speedb, we’re reinforcing our position as the world’s fastest real-time data platform. The future of Redis is bright, fueled by our community, customers, and a relentless pursuit of excellence.
