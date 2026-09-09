---
title: "Optimizing Pokémon GO: How a Redis Cluster on Google Cloud Improved Performance and Reliability During Raid Events"
linkTitle: "Optimizing Pokémon GO: How a Redis Cluster on Google Cloud Improved Performance and Reliability During Raid Events"
url: "/customers/niantic/"
description: "As thousands of Pokémon GO players participate in popular Raid Battles, Niantic’s Google Cloud servers had become bogged down during the preparation phase when people form and join teams, impacting..."
lastmod: 2025-09-12
hidden: true
---

*updated 12 September 2025*

###### Challenge

As thousands of Pokémon GO players participate in popular Raid Battles, Niantic’s Google Cloud servers had become bogged down during the preparation phase when people form and join teams, impacting latency. Niantic needed a fast, responsive database that scales quickly to accommodate surges in Pokémon GO activity.

###### Solution

To support heightened player activity, Niantic caches high volumes of game data in a Redis Enterprise cluster. All Pokémon GO servers can access this shared data, reducing latency and boosting performance for multi-player Raid events.

###### Benefits

Redis Enterprise requires much less overhead than disk-based database management systems, allowing Niantic to balance the server load and offer great player experiences. Average latency during the Raid preparation phase has dropped by 75 percent.

> "Redis is a leader in caching. High throughput, low latencies, and built-in analytics allow us to deliver rich gaming experiences to the Pokémon GO community."

Instant response times and ultra-fast performance are critical to enjoying a video game. Lag time is unacceptable even during peak periods, such as when players team up for the Raid Battles that have taken hold of the [Pokémon GO](https://pokemongolive.com/?hl=en) community.

In these battles, players join forces in a Pokémon gym to take on powerful and oftentimes rare Pokémon. Whenever players are in close proximity to a gym with an active Raid, they can join the Raid lobby to prepare for the upcoming battle.

While Pokémon GO users prepare for battle, [Niantic](https://nianticlabs.com/?hl=en)’s technology team—the game’s developer—must prepare for a massive surge in traffic on the servers that power these events. Pokémon GO operates in a multi-server environment. During normal gaming activity, players are evenly distributed across all servers. However, during Raids, players in the same gym need to be on the same server in order to access the game data stored in that server’s memory.

“Lots of data must be shared across the group of players,” explains Da Xing, staff software engineer at Niantic. “Once the group is formed, all the people on the group need to be moved to a server that can serve the group.”

Popular gyms attract more players, resulting in increased traffic to the servers hosting those gyms. In some cases, this can cause significant delays for players in the same Raid, as well as for those who are not in the Raid but are on the same server, eventually rendering the game unplayable. “No single server can handle that traffic load, which makes it difficult to provide a positive player experience,” Xing adds.

![Niantic Latency](/images/site-mirror/edfd62d6997371e815462caa1d57e259126a50a4-800x236.webp)

*The maximum recorded latency has decreased from over 1 second to approximately 250 milliseconds. Source: Niantic*

### Spawning a high-performance gaming environment

Initially, Niantic designed its Pokémon GO games around a stateful architecture, which made scaling and restarting servers difficult. Xing and other members of Niantic’s architecture team determined that if they could make the Pokémon GO servers stateless they would be able to scale up and down more quickly. “With the previous architecture, in order to scale a cluster, we have to cordon them one by one and wait for existing multiplayer sessions to expire,” he explains. “It can take as long as 30 minutes before we can restart our servers and add more players. Doing that for every server required higher operating costs.”

Niantic needed a data platform that is fast, responsive, and scales quickly to accommodate surges in Pokémon GO activity. Xing and his team selected [Redis Enterprise on Google Cloud](https://redis.io/cloud-partners/google/) because it enables low latency and high availability with zero-downtime scaling. Standard features include persistence, in-memory replication, instant failover, backups, and disaster recovery.

“Initially, we looked at in-memory solutions for our existing Google Cloud servers,” Xing continues. “However, Google Cloud Memorystore had drawbacks, and adding more Google Cloud servers to handle Raid groups is expensive. Adding Redis clusters is less expensive than deploying additional Google Cloud servers. We can deploy a large-scale cluster at a reasonable price.”

### Attacking latency challenges

In Niantic’s new Raid architecture, all servers in a game cluster can access the data stored in a centralized Redis cache—a temporary holding location for repeated access to the same information. There is no need for players in the same gym to be on the same server to access the shared data.

As players gather in a Raid lobby, Niantic records who has committed to each group, at what time, and how the players are related by previous social interactions. This is stored as JavaScript Object Notation (JSON) keys in Redis Enterprise, along with key timestamps. The cache also maintains data about the social features of each game, along with statistics about player locations, tendencies, and performance.

In-memory caching is a technique where frequently accessed data is stored in memory instead of being retrieved from disk or remote storage. This technique improves application performance by reducing the time needed to fetch data from storage devices. In the gaming industry, caching is an efficient way to serve content such as graphics, pictures, thumbnails, music, labels, metadata, and tags quickly and efficiently.

In-memory caching is perfect for the Pokémon GO Raid preparation phase because the real-time data exchanged between the client devices and the servers is only meaningful during the 10 or 15 minutes of the Raid play. “Once the gameplay is finished and the players are rewarded, the data expires,” says Xing. “There is no need for persistent data storage.”

This approach also ensures better economies of scale. Players can connect to any server, regardless of where a gym is hosted, allowing the servers to sustain higher query performance during popular Raid events.

“Moving Raid events to Redis Enterprise is much more efficient,” Xing sums up. “Redis Enterprise is very reliable and it has very fast read/write access. Furthermore, by breaking the data into multiple shards, multiple machines can process requests in a linear fashion.”

### Defending the player experience

Since deploying Redis Enterprise, server hot spots have been reduced significantly. The majority of servers host a relatively consistent volume of traffic during the Raid preparation phase. The maximum recorded latency has decreased from over 1 second to approximately 250 milliseconds—a 75 percent reduction.

Because the servers are more reliable, annoying delays and server “hiccups” during Raid events have been greatly reduced. Redis Enterprise provides a more stable experience during these events and saves operational and maintenance costs that can be invested in other areas to improve the overall gaming experience.

“With its exceptional caching capabilities, Redis Enterprise presented us with a high-performance, highly reliable, cost-effective alternative,” Xing concludes. “Redis is a leader in caching. High throughput, low latencies, and built-in analytics allow us to deliver rich gaming experiences to the Pokémon GO community.”
