---
title: "Session Store Patterns"
linkTitle: "Session Store Patterns"
url: "/blog/session-store-patterns/"
description: "On a typical day, you might open your web browser and rapidly access social media, do some shopping, newspapers and more. You likely have numerous notifications from various events you may or may..."
date: 2019-03-12
blogCategories:
- "How To and Tutorials"
authors:
- "Redis  "
lastmod: 2025-03-27
hidden: true
mirrored: true
---

*By Redis   · Published 12 March 2019 · updated 27 March 2025*

![Blog tile image](/images/site-mirror/4eec81f7ee963127036a363a1328d9037bf7565d-390x390.webp)

On a typical day, you might open your web browser and rapidly access social media, do some shopping, newspapers and more. You likely have numerous notifications from various events you may or may not actually attend, and you might expect your preferred shopping site to tailor search results to your order history. Perhaps your media platform of choice presents you with topics in which you’ve previously demonstrated an interest, in order to encourage you to continue to consume. All of these phenomena are indicative of an intelligent session store — that is, a session store that stores data beyond your username or basic preferences.

When traffic to any given server increases, a session store is often the ideal mechanism to hold user data. But in order for a session store to be able to store and process intelligent — or more complex — data, it might require the assistance of a microservice. By decoupling session storage from the server, microservices enable companies to handle more complex use cases and process more advanced data without compromising on speed or performance.

Microservices can make it possible for social media applications to send you a group notification, for example, or for an eCommerce site to recommend products for you based on previous purchases you’ve made. And if your company would like to use microservices in this way — in order to facilitate advanced data processing and more effective use of infrastructure— Redis is the ideal choice. By serving as both a database and a transport mechanism, Redis allows companies to add on a limitless number of servers, and makes it possible for a microservice and a server to communicate with one another.

When you compare Redis to other popular databases, you’ll find that Redis has true [highly availability](/redis-features/high-availability), and is able to perform more writes and reads at much lower latencies. Perhaps more importantly, a Redis powered session store microservice is able to implement a patterns that optimize user experience: content surfacing, activity pattern monitoring and group notifications with minimal resources

For news sites and e-commerce platforms, it is of the utmost importance that users are consistently shown new and personalized content. This can be complicated to execute, as it would involve storing every piece of content a user has ever interacted with. However, Redis surmounts these challenges by using a session store contained [Bloom filter](/blog/rebloom-bloom-filter-datatype-redis/) to cross-check whether or not a certain piece of content is new to a particular user. Bloom filters are incapable of returning false negatives, so content that does not appear in a certain user’s Bloom filter is guaranteed to be “fresh” content for that user, yet they don’t need to store each item

Activity pattern monitoring, meanwhile, is one of the best tools in a company’s arsenal to ensure that their clients’ experience on a site is expertly personalized. Redis’ microservice can help your company collect users’ behavioral data, and then use that data to better customize any given user’s experience. This can be a difficult process, especially given the limitations of a microservice, but Redis makes it possible by recording site activity with bit counting, tracking the unique pages a user visits in a [HyperLogLog](/redis-best-practices/counting/hyperloglog/) and combining these data points with specific insights, such as the number of times a user has interacted with a particular page or whether or not a user is new to a site. And because Redis employs a HyperLogLog, it is nearly impossible for third parties to extract user information, which can help reassure users about their privacy.

[Redis Enterprise](/redis-enterprise/) can also improve a website’s performance by making group notifications much more efficient. By storing group notifications in a [simple List data structure](https://redis.io/topics/data-types) and creating a Bloom filter for each user in their Redis-backed session, Redis has created a very lightweight process for sending group notifications and assessing when they have been read and received. Redis Enterprise is particularly well-designed for this operation because it enables persistence through in-memory replication.

In order to create a site that is engaging to each and every user, it is important to go beyond the basics. A session store is a useful way to store user data, but microservices backed by Redis can help your company excel by processing intelligent data and making sure that your user retention rate is high. If you have any questions about using microservices to make your session store more intelligent, or you’re curious about the patterns and modules that Redis offers, please don’t hesitate to reach out to us at [product@redis.com](mailto:product@redis.com).
