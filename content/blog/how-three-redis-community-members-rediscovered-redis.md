---
title: "How Three Redis Community Members Rediscovered Redis"
linkTitle: "How Three Redis Community Members Rediscovered Redis"
url: "/blog/how-three-redis-community-members-rediscovered-redis/"
description: "We are constantly inspired by the creative and powerful ways the Redis community uses Redis to power innovative applications. In the premiere issue of Rediscover Magazine, we showcased a trio of..."
date: 2020-09-21
blogCategories:
- "Company"
authors:
- "Haley Kim"
lastmod: 2025-03-27
hidden: true
---

*By Haley Kim, Associate Content Producer · Published 21 September 2020 · updated 27 March 2025*

![Blog tile image](/images/blog/9522ab53c5d2ffa4c63de9c72e1d5aaf41370930-2550x1650.webp)

We are constantly inspired by the creative and powerful ways the Redis community uses Redis to power innovative applications. In the premiere issue of *Rediscover Magazine*, we showcased a trio of community members who have rediscovered Redis to help them conquer their data challenges.

Now, here’s your chance to get to know Carlos Justiniano, Matthew Goos, and Dan Pipe-Mazo a little better and learn how they use Redis in biotech, medtech, and robotics respectively.

## Carlos Justiniano

![](/images/blog/c5a78324f56ef34d8a9be90c271a6a38063f9968-846x846.webp)

Twitter: [@cjus](https://twitter.com/cjus)

GitHub: [@cjus](https://github.com/cjus)

Medium: [@cjus](https://medium.com/@cjus)

Veteran software developer Carlos Justiniano is Chief Technical Officer at [Skafos.ai](https://www.skafos.ai/). Previously he was Vice President of IoT and Cloud Platforms at Zenerchi (he’s still an advisor at the company), where his team used RedisGraph to power its BioGraph project, a navigable model of human physiology. He’s still new at Skafos, but has already proposed using RedisGraph and RedisAI to power its next-generation AI visual product search technologies. Carlos also wrote the [Hydra framework](https://www.hydramicroservice.com/), a Node.js package that leverages Redis to facilitate building distributed applications, including microservices architectures.

**Favorite Redis feature**: “My favorite feature of Redis has to be the ability to create a memory based key space, coupled with rich data structures.”

**RedisConf 2020 *****Takeaway***** session: **[**Creating a Model of Human Physiology using RedisGraph**](/redisconf/)

This was Carlos’ third RedisConf appearance, and his presentation focused on modeling human physiology with Internet of Things and wearable tech devices using RedisGraph. Watch him demonstrate how RedisGraph is powering Zenerchi’s biotech platform, which produces advanced 3D, VR, and AR visualizations.

[Click here to view video](https://www.youtube.com/embed/1SwDSm-tr-g)

## Matthew Goos

![](/images/blog/c8474213e4d510bc471fdbea292aa02c3d49fd65-960x960.webp)

Twitter: [@m4g005](https://twitter.com/m4g005)

LinkedIn: [@matthewgoos](https://www.linkedin.com/in/matthewgoos/)

Matthew Goos has more than 25 years of technology experience, and is the Co-Founder and CTO of [MDmetrix](https://www.adaptx.com/), an interactive data analytics platform that helps clinicians and institutions understand patterns in their data. MDmetrix built its Mission Control application to combat the spread of COVID-19 by providing analytics to institutions and physicians around the country to improve patient care and optimize utilization of resources. MDmetrix uses two Redis modules: [RedisJSON](/json/) for storing data on users and [RedisGraph](/modules/redis-graph/) for storing data for analysis.

**Favorite Redis feature**: “If you consider a module a feature, then our favorite thing is RedisGraph. It allows us to store our customer data flexibly so that our analytics engine can quickly process it.”

**RedisConf *****Takeaway***** 2020 interview: **[**Afternoon Keynote**](https://www.youtube.com/watch?v=WvjV3Hd06p4&t=1s)

Catch Matthew in conversation with Howard Ting, formerly CMO at Redis, as he explains more about how he and his team build Mission Control. MDmetrix was one of the winners of our [Rediscover Redis competition](/blog/meet-the-winners-of-the-rediscover-redis-competition/)!

[Click here to view video](https://www.youtube.com/embed/WvjV3Hd06p4)

## Dan Pipe-Mazo

![](/images/blog/e227f30714471983f6ed228aea2a29a18a7ed36b-933x1024.webp)

Twitter: [@dpipemazo](https://twitter.com/dpipemazo?lang=en)

GitHub: [@dpipemazo](https://github.com/dpipemazo)

LinkedIn: [@dpipemazo](https://www.linkedin.com/in/dpipemazo/)

Dan Pipe-Mazo is the CTO of [Elementary Robotics](https://elementaryml.com/), whose mission is to create more affordable and accessible robot assistants. Dan has spoken both at [Redis Day London 2018](/redisdays/) and [RedisConf 2019](/redisconf/) about [Atom](https://github.com/atom-robotics-lab), the [Redis Streams](https://redis.io/docs/manual/data-types/streams/)-based [microservice software](/solutions/microservices/) development kit that the robotic software stack is built on. Atom 2.0, currently released in beta, also uses RedisTimeSeries and Grafana. All Atom users get full dashboards and performance specs of all their microservices with zero additional work, for free. Elementary Robotics has been running 100% of its robotic data on Redis Streams for the last two years!

**Favorite Redis feature**: “Redis Streams are a game-changer in robotic software as the same action on the publisher side, (XADD), can be interacted with on the client side in either a typical Pub/Sub fashion (XREAD) or a last-value-cache fashion (XREVRANGE). This is perfect for robotics in which we have several high-frequency data inputs (motor position, temperature, etc.) being injected at very high frequencies (> 1kHz).”

**RedisConf *****Takeaway***** 2020 session: **[**Build a Message Bus with Redis Streams and FastAPI**](/redisconf/)

Learn how to build a message bus—a way for producers to communicate with receivers by adding messages to a persistent data structure—in this session with Kyle Bebak, Web Architect at Elementary Robotics. He demonstrates how you can do this with Redis Streams and FastAPI, a Python web framework.

[Click here to view video](https://www.youtube.com/embed/LHOjW42-A40)

*Read more about Carlos, Matthew, and Dan in *Rediscover Magazine*, available free (online and in print) at *[*Redis.com/rediscover-magazine*](/rediscover-magazine/)*. The premiere issue features more than a dozen stories on rediscovery, the power of data, real-time financial services, database trends, serving artificial intelligence, and managing remote workers, plus exclusive interviews with Redis creator Salvatore Sanfilippo and more tech leaders.*
