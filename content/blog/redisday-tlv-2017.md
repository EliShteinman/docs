---
title: "From Tel Aviv w/ <3: Redis Day TLV 2017"
linkTitle: "From Tel Aviv w/ <3: Redis Day TLV 2017"
url: "/blog/redisday-tlv-2017/"
description: "Last month, Redis geeks and geekettes received the perfect Valentine’s gift: a day packed with sessions about everyone’s favorite in-memory database. Sponsored by Redis and hosted at the Tel Aviv..."
date: 2017-03-06
blogCategories:
- "Company"
authors:
- "Itamar Haber"
lastmod: 2025-03-27
hidden: true
---

*By Itamar Haber, Technology Evangelist · Published 6 March 2017 · updated 27 March 2025*

![Blog tile image](/images/site-mirror/0073e867b4e64f59de9047fdcde04295ba647e5c-772x550.webp)

![](/images/site-mirror/d31b97ac0d40abb5a1f3fcee8efd0f262e8fd47c-870x300.webp)

Last month, Redis geeks and geekettes received the perfect Valentine’s gift: a day packed with sessions about everyone’s favorite in-memory database. Sponsored by Redis and hosted at the [Tel Aviv Talkhouse](https://www.talkhouse.co.il/), the event was a huge success, with over 200 attendees showing up and staying all the way until SHUTDOWN.

Footage of the [sessions and presentations](https://www.youtube.com/watch?v=NLRbq2FtcIk) is available so you can absorb everything that went on at your own leisure. There’s also a [Twitter moment](https://twitter.com/i/moments/831606477961961474) and a bunch of [photos here](https://drive.google.com/open?id=0B79TLsuJUpU4VnNUVV9VVW94U3c). For a recap, read on.

The day consisted of no less than thirteen sessions spanning a wide spectrum of topics and presented by Redis users and developers. We kicked off with a keynote by Redis’ creator and developer, [Salvatore antirez Sanfilippo](https://twitter.com/antirez), who was visiting our local offices that week. In his session, Salvatore shared some of his philosophy and the near future plans for Redis.

Next on stage was [Ishay Green](https://www.linkedin.com/in/ishaygreen), co-founder, and CTO at [Spot.IM](https://www.wearetv.com/), a company that uses Redis as its primary database and powers the real-time communication between millions of users across thousands of website. Ishay delivered his entire presentation without the use of slides and live-demoed everything–ballsy move!

Following Green was [Cihan Biyikoglu](https://twitter.com/cihangirb), our VP of Product Management, who presented the company’s roadmap. In his talk, titled “Redis for the Enterprise,” Cihan presented Redis’ vision for our product lines and demonstrated how the open-source and commercial offers complement each other and meld together. Then it was time for a coffee break.

We resumed the sessions with a brilliant presentation on Multi-Master Replication in Redis from the Redis Architect, Yossi Gottlieb. Over the last year, Yossi and the Redis Labbers have been implementing a new way for replicating Redis databases. This new mechanism leverages Redis modules and is based on Conflict-free Replicated Data Types (CRDTs) for consensus-free and strong eventual consistency replication. [Watch his presentation](https://www.youtube.com/watch?v=b5UTfy3ftzI&list=PL83Wfqi-zYZFM5tZgZp1Ee5uGenVM0_Qv&index=4) and prepare to have your mind blown to pieces and then put gently back together.

Back already? Good, because next on our agenda we had [Dvir Volk](https://twitter.com/dvirsky), Senior Architect at Redis, with a guided tour through the rapid rise of [Redis modules](/modules/get-started/): their conception, the modules’ API evolution, early iterations, the [full text search](/blog/adding-search-engine-redis-adventures-module-land/) module [RediSearch](/search/), a module for serving [machine learning](/blog/machine-learning-steroids-new-redis-ml-module/) models, and much more.

The last talk before lunch was given by [Eitan Shapiro](https://www.linkedin.com/in/eitan-shapiro-a078007/) of [Videocites](https://www.videocites.com/), a company that offers a SaaS platform that performs a video-by-video search online, enabling content owners to track and monetize their properties. The service relies on RediSearch for indexing and querying millions of fingerprinted videos in real time and at low cost.

Our afternoon track began with [Datorama](https://www.salesforce.com/products/marketing-cloud/marketing-intelligence/)‘s Udi Kidron, who recounted the company’s recent migration of its centralized datastore to Redis from Hazelcast. Such migrations are far from trivial, especially given the company’s focus on data analytics and the criticality of its datastores. But with the team’s remarkable ingenuity and the assistance of the Redis community, it appears that it was [pulled off expertly](https://engineering.datorama.com/moving-from-hazelcast-to-redis-b90a0769d1cb).

The next presentation was about [RedisGraph](/modules/redis-graph/), a module that implements a graph database and supports a subset of neo4j’s Cypher query language. The developer, [Roi Lipman](https://twitter.com/roilipman), started the project in his spare time and submitted it to [the first ever Redis Modules Hackathon](/blog/first-ever-redis-modules-hackathon/). He won a prize for it and we made him a job offer that he couldn’t (and didn’t) refuse.

[Eyal Altshuler](https://www.linkedin.com/in/eyal-altshuler-55137784) from [Stratoscale](https://www.stratoscale.com/) presented how the company’s core product, Symphony, can be used for deploying and managing Redis OSS clusters in the Hybrid cloud. The proprietary solution is not only offered to their customers, but the team is actually “dog-fooding” and uses Redis for managing the platform’s object store.

Adam Lev of Tamar Labs presented a use case in which Redis was key to scaling a “Big Data” application for stream processing. With 20M concurrent active user events and thousands of active sessions, it had to be fast.

Another Redis use case was delivered by [Omer Anson](https://www.linkedin.com/in/omer-anson-94096334/) of [Huawei](https://www.huawei.com/). In order to develop a distributed cloud network that is both open source and vendor-neutral, Huawei used Redis as the northbound database on each node of [Dragonflow](https://github.com/openstack-archive/dragonflow). The presentation also included several benchmark tests that demonstrated the configuration’s scalability.

The case study about [WeAreTV](https://www.wearetv.com/), a startup that connects the audience with TV shows in real time, was presented by [Nimrod Ticozner](https://www.linkedin.com/in/nimrod-ticozner-68533070/). Deployed on Google’s Cloud Platform, the company operates Redis clusters in multiple environments. These are used for tracking user sessions and maintaining various metrics’ counters.

You usually save the best for last, but in this case, all that was left was me. I took the stage and presented [WeAreTV](https://www.wearetv.com/), a module we’ve developed that provides a native JSON data type in Redis. I did a stupendous job developing it and delivering the preso, as usual, and upon ending I unlocked the doors and let everybody finally leave ;).

It was a marvelous day, and we’d like to thank everyone involved, both the amazing Redis community who attended in unprecedented numbers and the speakers who kept them glued to their seats. We’d also like to apologize to all the people who didn’t make it past the waiting list. We promise that next year it’ll be bigger and better (the event, not the waiting list)! Feel free to reach out to me with anything via [email](mailto:itamar@redis.com) or [Twitter](https://twitter.com/itamarhaber) – I’m highly-available!
