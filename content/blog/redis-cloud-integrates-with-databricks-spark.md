---
title: "Redis Cloud Integrates With Databricks Spark"
linkTitle: "Redis Cloud Integrates With Databricks Spark"
url: "/blog/redis-cloud-integrates-with-databricks-spark/"
description: "Announcements are usually made about past events, while they are happening or about future ones. Today’s announcement of the integration between Databricks’ Spark service and Redis’ Redis Cloud is..."
date: 2016-06-06
blogCategories:
- "Tech"
authors:
- "Itamar Haber"
lastmod: 2025-03-27
hidden: true
---

*By Itamar Haber, Technology Evangelist · Published 6 June 2016 · updated 27 March 2025*

![Blog tile image](/images/site-mirror/d141493dfd444b3b306929f7415cf47bc906f420-220x220.webp)

Announcements are usually made about past events, while they are happening or about future ones. Today’s announcement of the integration between Databricks’ Spark service and Redis’ Redis Cloud is sort of a mix of all three types. It should be obvious why it falls into the third category, so I’d like explain what had transpired and is still happening that had led to this. Since you’re reading this blog, I assume that you already have the relevant background in data processing, so I’ll skip the product introductions and jump right into the middle of the matter at hand.

The relationship between Spark and Redis may not be immediately apparent, although both have put performance at scale as their key values. The purpose of each seemingly lies at opposite ends of a spectrum – the former is focused on processing data whereas the latter on serving it. But the fact that both are data-centric technologies is that which drew the two together despite, or perhaps because of, this polarity. While each excels in its domain, it is combining them that seemed to yield the greatest rewards – as each solution evolved and matured independently, so did the body of evidence from users of the potential synergies based on real use cases. Which led to the inception of the [spark-redis connector](https://spark-packages.org/package/RedisLabs/spark-redis).

The connector’s purpose is providing a way for moving data between Spark’s and Redis’ native data structures. Its [initial release](/blog/connecting-spark-and-redis) was aimed at providing that connectivity, while conserving a primary design principle shared by both Spark and Redis: the ability to use simple building blocks for composing something much more powerful. Once that bridge which allows transforming data between Spark’s RDDs and any Redis data structure was ready, we were able to use it for showing the [effectiveness of that combination](http://www.infoworld.com/article/3045083/analytics/give-spark-a-45x-speed-boost-with-redis.html).

We’ve just released the new version of the connector, v0.3, that brings full [support for Spark SQL](https://github.com/RedisLabs/spark-redis/releases/tag/0.3.0) but even without this new feature, the connector has been steadily gaining traction and is being put to good use (assuming that GitHub’s stars are a solid indicator :)).

Nothing, however, had quite prepared us for the amazing demo that Databricks’ Reynold Xin had shared during last month’s [RedisConf](http://redisconference.com/). This demo is a pure learning experience, and paraphrasing on a quote from Douglas N. Adams, a learning experience is one of those things that says, **“You know that thing you just did? I didn’t know you could do that with Spark, Redis and the spark-redis connector!”**.

The demo notebook starts by showing how a table is stored in Redis using a couple of Hash data structures. Once the data’s in place, the RDDs from Redis are used to create the respective DataFrames, which in turn are registered as tables. That’s basically less than 10 lines of code and that’s all it takes to start doing bona fide SQL queries with joins on the data in Redis. In the demo’s second part, Reynold shows how to perform textual analysis on the data with SparkML learning and ends by storing the models stored in (which can be consequently served from) Redis. That’s short, elegant and to the point – process in Spark, serve from Redis.

Which brings us back to the beginning – if you’ll scroll back to the demo notebook’s beginning, you’ll see that it begins by manually setting up the properties for connecting to Redis Cloud. We’ve published this notebook that explains how to setup a Redis Cloud database and obtain these connection properties. Eventually the integration will allow users of both products to easily use their existing accounts from both platforms. In practical terms this means that you’ll be able to spin up a Databricks Spark cluster from the console of your Redis Cloud database to immediately process the data in it, and at the same time you’ll be able to provision and use Redis databases directly from your Spark workspace. Once ready, the integration will make connecting the two services as simple as clicking a button, literally. Questions? Feedback? [Email](mailto:itamar@redis.com) or [tweet](https://twitter.com/itamarhaber) me – I’m highly available 😉
