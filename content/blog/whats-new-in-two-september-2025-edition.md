---
title: "What’s new in two: September 2025 edition"
linkTitle: "What’s new in two: September 2025 edition"
url: "/blog/whats-new-in-two-september-2025-edition/"
description: "Click here to view video"
date: 2025-10-01
blogCategories:
- "Tech"
authors:
- "Talon Miller"
lastmod: 2026-08-14
hidden: true
---

*By Talon Miller, Principal Technical Marketer · Published 1 October 2025 · updated 14 August 2026*

![Blog whats new in two](/images/site-mirror/240e8c42eca43562f3fb6b2558a548c7fd66b1a9-772x552.webp)

[Click here to view video](https://www.youtube.com/embed/Z0M0q5F8zpc?si=EFBysn1lpoGDrE1a)

Welcome to “What’s new in two,” your quick hit of Redis releases you might have missed in the past month. We’re covering the latest developments from September and expanding on what I covered in our latest video. Press play above if you’d rather watch than read. Let’s get started.

On September 4th we announced our Fall Release–a comprehensive set of updates across Redis for AI, Redis Cloud, and Redis Open Source. Let’s dive into the highlights.

## Fall Release 2025

## Redis for AI

### LangCache public preview

Meet our new fully managed semantic caching service. It stores and retrieves semantically similar calls to LLMs for chatbots and agents, saving roundtrip latency and drastically reducing token usage, cutting costs. [Try it out here](https://redis.io/langcache/).

### Hybrid search improvements

A number of improvements came to our [Redis Query Engine](https://redis.io/query-engine/) for specifically how hybrid search is set up and run:

- Improved accuracy–Combine text search and semantic relevance using multiple methods like linear fusions and Reciprocal Rank Fusion (RRF).
- Simpler implementation–Out-of-the-box so you don’t need custom code.
- No client-side merging–Results are fused efficiently on the server.

### Vector compression

Vector search in Redis now supports quantization of embeddings and dimensionality reduction through standard scalar quantization and more advanced algorithms based on Intel SVS. This has a real impact for performance like– 

- Up to 37% lower costs for Redis vector databases
- 144% faster search speeds
- Low accuracy impact compared with larger embeddings

#### [Get started here](/blog/quantization-and-dimensionality-reduction-are-now-available-in-redis-query-engine/)

### Vertical scaling generally available

Query Performance Factor (QPF) for our Redis Query Engine is here. This can add up to 16x more processing power–multi-threading can deliver real-time results on even larger dataset across even more complex queries. [Learn more on our docs](https://redis.io/docs/latest/operate/oss_and_stack/stack-with-enterprise/search/scalable-query-best-practices/).

## Redis Cloud

### 8.2 generally available

We announced 8.2 on Redis Open Source on last month’s episode and this month it comes to Redis Cloud. If you’re still on 7.2 then 8.2 has a lot to offer–

- Up to 91% faster commands
- Up to 37% smaller memory footprint with up to 67% reduction with JSON
- The addition of the Redis Query Engine, 18 data structures including vector sets, and 480+ commands like hash field expiration.

#### [Try Redis Cloud for free](https://redis.io/try-free/)

### Redis Data Integration (RDI) public preview in the Cloud

One of my favorite products is coming to the cloud! Keep your data fresh and in-sync with your external source databases using an easy no-code data pipeline. Learn more about [RDI here](https://redis.io/data-integration/).

### Redis Insight in Cloud

Redis Insight (an amazing developer companion tool while working with Redis) is now available on Redis Cloud. You can act and explore your Redis data straight from your browser. And soon, you’ll also get access to a redesigned UI and new onboarding experience for vector search and let me tell you an inside secret, *the new redesign is amazing*. Can’t wait. I hope this isn’t your first time hearing about Redis Insight but if it is, [check it out here](https://redis.io/insight/).

### Redis Released is live

We kicked off our worldwide event series in San Francisco on September 4th. It was an incredible time to hear from our customers and partners about what they’re building and learning how we can make Redis even better for the future of AI. We then continued the tour and had events in Dubai, Bengaluru, Singapore, Jakarta, Munich, and New York. And don’t worry if this is the first time you’re hearing about it, we still have plenty of locations left in October and even November, see if there are [any seats left here](https://redis.io/released/).

### New Developer Hub and Demo Center now live

I am super excited to share that we released a completely new [Developer Hub](https://redis.io/dev/) and [Demo Center](https://redis.io/demo-center/) in the first week of September. The dev hub is the best place to get tutorials, learn more about commands, and connect with the community. And the demo center has demo videos, interactive demos, and more to learn about the hottest things happening at Redis. Let us know what you think!

## Redis Acquiring Decodeable

Also on September 4th, we announced our intent to acquire [Decodable](https://www.decodable.co/), a real-time data platform that helps build, process, and manage streaming pipelines. I am looking forward to seeing how RDI evolves as it's a key part to our solution and this acquisition will help not only turbocharge what we’re doing with getting data into Redis and in sync with external sources but provide a wider breadth of capabilities and connections. Learn more [about this acquisition here](/blog/redis-to-acquire-decodable-to-turbocharge-our-real-time-data-platform/).

That’s a wrap on September updates. If you want to learn more I recommend you read the [announcement blog](/blog/fall-release-2025/) for the Fall Release from our CEO, Rowan or visit [Redis.io/new](https://redis.io/new). Whether you prefer watching or reading, catch more valuable updates in my next two-minute episode. See you next time.
