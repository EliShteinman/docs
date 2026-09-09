---
title: "Feature Stores Explained: The Three Common Architectures"
linkTitle: "Feature Stores Explained: The Three Common Architectures"
url: "/blog/feature-stores-explained-the-three-common-architectures/"
description: "Over the last three years, MLOps practitioners have recognized feature stores as a high value category in MLOps software. Despite their recent surge in popularity, feature stores existed long..."
date: 2022-11-30
blogCategories:
- "Tech"
authors:
- "Simba Khadder"
lastmod: 2026-05-29
hidden: true
---

*By Simba Khadder, Head of Context Engine at Redis. · Published 30 November 2022 · updated 29 May 2026*

![Feature Stores Explained: The Three Common Architectures](/images/site-mirror/a155c461bbe0fc70e642021756e0db3751c86168-2000x1396.webp)

![Redis](/images/site-mirror/a155c461bbe0fc70e642021756e0db3751c86168-2000x1396.webp)

## Introduction

Over the last three years, MLOps practitioners have recognized feature stores as a high value category in MLOps software. Despite their recent surge in popularity, feature stores existed long before the term 'feature store' was even coined. Companies like AirBnB, Uber, and Twitter built their primordial feature stores at the same time, and arrived at three distinct architectures which we have dubbed: literal, physical, and virtual.

We wrote this article to define the literal-physical-virtual framework. Using it, we can clarify the key architectural choices made by prominent feature stores and study their benefits and drawbacks.

## Goals of all Feature Stores

Before we start categorizing feature stores, let’s first define their motivations. MLOps has four goals: decrease model iteration time, increase model reliability, preserve compliance, and improve collaboration. As a part of the MLOps stack, a feature store helps an organization achieve these goals. It enhances the data analysis and transformation cycles of the machine learning process.

### Decrease Iteration Time

![Goals of all Feature Stores](/images/site-mirror/443e6af223a77454a22524c82e244a776d0786ba-1226x864.svg)

*The iteration cycle is made up of multiple experimentation loops with occasional deployment loops*

Machine learning is an iterative process. Models are black boxes, so enhancements on them are non-linear and opaque. To improve model performance, data scientists extract useful insights from primary data sources (i.e. feature engineering) and provide them as features to the model. In many machine learning use cases, especially on tabular and text data, data scientists spend most of their time fine tuning features. The faster a data scientist can iterate on features, the faster they can improve their models.

There are two iteration cycles to optimize: experimentation and deployment. Multiple experimentation cycles happen per deployment, so feature stores should optimize both.

### Experimentation

A feature store should aim to organize experimentation cycles. During experimentation, data scientists may end up creating dozens of notebooks to create hundreds of different data sets. Organization among the notebooks and datasets is ad-hoc, and documentation is often sparse. A feature store enforces standards for creating, naming, and documenting features.

### Deployment

A feature store allows a data scientist to deploy their feature logic into production. Rather than having to re-write their experimentation logic, they can deploy it as is. This saves time and removes potential human error. A feature store also provides other essential functionality such as data monitoring, version control, and access control.

### Increase Reliability

Feature stores limit the pool of possible errors to increase reliability. To visualize this, imagine a feature that’s stored in Redis for inference, S3 for training, and created through a directed acyclic graph (DAG) of transformations via Spark. The source data streams through Kafka and replicates into S3 to allow streams to be replayed later. In this common pattern, data scientists write feature logic twice. Their logic is often split across different jobs in a DAG. Many things can go wrong. Data scientists not only have to be great with data, they also have to be amazing DevOps and DataOps practitioners. A feature store abstracts DataOps and DevOps such that it fits naturally in the machine learning process. It removes most of the data engineering overhead required by data scientists to do their job.

### Preserve Compliance

![Preserve Compliance](/images/site-mirror/2ff0ee5b36e95bb0ba81045f6c6ef407c5b421af-1108x814.svg)

*Not all models may have access to all features*

Many machine learning use cases work with sensitive data where preserving compliance is paramount. Across an organization, some data is strictly regulated while others can be used freely. Even with the same data, context can change compliance rules. For example, if someone is in the EU, they’re subject to a different set of regulations. The same data used in separate models would also be subject to different rules. For example, a model used for ads optimization can probably use more data than a model used to process housing loan applications. A data scientist can integrate these rules into the feature store to make sure that governance is locked tight.

### Improve Collaboration

