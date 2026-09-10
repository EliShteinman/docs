---
title: "Public Preview: Active-Active Deployment With Redis Enterprise for Kubernetes"
linkTitle: "Public Preview: Active-Active Deployment With Redis Enterprise for Kubernetes"
url: "/blog/announcing-active-active-kubernetes/"
description: "We recently introduced Redis Enterprise 6.4.2-30 at its core, which has an emphasis on security features such as including extended client certificate validation and pub/sub access management."
date: 2023-03-16
blogCategories:
- "Tech"
authors:
- "Angel Camacho"
lastmod: 2025-03-27
hidden: true
mirrored: true
---

*By Angel Camacho, Contributor · Published 16 March 2023 · updated 27 March 2025*

![Blog tile image](/images/site-mirror/d350b833ef5018f73773116694e7dcc7a26dcf39-772x550.webp)

We recently introduced [Redis Enterprise 6.4.2-30](/blog/redis-enterprise-software-6-4-2/) at its core, which has an emphasis on security features such as including extended client certificate validation and pub/sub access management.

But it also has additional enhancements for our Kubernetes-based release. One that’s worth highlighting is how we manage Redis Enterprise inside Kubernetes clusters. We’re making that easier, and you can experiment with the features before they are publicly available. That is: We are proud to introduce the public preview of Active-Active database deployments with Redis Enterprise for Kubernetes.

# What is new with Active-Active deployments?

Redis Enterprise has had the capability to extend a database beyond one single region or single data center for some time. We call it [Active-Active Geo-Distribution](/active-active/), though it is also known as geo-replication.

What’s new here is that [Redis Enterprise for Kubernetes](/enterprise/redis-enterprise-on-kubernetes/) can extend a database to include Active-Active configuration in a simplified fashion, one that fits in with the Kubernetes declarative mannerisms.

*Related content: *[*Redis Enterprise Operator for Kubernetes*](/blog/redis-enterprise-operator-for-kubernetes/)

As you surely are aware, deploying a Redis Enterprise cluster requires preparation and planning. The operator uses the Kubernetes API to automate the deployment and management of Redis clusters. The task gets more complicated when you introduce [data replication](/blog/what-is-data-replication/) that reaches beyond a single data center or, in the case of [cloud](/redis-enterprise-cloud/overview/) infrastructure, beyond a single region or availability zone.

Until now.

# Here’s how we make it simpler

You currently use the Operator and the new Active-Active controller to provide a repeatable and predictable deployment model for your Redis Enterprise databases. The Operator constantly monitors your cluster’s health to provide automated high availability and scalability for your data layer.

But until today, deploying cluster replication across regions or data centers was a challenging endeavor, both because of the cluster itself and also because of the database and associated resources and manual processes.

What’s that mean, practically? Here are a few new things you can now do declaratively, in a few lines of YAML, in an Active-Active controller scenario:

- Create an Active-Active database
- Add a new cluster to an existing Active-Active database
- Remove a participating cluster from an Active-Active database
- Update participating cluster details

Here’s a quick preview of how you would express this configuration in Kubernetes. In this example, we create an Active-Active database named example-aadb-1. It has copies on two clusters, and the database has three shards on each cluster.

```
apiVersion: app.redislabs.com/v1alpha1
kind: RedisEnterpriseActiveActiveDatabase
metadata:
  name: example-aadb-1
spec:
  participatingClusters:
    - name: new-york-1
    - name: boston-1
  globalConfigurations:
    shardCount: 3

```

# Next steps

This feature is in public preview and has some configuration to turn it on for your environment. We encourage you to explore our [Redis Enterprise for Kubernetes documentation](https://docs.redis.com/latest/kubernetes/) and learn how to configure an Active-Active database. [Contact us](/meeting/) with any questions or feedback.
