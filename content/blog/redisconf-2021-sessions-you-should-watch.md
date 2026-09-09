---
title: "Here’s Which RedisConf 2021 Sessions You Should Watch"
linkTitle: "Here’s Which RedisConf 2021 Sessions You Should Watch"
url: "/blog/redisconf-2021-sessions-you-should-watch/"
description: "Every year the Redis community gathers for RedisConf, and this year was all about rediscovering the power of real-time data. More than 12,000 developers, architects, and business and technology..."
date: 2021-05-27
blogCategories:
- "Company"
authors:
- "Udi Gotlieb"
lastmod: 2025-03-27
hidden: true
---

*By Udi Gotlieb, Head of Redis Enterprise Product Marketing · Published 27 May 2021 · updated 27 March 2025*

![Blog tile image](/images/blog/c87f7c1acbbd04a1e2a0eaeee8e55b8b822f7b89-772x550.webp)

Every year the Redis community gathers for [RedisConf](https://redisconf.com/redisconf21/modules/83000/html&sa=D&source=editors&ust=1622137732959000&usg=AOvVaw24VAQSq47PsGeLNtWE5n70), and this year was all about rediscovering the power of real-time data. More than 12,000 developers, architects, and business and technology leaders from 122 countries registered for live keynotes, fireside chats, and 60+ breakout sessions. As of May 20, all RedisConf 2021 sessions can be viewed on our [YouTube](https://www.youtube.com/channel/UCD78lHSwYqMlyetR0_P4Vig&sa=D&source=editors&ust=1622137732960000&usg=AOvVaw3fRnAllX3vr6TfBGfQtUU7) channel!

With many sessions covering unique use cases, we took a vote and compiled the top breakout sessions for 10 different superlatives. Here are the winners:

## Most Entertaining Speaker(s)

[Watch the video](https://www.youtube.com/watch?v=mfahK1qHRhk)

The SitePro duo of CEO Aaron Phillips and Director of Technology Dustin Brown elicit great chemistry and infectious enthusiasm to detail how the company’s mission-critical IoT platform uses the RedisTimeSeries module in Azure to ensure congestion-free data flow. Aaron and Dustin begin the session discussing SitePro’s inception as an end-to-end metering system for oil and gas companies. They explain how the company started leveraging RedisTimeSeries after significant growth to give “historical context to real-time data.”

The session never gets boring, as Aaron and Dustin play off each other’s points, add familial metaphors for context, and explain the tooling and features utilized with RedisTimeSeries. Give this session a look for some laughter and to learn how RedisTimeSeries can empower real-time and historical data at scale.

## Best Slides

[Watch the video](https://www.youtube.com/watch?v=wK9UzZRBvFo)

Chris Oyler’s presentation slides go hand-in-hand with his humor and ability to visually showcase real-time event capture at scale. Less than 30 seconds into the presentation, Chris casually alludes to his startup, UserLeap, to a circus and himself to a clown. He keeps a calm, casual demeanor throughout, even while his slides transition from graphics of the UserLeap API to a picture of Sesame Street (which represents the anatomy of an event).

But even while his session is hilarious, what stands out is his ability to maintain focus on the topic at hand. He details how UserLeap did not have a need for a relational database, yet needed high-write and high-read throughput—compelling the company to go with Redis Cluster and utilize HA mode with auto-failover. Later in the session, Chris shows a two-day graph comparison of UserLeap’s average latency, noting that there was an average positive change of about 100 milliseconds in response time after his company adopted Redis. Chris’ ability to relate the visuals in his slides to his presentation—and maintain a sense of humor—makes this session a winner.

## Best Newcomer

[Watch the video](https://www.youtube.com/watch?v=MyHyoUlbLuI)

Masoud Koleini is not at all new to the IoT world, but he does take home the panel’s Best Newcomer award for his premiere RedisConf 2021 breakout session, High-performance edge inference with RedisAI. As data analysis on the edge continues to grow across industries, Masoud highlights the challenges of running applications on devices with limited computational power. He then details why Redis was chosen—because its low memory footprint enables machine learning applications to run on small devices.

His breakout session is a case study on edge inferencing, with an explanation of how RedisAI’s deep inference capabilities help analyze tensor data, as well as best practices when running the RedisAI module on Arm machines. If you are curious to how RedisAI can run deep learning data inference on your machine learning application, give this video a view.

## Most Approachable to Redis Beginners

[Watch the video](https://www.youtube.com/watch?v=BHR_mvafOEc)

Eric Brandes wins this award for his 20-minute walkthrough of addressing the common misconception that Redis cannot be a primary database. He gives a MythBusters-like presentation, explaining his firsthand experience in building a user-monitoring performance tool, Request Metrics, with Redis as the platform’s primary database. He then addresses the reasoning behind choosing Redis, like its low operational complexity, ability to use simplified architecture, low cost, and flexibility with durability requirements.

In a small window of time, Eric does a tremendous job guiding you through the nuts and bolts of his developer operations, from explaining Request Metrics’ operational setup to its scaling strategy. If you are a newcomer to Redis and are deciding how to implement the NoSQL database into your tech stack, take the time to watch Crazy like a fox: Redis as your primary database.

## Most Engaging for Redis Experts

[Watch the video](https://www.youtube.com/watch?v=tGXX89GYK4o)

This is a session to watch if you have a strong background using Redis. In this breakout session, Jim Brunner explores interesting and recurring issues that come with using Amazon ElastiCache for Redis. As a developer on the ElastiCache team, Brunner has worked exclusively on Redis internal development for the Amazon platform. He dives into developer nightmares like maxmemory overuse, unparamaterized LUA, and the connection storm while breaking down methods to avoid them.

Jim approaches each topic in a systematic way, addressing the subject of each use case, the scenario that occurs, the outcome, and lastly, the solution to mitigate the problem. While these use cases are in the “extreme,” this session is a useful asset for developers who want to mitigate potential issues with their cache.

## Best Redis at Scale Story

[Watch the video](https://www.youtube.com/watch?v=kN4RpZosa-M)

Digital transformation has become a critical focus area for banks to provide a successful user experience. Adi Shtatfeld of Redis introduces Bank Hapoalim’s Dani Sela and Yaniv Yair to deliver a firsthand look at how Redis Enterprise improved availability and customer satisfaction for the largest bank in Israel.

With more than million customers while earning $14 billion in revenue each year, Bank Hapoalim was hit with a pandemic reality—it realized it needed to configure its banking infrastructure to cope with the digital demands of its customers. The massive number of requests on Bank Hapoalim’s website and mobile app began to create server overloads on their MF backend systems, causing slower latency times as well as timeouts for customers. To accommodate its infrastructure, Bank Hapoalim turned to Redis Enterprise caching to decrease requests to the bank’s mainframe and relieve the resource shortage—in turn saving mass expenses.

## Best Redis Modules Story

[Watch the video](https://www.youtube.com/watch?v=-djLz8HgM-Q)

SmartSim is a library dedicated to accelerating the convergence of AI, analytics, and data science with numerical simulation models. The data science libraries and simulations were not originally connected and did not traditionally communicate with one another in real-time.

Simulations would take time, ranging from hours to weeks, to fully compute and be completed, while the data library could only be analyzed after the simulation’s completion. Using RedisAI, SmartSim can now interact with simulations at runtime with fast, in-memory storage at scale. The module also enabled online inference, training, and analysis of SmartSim’s simulations without using the filesystem and while allowing the team to view data **online**. View this session to see a highly granular presentation of leveraging RedisAI.

## Best AI Story

[Watch the video](https://www.youtube.com/watch?v=2Fr2enOwTdU)

With more than 40 machine learning models and an application that makes two million predictions per second, DoorDash takes home the prize for Best AI Story. ML Platform Engineer Arbaz Khan and Technical Lead Manager Zohaib Hassan explain how the company uses Redis as a scalable feature store to provide a batch of input variables for making real-time predictions. Compared to a disk-based database, Redis is able to provide a cheap, fast, and simple in-memory data store to limit storage overhead and provide data locality for DoorDash.

This session takes home this superlative category because of how in-depth the presenters explain their company’s use case of Redis. They pinpoint their reasoning behind choosing Redis to scale ML operations, supplement their decisions with visuals and data results, and discuss the next steps of this ongoing project. Watch this breakout session to understand how Redis can fit in as a scalable feature store for machine learning platforms.

## Most Likely to Survive an Apocalypse with Just Redis

[Watch the video](https://www.youtube.com/watch?v=sSFSuEVLNxE)

When Doomsday is on the horizon—whenever that may be—you’d want knowledge from experts in multiple fields, right? With that in mind, this superlative goes to Ayaka Shinozaki of Techspert.io for her session Building a knowledge graph using RedisGraph. Techspert.io is a startup that uses AI-driven search technology to match world-leading experts with organizations in need of their specialist insight. Compiling billions of publicly available data points across the internet, Techspert.io needed a database solution to record relationships between experts, institutions, and semantic concepts—and then give a real-time overview of the knowledge landscape. That’s where RedisGraph came in.

RedisGraph enables Techspert.io to connect facts such as location, field of expertise, and name with one another to create a defined relationship. Utilizing vertices and edges to represent facts, Techspert.io uses RedisGraph’s cost-effective full-text search querying to extract information about relationships through the knowledge graph. This breakout session is a must-see for developers wanting to create a knowledge graph database, as well as for developers seeking insight to prepare for a pending apocalypse.

## Best I-Can’t-Believe-You’re-Using-Redis-For-THAT Story

[Watch the video](https://www.youtube.com/watch?v=ZrTdDD2T7-k)

Redis has plenty of use cases, but our team crowned Dr. Alexander Mikhalev’s session, Using the Redis ecosystem to build NLP-based services, for its uniqueness and creativity. Dr. Alexander began building a natural language processing product during the RedisConf 2020 hackathon to help medical professionals navigate through medical literature. He envisioned creating a question answering system, or a chatbot, through machine learning, yet it had to be fast enough to exceed user expectations while also being highly available. Dr. Alexander realized he needed to build a knowledge graph that could pinpoint long, complex queries and a powerful engine to process fast API response times—so he developed a NLP pipeline with RedisGears, RedisAI, and RedisGraph all embedded into its core.

This breakout session clearly outlines the product’s API framework and how each module is configured, giving the viewer a thorough presentation into the interconnectedness of Redis modules. Watch this RedisConf 2021 session for inspiration on how Redis can help you create an application with innovation at its heart.

*These RedisConf 2021 sessions caught our eye, but there are many more to choose from on the platform. If you watched a session that helped you rediscover the power of real-time data, feel free to share with us on *[*Twitter*](https://twitter.com/Redis&sa=D&source=editors&ust=1622137732981000&usg=AOvVaw2mJQwE6rgkftsmipx4fwXQ)* with the hashtag #RedisConf2021 or join our *[*Redis Discord server*](https://www.google.com/url?q=/community/&sa=D&source=editors&ust=1622137732981000&usg=AOvVaw1sMocZAb0yiBMM2DJ1skr6)* for further community support.*
