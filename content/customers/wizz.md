---
title: "Redis Enterprise Powers International Expansion of Wizz, the Friend-Finding App"
linkTitle: "Redis Enterprise Powers International Expansion of Wizz, the Friend-Finding App"
url: "/customers/wizz/"
description: "Voodoo’s popular social app, Wizz, must support 88,000 queries per second (QPS) during peak traffic periods. This necessitates a resilient, high-throughput, low-latency database capable of handling..."
group: "Software"
lastmod: 2025-09-12
hidden: true
---

*updated 12 September 2025*

###### Challenge

Voodoo’s popular social app, Wizz, must support 88,000 queries per second (QPS) during peak traffic periods. This necessitates a resilient, high-throughput, low-latency database capable of handling hundreds of millions of users.

###### Solution

By using core Redis features such as micro caching, sharding, leaderboards, rate limiting, and PubSub, Wizz has created a highly available social entertainment environment that is easy to manage and use.

###### Benefits

Redis Enterprise on Google Cloud allowed Wizz to scale from a small online service hosting 40,000 sessions per day to a rapidly growing, international service hosting millions of sessions per day. And it’s done so with exceptional performance, uptime, and reliability.

> "The best matches on Wizz are among people who are using Wizz at the exact same moment, which makes the low-latency, real-time processing aspects of Redis Enterprise extremely important."

### Establishing a database infrastructure to support explosive growth

Wizz is a social discovery app and online experience that allows Gen Z teens to meet new people, chat, play games and make friends—a new category called social entertainment. Voodoo has lofty ambitions for this flagship application, with a goal to take on Facebook, TikTok, and other industry leaders. Launched in the United Kingdom in October 2022, the Wizz app quickly went viral through TikTok re-shares, with 20 million views and an average engagement rate of 20 days. As of this writing, Wizz is available in the United States, Canada, United Kingdom, and Australia—and will soon be available in 23 other countries around the world.

“Welcome to Wizz, where the fun comes from the unexpected.” That’s a great tagline for attracting Gen Z teens to a new social entertainment app, but it can be a nightmare for the IT professionals who must turn millions of unexpected user actions into a seamless online experience. That’s why Voodoo, the creator of the wildly popular Wizz mobile app, relies on Redis Enterprise to enable a secure, scalable, high performance database infrastructure.

### Selecting Redis Enterprise

