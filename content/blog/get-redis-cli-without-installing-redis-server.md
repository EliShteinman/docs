---
title: "How to Install Redis CLI Without Installing Redis Server (Even on Windows)"
linkTitle: "How to Install Redis CLI Without Installing Redis Server (Even on Windows)"
url: "/blog/get-redis-cli-without-installing-redis-server/"
description: "Redis CLI is invaluable for writing software for getting to know a new module. If you didn’t have a Redis command line interface, understanding Redis’ data structures and testing connections would..."
date: 2022-07-02
blogCategories:
- "How To and Tutorials"
authors:
- "Redis  "
lastmod: 2026-09-01
hidden: true
---

*By Redis   · Published 2 July 2022 · updated 1 September 2026*

![Blog tile image](/images/site-mirror/e52cffc4ae0ae4a941d16aec9562a67df2a9536b-772x550.webp)

[Redis CLI](/learn/operate/redis-at-scale/talking-to-redis/command-line-tool/) is invaluable for writing software for getting to know a new module. If you didn’t have a Redis command line interface, understanding [Redis’ data structures](/redis-enterprise/data-structures/) and testing connections would be far more complicated.

Redis CLI has two modes; the first is the interactive mode – REPL (Read Eval Print Loop) – where [Redis commands](https://redis.io/docs/latest/commands/) deliver replies from the Redis server. The other option is to set command mode. With this mode, redis-cli needs additional arguments to get a reply on the standard output. However, getting this jewel of a tool is not straightforward for many. The source code for the Redis command line interface is included in the Redis GitHub repository and is automatically compiled when you build Redis from source. But what happens if you can’t (or don’t want to) create a Redis configuration from source? It means you also don’t have a Redis command line interface and building an entire database, even a Redis database, from source just to get access to the[ command line interface](/insight/) utility is overkill and sometimes not even an option.

In this post, we’ll share how to get Redis CLI without having to install Redis or make a full Redis server, but first, let’s look at a couple of scenarios.

## Problem: Can’t build Redis from source

For those of us on Linux or macOS, building Redis from source involves having the relevant compilers and tools on your system, which produces both the command line interface (CLI) and the Redis server. For most developers on these platforms, that’s not a huge burden. For those interested in best practices for deploying and operating NoSQL, read our industry report on “[Best Practices for Deploying and Operating Your NoSQL Initiative](/docs/avoid-these-10-nosql-deployment-mistakes/).”

However, if you’re not on a UNIX-like system, things get complicated quickly. For various reasons, you can’t just compile Redis on Windows. Microsoft once supported a fork of Redis that ran directly on Windows-based machines, but it’s no longer maintained. That means that, on Windows, you can’t get a current version of Redis CLI.While it’s possible to use the [Windows Subsystem for Linux](https://medium.com/@RedisLabs/windows-subsystem-for-linux-wsl-10e3ca4d434e) that can run Redis, this has its own challenges, such as file system limitations and just generally not feeling native or appropriate for the system. In addition, there are many developers who have development machines locked down in a fun and creative ways to explicitly block this type of operation.

For example, you might be in a situation where you’re on a low-spec server and you just need to do some quick checks in Redis – getting the dependencies and building the software may not be possible in these constrained environments.

## Problem: Don’t want to build Redis from source

There are many situations where you may be building software that uses Redis, but you’ll never personally manage or administer a localhost process of Redis. Imagine if you’re using Redis Enterprise Cloud – you can have a Redis instance in seconds, but if you want to do anything with it you need to have CLI, which requires building the whole package from source code. Or perhaps you’re at a large organization that is running a self-managed[ Redis Enterprise Software](/enterprise/) cluster. Here too, you may not have an actual need to build the Redis server on your development machine, since you just want to connect remotely.

Finally, you might want to get up and running quickly. Pulling down the entire Redis C project (and all the tools needed to build that) might not be efficient for your workflow.

If you fall in one of the above scenarios, read on.

## Invoking Atwood’s Law

In 2007, Jeff Atwood wrote, rather disparagingly, “any application that can be written in JavaScript will eventually be written in JavaScript.”

Bringing this to Redis,[ Lu Jiajing](https://github.com/lujiajing1126) started a small project (less than 250 lines of JavaScript!) in 2015 to reimplement the overall operation of [Redis CLI in Node.js](https://github.com/lujiajing1126/redis-cli). Since then, it’s gotten closer to mimicking the[ Antirez-provided Redis CLI](https://redis.io/docs/manual/cli/). While not perfect (yet), it provides the bulk of the functionalities that you’d need on a day-to-day basis.

You may ask, why bother with this if you still have to install Node.js first? Well, first off, Node.js provides a much wider range of installation options than Redis. You can[ get it](https://nodejs.org/en/download/) as a GUI MSI for Windows or a pkg for macOS, as well as plain old compressed binaries for Windows, macOS, or Linux. You can also install Node.js via a[ package manager](https://nodejs.org/en/download/package-manager/) on many platforms.

## Installing and running Node.js Redis CLI

Once you’ve installed Node.js and[ npm](https://www.npmjs.com/), it’s a simple one-liner to get and install the Node.js version of redis-cli:

npm install -g redis-cli

Then you can run it with the command:

rdcli -h your.redis.host -a yourredispassword -p 11111

(using your relevant connection information).

Alternately, if you don’t like global installs, you can clone the repository and install the dependencies:

git clone[ https://github.com/lujiajing1126/redis-cli](https://github.com/lujiajing1126/redis-cli)

cd redis-cli

npm install

Then you can run it from this directory by invoking the index.js file directly with the command line arguments:

node index.js -h your.redis.host -a yourredispassword -p 11111

(using your relevant connection information).

## How to install Redis CLI without building Redis

There you have it. You can get redis-cli up and running on your development machine quickly and easily with Node.js redis-cli written by[ Lu Jiajing](https://github.com/lujiajing1126). Instead of building the whole Redis project with C, you can just grab Node.js (even better if you already have it installed, and you probably do, let’s be honest), install this small module, and start hacking away in Redis.

## Redis CLI auxiliary tasks and functions

We established that Redis CLI has two main modes, the interactive mode, and the command mode. Here are a few of the supplemental operations Redis CLI performs:

- Checks Redis server [latency](/active-active/)
- Support for running a [Lua script](/blog/bullet-proofing-lua-scripts-in-redispy/)
- Reviews scheduler [latency of local computer](https://redis.io/docs/latest/operate/oss_and_stack/management/optimization/latency/)
- Receive stats on key hits with [LRU workload simulations](https://redis.io/docs/manual/cli/#performing-an-lru-simulation)
- Use [quoted string and escaped string values](https://redis.io/docs/manual/cli/#string-quoting-and-escaping) to automatically delimit arguments with whitespace characters

## Bonus

One cool little use of this module is to make it a part of devDependencies in your package.json on a Node.js project. This way, you can effectively “pack in” redis-cli with your project, making sure everyone on your team has the tool. To do this, install it as a development dependency:

npm install -save-dev redis-cli

Then in your package.json, add the following line to the beginning of the scripts object:

"rediscli": "node ./node_modules/redis-cli/index.js",

Now, anyone who has your project can start Redis CLI by running:

npm start rediscli -h your.redis.host -a yourredispassword -p 11111

(using your relevant connection information).

You can even hard code in arguments if need be, but never include your Redis password in your package.json file!
