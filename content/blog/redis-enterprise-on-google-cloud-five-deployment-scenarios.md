---
title: "Running Redis Enterprise on Google Cloud Explained: Five Deployment Scenarios"
linkTitle: "Running Redis Enterprise on Google Cloud Explained: Five Deployment Scenarios"
url: "/blog/redis-enterprise-on-google-cloud-five-deployment-scenarios/"
description: "Deploying Redis Enterprise, the world’s fastest database, on the performant and secure Google Cloud will give our users the best of both worlds. This post will describe five different Redis..."
date: 2022-02-08
blogCategories:
- "Company"
- "Redis Modules"
- "Uncategorized"
authors:
- "Gilbert Lau"
lastmod: 2025-03-27
hidden: true
---

*By Gilbert Lau, Cloud Partner Solution Architect · Published 8 February 2022 · updated 27 March 2025*

![Blog tile image](/images/site-mirror/9e755fcc13280b99668203867278dc015a4389b7-772x550.webp)

Deploying Redis Enterprise, the world’s fastest database, on the performant and secure Google Cloud will give our users the best of both worlds. This post will describe five different Redis Enterprise deployment scenarios on Google Cloud. We will go through these deployment scenarios, characteristics, limitations, and caveats for each.

## Redis Enterprise on Google Cloud provides the best-in-class real-time platform

[Redis Enterprise integrates with Google Cloud (GCP)](/cloud-partners/google/) to provide a best-in-class customer experience in two major deployment form factors, a fully managed service, and a self-managed software. Apart from these consumption models, Redis serves as a key-value store, enabling many popular use cases such as caching, [session management](/solutions/session-management/) and confidently serves as a primary database for real-time applications. It empowers many different verticals such as retail, [financial services](/industries/financial-services/), online gaming, social media, and many more to run their mission-critical applications on Google Cloud. Redis modules such as RediSearch, RedisJSON, RedisGraph, and RedisTimeSeries provide developers with the necessary toolsets for building highly interactive applications at a lightning speed with extreme performance. Redis Enterprise will shorten the time to market for your next applications or services with linear scalability and five-nines (99.999% SLA) availability.

## Redis Enterprise as a managed database service on Google Cloud

As the term suggests, fully-managed allows customers to consume the Redis Enterprise database as a service. Redis as the provider of this service is responsible for managing the underlying infrastructure and the lifecycle of your Redis databases. It is a pay-as-you-go consumption model in which customers are billed at an hourly rate based on five predefined shard types. Shard types are based on capacity and performance characteristics, which are memory limit and throughput. This allows Redis to meet customers where they are at in terms of their use case, and stay cost-competitive . Choosing which shard types to support your Redis database deployment is opaque to the customers. Redis will determine the optimal underlying infrastructure resources to meet the SLAs set forth by the customers while minimizing the cost of running Redis on Google Cloud.

## Two ways to deploy Redis Enterprise on Google Cloud as a managed service

