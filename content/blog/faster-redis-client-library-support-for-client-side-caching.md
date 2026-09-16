---
title: "Faster Redis: Client library support for client-side caching"
linkTitle: "Faster Redis: Client library support for client-side caching"
url: "/blog/faster-redis-client-library-support-for-client-side-caching/"
description: "Getting faster than Redis isn’t easy, but starting today, you can read your most frequently accessed data, cut down on latency, and use resources more efficiently. Today, we’re proud to announce..."
date: 2024-10-28
blogCategories:
- "Announcements"
- "Engineering"
- "Features"
- "New Product Announcements"
- "Tech"
authors:
- "Mirko Ortensi"
lastmod: 2025-10-01
hidden: true
mirrored: true
---

*By Mirko Ortensi, Sr. Product Manager, Products · Published 28 October 2024 · updated 1 October 2025*

![Blog tile image](/images/site-mirror/54b9e4e05ea5755b5729a82423ecea5862ae08a6-772x552.webp)

Getting faster than Redis [isn’t easy](/blog/benchmarking-results-for-vector-databases/), but starting today, you can read your most frequently accessed data, cut down on latency, and use resources more efficiently. Today, we’re proud to announce that client-side caching support for the official Redis client libraries is now available.

- Jedis for the Java programming language
- Redis-py, for the Python programming language

Redis Community Edition has supported client-side caching since version 6. But, until now, you needed commercial third-party client libraries to use it because Redis didn’t offer support in the official client libraries. Now, you can benefit from near caching directly with the Redis official open-source client libraries, and with a few lines of code, you can enable caching at connection establishment time.

Let’s see how client-side caching can speed up data access by first taking a step back to review what near caching is and what motivates its use.

Redis’s client-server model means performance is network-bound. Every operation requires round-trip communication, which can affect performance, especially in high-throughput systems or when network latency is an issue.

![](/images/site-mirror/e3c8fb73a3bf26af66460d87ac700a9b2b9f7231-1154x355.webp)

One effective way to cut down on network overhead—and boost app performance—is through client-side caching, also called **near cache**. This technique allows frequent read operations to be served directly from a cache on the same application server where the client is running. With client-side caching enabled, client applications are served with data cached by the backend application, reducing network traffic and latency.

![](/images/site-mirror/e4cb5297804baaae4af6d2be79049c4763178901-1177x362.webp)

Here’s how it helps:

- Local caching is ideal for read-heavy scenarios, deployments in low bandwidth environments, and managing hot shards/keys (for reads).
- It reduces network round trips to the server, which helps lower both bandwidth consumption and costs—especially in the cloud.
- Server load is minimized, cutting down on computational overhead and saving on infrastructure costs.

## How it works

Let’s walk through an example to see how client-side caching works.

![](/images/site-mirror/38af83af90b9497af7b060b2a4b611da155fe68f-1126x481.webp)

1. SET foo bar
  1. Data is stored in the server
1. GET foo
  1. The command is sent to the server
  1. The client caches the reply in the local memory
1. GET foo
  1. The client gets bar from the local memory

Whenever tracked data is changed by an arbitrary client, the server publishes an invalidation message to all the clients that currently track the data.

![](/images/site-mirror/040813701a8392d652af0ea41b155ad8062737c9-1350x579.webp)

1. SET foo qux
  1. Client A changes the data
1. Invalidation message and cache removal
  1. Client B receives an invalidation message on the same connection established by the client and used to request the data initially
  1. Client B removes the data from the cache
1. GET foo
  1. Client B requests the data again
  1. Client B caches the reply in the local memory
1. GET foo
  1. Client B gets qux from the local memory

## Testing client-side caching

