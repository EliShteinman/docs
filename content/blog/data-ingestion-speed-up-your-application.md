---
title: "Data Ingestion: 6 Ways to Speed Up Your Application"
linkTitle: "Data Ingestion: 6 Ways to Speed Up Your Application"
url: "/blog/data-ingestion-speed-up-your-application/"
description: "Today’s world requires real-time responses – latency is the new outage, and your customers’ expectations for speed have only gone up. Real-time use cases are only possible with real-time solutions...."
date: 2022-08-03
blogCategories:
- "Tech"
authors:
- "Talon Miller"
lastmod: 2025-03-27
hidden: true
---

*By Talon Miller, Principal Technical Marketer · Published 3 August 2022 · updated 27 March 2025*

![Blog tile image](/images/blog/4b1d7ec9338e96d67c1f0f1cab48ed8c85f86830-772x550.webp)

Today’s world requires real-time responses – latency **is **the new outage, and your customers’ expectations for speed have only gone up. Real-time use cases are only possible with real-time solutions. An RDBMS isn’t capable of providing the speed and performance an in-memory database like Redis Enterprise can provide.

Read our White Paper “Latency is the New Outage.”

## Real-time use cases

### 1. Caching for a front-end DBMS

Legacy and traditional SQL databases aren’t designed for speed at scale, so for that reason, a cache is commonly used to store copies of lookup tables to reduce latency and increase throughput. This allows that front-end DBMS to scale easily while always being available.

### 2. Caching user session data

Caching user session data is crucial for building a scalable and responsive application. Storing every user interaction requires access to the session’s data, and keeping that data in the cache speeds up response time to the application user. Caching session data in this ingestion process is also very important on a larger scale for modern microservices architectures as the session data is typically used as the source of truth, helping with data quality. This ensures microservices state updates are fast and scalable.

### 3. Caching APIs

Modern application APIs are very busy and are the source of a lot of latency if not handled with performance in mind. Caching APIs ensures responses for the application are always real-time.

Let’s take a look at six different ways that data ingestion of part of your data lake into Redis Enterprise can transform your data layer so that you can keep that competitive edge and enable these real-time use cases.

## Data migration: blue-green deployment

![diagram of blue-green deployment](/images/blog/e22d9bd98786d3b090c56def884b45b8bf7b83f5-1024x440.webp)

Applications simply cannot take on the many risks of data migration, like unexpected (and usually longer than expected) outages. The less risky route that enterprises commonly rely on is blue-green deployments to ingest data in which the application continues to use the “blue” legacy database while a new “green” cloud-native database is deployed in parallel for live-production testing and cut-over of this new data pipeline with the assurance of rollback. Redis Data Integration (RDI) is a fast data ingestion tool that automatically converts data to Redis data structures such as Streams, Lists, Sets, Sorted Sets, and Hashes that make data processing simple and efficient. Redis’ Pub/Sub capabilities also make it an efficient message broker between distributed data ingest nodes.

## Database migration: multi-phase replatforming

![multi-phase replatforming diagram](/images/blog/3ee32319fd79bd3541819623dc24faea0ac46f69-1024x277.webp)

Mission-critical applications that are too complex and/or contain large amounts of big data are not appropriate for data ingestion blue-green deployment. They require a multi-phase data ingestion migration plan that can span months or even years to complete. Typically, these projects incrementally migrate small workloads to newly created modular applications or more recently to microservices. This application’s legacy database will often act as the system of record or data warehouse for the duration of the project, which makes consistency a challenge with the new database(s) that support the microservice architecture. Redis Connect can be used on a single, or small set of tables, to maintain consistency between the legacy system of record and new databases, sometimes even data ingest bi-laterally.

## Database read-replica: cache prefetching

![](/images/blog/434af24bcc27a34029224c287bb0fbcb133fc29d-1024x286.webp)

It is common for businesses to keep their legacy databases as a system of record to support their existing operations while, at the same time, leveraging read-replicas, or cache prefetching, ingest data in order to enable these real-time solutions. Redis Connect is used for streaming data indefinitely from the legacy database to Redis Enterprise. A very easy and nearly zero-risk way to finally enable real-time data use cases.

## Hybrid cloud deployment

![diagram of hybrid-cloud deployment with microsoft azure, aws and google cloud and redis enterprise](/images/blog/7543ab7eaba1c7a461517a0fe0f6eaee3431b4a4-1024x306.webp)

Legacy enterprise architectures, compliance risks, and operational concerns often act as barriers to migrating to the cloud. To overcome these challenges, enterprises have adopted a hybrid cloud architecture that splits deployments between on-premises and public clouds. Commonly, a stateless application is hosted on the cloud while operational data remains on-premises acting as the legacy system-of-record database. Redis Connect can be used for streaming data from the on-premises database to Redis Enterprise, which supports bi-lateral replication between its on-prem and public cloud replicas.

## Cloud bursting

Many industries are seeing unprecedented increases in transactions and high expectations for speed and availability. Businesses need to elastically provision, burst to the cloud, infrastructure to handle seasonal traffic peaks, expand data warehousing/analytics, improve disaster recovery objectives, or maintain operational business continuity in the event of a data center failure. The common solution involves leveraging the cloud for geo-distributed, on-demand infrastructure. Redis Connect can be used for streaming data from multiple sources to Redis Enterprise, which is capable of active-active geo-distributed hybrid cloud deployments.

## Microservice pattern: Command Query Responsibility Segregation (CQRS)

![image of command query responsibility segregation](/images/blog/447f71da7cb0a23a89f416f6440d8a0c37daf98f-1024x470.webp)

Microservices architecture adoption continues to grow as application modernization and cloud migration strategies accelerate. One of the most popular microservices design patterns is CQRS. In this pattern, different data structures (commonly supported by different databases) are used to independently optimize for writes (command) and reads (query). Implementing this pattern can be complex within a microservices architecture since consistency between command and query must be maintained. Redis Connect can be used to implement CQRS by streaming and transforming changed-data-events (CDC) from the command database to a read-optimized data structure in a query database/cache.

## Modernize your data layer

The six ways to transform your data layer with data ingestion discussed above provide easy-to-implement and enterprise-hardened ways to help your business stay efficient and competitive. Redis Enterprise is a great place to enable your data to accomplish those modern use cases and provide sub-millisecond responses. There are far more use cases possible than just the caching ones we covered today like leaderboards, message brokers, fraud detection, and more.
