---
title: "It’s a Wrap—RedisConf 19 Recap"
linkTitle: "It’s a Wrap—RedisConf 19 Recap"
url: "/blog/wrap-redisconf-19-recap/"
description: "Editor’s note: This post recaps RedisConf 2019. Join us at RedisConf 2020 on May 12-14 in San Francisco! You won’t want to miss keynote speaker Julia Liuson, Corporate Vice President of Microsoft’s..."
date: 2019-04-04
blogCategories:
- "Announcements"
authors:
- "Madhukar Kumar"
lastmod: 2025-03-27
hidden: true
---

*By Madhukar Kumar, VP of Technical and Product Marketing · Published 4 April 2019 · updated 27 March 2025*

![Blog tile image](/images/blog/49b35cc96bb9df676f7e7d0f0e7c042bbcf0e499-1539x1142.webp)

***Editor’s note:**** This post recaps RedisConf 2019. Join us at *[***RedisConf 2020***](/blog/rediscover-redis-at-redisconf-2020/)* on May 12-14 in San Francisco! You won’t want to miss keynote speaker Julia Liuson, Corporate Vice President of Microsoft’s Developer Division, who headlines a roster of more than 50 speakers sharing their expertise on the world’s most-loved database.*

On any other day, Pier 27 in San Francisco is a relatively quiet yet picturesque part of town but on Monday, April 1, hundreds of Redis users also lovingly referred to as Redis Geeks, descended on the pier as part of Redisconf ‘19 and turned it into a vibrant venue of knowledge exchange. It was no April fools’ gag either because the conference officially started a day later. So what was going on?

At Redis, the home of Redis and the team responsible for the largest annual Redis conference, we call this Day 0. This is the day where Redis Geeks can take part in Redis training. This year, in addition to the Redis training track, hundreds of developers also signed up for two half-day sessions around how to use Redis in microservices by none other than Chris Richardson, a notable figure in Microservices universe. Unlike last year, Redisconf 19 also featured the Silent Disco party inspired headphones that enabled attendees to sit in a large room, while a number of parallel sessions took place on different topics.

### Day 1

The next day over 1,500 Redis Geeks took over the Pier and the day started with some significant announcements by Redis creator Salvatore Sanfilippo, the creator of Redis and Ofer Bengal and Yiftach Shoolman, the co-founders of Redis.

Salvatore talked about the next big Redis release 6.0 and offered a preview of what is to come around multi-threading and Access Control Lists (ACLs). When Ofer and Yiftach took the stage they announced a slew of announcements that firmly positioned Redis Enterprise as the first true [multi-model database](/multi-model/).

The first announcement was a new Redis module that turns Redis into a Time Series Database with built-in functionality to manage time-stamped data. You can learn more about RedisTimeSeries [here](/multi-model/time-series/).

The second announcement was around [RedisAI](/multi-model/ai/) that enables users to serve their existing AI models including TensorFlow models against data within Redis. With the introduction of the two new models, Redis Enterprise is now a true multi-model database with support for all major data models. However, a true multi-model database doesn’t just have a polyglot persistence strategy, it should also allow interoperability between different data models and this is exactly what Yiftach announced with [RedisGears](/redis-enterprise/technology/gears/), an in-database programmable framework that allows inter-model communication without the need for extracting and transforming data from different models.

Day 1 also included a fireside chat between Ofer Bengal, CEO of Redis with Google Cloud CEO Thomas Kurian around Redis and it’s popularity among developers.

Finally, the keynote included a discussion panel with Engineers from two gaming companies – Etermax and Scopely, who discussed the importance of Redis and speed of deployment to their platforms success in online gaming use cases.

### Day 2

Day 2 was all about partnerships and the day started with a talk by Martin Ford, an NYT futurist on AI and its effects on society followed by Ofer and Yiftach taking the stage to highlight the power of our ecosystem with many product-level integrations that enhance the Redis experience.

The first part of the keynote included partnerships around visualizations, a popular topic around all Redis users. Redis announced the acquisition of RDBTools, a GUI for Redis developed by HashedIn. [RDBTools](https://rdbtools.com/) will now be maintained as part of the Redis portfolio of products. The next set of announcements included using Grafana for TimeSeries with an interactive demo. Subsequently, the audience got to see some pretty cool collaborations and demo of how to visualize Streams with [Lenses.io](https://www.landoop.com/) and [Linkurious](https://linkurio.us/) for Graph data.

Probably one of the biggest announcements came right after when Yiftach announced General Availability of Redis Enterprise on Intel’s newly unveiled persistent memory technology – [Optane](/press/redis-enterprise-intel-optane-dc-persistent-memory-offers-cost-effective-scaling-petabytes/).

Ofer then [announced](/press/redis-labs-introduces-redisedge-lean-multi-model-database-edge-application/) the availability of [RedisEdge](/solutions/redisedge/) for IoT, a brand new solution that uses all of Redis’ multi-model capability to deliver sub-millisecond latency data processing on IoT devices.

The next part of the Day 2 Keynote included talks from Redis partners Microsoft and Google and the audience was treated with a demo of a Redis operator by Aparna Sinha, Group Product Manager of Kubernetes.

We had over 100 breakout sessions, with topics ranging from getting started with Redis to best practices for clustering, geo-replicated databases for DR using CRDT and using Redis as a primary datastore. These sessions were packed with information from many of our Redis experts and customers from Netflix, Fiserv, IBM, Twitch, Verizon, New Relic, Microsoft, Credit Karma, Kong and many more, briefly punctuated with lunch that was served in typical San Francisco style — food trucks.

The three packed days seemed to pass in a blink and as much fun as it was to hear all the speakers and the new product announcements, RedisConf 19 came to an end on Wednesday evening. As one of the fellow Redis Geeks, I am now looking forward to the next RedisConf and can’t wait to go through this all over again.

We know that this event wouldn’t be the success that it is without the support from our community, customers, and partners — so a big thank you goes out to everyone involved for innovating and growing with us. We sincerely hope you had as much a fun time attending this event, as we did hosting the event.

If you’d like to try out the latest modules and connect it all with RedisGears, head over [here](/redis-enterprise/software/downloads/#downloads) to download the Redis Enterprise 5.5 Preview Edition.