Customers have the options to subscribe to our fully managed service through [Google Cloud Marketplace](https://console.cloud.google.com/marketplace/product/redis-marketplace-isaas/redis-enterprise-cloud-flexible-plan/) or directly on [Redis Enterprise Cloud](/redis-enterprise-cloud/overview/). There are benefits to subscribe through the Marketplace, such as existing Google Cloud commit drawdown and unified billing within Google Cloud. Customers with existing Google Cloud contracts usually take this route to simplify procurement and consolidate consumption billing.

The second way to consume our fully managed service is through Redis Enterprise Cloud. Here, customers will log into the Redis console directly without going through Google Cloud console. This option cannot burn down existing Google Cloud commits and does not support unified billing. However, customers can choose to deploy Redis Enterprise in three different plans: Fixed plan, Flexible plan, and Annual plan. For the Fixed plan, customers will pay a fixed monthly price according to their memory limit. Whereas the Flexible plan Redis will optimize the plan price according to the customer workloads. Behind the scenes, Redis will build an optimal, cost-effective infrastructure and Redis database configuration. Our customers will have the flexibility to change their plan options at any given time and their configuration. Price will change accordingly. Finally, the Annual plan offers our customers a discount towards the Flexible plan prices, by committing to a predefined annual consumption upfront. The annual commit applies to all the customer workloads across multiple clouds and regions. The data endpoints will be retained and the service to your application will not be disrupted. You can compare the plans’ features [here](/redis-enterprise-cloud/pricing/).

## Fully managed Redis Enterprise service offerings on Google Cloud

The table below summarizes the high-level differences between Google Cloud Marketplace and Redis Enterprise Cloud offerings in fully managed Redis Enterprise deployments:

|  | Google Cloud Marketplace | Redis Enterprise Cloud (Direct) |
|---|---|---|
| Deployment VPC |  |  |
| Connection Method | VPC Peering | Public db endpoints: Fixed PlansVPC Peering: Flexible & Annual Plans |
| Redis Modules | All (except Gears/AI) | All (except Gears/AI) |
| Redis On Flash | Available | Available |
| Active-Active Geo-Distribution | Available | Available |
| Supported Regions | Growing list of Google Cloud regions Redis supports | Growing list of Google Cloud regions Redis supports |
| Payment Terms | Monthly | Monthly: Fixed & Flexible PlansAnnual: Annual Plans |
| Billed By |  |  |
| Supported By |  |  |
| Characteristics | Google Cloud commits drawdown, unified billing | Zero interruption between plan migration |

## Self-managed Redis Enterprise deployment options on Google Cloud

If fully managed is not an option for the customers’ requirements, they can deploy Redis Enterprise as self-managed software. Customers are responsible for the underlying infrastructure on Google Cloud and the lifecycle of Redis Enterprise clusters hosting their databases. This requires customers to have full knowledge of Redis Enterprise from deployment, configuration, management, operations, and maintenance perspectives.

## Running as software on Google Cloud VM

Let’s talk about the first option of the self-managed offering. This option will require procurement of the software license for Redis Enterprise. Customers will spin up their own Google Compute Engine virtual machines hosting their Redis Enterprise clusters. They are responsible for the day-to-day operations of the clusters as well as scale-in and scale-out of the clusters to achieve optimal cluster configurations from the cost and performance standpoints. They will have full control of Redis and how their Redis Enterprise clusters are deployed and secured. They are in the full cockpit to configure, manage, and operate their clusters the way they like. They will subscribe to our world-class support to keep them up and running in optimal condition.

## Deploy Redis Enterprise on GKE cluster via GCP Marketplace

The second option for self-managed Redis is to deploy Redis Enterprise on a Google Kubernetes Engine (GKE) cluster via the Google Cloud Marketplace. Customers will be billed at an hourly rate per database shard. Similarly, they are responsible for the lifecycle of the Redis Enterprise clusters. Thus, knowing how to operate and manage the clusters on a daily basis. Since this option uses Redis Enterprise Operator to deploy a Redis Enterprise cluster and databases, any future operations of this cluster become easier with the automation already built into the operator itself, rather than running Redis Enterprise in GCE virtual machines. Assuming the underlying Kubernetes cluster has ample resources, scaling out a Redis Enterprise cluster can be done through a declarative update of the Redis Enterprise cluster’s Kubernetes resource definition. In addition, upgrading the Redis Enterprise version can also be accomplished through a declarative update of the Redis Enterprise cluster’s Kubernetes resource definition without introducing any downtime by leveraging the rolling update functionality from Kubernetes.

## Deploy Redis Enterprise via Redis Enterprise Operator for Kubernetes on …

Last, and the third option for self-managed Redis, is that customers can choose to deploy [Redis Enterprise](/enterprise/) on an existing Google Kubernetes Engine (GKE) cluster. Customers will assume the responsibility of managing the lifecycle of the Redis Enterprise clusters. The customer experience for day two operations is the same as the second option above through Google Cloud Marketplace. However, the customers will not be charged at an hourly rate by shard. Instead, customers need to procure our annual software subscription license. The table below explains the major differences between the deployments of Redis Enterprise on GCE VMs, Google Cloud Marketplace for Kubernetes, and customer’s provided GKE clusters.

## Summary of self-managed Redis Enterprise options on Google Cloud

|  | Google Compute Engine | Google Cloud Marketplace | Google Kubernetes Engine (GKE) Cluster |
|---|---|---|---|
| Deployment Infrastructure | Customer’s own VPCGCE VMs | Customer’s own VPCAnthos / GKE clusters | Customer’s provided GKE clusters |
| Enterprise Modules | All | All | All |
| Redis on Flash | Available | Coming Soon! | Coming Soon! |
| Active-Active Geo-Distribution | Available | Available | Available |
| Supported Regions | All Google Cloud regions | All Google Cloud regions | All Google Cloud regions |
| Payment Terms | Annual software subscription license | Monthly @ hourly rate per shard | Annual software subscription license |
| Billed By |  |  |  |
| Supported By |  |  |  |

## Summary of all available deployment options

Choosing which deployment option is totally dependent on your project needs. If you do not want to manage Redis Enterprise clusters, fully managed is an obvious choice with many great benefits. In addition, if you already have a committed contract with Google Cloud, subscribing to a fully managed service through Google Cloud Marketplace will definitely bring you very attractive cost benefits. If your company’s security or other compliance policies would not allow your data to reside in Redis’ managed VPC, self-managed is a clear choice as it will always run Redis Enterprise clusters in your own private VPC. Further, if your company has a mandate to standardize everything on Kubernetes, then deploying Redis Enterprise through Google Cloud Marketplace is a great option as it uses Redis Enterprise Operator to deploy and manage the lifecycle of your Redis Enterprise cluster and databases in a native Kubernetes way. Finally, it is not uncommon to switch from self-managed to fully managed and vice versa. Redis provides the flexibility for how our [customers](/customers/) want to manage their Redis Enterprise clusters as well as various consumption models best suited to their financial needs.

## Our partnership continues to grow

The collaboration between Redis and Google Cloud is never-ending. The two companies continue to strive to provide the best real-time data platform on Google Cloud. We are rolling out new features on Google Cloud on a regular basis. To learn more about our partnership, please visit our [partnership page](/cloud-partners/google/).
