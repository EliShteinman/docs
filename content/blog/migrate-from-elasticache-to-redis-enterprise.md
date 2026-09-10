---
title: "3 Ways to Migrate From ElastiCache to Redis Cloud"
linkTitle: "3 Ways to Migrate From ElastiCache to Redis Cloud"
url: "/blog/migrate-from-elasticache-to-redis-enterprise/"
description: "There are lots of choices when you migrate data from one platform to another. Fortunately, the issues are so well-understood that they are suited for a simple flow chart."
date: 2023-09-18
blogCategories:
- "Uncategorized"
authors:
- "Redis  "
lastmod: 2025-03-27
hidden: true
mirrored: true
---

*By Redis   · Published 18 September 2023 · updated 27 March 2025*

![Blog tile image](/images/site-mirror/2197c9cb9e6f3b24d4cbeea213bd8a4cf4482e5e-772x550.webp)

**There are lots of choices when you migrate data from one platform to another. Fortunately, the issues are so well-understood that they are suited for a simple flow chart.**

Data migration is an important, meaningful project, even if it isn’t one that brings practitioners a lot of glory. That is all the more reason to do it efficiently.

You have a multitude of ways to migrate data. Let’s offer some guidance.

There are three main migration paths for moving from [ElasticCache into Redis](/redis-enterprise-cloud/compare-us-with-aws-elasticache/). This flowchart helps you match your current environment to the appropriate process, with cautions to protect your data and make the migration a success.

![migration decision tree](/images/site-mirror/0f1926815b441777b0bf115717aeab170eab5891-1000x789.webp)

## Rip and replace

The primary decision point is whether you can tolerate a flush of all your Redis data. If you can, there’s no need to migrate the data at all. “Rip and Replace” is easy, but a flush results in slow performance while data is rehydrated.

![Rip and replace timeline](/images/site-mirror/069efc852fac6c0893c29be4ed0829d16170108d-1000x447.webp)

Pros

- Simple to execute
- Little to no Redis downtime

Cons

- Loss of all Redis data

## Offline data migration

If you use Redis as more than a cache–for instance, you employ Redis as a session store–you can’t stomach the lost data and poor performance of a full data flush. We don’t blame you. All data is important. That’s why we offer a durable persistence option.

The next question is whether you can tolerate downtime. How much downtime are we talking about? It could be as short as a few minutes. It depends on how long it takes to export and import your Redis data.

If a short amount of downtime seems tolerable, It might be worthwhile to do a few experiments in your test environment to get a more accurate estimate of downtime. Be careful of memory usage as it is a common issue with ElastiCache deployments.

If the estimated downtime is acceptable, we recommend offline data migration. This option is easy to accomplish but it results in downtime as data is exported from ElastiCache and imported into Redis Cloud.

![Offline data migration timeline](/images/site-mirror/7edb661ff88febd206b5b33b4dda75fa79fdbc57-1000x447.webp)

Pros

- Simple to execute
- Redis data is migrated from ElastiCache to Redis Cloud
- Supported by other Redis based solutions such as Amazon MemoryDB in addition to ElastiCache and Redis Enterprise
- Data consistency

Cons

- Downtime during migration
- Might take some time for large datasets

## Live data migration

There’s one more option. Live data migration can be executed without any downtime or lost data. However, it is more operationally complicated (a polite way of saying, “You may do a lot of cursing”), and you should think through the tradeoffs.

![Offline data migration timeline](/images/site-mirror/2b005624191ea8644820fee4f63f53de42f9d411-1000x457.webp)

This option relies on an external tool developed by our in-house Redis experts called [RIOT](/learn/riot/). Its [documentation](/learn/riot/#_elasticache_migration) details operational guidance in migrating from ElastiCache to Redis Enterprise. If you’re choosing this option, you may be grateful for the opportunity to contact one of our experts for guidance.

Pros

- Live ElastiCache data is migrated to Redis Cloud
- No downtime

Cons

- More steps and potential gotchas than other methods
- May require tuning during test stage
- May not work for all databases, such as those with large key sizes (100MB+)
- Data consistency is not guaranteed
- Potentially intensive on CPU resources
- It may require operational changes to ElastiCache
- Best effort support of RIOT

Hopefully this has helped you decide how to migrate to Redis Cloud. Now all you have to do is do it.

And now that you’re using Redis Cloud, perhaps you should experiment with the new-to-you features that you now have available? Learn about [triggers and functions](/blog/introducing-triggers-and-functions/) or how [auto-tiering](/blog/introducing-auto-tiering/) can help you manage large datasets.
