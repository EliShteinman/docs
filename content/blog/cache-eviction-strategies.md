---
title: "Cache Eviction Strategies Every Redis Developer Should Know"
linkTitle: "Cache Eviction Strategies Every Redis Developer Should Know"
url: "/blog/cache-eviction-strategies/"
description: "Here’s a real-world scenario. You set up a Redis database, and it’s doing wonders at speeding up your application. But as the data flows in and the volume increases, you notice a potential issue:..."
date: 2023-08-30
blogCategories:
- "Uncategorized"
authors:
- "John Noonan"
lastmod: 2026-06-01
hidden: true
---

*By John Noonan, Senior Product Marketing Manager · Published 30 August 2023 · updated 1 June 2026*

![Blog tile image](/images/blog/66844dda42348f10b83752f962ab2b2b1f2f8bf5-772x550.webp)

**Here’s a real-world scenario. You set up a Redis database, and it’s doing wonders at speeding up your application. But as the data flows in and the volume increases, you notice a potential issue: the cache is filling up. What will happen when it’s full? You may have heard about cache eviction but, perhaps, you’re fuzzy on the details.**

You’re not alone. Whether you’re a developer in a budding company or a system administrator in a large corporation, it’s important to understand cache eviction and know when and how to implement it. In this guide, we explore why.

## Understanding cache eviction

Cache eviction policies are a critical aspect of cache management when you use Redis (or any system that relies on caching… but we speak here from our own expertise). It addresses the challenges of cache size and memory usage. As the cache reaches its limits, it must make a crucial decision: should new data be rejected, or should space be created by discarding old data?

This is where cache eviction comes into play. However you resolve it, cache eviction involves determining which cache entries to retain and which to discard when a cache fills up. It’s necessary to achieve or maintain optimal application performance and consistency.

Eviction, in the context of caching, does not involve any landlords or overdue rents. Rather, it refers to the process of removing specific data from a cache. Because when a cache reaches its maximum storage capacity, some data must be removed to make space for new data–just like a bookshelf where you cannot force another book into the space available.

## Cache eviction strategies

Cache eviction strategies are protocols that dictate how a system responds when the cache is full. The decision about which data to evict (that is, remove) is made programmatically based on one of several strategies. Common strategies include:

- **Least Recently Used** (LRU): Picture this: you’re cleaning out your closet. What do you toss first? That funky shirt you haven’t worn since the ’80s, right? Or the ten-year-old dress that’s two sizes too small, the one you’ve been promising yourself you’ll fit into again someday? Similarly, LRU cache eviction policy evicts the least recently accessed cache entries first, based on the assumption that items not recently accessed are less likely to be needed soon.
- **Least Frequently Used** (LFU): Now, imagine you’re a librarian. Which books would you remove to make space on the library shelves? Probably the ones that are borrowed the least often. That’s what LFU does. A LFU cache eviction policy evicts the cache entries that are least frequently accessed first, assuming that items accessed infrequently are less likely to be needed in the near future.
- **Window TinyLFU** (W-TinyLFU): This one’s a bit more complex. Imagine you’re a radio station DJ. You want to play songs that are both popular (frequently requested) and current (recent hits). W-TinyLFU keeps the most relevant cache entries in the cache by considering both how recent and how frequently the data has been accessed. This cache eviction policy is especially beneficial in scenarios with varying access patterns and distributed caching environments.
- **Time To Live** (TTL): Consider a carton of fresh berries. Even if you enjoy them daily, there comes a point when they’ve been in the fridge too long and the berries start to mold. It’s time to toss them out, no matter how much you liked them. TTL is a similar concept in caching. Each cache entry is stamped with a specific “expiration date.” Once that time limit is reached, the entry is evicted, no matter how frequently or recently it was accessed. This method ensures that data doesn’t overstay its welcome, especially when it has the potential to become outdated or irrelevant. It’s a go-to strategy in scenarios where data updates regularly, and there’s a need to ensure the cache doesn’t serve stale information.

The effectiveness of these strategies depends on the specific use case.

## The risk of default settings

While Redis does have a default eviction policy (volatile-LRU), relying solely on it without understanding its implications can be risky. Applications serve diverse user needs, which means that data patterns and eviction requirements can vary significantly. Setting the right eviction policy can prevent potential headaches.

## Monitoring: the first line of defense

Before even thinking of eviction, it’s essential to know when to act. This is where monitoring tools come into play.

Redis provides tools like the INFO command for monitoring cache performance, while third-party monitoring tools like New Relic and Datadog offer more detailed analysis.

Tuning cache performance involves adjusting cache settings and eviction policies based on the information you discover from monitoring performance. In distributed caching scenarios, monitoring and tuning become even more critical to ensure consistent and efficient cache management across multiple nodes. (We have additional advice for what to look for in a third-party monitoring tool.)

## Choosing the right eviction policy in Redis

In Redis, the cache entry data structure is managed by the maxmemory configuration directive, which sets the memory limit. The maxmemory-policy configuration directive guides Redis in making its eviction decisions based on the chosen cache eviction policy. Both the maxmemory-policy and the eviction policy are among the configuration settings stored in the redis.conf configuration file.

There are quite a few Redis eviction policies, but you probably care most about these.

### allkeys-lru

Removes the least recently used cache entries, whether or not they have an expiration time set.

- Redis keeps track of when each key was last accessed. Every time a key is read or written, Redis updates this information.
- When the memory limit is reached and Redis needs to evict keys, it looks for the keys that haven’t been accessed for the longest time. These are the “least recently used” keys.
- Redis evicts these keys to make room for the new data.
- The allkeys-lru policy applies to all keys in the Redis database, regardless of whether they have an expiration time set. This is in contrast to the volatile-lru policy, which only applies to keys with an expiration time set.

### volatile-lru

Removes the least recently used cache entries with an expiration time set. This is suitable for scenarios where data needs to be refreshed periodically.

### allkeys-lfu

When Redis needs to make room for new data, this policy removes the least frequently used keys.

- Redis tracks how often each key is accessed. Every time a key is read or written, Redis increments a counter associated with that key.
- When the memory limit is reached, Redis looks for the keys with the lowest counter values, considered the “least frequently used” keys.
- Redis evicts these keys to make room for the new data.

### volatile-lfu

Similar to allkeys-lfu, this policy applies only to keys with an expiration time set.

### volatile-ttl

This policy removes keys with the shortest TTL first.

- Redis keeps track of the TTL for each key. The TTL is a duration after which the key is automatically deleted.
- When the memory limit is reached, it looks for the keys with the shortest TTL. These are the keys that are set to expire soonest.
- Redis evicts these keys to make room for the new data.

### noeviction

Instead of evicting any keys, this policy returns an error when the memory limit is reached and a write command is received. (Don’t throw out anything in the closet. Send an alarm!)

- When the memory limit is reached and Redis receives a write command, it checks the eviction policy.
- If the policy is set to noeviction, Redis doesl not evict any keys. Instead, it returns an error to the write command.
- Application code has to determine what to do with that error condition.

Each policy has its strengths and weaknesses. The best one for you depends on your specific needs.

It’s important to have a well-structured cache, combined with the right cache eviction policy in order to achieve performance goals when you have vast amounts of data. Redis, with its versatile capabilities, serves as an excellent caching solution and a powerful asset for applications handling large datasets. Effective cache management not only expedites data retrieval through cache hits but also mitigates the impact of cache misses, making Redis a reliable and efficient caching solution for diverse use cases.

Discover the intricacies of scaling cache with our comprehensive guide: The Definitive Guide to Caching at Scale with Redis. Learn the basics of caching to advanced enterprise application techniques in this one-stop resource.
