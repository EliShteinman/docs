---
title: "How To Use Google Cloud Dataflow to Ingest Data From Google Cloud Pub/Sub to Redis Enterprise"
linkTitle: "How To Use Google Cloud Dataflow to Ingest Data From Google Cloud Pub/Sub to Redis Enterprise"
url: "/blog/cloud-dataflow-pub-sub-to-redis/"
description: "Google Cloud Dataflow provides a serverless architecture that you can use to shard and process very large batch datasets or high-volume live streams of data in parallel. This short tutorial shows..."
date: 2023-04-11
blogCategories:
- "Tech"
authors:
- "Gilbert Lau"
lastmod: 2025-03-27
hidden: true
---

*By Gilbert Lau, Cloud Partner Solution Architect · Published 11 April 2023 · updated 27 March 2025*

![Blog tile image](/images/site-mirror/0d01fd3cb9170f91ed0ad4f58b8f034eb8e002b8-772x550.webp)

**Google Cloud Dataflow provides a serverless architecture that you can use to shard and process very large batch datasets or high-volume live streams of data in parallel. This short tutorial shows you how to go about it.**

Many companies capitalize on [Google Cloud Platform](/cloud-partners/google/) (GCP) for their data processing needs. Every day, millions of new data points, if not billions, are generated in a variety of formats at the edge or in the cloud. Processing this massive amount of data requires a scalable platform.

Google Cloud Dataflow is a fully-managed service for transforming and enriching data as a stream (in real time) or in batch mode (for historical uses), using Java and Python APIs with the Apache Beam software development kit. Dataflow provides a serverless architecture that you can use to shard and process very large batch datasets or high-volume live streams of data, and to do so in parallel.

A Dataflow template is an Apache Beam pipeline written in Java or [Python](/blog/how-to-build-a-powerful-search-engine-using-redis-python/). Dataflow templates allow you to execute pre-built pipelines while specifying your own data, environment, or parameters. You can select a Google-provided template or customize your own. The Google Cloud Dataflow pre-built templates enable you to stream or bulk-load data from one source to another such as [Pub/Sub](/blog/redis-cloud-expanded-programmability/), Cloud Storage, Spanner, SQL, BigTable, or BigQuery with an easy-to-use interface accessible via the Google Cloud console.

Redis Enterprise is used extensively across the Google Cloud customer base for many purposes, including [real-time transactions](/blog/how-to-create-a-real-time-mobile-banking-application-with-redis/), [chat/messaging](/solutions/messaging/), [gaming leaderboards](/solutions/leaderboards/), [healthcare claims processing](/industries/healthcare/), [real-time inventory](/solutions/real-time-inventory/), [geospatial applications](/glossary/geospatial-indexing/), and media streaming. As an in-memory database, Redis Enterprise consistently delivers millions of operations per second with sub-millisecond latency. Thus, Redis Enterprise perfectly complements many of the native Google Cloud managed services that drive real-time user experiences.

To give you a practical introduction, we introduce our custom template built for Google Cloud Dataflow to ingest data through Google Cloud Pub/Sub to a Redis Enterprise database. The template is a streaming pipeline that reads messages from a Pub/Sub subscription into a Redis Enterprise database as key-value strings. Support for other data types such as Lists, Hashes, Sets, and Sorted Sets will be built over time by Redis and Google experts, and perhaps by open-source community contributors.

## Our motivation: Let’s make this easy

We want developers to have a great experience with Google Cloud Dataflow and Redis Enterprise.

Using a pre-built template offers many benefits:

- You can run pipelines without the development environment and associated dependencies that are common with non-templated deployment. This is useful for scheduling recurring batch jobs.
- Runtime parameters allow you to customize the way a pipeline runs.
- Templates separate pipeline construction (performed by developers) from running the pipeline (which may be the responsibility of other personnel). Hence, there is no need to recompile the code every time the pipeline is run.
- Non-technical users can run templates using the Google Cloud Console, Google Cloud command-line interface, or the REST API.
- You can [extend templates with user-defined functions](https://cloud.google.com/blog/topics/developers-practitioners/extend-your-dataflow-template-with-udfs).

## How to use the Dataflow template: step-by-step

It helps to see how the process works, so here we walk you through the high-level workflow to show you how to configure a Dataflow pipeline using our custom template.

In this example, we process a message arriving at a pre-defined Pub/Sub subscription and insert the message as a key-value pair into a Redis Enterprise database.

From the Dataflow GCP console, enter a pipeline name and regional endpoint, and then select Custom Template. Enter gs://redis-field-engineering/redis-field-engineering/pubsub-to-redis/flex/Cloud_PubSub_to_Redis for the template path.

![A Google cloud template for adding the cloud dataflow to Redis enterprise](/images/site-mirror/cba9588b4e7f96b60c58711a94b80869a5070508-1824x1338.webp)

Next, enter the Pub/Sub subscription name that holds the incoming messages. Add the Redis Enterprise database parameters (e.g., Redis database host, Redis database port, and the Redis default user authentication password).

![A Google cloud template for adding the cloud dataflow to redis enterprise: create the pipeline from the template](/images/site-mirror/279f36ed5627999bfc93bd512a788517df4432a0-1986x1916.webp)

Choose Create Pipeline. The pipeline is now set to receive incoming messages. You may cheer, if you like to celebrate small victories.

You’re ready to publish a sample message to the Pub/Sub topic. Type in some sample data, and choose Publish.

![A Google cloud template for adding the cloud dataflow to redis enterprise: publish the message](/images/site-mirror/4a176df99a172b05c911b148796b19e9f62c8a92-1999x1040.webp)

Confirm that your sample data was published, if only for your own reassurance. To verify that the data was inserted into the Redis Enterprise database, you can use [Redis Insight](/insight/), a Redis GUI that supports command-line interaction in its desktop client.

![A Google cloud template for adding the cloud dataflow to redis enterprise: make sure it took.](/images/site-mirror/075915278b7a863b4814a7afbdb7ac8a9dfe6a04-1999x1345.webp)

## That’s just the start

The support model for this custom Dataflow template currently uses a community-based support mechanism. This means it is supported by the open source community on its [GitHub repo](https://github.com/redis-field-engineering/DataflowTemplates/tree/main/v2/pubsub-to-redis).

You are welcome to check out the open-source code and provide your feedback. We encourage you to add new features. Fork our GitHub repo and create a pull request when you are ready to contribute. Your support will make this project far more successful and sustainable.
