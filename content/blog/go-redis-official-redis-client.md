---
title: "Go-Redis Is Now an Official Redis Client"
linkTitle: "Go-Redis Is Now an Official Redis Client"
url: "/blog/go-redis-official-redis-client/"
description: "The Go-Redis client joins the family of officially supported clients under the Redis umbrella."
date: 2023-02-15
blogCategories:
- "New Product Announcements"
- "Tech"
authors:
- "Igor Malinovskyi"
lastmod: 2025-03-27
hidden: true
mirrored: true
---

*By Igor Malinovskyi, Contributor · Published 15 February 2023 · updated 27 March 2025*

![Blog tile image](/images/site-mirror/4d83e305e3cb3bc38913c86da00917cf0e02d85b-772x550.webp)

**The Go-Redis client joins the family of officially supported clients under the Redis umbrella.**

Do you program in the Go language and [want to use Redis](/try-free/)? We have good news for you! The open source [Go-Redis](https://github.com/redis/go-redis), which provides a type-safe API for Redis commands, now is easier for you to access and use.

Go-Redis is a community-driven project started by [Vladimir Mihailenco](https://github.com/vmihailenco), whose [Uptrace](https://uptrace.dev/) monitoring application creates automatic alerts for complex distributed systems. Community contributors including [Dimitrij Denissenko](https://github.com/dim) and [monkey92t](https://github.com/monkey92t) helped make the Go-Redis client a top choice for developers working with Redis.

Uptrace is an [OpenTelemetry APM](https://uptrace.dev/get/opentelemetry-apm.html) with an intuitive query builder, rich dashboards, alerting rules, and integrations for most languages and frameworks. It can process billions of spans and metrics on a single server, allowing you to monitor your applications at 10x lower cost.

Beginning with version 9, Go-Redis is hosted under the [official Redis organization on GitHub](http://github.com/redis). This change encourages even more collaboration and contributions from the community and ensures that the library stays up-to-date with the latest Redis and [Redis Stack](https://redis.io/docs/stack/) features. It also aligns the Go client with other officially supported Redis clients, such as [redis-py](https://github.com/redis/redis-py) for Python, [nredisstack](http://github.com/redis/nredisstack) for .NET, [jedis](http://github.com/redis/jedis) for Java, and [node-redis](http://github.com/redis/node-redis) for Node.js.

The end result: It’s easier for developers to find and use the appropriate Redis client for their preferred programming language.

Existing Go-Redis users should update their imports and dependencies to begin using version 9:

```go
// old, v8
import "github.com/go-redis/redis/v8"

// new, v9
import "github.com/redis/go-redis/v9"

```

If you’re new to Go-Redis, please do explore it! Version 9 adds support for the [RESP3 protocol,](https://github.com/antirez/RESP3/blob/master/spec.md) introduces a new hooks API, improves pipeline retries, and allows performance monitoring via OpenTelemetry.

Thank you again to everyone who has been a part of this project thus far. We can’t wait to see what the future holds for the Go client for Redis and the wider Redis community!
