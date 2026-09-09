---
title: "Redis Enterprise’s Fully Managed Service in Google Cloud Platform Now Available in Delhi"
linkTitle: "Redis Enterprise’s Fully Managed Service in Google Cloud Platform Now Available in Delhi"
url: "/blog/redis-enterprise-in-google-cloud-available-in-delhi/"
description: "We are very excited to share that our fully managed Redis Enterprise service in the Google Cloud Platform is now available in the Delhi region (Asia-South2) in addition to the Mumbai (Asia-South1)..."
date: 2022-04-06
blogCategories:
- "Announcements"
- "Company"
- "News"
- "Product Releases"
authors:
- "Gilbert Lau"
- "Abhishek Srivastava"
lastmod: 2025-07-03
hidden: true
---

*By Gilbert Lau, Abhishek Srivastava · Published 6 April 2022 · updated 3 July 2025*

![Blog tile image](/images/blog/5f8cce3a025d1e8da1aea15c7b09b9d41303c667-772x550.webp)

We are very excited to share that our fully managed Redis Enterprise service in the [Google Cloud Platform](/cloud-partners/google/) is now available in the Delhi region (Asia-South2) in addition to the Mumbai (Asia-South1) region of India. Today, there are over 20 Google Cloud Platform regions where customers can deploy Redis Enterprise through GCP Marketplace to support their real-time data use cases; those include enterprise cache, session management, gaming leaderboard, fraud detection, high-speed transactions, asynchronous communication, and more. Many of our customers have been using Redis Enterprise as their primary database in retail, gaming, the [financial services industry](/industries/financial-services/), and more to improve customer experience through sub-millisecond response time.

Active-Active Geo-Distributed topology has always been one of the primary differentiators of Redis Enterprise. [Active-Active Redis databases](/active-active/) provide a few core benefits over other geo-distributed solutions. For instance:

- Local latency on read and write operations (Redis provides sub-millisecond latencies)
- Seamless conflict resolution (“conflict-free”) for simple, as well as complex, data types
- Fast failover capability in case the majority of the participating clusters are down
- Optimal RTO and RPO guarantees for disaster recovery scenarios
- The obvious choice for distributed apps deployed across multiple regions
- The natural choice for microservices architectural pattern

With both Delhi and Mumbai regions in service, this enables our customers to bring real-time applications closer to their users in the Delhi region as well as provides them with a 5-9s (99.999%) service availability from Redis Enterprise’s [Active-Active Geo Distribution](/active-active/) to power their mission-critical workloads. More importantly, this allows our customers to execute their data governance strategy to comply with their data sovereignty or regulatory requirements and align with Indian data privacy laws.

Redis Enterprise Active-Active Geo-Distribution delivers local latency for globally distributed applications, unifies the data layer across regions and clouds, and ensures business continuity even when disaster strikes. To learn more about how to develop applications using Active-Active Geo-Distribution from Redis Enterprise, [download this whitepaper](/docs/developing-apps-using-active-active-redis-enterprise/) at no cost.

## Deploying in Delhi and Mumbai

The following diagram is a reference architecture that leverages Delhi and Mumbai as deployment regions for Redis Enterprise through GCP Marketplace. Both of these Redis clusters are part of the same Active-Active replication group. Each is capable of reading or writing independently of one another.

We have separate GKE clusters in each of these regions. The applications in each region connect to their respective Redis Enterprise cluster. This architecture utilizes the Multi-Cluster Ingress controller for GKE. It’s a Google-hosted service that supports deploying shared load balancing resources across clusters and across regions.

![](/images/blog/76a9bc92104b56f91f9e5155aa432247b27af1e3-1040x306.webp)

More Google Cloud Platform regions are expected to come online on a regular basis to make their managed cloud services more accessible to their customers. Redis is the same. We will run in lockstep with the Google Cloud Platform region roadmap to make Redis Enterprise available and truly accessible to an ever-growing Google Cloud Platform customer base around the globe. Digital natives who exist primarily or entirely online are no longer coming exclusively from advanced economies. Entrepreneurs of many developing countries are leveraging Google Cloud Platform’s global footprint to jumpstart their digital businesses and serve their valuable customers at a regional or global scale in no time and without any limitation.

Together, Google Cloud and Redis not only provide their customers with a ubiquitous platform to run their business in an always-on fashion. They also allow them to significantly shorten their time-to-market delivery of new products and services, as well as accelerate their product lifecycle. Through GCP Marketplace, Google Cloud Platform and Redis Enterprise provide a consumption-based OpEx model, allowing startups or small businesses to scale up or down, based on their respective seasonal or industry-specific business cycles. This makes any business become more agile and immune to volatile economic cycles. Coupled with the speed and high availability of Redis Enterprise, customers can rely on a real-time data platform to power their business-critical applications.

Google Cloud Platform’s distributed regional footprints are strategic to our partnership, as this will enable us to expand our reach to existing and new customers, support use cases requiring a global reach, and a highly available country-wide presence. We are currently offering a coupon credit to get you started with Redis Enterprise on Google Cloud!

---
