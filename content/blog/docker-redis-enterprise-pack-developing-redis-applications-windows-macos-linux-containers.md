---
title: "Docker and Redis Enterprise Pack – Developing Redis Applications on Windows, MacOS or Linux with Containers"
linkTitle: "Docker and Redis Enterprise Pack – Developing Redis Applications on Windows, MacOS or Linux with Containers"
url: "/blog/docker-redis-enterprise-pack-developing-redis-applications-windows-macos-linux-containers/"
description: "We are excited to announce the preview release of the new docker image for Redis Enterprise Pack."
date: 2017-04-12
blogCategories:
- "Company"
- "Tech"
authors:
- "Cihan B"
lastmod: 2025-03-04
hidden: true
mirrored: true
---

*By Cihan B · Published 12 April 2017 · updated 4 March 2025*

![Blog tile image](/images/site-mirror/2219a4fa742e9f73fa958a83666638ea740678e3-245x206.webp)

We are excited to announce the preview release of the new docker image for Redis Enterprise Pack.

Redis is the most popular database used with Docker containers. Redis Enterprise Pack extends open source Redis and delivers stable high performance, linear scaling and high availability with significant operational savings.

The new Redis Enterprise Pack image is available on [Docker Hub](https://hub.docker.com/_/redis).

Docker brings a great deal of benefits when working with Redis Enterprise Pack. Containers help scale-minimize Redis Enterprise Pack and fit it right into your development environment. You can run a full cluster locally on your Windows, macOS or Linux host.

- [Windows and Redis Enterprise Pack](/redis-enterprise-documentation/installing-and-upgrading/docker/windows/)
- [MacOS and Redis Enterprise Pack](/redis-enterprise-documentation/installing-and-upgrading/docker/macos/)
- [Linux and Redis Enterprise Pack](/redis-enterprise-documentation/installing-and-upgrading/docker/linux/)

## Quick Start with Redis Enterprise Pack using Docker

You can use Docker to run Redis Enterprise Pack container in MacOS, various Linux and Windows-based machines. Getting started is simple:

**Step 1: Run the Redis Enterprise Pack container**

docker run -d –cap-add sys_resource –name rp -p 8443:8443 -p 12000:12000 redis/redis

**Step 2: Setup Redis Enterprise Pack cluster**

Simply visit [https://localhost:8443](https://localhost:8443) on the host machine and follow the setup instructions.

**Step 3: Create a Redis database**

Create a Redis database on port 12000 – Click on advanced options to set the database port.

![](/images/site-mirror/a606710f730b5e8848c58f04e713ce8bf73a0e6a-1710x1170.webp)

**Step 4: Connect to your database using redis-cli**

docker exec -it rp bash
# sudo /opt/redis/bin/redis-cli -p 12000
# 127.0.0.1:16653> set key1 123
# OK
# 127.0.0.1:16653> get key1
# “123”

## Redis Enterprise Pack Container Architecture

A container image represents a single node of the Redis Enterprise Pack cluster. Each container instance can run multiple open source Redis shards to provide seamless scaling. Redis Enterprise Pack Proxy is a high-speed process that scales all connections from Redis applications to the cluster while improving latency and throughput. The Cluster Manager governs and constantly monitors the cluster of Redis Enterprise Pack nodes, and provides efficient multi-tenancy architecture to reduce effects of noisy-neighbours. Redis Enterprise Pack also comes with a simple visual UI for administration, alerting and monitoring over HTTPS.

![](/images/site-mirror/e2659f8c950c3538caf51ed8b438317ddfe17db4-2418x1113.webp)

## Common Docker Deployment Topologies with Redis Enterprise Pack

When deploying Redis Enterprise Pack using Docker, there are a few common topologies:

- **Topology #1:** The simplest topology is to run a single node cluster with a single container in a single host machine (host OS). This is best for local development or functional testing. Obviously, in a single node topology, Redis Enterprise Pack can’t replicate to slave shards or provide any protection for failures.

![](/images/site-mirror/8e7d8ed08e81cc01bbcbeff69ed4980ba65269c4-255x378.webp)

- **Topology #2:** You may also run a multi-node cluster with multiple Redis Enterprise Pack containers, all deployed to a single host machine (host OS). This topology is similar to Topology #1 except that you run a multi-node cluster to develop and test against. This helps you build scale-minimized systems that closely replicate the behavior of your production environment with Redis Enterprise Pack.

![](/images/site-mirror/128431fc0598fe1255c94163aa6009f95a43630a-777x380.webp)

- **Topology #3:** You may also run a multi-node cluster with multiple Redis Enterprise Pack containers, each deployed to its own host machine. This topology minimizes interference between Redis Enterprise Pack containers so the performance is more predictable than that of Topology #2.

![](/images/site-mirror/05e5530732b9a2cde9a93a141d9ab13c475945fb-780x380.webp)

You can find more detailed information in our [documentation](/redis-enterprise-documentation/installing-and-upgrading/docker/) on Docker.
