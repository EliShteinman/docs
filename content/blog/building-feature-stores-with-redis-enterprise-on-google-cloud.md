---
title: "Building Feature Stores with Redis Enterprise on Google Cloud"
linkTitle: "Building Feature Stores with Redis Enterprise on Google Cloud"
url: "/blog/building-feature-stores-with-redis-enterprise-on-google-cloud/"
description: "Every day, more and more companies are building feature stores for machine learning (ML) with Redis and Redis Enterprise as the online feature store. In previous blog posts, we shared use cases and..."
date: 2022-08-10
blogCategories:
- "Tech"
authors:
- "Nava Levy"
- "Gilbert Lau"
lastmod: 2025-07-03
hidden: true
---

*By Nava Levy, Gilbert Lau · Published 10 August 2022 · updated 3 July 2025*

![Blog tile image](/images/blog/e52cffc4ae0ae4a941d16aec9562a67df2a9536b-772x550.webp)

Every day, more and more companies are building [feature stores for machine learning (ML)](/solutions/feature-store/) with Redis and Redis Enterprise as the [online feature store](/solutions/feature-store/). In previous blog posts, we shared use cases and [benchmarks](/blog/feature-stores-for-real-time-artificial-intelligence-and-machine-learning/) illustrating how Redis Enterprise is the most performant and cost-effective online feature store for high throughput, low latency, or real-time use cases.

