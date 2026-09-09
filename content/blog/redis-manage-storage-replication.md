---
title: "Redis to Manage Storage Replication"
linkTitle: "Redis to Manage Storage Replication"
url: "/blog/redis-manage-storage-replication/"
description: "Redis is a simple, yet powerful in-memory database platform with use cases ranging from session management, queues and pub/sub to general-purpose cache. With its persistence and in-memory..."
date: 2018-04-18
blogCategories:
- "Company"
- "How To and Tutorials"
authors:
- "Rahul M"
lastmod: 2025-06-23
hidden: true
---

*By Rahul M · Published 18 April 2018 · updated 23 June 2025*

![Blog tile image](/images/site-mirror/0073e867b4e64f59de9047fdcde04295ba647e5c-772x550.webp)

[Redis](/redis-features/redis) is a simple, yet powerful in-memory database platform with use cases ranging from session management, queues and pub/sub to general-purpose cache. With its persistence and in-memory replication capabilities, [Redis Enterprise](/redis-enterprise/) is also used as a primary datastore.

As a software engineer, I frequently use Redis to overcome unique problems. In one project, our use case was simple: I wanted to replicate the contents of a file system partition with a fixed, well-defined structure: at the root of the file system we had a fixed set of directories, each with more than a million files. Our previous solution ran two processes in parallel, 24/7 to identify the modified files. The first process scanned all the file contents and identified the changed content since the previous replication. A job ran once every 24 hours to replicate the changed files. The second process indexed all the files that were successfully replicated.

![](/images/site-mirror/56e99344336f7bcf0fc667c771429cbf448cf21a-937x716.webp)

In our previous solution, we used an SQL database to store the file metadata (such as name, size, permissions, path, etc.) and all the information related to modified files. The scheduled replication job queried the database to pull the list of files that were modified, then replicated the content onto a remote server. After replication, it updated the SQL database, marking the files as ‘copied,’ after which the indexing process picked up the marked list to index the file content.

## Redis to the Rescue

Our previous design had major disadvantages: we had to write a lot of code to save/retrieve/modify data in the SQL database, and as the database grew, we had to build a mechanism to prune the data. As the operational overhead became extensive, we started looking at ways to break free of this architecture.

That’s when we found Redis. Redis instantly solved many of our problems. In our new solution, we used the Redis pub/sub feature to notify our various processes of new detections. The scan process published the details of the changed file(s) to a Redis channel. The replication process subscribed to that channel and replicated the file as soon as it was notified. Then the replication process notified the indexing process (via another Redis pub/sub channel). This system eliminated the need to run a job once a day and instead ran replication as an ongoing process. We also saved ourselves the hassle of cleaning up the SQL database!

Before considering the Redis pub/sub model, we also considered RabbitMQ, Kafka, etc. Each was good but required a lot of work on our end, with a bit of a learning curve. None were as versatile and easy to use as Redis.

As we adopted Redis, we discovered many of its other advantages. We started using built-in data structures such as Lists, Hashes and Sets, to perform analytics. For example, we wanted to know the frequency of changes to the files and directories, and which applications made those changes. We used Redis and its data structures to gather this information. We then passed it to the indexing process and enriched the indexed meta data with analytics data.

Getting started with Redis is extremely easy. You can sign up for Redis Cloud for free at: [/redis-enterprise-cloud-free-30-mb-plan](/redis-enterprise-cloud-free-30-mb-plan)

*This is a guest post by Rahul, a Software Engineer and user of Redis Enterprise as part of his work.*
