---
title: "7 Redis Worst Practices"
linkTitle: "7 Redis Worst Practices"
url: "/blog/7-redis-worst-practices/"
description: "Click here to get started with Redis Enterprise. Redis Enterprise lets you work with any real-time data at any scale, anywhere."
date: 2020-03-23
blogCategories:
- "Tech"
authors:
- "Redis  "
lastmod: 2026-06-01
hidden: true
mirrored: true
---

*By Redis   · Published 23 March 2020 · updated 1 June 2026*

![Blog tile image](/images/site-mirror/0073e867b4e64f59de9047fdcde04295ba647e5c-772x550.webp)

[*Click here to get started with Redis Enterprise. *](/try-free/)*Redis Enterprise lets you work with any real-time data at any scale, anywhere.*

*Your scientists were so preoccupied with whether or not they could, they didn’t stop to think if they should.*—Dr. Ian Malcolm, in *Jurassic Park*

“Best Practices” has become a trope in technology. Sure, you can do something with a given tool, but is doing so *really* a good idea? The fact that this topic comes up again and again, speaks to the flexibility of our tools. Best practices are great for beginners to learn the right things from the get-go. The problem is that, sometimes, as software engineers, we have imperfect memories of these best practices. Other times we accomplished what we need to do by not reading the manual and just hammering that square peg into the round hole, not realizing we were inadvertently playing the game on hard mode.

So let’s take a different approach: instead of looking at the best practices, let’s look at the worst. We’ve seen customers, open-source users, and even tools implement patterns that cry out for a disapproving headshake. Granted, we haven’t centralized this kind of wisdom before, so let’s start now with seven Redis ‘worst practices.’


## 1. No password

