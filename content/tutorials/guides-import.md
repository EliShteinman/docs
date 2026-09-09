---
title: "Import Data into Redis"
linkTitle: "Import Data into Redis"
url: "/tutorials/guides/import/"
description: "Redis offers multiple ways to import data into a database: from a file, a script, or from an existing Redis database. Whether you need to bulk load CSV data, restore an RDB snapshot, or migrate..."
aliases:
- "/tutorials/guides-import/"
date: 2026-02-25
lastmod: 2026-03-19
hidden: true
---

*Published 25 February 2026 · updated 19 March 2026*

> **TL;DR:**
>
> The fastest way to bulk load data into Redis is with `redis-cli --pipe`, which uses the Redis protocol to stream commands directly into the server. For structured data like CSV, JSON, or SQL, use [RIOT-X](https://github.com/redis/riotx-dist) to transform and import in a single step.

Redis offers multiple ways to import data into a database: from a file, a script, or from an existing Redis database. Whether you need to bulk load CSV data, restore an RDB snapshot, or migrate from an RDBMS, this guide covers the most common approaches.

## What you'll learn

- How to bulk insert data using a redis-cli script
- How to use redis-cli pipe mode for mass insertion
- How to restore data from an RDB file
- How to import and synchronize data using RIOT (CSV, JSON, SQL)
- How to load data into Redis Cloud

## How do I bulk insert data using a redis-cli script?

1\. Create a simple file `users.redis` with all the commands you want to run

```bash
HSET 'user:001' first_name 'John' last_name 'doe' dob '12-JUN-1970'
HSET 'user:002' first_name 'David' last_name 'Bloom' dob '03-MAR-1981'
```

2\. Use the `redis-cli` tool to execute the script

```bash
redis-cli -h localhost -p 6379 < users.redis
```

This approach runs each command sequentially and will not impact the existing data, except if you modify existing keys in the script.

> **INFO**
>
> Sample dataset: You can find sample datasets ready to be imported using this method in the [`redis-datasets`](https://github.com/redis-developer/redis-datasets) repository.

## How do I use redis-cli pipe mode for mass insertion?

For large-scale bulk loading, `redis-cli --pipe` is significantly faster than running commands one at a time. Pipe mode sends data using the Redis protocol in a streaming fashion, avoiding the round-trip latency of individual commands.

```bash
cat data.txt | redis-cli --pipe
```

The input file must use the Redis serialization protocol (RESP). You can generate RESP-formatted commands from CSV or other data sources using a script and then pipe the output into Redis.

## How do I restore data from an RDB file?

If you have an RDB file `dump.rdb` that contains the data you want, you can use this file to create a new database.

1.  Copy the `dump.rdb` file into the Redis working directory.

    If you do not know which folder this is, you can run the command [`CONFIG get dir`](https://redis.io/commands/config-get) on your running Redis instance.

2.  Start the Redis service with `redis-server`.
3.  The file `dump.rdb` is automatically imported.
4.  Connect to the database using `redis-cli` or any other client to verify the data has been imported (for example, using [`SCAN`](https://redis.io/commands/SCAN)).

### Related Articles

[Redis Persistence](https://redis.io/topics/persistence)

## How do I import data using RIOT?

[Redis Input/Output Tools (RIOT-X)](https://github.com/redis/riotx-dist) is a set of import/export command line utilities for Redis. RIOT-X is the recommended tool when you need to bulk import CSV, JSON, or SQL data into Redis.

- **RIOT DB:** migrate from an RDBMS to Redis, Search, JSON, and more.
- **RIOT File:** bulk import/export data from/to files (CSV, JSON).
- **RIOT Gen:** generate sample Redis datasets for new feature development and proof of concept.
- **RIOT Redis:** live replication from any Redis database (including AWS ElastiCache) to another Redis database.
- **RIOT Stream:** import/export messages from/to Kafka topics.

## How do I import data into Redis Cloud?

You can easily import data into Redis Cloud. See the following documentation:

- [Importing Data into Redis Cloud](https://redis.io/tutorials/guides/import/)

## Next steps

Once your data is loaded into Redis, you may want to create indexes to query it efficiently. See the [Indexing and Querying](/tutorials/guides/indexing/) guide to learn how to build secondary indexes using Sorted Sets, Hashes, and Redis Search.
