---
title: "Redis Cloud Private"
linkTitle: "Redis Cloud Private"
url: "/blog/redis-cloud-private/"
description: "We are very excited to announce the preview release of the new simplified Redise Cloud Private (RCP) managed DBaaS."
date: 2017-06-03
blogCategories:
- "Company"
- "Tech"
authors:
- "Aviad Abutbul"
lastmod: 2025-03-04
hidden: true
mirrored: true
---

*By Aviad Abutbul, Senior Director of Product Management · Published 3 June 2017 · updated 4 March 2025*

![Blog tile image](/images/site-mirror/1e6bc3d31b3e728935a521bbd6ce81d50c157b0d-798x797.webp)

We are very excited to announce the **preview release** of the new simplified **Redise Cloud Private** (RCP) managed DBaaS.

**Redise Cloud Private** delivers a fully managed, cost effective, stable high performance Redis databases in **dedicated** clusters within **your cloud account, using your own instances, inside your VPC**, with the option to run Redis databases on RAM or RAM+Flash ([Redise Flash](/products/redis-cloud-private/flash-memory/)) as an extension of memory, using High IOPS NVMe-based SSD instances.

While Redise Cloud Private (RCP) is a long standing option for customers running production clusters, there were manual aspects to the setup. Today we released the capability to **automatically deploy** dedicated RCP clusters into your cloud account **in just a few clicks**.
To provision RCP, users provide dataset size and throughput requirements with the credentials for RCP to operate in your own VPC. RCP automatically plans and provisions your cluster and databases in an instant. Users can scale RCP throughput and dataset size up and down at any time with a simple click as well. After your cluster is deployed, our team of Redis experts, monitor and manage your RCP cluster just like any fully managed service for you.

![](/images/site-mirror/0e8c31a375e14d6a3479a2c875062d0c72fd6a02-1239x427.webp)

*Redis Cloud Private – Subscription Creation*

## Redise Cloud Private Benefits

With **Redise Cloud Private** you get reduced operational complexity, with the effortless scaling, and high resilience of Redise, delivered securely inside your private cloud environment.

**Redise Cloud Private** allows you to easily implement our [Redise Flash](/products/redis-cloud-private/flash-memory/) technology that will allows you to **slash operational expenses** when hosting large datasets in Redis by utilizing Flash memory(SSDs) in combination with RAM. In addition since RCP is running within your cloud account you can benefit from the special rates you have with your cloud provider.

With RCP you can forget about instances, clusters, scaling, data persistence/high availability settings and failure recovery. **Redise Cloud Private** comes with zero operational hassle!

Efficiently replicate Redis databases between **Redise Cloud Private** and [**Redise Pack**](/products/redis-pack/) or across cloud regions, with built-in compression and WAN optimization technologies. Create multi-region, multi-cloud or hybrid (on-premises and cloud) Redise deployments that accelerate your applications and require zero time to DR.

You can read more about about RCP benefits [here](/products/redis-cloud-private/).

## Get Started With Redise Cloud Private

The steps for creating a simple Redis Cloud Private (RCP) deployment are as follows:

1. Sign up for an RCP account
1. Create a dedicated AWS account for RCP
1. Create a new RCP subscription
1. Create a new database definition
1. Set up Amazon Virtual Private Cloud (VPC) Peering
1. Connect to your database

You can read more about it at following [link.](/redis-cloud-private-documentation/quick-setup/)

## Pricing

When you enter your database requirements – specifically memory limit and max throughput, we plan both the infrastructure and the number of **shards** (shard is any type of provisioned Redis instance, such as a master copy, slave copy of data etc.) needed to support your need.

Redise Cloud Private is pricing is based on the number of **shards** you asked for.
Every time there will be a change needed to the number of shards you will prompted with the new number and will be asked to approve that change.

![](/images/site-mirror/d667c69a6e148e56130144595eb1f24e4970486f-1239x814.webp)

*Redis Cloud Private*

## Wrap-up

With RCP you get reduced operational complexity, with the effortless scaling, and high resilience of Redise, delivered securely inside your private cloud environment.

We are currently only supporting AWS for the zero-touch deployments, other cloud platforms will come soon. Please [contact us](/pricing/redis-cloud-private/) if you need an RCP deployments on other cloud providers.

This is still a **preview** and we would very much love to get your inputs and feedback. Feel free to reach out to us at [pm.group@redislab.com](mailto:pm.group@redislab.com).