Feature stores promote sharing and communicating within and across teams. In data science workflows without them, notebooks are siloed and transformations and features are often copied and pasted. Feature stores ensure that transformations are defined in a standardized form. Data scientists can then more easily share and understand each other's work. Furthermore, by storing these definitions in a centralized repository, data scientists can explore and leverage each other's resources. Feature lineage allows data scientists to understand the steps taken to create each feature. By making transformation and feature logic immutable in a feature store, resources can be reused without risk of upstream logic changing. This allows data scientists to safely leverage resources from other teams.

## The Anatomy of a Feature

![The Anatomy of a Feature](/images/site-mirror/4c1d0fc3c68c6fc1ecc9dfbec5d6c03524168325-1706x1070.svg)

*The anatomy of a user's average purchase price feature*

A data scientist will think of a feature in its logical form. Something like: “a user’s average purchase price”. In reality, the feature’s definition is split across different pieces of infrastructure: the data source, the transformations, the inference store, the training store, and all their underlying data infrastructure. A feature store should provide an abstraction to join a feature's logical form with the actual underlying components. We will explain what the components might look like for the “user’s average purchase price” example.

### The Data Source

![The Data Source](/images/site-mirror/0dfd1b10209e7a063287f7c17907839be75aeb9c-1707x1070.svg)

*The feature's data source*

All features originate from a set of initial data sources. These sources can be anything from streams to files to tables. A feature can simply be a single field of a data source. More commonly, it’s created via a set of transformations from one or multiple sources. In this example, the data source is a CSV with three columns: user, price, and date.

### The Transformation Logic and Lineage

