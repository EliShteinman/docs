---
title: "Redis Enterprise and Kafka"
linkTitle: "Redis Enterprise and Kafka"
url: "/compare/redis-enterprise-and-kafka/"
description: "Build real-time streaming data pipelines with real-time data access."
lastmod: 2026-05-26
---

*updated 26 May 2026*

Build real-time streaming data pipelines with real-time data access.

## How Kafka and Redis Enterprise work together

Through its extended ecosystem, Kafka is used to build real-time streaming data pipelines – it is all about data in motion. A real-time data pipeline is a means of moving data from its origin or multiple heterogeneous origins (source) to a destination (target) which can handle millions of events at scale in real time. It combines messaging, storage, and stream processing to allow storage and analysis of both historical and real-time data.

[Redis Enterprise](https://redis.io/enterprise/) (the target), along with additional data models such as time series and JSON, is an in-memory database capable of easily ingesting and managing a variety of data models from multiple sources, providing real-time analysis and data access. Real-time access is where the data store presents the most current data and responds to queries all in real time. Redis Enterprise and Kafka using Kafka Streams deliver real-time access and analysis for heterogeneous data sources.

## Redis Enterprise and Kafka Connect

The Kafka community relies on Kafka Connect to integrate with other applications and data systems, so we made connectors. Redis Enterprise provides pre-built, Confluent certified connectors for Kafka Connect to help you quickly and reliably integrate Redis Enterprise and Kafka. The Kafka-Redis **Sink Connector** exports data from Kafka to Redis Enterprise. The Kafka-Redis **Source Connector** subscribes to Redis Enterprise channels using Redis Streams and writes the received messages to Kafka.

As shown in the image below, this is a bridge between Redis Enterprise and Kafka, with the Sink Connector moving data into Redis Enterprise and the Source Connector for the replicated data from [Redis Enterprise Streams](https://redis.io/docs/manual/data-types/streams/) to Kafka. Redis Streams is a Redis Enterprise data type representing a time-ordered log so that you can add new messages in an append-only mode. Download the [Kafka Connectors](https://www.confluent.io/hub/redis/redis-kafka-connect) to start connecting your data.

There are three primary use cases for Redis Enterprise and Kafka:

1. Real-time Data Access with a Real-time Data Pipeline
1. Interservice Microservices Communication
1. Data Synchronization from Legacy Databases

## Real-time data access with a real-time data pipeline

In this real-time inventory use case, Kafka, acting as the real-time data pipeline, gathers and distributes events from several different sources: the warehouse, the order management system, and the sales forecasting system, and provides this information to the inventory manager. Redis Enterprise is the in-memory database that enables real-time data access and maintains the inventory state with instant changes in the merchandise being tracked. The inventory status is then sent back to Kafka, who distributes this information to marketing, stores, and fulfillment. Together, Kafka and Redis Enterprise ensure inventory is tracked and communicated in real time throughout the organization; they provide real-time data access with a real-time data pipeline.

## Interservice microservices communication

The following microservices use case for fraud detection is an excellent example of interservice communication between microservices backed by Redis Enterprise. This architecture uses Redis Enterprise as the source and the target for information with the events managed by Kafka. Kafka provides subscription-based messages between various microservices, acting as a relay that enables application flexibility by decoupling producers from consumers. The microservices authenticate the digital identity, transaction scoring, payment history, etc by using Redis Enterprise and various data models as their analytics engines. Redis Enterprise sends events and information to Kafka, and Kafka distributes these events and information based on subscriptions to other microservices. Together Redis Enterprise and Kafka using Kafka Streams provide real-time interservice communication between microservices.

## Data synchronization: Cache prefetching

Cache prefetching is a technique where data is read from their original storage in slower memory (the legacy database) which is then written to a much faster in-memory database, Redis Enterprise, before it is needed. Kafka Connect propagates changed-data events as they occur on the source (the legacy database), so the Redis Enterprise cache is always consistent with the legacy system.

## Data synchronization: CQRS

[CQRS (Command Query Responsibility Segregation)](https://redis.io/solutions/microservices/cqrs/) is an application architecture pattern often used in cache prefetching solutions. CQRS is a critical pattern within microservice architectures that decouple reads (queries) and writes (commands). With Kafka as the event log and Redis Enterprise as the system of record, by using CQRS you can avoid slow queries.

## Data synchronization: Data migration

Kafka Connect provides seamless replication from an on-premises legacy database to Redis Enterprise with real-time replication and consistency among various platforms. For a single migration, Kafka Connect can be used to synchronize the data until the cut-over date to Redis Enterprise. For longer migrations, sometimes years, where companies are moving from a monolithic environment to microservices, Kafka Connect can be used to maintain synchronized databases for the duration.

## Try for free or download today

### Redis Cloud

Start today for free with Redis Cloud Essentials.

### Redis Enterprise Software

Download Redis Enterprise 6.4.2
