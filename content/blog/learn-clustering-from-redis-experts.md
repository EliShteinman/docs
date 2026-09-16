---
title: "Learn Clustering From Redis Experts"
linkTitle: "Learn Clustering From Redis Experts"
url: "/blog/learn-clustering-from-redis-experts/"
description: "These five videos break down the general concepts of clustering through webinars, tutorials, walk-through demos, and even a real-world customer success story from a Fortune 500 company."
date: 2023-05-09
blogCategories:
- "Uncategorized"
authors:
- "Redis  "
lastmod: 2025-03-27
hidden: true
mirrored: true
---

*By Redis   · Published 9 May 2023 · updated 27 March 2025*

![Blog tile image](/images/site-mirror/f712d44c7cf2e222f20a4f8794b58f8d212f392f-772x550.webp)

**These five videos break down the general concepts of clustering through webinars, tutorials, walk-through demos, and even a real-world customer success story from a Fortune 500 company.**

So many large datasets, so little time.

Clustering has been a major boon for DevOps. We define a cluster as “a set of cloud instances, virtual machine/container nodes, or bare-metal servers that let you create any number of Redis databases in a memory/storage pool that’s shared across the set.”

Clustering allows IT teams to parse enormous blocks of data quickly, giving them more time to work on other projects, not to mention the flexibility, cost-efficiency, and reliability it generates in your applications. These five videos run the gamut to explain clustering and show how it’s used, from high-level information for those just getting started with clustering to hands-on demos you can follow along with.

## What is clustering?

How does clustering work? In this video, Justin Castilla, a senior developer advocate at Redis, breaks down clusterings’ top concepts. He explains how it amplifies availability for applications and scales for extra memory, CPU capacity, and throughput.

“Scalability is the property of a system to handle a growing amount of work by adding resources to the system,” says Castilla. To further explain how clustering works, he focuses on the two most common scaling strategies: vertical scaling (also called *scaling up*) and horizontal scaling (*scaling out*).


![image of three redis instances](/images/site-mirror/2d66726410962e97f390051d07af0b6962876fc7-1084x554.webp)


Castilla breaks the video into chapters: sharding, resharding, hash slots, high availability, and split-brain situation, making for a high-level but thorough examination of how clusters work.

Take a closer look at this video’s description on YouTube; Castilla provides a helpful supplemental tutorial and Redis cluster specification links to help you get started.

Click here to watch.

## How to create a cluster

Are you past the basic clustering concepts and ready to create your own Redis clusters? Justin Castilla is there again.


![Justin Castilla and an interface with code.](/images/site-mirror/73a93f776db94b7090c68096ccab1031dd5f70fc-1089x561.webp)


In just ten minutes, Castilla walks you through his demonstration in four steps:

- creating a redis.conf file template
- setting up a cluster configuration
- starting your server with the local redis.conf file, and
- launching the Redis cluster info command

It’s practical information that you can put to use.

Click here to watch.

## How Uber uses clusters

In this presentation from RedisConf 2021, Uber software engineers Anders Persson and Bisheng Huang present the use cases that called for enhanced application scalability. They go through the process by which they migrated to a cluster from initial evaluation to production launch.

Persson and Huang detail how their team built a cluster management library in Go to automate its cluster management. They explain how this new framework could handle several operations, such as adding and removing nodes, restarting nodes, scaling clusters horizontally and vertically, as well as failure recovery protocols.


![Professional deck presentation from Uber on using Redis clusters from RedisConf 2021](/images/site-mirror/a9453748e6901d883d6c20c2069263132c3cefd9-1423x616.webp)


Watch and listen as they outline the important lessons learned during their migration process.

Click here to watch.

## Building for high availability and extreme performance with clusters

AWS was also on hand at RedisConf 2021 to discuss clustering. Its representative explained how clustering is seen as a solid, consistent strategy to establish high availability and maximize application performance.

Presented by Madelyn Olson, a software engineer for Amazon ElastiCache, this presentation covers how clustering helps achieve millions of operations per second and the opportunities for improving performance and reliability.


![Deck presentation on clustering from RedisConf 2021.](/images/site-mirror/eacd68a4d9a87c344c22ab41e3a6b4ade9ee6787-1423x650.webp)


Olson introduced her presentation by saying she hopes “not to just give a bullet point list of what [a cluster does], but to give everyone an intuitive understanding of what it is and some of the choices that were made during development.” Watch her presentation to learn how to use meshes between different nodes in a cluster and how to shard data so that each shard has its own unique data set.

Click here to watch.

## Using hashtags in clustering

One of the challenges of using clusters is keeping data together that belongs to the same user or application. As Justin Castilla explains in this demonstration, data is stored in different shards based on its hash slot.

What’s a hash slot? As Castilla describes it, “Hash slots are a way to distribute data across shards in [a cluster]. Each key is assigned to a single hash slot, and all keys in the same hash slot are stored on the same shard. This ensures that all of the data for a particular key is always stored together, which can improve performance and scalability.”


![](/images/site-mirror/d7b2bedf28f47d597e12792c8f2fde4a6f220d9b-1600x867.webp)


Castilla notes that hashtags are the piece that “allows you to group your data in a given slot since we don’t want to force you to reverse engineer the crc16 to make sure all the data ends up together.”

Castilla demonstrates how hash slots work, provides examples of clusters, cluster slots, and cluster visualization, covers a section on primary shards, using hash slots, and reviews clustering limitations.

Click here to watch.

## The next step for mastering clusters with Redis

How do clusters work with key-value stores? Dive into Redis Clustering Best Practices With Multiple Keys to understand the value of working with keyspaces, avoiding CROSSSLOTS errors, and evaluating MULTI/EXEC transactions.

Looking to understand how clusters power today’s microservices? Download our e-book Redis Microservices for Dummies for more information.
