---
title: "Redis Enterprise on AWS serves as Swiss Army knife for fast-growing platform’s data layer needs"
linkTitle: "Redis Enterprise on AWS serves as Swiss Army knife for fast-growing platform’s data layer needs"
url: "/customers/hackerrank/"
description: "HackerRank’s mission is to become the single source of truth for every engineer’s technical ability, so it needed a fast, scalable, and reliable data platform that didn’t require a lot of..."
lastmod: 2026-09-01
hidden: true
---

*updated 1 September 2026*

###### Challenge

HackerRank’s mission is to become the single source of truth for every engineer’s technical ability, so it needed a fast, scalable, and reliable data platform that didn’t require a lot of maintenance and configuration in order to focus on innovation. In addition, HackerRank needed a real-time leaderboard to showcase top developers.

###### Solution

HackerRank was using multiple solutions to cobble together a data layer, but Redis Cloud let the team consolidate on a unified data platform that suited all its use cases. For large-scale recruiting events where 20,000+ developers take coding tests at the same time, Redis Cloud handles everything with ease. And Redis Cloud’s in-memory performance keeps real-time standings no matter how many developers are taking tests simultaneously.

###### Benefits

Adopting Redis Cloud gave the HackerRank team all the tools it needs to scale as its platform grows. The DevOps team can now focus on developing features to help HackerRank stand out from its competition instead of maintenance and configuration.

> "With such a small core team focused on innovation, we want to pick partners and services that we don’t have to manage. We want them fully managed to the level of quality that we care about."

HackerRank is the industry leader in pre-screening, technical assessments, and remote interview solutions for hiring developers. The platform has more than 11 million developers, who use it to practice coding skills, prepare for job interviews, and get hired.

HackerRank’s overarching goal is to become the single source of truth for every engineer’s technical ability. Every day, more than 70,000 candidates compete in code competitions and are subsequently ranked on the company’s public, global leaderboard. The leaderboard is one of the most heavily used components in HackerRank’s system, and must perform under significant stress during peak times, from large coding events to surges in company recruiting.

### Redis Cloud fuels the HackerRank data layer

HackerRank was using multiple solutions to cobble together a data layer, but the small DevOps team knew that as the company grew it needed innovation that could move the needle towards HackerRank’s mission. It was looking for a fast, scalable, and reliable data platform that didn’t require a lot of time on maintenance and configuration, along with a superb real-time leaderboard to showcase top developers.

“With such a small core team focused on innovation, we want to pick partners and services that we don’t have to manage. We want them fully managed to the level of quality that we care about,” says Swapnil Talekar, Engineering Manager at HackerRank.

Redis Cloud consolidated all HackerRank’s solutions on a unified data platform that suited all of the company’s use cases. HackerRank developed its backend infrastructure with as low latency as possible, using Redis Cloud to build not only its caching layer but also its database for all of its real-time use cases. For code compilation and execution, HackerRank leverages the [RedisJSON module](https://redis.io/json/) to provide live execution status, reducing latency and providing real-time updates to users.

### Real-time leaderboards for developers is the lifeblood of HackerRank

HackerRank also uses the [RedisBloom module](https://redis.io/probabilistic/) to implement key aspects of its global leaderboard. HackerRank gets tens of thousands of submissions every minute—in order for the global leaderboard to keep up with the correct rankings, it needs an extremely scalable solution. Redis Enterprise, along with the RedisBloom module, allows the team to handle everything with ease.

### Key benefits of adopting Redis Cloud

Adopting Redis Cloud allows the HackerRank team to easily grow its platform to handle future growth. Redis Cloud takes the burden of maintenance and configuration off HackerRank’s DevOps team, who no longer needs to worry about availability and latency for its real-time leaderboard standings, even during large-scale recruiting events. Instead, the team can now focus on innovation as it develops competitive differentiators for HackerRank—working toward the company’s goal of becoming the single source of truth for every engineer’s technical ability.
