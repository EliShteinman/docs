---
title: "Redis Streams + Apache Spark Structured Streaming"
linkTitle: "Redis Streams + Apache Spark Structured Streaming"
url: "/blog/redis-streams-apache-spark-structured-streaming/"
description: "Recently, I had the honor of presenting my talk, “Redis + Structured Streaming: A Perfect Combination to Scale-out Your Continuous Applications” at the Spark+AI Summit."
date: 2019-06-03
blogCategories:
- "Tech"
authors:
- "Roshan Kumar"
lastmod: 2026-09-01
hidden: true
---

*By Roshan Kumar, Senior Product Manager · Published 3 June 2019 · updated 1 September 2026*

![Blog tile image](/images/site-mirror/e66f02f129cf4dfa2170a2ae5761c911ad75f50d-548x287.webp)

Recently, I had the honor of presenting my talk, “[Redis + Structured Streaming: A Perfect Combination to Scale-out Your Continuous Applications](https://databricks.com/session/redis-structured-streaming-a-perfect-combination-to-scale-out-your-continuous-applications)” at the Spark+AI Summit.

My interest in this topic was fueled by new features introduced in Apache Spark and Redis over the last couple months. Based on my previous use of Apache Spark, I appreciate how elegantly it runs batch processes, and the introduction of [Structured Streaming](https://spark.apache.org/docs/latest/structured-streaming-programming-guide.html) in version 2.0 is further progress in that direction.

Redis, meanwhile, recently announced its new data structure, called “[Streams](https://redis.io/docs/latest/develop/),” for managing streaming data. Redis Streams offers asynchronous communication between producers and consumers, with additional features such as persistence, look-back queries, and scale-out options – similar to Apache Kafka. In essence, with Streams, Redis provides a light, fast, easy-to-manage streaming database that benefits data engineers.

Additionally, the [Spark-Redis library](https://github.com/RedisLabs/spark-redis) was developed to support Redis data structures as resilient distributed data sets (RDD). Now, with Structured Streaming and Redis Streams available, we decided to extend the Spark-Redis library to integrate Redis Streams as a data source for Apache Spark Structured Streaming.

![](/images/site-mirror/c849a2ca473b00233e14d213c39a2ed71a69e18d-1557x583.webp)

During my talk last month, I demonstrated how you can collect user activity data in Redis Streams and sink it to Apache Spark for real-time data analysis. I developed a small, mobile-friendly Node.js app where people can click on the dog they love most, and I used it to run a fun contest through my session. It was a tough fight, and a couple of folks in the audience even got creative with hacking my app. They changed the HTML button name using the “page inspect” option and tried to mess with my demo. But in the end, Redis Streams, Apache Spark, the Spark-Redis library, and my code were all robust enough to handle those changes effectively.

![](/images/site-mirror/8ab71f8b122241069ae78d4f2de9c078c31fed1f-1557x712.webp)

The audience also asked some interesting questions during and after my presentation, such as:

1. How can I scale out if my data processing is slower than the rate at which Redis Streams receives the data? **My Answer:** Configure a consumer group, and run each Spark job as a different Redis Streams consumer belonging to that group. That way, every job gets an exclusive set of data. It’s important to set the output mode to “update” so that each job doesn’t overwrite the other job’s data commits.
1. What happens to the data in Redis Streams if I restart my Spark job? **My Answer:** Redis Streams persists data. Therefore, your Spark job won’t miss any data. If you restart your Spark job, it will pull the data from the point where it left off.
1. Can I develop my Spark app in Python? (My demo was written in Scala) **My Answer:** Yes, you can. Please see our Spark-Redis documentation on GitHub.
1. Can I deploy Redis Streams on the cloud? **My Answer:** Yes, Streams is just another data structure in Redis that’s built into Redis starting from release 5.0. The quickest way to start is to sign up at [Try Free](/try-free/).

My main takeaway from the summit was that there’s growing interest in continuous processing and data streaming. Owing to the demand, we published [a more detailed article on this topic over at InfoQ](https://www.infoq.com/articles/data-processing-redis-spark-streaming), which offers a detailed recipe for how to set up Redis Streams and Apache Spark and connect both using the Spark-Redis library. Or feel free to check out the [full video of my presentation here](https://databricks.com/session/redis-structured-streaming-a-perfect-combination-to-scale-out-your-continuous-applications).
