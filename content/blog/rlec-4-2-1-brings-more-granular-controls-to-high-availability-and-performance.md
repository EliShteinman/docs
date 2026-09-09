---
title: "RLEC 4.2.1 Brings More Granular Controls to High Availability and Performance"
linkTitle: "RLEC 4.2.1 Brings More Granular Controls to High Availability and Performance"
url: "/blog/rlec-4-2-1-brings-more-granular-controls-to-high-availability-and-performance/"
description: "Redis Enterprise Cluster (RLEC) has been very successful since its initial release. It serves many customers’ production Redis deployments, enabling them to use the fastest database in the world..."
date: 2015-11-02
blogCategories:
- "Company"
authors:
- "Itai Raz"
lastmod: 2025-03-27
hidden: true
---

*By Itai Raz · Published 2 November 2015 · updated 27 March 2025*

![Blog tile image](/images/blog/b403ed85e80743acbb2eca3e98595362f84d9735-140x92.webp)

![RLEC 4.2.1 Brings More Granular Controls to High Availability and Performance](/images/blog/01393dc2f87a2ca6a9879a0aa3294f65421da441-635x200.webp)

Redis Enterprise Cluster (RLEC) has been very successful since its initial release. It serves [many customers’ production Redis deployments](/press-releases/customers-reap-benefits-of-highly-available-and-scalable-redis-deployments-powered-by-redis-labs-enterprise-cluster-rlec), enabling them to use the fastest database in the world with minimal operational overhead.

Recently we released our 4.2.1 version of RLEC, which includes some very useful enhancements and features that customers have been asking for, such as:

- Cross region / cloud replication
- Multi-IP and IPv6 support
- Improved AOF
- Cloud and local-network profiles support
- rsyslog logging support
- OpenStack Object Store (“Swift”) storage location support

and many more…

Below is an overview of some key updates, and you can read the full details in the [release notes](/redis-enterprise-documentation/release-notes).

## Cross region / cloud replication

RLEC includes a very useful feature called “Replica of” so you can define a database to be a replica (destination) of another database (source). Once defined and loaded with your initial data set, all write commands are synchronized from the source to the destination. This lets you maintain a database (destination) that is an exact replica another database.

This configuration can be very useful, for example, if you would like to distribute the read load of your application across multiple databases. In addition, it can be used for a one-time synchronization of a database either within RLEC or from an OSS Redis.

Your source and destination databases can even have different deployment architectures. For example, the source database can be a clustered (sharded) database, while the destination database can be a simple one-shard database.

Now, the “Replica of” feature has been enhanced to allow ***cross region / cloud replication over WAN*** by allowing traffic compression. So now you can deploy two RLEC clusters in different regions or clouds, and enable replication between databases in these clusters. When defining the replication, you can decide whether you would like to use data compression, and control the compression level.

In addition, the feature has also been enhanced to allow defining multiple source databases for a single destination database.

Here is an architecture example that shows how multiple replicas in the same cluster can help scale read load, and a replica in another cluster on another cloud platform can handle remote reads or serve for disaster recovery purposes.

![Cross region / cloud Replica of](/images/blog/6287fdf61da18180d1ce2617b1c23c35e2e9762d-615x264.webp)

## Multi-IP and IPv6 support

We’ve also added support for multiple IPs per node. You can now define multiple IPs per node, and determine which are used for internal cluster traffic, and which are used for traffic from the client to communicate with database endpoints. By doing so, you can physically separate internal cluster management traffic from client-database traffic, allowing you to achieve better performance from your databases.

Another nice feature that can greatly improve security is our support for IPv6 address types. The multiple IP addresses from above can be either traditional IPv4 type addresses, or newer and more secure IPv6 type addresses.

Here is an architecture example that shows how multiple clients can connect to the same node using different IPs, or connect to a different node using IPv6. This is a great way to logically separate different client connections to a database, or to distribute the traffic.

![Multi-IP and IPv6 support](/images/blog/57dab724369c8c9036e81bcb8070ed81b6164054-637x477.webp)

## Improved AOF

AOF (Append Only File) is a very useful persistence mechanism for Redis. When you use it, every write command to Redis is accumulated in the persistence file, so you can “replay” all these commands if you ever need to restore the data from persistence. As you can imagine, this file can get big over time, which is why there is an AOF rewrite mechanism, which can be triggered every once in awhile to reduce the AOF file size.

It is a great mechanism, but at times can be less than optimal and cause overhead on the storage system — delaying Redis execution and slowing down your database.

In this release, we have made various improvements to the AOF rewrite mechanism, and also introduced the concept of AOF SLAs in which you can define AOF file size and load-time thresholds to control when AOF rewrites are triggered.

In addition, we added AOF-related alerts that help identify disk space and degraded disk I/O performance issues.

## Cloud and local-network profiles support

We have many customers running RLEC in their own data center over their own network, but we also have many who run RLEC on public cloud platforms, where network stability is far less reliable. In a public cloud environment you would rather wait a bit before declaring a node as down because it might just be unresponsive due to a temporary network glitch that could be resolved after a few seconds. On the other hand, in a stable on-premises or private-cloud environment you’d likely prefer to immediately declare a node as down and trigger auto-failover as soon as the event happens.

To allow customers to optimize their deployments no matter what environment they are running on, we have introduced the concept of environment profiles. You can now choose which profile you are running on, and RLEC will adapt itself to provide optimized performance and high-availability assurance in accordance with your specific environment.

As indicated above there are many other interesting and noteworthy features and improvements in this release so please make sure to download the new release from our [downloads page](/redis-enterprise-downloads), and review the [release notes](/redis-enterprise-documentation/release-notes).

We are now working hard on more great features for the next release — stay tuned.

If you have any questions or feedback don’t hesitate to reach out to me at: [itai.raz@redis.com](mailto:itai.raz@redis.com).
