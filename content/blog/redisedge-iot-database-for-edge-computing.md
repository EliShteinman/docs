---
title: "RedisEdge: A Dedicated IoT Database for Edge Computing"
linkTitle: "RedisEdge: A Dedicated IoT Database for Edge Computing"
url: "/blog/redisedge-iot-database-for-edge-computing/"
description: "RedisEdge from Redis is a purpose-built, multi-model database for the demanding conditions at the Internet of Things (IoT) edge. It can ingest millions of writes per second with <1ms latency and a..."
date: 2020-04-29
blogCategories:
- "Uncategorized"
authors:
- "André Srinivasan"
lastmod: 2025-07-03
hidden: true
---

*By André Srinivasan, Solutions Architect · Published 29 April 2020 · updated 3 July 2025*

![Blog tile image](/images/site-mirror/438362d90c26e20f2a19776b45644c691fa1cecd-772x550.webp)

RedisEdge from Redis is a purpose-built, multi-model database for the demanding conditions at the Internet of Things (IoT) edge. It can ingest millions of writes per second with <1ms latency and a very small footprint (<5MB), so it easily resides in constrained compute environments. It can run on a variety of edge devices and sensors ranging from ARM32 to x64-based hardware. RedisEdge bundles open source Redis (version 5 with Redis Streams) with the RedisAI and RedisTimeSeries modules, along with RedisGears for inter-module communication.

![](/images/site-mirror/1faabfe7611f95c96d9ffa6994fbb1d7ca760033-1024x195.webp)

*To participate in the RedisEdge Preview Program, send an email to *[*RedisEdge@redis.com*](mailto:RedisEdge@redis.com).

## Unburden your application from the complexities of the IoT edge environment

Redis has partnered with the emerging leaders in the IoT edge platform space, [EdgeX Foundry](https://www.edgexfoundry.org/) and [Microsoft Azure IoT Edge,](https://azure.microsoft.com/en-us/services/iot-edge/) to bring RedisEdge to their users. EdgeX Foundry is a Linux Foundation project with more than 70 member companies. It provides an open source IoT edge platform designed to make it easy for anyone to develop IoT edge applications.

![](/images/site-mirror/f4aa63f4668a845e329e9d01cb6692c32cd9ed0a-1024x621.webp)

RedisEdge is also available as a module for Azure IoT Edge, making it easy for IoT application developers using Azure IoT services to leverage the power of Redis. Azure IoT Edge with RedisEdge helps businesses focus on insights instead of data management. Developers can configure and deploy their solutions via standard containers and monitor them from the cloud.

![](/images/site-mirror/08a1ef621814387a08a4021ae44120e8f2b1dd16-1500x1059.webp)

## A purpose-built database for the IoT edge

In the wild of the IoT edge environment, diverse conditions and requirements can tax any data services platform. Applications inevitably require multiple data models (e.g. time-series, graph) to support video streaming analytics, image recognition, and other complex computing requirements. RedisEdge is a multi-model database that handles various data models gracefully, removing the complexities of polyglot persistence architectures.

RedisEdge supports all 10 native Redis data structures, including the new Redis Streams data structure, providing ultimate flexibility and simplicity for application developers.

![](/images/site-mirror/91235eac1829caa376609104d28d0b36d392310b-1024x348.webp)

IoT edge application developers should not have to deal with the complexities of the IoT edge stack, such as messaging and networking protocols. With RedisEdge embedded in EdgeX Core Services and Azure IoT Edge platforms, developers can instead focus on their applications and business needs, and leave the data services and platform to us, partnered with the leading IoT edge platform providers.

## Related resources

- [4 Steps to Select the Right Database for Your IoT Solution](/docs/4-steps-select-right-database-iot-solution/)
- [Fog Computing and the need for RedisEdge](/blog/fog-computing-need-redisedge/)
