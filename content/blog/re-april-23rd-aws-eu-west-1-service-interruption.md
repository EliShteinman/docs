---
title: "Re: April 23rd AWS EU-WEST-1 Service Interruption"
linkTitle: "Re: April 23rd AWS EU-WEST-1 Service Interruption"
url: "/blog/re-april-23rd-aws-eu-west-1-service-interruption/"
description: "This week on Tuesday, April 23rd, Amazon cloud’s eu-west-1 data region experienced a service degradation. It was not highly publicized, although some reported on Twitter about AWS’ connectivity..."
date: 2014-04-24
blogCategories:
- "Tech"
authors:
- "Chen Waiss"
lastmod: 2025-03-04
hidden: true
---

*By Chen Waiss · Published 24 April 2014 · updated 4 March 2025*

![Blog tile image](/images/blog/0073e867b4e64f59de9047fdcde04295ba647e5c-772x550.webp)

![](/images/blog/b938a55c885030f4d78c93870c68cc0db8b66050-635x200.webp)

This week on Tuesday, April 23rd, Amazon cloud’s eu-west-1 data region experienced a service degradation. It was not highly publicized, although some reported on Twitter about AWS’ connectivity issues and node failures. Analyzing the impact of this incident on our services can provide us and our customers with valuable insights regarding the efficiency of Redis’ automatic failover mechanisms.

What occurred in AWS’ EU region was a multiple node failure event, in which several nodes within the same Redis cluster became temporarily unavailable. In some clusters the nodes were affected one by one, while in other cases all nodes malfunctioned simultaneously, causing different results:

- Customers who subscribe to our [Multi-AZ plan](/blog/first-we-take-virginia-then-we-take-dublin-announcing-the-availability-of-multi-az-in-aws-eu-west), in which clusters operate simultaneously in several availability zones, were kept completely out of harm’s way during the Amazon cloud failure.
- Customers using our [in-memory replication capability](/blog/high-availability-for-in-memory-cloud-datastores) did not experience any downtime or data loss when encountering nodes that failed consecutively. Thanks to our instant failover mechanism, all data from failing nodes was constantly replicated onto functioning ones.
- Customers who encountered nodes failing simultaneously did experience downtime due to Amazon’s connectivity issues. However, all their data was fully recovered using the solutions that we employ. Redis enables data persistence to EBS. Thanks to this, we managed to quickly restore the data from all failed nodes and deliver it to the users who had enabled data persistence. We also noticed that some of the customers who use our backup to S3 capability restored their data quickly without any intervention from our side.

Some of Amazon’s services were disrupted for several hours, with our ops monitoring the situation the entire time. We were pleasantly surprised by how few customers actually contacted us about this issue. It is encouraging to be able to observe the way that our services protect our customers from damage when failovers occur.

We at Redis offer several different mechanisms intended to protect our customers from precisely these scenarios. Organizations considering using our services should take this event into account in order to make an informed decision that suits the level of protection that they require.

[Check out this article for more information about our high availability mechanisms](/blog/high-availability-for-in-memory-cloud-datastores)
