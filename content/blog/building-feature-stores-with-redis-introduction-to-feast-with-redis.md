---
title: "Building Feature Stores with Redis: Introduction to Feast with Redis"
linkTitle: "Building Feature Stores with Redis: Introduction to Feast with Redis"
url: "/blog/building-feature-stores-with-redis-introduction-to-feast-with-redis/"
description: "A feature store is a centralized place where data scientists from different teams across your organization can share features) for machine learning. The feature store allows them to search, reuse,..."
date: 2021-11-09
blogCategories:
- "How To and Tutorials"
- "Tech"
authors:
- "Nava Levy"
- "Guy Korland"
lastmod: 2026-05-21
hidden: true
---

*By Nava Levy, Guy Korland · Published 9 November 2021 · updated 21 May 2026*

![Blog tile image](/images/blog/5af543d9cc9523d59491580a5efc4f91d2d9d6f3-772x520.webp)

A [feature store](/solutions/feature-store/) is a centralized place where data scientists from different teams across your organization can share [features](https://en.wikipedia.org/wiki/Feature_(machine_learning)) for machine learning. The feature store allows them to search, reuse, and serve features in production at scale. As MLOps matures, feature stores are becoming a cornerstone of machine learning platforms for a few reasons:

- Features are at the core what makes ML systems effective. Engineering these features is complicated and takes a tremendous amount of time. Features stores save time and improve ML system outcomes by allowing engineers to **reuse features** across different ML use cases.
- Feature stores let engineers reuse the same features across **training and production**, ensuring consistency and reproducibility of the engineered feature.
- **Low-latency feature serving** is key for real-time use cases. Feature stores serve features to ML models from an** online store** for real-time inference with low latency.

## Redis powers online feature stores

When companies need to deliver real-time, ML-based applications to support high volumes of online traffic, Redis is most often selected as the foundation for the online feature store, thanks to its ability to deliver ultra-low latency with high throughput at scale. We’re seeing ML cloud platform providers offer feature stores using Redis, as in the recent examples of [H2O AI Feature Store](https://www.h2o.ai/feature-store/) and Microsoft’s [Azure Feature Store](https://techcommunity.microsoft.com/t5/ai-customer-engineering-team/bringing-feature-store-to-azure-from-microsoft-azure-redis-and/ba-p/2918917). And we’re also seeing a host of build-your-own implementations of feature stores using Redis at a variety of companies including [Wix](https://youtu.be/E8839ENL-WY), [Swiggy](https://bytes.swiggy.com/enabling-data-science-at-scale-at-swiggy-the-dsp-story-208c2d85faf9), [Comcast](https://cdn.oreillystatic.com/en/assets/1/event/300/Automating%20ML%20model%20training%20and%20deployments%20via%20metadata-driven%20data%2C%20infrastructure%2C%20feature%20engineering%2C%20and%20model%20management%20Presentation.pdf), [Zomato](https://www.zomato.com/blog/elements-of-scalable-machine-learning), [AT&T](https://youtu.be/AXQt_oW9JEc), [DoorDash](https://doordash.engineering/2020/11/19/building-a-gigascale-ml-feature-store-with-redis/), [iFood](https://databricks.com/session_na20/building-a-real-time-feature-store-at-ifood), and [Uber](https://youtu.be/3Edcx1etACY).

These companies have huge datasets, with hundreds to thousands of features feeding ML systems of massive scale. Their Redis-backed feature stores support time-sensitive, mission-critical business applications, many for recommendation and fraud detection, using real-time data.

Open source feature store implementations such as Feast are also choosing Redis. Redis was selected as Feast’s online store for real-time use cases at scale, first by the Indonesian ride-hailing company [Gojek](https://youtu.be/DaNv-Wf1MBA?t=836) (who was the initial creator of Feast in collaboration with Google), and later by Feast’s early adopters, such as [Udaan](https://hasgeek.com/fifthelephant/mlops-conference/schedule/managed-feature-store-improving-data-reusability-providing-a-means-for-low-latency-real-time-prediction-at-udaan-HsZnfC4VUNdWUyJXXwfp5m) and [Robinhood](https://www.applyconf.com/agenda/how-robinhood-built-a-feature-store-using-feast/). In addition to that, Redis was selected by Microsoft for the online store of its new [Azure Feature Store with Feast](https://techcommunity.microsoft.com/t5/ai-customer-engineering-team/bringing-feature-store-to-azure-from-microsoft-azure-redis-and/ba-p/2918917) (stay tuned for more details on that soon!).

To provide a better understanding of how feature stores work, and why Redis is such a key feature store component, we’re going to use the rest of this article to introduce Feast and show how you can use it to build your own feature store with Redis.

## What is Feast?

Feast (**Fea**ture **st**ore) is an open source feature store that’s part of[the Linux Foundation’s AI & Data Foundation](https://lfaidata.foundation/blog/2020/11/10/feast-joins-lf-ai-data-as-new-incubation-project/). Feast can serve features from a low-latency online store or from an offline store, while also providing a central registry, storage, and serving. This allows ML engineers and data scientists to discover the relevant features for ML use cases and serve them in production.

![Redis + Feast diagram](/images/blog/b2f49d9316c1d0f588c59832b63f25edb271b138-1024x532.webp)

Feast is built in a modular way so that you can adopt all or some of its components. Because Feast is open source, you can deploy a [Feast Feature Store](https://drive.google.com/file/d/1ocJNDbEUxXVJqyBVD35k-Vvr1y8hjN5k/view) and customize it for your own needs, without having to start building a feature store from scratch. Companies who choose Feast with Redis for their feature store have significantly shortened development time and effort, as compared to building out their own feature store. In the next section, we’ll go over Feast’s key components.

## Feast architecture and key components

If you look at the Feast architecture diagram below, you’ll notice several key components:

**Feast registry:** Feast registry is an object store-based registry, which is a central catalog of all of the feature definitions and their related metadata. This registry allows data scientists to search, discover, and collaborate on new features. The registry also allows for programmatic access through the Feast SDK.

**Feast Python SDK/CLI:** The SDK is the primary user-facing tool for managing version-controlled feature definitions, materializing (load) feature values into the online store, building and retrieving training datasets from the offline store, and serving online features.

**Online Store:** The online store is a database that stores only the latest feature values for each entity. The online store provides low-latency online feature value lookups. Feast allows users to load or materialize their feature data into an online store in order to serve the latest features to models for online prediction.

**Offline Store:** Offline stores maintain a record of historic time-series feature values. The offline store persists batch data that has been ingested into Feast. This data is used for producing training datasets. Feast does not manage the offline store directly, but runs queries against it.

![Redis + Feast diagram](/images/blog/aa02301cf1a38ddf8ec80947442a2d443b64f3d3-1019x1024.webp)

The high-level architecture diagram above describes the following flow, as an example:

1. A data/ML engineer creates the features using their preferred tools. These features are ingested into the offline store.
1. The data/ML engineer (or CI/CD process) can persist the feature definitions into a central registry.
1. The data/ML engineer (or CI/CD process) can materialize (load) features into Redis (online store).
1. The ML engineer or data scientist consumes the offline features to train a model.
1. The ML engineer or data scientist deploys the model for production for serving.
1. The backend system makes a request to the inference server endpoint, which makes a request to Redis, the online store, to get the online features.

You can find more details on Feast, including its concepts, architecture, and releases, at [feast.dev](http://www.feast.dev). Next, let’s see how to quickly get started with building your own feature store using Feast with Redis.

## Start using Feast with Redis

Choosing Redis as the online store for Feast (for Feast versions >= v0.11) takes just a couple of lines of configuration: Define the online_store in the Feast YAML configuration file, setting the type and connection_string values in feature_store.yaml as follows:

```javascript
project: fraud
registry: data/registry.db
provider: local
online_store:
  type: redis
  connection_string: localhost:6379
```

By adding these two lines for online_store (type: redis, connection_string: localhost:6379) in the YAML configuration file, Feast will use Redis as its online store.

We just showed how to connect a **single Redis instance** to Feast. If you’re using a **Redis open source cluster** with SSL enabled and password authentication, you’ll need to use a [different connection_string value](https://docs.feast.dev/reference/online-stores/redis).

See the [Feast documentation](https://rtd.feast.dev/en/master/#feast.infra.online_stores.redis.RedisOnlineStoreConfig) for a full listing of the configuration options for Redis. You can also consult the [Feast online store format](https://github.com/feast-dev/feast/blob/master/docs/specs/online_store_format.md) to better understand the data model used to store feature values in Redis.

## How to learn more

At Redis, we’re committed to making Feast faster and more reliable for delivering real-time ML use cases at scale. For the recent [Feast v0.14 ](https://github.com/feast-dev/feast/releases/tag/v0.14.0?utm_medium=email&_hsmi=2&_hsenc=p2ANqtz-_SRbQBIYoNaQy52TkMXq2lKT_ecbGJl8XLJ9pj8_bBN8iXvgogVFIY3hBNoyv5eEpukwSNmj4fAdSE9ckLcJzhi_dZsg&utm_content=2&utm_source=hs_email)release, we were thrilled to help the [core online serving path become 30% faster!](https://groups.google.com/g/feast-dev/c/D0IHN_DALFA?pli=1)

For next steps, we recommend learning about how and for which uses cases companies are using features stores with Redis for the online store ([Wix](https://youtu.be/E8839ENL-WY), [Swiggy](https://bytes.swiggy.com/enabling-data-science-at-scale-at-swiggy-the-dsp-story-208c2d85faf9), [Comcast](https://cdn.oreillystatic.com/en/assets/1/event/300/Automating%20ML%20model%20training%20and%20deployments%20via%20metadata-driven%20data%2C%20infrastructure%2C%20feature%20engineering%2C%20and%20model%20management%20Presentation.pdf), [Zomato](https://www.zomato.com/blog/elements-of-scalable-machine-learning), [AT&T](https://youtu.be/AXQt_oW9JEc), [DoorDash](https://doordash.engineering/2020/11/19/building-a-gigascale-ml-feature-store-with-redis/), [iFood](https://databricks.com/session_na20/building-a-real-time-feature-store-at-ifood), [Uber](https://youtu.be/3Edcx1etACY)), and specifically how they’re using Feast with Redis ([Gojek](https://youtu.be/DaNv-Wf1MBA?t=836), [Udaan](https://hasgeek.com/fifthelephant/mlops-conference/schedule/managed-feature-store-improving-data-reusability-providing-a-means-for-low-latency-real-time-prediction-at-udaan-HsZnfC4VUNdWUyJXXwfp5m), [Robinhood](https://www.applyconf.com/agenda/how-robinhood-built-a-feature-store-using-feast/)). We also recommend reading about the new [Azure Feature Store for Feast](https://techcommunity.microsoft.com/t5/ai-customer-engineering-team/bringing-feature-store-to-azure-from-microsoft-azure-redis-and/ba-p/2918917) and checking out the quick-start tutorials on [Azure GitHub repo](https://github.com/Azure/feast-azure).

We hope you’ve enjoyed this introduction to using Feast with Redis. We’ll be posting more resources soon, but if you have any feedback or questions, please [don’t hesitate to contact us](mailto:featurestore@redis.com).
