---
title: "Getting started with Redis Functions"
linkTitle: "Getting started with Redis Functions"
url: "/tutorials/create/redis-functions/"
description: "The most impactful addition to Redis version 7.0 is Redis Functions — a new programmability option, improving on scripts by adding modularity, reusability, and better overall developer experience."
group: "For developers"
aliases:
- "/tutorials/create-redis-functions/"
date: 2026-02-25
lastmod: 2026-02-25
hidden: true
mirrored: true
---

*Published 25 February 2026*

> **TL;DR:**
>
> Redis Functions, introduced in Redis 7.0, replace ad-hoc `EVAL` Lua scripts with persistent, modular server-side code. Functions are stored in the database, replicated automatically, and loaded via `FUNCTION LOAD`. You call them with `FCALL` instead of `EVAL`, eliminating the need to ship script source on every invocation.

## What you'll learn

- What Redis Functions are and how they improve on `EVAL` scripts
- How to create a function library in Lua and load it into Redis
- How to call functions with `FCALL`
- How to use functions to maintain a consistent data schema with automatic timestamps

## Prerequisites

- **Redis 7.0 or later** — Redis Functions are not available in earlier versions. Follow the [Redis quick start](/tutorials/howtos/quick-start/#setup-redis) to get set up.
- A terminal with access to `redis-cli`.

## What are Redis Functions?

The most impactful addition to Redis version 7.0 is **Redis Functions** — a new programmability option, improving on scripts by **adding modularity, reusability, and better overall developer experience**.

Functions are, in contrast to scripts, persisted in the .rdb and .aof files as well as automatically replicated to all the replicas, which makes them a first-class citizen of Redis.

Redis has the capability of supporting multiple execution engines so in one of the future releases we'll be able to write Redis Functions in Lua, Javascript, and more languages, but at the moment (Redis v7.0) the only supported language is Lua.

## How do Redis Functions compare to EVAL scripts?

If you have used `EVAL` to run Lua scripts in Redis before, you may wonder why you should switch to Redis Functions. The table below summarizes the key differences:

| Feature         | `EVAL` scripts                                                                      | Redis Functions                                         |
| --------------- | ----------------------------------------------------------------------------------- | ------------------------------------------------------- |
| **Persistence** | Not persisted; must be resent on every call or cached via `SCRIPT LOAD` / `EVALSHA` | Persisted in RDB/AOF and replicated automatically       |
| **Modularity**  | Single monolithic script per call                                                   | Libraries can contain multiple named functions          |
| **Invocation**  | `EVAL <script> numkeys ...` or `EVALSHA <sha1> ...`                                 | `FCALL <function> numkeys ...`                          |
| **Deployment**  | Client must manage script source/SHA                                                | Load once with `FUNCTION LOAD`; available after restart |
| **Replication** | Scripts replicated as commands                                                      | Functions replicated as part of the data set            |
| **Upgrades**    | Replace by sending new script text                                                  | `FUNCTION LOAD` with `REPLACE` flag                     |

In short, Redis Functions give you **stored-procedure-like behavior** — load your code once and call it by name from any client, without managing SHA hashes or script source distribution.

## How do you create a Redis Function library?

A common pain point for developers is to maintain a consistent view of data entities through a logical schema. Redis Functions are ideally suited for solving this problem and in this tutorial, we will demonstrate just that — we'll create a library with two functions; the first one will make sure that we can automatically set `_created_at` and `_updated_at` timestamps for hash keys and the second one will simply update the `_updated_at` timestamp without changing the other elements, simulating the "touch" Unix function. Let's go!

> **NOTE**
>
> In the rest of this tutorial we'll use the `$` character to indicate that the command needs to be run on the command prompt and `redis-cli>` to indicate the same for a `redis-cli` prompt.

### Warm-up: your first function

Now that we have our Redis server running, we can create a file named `mylib.lua` and in it create a function named `hset` that would receive the keys and arguments we pass on the command line as parameters. **Functions in Redis are always a part of a library, and a single library can have multiple functions.**

For starters, let's create a simple function that returns "Hello Redis 7.0" and save it in the `mylib.lua` file.

```bash
#!lua name=mylib

local function hset(keys, args)
   return "Hello Redis 7.0"
end
```

### Adding automatic timestamps with HSET

We're now ready to start working on the requirement. First, let's implement the part that adds an `_updated_at` timestamp:

```bash
#!lua name=mylib
local function hset(keys, args)
   local hash = keys[1]  -- Get the key name
   local time = redis.call('TIME')[1]  -- Get the current time from the Redis server

   -- Add the current timestamp to the arguments that the user passed to the function, stored in `args`
   table.insert(args, '_updated_at')
   table.insert(args, time)

   -- Run HSET with the updated argument list
   return redis.call('HSET', hash, unpack(args))
end

redis.register_function('my_hset', hset)
```

## Frequently asked questions

### What Redis version do I need for Functions?

Redis Functions require **Redis 7.0 or later**. If you are running an older version, you will need to upgrade before using `FUNCTION LOAD` and `FCALL`.

### Can I use languages other than Lua?

At the time of writing, Lua is the only supported scripting engine. Redis is designed to support multiple execution engines, so additional languages may be available in future releases.

### Are Redis Functions replicated to replicas?

Yes. Unlike `EVAL` scripts, Redis Functions are persisted in RDB and AOF files and automatically replicated to all replicas, making them a first-class part of your data set.

## Next steps

- Read the [Redis Functions documentation](https://redis.io/docs/latest/develop/interact/programmability/functions-intro/) for the full command reference.
- Learn about [Redis Lua scripting](https://redis.io/docs/latest/develop/interact/programmability/eval-intro/) if you need to support older Redis versions.
