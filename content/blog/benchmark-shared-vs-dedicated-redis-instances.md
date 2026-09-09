---
title: "Benchmark: Shared vs. Dedicated Redis Instances"
linkTitle: "Benchmark: Shared vs. Dedicated Redis Instances"
url: "/blog/benchmark-shared-vs-dedicated-redis-instances/"
description: "Eli"
date: 2013-06-27
blogCategories:
- "Tech"
authors:
- "Redis  "
lastmod: 2026-08-13
hidden: true
---

*By Redis   · Published 27 June 2013 · updated 13 August 2026*

![Blog tile image](/images/site-mirror/4d83e305e3cb3bc38913c86da00917cf0e02d85b-772x550.webp)

[Eli](http://stackoverflow.com/questions/16221563/whats-the-point-of-multiple-redis-databases)

[kenn](http://stackoverflow.com/questions/5148390/redis-databases-on-a-dev-machine-with-multiple-projects)

[Chris Laskey](https://chrislaskey.com/)

[matteo on the Redis group](https://groups.google.com/forum/#!topic/redis-db/hjJRhlXN214)

**The Theory**

**The Proof**

[here](https://github.com/GarantiaData/memtier_benchmark)

**memtier_benchmark -s <host> -p <port> -P redis -t 4 -n 10000 –ratio 1:1 -c 25 -x 10 -d 100 –key-pattern S:S**

[ZINTERSTORE](https://redis.io/commands/zinterstore)

**The Inevitable Conclusion**

---
