---
title: "What’s New in Two with Redis – April Edition"
linkTitle: "What’s New in Two with Redis – April Edition"
url: "/blog/whats-new-in-two-with-redis-april-edition/"
description: "Click image to view video"
date: 2024-05-03
blogCategories:
- "Tech"
authors:
- "Talon Miller"
lastmod: 2025-06-11
hidden: true
---

*By Talon Miller, Principal Technical Marketer · Published 3 May 2024 · updated 11 June 2025*

![Blog tile image](/images/blog/b3bc49fca4afdc502e701986cdf738021d66979d-772x552.webp)

[Click image to view video](https://www.youtube.com/embed/pkKQG5Hnu28?si=f-J746A6p5j2FHCQ)

Welcome to “What’s New in Two,” the place to catch up on the Redis releases you might have missed from last month. In this article, we’ll delve deeper into developments from April, expanding on what I covered in our latest video. I’ve included a video thumbnail above for those who prefer watching a quick recap of this month’s updates. Let’s dive in.

You know our name, now [meet our new brand](https://www.youtube.com/watch?v=jbJHu3CjHi0). You’ve always known us for caching, but the thousands of customers who use Redis for vector search or as their NoSQL database know us for a different kind of fast. We thought it was time to reflect that in our brand so the world can see how fast feels. You can see it in action on our redesigned website.

Speaking of our website, exciting news for all Redis users. We’ve redesigned and merged redis.io and redis.com, bringing our new branding to life, and making it easier than ever to access all the resources you need. Our source available, Redis Cloud, and Redis Software docs are now consolidated in [one place](https://redis.io/docs/latest/), making it a breeze to find what you’re looking for. Plus, we’ve added Copilot to the docs, a [Chatbot](https://redis.io/chat) trained on all things Redis, built using Redis vector search, to help you find what you need, fast. And that’s not all — we’ve also introduced [new tutorials and curated learning paths](https://redis.io/learn), such as the [Vector](https://redis.io/learn/vector/) database learning hub to help you become a Redis expert. No matter what flavor of Redis you’re using, we’ve got you covered at redis.io.

Now, let’s get into some [Redis Cloud](https://redis.io/try-free/) updates. Some huge news, database creation is now use case driven. This is available now for all new subscriptions and will be rolled out to all current customers by May 5th. You’ll also notice that our Fixed and Flexible subscriptions names have been renamed Essentials and Pro. 

Next, we’re happy to announce the general availability of AWS Transit Gateway for Redis Cloud, so now all customers can [connect their AWS environments with Redis Cloud](https://redis.io/docs/latest/operate/rc/security/aws-transit-gateway/) through Transit Gateway. 

In addition, Redis Cloud now supports Replica-of with TLS for source databases with TLS or mTLS enabled. Replica-of, also known as Active-passive, is commonly used to replicate data [from one database to another](https://redis.io/docs/latest/operate/rc/databases/migrate-databases/#sync-using-active-passive) using a source/target data transfer, so now this process supports TLS.

Next, we’re improving how set up databases with search and query in our cloud. You can now set the throughput needed for new databases with Search and query using operations per second. In addition, the cloud API is modified to accept operations per second for search and query. This enhancement should simplify the configuration of new databases and help seamlessly scale query workload in and out as needed.

With our newest update to [Kubernetes](https://redis.io/docs/latest/operate/kubernetes/), we’re providing a way of tearing down and deleting stateful sets. Resizing the PVC and then recreating it back like before but with the newly desired scale, all handled by our [Redis Enterprise for Kubernetes Operator](https://redis.io/docs/latest/operate/kubernetes/deployment/).

Next, here is an update on our [Redis Enterprise Software](https://redis.io/docs/latest/operate/rs/) UI, you can now easily manage locked users. When a user is locked out due to incorrect password attempts, the admin will get a tag in the UI to reset the user’s password. Similarly, we added the ability to change passwords at login, and finally, you can now choose the database version during creation which is some nice added flexibility. For example, Each Redis Enterprise Cluster holds 3 Redis db versions, and the (configurable) default for new databases is the latest. Choosing a version other than the default is important when you need to create a database that correlates to another database in a previous version, e.g. test db, and now you need to make the production db. You want to have the same redis version, and now it’s easy to manage. 

Finally, let’s finish with a cool [Redis Insight](https://redis.io/docs/latest/develop/connect/insight/) update – you can now load demo data with one click. This is a great feature for a new or empty database you want to quickly get up and running and start testing with some data. 

That’s a wrap for this month’s “What’s New in Two,” where we’ve taken a closer look at Redis’ latest features and enhancements in April. Whether you prefer watching or reading, stay tuned for more valuable updates in my next two-minute episode. May releases are just around the corner, so stay tuned. And if you missed [last month’s update](https://www.youtube.com/watch?v=N6O00qkVc4w), two minutes is all you need to catch up. See you in the next one.
