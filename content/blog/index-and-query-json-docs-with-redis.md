---
title: "Indexing, Querying, and Full-Text Search of JSON Documents with Redis"
linkTitle: "Indexing, Querying, and Full-Text Search of JSON Documents with Redis"
url: "/blog/index-and-query-json-docs-with-redis/"
description: "Related Resource: Click to download RedisJSON module."
date: 2021-07-07
blogCategories:
- "New Product Announcements"
- "Tech"
authors:
- "Pieter Cailliau"
lastmod: 2026-05-26
hidden: true
---

*By Pieter Cailliau, Product Manager · Published 7 July 2021 · updated 26 May 2026*

![Blog tile image](/images/blog/1bc52f14a1815b2ddf4f83221623b923b2bd04f5-772x520.webp)

*Related Resource: Click to *[*download RedisJSON module*](/json/)*.*

RedisJSON and RediSearch are by far the most popular Redis modules in our cloud. (See Fig. 1) The docker images of [RedisJSON](https://hub.docker.com/r/redislabs/rejson/) and [RediSearch](https://hub.docker.com/r/redislabs/rejson/) (bundled with Redis) are pulled [more than 2000 times](https://hub.docker.com/r/redislabs/rejson/) every single day. This is why we think of Itamar Haber, technology evangelist at Redis, as a visionary when he wrote the first version 4 years ago. In April, we made several [announcements at RedisConf](/blog/top-9-takeaways-from-redisconf-2021/) related to JSON, indexing and full-text search capabilities. Today, we’re happy to announce the private preview of these capabilities.

In this blog, we’ll give you an overview of the current RedisJSON capabilities. After that we’ll dive into the new capabilities section of this private preview. The ability to index, query, and use full-text search on JSON documents using RediSearch is the coolest new feature of this release. Finally, we’ll show you how to quickly get started.

![modules by REC](/images/blog/bd8042cf72910b77c6caa158ecdc26aeb9a77dc9-1024x690.webp)

## JSON capabilities

When you don’t have RedisJSON, you model nested documents in Redis by using the String data structure.

```python
redis.cloud:6379> SET myDoc '{"colors": ["green"]}'
OK

```

**But, what if we need to update a subpart of the document?**

To preserve the atomicity of the operation, we will need to:

1. [WATCH](https://redis.io/commands/watch/) for the document
1. Read the previous version and deserialize it
1. Embed the update in a Redis transaction
1. Serialize to JSON and update the document
1. Execute the transaction

We may need to retry all these steps if another client updated the document during this process.

```python
redis.cloud:6379> WATCH myDoc
OK
redis.cloud:6379> GET myDoc
"{\"colors\": \"green\"}"
redis.cloud:6379> MULTI
OK
redis.cloud:6379>(TX) SET myDoc '{"colors": ["green", "blue"]}'
QUEUED
redis.cloud:6379>(TX) EXEC
1) OK

```

However, with RedisJSON, we can do this update **with a single atomic transaction**:

```python
redis.cloud:6379> JSON.ARRAPPEND myDoc colors '"blue"'
(integer) 2

```

Let’s look at another example, one where you have a large JSON, but only require a subpart of that document in your application.

*Without RedisJSON:*

You have to:

1. Retrieve the whole json string, serialized as a string
1. Deserialize the JSON
1. Extract the subpart you need

```python
client.get("myDoc", function(err, reply) {
  const myJson = JSON.parse(myJsonString);
  const color = myJson.colors[0];
});

```

With RedisJSON, you can retrieve only the data you require with a single command, minimising CPU cycles, network overhead, and, most importantly, latency.

```python
redis.cloud:6379> JSON.GET myDoc $.colors[0]
"\"green\""

```

As you can see, RedisJSON simplifies JSON document manipulations. The current GA version of RedisJSON (v1.0) is the version the community is already widely using and solves exactly the shortcomings of modeling nested structures with a String data structure. Here’s an overview of some of its key capabilities.

***Store (or update) a JSON document associated with a key in Redis***

```python
redis.cloud:6379> JSON.SET myDoc . '{"title": "css", "colors": ["green"]}'
OK

```

***Replace a subpart (eg. the string value of a key)***

```python
redis.cloud:6379> JSON.SET myDoc title '"style"'
OK

```

***Add an item to a collection or a map***

```python
redis.cloud:6379> JSON.ARRAPPEND myDoc colors '"red"' '"blue"'
(integer) 3

```

***Extract the whole document***

```python
redis.cloud:6379> JSON.GET myDoc .
"{\"title\":\"css\",\"colors\":[\"green\"]}"

```

***Extract part of it using a subset of JSONPath***

```python
redis.cloud:6379> JSON.GET myDoc colors[0]
"\"green\""

```

## RedisJSON 2.0: Private Preview release

We announced this version at RedisConf 2021, and today we’re happy to announce that it’s available as a private preview for a select group of our Redis Enterprise customers—and as a release candidate to our community. This version has three major features, namely, full support of JSONPath expression, support for Active-Active (with Redis Enterprise), and the ability to index, query, and use full-text search on JSON documents with RediSearch. But there’s more! Let’s dive into the new goodies.

## Rewritten in RUST

[System programming languages](https://en.wikipedia.org/wiki/System_programming_language) is a family of languages oriented to efficiency. Programs written in these languages are usually lightweight and provide the best performances. This is [the reason](https://blog.eduonix.com/web-programming-tutorials/what-is-redis-and-why-is-it-so-popular/) why Redis has been historically written in C. It also explains why Redis is able to achieve extremely low latencies and high throughputs. Most of the Redis modules are written in C, C++, or Rust, which are languages of the same family.

JSON is especially well served by the Rust community including very fast and efficient [JSON serialisation](https://blog.logrocket.com/json-and-rust-why-serde_json-is-the-top-choice/) and [JSONPath implementation](https://crates.io/crates/jsonpath_lib). Giving the benefit of those implementations to Redis users was obvious and just required a mapping between the Redis module API and Rust.

## Full support for JSONPath

And here is the benefit of this RUST rewriting. This new version includes a comprehensive support of JSONPath. It is now possible to use all the expressiveness of JSONPath expressions.

***Given a JSON document***

```python
redis.cloud:6379> JSON.SET myDoc $ '{"colors":["red", "blue", "green"]}'
OK

```

***Wildcards (was previously limited to the first item)***

```python
redis.cloud:6379> JSON.GET myDoc $.colors[*]
"[\"red\",\"blue\",\"green\"]"

```

***Extract slices***

```python
redis.cloud:6379> JSON.GET myDoc $.colors[0:2]
"[\"red\",\"blue\"]"
redis.cloud:6379> JSON.GET myDoc $.colors[-1]
"["\"green\"]"

```

***A more advanced example with filter expressions***

```python
redis.cloud:6379> JSON.SET myDoc $ '{"books": [{"title": "Peter Pan", "price": 8.95}, {"title": "Moby Dick", "price": 12.99}]}'

redis.cloud:6379> JSON.GET myDoc '$.books[?(@.price < 10)]'
"[{\"title\":\"Peter Pan\",\"price\":8.95}]"

```

## Support for Active-Active

[Active-Active](/active-active/) is a feature provided by Redis Enterprise. Active-Active allows you to replicate your database into several geographically-distributed Redis Enterprise clusters. The users can connect to the closest cluster with local read and write latencies.

The implementation is based on [Conflict-free Replicated Data-Type](https://en.wikipedia.org/wiki/Conflict-free_replicated_data_type) ([CRDT](/blog/diving-into-crdts/)) technology. While implementing it for most of the core data structures supported by Redis, Redis developed a strong knowledge and experience confirmed by this new implementation made for JSON.

Application developers can now rely on this to build geo-distributed applications using JSON documents. Here is an example of a succession of operations in an active-active environment with two clusters:

![Clusters](/images/blog/18603d579c87da76682981fccec677afcf597b6b-565x240.webp)

Let see the detail of each operations:

- T1: A client sets a JSON document on Cluster 1.
- T2: The synchronisation process replicates the document on Cluster 2.
- T3: Both clusters contain the same document.
- T4: A client adds the blue color to the colors array in Cluster 1, and, concurrently, another client is adding the green color to the same array in Cluster 2.
- T5: The synchronization process merges the operation and updates the document on both clusters.
- T6: Both clusters contain the same document.

## RediSearch 2.2: Private Preview release

This blog also announces the availability of a private preview for RediSearch 2.2 (as a private preview for a select group of our Redis Enterprise customers and as a release candidate to our community).

In this section we’re going to describe the new features provided by this new release of RediSearch. But first, here is a reason why we are releasing those two popular modules together:

### Indexing, querying, and full-text search of JSON documents

This particular new feature will bring Redis’ JSON capabilities to a whole new level. Going beyond being a Key-Value store, until now, RediSearch has been providing indexing and search capabilities on hashes. Under the hood, RedisJSON 2.0 exposes an internal public API. Internal, because this API is exposed to other modules running inside a Redis node. Public, because any module can consume this API. So does RediSearch 2.2 !

By exposing its capabilities to other modules, RedisJSON gives RediSearch the ability to index JSON documents so users can now find documents by indexing and querying the content. These combined modules give you **a powerful, low latency, JSON-oriented document database**!

Let’s have a look at what this would look like.

We should first populate the database with a JSON document using the JSON.SET command.

```python
redis.cloud:6379> JSON.SET myDoc $ '{"title": "foo", "content": "bar"}'
OK

```

To create a new index, we use the FT.CREATE command. The schema of the index now accepts JSONPath expressions. The result of the expression is indexed and associated with an attribute (here: title).

```python
redis.cloud:6379> FT.CREATE myIdx ON JSON SCHEMA $.title AS title TEXT
OK

```

We can now do a search query and find our JSON document using FT.SEARCH:

```python
redis.cloud:6379> FT.SEARCH myIdx "@title:foo"
1) (integer) 1
2) "myDoc"
3) 1) "$"
   2) "{\"title\":\"foo\",\"content\":\"bar\"}"

```

## Aggregation on JSON documents

[Aggregation](https://redis.io/docs/stack/search/reference/aggregations/) is a powerful feature of RediSearch that can be used to create analytic reports or perform faceted search style queries. Now that RediSearch can access JSON documents, it’s possible to load any value from a JSON document using JSONPath expression and use it in a pipeline whether the value is indexed or not.

Let’s create an index:

```python
redis.cloud:6379> FT.CREATE myIdx ON JSON SCHEMA $.user.name AS name TEXT
OK

```

Add a JSON document to the database:

```python
redis.cloud:6379> JSON.SET myDoc . '{"user":{"name":"John 
Smith","hp":1000, "dmg":150}}'
OK

```

And do a simple computation using two numeric value extracted from the JSON document:

```python
redis.cloud:6379> FT.AGGREGATE myIdx '*' LOAD 6 $.user.hp AS hp $.user.dmg AS dmg APPLY '@hp - @dmg' AS points
1) (integer) 1
2) 1) "point"
   2) "850"

```

## More flexibility on the indexing strategy

With the new version of RediSearch, it’s now possible to index the same value (field on hashes, or JSON Values from a JSON document) with different parameters. Here is a typical use case, solved by this new feature:

Let’s have a database containing documents that belong to categories.

```python
redis.cloud:6379> HSET myDoc category "foo,bar,hello world"
(integer) 1

```

Using the TAG type you can then easily filter your search results on any category:

```python
redis.cloud:6379> FT.CREATE myIdx ON HASH SCHEMA category TAG
OK
redis.cloud:6379> FT.SEARCH myIdx "@category:{foo}"
1) (integer) 1
2) "myDoc"
3) 1) "category"
   2) "foo,bar,hello world"

```

But what if you also want to be able to do a full-text search on categories?

```python
redis.cloud:6379> FT.SEARCH myIdx "@category:{foo} @category:(hello)"
1) (integer) 0

```

Until now, with hashes, you had to duplicate the value into two fields, which would consume twice the memory.

This is where FT.CREATE…AS has become more than handy. Let’s get back to our nice and simple document:

```python
redis.cloud:6379> HSET myDoc category "foo,bar,hello world"
(integer) 1

```

…and use the new AS feature:

```python
redis.cloud:6379> FT.CREATE myIdx ON HASH SCHEMA category TAG category 
AS cat_txt TEXT
OK

```

…and…

```python
redis.cloud:6379> FT.SEARCH myIdx "@category:{foo} @cat_txt:(hello)"
1) (integer) 1
2) "myDoc"
3) 1) "category"
   2) "foo,bar,hello world"

```

Bingo! We can now filter by a tag, and do a full text search in the same field, **without having to duplicate the data.**

## Query profiling

Time complexity of most of the Redis commands is well documented. As an example, [HMGET](https://redis.io/commands/hmget/) comes with a complexity of O(N), “where N is the number of fields being requested.” With RediSearch, it’s possible to write advanced queries. The complexity of the FT.SEARCH and the FT.AGGREGATE commands, however, depend on the complexity of the query.

We wanted to give you the tools to understand what’s happening under the hood when a query is executed, to figure out where time is consumed, and how the query can be optimized. The new [FT.PROFILE](https://redis.io/commands/ft.profile/) command returns a tree showing the main steps used by RediSearch to execute the query. For each step, a time information is given.

So what happens inside RediSearch when we are doing a query with a fuzzy search ?

Let see an example:

```python
redis.cloud:6379> HSET doc:1 text "hello world"
(integer) 1

redis.cloud:6379> HSET doc:2 text "hallo world" 
(integer) 1

redis.cloud:6379> FT.CREATE idx ON HASH SCHEMA text TEXT
OK

```

We are ready to profile our query. Let’s run the profiling and decompose the profiling result.

redis.cloud:6379> FT.PROFILE idx SEARCH LIMITED QUERY "%hello%"

First we get the result. Useful to check that the profiling query returns what is expected.

```python
1) 1) (integer) 2
   2) "doc:2"
   3) 1) "text"
      2) "hallo world"
   4) "doc:1"
   5) 1) "text"
      2) "hello world"

```

Here is the total time, called “profile time”, because it includes the time spent in collecting the profile information.

```python
2) 1) 1) Total profile time
      2) "1.552"

```

The time spent in parsing the query and building the execution plan:

```python
2) 1) Parsing time
      2) "0.90900000000000003"
   3) 1) Pipeline creation time
      2) "0.105"

```

Here is the time spent in finding the fuzzy matches in the dictionary:

```python
4) 1) Iterators profile
      2)  1) Type
          2) UNION
          3) Query type
          4) "FUZZY - hello"
          5) Time
          6) "0.025999999999999999"
          7) Counter
          8) (integer) 2
          9) Child iterators
         10) "The number of iterators in the union is 2"

```

And finally, have you ever wondered what it means to build a search result? We need to compute the full-text score for each document, sort them by score, and finally load the fields. With this information you can identify bottlenecks, make queries faster, and improve performance of the server.

```python
5) 1) Result processors profile
      2) 1) Type
         2) Index
         3) Time
         4) "0.040000000000000001"
         5) Counter
         6) (integer) 2
      3) 1) Type
         2) Scorer
         3) Time
         4) "0.026000000000000002"
         5) Counter
         6) (integer) 2
      4) 1) Type
         2) Sorter
         3) Time
         4) "0.032000000000000001"
         5) Counter
         6) (integer) 2
      5) 1) Type
         2) Loader
         3) Time
         4) "0.255"
         5) Counter
         6) (integer) 2

```

## How to get started

We believe that these new capabilities are game changers for application developers and the Redis community. Here’s how you get started.

### Use the docker image of the preview

To get started you can pull the following [docker image](https://hub.docker.com/r/redislabs/redismod) with the :preview tag:

```javascript
docker run -p 6379:6379 redis/redismod:preview
```

Alternatively, you can compile from the RC1 release tags ([v2.2.0](https://github.com/RediSearch/RediSearch/releases/tag/v2.2.0) for RediSearch, [v2.0.0](https://github.com/RedisJSON/RedisJSON/releases/tag/v2.0.0) for RedisJSON) on both repositories and load them to Redis.

Once you’re up and running, you can try out all the above commands or with this [quickstart guide](https://redis.io/docs/stack/search/indexing_json/). We will also be launching a series of blogs about *RedisMart*, an online retail application that we showcased [during the keynote of RedisConf 2021](https://youtu.be/unQydnwJkZ4?t=1969). RedisMart leverages RediSearch and RedisJSON deployed in a geo-distributed manner to deliver the [best online retail experience](/industries/retail/). In this series, we’ll walk you step by step through how we build this application.

## Develop using the latest versions of the compatible clients

The following list of clients are currently being upgraded so you’re able to use the new features with a good developer experience. Check the latest releases and/or the pull requests (at this moment most of them are supporting the preview version on the master branches).

|  | RedisJSON | RediSearch |
|---|---|---|
| Node.js | redis-modules-sdk | redis-modules-sdk |
| Java | JredisJSON | JRediSearch |
| .NET | NRedisJSON | NRediSearch |
| Python | redisjson-py | redisearch-py |

## Join the community

We welcome any feedback, bug reports, feature requests while we work towards General Availability. Leave feedback on the documentation websites or in the github repositories of [RediSearch](/search/) (on [Github](https://github.com/RediSearch/RediSearch/)) or [RedisJSON](/json/) (on [Github](https://github.com/RedisJSON/RedisJSON/)), or get in touch with us on [Discord](https://discord.com/invite/redis).
