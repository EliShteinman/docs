---
title: "MrQ scales personalized gaming experiences with Redis Cloud"
linkTitle: "MrQ scales personalized gaming experiences with Redis Cloud"
url: "/customers/mrq/"
description: "For MrQ, a smooth player experience isn’t just about speed—it’s about personalization. Every promotion, game, and feature aims to feel as if it was built for each player. Achieving that level of..."
lastmod: 2026-02-12
hidden: true
---

*updated 12 February 2026*

### Building unique, personalized player journeys

For MrQ, a smooth player experience isn’t just about speed—it’s about personalization. Every promotion, game, and feature aims to feel as if it was built for each player. Achieving that level of detail requires processing high volumes of real-time data across multiple systems without losing performance.

“We want to offer players an experience where they feel in control and that the experience has been handcrafted for them,” said Iulian Dafinoiu, Chief Technology Officer at MrQ. “You’re wondering: how on earth do they know so much about you, what you like, and what you don’t like… That’s nirvana for us.”

The Goosicorn team strives to replicate the feel of an in-person casino, where nothing gets between what players want to do and how they want to play. Even latency in something as simple as logging in or spinning a slot can break immersion. As the player base grew, system load surged, with traffic sometimes spiking up to 300-400x during promotional campaigns.

### Scaling throughput from hundreds to thousands of transactions per second (TPS)

MrQ’s JVM-based Kotlin platform runs on AWS with MongoDB Atlas as its database and Apache Kafka streams for WebSocket message distribution. Fetching data directly from the database and streaming it through Kafka created overhead across microservices. The team needed a distributed cache to reduce communication between services and deliver faster responses.

After testing Valkey, Memcached, and Amazon ElastiCache, the team chose Redis Cloud for its performance, reliability, and simplicity. Features like sorted sets for leaderboards and Pub/Sub for messaging proved ideal for gaming workloads.

Following migration to Redis, throughput jumped from roughly 200 TPS to more than 5,000—a 20x increase that showed Redis could scale easily. Redis Cloud kept performance high even under heavy load, reducing Kafka bottlenecks and simplifying architecture.

One critical improvement came from handling live player connections. Goosicorn games rely on WebSockets, and Redis Pub/Sub enabled the team to architect a simpler, more scalable solution. Nodes could be scaled horizontally without additional overhead, and messages could be published to players from any part of the system.

At the same time, Redis minimized unnecessary interservice communication: game configurations and player session details could be accessed directly from cache instead of calling separate services or streaming through Kafka. With Redis, the process is abstracted away: the team simply publishes to the right channel and trusts Redis to deliver instantly and reliably. Internal traffic reduced dramatically, freeing the system from bottlenecks in Kafka streams and improving overall responsiveness.

“Apart from the amazing performance of Redis as a distributed cache and the simplicity of use, you can do amazing things with it,” said Diego Marzo, Software Architect at MrQ. “The fact we were able to develop a new version of our communication layer, using Redis underneath to be able to send messages to the players and broadcast data to them in a transparent way, it is simply amazing.”

Cost efficiency also helped seal the deal. Competing solutions required heavier management and higher costs, while Redis Cloud offered performance, elasticity, and affordability that enabled the team to focus on gameplay innovation.

> Fundamentally Redis ticked all the boxes. It provides all that we need in a very cost effective and simple way. Tooling like the Redis Cloud console and Redis Insight make the investigation of any kind of issue very intuitive, which is very valuable for us.

### Handling burst traffic with ease

Promotions often caused traffic surges of 30–50x within minutes, with tens of thousands of players logging in simultaneously. Redis Cloud gave the team confidence their system could handle spikes without latency or failures. Its bursting capabilities allowed capacity to scale up on demand and back down afterward, keeping infrastructure costs in check.

The first time MrQ ran its flagship campaign, The Big Weekender, the system struggled with the surge. With Redis Cloud, Marzo and software engineer Tom Bullock rebuilt the architecture in weeks instead of months and launched the next campaign at full speed.

“Diego and I aren’t infrastructure guys. If we had any solution that we had to manage ourselves, we would have to be moving all these over and juggling all those, but the Redis Cloud solution meant […] [Redis] would be more than willing to handle that spike of traffic,” said Bullock. “Then if needed, we can easily click a few buttons and increase what we’re paying for in terms of load, but then also decrease it afterwards. The bursting capability was one of the massive selling points.”

Redis Cloud’s burst feature lets Goosicorn run clusters at a lower baseline cost—tuned for 99% of expected traffic without overprovisioning. When load spikes, Redis automatically absorbs it and scales back down afterward. The result is consistent performance and predictable costs.

> A good part of why they were able to turn it around is because of Redis. They were able to leverage a managed solution, we didn’t have to mess around with things that we didn’t need to do. I even remember [Bullock] bragging about deleting how many files and thousands of lines of code to simplify everything and turn this around in such a quick time. To me that was the best outcome. [...] Redis Cloud empowered that.

### Faster debugging and iteration with Redis Insight

Performance wasn’t the only gain. Redis Insight, a free tool that helps devs visualize, debug, and optimize data in Redis, became a key part of the workflow. The team could see what was cached, monitor live traffic, and inspect Pub/Sub channels in real time.

“We really like it and we believe it’s very useful,” said Marzo. “First because you can have access to the caches; you can see real-time what is cached and what is not. You can see all the traffic, how many keys you are inputting, and all of that. Apart from that, the Pub/Sub monitor is really important–especially in development time. When we are developing something, you are able to see what’s going on, what is coming, and what is going out very easily and nicely.”

Redis Insight also accelerated development of multiplayer features. For example, the racing game engine runs on a single node to ensure consistency in generating random events. Using Redis Pub/Sub, that node broadcasts state changes like player positions or results to other nodes, which then update players in real time through WebSockets. Previously, with Kafka-based communication, the team had to push these updates through multiple services, consuming and redistributing messages via WebSockets. With Redis Insight, the team could observe those messages as they happened and confirm the system worked exactly as intended.

Debugging and iterating was faster too. Developers could filter, search, and group keys, then make live edits to values and see immediate results. They were also able to manage their key values more easily with formatters that made their data more readable and accessible. This meant faster testing of configurations and less time wasted redeploying services.

During stress tests, Redis Insight helped confirm Redis Cloud maintained low latency even as traffic surged. Ahead of a campaign expected to generate massive spikes in player traffic, the team used Redis Insight to monitor throughput and latency under load, ensuring response times stayed low even as volume climbed. This investigation helped confirm Redis Cloud could handle real-world demand without slowing down or dropping requests.

> Even though we're backend developers and we're always in the code doesn't mean we don't love a good UI. Redis Insight—it just works.

### A faster, smarter architecture for modern gaming

With Redis at the core of its architecture, MrQ can now store and serve the real-time player data that powers its personalization strategy. From tailored promotions to frictionless gameplay, Redis provides the low-latency, high-throughput foundation for handcrafted experiences.

Looking ahead, MrQ plans to expand Redis Cloud across other platform components, including leaderboards and features that currently rely on local Redis instances.

“We can see the added value of Redis Cloud, and we want to take advantage,” said Marzo.

The combination of Redis Cloud’s performance and Redis Insight’s visibility gives MrQ the confidence to innovate faster, support more players, and stay ahead in a competitive market.

“Not only are we confident internally now that we won’t have players complain about technical limitations on our side—they’re going to have that seamless experience,” said Bullock. “Although Diego and I did put a lot of effort into this, I think it would have been completely worthless if we didn’t have Redis come along and take up a lot of the heavy lifting for us.”