We also shared tutorials on running Redis with the popular open source feature store Feast, [locally](/blog/feast-with-redis-tutorial-for-machine-learning/), onGoogle[Colab](https://colab.research.google.com/drive/1MzieQE7h2BlVO6LT0IZGY9AozmhG1K9J?usp=sharing), and [Azure](https://techcommunity.microsoft.com/t5/ai-customer-engineering-team/bringing-feature-store-to-azure-from-microsoft-azure-redis-and/ba-p/2918917)—including with enterprise-grade Redis, thanks to the [Enterprise Tiers](https://docs.microsoft.com/en-us/azure/azure-cache-for-redis/quickstart-create-redis-enterprise) of Azure Cache for Redis. In addition, we explained why Redis OSS or AWS Elasticache is often not enough and why companies that are outgrowing their OSS or ElastiCache implementations are [upgrading to Redis Enterprise on AWS.](/blog/signs-youve-outgrown-elasticache/)


In this blog post, we focus on why leading companies, such as Feast co-creator [Gojek](https://www.cnbc.com/2021/06/09/goto-how-gojek-and-tokopedia-teamed-up-in-indonesias-biggest-merger.html), are migrating to [Redis Enterprise on Google Cloud](/blog/redis-enterprise-on-google-cloud-five-deployment-scenarios/). We also share a quickstart tutorial on **how to run Redis Enterprise with Feast on Google Cloud Platform (GCP).**

![diagram displaying feature store with google colab using redis enterprise](/images/blog/cebef0e194fd6988b79b2665b05e64d066185e50-1024x703.webp)

### Redis Enterprise as the online feature store on Google Cloud Platform

If you are already familiar with GCP, then Redis Enterprise on Google Cloud may be your best option. It’s not only the most performant database for online feature stores on GCP (see, for example, [benchmarks](https://feast.dev/blog/feast-benchmarks/) performed by Feast that compare Google Cloud Datastore to Redis), but it also provides you a fully managed option for your online feature store, allowing for simple management and scaling of Redis Cluster—a major benefit of [Redis Enterprise over Redis OSS](https://www.youtube.com/watch?v=osxzKxiznm4). In addition to the high performance and ease of management, Redis Enterprise on Google Cloud provides linear scalability and five-nines (99.999% SLA) availability, ensuring the online feature store is cost-effective at scale and experiences no downtime.

### Gojek upgrades its online feature store to Redis Enterprise

For these reasons, leading companies such as Indonesian ride-hailing service Gojek have upgraded from Redis OSS to Redis Enterprise on Google Cloud. Since then, Gojek has expanded into numerous new countries, transforming into a “super app” that provides more than 20 services, including an e-wallet service, food delivery, courier service, and more. It has become one of the most successful and fastest-growing technology companies, valued at more than $10B, with its [ML platform powering many of its use cases](https://www.gojek.io/blog/feast-bridging-ml-models-and-data).

Gojek is also the co-creator (together with Google Cloud) of [open source feature store Feast](https://cloud.google.com/blog/products/ai-machine-learning/introducing-feast-an-open-source-feature-store-for-machine-learning), which it launched in January 2019 using Redis OSS for its online feature store.

Feast is part of[ the Linux Foundation’s AI & Data Foundation](https://lfaidata.foundation/blog/2020/11/10/feast-joins-lf-ai-data-as-new-incubation-project/). Feast can serve features from a low-latency online store or an offline store while also providing a central registry, storage, and serving. This allows ML engineers and data scientists to discover the relevant features for ML use cases and serve them in production.

Today Feast has become the most popular open source feature store. It is deployed together with Redis as its online store in leading companies such as online mortgage company [Better.com](https://youtu.be/Vvfit9Slb8U), American FinServ company [Robinhood](https://www.tecton.ai/apply/session-video-archive/how-robinhood-built-a-feature-store-using-feast/), Indian B2B wholesale retailer platform [Udaan](https://hasgeek.com/fifthelephant/mlops-conference-july-2021/schedule/managed-feature-store-improving-data-reusability-providing-a-means-for-low-latency-real-time-prediction-at-udaan-HsZnfC4VUNdWUyJXXwfp5m), digital consulting company [Publicis Sapient](https://youtu.be/UJLQgxr_Za0), and many more—including, of course, Gojek itself. (For more details on Feast and its components, check out this [Feast with Redis overview](/blog/building-feature-stores-with-redis-introduction-to-feast-with-redis/), as well as the Feast documentation on Feast.dev.)

Since the launch of Feast, Gojek and its feature store have grown substantially in terms of scale and the number of use cases, to the point where the company has outgrown its Redis OSS implementation and moved to Redis Enterprise on Google Cloud instead. Gojek can now enjoy all the goodness of Redis OSS together with the benefits of Redis Enterprise: a fully managed cluster, five-nines availability, linear scalability, and other Redis Enterprise features such as Redis [modules](/redis-enterprise/modules/) and enterprise-grade security.

### Getting started with Redis Enterprise on Google Cloud with Feast

Now for a short overview of the quickstart tutorial on running Redis Enterprise on Google Cloud with open source Feast. Detailed explanations are available inside the tutorial itself on [Google Colab](https://colab.research.google.com/drive/1OfkAbpBOIbk5yOyOBuIPekA0AIsqvnUZ?usp=chrome_omnibox#scrollTo=p5JTeKfCVBZf).

The tutorial provides a step-by-step guide that walks you through using Feast with Redis Enterprise as its online feature store for ML on GCP. It’s based on the [Feast Quickstart tutorial](https://docs.feast.dev/getting-started/quickstart), but instead of using the default online store, it uses Redis Enterprise as its online store to deliver real-time predictions at scale. If you’re unfamiliar with Feast or Redis Enterprise on Google Cloud, then the fastest way to get started is by taking this helpful tutorial.

#### In this tutorial, you will:

1. Deploy a feature store Google Colab with a Parquet file offline store and Redis Enterprise on Google Cloud as its online store.
1. Build a training dataset using the demo time series features from the Parquet files.
1. Materialize (load) feature values from the offline store into the Redis Enterprise online store.
1. Read the latest features from the Redis Enterprise online store for inference.

You can run the tutorial on Google Colab by following the steps described in the [Colab notebook](https://colab.research.google.com/drive/1OfkAbpBOIbk5yOyOBuIPekA0AIsqvnUZ?usp=chrome_omnibox#scrollTo=p5JTeKfCVBZf).

#### Prerequisite for running the tutorial

To run this tutorial, you will need a [Redis Enterprise database instance](https://console.cloud.google.com/marketplace/product/redis-marketplace-isaas/redis-enterprise-cloud-flexible-plan/) from Google Cloud Marketplace. If you do not have an existing Redis Enterprise subscription through Google Cloud Marketplace, you can claim your FREE Google Cloud Marketplace [$400 credit](/lp/google-marketplace-offer/).

#### Tutorial scenario and steps

In this tutorial, we use feature stores to generate training data and power online model inference for a ride-sharing driver satisfaction prediction model. In the demo data scenario, we surveyed some drivers to determine how satisfied they are with their experience using a ride-sharing app. The goal is to generate predictions for driver satisfaction for the rest of the users so we can reach out to potentially dissatisfied users.

Tutorial steps:

1. Install Feast and verify your Redis Enterprise database in Google Cloud Marketplace.
1. Create a feature repository and configure Redis as the online store.
1. Register feature definitions and deploy your feature store.
1. Generate training data.
1. Load features into your Redis online store.
1. Fetch feature vectors for inference from Redis online store.

## What’s next?

In this blog post and accompanying Colab tutorial, we introduced you to Redis Enterprise as an online feature store on Google Cloud. We provided a quick introduction to the popular open source feature store Feast, as well as a step-by-step tutorial on how to set up Redis Enterprise on Google Cloud as the online store for Feast. To learn more about Redis Enterprise, check out the resource section of Redis.com for additional blog posts, ebooks, webinars, and more.

Go experience the speed and scalability of Redis Enterprise as the online feature store for your Feast deployment!
