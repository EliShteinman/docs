---
title: "Redis Insight makes RDI even simpler"
linkTitle: "Redis Insight makes RDI even simpler"
url: "/blog/redis-insight-makes-rdi-even-simpler/"
description: "Get seamless data integration and faster data access with Redis Data Integration (RDI)— no-code required. Seamlessly sync your database to Redis in near real-time and build apps at scale, faster..."
date: 2024-08-06
blogCategories:
- "Tech"
authors:
- "Yaron Parasol"
- "Viktar Starastsenka"
lastmod: 2025-07-03
hidden: true
mirrored: true
---

*By Yaron Parasol, Viktar Starastsenka · Published 6 August 2024 · updated 3 July 2025*

![Blog tile image](/images/site-mirror/28a0f96c475dc0ba8c533b2ac6f21557aa3c83ee-772x552.webp)

Get seamless data integration and faster data access with Redis Data Integration (RDI)— no-code required. Seamlessly sync your database to Redis in near real-time and build apps at scale, faster than ever before.

RDI establishes a data streaming pipeline that mirrors data from your existing database to Redis, so if a record is added or updated, those changes automatically flow into Redis. Plus, it’s fully integrated into Redis Insight, making it easy to create, validate, deploy, and monitor your data pipelines directly from the most powerful, most used Redis GUI.

## Enjoy effortless and dependable data syncing with RDI

We built an end-to-end solution using a Capture Data Change (CDC) mechanism that mirrors your apps’s primary database to Redis and a Stream Processor to map and transform source data such as relational tables into fast Redis data structures that match your requirements.

And with RDI, you get an enterprise-grade pipeline that’s highly available, guarantees at-least-once delivery, and ticks all the essential enterprise boxes.

Flexible and easy to use, RDI supports the most popular databases and requires no code. RDI pipelines are declarative, using prebuilt transformations that can be easily configured using expressions and built-in functions. Focus on your application code, create your pipelines with YAML files, and let RDI handle the rest.

### Manage your data pipeline easily using YAML files

Get the flexibility you need to design your pipeline with RDI using a series of YAML files. Configure your [RDI pipeline](https://redis.io/docs/latest/integrate/redis-data-integration/ingest/data-pipelines/data-pipelines/) easily with human-readable YAML files:

- **config.yaml**: This is the main configuration file – and the only mandatory one. This file configures the connection to the source, the dataset to replicate (tables, columns), and then the connection to the target Redis database.
- **Job files:** These are optional configuration files per ‌source table. This lets you massage the data, starting from simple things like changing field names all the way to calculated values and nesting into JSON of one-to-many relationships.

Even the most simple configuration file needs tooling to make you productive. Enter Redis Insight.

## Deploy, manage, and visualize your RDI data pipelines in Redis Insight

Redis Insight is the most popular Redis developer tool. Now it’s more useful than ever, equipped with new features to help you build fast apps faster.

### Create, test & deploy RDI pipelines

Redis Insight makes pipeline creation simple. With Redis Insight, you can seamlessly:

- Simplify templates & code completion: Redis Insight gets you started with essential files and guides you through code completion, so you don’t have to switch back and forth to reference documentation.
- Dry-run your transformations: Test a job with transformations anytime and compare the results with input mock data.
- Ready, set, deploy: So you’ve dry-run your pipeline? Why not test it with some real data? One click in Redis Insight, and your pipeline is deployed to RDI so you can watch it in action.
- Verify the results: Redis Insight provides pipeline counters and performance statistics to see your pipeline health and performance. Want to go deeper? Connect to the target Redis database and have a closer look at the data.

### Streamlined pipeline creation

First, add your RDI endpoint in Redis Insight via the new “Redis Data Integration” tab. From there, you can manage your pipeline by:

- Downloading it from the RDI server if it’s already deployed.
- Uploading an existing RDI pipeline from a file.
- Creating a new pipeline from scratch using RDI templates for easy configuration.

![](/images/site-mirror/0649b2dc9f9d9d7a6bcbc08f1c2321fb9e328222-1600x944.webp)

### Pipeline configuration and testing

When creating a new RDI pipeline, Redis Insight auto-completes your configuration file. After specifying the configuration, you can test target database connections to verify your RDI instance writes data successfully.

![](/images/site-mirror/2e93f3be43b28b3e92aa03447d20840ab7d80293-1600x944.webp)

### Data transformation

RDI’s other main function is to map data from a source database to a Redis key type. There are two types of data transformations in RDI:

1. **Default transformation**: Each source row is automatically converted into a hash or JSON key in Redis, with the schema used to convert source columns to Redis hash fields or JSON types.
1. **Declarative transformation**: This advanced transformation is specified in YAML files, with each job containing transformations for source tables. These built-in transformations can be customized ‌to manipulate the data and map to additional Redis data structures (strings, sets, streams).

Redis Insight helps you create ‌jobs. Here’s how:

- Templates for easy job creation.
- Auto-completion and syntax highlighting for YAML files.
- Auto-completion and syntax highlighting for JMESPath and SQL functions in a dedicated editor.

![](/images/site-mirror/13f3d4df74c4b957d97137d85d1f8df5f01d16fd-1600x945.webp)

Once your data transformation job is ready, you can perform a dry run to view the transformation results without affecting your actual data. After finalizing the transformation jobs, you can download the pipeline to a file or deploy it to your RDI server using a dedicated deployment button.

### Monitoring and management

After deployment, navigate to the Statistics page in Redis Insight to view the current RDI engine status, target database configuration, and processing statistics broken down by stream. This overview lets you easily monitor your data integration pipeline.

![](/images/site-mirror/4152225f3c537aef0515882334307282edcd8cf3-1600x802.webp)

Plus, add your Redis database in Redis Insight to filter and visualize Redis keys, allowing you to track the data transformation results.

Redis Insight also gives you tutorials on [querying your data directly in Redis](https://redis.io/search/) in real-time, using Redis for common use cases, and many other tutorials to help you get the most out of Redis.

Want to start building faster apps using RDI?

[Talk to sales](https://redis.io/meeting/) to get started with [RDI](https://redis.io/docs/latest/integrate/redis-data-integration/).

Download Redis Insight for free from our [website](https://redis.io/insight/?utm_source=redisinsight&utm_medium=website&utm_campaign=install_redisinsight#insight-form).

## Related resources

#### post

### Redis Data Integration, now GA

We don’t just help you build fast apps. We help you do it fast. That’s why we’re excited to announce that Redis Data Integration (RDI) has arrived for…

#### page

### RedisInsight

Get the best in GUI Redis Insight is a powerful desktop user interface that helps you visualize and optimize your data for Redis and Redis Stack. Plus it…

#### page

### Meeting

Talk to our team Build better apps with our self-managed, on-prem software designed for enterprise compliance, reliability, and resilience. Work with our solutions architects to understand your requirements and…

![Close](/images/site-mirror/96e244338b2f3fee742526528445ee7fd0a56a5c-17x17.svg)

*(interactive chart, not available offline)*

*(interactive chart, not available offline)*

*(interactive chart, not available offline)*
