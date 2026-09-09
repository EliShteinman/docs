---
title: "Video Walk-Throughs of Redis Enterprise"
linkTitle: "Video Walk-Throughs of Redis Enterprise"
url: "/blog/video-walk-throughs-redis-enterprise/"
description: "We’ve been busy working on some video walk-throughs of common situations with Redis Enterprise."
date: 2017-08-14
blogCategories:
- "Company"
- "Tech"
authors:
- "Redis  "
lastmod: 2025-03-04
hidden: true
---

*By Redis   · Published 14 August 2017 · updated 4 March 2025*

![Blog tile image](/images/site-mirror/b586a7f76832f413f760195acb5122d7bf1e1228-955x539.webp)

We’ve been busy working on some video walk-throughs of common situations with Redis Enterprise.

In the first video, we talk about how to replicate between different clusters. This feature is useful in several circumstances: recovering from a disaster, speeding up read performance, geo-located databases, and making duplicates for testing or reporting. This can be done entirely from the Redis Enterprise UI and is a short point-and-click operation. Honestly, it’s pretty neat to see replication between clusters occur so seamlessly.

[Click here to view video](https://www.youtube.com/embed/AG-XGn7BQkQ)

In the second video, we go over some setup techniques to achieve high availability. What’s interesting about high availability on Redis Enterprise is how, if properly setup, you can guard against a huge number of situations that would otherwise leave you paralyzed. This video is also a good introduction to some of the core features of Redis Enterprise (sharding and clustering) and, if you pay attention, you can see one of my favourite parts of clustering: hundreds of thousands of operations per second. If you don’t get excited about high performance then go write COBOL on a System/360 or something (actually, if you’re reading this and still writing mainframe COBOL – please reach out – I legitimately want to talk to you).

[Click here to view video](https://www.youtube.com/embed/qIZuW_8bPtQ)

After showing you the setup, we do a manual failover to see how much it affects the cluster (spoiler: not much). Failing over the shard is done in *rladmin*, the CLI tool for manipulating some of the lesser used, but still important, parts of Redis Enterprise. Finally we segue into regional replication, where we replicate between shards in the same cluster with a few short clicks.

What do you think? Do you want to see more of these videos? If so, what kind of topics would you like to see? Let us know by reaching out on twitter [@Redis](https://twitter.com/redis/)
