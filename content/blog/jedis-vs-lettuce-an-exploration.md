---
title: "Jedis vs. Lettuce: An Exploration"
linkTitle: "Jedis vs. Lettuce: An Exploration"
url: "/blog/jedis-vs-lettuce-an-exploration/"
description: "I’m an explorer by heart, so when I have to make a technical decision—like, say, choosing a Redis client—I go a-spelunking. Herein is the account of my exploration of the rhyming duo of Java..."
date: 2022-09-12
blogCategories:
- "Tech"
authors:
- "Redis  "
lastmod: 2026-06-01
hidden: true
---

*By Redis   · Published 12 September 2022 · updated 1 June 2026*

![Blog tile image](/images/site-mirror/684d4dc128cdc44561956d60cc56be87d61946ee-1000x575.webp)

I’m an explorer by heart, so when I have to make a technical decision—like, say, choosing a Redis client—I go a-spelunking. Herein is the account of my exploration of the rhyming duo of Java clients: [Jedis](https://github.com/xetorthio/jedis) versus [Lettuce](https://lettuce.io/).

Let’s start with the basics, and examine each client, to understand the differences between the two.

## What is Lettuce?

Lettuce is a Redis Java client that is fully non-blocking. It supports both synchronous and asynchronous communication. Its complex abstractions allow you to scale products easily.

Consider Lettuce as a more advanced client that supports Cluster, Sentinel, Pipelining, and codecs.

## What is Jedis?

Jedis is a client library inside Redis that’s designed for performance and ease of use. Jedis is a lightweight offering compared to other Redis Java clients; it offers fewer features but can still handle large amounts of memory.

Due to its simpler functionality, Jedis is easier to use, but it only works with clusters synchronously. If you choose Jedis, you may find it less challenging to focus on the application and data rather than the data storage mechanism.

[The gnomic goal of profit, like underpants, is always there.](https://www.youtube.com/watch?v=tO5sxLapAts) But the part that you can benefit from is the selection criteria. It will allow us to decide when Jedis is the right call and when Lettuce is the way to go. This is super important because we all know the answer to *any* question when selecting tools is, “it depends.”

My comparison plan was simple:

- Try some simple things in code
- Try some advanced things in code
- Arrive at some sort of selection criteria
- …
- Profit!

## A simple kind of code

To get to the bottom of the Jedis versus Lettuce debate, let’s compare code for the simplest of all exercises: setting and getting a value from a single instance of Redis.

First, we do this with Jedis:

```python
package com.guyroyse.blogs.lettucevsjedis;

import redis.clients.jedis.Jedis;

public class JedisSetGet {

    private static final String YOUR_CONNECTION_STRING = "redis://:foobared@yourserver:6379/0";

    public static void main(String[] args) {

        Jedis jedis = new Jedis(YOUR_CONNECTION_STRING);

        jedis.set("foo", "bar");
        String result = jedis.get("foo");

        jedis.close();

        System.out.println(result); // "bar"
    }
}

```

Looking at the code, this is pretty simple. Create a connection. Use it. Close it.

Next, we do it with Lettuce:

```python
package com.guyroyse.blogs.lettucevsjedis;

import io.lettuce.core.RedisClient;
import io.lettuce.core.api.StatefulRedisConnection;
import io.lettuce.core.api.sync.RedisCommands;

public class LettuceSetGet {

    private static final String YOUR_CONNECTION_STRING = "redis://:foobared@yourserver:6379/0";

    public static void main(String[] args) {
        RedisClient redisClient = RedisClient.create(YOUR_CONNECTION_STRING);
        StatefulRedisConnection<String, String> connection = redisClient.connect();
        RedisCommands<String, String> sync = connection.sync();

        sync.set("foo", "bar");

        String result = sync.get("foo");

        connection.close();
        redisClient.shutdown();

        System.out.println(result); // "bar"
    }
}

```

This looks a bit more involved. There’s a Java client, a connection, and a command object. And their names and templated nature suggest that there might be multiple varieties of them. Maybe in addition to a StatefulRedisConnection<String, String> type, we have a stateless variety that takes a byte[]]? (Spoiler: there are multiple connection types for clustering and master/replica configurations, but not stateless ones.)

Once you’re beyond the setup and teardown, however, it’s the same basic code in either client: Create a connection. Use it. Close it.

Right now, for something as simple as this, Jedis looks easier. That makes sense since it has less code. But I am certain that the Lettuce software has all this stuff for a reason—probably to handle more advanced scenarios.

## Jedis and multi-threaded code

Jedis can handle multi-threaded applications just fine, but a Jedis connection is not thread-safe. So don’t share them. If you share a Jedis connection across threads, Redis blurts out all sorts of protocol errors, like:

expected '$' but got ' '

To solve these sorts of problems, use JedisPool—a thread-safe object that dispenses thread-unsafe Jedis objects. Using it is simple, like the rest of Jedis. Just ask for a thread and return it to the pool via .close() when you’re done. Here it is in action:

```python
package com.guyroyse.blogs.lettucevsjedis;

import redis.clients.jedis.*;

import java.util.List;
import java.util.Set;
import java.util.stream.Collectors;
import java.util.stream.IntStream;

public class JedisMultithreaded {

    private static final String YOUR_CONNECTION_STRING = "redis://:foobared@yourserver:6379/0";

    public static void main(String[] args) {
        JedisPool pool = new JedisPool(YOUR_CONNECTION_STRING);

        List<String> allResults = IntStream.rangeClosed(1, 5)
                .parallel()
                .mapToObj(n -> {
                    Jedis jedis = pool.getResource();

                    jedis.set("foo" + n, "bar" + n);
                    String result = jedis.get("foo" + n);

                    jedis.close();

                    return result;
                })
                .collect(Collectors.toList());

        pool.close();

        System.out.println(allResults); // "bar1, bar2, bar3, bar4, bar5"
    }
}

```

Each of these Jedis objects encapsulates a single connection to Redis, so (depending on how large your pool is) there may be blocking or idle connections. Furthermore, these connections are synchronous, so there’s always a degree of idleness.

## Jedis, Lettuce, and clustering

I feel like I should talk about [clustering](https://docs.redis.com/latest/rs/clusters/), but there’s not much to say—at least in terms of comparisons. There’s plenty of capability to discuss, but both libraries support clustering. Unsurprisingly, Jedis is easier to use, but it works with clusters only synchronously. The Lettuce software is more difficult to use but is capable of synchronous, asynchronous, and reactive interaction with the cluster.

This is the recurring theme. And that shouldn’t be surprising. By its own admission, “Jedis was conceived to be EASY to use.” And Lettuce states, “Lettuce is a scalable Redis client for building non-blocking Reactive applications” right on its [homepage](https://lettuce.io/).

Of course, if you’re using [Redis Enterprise](/redis-enterprise/technology/redis-enterprise-cluster-architecture/), you don’t have to worry about clustering as it’s handled server-side. Just use the non-clustered APIs of Jedis or Lettuce, manage your keys so they’re slotted to the correct shards, and you’re good to go.

##
