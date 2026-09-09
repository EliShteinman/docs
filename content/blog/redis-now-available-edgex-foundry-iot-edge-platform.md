---
title: "Redis Now Available for the EdgeX Foundry IoT Edge Platform"
linkTitle: "Redis Now Available for the EdgeX Foundry IoT Edge Platform"
url: "/blog/redis-now-available-edgex-foundry-iot-edge-platform/"
description: "I’m thrilled to share that Redis is now available as an embedded data service for the EdgeX Foundry IoT Edge Platform. By leveraging Redis, the EdgeX Core Services delivers an exceptional..."
date: 2018-12-13
blogCategories:
- "Announcements"
- "New Product Announcements"
- "Product Releases"
authors:
- "André Srinivasan"
lastmod: 2025-03-27
hidden: true
---

*By André Srinivasan, Solutions Architect · Published 13 December 2018 · updated 27 March 2025*

![Blog tile image](/images/blog/0073e867b4e64f59de9047fdcde04295ba647e5c-772x550.webp)

I’m thrilled to share that [Redis](https://redis.io/) is now available as an embedded data service for the [EdgeX Foundry](https://www.edgexfoundry.org/) IoT Edge Platform. By leveraging Redis, the EdgeX Core Services delivers an exceptional performance, a small runtime footprint and the ability to ingest millions of device events at the IoT edge with <1ms latency to IoT solutions. The combination of EdgeX and Redis has been optimized to live on fog nodes, edge gateway devices and even IoT devices in some cases. Redis’ blazing fast performance and small memory footprint (<5MB) enables data analytics to be closer to the source and respond faster to real-time business needs.

In the wild of the IoT edge space, there are many diverse conditions and requirements that will tax any database trying to provide necessary data services. These conditions will inevitably require the use of multiple data models, as well as edge computing involving deep learning, image recognition and other complex computing requirements. As a multi-model database, Redis has the ability to handle these various data models gracefully, removing the complexities of an architecture with polyglot persistence.

EdgeX with the Redis open source database is available immediately under the 3-Clause BSD license.

### Introducing RedisEdge

In tandem with our partnership with EdgeX, Redis is introducing a new commercial product called [RedisEdge](/redis-enterprise/more/redis-edge/), a database built specifically to address the demanding conditions at the IoT edge. RedisEdge is a commercial product, fully compatible with Redis Enterprise, which makes it ideally suited to extend to a clustered Redis Enterprise in the cloud for IoT solutions that require a hybrid edge and cloud architecture.

We are in the early stages of a disruptive trend, with virtually all major cloud and technology players making large bets on IoT and edge computing. This is the fourth wave of computing over the past 50 years: Mainframe → Client/Server → Cloud → Edge. It is anticipated edge computing will accelerate over the next decade as many compute models transition from cloud computing to a hybrid edge/cloud architecture to optimize the latency, bandwidth, security and locality needs of IoT applications. Gartner projects that by 2020, processing and analytics for industrial IoT use cases will increase from <10% to 60% at the IoT edge. Redis partners like Microsoft Azure and EdgeX Foundry — which already incorporate RedisEdge and Redis into their IoT edge platforms — are ahead of the game and are therefore ready for this massive ground shift toward edge computing.

IoT edge application developers should not have to deal with the complexities of the IoT edge stack, including messaging and networking protocols. With RedisEdge, application developers can focus on their applications and business needs; Redis will take care of the rest.

Read more about bringing cloud principals to the edge [here](/blog/fog-computing-need-redisedge/).
