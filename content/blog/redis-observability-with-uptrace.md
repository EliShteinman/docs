---
title: "Enhancing Redis Observability with Uptrace"
linkTitle: "Enhancing Redis Observability with Uptrace"
url: "/blog/redis-observability-with-uptrace/"
description: "Everyone needs a way to monitor server behavior, if only to confirm that the system is running to spec. Several Application Performance Monitoring (APM) tools work with Redis, but perhaps you..."
date: 2023-07-19
blogCategories:
- "Uncategorized"
authors:
- "Talon Miller"
lastmod: 2025-03-27
hidden: true
---

*By Talon Miller, Principal Technical Marketer · Published 19 July 2023 · updated 27 March 2025*

![Blog tile image](/images/site-mirror/1336062e0885a89aab31d2517222f67e6debad0f-772x550.webp)

**Everyone needs a way to monitor server behavior, if only to confirm that the system is running to spec. Several Application Performance Monitoring (APM) tools work with Redis, but perhaps you haven’t heard of Uptrace. Let me tell you about it.**

Uptrace is an OpenTelemetry-based observability platform that helps developers and Ops users monitor and optimize complex distributed systems. It’s an open-source APM tool that supports distributed tracing, metrics, and logs. Automatic alerts for critical infrastructure can be sent via email, Slack, Telegram, and other notification channels.

Uptrace is a great platform for monitoring Redis that you should know about. Let’s dive in.

## Redis, observed differently

Uptrace is an [open source APM](https://uptrace.dev/get/open-source-apm.html) available both as an open-source version and an enterprise cloud version; the latter has more features and support options. The open-source version is quite robust as it has Prometheus remote write, AWS CloudWatch, vector logs, percentiles, and alerting, to name just a few examples. To evaluate its use with Redis, we set up open-source deployments of Uptrace and also tested the enterprise edition, called Uptrace Cloud.

Its UI looks amazing, and it genuinely is easy to navigate.

![Uptrace overview](/images/site-mirror/1faee2f1f6320b68a666a36ce0a0fa62e3b5517c-1000x467.webp)

*Uptrace overview*

You can connect to multiple databases but, for our purposes, we drill down to just see the Redis database. It presents us with traces of how our GET, SET, and DEL commands are doing. That provides a quick health check on our cache performance.

![Uptrace can drill down into Redis, so you can look at the traces ](/images/site-mirror/f980fbca8a33710910b4c388053cbf40b76ec6be-1000x385.webp)

*Uptrace can drill down into Redis, so you can look at the traces*

The Uptrace spans tab helps us visualize command responsiveness down to the millisecond using a heatmap. This gives a quick, easy look at whether a [Redis database](/blog/redis-cache-vs-redis-primary-database-in-90-seconds/) is performing to expectations. If the heat moves a bit higher (longer millisecond response time), then a bottleneck is starting or inefficiencies are developing.

In the image below, this Redis database is completing the majority of GET, SET, and DELETE commands at around 1 millisecond, which is a good target for our [cache performance](/solutions/caching/).

![Uptrace heatmap of Redis caching commands](/images/site-mirror/84016e95f4ba5a649a26ac4ec25ca11fe067dc31-1000x474.webp)

*Uptrace heatmap of Redis caching commands*

You can build your own custom metrics that appear on the Uptrace dashboard. For example, memory usage is an important metric for Redis. This screen capture shows how to accomplish that.

![Creating a memory usage custom metric in Uptrace ](/images/site-mirror/1a8e2d0b9217e716f634170a47de50158fa2bc23-594x283.webp)

*Creating a memory usage custom metric in Uptrace*

Uptrace has plenty of other appealing features. One that we found super useful is its optimized storage, which includes performance optimization for common queries, efficient sharding for databases, and improved support for cold storage like S3. Specifically for Redis, Uptrace also supports improved storage policies that give more flexibility to move data between SSD and cold storage; doing so reduces costs, because you don’t have to store as much on SSD.

## Give Uptrace a try

So, what are you waiting for? Try Uptrace as your next [OpenTelemetry backend](https://uptrace.dev/blog/opentelemetry-backend.html) or check out the cloud demo of [Uptrace](https://uptrace.dev/).

We offer huge thanks to [Vladimir Mihailenco](https://github.com/vmihailenco) for his many contributions to the DevOps ecosystem, which includes not only Uptrace but also the now-officially-supported Redis Client library for Golang, go-redis. To learn more about the fastest and easiest way to get started with the Go Programming Language and Redis, read [Go-Redis Is Now an Official Redis Client](/blog/go-redis-official-redis-client/) or visit the GitHub [repo](https://github.com/redis/go-redis). Happy developing!
