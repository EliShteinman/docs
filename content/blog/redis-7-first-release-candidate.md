---
title: "Redis 7.0: The First Release Candidate is Here!"
linkTitle: "Redis 7.0: The First Release Candidate is Here!"
url: "/blog/redis-7-first-release-candidate/"
description: "Click here to get started with Redis Enterprise. Redis Enterprise lets you work with any real-time data, at any scale, anywhere."
date: 2022-01-31
blogCategories:
- "Company"
- "Product Releases"
authors:
- "Redis  "
lastmod: 2025-03-04
hidden: true
mirrored: true
---

*By Redis   · Published 31 January 2022 · updated 4 March 2025*

![Blog tile image](/images/site-mirror/9e755fcc13280b99668203867278dc015a4389b7-772x550.webp)

[*Click here to get started with Redis Enterprise. Redis Enterprise lets you work with any real-time data, at any scale, anywhere.*](/try-free/)

*The new version is an evolutionary step to some of Redis’ features, adds new ones, and delivers more raw power at better resource utilization.*

Today, we proudly announce the availability of Redis v7’s first release candidate (RC1). Version 7.0 is a significant milestone for the project that’s been under development for the better part of last year. This major release is an opportunity to make more radical changes in terms of functionality and internals. We expect to follow our usual [release cycle](https://redis.io/topics/releases), so two more candidates, each about three weeks apart, are planned before the general availability of Redis 7.0.

Redis 7.0 adds many new features, such as Functions, ACL v2, sharded Pub/Sub, and more. We’ll cover these in this and a series of following posts. In addition, a lot of the work put into this version focused on improving and optimizing parts of Redis that are less visible to most users. This effort spanned practically every Redis subsystem, touching persistence, replication, network, memory, and compute usage. The result is a faster, more stable, and more economical Redis than ever before.

The new Redis version doesn’t herald new data structures or push its operational aspects to new realms. Instead, it is more about taking an introspective look at the project, challenging some of the existing design assumptions, taking bolder steps towards improving the infrastructure, and internalizing the community’s needs and use cases.

Redis Functions are an example of the above. Functions belong to the broader topic of Redis Programmability, which means the ability to program Redis. To “program Redis” means to have the server execute user logic, primarily for data locality. Programmability has been a part of Redis ever since the introduction of Lua scripts in version 2.6 (please refer to [Introduction to Eval Scripts](https://redis.io/topics/eval-intro) for more details).

The adoption of Lua scripts by Redis users has been rising ever since. Scripts provide an effective and simple way to compose server-side workflows from core Redis operations and control structures. They can serve as an abstraction of the underlying data structures from the application’s native code. An application’s set of Lua scripts implements its logical operations (for example, an “add user” or “place order” script).

Because scripting is a popular Redis feature that has been around for a long while, we’ve collected a lot of feedback about it. We found that most of the requirements fall into three buckets:

1. **Independence**: Scripts are a part of the application. They reflect its innards, so they are tightly coupled to the implementation. The application needs to embed scripts’ source code and load them at runtime. This entanglement increases the complexity in every stage of the application’s lifecycle, from development, through testing, to deployment.
1. **Execution Engine**: There is only one language for writing scripts in Redis: Lua. Furthermore, due to a myriad of technical reasons, Redis has been using the same Lua 5.1 for all this time. Many would like to have a newer version. Most want a different language altogether.
1. **Robustness**: The design and implementation of Lua scripting in Redis, like any other software, make assumptions and have their limits. In some cases, this makes extending the mechanism extremely complex, if not impossible. The lack of foundation blocks us from adding potentially valuable features (such as event processing and cluster scripts, for example).

That brings us back to Redis Functions. In Redis 7.0, functions are entirely independent of the application. As a result, functions are executable software artifacts that are first-class database citizens. The Redis server manages functions just like user data, so they are persisted and replicated for availability. Loading functions to the database is no longer the application’s responsibility during runtime and becomes an administrative maintenance task that can be scheduled and managed.

Having functions reside in the server’s context frees the application from the functions’ implementation. Instead, the application relies on function signatures as its API to the embedded logic and is entirely oblivious of the Redis command and types that are in play. It allows different applications to share functions. It also enables developing, testing, and maintaining functions without a mandatory dependency on the application.

The design of Redis Functions is engine-agnostic. Although Redis 7.0 only supports functions written in Lua 5.1, the implementation of internals is nearly ready to hook with other execution engines. We plan to add support for more types of execution engines in the future.

Another paradigm shift that functions make is the use of libraries. Libraries can consist of one or more registered functions and any additional internal ones. Registered functions are the library’s entry points and the application’s contractual API. On the other hand, internal functions can be natively called inside the library for code reusability.

We expect that the introduction of functions in Redis 7.0 is a big step in the direction of taking Redis’ programmability to the next stage. If you’re already using Lua scripts in your application, migrating to using functions is optional and simple (see [Redis Functions](https://redis.io/topics/functions-intro) for more). What’s even better is that, as we go forward, functions offer a better foundation to improve and innovate with Redis programmability.
