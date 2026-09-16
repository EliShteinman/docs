---
title: "RedisInsight—The Redis GUI You’ve Been Looking For"
linkTitle: "RedisInsight—The Redis GUI You’ve Been Looking For"
url: "/blog/redisinsight-gui/"
description: "When it comes to databases, there are two kinds of people in the world. Those who love to type commands and those who like to interact with their data visually."
date: 2019-11-12
blogCategories:
- "Product Releases"
authors:
- "Pieter Cailliau"
lastmod: 2025-03-27
hidden: true
mirrored: true
---

*By Pieter Cailliau, Product Manager · Published 12 November 2019 · updated 27 March 2025*

![Blog tile image](/images/site-mirror/ff1cc0a50e77fff71b6aee1606e6c2b24bf91bb2-974x677.webp)

When it comes to databases, there are two kinds of people in the world. Those who love to type commands and those who like to interact with their data visually.

OK, maybe the world doesn’t always need to be divided into two categories. Sometimes you want the best of both worlds. And now Redis gives you exactly that—you can continue to use Redis’ familiar command-line interface (CLI) and also choose to work with your data visually.

At [RedisConf 2019](/redisconf/) earlier this year, we [announced that we were acquiring RDBTools](/blog/rdbtools/)—a popular graphical user interface (GUI) tool for manipulating and visualizing Redis data—from [HashedIn](https://hashedin.com/). We are happy to announce that after months of tinkering and adding features into the product, the brand new version of the tool—now called [RedisInsight](/insight/)—is available to download for Microsoft Windows, Apple macOS, and Ubuntu Linux for free.

Wait, did you say “*FREE*?”

Yes, I did! RedisInsight is 100% complimentary! We want every Redis user to be able to take advantage of RedisInsight. We hope it will make Redis easier to use, with better visibility of your data. Eventually, you’ll be able to use RedisInsight as a single place for both GUI- and CLI-based interactions with your Redis database.

![](/images/site-mirror/74b7b8df7e0adca2cea0c4d0cddddaeea5a435d7-1362x619.webp)

*RedisInsight lets you plot several time series in a single graph with dual axes, zoom in with click-and-drag, and optionally optimize the amount of data retrieved for visualization purposes.*

RedisInsight is designed to educate and “give insights” to Redis users in several ways:

- By making it easier to write commands for all data structures (including all Redis modules).
- By recommending more optimal data structures and ways to use them. These recommendations are created specifically for their use case and based on years of experiences of optimizing Redis.
- By having a single consolidated tool that present an overview of everything happening inside the database, whether it’s in development or production.

So what exactly can you do with this powerful new tool? Turns out, quite a few things:

- **Explore and interact with your data:** Within RedisInsight, you can view different data structures visually or dive in to your friendly commands with a familiar REPL (read-eval-print-loop) that includes enhanced type-ahead command help. In addition, RedisInsight now has enhanced support for data from Redis modules and complex data structures like Streams and Graph.
- **Analyze and reduce memory usage:** Within RedisInsight you can do a full memory analysis both online and offline. What’s really useful is that you can upload an RDB file from another Redis instance and analyze the memory usage of the dataset within RedisInsight.
- **Bulk management:** Ever wished there was an easy way to do bulk operations like renaming, expiring, deleting, etc. a large number of keys in one go—even on key patterns? Well the Bulk Actions menu in RedisInsight lets you do just that.
- **Basic cluster management:** With RedisInsight you can directly manipulate key configurations including managing cluster and properties that affect your Redis cluster, like cluster node timeout, cluster IP, port etc..
- **View the slow log:** RedisInsight gives you visibility into your slow logs so you can identify, troubleshoot, and fix bottlenecks and find optimization opportunities.

![](/images/site-mirror/8be8037d7732cde811470822016468974a4ca64b-1362x619.webp)

*The RedisInsight Profiler lets you create real workloads and test which commands have the most impact on the database.*

If you ever thought it would be nice to have a GUI for Redis or to visually view the data inside your Redis instance, you now have the choice to download RedisInsight and make it part of your development and operational toolkit.

Learn more and give it a try at [/insight/](/insight/).

**Note:** For the visualization component of RedisIngraph in RedisInsight, we partnered with [Linkurious](https://linkurious.com/). RedisInsight leverages Linkurious’ powerful graph-visualization library Ogma, which enables you to interactively explore data within RedisGraph.
