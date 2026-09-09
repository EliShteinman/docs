---
title: "February 8th outage – post-mortem"
linkTitle: "February 8th outage – post-mortem"
url: "/blog/february-8th-outage-post-mortem/"
description: "Watch the video"
date: 2016-02-10
blogCategories:
- "Tech"
authors:
- "DevOps Team"
lastmod: 2025-03-04
hidden: true
---

*By DevOps Team · Published 10 February 2016 · updated 4 March 2025*

![Blog tile image](/images/blog/9116a25b5bda9c63ea60b7c82a264d51f0be24d2-635x200.webp)

[Watch the video](/wp-content/uploads/2016/02/RL-banner-Service-Availability-635x200-v2b2.png)

On Monday February 8th 2016, at 17:45 UTC, we experienced a major outage in one of the Google Cloud Platform clusters that we employ in providing the Redis Cloud service. By 19:30 UTC we were able to bring the service back to over 95% of affected users that have the following suffix pattern in their databases endpoints: *us-central1-1-1.gce.garantiadata.com*, and had it completely recovered by 20:38 UTC.

Redis Cloud clusters are built in a Docker container-like fashion – the infrastructure consists of bare-metal or virtual servers, on top of which we deploy our cluster tools. Once deployed, each cluster can host multiple databases, with each such database running in a fully secure and isolated manner. Our clusters are fault tolerant so they are able to withstand a single node’s failure and recover from it without interruption to the service. The day before yesterday, however, regrettably was different as a bug introduced by a software update caused multiple nodes in the same cluster to fail simultaneously. Due to the failure’s nature, we had to resort to manual recovery of the cluster.

The following is the outage’s timeline:

- At 10:30 UTC our DevOps team had begun deployment of the weekly upgrade to our service’s software.Our weekly updates are done only to non-critical cluster components and do not affect the service. Any maintenance activities that do affect the service are managed differently and are announced to our users well beforehand.
- The weekly upgrade is deployed to our clusters gradually. First, we deploy the upgrade to a single cluster and perform sanity and stability testing on it. Only then do we continue rolling out the upgrade, one cluster at a time, cloud by cloud.
- At 17:30 UTC the weekly update was first deployed on Google Cloud Platform to cluster *us-central1-1-1.gce.garantiadata.com*.
- Deploying the upgrade to GCP’s nodes had caused a manifestation of a serious issue in one of the cluster’s management processes, locking it in a resource-intensive infinite loop. After a several minutes of thrashing, the server became unresponsive.
- At 17:41 UTC the first node in the cluster had failed due to that software issue. An automated failover had been triggered immediately and was successful.
- At 17:45 UTC four additional nodes had stopped responding. Because a majority of the cluster’s nodes failed, automatic recovery wasn’t possible and our DevOps team had started manual recovery.
- Manual recovery of the cluster consists of multiple automated actions, so between 17:45 and 19:30 UTC our team took the following steps:
  1. All nodes in the cluster were shut down and terminated.
  1. All of the cluster’s endpoints were deleted from the DNS zone associated with the cluster.
  1. New cluster nodes have been provisioned and built from scratch excluding the weekly update.
  1. The storage used by the cluster’s original nodes was reconnected to its new nodes, allowing the recovery of persistence-enabled databases.
  1. All databases without data persistence have been bootstrapped, launched and were immediately available afterwards.
  1. All databases with data persistence have been bootstrapped, launched and began recovery. The time it takes a database to be recovered from storage to memory is proportional to the database’s size and operations complexity, so bigger databases were slower to come online.
- Our DevOps team had hit another issue while performing the recovery, which made the process take longer. Our DNS provider throttled the delete requests that our tools generate, and the retries for these throttled requests weren’t handled correctly. This resulted in DNS entries that had to be removed manually before the cluster was relaunched, adding to the downtime’s duration.
- At 20:38 UTC the last (and largest) of the cluster’s databases was successfully recovered from persistence and the service was back to being fully operational.

While words are of little consolation, we sincerely apologize for this outage and are acutely aware of the impact it had on many of our customers. All of us here at Redis are devoted to providing the best Redis-as-a-Service solution and we’ll spare no effort in fulfilling this mission. Due to this outage, despite it being the first of kind for us, we’ve taken immediate steps to ensure that such incidents do not recur. Specifically, here are the action that we’ll be taking in the immediate short term:

1. All automatic weekly upgrades are suspended until an appropriate procedure that prevents events such as this outage is deployed.
1. We’re revalidating our QA processes that concern DevOps code deployments.
1. We’re improving our tooling so it can handle throttling of DNS requests.
