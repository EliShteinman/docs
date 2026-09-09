---
title: "Containers, Kubernetes and Redis Enterprise Kubernetes Service Explained"
linkTitle: "Containers, Kubernetes and Redis Enterprise Kubernetes Service Explained"
url: "/blog/containers-kubernetes-redis-enterprise-kubernetes-service-explained/"
description: "Containers are lightweight, stand-alone, portable, self contained software execution environments. Containers have their own CPU, memory, I/O and networking resources but they share the kernel of..."
date: 2018-02-08
blogCategories:
- "Company"
- "Tech"
authors:
- "Vick Kelkar"
lastmod: 2025-03-27
hidden: true
---

*By Vick Kelkar, Principal Product Manager · Published 8 February 2018 · updated 27 March 2025*

![Blog tile image](/images/site-mirror/1262809f4b506c7aff5e1a7ec027a40edff37b44-1200x1000.webp)

Containers are lightweight, stand-alone, portable, self contained software execution environments. Containers have their own CPU, memory, I/O and networking resources but they share the kernel of the host operating system. Containers are based on linux namespaces and cgroups. [Namespaces](http://man7.org/linux/man-pages/man7/namespaces.7.html) (developed by IBM) create resource isolation for a single process while [cgroups](https://www.kernel.org/doc/Documentation/cgroup-v1/cgroups.txt) (developed by Google) manage resources for a group of processes. Containers have low startup overhead compared to that of a virtual machine running on a hypervisor. Containers are quickly becoming the basic unit of development and software packaging because they decouple applications from operating systems.

[Kubernetes](https://kubernetes.io/) is a popular open-source container orchestration engine used to deploy containerized applications. A Kubernetes cluster offers self-healing (restarts), scaling, scheduling and rolling updates of your containerized applications. These are some of the basic primitives that make up a Kubernetes cluster:

- Master – Host that contains the API server, controller manager server and etcd
- Node – Provides the runtime environment for containers
- Pod – One or more containers deployed together on a single node
- Namespace – Provides a virtual workspace on the same physical cluster
- Service – Group of pods that provide network service on a certain port
- Deployment – Declare desired state of running pods and upgrade strategy of running pods
- StatefulSet – Pods in StatefulSets are not interchangeable and each pod has unique identifier
- PersistentVolume (PV) – Storage in the cluster whose lifecycle is independent of a pod
- PersistentVolumeClaim (PVC) – A request for storage by the user/application

Read more about the primitives mentioned above in the Kubernetes [docs.](https://kubernetes.io/docs/concepts/)

Redis Enterprise Kubernetes Service

Redis is an in-memory, schema-less database. It uses optimized data structures to deliver sophisticated functionality with great simplicity. Redis offers extensibility through Redis Modules and is optimized to deliver million of operations with sub-millisecond latency. Some of the Redis use cases include real-time analytics, [high-speed data ingest](/solutions/fast-data-ingest/), session storage, high-speed transactions and in-app social functionality. [Redis Enterprise](/redis-enterprise/advantages/) provides a high performance, low latency, in memory NoSQL solution to enterprises. It enhances Redis by offering data persistence, automatic failovers, backups and replication across datacenters. Redis Enterprise is offered as a [fully managed cloud service](/products/redis-cloud/) or as [downloadable software](/products/redis-pack/).

At Redis, we are working on developing a Redis Enterprise Kubernetes service. The service will expose the Redis pods to the Kubernetes cluster using the *LoadBalancer* Kubernetes resource. The native headless Kubernetes service will take advantage of the PV, PVC and StatefulSets primitives to create a service with persistence on a Kubernetes cluster. The service will use the Kubernetes Secrets primitive to auto bootstrap Redis pods into a Redis Enterprise cluster.

![](/images/site-mirror/deb617942b0b60da2220b15078ed6995fc3225db-666x391.webp)

We added a headless Redis Enterprise service to ensure that we have an easy way to identify service pods. The advantage of a headless service is that you can reference a particular service pod in the service using the index of the service name. StatefulSets allow you to deploy the service in a consistent and reproducible way. With our Kubernetes release, we will enhance the Redis Enterprise cluster bootstrapping experience. The release will also publish our BDB endpoint in the Kubernetes service catalog on a periodic interval. In the next blog post we will spin up the newly developed Redis Enterprise Kubernetes services on a Kubernetes cluster and we will post results of a load test of the service running on a Kubernetes cluster.
