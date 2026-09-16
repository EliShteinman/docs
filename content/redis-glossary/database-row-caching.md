---
title: "Database row caching"
linkTitle: "Database row caching"
url: "/glossary/database-row-caching/"
description: "Database row caching is a technique used to improve performance and reduce the load on a relational database by storing frequently accessed database rows in memory, making it faster to retrieve..."
lastmod: 2025-06-30
mirrored: true
---

*updated 30 June 2025*

## What is database row caching?

Database row caching is a technique used to improve performance and reduce the load on a relational database by storing frequently accessed database rows in memory, making it faster to retrieve data from the cache rather than reading from the database.

## Database row caching in Redis

In an effort to improve performance, login and visitor sessions, shopping carts, and entire pages have been moved from a relational database to Redis. Individual product pages typically load only one or two rows from the database, and these rows can be cached individually in Redis. Caching individual rows from the relational database can be useful in cases where a full page cannot be cached or when reading the item’s row from the database could push the database to become overutilized, increasing costs.

To cache database rows in preparation for a heavy load, a daemon function can be written to cache specific database rows in Redis, updating them on a variable schedule. The rows will be stored as JSON-encoded dictionaries, and column names and row values will be mapped to the dictionary keys and values. The caching function will use two ZSETs, the scheduleZSET, which will use the row ID from the original database row as the member of the ZSET, and the delayZSET, which will use the same row ID for the members but the score will be how many seconds to wait between cache updates.

When the row ID is in the delay ZSET, it will be added to the schedule ZSET with the current timestamp. If a row needs to be removed from the cache, the delay can be set to less than or equal to 0, and the caching function will handle it. The scheduling function sets the delay for the item first, and then schedules the item to be cached now.

The caching function will pull the first item from the schedule ZSET with its score. If there are no items or if the timestamp returned is in the future, it will wait 50 milliseconds and try again. When an item that should be updated now is identified, the row’s delay is checked. If the delay for the next caching time is less than or equal to 0, the row ID is removed from the delay and schedule ZSETs, the cached row is deleted, and the function tries again. For any row that should be cached, the row’s schedule is updated, the row is pulled from the database, and a JSON-encoded version of the row is saved in Redis.

Overall, caching individual database rows can be an effective way to improve database performance, reduce the load on a relational database, and lower costs. By using Redis to cache frequently accessed rows, databases can operate more efficiently, even under heavy loads. Although other serialization formats such as XML, Google’s protocol buffers, Thrift, BSON, or MessagePack can be used, JSON is generally preferred because it is human-readable and concise, with fast encoding and decoding libraries available in every language with an existing Redis client. Though Redis does not allow nested structures, key names can be used, or nested structures can be explicitly stored using JSON or some other serialization library of choice.
