---
title: "Introducing RedisInsight 2.0: A Whole New Redis Developer Experience"
linkTitle: "Introducing RedisInsight 2.0: A Whole New Redis Developer Experience"
url: "/blog/introducing-redisinsight-2/"
description: "RedisInsight 2.0 which provides an updated UI, browser tool, advanced CLI, custom data visualization, and built-in guides to help with using Redis data models like JSON and time series. Click here..."
date: 2021-11-23
blogCategories:
- "Uncategorized"
authors:
- "Olga Lopaci"
lastmod: 2025-03-27
hidden: true
mirrored: true
---

*By Olga Lopaci · Published 23 November 2021 · updated 27 March 2025*

![Blog tile image](/images/site-mirror/c366f211c9b1d6d9405188239aa9124b4d69cfcb-935x628.webp)

*RedisInsight 2.0 which provides an updated UI, browser tool, advanced CLI, custom data visualization, and built-in guides to help with using Redis data models like JSON and time series. *[*Click here to try RedisInsight 2.0.*](/insight/#insight-form)

The Redis [manifesto](https://github.com/redis/redis/blob/unstable/MANIFESTO) states, “We’re against complexity,” followed by, “One of the main Redis goals is to remain understandable.” Although mainly referring to the Redis underlying code, we took these beliefs to heart when we worked on the brand new version of RedisInsight.

[RedisInsight](/insight/) is the free tool that lets you do both GUI- and CLI-based interactions with your Redis database, and so much more when developing your Redis based application.

In the last year, we have seen great adoption of the tool—the number of active users has more than doubled over the year. This growth in user adoption has come with a lot of extensive feedback provided by our users via the in-app survey. So a makeover was much needed and due!

## Welcome to the new RedisInsight 2.0

Our aim has always been to improve the developer experience and provide an environment that would encourage Redis-based ideation and prototyping. RedisInsight 2.0 is a complete product rewrite based on a new tech stack. This version contains a number of must-have and most-used capabilities from previous releases, plus a number of differentiators and delighters. We focused on ease of use and functionality so the app could deliver increased developer productivity and shorter time to market when developing with Redis!

## So what’s new and improved?

### New tech stack

RedisInsight now incorporates a completely new tech stack based on the popular Electron framework. You can run the application locally along with your favorite IDE, and it remains cross-platform, supported on Linux, Windows, and MacOS.

### Feature revamp

We’ve revamped a number of existing features, starting with the most popular ones:

- *Browser tool*: Now with visual cues for quickly identifying the data types and instantly accessible key ttl and size data for lazy memory analysis.
- *CLI*: Accessible at any time within the database workspace with a convenient command helper that lets you search and read on Redis commands.

![](/images/site-mirror/fc2210b649faf10946dbfbffed6272c8546d71dd-1024x544.webp)

### Workbench

A new workspace where you can build and run commands in a multiple line format and visualize their output in a way that’s easily digestible. Workbench highlights include:

- *Streamlined look and feel:* Based on the [Monaco Editor](https://microsoft.github.io/monaco-editor/) with syntax highlighting and intelligent auto-complete for Redis commands and shortcuts familiar to the developer. The feature provides support for the following Redis modules: [RediSearch](https://oss.redis.com/redisearch/), [RedisJSON](https://oss.redis.com/redisjson/), [RedisGraph](https://oss.redis.com/redisgraph/), [RedisTimeSeries](https://oss.redis.com/redistimeseries/), [RedisGears](https://oss.redis.com/redisgears/), [RedisAI](https://oss.redis.com/redisai/) and [RedisBloom](https://oss.redis.com/redisbloom/).
- *Advanced data visualizations:* Provided via built-in plugins as well as the ability to render custom plugins developed by external developers. Visualize your data in a format that’s easy to understand and consume.
- *Built-in Guides:* Developers can conveniently discover Redis features and capabilities via built-in guides. The first guide produced covers document capabilities within Redis.

![](/images/site-mirror/71644f7e9e1bcdd03f8cb74f930e6a88b3720c7c-1024x603.webp)

### Custom visualization plugins

Redis can hold a range of different data types. Visualizing these in a format that’s convenient to you for validation and debugging is paramount. You can now easily extend the core functionality independently by building your own custom visualization plugin. Reference example and [documentation](https://github.com/RedisInsight/RedisInsight/wiki/Plugin-Documentation) is provided for you to get quickly started.

### Accessibility

We’ve introduced the much-requested Dark mode and adjusted the app color palette to adhere to the highest level of [Web Content Accessibility Guidelines](https://www.w3.org/WAI/standards-guidelines/wcag/).

### Publicly available code

RedisInsight 2.0 code is now publicly available on GitHub! The reason for this is that we want to stay open and transparent, but also create a channel to easily engage with the Redis community looking to contribute towards the best-in-class Redis GUI.

## The road ahead

This is just the **start of the journey**. We’d love your help to make RedisInsight even better, so we welcome feedback, suggestions, and contributions!

We’re already working on the next iteration of the app that will include, among other features:

- A tree view of your keyspace
- Redis monitor
- More built-in guides!
- Saveable scripts within Workbench
- RedisInsight Plugin SDK package available on npm

RedisInsight 2.0 is currently available in public preview. You can download it from [here](/insight/) and learn more from the [release notes](https://docs.redis.com/latest/ri/release-notes/).

Feel free to provide [feedback](https://github.com/RedisInsight/RedisInsight/issues/new/choose) and check out the [GitHub project](https://github.com/RedisInsight/RedisInsight)!

You also might be interested to read about the public release of RedisJSON and its performance benchmarking ([blog](/blog/redisjson-public-preview-performance-benchmarking/)). RedisInsight 2.0 provides a built-in guided tutorial of the document capabilities that come with RedisJSON.
