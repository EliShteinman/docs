---
title: "Redis vs. ElastiCache: Networking, VPC, and public IP"
linkTitle: "Redis vs. ElastiCache: Networking, VPC, and public IP"
url: "/blog/redis-vs-elasticache/"
description: "When choosing how to run Redis in your environment, you’re not just comparing features. You’re deciding how Redis will operate inside your current architecture and how that choice will hold up as..."
date: 2025-12-16
blogCategories:
- "Tech"
authors:
- "James Tessier"
lastmod: 2026-06-01
hidden: true
mirrored: true
---

*By James Tessier, Senior Technical Product Marketing Manager, Competitive Intelligence · Published 16 December 2025 · updated 1 June 2026*

![Redis](/images/site-mirror/04acf41bae9b96ea218b39582290b1c2ff00ff5a-1200x628.webp)

When choosing how to run Redis in your environment, you’re not just comparing features. You’re deciding how Redis will operate inside your current architecture and how that choice will hold up as you grow across accounts, VPCs, and external services.

That’s where the networking differences between Amazon ElastiCache and Redis Cloud matter. Each takes a distinct approach to public/private connectivity, cross-VPC access, and how much ownership you retain over IAM, and data governance. Those choices shape how easily Redis fits into the environment you’re building now and the one you’ll grow into later. For many teams, the Redis Cloud vs ElastiCache networking differences end up being the deciding factor in which can be safely deployed inside their AWS footprint.

## The core models

ElastiCache and Redis Cloud take different approaches to how they fit into your environment. Seeing those models clearly makes the rest of the networking comparison much simpler.

### ElastiCache

ElastiCache supports both Redis and Valkey and offers two ways to deploy it:

