---
title: "Introduction to Redis Enterprise on OpenShift"
linkTitle: "Introduction to Redis Enterprise on OpenShift"
url: "/blog/introduction-redis-enterprise-openshift/"
description: "Here’s a brief introduction to Red Hat OpenShift, including questions we often get asked and our thoughts on why it’s a great choice for deploying and running your Redis Enterprise Cluster."
date: 2019-08-21
blogCategories:
- "Tech"
authors:
- "Redis  "
lastmod: 2025-03-27
hidden: true
---

*By Redis   · Published 21 August 2019 · updated 27 March 2025*

![Blog tile image](/images/site-mirror/0a6fc94b9a9740543293927deb92fc524b3a03ea-386x260.webp)

Here’s a brief introduction to Red Hat OpenShift, including questions we often get asked and our thoughts on why it’s a great choice for deploying and running your Redis Enterprise Cluster.

## What is OpenShift?

There are a few pieces of background you should have before I can properly answer that question, so let me start with a simple definition and then progressively fill in the details.

**OpenShift is Red Hat’s Platform-as-a-Service (PaaS) offering for running containerized applications based on **[**their Kubernetes distribution**](https://www.okd.io/)**.**

### What is a Platform-as-a-Service (PaaS)?

PaaS is a category of cloud computing services that allows customers to deploy and run applications without having to worry about many operational details. With an Infrastructure-as-a-Service (IaaS) offering, you pay for computing units (be it bare-metal servers or virtual machines), and then it’s up to you to properly install all the necessary software and operate it over time. With PaaS, you don’t need to spend resources or expertise on operating your infrastructure. To support this level of automation, OpenShift makes use of Kubernetes.

### What is Kubernetes?

Kubernetes is an open source container-orchestration system for automated provisioning, scaling and management of your apps and services. In other words, Kubernetes runs clusters of services for you. It was open sourced by Google and is now part of the Cloud Native Computing Foundation (CNCF). You can think of OpenShift as a distribution of Kubernetes, however keep in mind that OpenShift is a product, while Kubernetes and its various distributions are just projects. When you install Kubernetes, it’s up to you to figure out how to set it up correctly, and if something doesn’t work, you can count on community support at best. OpenShift, being a product, bundles access to Red Hat’s support. This might seem like a small difference to some, but it’s hugely important for enterprises. OpenShift is based on a [Kubernetes distribution called OKD](https://www.okd.io/).

### What is OKD and what are Kubernetes distributions in general?

OKD is Red Hat’s open source distribution of Kubernetes that powers OpenShift. As mentioned above, OKD is the open source *project*, while OpenShift is the *product*. A distribution of Kubernetes includes core Kubernetes components plus an opinionated choice of tooling that surrounds the core engine. In many ways, it’s the same thing that happens with Linux distributions: the kernel is Linux, but all the components around it differ depending on the choices of the respective maintainers. OKD, for example, has a different way of specifying the desired layout of a service cluster compared to vanilla Kubernetes (OKD templates vs. Helm charts).

### What are the benefits of using OpenShift?

First of all, we must talk about the benefits of using Kubernetes in general. With Kubernetes, developers gain a self-service interface for orchestrating resources. When a developer writes code for their application, they also write any infrastructural requirements (e.g., databases, caches, load balancers) into a configuration file. This file is then checked into a source-control repository with the rest of the code.

Developers that use this method don’t need deep operational knowledge because Kubernetes handles the details for them. After that, running the infrastructure is just as easy. Any change applied to the aforementioned configuration file will then be used by Kubernetes to infer the desired cluster state. Kubernetes knows how to assess the current cluster state and determine which operations to apply in order to transition towards the desired state. This also applies, for example, to horizontal scaling when the developers can simply changes the number of desired replicas of a given service.

The benefits of using OpenShift relate to Red Hat’s expertise running open source services and infrastructure. OpenShift is purpose-built for a great Kubernetes experience, starting from the operating system (OS) itself. OpenShift 4 (the latest version to date) is optimized to run on CoreOS, a Linux distribution specialized to run containerized applications (acquired by Red Hat in January 2018). OpenShift also features tools that are missing from vanilla Kubernetes, such as a web control panel for service deployment and monitoring, an integrated CI/CD system and many others.

## Why Redis Enterprise on OpenShift?

Redis Enterprise Cluster helps you scale linearly to millions of operations per second. [We can manage it for you](/pricing/), so you don’t need Kubernetes for that. That said, if you are already investing in the Kubernetes ecosystem and want your developers to have the same self-service access to Redis Enterprise as any other resource, we have great support for OpenShift through the [Operator Framework](https://kubernetes.io/docs/concepts/extend-kubernetes/operator/).

Kubernetes needs to manage many different kinds of resources in a highly automated way, but it can’t know how to run everything right out of the box. The Operator Framework is a way of extending Kubernetes by adding custom logic specifically designed to manage a single type of resource. At Redis, we have created and maintain an operator for Redis Enterprise that you can easily get from the [OperatorHub](https://operatorhub.io/operator/redis-enterprise), OpenShift’s marketplace for operators.

Once you set it up, you will then be able to focus on what you really care about: developing your applications. Redis Enterprise can help you consolidate your existing architecture and expand to new possibilities like deploying a geo-distributed multi-master database cluster. For more information on design patterns for replication, [take a look at Sheryl Sage’s guest post on the official OpenShift blog](https://blog.openshift.com/building-modern-distributed-applications-with-redis-enterprise-on-red-hat-openshift/).

## Next steps

To learn how to use the Redis Enterprise Cluster operator on OpenShift, [read this how-to by Amiram Mizne](/blog/install-redis-enterprise-clusters-using-operators-openshift/), checkout our [documentation](https://docs.redis.com/latest/platforms/openshift/) or [sign up for a free OpenShift trial](https://www.openshift.com/).
