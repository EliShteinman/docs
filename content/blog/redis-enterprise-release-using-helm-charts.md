---
title: "An Introduction to the Helm Tool and Helm Charts"
linkTitle: "An Introduction to the Helm Tool and Helm Charts"
url: "/blog/redis-enterprise-release-using-helm-charts/"
description: "Manual deployments of Kubernetes clusters can be a real hassle. Installing and maintaining a cluster is a complex task unless there are automations to fast-track the process, and the potential for..."
date: 2022-09-12
blogCategories:
- "Company"
- "How To and Tutorials"
authors:
- "Angel Camacho"
lastmod: 2025-03-27
hidden: true
---

*By Angel Camacho, Contributor · Published 12 September 2022 · updated 27 March 2025*

![Blog tile image](/images/blog/0e4ddcbb08c5955d84fbd3d2fdedf94e99ec5c1a-772x550.webp)

**Manual deployments of Kubernetes clusters can be a real hassle. Installing and maintaining a cluster is a complex task unless there are automations to fast-track the process, and the potential for error is high. To mitigate these complications is Helm, a Kubernetes package manager, and Helm charts, a blueprint that defines how clusters are deployed. We explore the pros and cons of a Redis Helm chart as well as how the new Redis Enterprise Operator for Kubernetes solves most of the pain points that arise with using the Helm package manager.**

## How Helm works

Developers rely on open source interfaces like [Kubernetes](/enterprise/redis-enterprise-on-kubernetes/) to manage and deploy containerized applications. Applications and services run in a **container** and are deployed in a [**cluster**](/redis-enterprise/technology/redis-enterprise-cluster-architecture/)**.** Keeping everything working right is a process that requires attention to detail. There’s a lot to keep track of: managing configurations, using the proper commands, choosing the correct values, and packaging the right application files. It’s easy to get wires crossed.

**Helm** is an open source Kubernetes package manager that uses configurations and the defined values within manifest files to enable the efficient deployment and installation of an application or service in a cluster.

Developers use these manifest files to specify every configuration necessary for a successful deployment. These are executed with commands using a [command line interface](/blog/get-redis-cli-without-installing-redis-server/) (CLI).

But to deploy a single container, a developer only needs a simple manual process. Once the need for multiple containers arises, it’s probably best to begin executing with configuration files. If your architecture requires a cluster (which may need multiple containers or pods), those configuration files are best folded into a **Helm chart**.

Get started by performing a [Helm install](https://helm.sh/docs/intro/install/).

### Helm charts

To properly install an application in a Kubernetes pod or cluster, you need the set of pre-configured resource definitions that come packaged in a **Helm chart**. This chart contains the customized information for many scenarios: everything from running anything from a small application to a complex database within a cluster.

Helm charts are a sound choice for development teams. The developers can sidestep deploying from scratch and start with a bespoke configuration that reduces the risk of misconfiguring resources.

Helm charts are stored in a **repository**. A chart repository enables Helm to break down the workplace silos that encumber development teams by storing the resource definitions in a central hub.

A chart may even depend on another chart. Nesting a chart within another creates a synchronized **dependency**. Helm makes it easy for developers to manage any dependency in a chart, which provides the URL for the chart repository server storing templated files.

Once a chart runs an instance (when it adds a pod to the network), it creates a **release**. For every running instance, there is a release. (We explore a Redis instance and release in more detail below).

In short: A chart enables streamlined deployments of regularly used and repeatable applications and services in a cluster.

## Redis Enterprise release

Redis has deployed hundreds of clusters in Kubernetes. From the beginning, we realized that a manual process would not cut it. The first issue is to make Redis cluster deployments easier to reproduce; it’s also a matter of scaling operations. We needed the ability to deploy a Redis cluster in a single Helm CLI line.

### Redis Enterprise Operator for Kubernetes

So far, we’ve covered how charts accelerate productivity, allowing developers to cut corners guilt-free. Here are a few other benefits worth highlighting.

### Advantages of using Helm charts

- They’re simple: Reduces deployment complexity down to a single Helm CLI command
- They’re reproducible: Allows deployments to be repeatable, predictable, and efficient across various environments, including [cloud](/redis-enterprise-cloud/overview/)
- They’re streamlined: Enables new team members to get up to speed on existing projects
- They’re organized: Maintains and automatically versions past configurations executed with Helm
- They’re flexible: ‘Package’ command shares a chart with the Helm repository, where it’s easily accessed by anyone on the project

### Where Helm charts fall short

It’s not uncommon for an application to need a cluster for every stage of its lifecycle – and those lifecycles only grow more challenging the more intricate applications become.

The Helm package manager is an excellent tool for setting a workable, reproducible foundation for a cluster. Still, it won’t provide automatic failover when a cluster has maxed out its resources. Clusters change over time. Perhaps it’s an added Redis node, pod, or Kubernetes application… but clusters rarely stay in a fixed state. These state changes are impossible to reflect in a Helm chart unless you have charts for everything, and again it becomes a manual process.

## Redis Enterprise Operator for Kubernetes

We took everything we learned while deploying applications on Kubernetes containers and translated it into the[ Redis Enterprise Operator for Kubernetes](/blog/redis-enterprise-operator-for-kubernetes/).

The operator is a tool for businesses that need to manage a Redis instance in Kubernetes at scale. It controls the provisioning, scaling, and availability of the Redis cluster and manages the containers’ lifecycle in any infrastructure.

The Redis Enterprise Operator understands the lifecycle of an application and creates new resources to sustain the application. For instance – ever set up a gift card to automatically reload funds once they’ve been depleted? The operator automatically provisions a cluster with the resources it needs to keep running, be it an added Redis node or load balancing a [Redis cache](/solutions/caching/) to maintain sub-millisecond latency.

With Helm charts, teams can get an application up and running quickly and depend on the operator to ensure that each stage of the application’s lifecycle has the resources it needs to keep going.

In short, the Redis Enterprise Operator for Kubernetes keeps the proverbial balls in the air by ensuring a cluster always has what it needs for optimal performance.

## FAQs

Namespaces are used in Kubernetes to separate and disperse clusters into sub-clusters logically. It’s a way of isolating and identifying resources with unique names. A namespace is especially helpful for teams with robust operations across many departments. It’s a useful way for various users to tap into specific cluster resources without engaging others, thus, lowering any system complexity.

Yes. A REC can have multiple databases running at high capacity without any performance degradation.

Yes. Every REC is managed by one namespace, and each namespace needs its own operator.

A REC on Kubernetes can be deployed via cloud, on-prem, for a [microservices](/solutions/microservices/) architecture, or any combination for a true [hybrid cloud](/redis-enterprise-cloud/multicloud/) experience.

[Find more answers to your Redis Enterprise on Kubernetes questions in these FAQs.](https://docs.redis.com/latest/kubernetes/faqs/)