Based on the number of code examples I see floating around the web (indeed, probably even some of my own from years ago), a lot of people don’t bother to set a password on their Redis instance. For this to be a truly worst practice in current versions of Redis, you have to try really hard in redis.conf to open up a password-less Redis instance to the whole internet. Older versions, however, did allow for this practice. Why is forgoing a password a bad idea? Without a password, your server *will be found. *Once it is found, all sorts of shenanigans can occur, from flushing the database to stalling Redis by running high-complexity commands, all the way to altering files (via [CONFIG SET](https://redis.io/commands/config-set/)/[GET](https://redis.io/commands/config-get/)).

**TL;DR: **You will be h4x0r3d without a password.

**Best-practice alternative**: Set a password and use [AUTH](https://redis.io/commands/auth/).

## 2. KEYS

Weirdly, [KEYS](https://redis.io/commands/keys/) is one of the first commands people learn in Redis, even though using it is terrible (in production). For those who are enlightened enough to *not* know KEYS, it does a full iteration of all the keys (or a pattern) in a given database. Granted, this can be useful, especially for debugging, and not really a big deal if you have only a small number of keys. However, KEYS is a hidden killer as you scale. Consider four facts:

1. Redis is (for practical purposes) single-threaded
1. Redis can hold 232 keys
1. Redis Enterprise limits key sizes to 64KB while Redis Open Source’s limit is 512MB
1. KEYS is an O(n) operation.

So, writing an application that depends on KEYS is fine when you have dozens of keys—but this operation takes longer and longer with more and more keys. During this time, Redis is doing nothing but churning through the keys in the database. Imagine having to do 4,294,967,295 of anything, and you can understand why it will not be fast. Finally, KEYS is a synchronous command, so building up a response of all these keys—especially if they are large keys—is going to take a while, not to mention the time it takes to send it over the wire.

**TL;DR:** Redis gets bigger than you expect, and KEYS can clog your Redis server for a long time.

**Best-practice alternative**: Use [SCAN](https://redis.io/commands/scan/), which spreads the iteration over many calls, not tying up your whole server at one time.

## 3. Numbered databases/SELECT

[Salvatore Sanfilippo, the author of Redis, once called numbered databases the worst design mistake he ever made in Redis](https://groups.google.com/forum/#!msg/redis-db/vS5wX8X4Cjg/8ounBXitG4sJ). This design choice is a cautionary tale in building something that looks like it does one thing but actually does another. Thankfully, while this is becoming less common in the wild, Redis still ships with the ability to switch between different “databases” with the [SELECT](https://redis.io/commands/select/) command. Each database is isolated from a key perspective. So, key foo:bar on database 0 can be completely distinct from foo:bar in database 9. This all sounds rather nice, right? The problem is that these databases are not isolated in any other way. Running KEYS on database 0 will still freeze database 9. In effect, it looks like you can run independent workloads on each database, but in reality, they aren’t independent at all.

A bummer, but not really the worst practice, right? Well, the problem is that numbered databases are not well supported throughout the ecosystem. The first, and probably most dire, nail in the coffin of numbered databases is that they aren’t supported by any clustering system (open source nor Redis Enterprise clustering). In effect, you will never be able to leave a single node of Redis. Also, some modules do not support numbered databases.

**TL;DR:** Numbered databases don’t do what you think they do—and then paint you into a scaling corner.

**Best-practice alternative: **Run isolated instances of Redis—it has a low overhead, so why not? If you’re running Redis Enterprise, databases are isolated/multi-tenant by default.

## 4. Unbounded Returns with HGETALL, LRANGE, SMEMBERS, and ZRANGE

These commands fall into an interesting bucket: useful and benign most of the time, but cursed devils other times. The hash data structure in Redis allows you to set a series of field/value pairs under one key—[HGETALL](https://redis.io/commands/hgetall/) is a simple command that lets you retrieve everything in a hash all at once. This is fine, as most of the time you’re dealing with maybe up to a three-digit number of fields. Like keys, you can have 232 fields *and* values per hash. In most circumstances, you won’t have anywhere remotely near this many, but in some situations, you can accumulate high numbers of fields and values by the nature of your code (or logical error), additively increasing the number of fields over time. Then you run HGETALL and receive thousands of fields and values that may be up to 512MB each, meaning you have virtually the same problem as you do with KEYS.

Things are perhaps worse in [LRANGE](https://redis.io/commands/lrange/). LRANGE gets items out of a list in a given range; to get all the items LRANGE 0 -1 will do the trick. Lists in Redis are effectively linked lists, meaning each element has to be visited sequentially (to get the pointer to the next element). By now, you might have guessed that 232 elements (up to 512MB each) is the maximum, and you can accumulate very high numbers of elements. If you’re using Lists as a queue, just having a worker offline for a few minutes can cause the size of a list to grow quickly.

The story is more or less the same with Sorted Sets and Sets. They can store a ton of pieces of data, and each piece can be quite large. When you request all of them, this can take time.

**TL;DR: **Redis can store very large data structures. Expect the number of results to be 232 unless you know the number.

**Best-practice alternatives: **Run a command that sanity checks the size of data structures ([HLEN](https://redis.io/commands/hlen/) for hashes, [LLEN](https://redis.io/commands/llen/) for lists, [SCARD](https://redis.io/commands/scard/) for sets, and [ZCARD](https://redis.io/commands/zcard/) for sorted sets).

## 5. One request per connection

Many databases use the concept of REST as a primary interface—send a plain old HTTP request to an endpoint with arguments encoded as POST. The database grabs the information and returns it as a response with a status code, and closes the connection. Redis should be used differently—the connection should be persistent, and you should make requests as needed to a long-lived connection. However, well-meaning developers sometimes create a connection, run a command, and close the connection. While opening and closing connections per command will technically work, it’s far from optimal and needlessly cuts into the performance of Redis as a whole.

Using the OSS Cluster API, the connection to the nodes is maintained by the client as needed, so you’ll have multiple connections open to different nodes at any given time. With Redis Enterprise, the connection is actually to a proxy, which takes care of the complexity of connections at the cluster level.

**TL;DR: **Redis connections are designed to stay open across countless operations.

**Best-practice alternative: **Keep your connections open over multiple commands.

## 6. Hot keys

Redis can easily become the core of your app’s operational data, holding valuable and frequently accessed information. However, if you centralize the access down to a few pieces of data accessed constantly, you create what is known as a hot-key problem. In a Redis cluster, the key is actually what determines where in the cluster that data is stored. The data is stored in one single primary location based on hashing that key. So, when you access a single key over and over again, you’re actually accessing a single node/shard over and over again. Let’s put it another way—if you have a cluster of 99 nodes and you have a single key that gets a million requests in a second, all million of those requests will be going to a single node, not spread across the other 98 nodes.

Redis even provides tools to find where your hot keys are located. Use redis-cli with the –hotkeys argument alongside any other arguments you need to connect:

$ redis-cli --hotkeys

**TL;DR: **Don’t create a small number of frequently accessed keys.

**Best-practice alternatives: **When possible, the best defense is to avoid the development pattern that is creating the situation. Writing the data to multiple keys that reside in different shards will allow you to access the same data more frequently.

## 7. Running ephemeral Redis as a primary database

Redis is often used as a primary storage engine for applications. Unlike using Redis as a cache, using Redis as a primary database requires two extra features to be effective. Any primary database should really be highly available. If a cache goes down, then generally, your application is in a brown-out state. If a primary database goes down, your application also goes down. Similarly, if a cache goes down and you restart it empty, that’s no big deal. For a primary database, though, that’s a huge deal. Redis can handle these situations easily, but they generally require a different configuration than running as a cache.

**TL;DR:** Redis as a primary database is great, but you’ve got to support it by turning on the right features.

**Best-practice alternatives: **With Redis open source, you need to set up Redis Sentinel for high availability. In Redis Enterprise, it’s a core feature that you just need to turn on when creating the database. As for durability, both Redis Enterprise and open source Redis provide durability through AOF or snapshotting so your instance(s) start back up the way you left them.

There you have it—seven worst practices of Redis. Did we cover all of the bad practices out there? Of course not. Keep an eye on our blog or sign up for the Redis Watch newsletter to discover more things you absolutely, positively don’t want to do in Redis.

Did this post give you the flop sweats because you may be guilty of one (or seven) of these worst practices? Let us know on social media. As always, we love feedback on Twitter [@Redis](https://twitter.com/Redisinc).

## Want to learn more?

Watch our recent Tech Talk on Buy vs Build: Clustering & Provisioning in Redis Open Source vs Redis Enterprise!

[Watch the video](/events/redis-security-and-access-management-build-vs-buy/)
