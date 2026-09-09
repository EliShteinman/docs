---
title: "AWS VPC endpoints on Redis Cloud"
linkTitle: "AWS VPC endpoints on Redis Cloud"
url: "/blog/aws-vpc-endpoints-now-available-on-redis-cloud/"
description: "Redis is now a launch partner with Amazon Web Services (AWS) for AWS VPC endpoints for resources—a new capability that gives you private access to VPC resources using AWS PrivateLink and VPC..."
date: 2024-12-02
blogCategories:
- "Uncategorized"
authors:
- "Redis  "
lastmod: 2025-03-27
hidden: true
---

*By Redis   · Published 2 December 2024 · updated 27 March 2025*

![Blog tile image](/images/blog/32a99e2a16d4f41b5e35e8f03bd8d33786568ffb-772x552.webp)

Redis is now a launch partner with Amazon Web Services (AWS) for AWS VPC endpoints for resources—a new capability that gives you private access to VPC resources using AWS PrivateLink and VPC Lattice. Soon, Redis Cloud users can take advantage of this capability to privately and securely connect their Redis databases to AWS resources across VPCs and accounts.

This adds to our lineup of secure connectivity options for Redis Cloud on AWS—including with AWS [TransitGateway](https://redis.io/docs/latest/operate/rc/security/aws-transit-gateway/) and through [VPC peering](https://redis.io/docs/latest/operate/rc/security/vpc-peering/), so you can connect your resources with confidence.

Redis Cloud users who use AWS VPC endpoints for resources get the full power of AWS PrivateLink and VPC Lattice working together. Your traffic stays locked down—private and off the public internet.

No load balancers needed on the resource owner’s side for connectivity through VPC endpoints to Redis Cloud databases. Plus, you can share exactly what you want—like your Redis Cloud database—without exposing a single other resource in your VPC.

This is private connectivity, done smarter.

AWS VPC endpoints for resources are rolling out first to Redis Cloud Professional subscribers. You’ll find the option to activate them right next to the configuration settings for AWS Transit Gateway and VPC peering under the Connectivity tab.

And Redis Cloud users using AWS VPC endpoints for resources will still have access to the best of Redis, including the highest SLA offered in the industry with [99.999% availability when leveraging multi-region Active-Active](https://redis.io/active-active/), powered by CRDT.

Resources in the same region stay securely and privately connected through AWS PrivateLink and VPC Lattice. Devs also keep full access to the Redis ecosystem, including [Redis Insight](https://redis.io/insight/)–the official Redis GUI–and official open source client libraries for [Python](https://redis.io/docs/latest/develop/connect/clients/python/), [Java](https://redis.io/docs/latest/develop/connect/clients/java/), [Go](https://redis.io/docs/latest/develop/connect/clients/go/), [Node](https://redis.io/docs/latest/develop/connect/clients/nodejs/), and [.NET](https://redis.io/docs/latest/develop/connect/clients/dotnet/) supported directly by us.

With AWS VPC endpoints, securing your data connectivity between Redis Cloud and AWS is easier than ever. Let’s see how you put it to work.

## How to get started

New users can start a free 14-day trial on the [Redis AWS Marketplace listing](https://aws.amazon.com/marketplace/pp/prodview-mwscixe4ujhkq?sr=0-2&ref_=beagle&applicationId=AWSMPContessa) today to set up and prepare for connecting with AWS VPC endpoints for resources through AWS PrivateLink and VPC Lattice.

Existing customers can reach out to their Redis account manager to set up resource sharing and keep their connections private and reliable.
