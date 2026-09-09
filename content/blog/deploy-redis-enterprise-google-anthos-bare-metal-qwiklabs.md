---
title: "Learn How to Deploy Redis Enterprise on Google Anthos Bare Metal with new Qwiklabs"
linkTitle: "Learn How to Deploy Redis Enterprise on Google Anthos Bare Metal with new Qwiklabs"
url: "/blog/deploy-redis-enterprise-google-anthos-bare-metal-qwiklabs/"
description: "If you’d like to deploy Redis Enterprise in a Kubernetes environment on Google Anthos Bare Metal, then our latest Qwiklabs module is for you. This module, produced in collaboration with Google..."
date: 2021-12-06
blogCategories:
- "How To and Tutorials"
- "Tech"
authors:
- "Gilbert Lau"
lastmod: 2025-03-27
hidden: true
---

*By Gilbert Lau, Cloud Partner Solution Architect · Published 6 December 2021 · updated 27 March 2025*

![Blog tile image](/images/blog/478a155459951857744a83f2fbf3dbc35f98fe21-772x550.webp)

If you’d like to deploy Redis Enterprise in a Kubernetes environment on Google Anthos Bare Metal, then our latest Qwiklabs module is for you. This module, produced in collaboration with Google Cloud, will teach you how to run Redis Enterprise and a Knative serverless application on an Anthos Bare Metal cluster deployment. Anthos unifies the management of infrastructure and applications across on-premises, edge, and in multiple public clouds, with a Google Cloud-backed control plane for consistent operation at scale. This is part of Redis’ effort to run Redis anywhere and on any cloud, whether it’s on-premises or in the cloud.

The [first joint Redis/GCP Qwiklabs](https://www.qwiklabs.com/focuses/14763?parent=catalog) covered the foundational knowledge of Redis and RediSearch. [Redis](https://redis.io/) is an open source (BSD licensed), in-memory data structure store, used as a database, cache, and message broker. It’s designed for applications requiring the fastest possible response times. Redis uses key/pair values at its core, and those keys point to any number of supported data structures such as [strings](https://redis.io/commands#string), [hashes](https://redis.io/commands#hash), [sets](https://redis.io/commands#set), and [lists](https://redis.io/commands#list) to empower many use cases in retail, gaming, and banking industries. When it comes to hashes, what if you want to retrieve hashes based on their contents, not just based on their key? What if, for example, you want to get a list of all movies directed by Steven Spielberg? RediSearch is the tool that makes this possible and lightning fast.

## What you’ll learn in this Qwiklabs

Deploying Redis Enterprise in a Kubernetes environment has been gaining a lot of traction, as Redis Enterprise serves very effectively as the real-time data platform for building microservices due to its speed and performance. In this latest Qwiklabs, you’ll learn how to install the Redis Enterprise Operator. The operator is responsible for creating two custom resources: Redis Enterprise cluster and Redis Enterprise database. It provides a cloud-native means of managing the lifecycle of Redis Enterprise instances in a Kubernetes environment. This lab will also guide you through how to create and deploy a Knative serverless application on an Anthos Bare Metal cluster. The app you create from this lab will connect to a Redis Enterprise database that you will create and will scale out based on the traffic from a performance testing workload.

Learning and earning credentials from Qwiklabs is one of the easiest and most convenient ways to gain hands-on knowledge about Google Cloud and other third-party technologies, such as Redis Enterprise. If you want to learn how to build real-time apps, check out the Redis Developer Hub at [developer.redis.com](/learn/). There you’ll find huge repositories of working code examples to learn from, and realize the power of our primitive data structures and enterprise modules, such as RediSearch, RedisJSON, RedisTimeSeries, RedisGraph, and RedisBloom.

## Try it out and let us know what you think

Ready to give it a try? Get into the driver seat to take our “Deploying Redis Enterprise for GKE and Serverless App on Anthos Bare Metal” self-paced lab at [https://www.cloudskillsboost.google/focuses/21603?parent=catalog](https://www.cloudskillsboost.google/focuses/21603?parent=catalog). Once you complete the lab, please provide your feedback and rating. Your input means a lot to us!
