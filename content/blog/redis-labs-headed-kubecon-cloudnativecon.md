---
title: "Redis Labs is headed to KubeCon and CloudNativeCon"
linkTitle: "Redis Labs is headed to KubeCon and CloudNativeCon"
url: "/blog/redis-labs-headed-kubecon-cloudnativecon/"
description: "This December, Redis — the company behind Redis — is headed to KubeCon and CloudNativeCon in Seattle. Redis is a NoSQL in-memory database and is known for its simplicity and efficient performance...."
date: 2018-12-10
blogCategories:
- "Company"
authors:
- "Vick Kelkar"
lastmod: 2025-03-27
hidden: true
---

*By Vick Kelkar, Principal Product Manager · Published 10 December 2018 · updated 27 March 2025*

![Blog tile image](/images/site-mirror/32ee5db9cd1fd9039f0e358217b6aa816272c948-1200x1000.webp)

This December, Redis — the company behind Redis — is headed to [KubeCon and CloudNativeCon](https://events.linuxfoundation.org/events/kubecon-cloudnativecon-north-america-2018/) in Seattle. [Redis](/community/oss-projects/) is a NoSQL in-memory database and is known for its simplicity and efficient performance. Furthermore, Redis is also the most popular database on Stackoverflow and has surpassed one [billion container](/blog/redis-enters-billion-downloads-club/) downloads on Docker Hub. While in Seattle, our team will be showcasing the work that makes [Redis Enterprise](/redis-enterprise/) containers a great choice for developing containerized, stateful microservices on a cloud native platform like Kubernetes.

Our Enterprise product addresses the needs of cloud native production environments by providing [multi-tenancy](/blog/multi-tenancy-redis-enterprise/), high-availability and automatic failovers on [cloud native platforms.](https://www.slideshare.net/slideshow/redisconf18-redis-enterprise-on-cloud-native-platforms/99432734) We have enhanced the security of our managed Redis offering with [Two-Factor authentication](/blog/redis-labs-adds-two-factor-authentication-enhance-account-security/). We are working with our partners like [RedHat](/blog/redis-labs-red-hat-partner-bring-open-source-enterprise/) and Pivotal to develop solutions for Kubernetes-based distributions like [OpenShift](https://blog.openshift.com/using-the-redis-enterprise-operator-on-openshift/) and [PKS](/blog/use-redis-enterprise-kubernetes-release-pivotal-container-service/). For our Redis Enterprise containerized release, we are leveraging [Operators](/blog/redis-enterprise-operator-kubernetes/) to offer a persistent stateful service for your containerized workloads and microservices.

Redis Enterprise is an excellent choice of database for your microservices. It supports multi-tenancy: you can [configure multiple, isolated databases](/redis-enterprise-documentation/administering/database-operations/creating-database/) on a single Redis Enterprise cluster. You can run multiple database endpoints on a simple three-node cluster, allowing each microservice to access its respective database with minimal server infrastructure and/or operational overhead. [Redis Enterprise’s Kubernetes integration](/blog/containers-kubernetes-redis-enterprise-kubernetes-service-explained/) includes:

1. Redis Enterprise persistence, provided using Kubernetes StatefulSet and StorageClass.
1. Redis Enterprise’s headless service registered in the Kubernetes service catalog.
1. The ability to manage a Redis Enterprise license using [Kubernetes secrets](https://kubernetes.io/docs/concepts/configuration/secret/) primitive.
1. Auto-bootstrapping multi-node Redis Enterprise clusters using Kubernetes secrets.
1. Maintaining and upgrading Redis Enterprise using rolling upgrades.

![Redis Enterprise Headless Service](/images/site-mirror/8b4f2e10667ad9fd8a8700dd68ed977ba8034387-1687x848.webp)

Come to the Redis booth at KubeCon and CloudNativeCon to hear about new features of Redis, like the [Redis Streams](/blog/use-redis-streams-apps/) data structure, or how you can extend the functionality of Redis using modules like [RediSearch](/blog/mastering-redisearch-part/) and [RedisGraph](/blog/announcing-redis-enterprise-release-redisgraph-streams-redis-5-0-popular-redis-java-python-clients/). If you would like to learn how your business can run Redis Enterprise on Kubernetes and/or OpenShift cluster, please don’t hesitate to stop by our booth! If you would like to start experimenting with our Redis Enterprise release for cloud native platforms, please [contact us](/meeting/).
