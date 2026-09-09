---
title: "5 Steps to Building a Great Redis Module"
linkTitle: "5 Steps to Building a Great Redis Module"
url: "/blog/5-steps-building-great-redis-module/"
description: "Here are five things to keep in mind when writing a Redis module. While this list is non-exhaustive, my aim is to offer a good way to get started if you don’t yet have much experience with module..."
date: 2019-07-22
blogCategories:
- "Tech"
authors:
- "Redis  "
lastmod: 2026-09-01
hidden: true
---

*By Redis   · Published 22 July 2019 · updated 1 September 2026*

![Blog tile image](/images/blog/ec36ce78523e1a760cc34f880f7775d2526fb84e-5000x3000.webp)

Here are five things to keep in mind when [writing a Redis module](/blog/writing-redis-modules/). While this list is non-exhaustive, my aim is to offer a good way to get started if you don’t yet have much experience with module building.

## 1. Find a compelling module use case

Redis already has plenty of tools that allow you to build the exact solution you need. One example could be locks. [Using SET with the NX option](https://redis.io/docs/latest/commands/set/), you can create a lock key, and by combining it with [EXPIRE](https://redis.io/commands/expire), you get a lock lease. This can be very useful when solving coordination problems. When built-in commands are not enough, you might also resort to [Lua scripts](https://redis.io/commands/eval), which add full programmability to composite operations that are then executed atomically by Redis.

Modules go a step further, giving you even more flexibility and speed, thanks to their ability to access lower-level APIs compared to Lua, but they’re more challenging to maintain and distribute. Go for a module only when Lua can’t fully solve your use case.

### Modules can add new commands

Modules can add new commands to Redis that execute arbitrary C functions (to be precise, you can also use [Rust](https://github.com/RedisLabsModules/redismodule-rs), [Zig](/blog/write-redis-module-zig/) or any C-ABI compatible language). What you do in your function is up to you. A basic, but useful, starting point could be implementing a command that is similar to an existing one but does something more. An example of this could be [SETNE](https://github.com/kristoff-it/redis-setne) (which was first mentioned by a user in [this GitHub Pull Request](https://github.com/antirez/redis/pull/4258)). SETNE behaves exactly like SET, but when the new value is equal to the current one, it does not modify the key, thus avoiding producing a spurious [keyspace notification](https://redis.io/topics/notifications). In general, to get some practice, think about small additions you could make to existing commands to help with specific use cases.

Most of those small additions would be best implemented as Lua scripts, but it’s a good way to gain some experience in case you can’t come up with compelling module ideas right from the start. A couple exercises left to the reader: SETEQ, HINCRDATEBY.

### Modules can add new data types

The most effective way a module can add functionality to Redis is by adding a new data type. Redis has a strong focus on proper design of data structures and their related algorithms and properties. While you might not know what the exact implementation of the Set data type is, you know for sure that set membership ([SISMEMBER](https://redis.io/commands/sismember)) is always going to be fast regardless of Set size (i.e., it has sub-linear asymptotic complexity), for example.

This is the basis behind our own modules:

- [RediSearch](http://redisearch.io/) is a full-text search module based on inverted indices.
- [RedisGraph](http://redisgraph.io/) is graph module based on sparse matrices.
- [RedisTimeSeries](http://redistimeseries.io/) is similar to Redis Streams but optimized for numerical series.
- [RedisBloom](http://redisbloom.io/) offers a few different probabilistic data structures.
- [RedisAI](http://redisai.io/) runs Tensorflow deep-learning graphs (and a few other types).

These are serious modules, but not every module that introduces a new data type has to be this complex. There are plenty of simpler data types that could be useful as a module. A basic example could be a different implementation of an already present data type in Redis, like using an ArrayList to implement Lists, for example.

## 2. Polish your API

Don’t forget that wrong usage of your module’s commands is going to be as important to prepare for as correct usage. Redis users like to try commands by hand to get a better understanding, and typing in wrong arguments is part of that process. Your API should be easy to use and hard to misuse, but when the inevitable happens, make sure to report meaningful error messages.

Take a look at how standard commands behave within Redis and see if you can come up with something that works on the same assumptions. This will lessen the mental overhead required to use your commands. One example is that, in Redis, most commands have sensible behavior when called on a non-existent key: [INCR](https://redis.io/commands/INCR) will assume a missing key has value 0 so it will set it to 1, [SADD](https://redis.io/commands/sadd) will assume a missing key is an empty set, and so forth.

## 3. Be a good citizen

Modules can interact with the Redis ecosystem. [Make sure to read the documentation](https://redis.io/docs/latest/develop/reference/modules/) to learn how to get the details right, especially if your module implements a new data type. Here are the two most important aspects to get right.

### Command flags

When you’re declaring a new command, [you must specify a few flags](https://redis.io/topics/modules-api-ref#coderedismodulecreatecommandcode) to tell Redis what your command is going to do when invoked. Is it going to just read data or also write it? Is it going to allocate memory or just modify existing data? Make sure to fill those options correctly. For example, in out-of-memory (OOM) situations, deny-oom is an important flag that will tell Redis to deny access to a command that allocates memory, otherwise the whole process will be killed by the OOM killer! Even the read-only flag is important. [New client-side caching functionality](http://antirez.com/news/130) will use it to decide whether to enable tracking for a given key or not.

### Command replication

When Redis is run in a master/replica setup, the master must know which commands it should send to replicas or not. Not every command should be replicated, and some might need to be replicated only under specific conditions. For instance, I mentioned above the SETNE command that would set a key value only if the new value is different from the current one (otherwise it does nothing). In this case, the command should be replicated only when it is effectively applying a change to the key. There is no reason to make each replica execute it if it would not perform any write. Redis can’t know what to do from the outside, so you must make proper use of [RedisModule_ReplicateVerbatim](https://redis.io/docs/latest/develop/reference/modules/modules-api-ref/) and related functions.

## 4. Write great documentation

It doesn’t matter how useful your module is if no one understands how to use it. Polishing your API can help immensely in that regard, but first you need to convince potential users that the module is at least worth trying out. A good module should have good documentation that explains the general goal of the module and lists detailed information for each command.

If you take a look at [redis.io](https://redis.io/), you will see that each command lists its relative BigO complexity and has a few extra notes for when a command has particularly big or small constants, or when there are notable edge cases. Try to replicate that format, especially with regards to the syntax for command examples. Notice how each example uses lowercase names for placeholders, while uppercase ones denote keywords that must be used verbatim, with optional values between square brackets. Look at the [documentation of SET](https://redis.io/docs/latest/commands/set/) to see an example of this.

## Most importantly: Strive for simplicity

Always keep in mind that the first design principle behind Redis is simplicity. This doesn’t mean your module should never explore other options and occasionally sacrifice simplicity for other benefits (modules exist precisely to let Redis users experiment), but always be mindful of what you’re giving up.

Generally speaking, when you sacrifice simplicity for ease of use you’re also implicitly constraining the ways in which your users will be able to use your module. In Redis, most utility generally doesn’t come from a given command used in isolation, but rather in how users can combine different commands together. Smaller, clearer, simpler commands will always be easier to combine and thus yield greater results in the grand scheme of things. For this reason, I recommend increasing ease of use by properly applying the techniques described above before resorting to this kind of trade-off.

Another potential trade-off could be in favor of efficiency. This may be worth exploring and is one that Redis occasionally makes itself. A few built-in data types have two internal representations — one optimized for when the data type only has a few elements in it, while the second one is for when the key grows over a certain threshold. Two representations (plus the mechanism to switch between the two) are certainly more complex than just one, but the benefits might be worth it. This is especially true since the added complexity doesn’t show up in the user interface, as users will interact with the data type in the same way regardless of which internal representation is in use.

## In conclusion

Take a look at [which modules already exist](https://redis.io/modules), and see if you can find inspiration. We published [an SDK for writing modules in Rust](https://github.com/RedisLabsModules/redismodule-rs) and also [wrote about doing it in Zig](/blog/write-redis-module-zig/), so don’t worry if you don’t *(want to)* know C. We also have talks on YouTube ([Rust](https://www.youtube.com/watch?v=c1E8jxWVfoI), [Zig](https://www.youtube.com/watch?v=eCHM8-_poZY)), if you prefer listening over reading.

If you do end up writing a module, please make sure to send a pull request to [antirez/redis-doc](https://github.com/antirez/redis-doc) to have it added on [redis.io](https://redis.io/) and, if you feel like it, [shoot me a tweet @croloris](https://twitter.com/croloris). I’ll be happy to try out your module.
