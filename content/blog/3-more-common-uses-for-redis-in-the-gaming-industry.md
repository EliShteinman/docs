---
title: "3 (More) Common Uses for Redis in the Gaming Industry"
linkTitle: "3 (More) Common Uses for Redis in the Gaming Industry"
url: "/blog/3-more-common-uses-for-redis-in-the-gaming-industry/"
description: "At the Game Developers Conference (GDC) four months back, I had great discussions with game developers that use Redis – here’re my takes from that event. And this week, I was pleased to check out..."
date: 2014-08-14
blogCategories:
- "Tech"
authors:
- "Itamar Haber"
lastmod: 2025-03-27
hidden: true
mirrored: true
---

*By Itamar Haber, Technology Evangelist · Published 14 August 2014 · updated 27 March 2025*

![Blog tile image](/images/site-mirror/c29e76ba28eed51f582145f86d6591b3d1040412-300x200.webp)

At the [Game Developers Conference](https://www.gdconf.com/) (GDC) four months back, I had great discussions with game developers that use Redis – here’re [my takes](/blog/the-top-3-game-changing-redis-use-cases) from that event. And this week, I was pleased to check out [GDC Europe](https://www.gdceurope.com/) and at [Gamescom](https://www.gamescom.global/). While GDC’s European version is significantly smaller than its American equivalent, it was still a lot of fun meeting and conversing with developers. Gamescom is, well, gamescom (see photo of yours truly).

Interestingly, and similarly to my previous GDC experience, I found out about more common use cases for Redis. Leaderboards, sessions and profiles are naturally still the top functions for which game developers use Redis, but a few more kept popping up insistingly…

## Data Management

There are all kinds of games, and some of them use rely on data almost as extensively as they do on their code and media. Online, social and mobile games are perhaps most known for stringent latency and performance requirements when it comes to data management, and Redis is heavily used to fulfill these. One gaming developer I talked with uses Redis to cache Javascript snippets, which make up the entire game. I also heard that a well-known online gaming brand is using Redis to keep every real-time statistic and aggregate that it collects from each of its players in real time. I learned that another gaming service captures real-time in-game events using Redis – its raw event stream is used for dashboards and powering interactive customized campaigns, on top of being consumed by downstream processes for deeper analytics and long-term storage.

## Ad Networks

Whenever your free-but-ad-supported game presents you with a 15-second trailer, you can be almost certain that there’s a Redis server involved (and probably more than one). This “fact” is hardly surprising considering the volume of requests and tight latency budgets ad networks are working with/against. An ad server is all about speed, and Redis fits that bill perfectly. Counting impressions? Check. What about clicks? Of course. Need your campaign metrics snappy? Done. Want to keep your viewers’ segments handy? No problem. And these are just the basics of ad serving. More often than not, once Redis is a part of the ad network’s stack, it is put to extensive use to support the unique focus and strengths of each network.

## Customization

Redis can be extended via Lua scripts or, as an open source project, forked and modified freely. This flexibility and openness appeals to a lot of developers, but perhaps even more so to the creative members of the entertainment industry. Some developers I met had implemented the entire player matching mechanism of their multi-player online game using a clever combination of Lua scripts, sorted sets and lists. I found out another game’s servers are using a modified fork that includes “optimizations to almost all commands to better fit our use cases” (stay tuned for more on that – I’m hoping to get more details). I also got a tip about a persistence to Big Data store patch that is supposed to be open sourced in the near future.

It is really amazing to see Redis all over the place, but personally I think the fact it is used so extensively with games is awesome. I really need to get into my Bowser costume now, but feel free to [email](mailto:itamar@redis.com) or [tweet](https://twitter.com/itamarhaber) me – I’m highly available 🙂