![The feature's transformation](/images/site-mirror/6c3bc810d8537825fe5eecfac20cc970c0b7ca69-1707x1070.svg)

*The feature's transformation*

Features can be created through a series of transformations on a dataset. These transformations can be anything from SQL queries to PySpark jobs to local python functions. Transformations can be chained together and form a directed acyclic graph (DAG). This DAG is often the closest thing to the logical form of a feature. In the example above, it’s a simple SQL query.

### The Inference (Online) Table

![The feature's inference store](/images/site-mirror/304ba37e32f4ad4cb16c09ab09cad842b7c12c6a-1707x1070.svg)

*The feature's inference store*

Deployed models need to be able to access the current values of their features for inference. Inference use cases are often very sensitive to latency. It’s typically infeasible to generate a feature for the models at point of time. Rather, features are pre-processed and stored in low-latency storage.

If this example feature was used millions of times a day and if the original data source was billions of rows, it’d be impractical to run an ad-hoc query to generate the feature. It’d be too slow and expensive. To avoid this, the feature can be constantly pre-processed. Its storage, or cache layer, is the inference store.

### The (Offline) Training Store

![The feature's training store](/images/site-mirror/bf700ebd93e681ff7c4b0d05e5f6dd55db91719e-1707x1070.svg)

*The feature's training store*

Features also exist in one or multiple training sets. A training set consists of a label (what the model aims to predict) and a set of features associated with it. When training, the focus is on throughput and the training set API. It’s common to loop through a dataset multiple times, sample the dataset, and update it with more data. This type of iteration can be accomplished with a set of files in object storage or an analytics database.

Point-in-time correctness is critical when building training sets. The value of a feature should be exactly as it would have been at the point in time of the label. In this example, if a label was set for Jan 2nd, the corresponding feature for “Alex” should be $10. If it was pulled from the inference store, it would be incorrect. Generating point-in-time correct features is difficult, and we will have another blog post coming out addressing exactly this problem.

### The Infrastructure Providers

![The feature's infrastructure providers](/images/site-mirror/455b9ced5ca82b8404abb15022347666d66e564b-1706x1070.svg)

*The feature's infrastructure providers*

The components above depend on storage and compute. The original data needs to be stored somewhere. It could be in a table in Snowflake, a directory in HDFS, or even a local filesystem. Transformations need a compute provider to run them. It could be Dask, Spark, Snowflake, Flink, or a combination. The training set and inference store need underlying infrastructure providers. In this example, the data starts in S3, is transformed with Spark, and stored in S3 for training and Redis for inference.

## The Feature Store Abstraction

A feature store’s goal is to allow a data scientist to define their features as closely as possible to its logical representation. The feature store maps this logical form to the real components that make it up. There are three common design patterns for feature stores: literal, physical, and virtual.

Literal feature stores act as a centralized storage of feature values. Data scientists use their data pipelines to compute features and store all of them in the feature store. They use the feature store’s API to train and serve features to their models.

Physical feature stores both compute and store feature values. They unify the computational steps required to generate a training set and current feature values for inference allowing a single feature definition to be used. They essentially replace infrastructure like Spark and Redis with something built from the ground up for machine learning use cases.

Virtual feature stores turn existing data infrastructure into a feature store. They centralize and standardize feature definitions while distributing compute and storage amongst a heterogeneous set of providers. They solve the organizational problems around building and maintaining features, while maintaining a low adoption cost and high flexibility.

There is no one-size-fits-all feature store. All come with their own pros and cons. As the MLOps space matures, we expect to see different feature store architectures to fit their way into different MLOps stacks, and the vocabulary we use to talk about MLOps to further specialize.

## Literal Feature Store

By name alone, a feature store implies that it would store pre-processed features. A literal feature store stays true to this implication, It only provides storage for features, hence the name “Literal” feature store. It does not manage anything related to computing and creating features.

### The Architecture

The literal feature store looks like a specialized data store. Features are written to the feature store after being processed by the user’s own infrastructure. The feature store serves features to models for inference and generates point-in-time correct training sets.

![The Literal Feature Store Architecture](/images/site-mirror/d175ba2169cca58d596dbc17ddbf3e87d32e7d22-1676x901.svg)

*The Literal Feature Store Architecture*

### Analysis

By design, literal feature stores do not manage your transformations, making them the lightest weight of the three feature store architectures. Adoption cost is low. Data scientists simply point their data pipelines at a new storage layer. The pipelines use the API to write data to the store, which then serves the data to models. In return, data scientists get point-in-time correctness of their features and a cleaner serving abstraction.

### When is this the right choice

If a team’s data scientists are happy with how they build, maintain, and version their data pipelines, they may just want a purpose-built storage layer for production features. In this situation, a literal feature store is likely the right choice.

The pros and cons of this architecture are highlighted when examining the process to change a feature.It happens in three steps:

1. Write and run your new data transformation in your existing transformation pipeline. Note that this happens outside of the literal feature store.
1. A new feature table must be created, since the old one cannot be directly overwritten. Once the new feature is created, the transformation pipeline should pipe all of its data into it.
1. All the models that use this new feature should be updated to point at the new feature.

### Examples

The most popular feature store with this architecture is Feast. In this architecture, transformations are initially all written to an offline store. The user of Feast must then manually materialize the features into the online store. Feast mimics a virtual feature store by having its offline and online stores sit above existing storage infrastructure. It passes responsibility of generating the features to the data scientist’s data pipelines. Feast acts similarly to its underlying storage providers, but also generates point-in-time correct features based on the final feature values.

![Feast Architecture, a literal feature store](/images/site-mirror/8d222a783f62c2425169ec03275c88211e952ec4-1225x1227.webp)

*Feast Architecture, a literal feature store*

([source](https://docs.feast.dev/getting-started/architecture-and-components/overview))

## Physical Feature Store

The physical feature store computes and stores your features. It is the most common type of feature store found among vendors and in-house feature stores. It has its own domain-specific language to define transformations and its own storage layer to store and serve features.

### The Architecture

The physical feature store consists of a metadata layer, an inference store, a training store, and a transformation engine. Unlike a virtual feature store, the physical feature store comes with its own storage and transformation layer. It replaces existing data infrastructure.

![The Physical Feature Store Architecture](/images/site-mirror/88fdfc6abef17e64231785cc012dd87a2d2bc2af-1822x938.svg)

*The Physical Feature Store Architecture*

### Analysis

This architecture comes with the most functionality and high performance. However, it also comes with the highest adoption cost and least flexibility. The user does not have the luxury of customizing their infrastructure - they are locked into the physical feature store’s provider. By owning the transformation layer, a data scientist doesn’t have to work across different data infrastructure like Airflow, Spark, and Flink. A physical feature store aims to be at a similar abstraction layer to Spark, but optimized for the feature creation process.

It aims to take on the problems that arise with processing features. This includes handling streaming data, optimizing window transformations, and providing low latency feature serving.

### When is this the right choice

This architecture is the right choice for teams struggling to process streaming data and meeting latency and processing requirements. When building an in-house physical feature store, teams must weigh the cost of building and maintaining a large data infrastructure in-house with the value it provides. When working with a vendor, a team must determine if rewriting their features and replacing their existing infrastructure is worth the return on investment.

### Examples

Most of the popular in-house feature stores like AirBnB’s Zipline, Lyft’s Dryft, and Uber’s Michelangelo adhere to this architecture. Much of their motivation for building their feature stores originated from problems processing existing features.

Before:

![A Real-World Architecture before adding a Physical Feature Store](/images/site-mirror/90ed8606a0bd335b503e469ac0e81b3a115e5390-1600x838.webp)

*A Real-World Architecture before adding a Physical Feature Store*

([source](https://www.datagrom.com/data-science-machine-learning-ai-blog/feature-store-uber-ai-large-scale-machine-learning))

After:

![A Real-World Architecture after adding a Physical Feature Store](/images/site-mirror/9008e31d88c96646a084a16556dea8ca91d64f68-1600x838.webp)

*A Real-World Architecture after adding a Physical Feature Store*

([source](https://www.datagrom.com/data-science-machine-learning-ai-blog/feature-store-uber-ai-large-scale-machine-learning))

You can see in this model that Tecton, which is based on Uber’s Michaelangelo architecture, provides a framework to run and store your feature pipelines. Unlike a literal feature store, this physical feature actually runs the transformations, even in complex streaming use cases.

## Virtual Feature Store

The virtual feature store aims to solve a subset of the problems of a physical feature store, without the high adoption cost and with more flexibility. Unlike the literal feature store, virtual feature stores still manage transformations. However, in contrast to a physical feature store, a virtual feature store coordinates and manages the transformations rather than actually computing them. The computations are offloaded to the organization's existing data infrastructure. A virtual feature store is more akin to a framework and workflow, than an additional piece of data infrastructure. It transforms your existing data infrastructure into a feature store.

### The Architecture

The virtual feature store is made up of a metadata layer, an inference store, a training store, and a coordinator. Like some literal feature stores, the training store and inference store sit on top of existing data infrastructure. The coordinator’s goal is to put the underlying infrastructure in the same state defined in the metadata. For example, if a user defines a feature as a series of PySpark jobs, it’d be the coordinators job to make sure the jobs are successfully run. In this way, it will often replace an existing orchestrator like Airflow for feature creation use-cases.‍

![A Virtual Feature Store’s Architecture](/images/site-mirror/166b221609e01535ecb7386a7c8ea2492d41803a-1600x1117.webp)

*A Virtual Feature Store’s Architecture*

### Analysis

A virtual feature store aims to solve the organizational problems machine learning teams face when working with features. It manages the metadata of all features, from their names, versions, descriptions, owners, providers, transformation logic and more. Rather than working directly with the APIs of their data infrastructure, data scientists can work with an abstraction that is built for their workflow. Features become a first class component of the machine learning process.

Unlike a physical feature store, the actual transformation code does not have to be re-written into a custom DSL. Rather, the virtual feature store’s API requires data scientists to specify names, version, descriptions, owner, providers, and other metadata needed to create and manage the features.

The virtual approach allows teams to choose the right infrastructure to meet their needs, while maintaining the same abstraction. For example, if you deal heavily with streaming data, you may want to leverage Flink. The virtual approach supports that choice while maintaining the same abstractions. You can also mix and match infrastructure for different use cases in the organization, but interact with them all with the same abstraction.

#### When is this the right choice

This architecture offers a number of advantages to teams who want to transform their existing data infrastructure into a feature store. The workflow creates a consistent versioning scheme, and centralizes the feature definitions, while allowing their actual execution and storage engines to be distributed. It allows data scientists to explore the feature’s metadata, including its owner, transformation lineage, and any training sets it belongs to.

The virtual feature store architecture is often the correct choice for organizations with heterogeneous data infrastructure. The physical feature store is inherently centralized, it performs all the compute and storage. The literal feature store is also centralized, with all of the features stored in one central place. In a virtual feature store, the feature definitions are centralized, but the actual infrastructure is not. It enables this architecture to achieve the same organizational benefits, while keeping the technical benefits of your existing data infrastructure.

### Examples

At Triton, we pioneered this architecture. We realized that our biggest problem was related to organization and workflow, and not with the actual infrastructure we were using (Pulsar and Flink). We came to the conclusion the ML teams want a workflow, not more data infrastructure, and built a feature store around that premise. Featureform was built from the ground up from everything we learned building that original virtual feature store.

## Conclusion

As time has progressed, the focus of MLOps has shifted from infrastructure to workflows. Computation is not the issue anymore, as infrastructure providers like Spark, Snowflake, and Redis have improved to handle heavier machine learning workloads. The problem is that these providers’ workflows are not optimized for the machine learning process.This realization spawned the Virtual Feature Store approach, the newest of the three architectures. The broad range of problems faced by machine learning teams requires an equally wide variety of MLOps solutions. As data infrastructure continues to evolve, the virtual feature store could very well become the de-facto architecture. The main goal of MLOps will be about coming up with a machine learning workflow that just, simply put, works. That’s why we built (and open-sourced) Featureform. Also, if these problems sound interesting to you, we’re hiring!
