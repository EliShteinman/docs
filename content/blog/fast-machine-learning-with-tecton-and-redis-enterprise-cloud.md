---
title: "Delivering Fast Machine Learning with Tecton and Redis Enterprise Cloud"
linkTitle: "Delivering Fast Machine Learning with Tecton and Redis Enterprise Cloud"
url: "/blog/fast-machine-learning-with-tecton-and-redis-enterprise-cloud/"
description: "Real-time machine learning (ML) applications are everywhere — from approving credit card transactions as they happen, to immediately generating personalized recommendations for your favorite..."
date: 2022-03-10
blogCategories:
- "Company"
- "Guest Blogs"
authors:
- "Ed Sandoval"
- "Eddie Esquivel"
lastmod: 2025-07-03
hidden: true
mirrored: true
---

*By Ed Sandoval, Eddie Esquivel · Published 10 March 2022 · updated 3 July 2025*

![Blog tile image](/images/site-mirror/bed06e38e7a81fe92ac9e1967723ede840612505-772x550.webp)

Real-time machine learning (ML) applications are everywhere — from approving credit card transactions as they happen, to immediately generating personalized recommendations for your favorite streaming service. These applications can’t afford any delay; they require live access to fresh data in order to provide ultra-low-latency inference (100 milliseconds or less). To give developers and organizations cost-effective real-time capabilities for high-scale ML applications, we’re excited to jointly announce a first-class integration of [Tecton](https://www.tecton.ai/) and [Redis Enterprise Cloud](/redis-enterprise-cloud/overview/).

Redis Enterprise Cloud is the best version of Redis, delivering best-in-class performance, scalability and cost-effectiveness across cloud vendors. Redis has been voted the most loved database by developers for five consecutive years in [Stack Overflow’s annual developer survey](https://insights.stackoverflow.com/survey/2021#section-most-loved-dreaded-and-wanted-databases). Popular with [financial services](/docs/data-innovation-in-banking-finance/), e-commerce and gaming industries, Redis has a track record of meeting the most demanding latency (sub-millisecond) and high-availability requirements, making it ideally suited to serve the needs of real-time ML applications.

Tecton is the leading feature store for enterprises looking to accelerate their time to production for ML projects. Its foundations came from the experience building [Uber Michelangelo](https://eng.uber.com/michelangelo-machine-learning-platform/), the platform powering every ML application at Uber. Tecton is a system to operate and manage data pipelines and features for production ML applications. Typical use cases include fraud detection, real-time recommendations, dynamic pricing, and personalization.

Now that Tecton’s Feature Store integrates with Redis Enterprise Cloud for online serving, it’s easier and more cost-effective than ever to productionize low-latency, high-throughput ML use cases. For Tecton users running at high scale, a benchmark analysis shows that Redis Enterprise achieves 3x faster latency while at the same time being 14x less expensive than Amazon DynamoDB (read more on Tecton’s [blog here](https://www.tecton.ai/blog/announcing-support-for-redis)). In this article, we’ll take a deeper look at how Redis Enterprise and Tecton work together.

## How Tecton integrates with Redis

To understand where Tecton and Redis fit together to enable real-time ML, let’s take a look at steps for productionizing an ML use case like fraud detection:

- First, raw data is required (e.g. all of a user’s historical transactions + their current transaction in real-time). This data is most likely spread through various data warehouses and data streams across the enterprise.
- To generate features for a model, you need to connect to those data sources and define and execute the data transformations that will yield features. For example, one feature might look at the average transaction amount for the user over the past six months and compare it against their current transaction.
- Ultimately, you need to serve your features to the ML model that’s making real-time predictions, and do this at sub-100ms latencies so that users don’t perceive any delay.

Tecton’s Feature Store is designed to handle these steps, abstracting away all the work of orchestrating feature transformations and data pipelines so your data science and data engineering teams can focus on building models. However, Tecton is not a compute engine or a database. Instead, it sits on top of the infrastructure that customers already use, so you’re free to build the ML stack that’s right for you.

Redis Enterprise Cloud is one of these infrastructure components, bringing customers a new high-performance option for the **online store **used by Tecton’s Feature Store.

![](/images/site-mirror/100f7e39000a6a6f3346b9090ae3d0aeabc41d0f-1024x285.webp)

## How Tecton uses online vs. offline stores

Tecton’s Feature Store supports the two main access patterns for ML: retrieving millions of rows of historical data for model training, and retrieving a single row, in a matter of milliseconds, to serve features to models running in production. Since these use cases are so different in terms of performance and cost tradeoffs, we support different types of databases for offline vs. online feature retrieval.

For the offline feature store, Tecton supports S3, as it provides cost-effective storage that’s able to scale to meet your offline feature serving needs for model training. For the online feature store, Tecton now offers customers a flexible choice between DynamoDB (on-demand capacity mode) and Redis Enterprise Cloud.

## Eliminating training-serving skew

Without this dual database approach, many organizations implement separate data pipelines for offline training and online serving. Minor differences in how the pipelines are implemented can completely derail model performance, because the data the model sees in training does not match the data it encounters in production. This mismatch is called training-serving skew, and it is incredibly time-consuming to debug.

Tecton’s Feature Store automatically resolves training-serving skew by coordinating data across offline and online environments, so it’s always synchronized. Users can start off using an offline store only with batch inference, and once they’re ready for online inference, update a single line of code to start materializing data into the online store.

## Advantages of Redis Enterprise Cloud for Tecton users

For Tecton users operating at high scale, one of the key advantages of using Redis Enterprise Cloud is performance and cost savings. Based on a benchmark analysis of serving online features at high-throughput, Redis was 3x faster and 14x cheaper than DynamoDB onTecton.

Redis Enterprise Cloud also offers excellent operational capabilities ready to meet current and future low-latency storage needs. It offers high availability with an SLA of 99.999% uptime, multiple database persistence, backup, and recovery options. Customers with large feature datasets can achieve additional cost savings by tiering the online feature store over DRAM and SSD.

## How to get started

If you aren’t already using Redis Enterprise Cloud, you can sign up for an account [here](/try-free/). We recommend that Tecton users deploy Redis Enterprise Cloud in AWS to minimize latency, as Tecton runs natively in AWS and is able to establish peering connectivity into Redis Enterprise Cloud. In the future, Tecton plans to add native support for other cloud vendor platforms.

If you’re not a Tecton user and are interested in learning more, you can register for a free trial of Tecton [here](https://www.tecton.ai/tecton-free-trial/).
