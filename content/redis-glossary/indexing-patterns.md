---
title: "Indexing Patterns"
linkTitle: "Indexing Patterns"
url: "/glossary/indexing-patterns/"
description: "Indexing patterns refer to the strategies used to organize and structure data in a search index to optimize the performance of search queries. The goal of indexing patterns is to reduce the amount..."
lastmod: 2025-06-30
mirrored: true
---

*updated 30 June 2025*

## Indexing Patterns Defined

Indexing patterns refer to the strategies used to organize and structure data in a search index to optimize the performance of search queries. The goal of indexing patterns is to reduce the amount of time and resources required to search large datasets.

## Redis Best Practices for Indexing Patterns

Redis is an in-memory key-value store that is commonly used as a cache or a database. Unlike traditional relational databases, Redis does not support SQL queries and indexing patterns in the same way. Redis Search, a source available Redis module, has been mostly known as a tool for full-text search. But with its recent 2.0 release, [Redis Search](https://redis.io/search/) has become more powerful and general purpose, providing the missing query and indexing engine for Redis.

### The Redis Data Model

A Redis database contains many keys, and the key names create a namespace. Each key in a Redis database is like a primary key in a relational database. For example, to model a user in Redis, one way is to have a hash for each user. Each hash is accessed with a key like “users:profile:user_id”. Inside the hash, the user’s first and last name, username, registration date, and other data are stored.

### Secondary Indexing in Redis

If you want to query on attributes other than the primary key, such as by last name or registration date or country of residence, you need a secondary index. A secondary index maps each attribute to a set of primary keys that have that attribute. In Redis, you need to create a Redis Search index on your data before you can query it.

### Traditional Databases vs. Redis

In a traditional relational database like PostgreSQL, you store your data in tables and query it using SQL. To make the queries efficient, you add indexes. In Redis, you store your data in hashes and create a Redis Search index on the data before querying.

### Creating Redis Search Indexes

Creating Redis Search indexes involves specifying the fields you want to index, which data type they are, and the name of the index. For example, to index the first name, last name, bio, registration date, and country code of a user, you would run the following command:

### Querying Redis Search

Once you have created an index, you can query it using Redis Search’s querying features. Redis Search supports complex querying features such as full-text search, numeric range queries, and geospatial queries.
