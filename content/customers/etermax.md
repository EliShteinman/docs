---
title: "Etermax reduced AWS infrastructure costs by 30%"
linkTitle: "Etermax reduced AWS infrastructure costs by 30%"
url: "/customers/etermax/"
description: "As Etermax watched its customer base rise by two-to-three million new users every week with no end in sight, it knew it was fast approaching the limits of its open source Redis installation. Facing..."
group: "Gaming"
lastmod: 2025-09-12
hidden: true
mirrored: true
---

*updated 12 September 2025*

###### The Challenge

As Etermax watched its customer base rise by two-to-three million new users every week with no end in sight, it knew it was fast approaching the limits of its open source Redis installation. Facing CPU and memory bottlenecks, lack of scalability, and prohibitive costs in its existing database configuration, a database upgrade was sorely needed.

###### Solution

Redis Cloud’s auto-sharding and auto-scaling capabilities, along with its ability to run multiple Redis instances on the same server, allowed Etermax to maximize the throughput of its servers while minimizing costs.

###### Benefits

Redis Cloud was not only able to meet high availability and performance demands, it also helped cut Etermax’s AWS infrastructure costs by 30%.

> “In some cases, we were even getting to 95% CPU utilization. It would have been impossible to scale to 25 million daily users with any solution other than Redis Cloud.”

Nothing ticks off gamers more than a game that lags and introduces delays. But avoiding performance issues becomes even more difficult when a game is flooded with new users. In late 2014, Etermax’s online Trivia Crack game went viral. As the gaming company watched its customer base rise by two to three million new users every week, it knew it was fast approaching the limits of its open source Redis installation.

“We were hitting physical limits with our existing Redis installation,” says Etermax’s former CTO Gonzalo Garcia. “CPU bottlenecks were unavoidable with single-threaded Redis and even the largest AWS instances couldn’t utilize all the cores.”

Memory bottlenecks were an issue as well. The company’s pre-sharded solution maxed out at 16 endpoints of 244GB, which limited its ability to scale. And maintaining a completely redundant infrastructure for high availability was far too costly under the current configuration. It was clear Etermax needed a new solution.

### Redis Cloud changes the game

At around 10 million users, Etermax reached out to Redis for help. With Redis Cloud deployed in the company’s virtual private cloud, Etermax was able to scale without any downtime or performance impact, even as users peaked to an eye-popping 25 million per day. Redis Cloud’s auto-sharding and auto-scaling capabilities, along with its ability to run multiple Redis instances on the same server, allowed Etermax to maximize the throughput of its servers while minimizing costs—the company cut its AWS infrastructure costs by 30%.

“In some cases, we were even getting to 95% CPU utilization,” Garcia says. “It would have been impossible to scale to 25 million daily users with any solution other than Redis Cloud.”

Additionally, Redis Cloud’s in-memory replication and auto-failover features solved Etermax’s availability issues. The company, which had been performing just one backup per day due to the prohibitive costs of standing up fully redundant infrastructure, was able to dramatically improve reliability for its users without adding expensive hardware.

In addition to using Redis as a persistent database, the gaming company leverages Redis’ many features and data types for advanced functionality throughout its gaming operations, including:

- Session and device management
- Password authentication
- Caching for queries that run slow
- Expiration of game state once game ends
- User and game information indexing, such as all the questions a user has answered and all players a user has played against (stored as hashes)
- Real-time personalization in deciding which questions to serve up next based on user preferences and behavior
- Data processing that turns user preferences and behavior into business metrics for analysis by developers
- Game expiration notifications
- Username searches

### Future fine-tuning

“The move to Redis Cloud allowed us to concentrate on quickly adding features and growing our network in order to keep pace with the incredible user ramp up our games were experiencing,” Garcia says. “Once we’ve reached a stable state, we look to fine tune our deployment to gain even more efficiency and performance.”

To that end, one feature of a fully-managed, enterprise-grade Redis that Etermax explored is its built-in integration with Flash storage. By storing inactive user data on cost- effective Flash-based SSDs rather than more expensive RAM, Etermax can continue to reduce its applications’ operational costs—it’s expecting to reduce its AWS infrastructure costs by 70%—without compromising responsiveness.
