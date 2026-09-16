---
title: "Redis and Golang: Designed to Improve Performance"
linkTitle: "Redis and Golang: Designed to Improve Performance"
url: "/blog/redis-go-designed-improve-performance/"
description: "Golang or Go (https://golang.org/) and Redis have a lot in common. Go is fast and simple. It’s a great tool for prototyping things, and has the added benefit of really fast execution with little..."
date: 2018-03-05
blogCategories:
- "Company"
- "New Product Announcements"
authors:
- "Miguel Allende"
lastmod: 2025-03-27
hidden: true
mirrored: true
---

*By Miguel Allende, Customer Advocacy Manager · Published 5 March 2018 · updated 27 March 2025*

![Blog tile image](/images/site-mirror/0073e867b4e64f59de9047fdcde04295ba647e5c-772x550.webp)

![](/images/site-mirror/049ff5e2ed1c9812abbab7b0cd9c2de4e220cd59-545x323.webp)

Golang or Go ([https://golang.org/](https://golang.org/)) and Redis have a lot in common. Go is fast and simple. It’s a great tool for prototyping things, and has the added benefit of really fast execution with little memory. Similarly, Redis is simple, persistent and benchmarked as the [fastest in-memory database](/docs/nosql-performance-benchmark/). Developers are always looking to improve performance, but often must increase complexity to achieve it. This is not the case with Redis and Go, and that’s why both are quickly becoming the most popular open source languages and databases respectively. Redis was named the[most loved database by developers for 2017](/docs/nosql-performance-benchmark/) and Go was named one of the[ top 5 most loved programming languages by developers](https://insights.stackoverflow.com/survey/2017#most-loved-dreaded-and-wanted). Though they perform different tasks, their value proposition is the same: improved performance without sacrificing simplicity.

Interested in getting started with Redis and Go? This blog post ([https://golangme.com/blog/how-to-use-redis-with-golang/) ](https://golangme.com/blog/how-to-use-redis-with-golang/)has you covered. It explains how to develop application cache, session store, counters, real-time analytics, publish/subscribe and job queue management. The blog post also highlights a few code examples of how to use the popular Redigo client to:

- Connect your Go application to a Redis database
- Improve performance using pipelining
- Use the Scan function to convert byte arrays into Go data types

**Popular Golang clients for Redis**

Redigo ([https://github.com/garyburd/redigo](https://github.com/garyburd/redigo)) provides a print-like API for all Redis commands. It also supports pipelining, publish/subscribe, connection pooling and scripting. Redigo is easy to get started—you can access the complete API reference here:[https://godoc.org/github.com/garyburd/redigo/redis](https://godoc.org/github.com/garyburd/redigo/redis).

Radix ([https://github.com/mediocregopher/radix.v2](https://github.com/mediocregopher/radix.v2)) provides single purpose, easy-to-get-started packages for most Redis commands including pipelining, connection pooling, publish/subscribe, clustering and scripting.

Redis and Golang make a magical combination for programmers.[Redis Cloud](https://app.redis.com/#/sign-up/cloud?direct=true) is a great way to get started with a Redis database in just minutes!
