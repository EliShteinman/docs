---
title: "Getting Started with Node and Redis"
linkTitle: "Getting Started with Node and Redis"
url: "/tutorials/develop/node/gettingstarted/"
description: "Redis is an open source, in-memory, key-value data store most commonly used as a primary database, cache, message broker, and queue. Redis cache delivers sub-millisecond response times, enabling..."
group: "For developers"
aliases:
- "/tutorials/develop-node-gettingstarted/"
date: 2026-02-25
lastmod: 2026-02-25
hidden: true
mirrored: true
---

*Published 25 February 2026*

> **TL;DR:**
>
> Install the `redis` npm package (node-redis) or `ioredis`, call `createClient()` to connect Node.js to Redis, then use `set` and `get` for basic operations. Both clients support modern async/await patterns and deliver sub-millisecond response times.

## What you'll learn

- How to install and configure node-redis or ioredis
- How to connect Node.js to a Redis server
- How to run basic Redis commands (strings, sorted sets) from JavaScript
- How node-redis and ioredis compare so you can choose the right Redis npm package
- Where to go next with Express, Redis OM, and more

## Prerequisites

- **Node.js** v18 or later (LTS recommended)
- **npm** or **yarn** package manager
- A running Redis server — follow the [Redis quick start](/tutorials/howtos/quick-start/) to set one up

## Introduction

Redis is an open source, in-memory, key-value data store most commonly used as a primary database, cache, message broker, and queue. Redis cache delivers sub-millisecond response times, enabling fast and powerful real-time applications in industries such as gaming, fintech, ad-tech, social media, healthcare, and IoT.

Redis is a great database for use with Node.js. Both Redis and Node share similar type conventions and threading models, which makes for a very predictable development experience. By pairing Node.js and Redis together you can achieve a scalable and productive development platform.

Redis has two primary Node.js clients which are [node-redis](https://github.com/redis/node-redis) and [ioredis](https://github.com/redis/ioredis). Both are available through npm. We generally suggest using node-redis, as it has wide support for Redis modules, is easily extended, and is widely used. Check out a [list of Redis clients that the community has built (search Node)](https://redis.io/docs/latest/integrate/).

## How do I install node-redis?

Run the following command to install the Redis npm package:

```bash
npm install redis
```

## How do I connect to Redis from Node.js?

Use `createClient()` from the `redis` package to open a connection. The example below connects to Redis, sets and gets a string key, adds items to a sorted set, and iterates over the results:

```javascript
import { createClient } from 'redis';

async function nodeRedisDemo() {
    try {
        const client = createClient();
        await client.connect();

        await client.set('mykey', 'Hello from node redis');
        const myKeyValue = await client.get('mykey');
        console.log(myKeyValue);

        const numAdded = await client.zAdd('vehicles', [
            {
                score: 4,
                value: 'car',
            },
            {
                score: 2,
                value: 'bike',
            },
        ]);
        console.log(`Added ${numAdded} items.`);

        for await (const { score, value } of client.zScanIterator('vehicles')) {
            console.log(`${value} -> ${score}`);
        }

        await client.quit();
    } catch (e) {
        console.error(e);
    }
}

nodeRedisDemo();
```

## How do I use ioredis with Node.js?

### Step 1. Install ioredis using npm (or yarn)

```bash
npm install ioredis
```

### Step 2. Write your application code

```javascript
const Redis = require('ioredis');

async function ioredisDemo() {
    try {
        const client = new Redis();

        await client.set('mykey', 'Hello from io-redis!');
        const myKeyValue = await client.get('mykey');
        console.log(myKeyValue);

        const numAdded = await client.zadd('vehicles', 4, 'car', 2, 'bike');
        console.log(`Added ${numAdded} items.`);

        const stream = client.zscanStream('vehicles');

        stream.on('data', (items) => {
            // items = array of value, score, value, score...
            for (let n = 0; n < items.length; n += 2) {
                console.log(`${items[n]} -> ${items[n + 1]}`);
            }
        });

        stream.on('end', async () => {
            await client.quit();
        });
    } catch (e) {
        console.error(e);
    }
}

ioredisDemo();
```

## node-redis vs ioredis: which should I use?

| Feature              | node-redis                                 | ioredis                       |
| -------------------- | ------------------------------------------ | ----------------------------- |
| Redis module support | Full support (RediSearch, RedisJSON, etc.) | Limited                       |
| API style            | Async/await with `client.connect()`        | Auto-connect on instantiation |
| Cluster support      | Yes                                        | Yes                           |
| Sentinel support     | Yes                                        | Yes                           |
| Lua scripting        | `evalSha` / `eval`                         | `defineCommand` helper        |
| TypeScript           | Built-in types                             | Built-in types                |
| Maintained by        | Redis official                             | Community                     |

**Recommendation:** Use **node-redis** if you need advanced Redis data structure support (Search, JSON, time series, probabilistic, vectors) or want the officially maintained Redis JavaScript client.

## Example projects

### Hacker News Clone in Node.js

![Hacker News Clone project illustration built with Next.js and Redis](/images/site-mirror/40002b10c5b21c29a5183c331246bd05d0660ed4-1190x1152.webp)

[A Hacker News Clone project](/tutorials/how-to-build-a-hackernews-clone-using-redis/) built in Next.js, Node.js, and Express based on Search and JSON.

---

### Shopping Cart application in Node.js

![Shopping Cart application illustration showing Node.js and Redis integration for e-commerce](/images/site-mirror/90ed2da4a2562d555bc9c421a88475aa42a068cb-1130x1006.webp)

[Shopping Cart app in Node.js](/tutorials/how-to-build-a-shopping-cart-app-using-nodejs-and-redis/) module functionalities.

## More developer resources

### Sample code

[**Basic Redis Caching**](/tutorials/howtos/caching/) — This application calls the GitHub API and caches the results into Redis.

[**Redis Rate-Limiting**](/tutorials/howtos/ratelimiting/) — This is a very simple app that demonstrates rate-limiting feature using Redis.

﻿[**Notifications with WebSocket, Vue & Redis**](https://github.com/redis-developer/redis-websockets-vue-notifications) — This project allows you to push notifications in a Vue application from a Redis PUBLISH using WebSockets.

### Technical articles & videos

[**Redis Rapid Tips: ioredis**](https://www.youtube.com/watch?v=H6rikGCYPUk) (YouTube)

﻿[**Mapping Objects between Node and Redis**](https://www.youtube.com/watch?v=dukkMLbzPfA) (YouTube)

### Redis University

Build full-fledged Redis applications with Node.js and Express.

[YouTube: https://www.youtube.com/embed/Ik1WXPX3WNU](https://www.youtube.com/embed/Ik1WXPX3WNU)

## Next steps

- [**Express + Redis OM for Node.js**](/tutorials/develop/node/redis-om/) — Build a REST API in minutes using Express and Redis OM to map objects to Redis easily.
- [**Redis Caching Quick Start**](/tutorials/howtos/caching/) — Learn how to cache API responses with Redis and Node.js.
- [**Redis Rate-Limiting**](/tutorials/howtos/ratelimiting/) — Add rate limiting to your Node.js application using Redis.
