---
title: "LRU Cache"
linkTitle: "LRU Cache"
url: "/glossary/lru-cache/"
description: "The Least Recently Used (LRU) Cache operates on the principle that the data most recently accessed is likely to be accessed again in the near future. By evicting the least recently accessed items..."
lastmod: 2026-05-21
mirrored: true
---

*updated 21 May 2026*

## What is LRU Cache?

The Least Recently Used (LRU) Cache operates on the principle that the data most recently accessed is likely to be accessed again in the near future. By evicting the least recently accessed items first, LRU Cache ensures that the most relevant data remains available in the cache.

LRU Cache offers several advantages over other caching algorithms. It provides a good balance between performance and memory usage, making it suitable for a wide range of applications. Unlike other algorithms that might prioritize data based on frequency or other metrics, LRU focuses solely on the recency of access, making its [eviction](/blog/cache-eviction-strategies/) decisions predictable and consistent.

Many systems, from databases to web browsers, employ LRU caching due to its effectiveness. For instance, operating systems use LRU algorithms to manage memory pages, ensuring that the most recently accessed pages are readily available, while less frequently accessed pages are swapped out.

## How LRU Cache works

The LRU Cache maintains a list of data items, with the most recently accessed items at the front and the least recently accessed items at the back. When a data item is accessed or added, it’s moved to the front of the list. If the cache reaches its capacity and needs to evict an item to make space for a new one, the item at the back, being the least recently used, is removed.

**Underlying data structures**

