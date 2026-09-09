---
title: "Fast Data Ingestion"
linkTitle: "Fast Data Ingestion"
url: "/solutions/fast-data-ingest/"
description: "Data ingestion is the collecting, storing, and processing large volumes of high-variety, high-velocity data presents several complex design challenges—especially in fields like Internet of Things..."
lastmod: 2025-08-06
---

*updated 6 August 2025*

## What is data ingestion?

Data ingestion is the collecting, storing, and processing large volumes of high-variety, high-velocity data presents several complex design challenges—especially in fields like Internet of Things (IoT), e-commerce, security, communications, entertainment, finance, and retail. Given that responsive, timely, and accurate data-driven decision making is core to these businesses, real-time data collection and analysis are critical.

An important first step in delivering real-time data analysis is ensuring adequate resources are available to effectively capture fast data streams. While the physical infrastructure (including a high-speed network, computation, storage, and memory) plays an important role here, the software stack must match the performance of its physical layer or organizations may end up with a massive backlog of data, missing data, or incomplete, misleading data.

## Challenges and best practices for fast data ingest

High-speed data ingestion often involves different types of complexities:

1. **Large volumes of data arriving in bursts:** Bursty data requires a solution capable of processing large volumes of data with minimal latency. Ideally, it should be able to perform millions of writes per second with sub-millisecond latency, using minimal resources.
1. **Data from multiple sources/formats:** Data ingest solutions must also be flexible enough to handle data in many different formats, retaining source identity if needed and transforming or normalizing in real time.
1. **Data that needs to be filtered, analyzed, or forwarded:** Most data ingest solutions have one or more subscribers who consume the data. These are often different applications that function in the same or different locations with a varied set of assumptions. In such cases, the database must not only transform the data, but also filter or aggregate it depending on the requirements of the consuming applications.
1. **Managing a steady data channel between producers and various types of consumers:** If the data arrival pattern isn’t continuous, then producers and consumers need a channel that will let them transfer data asynchronously. The channel must also be resilient to connection loss and hardware failures. In many use cases, producers and consumers do not operate at the same rate. This can lead to data backlogs that further delay consumers from acting on the data.
1. **Data from geographically distributed sources:** In this scenario, it is often convenient for the underlying architecture to distribute data collection nodes close to the source. That way, the nodes themselves become part of the fast data ingest solution, to collect, process, forward, or reroute ingest data.

## We make fast data ingest easier

**High performance with the fewest number of servers**

When it comes to performance, Redis Enterprise has been [benchmarked](/blog/redis-enterprise-extends-linear-scalability-200m-ops-sec/) to handle more than 200 million read/write operations per second, at sub-millisecond latencies with only a 40-node cluster on AWS. This makes Redis Enterprise the most resource-efficient NoSQL database in the market.

**Flexible data structures and modules for real-time analytics: Redis Streams, Pub/Sub, Lists, Sorted Sets, Time Series**

Redis offers a variety of data structures such as Streams, Lists, Sets, Sorted Sets, and Hashes that provide simple and versatile data processing in order to efficiently combine high-speed data ingest and real-time analytics.

Redis’ Pub/Sub capabilities allow it to act as an efficient message broker between geographically distributed data-ingest nodes. Data-producing applications publish streaming data to channels in the format(s) required, and consuming applications subscribe to those channels that are relevant to them, receiving messages asynchronously as they are published.

Lists and Sorted Sets can be used as data channels connecting producers and consumers. You can also use these data structures to transmit data asynchronously. Unlike Pub/Sub, Lists and Sorted Sets offer persistence.

Streams can do even more, offering a persistent data ingest channel between producers and consumers. With Streams, you can scale out the number of consumers using consumer groups. Consumer groups also implement transaction-like data safety when consumers fail in the midst of consuming and processing data.

And finally [Time Series](https://redis.io/timeseries/) provides an enhanced fast data ingest feature set including downsampling, special counter operations on the last ingested value, and double delta compression combined with real-time analytics capabilities like for data labeling with built-in search, aggregation, range queries, and a built-in connector to leading monitoring and analytics tools such as Grafana and Prometheus.

**Active-Active Geo-Distribution deployment**

Redis Enterprise’s [CRDTs-based Active-Active technology](https://redis.io/active-active/) enables complex data-ingest and messaging operations across geo locations and enables application to be deployed in a completely distributed manner to significantly improve availability and application response time.

**Extend Redis DRAM with SSD and persistent memory**

Redis Enterprise’s [Auto Tiering](https://redis.io/auto-tiering/) technology enables extending DRAM with SSD and persistent memory, allows storing very large multi-terabyte datasets using the same infrastructure costs of a disk-based databases and while keeping database latencies at sub-millisecond levels even when ingesting more than 1M items/sec on each node of the Redis Enterprise cluster.

## How to implement fast data ingest with Redis

Here are a few code snippets written in Java. They all use the Jedis library. First, follow the instructions on Jedis’ [getting started page](https://github.com/xetorthio/jedis/wiki/Getting-started) to download the latest version of Jedis.

1. **Fast data ingest using Redis Streams**

A. Publish a message to a stream data structure. This program uses XADD to add new items to the stream. File name: StreamPublish.java.

B. Consume data from a stream asynchronously. Wait for the message if the stream is empty. This program uses the XREAD command. File name: StreamConsumeAsync.java.

C. Query a stream using the XRANGE command. File name: StreamQuery.java

2. **Fast data ingest using Pub/Sub**

A. Publish to a channel. File name: PubSubPublish.java

B. Subscribe to a channel. File name: PubSubPublish.java

3. **Fast data ingest using Lists**

A. Push data to a list. File name: ListPush.java

B. Pop data from a list. File name: ListPop.java
