---
title: "Indexing and Querying"
linkTitle: "Indexing and Querying"
url: "/tutorials/guides/indexing/"
description: "Redis is a key-value store, so retrieving data by anything other than its key requires a secondary index. This guide covers how to build indexing and querying patterns in Redis using core data..."
aliases:
- "/tutorials/guides-indexing/"
date: 2026-02-24
lastmod: 2026-02-24
hidden: true
---

*Published 24 February 2026*

Redis is a key-value store, so retrieving data by anything other than its key requires a secondary index. This guide covers how to build indexing and querying patterns in Redis using core data structures.

**What you'll learn:**

- How to create secondary indexes with sorted sets, sets, and lists
- When to use lexicographical ranges for composite indexes
- How to query data without the Redis Search module
- When to upgrade to Redis Search for automatic indexing

## Introduction

Conceptually, Redis is based on the key-value database paradigm. Every piece of data is associated with a key, either directly or indirectly. If you want to retrieve data based on anything besides the key, you'll need to implement an index that leverages one of the many data types available in Redis.

You have various ways to create index using Redis core data structures, for example:

- Sorted sets to create secondary indexes by ID or other numerical fields.
- Sorted sets with lexicographical ranges for creating more advanced secondary indexes, composite indexes and graph traversal indexes.
- Sets for creating random indexes.
- Lists for creating simple iterable indexes and last N items indexes.

When using these data structures you must create your own API to keep the index up-to-date. To simplify and automate this task, Redis has Search that allows indexing and querying.

## How do I build a secondary index in Redis?

To build a secondary index in Redis, store your primary data in hashes and maintain a sorted set or set that maps the indexed field values to the hash keys. For example, if you have user hashes keyed by `user:{id}`, you can create a sorted set `index:users:age` where each member is the user key and the score is the user's age. This lets you query users by age range using `ZRANGEBYSCORE`.

For multi-field queries, use composite indexes by combining field values into sorted set members with lexicographical ordering, then query with `ZRANGEBYLEX`.

If your data has been [imported into Redis](/tutorials/guides/import/) using hashes, these indexing strategies let you query it efficiently without changing the underlying storage model.

## When should I use Redis Search instead of manual indexes?

If you need full-text search, faceted queries, or automatic index maintenance, [Redis Search](https://redis.io/docs/latest/develop/ai/search-and-query/) is the better choice. Manual indexes work well for simple lookups and range queries, but Redis Search handles complex querying patterns with less application code.

You can follow the [Redis quick start](/tutorials/howtos/quick-start/#secondary-indexing-and-searching-with-redis) to learn more about Redis Search, or see it in action with the [movies database search tutorial](/tutorials/howtos-search-movies-database-with-redis/) which demonstrates indexing, querying, and aggregations on a real dataset.

## Next steps

- [Import data into Redis](/tutorials/guides/import/) to prepare datasets for indexing
- [Search a movies database with Redis](/tutorials/howtos-search-movies-database-with-redis/) to see Redis Search in practice
- [Redis Search documentation](https://redis.io/docs/latest/develop/ai/search-and-query/) for the full query and indexing API