- A node-based deployment that lives directly [inside your VPC](https://docs.aws.amazon.com/AmazonElastiCache/latest/dg/elasticache-vpc-accessing.html).
- A serverless deployment that connects [via a VPC endpoint](https://docs.aws.amazon.com/AmazonElastiCache/latest/dg/WhatIs.corecomponents.html) inside your VPC.

Both models stay fully private and tied to AWS networking. Any access outside that boundary requires additional AWS networking layers.

### Redis Cloud

Redis Cloud delivers managed Redis as one service with multiple connectivity options:

- Private connectivity using [VPC peering](https://redis.io/docs/latest/operate/rc/security/vpc-peering/) for direct VPC-to-VPC access.
- Private connectivity using [AWS PrivateLink](https://redis.io/docs/latest/operate/rc/security/aws-privatelink/) for cross-account, multi-VPC access.
- Private connectivity using [Transit Gateway](https://redis.io/docs/latest/operate/rc/security/aws-transit-gateway/) for more complex topologies.
- Public IP connectivity through a [TLS endpoint](https://redis.io/docs/latest/operate/rc/security/database-security/tls-ssl/).
- Running Redis Cloud [inside your own VPC](https://redis.io/docs/latest/operate/rc/subscriptions/bring-your-own-cloud/) while Redis manages the service.

All of these are options for Redis Cloud, not separate products. You configure VPC peering, AWS PrivateLink, and Transit Gateway directly from the Redis Cloud console on the subscription’s Connectivity tab. With ElastiCache, those are generic AWS networking features you wire up yourself and then point your apps at the cluster endpoints.

What differs between the two platforms is the range of connection paths you can choose from and how well those paths fit architectures that grow across accounts, VPCs, and external services. Once you see the basic shapes, the next question is what happens when your environment is not neatly contained inside a single VPC boundary.

## How private connectivity actually works

For most teams, private connectivity is the default. The question is not whether you can keep Redis private, but how much work it takes to wire that private access into the rest of your environment.

With node based ElastiCache, private access means the service lives inside a single VPC and exposes private endpoints there. With ElastiCache Serverless, the cluster is in its own VPC and private VPC endpoints are added to your VPC. With either service, anything outside of that VPC connects through AWS networking features you must configure yourself, such as VPC peering, Transit Gateway, or your own proxy layer. ElastiCache does not manage those connections for you. You build the network paths in AWS, then point your apps at node endpoints inside of that VPC.

Redis Cloud supports the same private connectivity patterns. The difference? It treats them as part of the product instead of external plumbing. You can set up private connectivity from the Redis Cloud console using VPC peering, AWS PrivateLink, or Transit Gateway on AWS, and the service presents a single stable endpoint for clients. Redis Cloud manages the routing and topology behind that endpoint, so you plug it into your existing VPC layout instead of reshaping the layout around the service.

Both approaches keep Redis private. The difference is where the networking work lives. With ElastiCache, private connectivity sits outside the service as AWS networking you own. With Redis Cloud, private connectivity is part of how the service behaves.

### Choosing between VPC peering, Transit Gateway, and PrivateLink for Redis Cloud

Redis Cloud customers usually start with VPC peering or Transit Gateway for production. Those models fit single-account or straightforward multi-VPC topologies and behave like standard VPC-to-VPC networking. PrivateLink is a better fit when you have overlapping CIDR ranges, many consumer VPCs across accounts, or security policies that prefer service endpoints over full VPC routing. In those cases, Redis Cloud exposes a PrivateLink endpoint that applications can reach from their own VPCs without reshaping existing network layouts.

## The pain of private-only designs

Once you look past the initial setup, the limits of a private-only model start to show up as your environment grows.

What private-only designs mean in practice:

- **ElastiCache**: Only private access. Any cross-VPC or external use case becomes an AWS networking project.
- **Redis Cloud**: Supports the same private paths with native connectivity controls and also offers public TLS endpoints with CIDR controls, making cross-account or partner access possible without extra AWS plumbing.

**Impact**: As your architecture grows, Redis Cloud lets you add new consumers without redesigning the network boundary.

ElastiCache offers only private access, which works fine when every service that needs Redis lives in the same VPC. Many environments don’t stay that simple for long.

When anything outside that VPC needs access, you have to start building around the boundary. That typically means implementing one or more of:

- Transit Gateway attachments
- VPC peering chains
- AWS PrivateLink services
- Custom proxy layers

Each one adds cost, review cycles, and coordination with network and security teams.

External tools and partners make this even harder. CI systems, analytics platforms, observability agents, SaaS integrations, or services in other accounts all need their own path in. With ElastiCache, every one of those paths becomes an AWS networking project.

For node based ElastiCache clusters, the private-only model also affects scale. Each node consumes an IP address in your subnets, so multi-AZ clusters, replicas, and resharding events can run subnets out of address space. When that happens, scaling stops until you redesign your network or migrate the cluster. This IP exhaustion risk doesn’t apply to ElastiCache Serverless, which runs in an AWS-managed VPC, but the same private-only and VPC boundary constraints still apply.

These issues all show up before you ever think about public access. They start with how private connectivity behaves when your architecture is no longer a clean, single VPC fit.

### Example: An advantage of a public IP address option

For most workloads, private connectivity is the steady state. Public access is a tool you reach for when you need speed. Yes, Redis Cloud supports public IP via TLS endpoints.

One large B2B marketplace uses Redis Cloud to avoid turning every new partner integration into a networking project. For new integrations, partner teams connect to Redis Cloud over TLS using public endpoints with CIDR limits. This means they can build and test their integration immediately, instead of waiting for new network paths. Once an integration is ready for production, they move that traffic to private connections over VPC peering. They change only the connection-string and do not change Redis data structures or client logic.

With ElastiCache’s private-only model, they’d need to stand up and maintain custom proxy infrastructure in front of the cluster to support the same pattern.

## How cluster behavior shows up in your network

Connectivity alone doesn’t tell the whole story. Cluster behavior shows up directly in how your apps and network handle scale and failover.

ElastiCache exposes individual nodes to your apps. Clients have to understand Valkey’s cluster layout, reconnect on failovers, and adjust to endpoint changes. Every node also consumes an IP in your subnets. As clusters grow, those IPs add up and can block scaling.

Redis Cloud avoids all of that. A proxy presents a single stable endpoint and hides the topology behind it. Failovers and resharding don’t change how clients connect. Redis Cloud manages node IPs internally, so you aren't planning IPs at the node level. In the BYOC model, Redis infrastructure still consumes IPs from your VPC, but Redis manages those resources for you.

A stable endpoint and hidden topology make it much easier to connect Redis across VPCs, accounts, and external services without turning every change into a networking task.

## When you need full control

Some teams also have requirements that aren’t just about connectivity, but about where Redis must physically live.

Most teams get the flexibility they need from Redis Cloud’s standard private and public connectivity options. But some environments have stricter requirements. They need Redis to live inside their own VPC boundary. Naturally, you may think ElastiCache is the straightforward answer. It fits cleanly into your VPC and satisfies those network constraints, but you’re still responsible for the operational overhead that comes with a node-based system. That means managing nodes, monitoring performance, scaling at the right time, and pre-provisioning capacity.

That’s where running Redis Cloud inside your VPC comes in. You keep ownership of your IAM policies, VPC layout, and data governance, and Redis continues to manage the service. The connectivity model stays the same, but the control boundary shifts to match the rest of your environment.

This option isn’t for every team, but when your environment demands deeper control over where Redis lives, it gives you that control without taking on full Redis operations.

## The hidden cost of cross-AZ traffic

There is one more difference that often shows up late: how easy it is to see what cross-AZ traffic is costing you.

Both ElastiCache and Redis Cloud incur the same AWS cross-AZ data-transfer charges. The difference is how easy it is to understand where those charges come from.

With ElastiCache, cross-AZ traffic doesn’t show up as an ElastiCache line item. It appears as generic EC2 regional data-transfer fees. Replication, failover resyncs, node replacements, and client traffic that crosses AZ boundaries all contribute, but none of it is labeled as Valkey traffic. That makes it easy to miss the connection until the charges show up in your bill.

Redis Cloud doesn’t change the underlying AWS fees, but it makes them easier to account for. Multi-AZ traffic is surfaced transparently and tied directly to your Redis deployment, so you can see how your architecture drives those costs. You may still be surprised by the volume, but not by where it came from.

The fee is the same, but the visibility isn’t. Of course, cross AZ charges are only one part of the cost picture. Total cost of ownership depends on your environment and deployment model. We cover those tradeoffs in detail in [here](/blog/redis-vs-elasticache-which-is-more-cost-effective/).

## Where the models fit

Pulling all of this together, the fit depends less on features and more on the shape of your environment. If you’re mostly inside a single AWS account and region, standard private connectivity is usually enough. As soon as you’re connecting multiple VPCs, accounts, or external services, the additional connectivity options Redis Cloud gives you become the difference between simple wiring and ongoing networking projects.

ElastiCache works best when your architecture stays inside a single VPC or tightly controlled AWS footprint. If every service that needs Valkey lives in one place and you don’t expect much external access, the private-only model is predictable and straightforward. The tradeoff is that the network boundary is fixed, and extending the service to new consumers often requires additional AWS networking work.

Redis Cloud fits cleanly in those same environments. Private-only, single-VPC architectures work just as well with Redis Cloud as they do with ElastiCache, but you also gain the flexibility to expand without redesigning your network. As soon as your architecture spans multiple VPCs, multiple accounts, third-party services, or hybrid setups, Redis Cloud’s connectivity options become an advantage rather than a constraint.

Running Redis Cloud inside your own VPC is the right fit when you need Redis to live under your governance model but still want Redis to manage the service. It supports strict compliance or traffic-control requirements without reintroducing node operations.

Both services support single VPC access patterns. If your architecture extends beyond that, or you want the flexibility to grow without reworking your network, Redis Cloud is the better fit. And if you want to [explore how this plays out in multi-cloud scenarios, we cover that in a related post](/blog/redis-vs-valkey-for-multi-cloud-flexibility/).

## Wrapping it up

Both services work well in simple, private-only environments. The gap appears as soon as your architecture is no longer a clean fit for a single VPC boundary. ElastiCache keeps you tied to that shape. Redis Cloud gives you managed Redis that fits single VPC setups and keeps working when you add more accounts, VPCs, services, and clouds.

Networking is only one part of the story. Other posts in this series look at [resource efficiency](/blog/redis-elasticache-valkey-sprawl/), [data synchronization](/blog/rdi-vs-elasticache/), and [high availability](/blog/redis-vs-elasticache-ha/), so you can closely examine all of the differences between Redis Cloud and ElastiCache. If you’re ready to talk shop, [book some time with an expert](https://redis.io/meeting/).