Implementing an LRU Cache typically involves using a combination of [data structures](https://redis.io/redis-enterprise/data-structures/). A common approach is to use a doubly-linked list to maintain the order of items based on access recency, and a hash map to achieve constant-time access to any item in the cache. This combination effectively creates a data structure that supports the operations required for LRU Cache.

**Eviction process**

When the cache is full and a new item needs to be added, the eviction process is triggered. The item at the back of the list, which represents the least recently used data, is removed from both the list and the hash map. The new item is then added to the front of the list and its reference, known as the cache key, is stored in the hash map along with its corresponding cache value.

**Optimizations and variations**

While the basic LRU Cache algorithm is straightforward, there are variations and optimizations to cater to specific needs. For instance, some implementations might use a “counter” or “timestamp” approach to track recency, while others might introduce additional layers or segments for more granular control over eviction decisions. It’s also essential to handle scenarios like a cache miss, where the requested element is not found in the cache.

## Implementing LRU Cache

**Choosing the right data structures**

The efficiency of an LRU Cache implementation largely depends on the choice of underlying data structures. A combination of a doubly-linked list and a hash map is commonly used. The doubly-linked list allows for constant-time additions and removals, especially when dealing with the head or tail of the list. The hash map ensures constant-time access to any element in the cache.

**Python implementation**

In Python, one can utilize the `OrderedDict` from the `collections` module to implement an LRU Cache. The `OrderedDict` maintains the order of items based on their insertion or access, making it suitable for the LRU mechanism. By pairing this with a capacity check, one can easily evict the least recently used items when the cache is full.

**Java implementation**

In Java, the LRU Cache can be implemented using a combination of `LinkedHashMap` and overriding its `removeEldestEntry` method. This method is called after `put` and `putAll` methods and allows developers to control the removal of the oldest entry in the map.

**JavaScript implementation**

For JavaScript, one can use the built-in `Map` object, which maintains the insertion order of keys. By tracking the size of the map and using the `Map.prototype.delete` method, developers can manage the eviction of the least recently used items.

**Considerations for scalability**

While the basic implementation of LRU Cache is suitable for many applications, scalability considerations might arise in distributed systems or high-traffic scenarios. In such cases, developers might look into distributed caching solutions or explore variations of the LRU algorithm that cater to large-scale environments.

## Real-world applications of LRU Cache

**Web browsers**

Web browsers, such as Chrome and Firefox, employ LRU Cache to store frequently accessed web pages. This allows users to quickly revisit pages without the need to fetch the entire content from the server, enhancing the browsing experience and reducing latency.

**Operating systems**

Operating systems use LRU Cache for memory management, specifically in the page replacement algorithms. When a program requires more memory pages than are available in physical memory, the operating system decides which pages to evict based on the LRU principle, ensuring that the most recently accessed pages remain in memory.

**Content delivery networks (CDNs)**

CDNs, which distribute web content to servers located closer to the end-users, utilize LRU Cache to store popular content. By caching frequently accessed data, CDNs can deliver content faster to users, reducing the load on the origin server and improving website performance.

**Databases**

Databases, especially those handling large volumes of data, use LRU Cache to store frequent query results. This reduces the need to access the underlying storage system for repeated queries, leading to faster query response times and optimized database performance.

**Mobile applications**

Mobile applications, particularly those requiring offline access or rapid data retrieval, implement LRU Cache to store frequently accessed data. This ensures that users can access key features of the app without delays, even in low connectivity scenarios.

## Common pitfalls and best practices

**Over-reliance on caching**

While caching can significantly improve performance, over-relying on it can lead to outdated data being served to users. It’s essential to strike a balance between caching data and ensuring that users receive the most up-to-date information.

**Not setting a cache eviction policy**

Failing to set an eviction policy can lead to the cache becoming full and not being able to store new data. This can result in frequent cache misses, negating the benefits of caching. Implementing an eviction policy, such as LRU, ensures that the cache remains effective.

**Ignoring cache size limitations**

Setting an overly large cache size can consume excessive system resources, while setting it too small can lead to frequent evictions. It’s crucial to monitor cache performance and adjust the size based on the application’s needs.

**Not considering thread safety**

In multi-threaded environments, multiple threads might access the cache simultaneously. Without proper synchronization mechanisms, this can lead to data inconsistencies. Implementing thread-safe caching mechanisms ensures data integrity.

**Best practices**

To maximize the benefits of LRU Cache, developers should regularly monitor cache hit and miss rates, adjust cache sizes based on system resources and application needs, implement appropriate eviction policies, and ensure thread safety. Additionally, setting appropriate time-to-live (TTL) values for cached data can help in serving relevant and updated data.

## LRU Cache vs. other caching algorithms

Caching algorithms determine which items to evict from the cache when space is needed for new data. While LRU Cache evicts the least recently used items, [other algorithms](https://redis.io/glossary/cache-invalidation/) use different criteria for eviction.

**First-In-First-Out (FIFO)**

FIFO is a straightforward caching algorithm that evicts the oldest item in the cache. It operates on the principle that the first item added to the cache will be the first one to be removed. While simple, FIFO doesn’t always consider the relevance or frequency of data access.

**Least Frequently Used (LFU)**

LFU Cache evicts the least frequently accessed item. It maintains a count of how often an item is accessed and removes the item with the lowest count when eviction is needed. This approach can be effective when access patterns are consistent, but it may retain infrequently used data if it was accessed multiple times in the past.

**Random Replacement (RR)**

As the name suggests, RR Cache evicts a random item from the cache when space is needed. This algorithm is simple and doesn’t require tracking access patterns, but it can be unpredictable in its eviction choices.

**Comparative analysis**

While LRU Cache is effective in many scenarios due to its focus on recent data access, other algorithms might be more suitable depending on specific use cases. For instance, LFU can be beneficial when certain data items are accessed sporadically but are still essential to keep in the cache. On the other hand, FIFO might be suitable for scenarios where data access patterns are sequential. Choosing the right caching algorithm requires understanding the application’s data access patterns and the trade-offs of each algorithm.

## Advanced topics in LRU Cache

**2Q algorithm**

The 2Q algorithm is an enhancement of the LRU Cache algorithm. It introduces two queues: one for pages accessed only once (Am) and another for pages accessed more than once (A1). This distinction allows the algorithm to better manage cache evictions by prioritizing frequently accessed pages while also considering recent access patterns.

**Low Inter-reference Recency Set (LIRS)**

LIRS is a caching algorithm designed to outperform LRU in scenarios where the access pattern has a large loop. LIRS differentiates between recency and inter-reference recency, allowing it to make more informed eviction decisions. By doing so, LIRS can maintain high cache hit rates even in challenging access patterns.

**Segmented LRU (SLRU)**

SLRU divides the cache into two segments: a probationary segment and a protected segment. New entries enter the probationary segment, and if they are accessed again, they move to the protected segment. This approach allows SLRU to maintain the benefits of LRU while also considering frequency of access.

**Adaptive Replacement Cache (ARC)**

ARC is a self-tuning caching algorithm that dynamically adjusts the size of its LRU and LFU components based on the observed access patterns. This adaptability allows ARC to perform well in a wide range of scenarios, balancing both recency and frequency of access.

**Considerations for advanced caching**

While the basic LRU Cache algorithm is effective for many applications, advanced variations can offer improved performance in specific scenarios. However, implementing these advanced algorithms requires a deeper understanding of their mechanics and the specific challenges they address. Developers should evaluate the access patterns of their applications and choose the caching algorithm that best aligns with their needs.
