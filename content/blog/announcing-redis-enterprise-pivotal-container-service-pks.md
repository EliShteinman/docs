---
title: "Announcing Redis Enterprise on Pivotal Container Service (PKS)"
linkTitle: "Announcing Redis Enterprise on Pivotal Container Service (PKS)"
url: "/blog/announcing-redis-enterprise-pivotal-container-service-pks/"
description: "We are incredibly excited to announce the preview of a jointly developed solution between Redis and Pivotal, which will deliver easy integration of Redis Enterprise as a native service on PKS...."
date: 2018-11-05
blogCategories:
- "Announcements"
- "New Product Announcements"
authors:
- "Cassie Zimmerman"
lastmod: 2025-03-27
hidden: true
---

*By Cassie Zimmerman, Director, Strategic Alliances · Published 5 November 2018 · updated 27 March 2025*

![Blog tile image](/images/site-mirror/0073e867b4e64f59de9047fdcde04295ba647e5c-772x550.webp)

We are incredibly excited to announce the preview of a jointly developed solution between Redis and Pivotal, which will deliver easy integration of [Redis Enterprise](/redis-enterprise/) as a native service on PKS. Together, this solution gives developers instant, self-service access to a cloud-native, stateful data service that is portable, operationally simple, and brings speed and simplicity to accelerate application development. But first, let’s take a look back at how we got here, and why we’re thrilled to launch this new solution.

### Why Redis in Containers?

For years, Redis has been one of the most vibrant and well respected open source technologies amongst the developer community. Since it was designed as a flexible key-value store that supports various data structures, Redis has grown quickly in popularity as a lightweight, extremely fast and simple-to-develop-on database. In fact, Redis is the [world’s most loved database](https://www.prnewswire.com/news-releases/redis-named-the-most-loved-database-for-second-consecutive-year-300612994.html), and by far the most downloaded container on Docker Hub outside of Linux ([at over 1 Billion ](https://www.prnewswire.com/news-releases/redis-establishes-a-new-industry-benchmark-with-one-billion-downloads-on-docker-300719558.html)pulls!).

Getting started with Redis in containers is easy work for a developer, taking only a few minutes to set up and get working with an application. A small investment of time and effort can have an immediate, dramatic impact on performance, usually by orders of magnitude.

### First Came Containers, Then Came Kubernetes

If you’re adopting microservices, you’ll want to run multiple containers across multiple machines. You’ll need to manage your containers in a way that lets them communicate, auto-heal (in case of a failed machine) and handle storage considerations, among other things. Doing this manually is an operational nightmare, hence the need for Kubernetes! Kubernetes is an open source container orchestration platform that helps large numbers of containers work together in harmony.

### First Came Kubernetes, Then Came PKS

The Pivotal Container Service (PKS) takes things a step further, handling the heavy operational burdens required to deliver production-ready environments. PKS acts as the enterprise orchestrator for Kubernetes deployments, allowing users to reliably deploy and run containerized workloads across private and public clouds. It eases the common challenges of container orchestration with built-in high availability, monitoring, automated health checks and much more.

### Scaling Redis with Redis Enterprise

At Redis, we follow similar principles. Redis Enterprise expands upon the core principles of Redis: simplicity, transparency and the belief that making software should be fun. Redis Enterprise is a “container-like” enterprise deployment framework for open source Redis. It extends the power of Redis by adding capabilities you need in production scenarios — including true high availability (HA), automatic failover, replication across data centers, data persistence and more. Our enterprise layer makes scaling completely seamless to the developer. At the same time, the scale is completely transparent at the operations layer to give operators complete control over their deployments.

Given all of these developments, we feel Redis Enterprise + PKS is a perfect combination. As we work to release a generally available version of Redis Enterprise on PKS in the coming months, we will also add support for active-active replication using CRDTs for globally distributed applications.

If you would like to start experimenting with our Redis Enterprise release for PKS, please reach out to [channel@redis.com](mailto:channel@redis.com), so we can help you with any Redis questions. We will also have a Redis booth (booth #XYZ?) at VMworld Europe this week in Barcelona, so drop by to learn more.

### More resources:

**Blog**: [Why Use Redis Enterprise Kubernetes Release on Pivotal Container Service?](/blog/use-redis-enterprise-kubernetes-release-pivotal-container-service/)

**Video**: [Redis Enterprise on Cloud Native Platforms](https://www.slideshare.net/slideshow/redisconf18-redis-enterprise-on-cloud-native-platforms/99432734)

**Blog**: [Redis Enterprise Operator for Kubernetes](/blog/redis-enterprise-operator-kubernetes/)
