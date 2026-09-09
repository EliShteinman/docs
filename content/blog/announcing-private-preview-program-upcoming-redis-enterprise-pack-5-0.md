---
title: "Announcing the Private Preview Program for the Upcoming Redis Enterprise Pack 5.0"
linkTitle: "Announcing the Private Preview Program for the Upcoming Redis Enterprise Pack 5.0"
url: "/blog/announcing-private-preview-program-upcoming-redis-enterprise-pack-5-0/"
description: "This content was written prior to a change in Redis’ naming convention – Redis Enterprise is now the moniker for all our products."
date: 2017-08-31
blogCategories:
- "Company"
- "Tech"
authors:
- "Cihan B"
lastmod: 2025-03-04
hidden: true
---

*By Cihan B · Published 31 August 2017 · updated 4 March 2025*

![Blog tile image](/images/site-mirror/405db99869a0382c8a9fd187cc134a0eefb142ba-804x1050.webp)

This content was written prior to a change in Redis’ naming convention – Redis Enterprise is now the moniker for all our products.

Greetings, I am very excited to announce the preview program for our upcoming release of Redis Enterprise Pack version 5.0. As part of the program, we will give you a chance to directly provide feedback on the new capabilities and be part of the inner circle with engineering teams that deliver Redis open source bits and Redis Enterprise services and products.

5.0 is a huge release with improved high availability, better scaling performance for Redis applications, advanced security and real-time search + query with indexing at Redis speeds. Here are the highlights;

- **Geo-distributed, Active-Active Redis Applications with CRDBs (conflict-free replicated databases):** Globally distributed interactive applications are hard to develop due to read and write conflicts. The new CRDBs enable the same sub-millisecond latencies you are accustomed to getting with Redis applications with globally-distributed deployment topologies. CRDB make building complex geo-distributed apps simple by using the built in smarts of proven [CRDT](/blog/diving-into-crdts/) (conflict free replicated data-types) approach. For always-on availability, CRDTs create a simple to manage, “AP-leaning” deployment of Redis (AP refers to A -“available” and P – “partition-loss tolerant” of CAP).

![](/images/site-mirror/596c3ea19d4b8cf4dd61486448533bdce983c8a3-885x641.webp)

*Figure.1: Geo-distributed CRDBs*

- **Fast Search & Query in Redis with in-memory Indexing**: The new RediSearch module combined with the new Redis 4.0 engine, provides high performance, integrated query and full-text search over efficient in-memory indexes. The RediSearch in-memory architecture allows a fast distributed index that span the Redis Enterprise cluster. This index is also built to stay fresh and up-to-date under fast data update rates. RediSearch is great for product catalogs, auto complete engines and so on in Redis.
- **Native JSON processing in Redis**: The new ReJSON Module combined with the new Redis 4.0 engine provides native and fast JSON data handling with enhanced ability to read and update subsections of JSON documents with native Redis commands. This is greatly useful for product catalogs or user profiles with many attributes and so on in Redis.
- **Redis 4.0 Compatibility and Extending Redis with Custom Modules: **The new Redis 4.0 engine includes the ability to load your own modules into Redis. With Redise Pack 5.0, developers can load their custom modules into Redise Pack 5.0 for better performance, scaling and high availability of their custom developed modules.
- **Fast “Existence” Search with Bloom Filters: **Bloom filters provide a probabilistic index that checks for existence of an item in a list. Bloom filter indexing uses a very small sparse bit based index and is optimized for very low latency query – so tiny index and faster lookup compared to other indexes. . It is useful in cases like checking if an Ad has been shown to a user already, or you can use it in [fraud detection](/solutions/fraud-detection/) to detect blacklisted merchants for a given users payment method or permission checks to see if a UserID exists on a large list of authorized users etc and so on with a tiny index optimized for writes in Redis.
- **Integrated Account Management with LDAP**: The new capability allows integrated account stores with LDAP to authenticate system admins in Redis Enterprise Pack.

Besides the top features, Redis Enterprise Pack 5.0 also bring other improvements in core performance, scale and high availability for general Redis applications.

Trying Redis Enterprise Pack 5.0 is simple. You can get the preview product on Ubuntu, RHEL, Oracle Linux or get the docker image for MacOS or Windows.

## How to sign up for the preview program?

The program will start around Sept 11th, run for a few weeks and is expected to complete around late Oct 2017.

To sign up, please send an email to [pm.group@redis.com](mailto:pm.group@redis.com) and we will get you started with preview documentation and preview builds for you to try.
