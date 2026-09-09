---
title: "Redis Namespace and Other Keys to Developing with Redis"
linkTitle: "Redis Namespace and Other Keys to Developing with Redis"
url: "/blog/5-key-takeaways-for-developing-with-redis/"
description: "Download Nine Essential Database Capabilities and make sure your database has what it takes to meet all your demands"
date: 2022-05-18
blogCategories:
- "Tech"
authors:
- "Itamar Haber"
lastmod: 2026-08-13
hidden: true
---

*By Itamar Haber, Technology Evangelist · Published 18 May 2022 · updated 13 August 2026*

![Blog tile image](/images/site-mirror/e52cffc4ae0ae4a941d16aec9562a67df2a9536b-772x550.webp)

![redis namespace](/images/site-mirror/ecc6a0858fe54fe19e69c00e009af3bc3d324aff-300x200.webp)

[*Download Nine Essential Database Capabilities*](/docs/9-essential-database-capabilities/)* and make sure your database has what it takes to meet all your demands*

Developing an application with Redis is a lot of fun, but as with any technology, there are a few points you should keep in mind while designing a Redis-based or Redis namespace application. You’re probably already familiar with relational database development, but while many of the same practices apply, keep in mind that Redis is an in-memory database and it is (mostly) single-threaded. Read on to explore Redis keys best practices.

Therefore, there are several peculiarities you should pay attention to when using Redis:

## 1. Keep track of your keys with Redis namespace

Databases store data, but any developer can lose track of some of the data you’re putting into Redis. This is only natural, due to your application’s requirements changing or you changing the way you store the data. Perhaps you’ve neglected to EXPIRE some of the keys, or maybe a module of the application has been retired.

Whatever the case, chances are that some of the data in your Redis database are no longer used and taking up space for no purpose. Redis’ schema-less nature makes it extremely difficult to make sense of your dataset’s contents unless you use a solid nomenclature for your keys. Using a proper naming methodology with Redis namespace for your keys can make the housekeeping of your database much easier. When you namespace your keys by application or service – the convention is to use the colon (‘:’) character to delimit parts of the key’s name -a Redis namespace best practice. This way, you’ll be able to identify them easily during a data migration, conversion, deletion, or move. Redis namespace & Redis namespace keys help with this identification.

Beyond Redis namespace, Another common use case for Redis is as a secondary data store for “hot” data items, while most of the data is kept in another database (e.g. PostgreSQL, MongoDB). In such cases, developers quite often forget to remove the data from Redis when it is moved from the primary data store. This sort of cross-datastore dependency requires a cascading delete, which can be implemented by keeping all the identifiers for a given data item in a Redis set. This ensures that a cleanup procedure invoked after deletion from the primary data store only needs to iterate through that set’s contents in order to remove all the relevant copies and related tidbits (including the set itself upon completion).

## 2. Keep track of the length of your key names

This might seem contradictory to the above regarding Redis namespace, but since key names take up memory as well, you should strive to keep them short. Obviously, this becomes an issue with datasets consisting of millions or billions of keys, but the fact is that long keys have a price with any hashtable.

For example: consider that storing 1,000,000 keys with Redis namespace, each set with a 32-character value, will consume about 96MB when using 6-character key names, and 111MB with 12-character names (on a 32-bit Redis server). This overhead of more than 15% becomes quite significant as your number of keys grows. With Redis deleting keys with prefixes is also a possibility.

## 3. Use the right data structures

Either because of memory usage or performance, sometimes one data structure is a better fit for your data set than another. Here are a few best practices to bear in mind:

- Instead of storing your data in thousands (or millions) of independent string values, consider grouping related data with the hash data structure. Hashes are very efficient and can decrease your memory usage (plus they offer the added value of abstracting some of the details and making your code more readable). For more information on that, check out this [article](https://redis.io/topics/memory-optimization).
- When applicable, use lists instead of sets. If you don’t need the set’s properties for ensuring uniqueness or checking membership, a list will consume less memory and perform inserts faster.
- Sorted sets are the most expensive data structure, both in terms of memory consumption and basic operations complexity (e.g. ZADDing a new member). If you just require a way to look up scores and order isn’t important, consider using hashes instead.
- An often overlooked feature in Redis are bitmaps, or bitsets (available since v2.2). Bitsets allow you to perform several bit-level operations on Redis values, which could mean storing large amounts of data efficiently. This can be used, for example, for some [lightweight analytics](http://blog.getspool.com/2011/11/29/fast-easy-realtime-metrics-using-redis-bitmaps/).

## 4. Use SCAN, never use KEYS

The [SCAN](https://redis.io/commands/scan) command is available starting with Redis v2.8 and enables you to retrieve keys in the keyspace using a cursor. This behavior is unlike that of the (hiss) KEYS command, which returns all matching elements at once, but is considered risky in production because it may block your Redis server and even exhaust its RAM resources. SCAN, on the other hand, makes it possible to inspect the data without the risk of blocking your server or having to rely on a slave.

Note that SCAN requires you to read a cursor value that’s passed to the subsequent call to SCAN. SCAN also accepts a keyname pattern and an optional count argument. Another difference between SCAN and KEYS is that it is possible to get the same key name more than once with SCAN.

SCAN is accompanied by SSCAN, HSCAN, and ZSCAN, which allow you to iterate the contents of sets, hashes, and sorted sets (respectively).

## 5. Use Server-Side Lua Scripts

As a developer, you’ll be navigating familiar ground once you embrace Redis’ ability to run Lua scripts. One of the easiest languages to pick up, Lua offers you the ability to express your creativity with code that runs inside the Redis server itself. When applied correctly, Lua scripts can make a world of difference in terms of performance and resource consumption. Instead of bringing data to the (application’s) CPU, scripts allow you to execute logic near the data, which reduces network latency and redundant transmission of data.

A classic example of Lua’s dramatic impact happens when you’re fetching a lot of data from Redis only to filter or aggregate it in your application. By encapsulating the processing workflow in a script, you only need to invoke it in order to get the significantly smaller answer at a fraction of the time and the resources.

**Pro Tip:** Lua is great, but once you move workflows to it you may find that error reporting and handling are harder (you are running, after all, inside the Redis server). One clever way around that is using Redis’ Pub/Sub and having your scripts publish their “log” messages to a dedicated channel. Then, set up a subscriber process to get these messages and handle them accordingly.

There are probably many other important tips you’ll pick up during your Redis escapades, but this list should help to get you started with some of the most important ones. If you have other suggestions that you want to share, feedback or questions – please feel free to [shout](https://twitter.com/itamarhaber) at [me](mailto:itamar@redis.com), I’m highly available 🙂

---