With a small tech team of just eight people, Wizz needs software that is easy to deploy, manage, and maintain. They selected [Redis Enterprise on Google Cloud](https://redis.io/cloud-partners/google/) because it is powerful, cost effective, and scales readily with a couple of clicks. “We need to simplify management, and we don’t want to bother with scaling our infrastructure,” says Gautier Gédoux, chief technology officer at Wizz. “Redis Enterprise is very stable and easy to use.”

Initially, Wizz deployed Redis in the form of Google Cloud’s Memorystore, a fully managed in-memory data store service. However, Wizz discovered they required dedicated Redis support and greater capabilities to ensure even lower latency and reliable scalability as the app grew in popularity globally. To ensure they delivered against these requirements, Wizz decided to establish a direct contract with Redis that gives them more control over the Redis deployment.

Since migrating to Redis Enterprise on Google Cloud—which is supported by Redis—Gédoux and his team have enjoyed the technical support and higher availability for their Redis Enterprise deployments. “With one email message to Redis support, we have been able to get fast, actionable information that has enabled us to effectively scale Wizz without sacrificing performance or impacting our users’ experience at all,” Gédoux says.

### Caching data to enable exceptional customer experiences

As a social discovery, gaming, and entertainment app, Wizz is designed to enable people to easily meet and befriend each other in a safe, vibrant, interactive environment. The service is driven by one-to-one messaging as well as by real-time chat sessions that often involve multiple participants. A match-making algorithm helps like-minded teens find each other and instantly communicate within the app.

Users expect instantaneous service and personalized experiences. To enable real-time interactions, Redis Enterprise stores data about messages sent, messages received, and messages read in a distributed caching engine that supports stateless application processes. That minimizes duplication of cached data and virtually eliminates requests to external data sources–currently about 50 million messages per day. “All the data from thousands of simultaneous sessions is administered in real time by Redis,” Gédoux says.

However, Redis Enterprise is more than just a cache for Wizz application data. If Redis fails, the application fails. To ensure stable operation, Wizz uses Redis Enterprise for session management and session state monitoring as well.

Redis Enterprise caches session state data in an extremely fast in-memory cache, enabling an instantaneous response to each tap, swipe, chat, and gaming request. This allows Wizz to remember pertinent details about each user, including login credentials, personalization information, and recent actions, such as which friends they interacted with. When a user disconnects, some data is persisted in the database for future use.

### Achieving global messaging performance with Redis PubSub

Wizz uses WebSockets to coordinate data among geographic regions. As the service expands, the tech team is considering using Redis Enterprise’s sharding capabilities to partition large databases into small components that are faster and easier to manage. “Database read time is very important to us, so we are using Redis to synchronize all our WebSockets,” Gédoux explains. “We don’t want to depend on a cluster-wide server. We want U.K. users to be able to speak with U.S. users, and so forth.”

To enable consistent messaging, both within and between regions, Redis is used as a Publisher/Subscriber platform. Published messages are characterized into channels, without knowledge of what (if any) subscribers there may be. Subscribers express interest in one or more channels, such as favorite pets, scary experiences, or anything else users want to talk about.

### Using Redis Enterprise to improve stability and query performance

The first iteration of the Wizz architecture relied on another cloud database that tended to bog down if the client load grew too quickly. Today, critical database processing has been migrated to Redis Enterprise, which can support the real-time processing loads that are essential for this widely used social entertainment application. “The built-in alerting system has allowed us to prevent downtime, especially on spiky traffic,” Gédoux says.

Scaling Redis Enterprise on the Google Cloud environment is easy. “With a couple of clicks, we can open new database instances or add CPU power to support a rising query load,” Gédoux says. “Without Redis Enterprise, it would be very costly to enable this same experience for our users.”

Wizz also uses [Redis Enterprise for leaderboards](https://redis.io/solutions/leaderboards/) that power its matchmaking algorithm. A leaderboard is a type of scoreboard that keeps track of user names, rankings, current scores, and other data points pertinent to an application experience. “The best matches are among people who are using Wizz at the exact same moment, which makes the low-latency, real-time processing aspects of Redis Enterprise extremely important,” Gédoux says. Redis Enterprise tracks sessions and knows exactly when users connect, so people can have synchronous, interactive discussions.

### Preventing cyber attacks with Redis rate limiting

Wizz uses Redis rate limiting functions to put a cap on how often a user can repeat an action, such as placing a limit on the number of server requests allowed in a one-minute period. This is an important facet of Wizz’s cybersecurity practice, since it prevents malicious actors from succeeding with denial of service (DoS) attacks, in which excessive server requests can bring an online service to a halt.

Wizz experienced the devastating impact of a cyberattack in October 2022 when hackers succeeded in corrupting a cloud database from another vendor, resulting in a three-hour outage. Rate-limiting policies in Redis will prevent these incidents from occurring in the future. “In one day we put a rate limiter in place, so if we get attacked it doesn’t corrupt the entire database,” Gédoux says.

### Adopting a micro-monolithic software architecture

Gédoux and his team built Wizz on a micro-monolithic architecture, in which many [microservices](https://redis.io/solutions/microservices/) are grouped together, simplifying development and deployment of the data environment.“The Wizz service depends on lots of databases,” Gédoux says. “Each one binds to a micro-monolith that combines many microservices.”

Wizz plans to expand this versatile software environment as it rolls out the social entertainment service in 27 additional countries, beginning with Germany, France, and the Netherlands. Gédoux says it is extremely easy to spin up new Redis clusters, as well as to replicate user subscriptions across geographies. The development team is considering using the Active-Active feature of Redis Enterprise to streamline communication by allowing users in any country to see who’s online from moment to moment, as well as to accelerate messaging through WebSockets across regions.

“We don’t need to think about Redis,” Gédoux concludes. “It just works. We have only had to call the support line once, and the Redis Enterprise service has never failed.”