To start experimenting with the feature, remember that client-side caching needs the RESP3 [protocol](https://redis.io/docs/latest/develop/reference/protocol-spec/#the-new-protocol-version-resp3) since [push notifications](https://redis.io/docs/latest/develop/reference/protocol-spec/#pushes) are required. Make sure you select the correct protocol version when you’re setting up the connection.

To streamline your development experience across all Redis products, you’ll need Redis CE 7.4, Redis Stack 7.4, or newer. You can also test the latest [Redis 8 M01](/blog/redis-8-0-m01-released-one-redis-for-every-use-case/) milestone release. Client-side caching is fully compatible with [Redis Software](https://redis.io/enterprise/), [Redis Cloud](https://redis.io/cloud/), and Azure Cache for Redis Enterprise, where the feature is currently in preview and generally available soon.

We said client-side caching would be easy to set up with just a few lines of code, and here’s the proof. The example below won’t complicate your client setup. Just enable caching when you establish the connection, as shown in this Python example, and you’re ready to go.

```python
r = redis.Redis(
protocol=3,
cache_config=CacheConfig(),
decode_responses=True
)

r.set("city", "New York")
cityNameAttempt1 = r.get("city") # Retrieved from Redis server and cached
cityNameAttempt2 = r.get("city") # Retrieved from cache

```

The first time the key “city” is retrieved, it is read from the database and cached in the memory of the invoking process. Subsequent reads will be transparently served by the local cache, with minimal latency and no additional load on the database.

If you’re working with Java, all the heavy-lifting is done by Jedis. You can create a connection and enable client-side caching as follows.

```java
HostAndPort endpoint = new HostAndPort("localhost", 6379);
DefaultJedisClientConfig config = DefaultJedisClientConfig.builder().protocol(RedisProtocol.RESP3).build();
CacheConfig cacheConfig = CacheConfig.builder().maxSize(1000).build();
UnifiedJedis client = new UnifiedJedis(endpoint, config, cacheConfig);

Map<String, String> usr = new HashMap<>();
usr.put("id", "Johnny");
usr.put("first", "John");
usr.put("last", "Doe");
client.hset("session:e788eeb2", usr);
// Retrieved from Redis server and cached
client.hgetAll("session:e788eeb2"); 
// Retrieved from cache
client.hgetAll("session:e788eeb2"); 
// Peek into the cacheCache cache = client.getCache();
System.out.println(cache.getSize());
System.out.println(cache.getCacheEntries());
System.out.println(cache.getStats());

```

## Frequently Asked Questions

### Do client libraries support connection pooling?

You can enable client-side caching for both standalone connections and connection pools. It also works with Cluster and Sentinel APIs.

### When should I enable caching?

Each time the value of a cached key is modified in the database, Redis pushes an invalidation message to all the clients that are caching the key. This tells the clients to flush the key’s locally cached value, which is invalid. This behavior implies a trade-off between local cache hits and invalidation messages: keys that show a local cache hit rate greater than the invalidation message rate are the best candidates for local tracking and caching.

For example, counters represented as strings or embedded in hashes, leaderboards, and so on—keys like these could be read on a standard connection to prevent an excess of invalidation messages.

What should I do if I do not want to cache some keys?

To control what keys are cached, instantiate a standard connection without client-side caching enabled.

### What data is cached?

Clients cache a normalized version of the commands sent to the database together with the returned result. All the read-only commands are cached, except:

- Commands for probabilistic and time series data structures
- Search and query commands
- Non-deterministic commands (e.g., HSCAN, ZRANDMEMBER, etc.).

### How do I estimate the memory consumption of the local cache?

Cached items have variable sizes, so the memory consumption of a local cache is related to the workload and size of stored data. Clients support inspection of the cache, so relevant statistics about the locally stored data can support benchmarks.

### How do I verify that caching is working for my command?

If you’d like to see what’s happening under the hood, start the profiler in Redis Insight to see what commands are sent or use the MONITOR command in a redis-cli session from the terminal.

## Using the client libraries

Read more about client-side caching [here](https://redis.io/docs/latest/develop/connect/clients/client-side-caching/) and try your favorite client library using the following GA versions below. We’ll add client-side caching to more client libraries for other languages soon.

- Jedis [v5.2.0](https://github.com/redis/jedis/releases/tag/v5.2.0). Consult the Jedis-specific [documentation](https://redis.io/docs/latest/develop/connect/clients/java/jedis/#connect-using-client-side-caching).
- redis-py [v5.1.1](https://github.com/redis/redis-py/releases/tag/v5.1.1). Consult the redis-py-specific [documentation](https://redis.io/docs/latest/develop/connect/clients/python/redis-py/#connect-using-client-side-caching).
