---
title: "Redis Enterprise Operator for Kubernetes"
linkTitle: "Redis Enterprise Operator for Kubernetes"
url: "/blog/redis-enterprise-operator-for-kubernetes/"
description: "To streamline the management of a Kubernetes layer, we developed our own Kubernetes controller, the Redis Enterprise Operator for Kubernetes. Unlock the cloud-native data layer by downloading our..."
date: 2022-09-09
blogCategories:
- "Tech"
authors:
- "Redis  "
lastmod: 2025-03-27
hidden: true
---

*By Redis   · Published 9 September 2022 · updated 27 March 2025*

![Blog tile image](/images/site-mirror/e52cffc4ae0ae4a941d16aec9562a67df2a9536b-772x550.webp)

**To streamline the management of a Kubernetes layer, we developed our own Kubernetes controller, the Redis Enterprise Operator for Kubernetes. Unlock the cloud-native data layer by downloading our e-book below.**

[*Unlocking the Cloud-Native Data Layer*](/docs/unlocking-the-cloud-native-data-layer/)

As companies work to modernize their legacy systems, they are shifting architectures to take advantage of containerized applications. The initial adoption of container technology was driven by developers who needed flexible deployment options and simplified software stack management. According to [Gartner](https://www.gartner.com/document/4015168), by 2027, more than 90% of global organizations will be running containerized applications in production, a significant increase from fewer than 40% in 2021.

Infrastructure and operations leaders searching for agility and portability benefits within the infrastructure have embraced Kubernetes as the de facto standard platform for container scheduling and orchestration.

Below you can see the typical architecture of a [Redis Enterprise Cluster](/redis-enterprise/technology/redis-enterprise-cluster-architecture/) regardless of whether you deploy it as nodes or as containers. There is an inherited complexity in the administration of resources for scalability and availability of the cluster.

![illustration of nodes and clusters](/images/site-mirror/a538b348bbf6d9384b941d261543a080c9eec95e-1024x294.webp)

Deploying Redis Enterprise on Kubernetes increases automation and ease of management; the Redis nodes become Kubernetes pods, keeping all the benefits of Redis Enterprise. Its shared-nothing architecture is an ideal platform for a Kubernetes deployment taking advantage of persistent volumes for storage. These volumes enable containers to outlive their typical lifecycle and offer data persistence.

In short: You don’t need to worry about the scalability or availability of your stateful applications.

To simplify and automate the management of the Kubernetes layer, we developed our Kubernetes controller, better known as a Kubernetes Operator, which deploys a Redis Enterprise database service on a Kubernetes cluster.

The [Redis Enterprise Operator for Kubernetes](https://docs.redis.com/latest/kubernetes/architecture/operator/) delivers the knowledge we acquired over years of deploying millions of clusters into a controller that extends the functionality of the Kubernetes layer and understands the Redis Enterprise capabilities to create, configure, and manage the database and the overall cluster.

For example, the Kubernetes Operator constantly monitors the state of a cluster against its ideal state. If the cluster deviates from that state, the controller takes action to correct the problem; this is how a Kubernetes deployment can automate the scaling of the cluster or the recovery of a failed node.

![operator architecture diagram](/images/site-mirror/9657614a1dbc4be19c848be245ee0024f4a74bf7-610x437.webp)

**Why Operator?**

Let’s start by answering the question: “Why do you need an Operator?” Since 2016, CoreOS (now a part of Red Hat) has been advocating a need for a controller in Kubernetes that understands the lifecycle of an application. Although Kubernetes is good at scheduling resources and recovering containers gracefully from a failure, it does not have primitives that understand the internal lifecycle of a data service. As such, adopting the Operator paradigm for Redis Enterprise is a natural progression of our Kubernetes work. Operator not only offers the benefits of a typical controller but also allows you to describe failure recovery using domain and/or application knowledge.

**So what does the Redis Enterprise Operator actually provide?**

The Operator framework takes advantage of Custom Resource Definitions (CRDs) to manage and maintain domain-specific objects in Kubernetes. By capturing domain or application-specific lifecycle management logic inside the Operator, the Operator aims to reduce deployment and maintenance complexity. Thus, by making it easier to expose the Operators to specific namespaces and/or track instances across namespaces, the Operator will lower the operational burden for our customers. The following are our design goals for the initial release of Redis Enterprise Operator:

- Create a Redis Enterprise cluster in a user-defined namespace.
- Rejoin existing cluster nodes after a pod failure.
- Ability to evacuate databases on a pod gracefully before termination.
- Protect against invalid deployments.
- Provide a Redis Enterprise cluster state that allows for better lifecycle management (such as controlling the cluster version update process).

## Run Redis Enterprise anywhere!

You know the power of Redis Enterprise. Now imagine how much you can simplify your cluster administration by adding automated scalability and zero downtime upgrades by using the power of the Redis Enterprise Operator for Kubernetes.

On top of those benefits, add unprecedented flexibility to your deployment with seamless operations across on-premise infrastructure and public cloud, or any combination, thanks to the portability and compatibility offered by the Kubernetes layer.

Do you want to start on-prem and move to the cloud? Maybe you are already running in a private cloud. You can deploy [Redis Enterprise on OpenShift](https://docs.redis.com/latest/kubernetes/deployment/openshift/), [VMware Tanzu](https://docs.redis.com/latest/kubernetes/deployment/tanzu/), [Rancher Kubernetes Engine](https://www.rancher.com/products/rancher) (RKE), or [Community Kubernetes](https://kops.sigs.k8s.io/) (kOps).

Suppose you use a Kubernetes distribution offered by major cloud vendors because of regulations or your business strategy. In that case, you can do it with [Azure Kubernetes Service](https://azure.microsoft.com/en-us/products/kubernetes-service/) (AKS), [Google Kubernetes Engine](https://cloud.google.com/kubernetes-engine) (GKE), or [Amazon Elastic Kubernetes Service](https://aws.amazon.com/eks/) (EKS).

Adopting the [hybrid cloud or multicloud](/redis-enterprise-cloud/multicloud/) has never been easier. Start with an on-prem deployment and move to any infrastructure as your needs change. Download the e-book below to help you get started.
