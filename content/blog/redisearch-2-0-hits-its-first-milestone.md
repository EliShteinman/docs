---
title: "RediSearch 2.0 Hits Its First Milestone"
linkTitle: "RediSearch 2.0 Hits Its First Milestone"
url: "/blog/redisearch-2-0-hits-its-first-milestone/"
description: "We are happy to announce the release of the first milestone in the development of RediSearch 2.0. RediSearch is a real-time search engine that lets you query your Redis data to answer a wide..."
date: 2020-07-29
blogCategories:
- "Company"
- "Tech"
authors:
- "Pieter Cailliau"
lastmod: 2025-03-27
hidden: true
mirrored: true
---

*By Pieter Cailliau, Product Manager · Published 29 July 2020 · updated 27 March 2025*

![Blog tile image](/images/site-mirror/05927a960d149febe063fdf0e3b62ccebf46e4ab-325x235.webp)

We are happy to announce the release of the first milestone in the development of [RediSearch](/redis-enterprise/redis-search/) 2.0. RediSearch is a real-time search engine that lets you query your Redis data to answer a wide variety of complex questions.

This milestone, dubbed 2.0-M01, marks the re-architecture of the way indices are kept in sync with the data. Instead of having to write data through the index (using the FT.ADD command), RediSearch will now follow the data written in hashes and automatically index it.

The big advantage here is that you can now add RediSearch to your existing Redis instance and create a secondary index without having to update your application code. This lets you immediately start using RediSearch on your existing data, simply by loading the RediSearch module and defining the schema. General availability of RediSearch 2.0 is expected this Fall.

(**Note: **This new feature introduces some changes to [the API](https://oss.redis.com/redisearch/Commands/) (listed below). We try to maintain backward compatibility as much as we can, but in this case it was just not possible. We plan to make adjustments and fixes going forward as we gather customer feedback.)

![](/images/site-mirror/c0dc68fd6042448d0b22206077beef67944c814e-1024x814.webp)

*The architecture of the RediSearch 2.0 milestone.*

## API changes

As noted above, this RediSearch 2.0 milestone includes several changes to the API:

1. **The index no longer lives in the key space. **If you used the index key (idx:<index name>) to list the indexes in the database, for example, this will no longer work. However, we introduced a command [FT._LIST](https://github.com/RediSearch/RediSearch/pull/1337) to return all the indices in the database.
1. **Indexes must be created with a prefix/filter. **These specify which documents will be indexed automatically by RediSearch. You can specify a simple prefix and/or a complicated filter expression.
1. **Upgrades are not possible. **If you have an [RDB](https://redis.io/topics/persistence) created with an older version of RediSearch, RediSearch 2.0 will not be able to read it. Currently, you will have to re-index the entire data set. We are, however, working on an upgrade process for the GA release.
1. **It works only with Redis 6 and above.**
1. **The FT commands were mapped to their Redis-equivalent commands. **This allows existing applications to still work with RediSearch 2.0. The mappings are as follows:
  1. FT.ADD => HSET
  1. FT.DEL => DEL (DD by default)
  1. FT.GET => HGETALL
  1. FT.MGET => HGETALL
1. **The inverted index itself is no longer saved to the RDB**. This does not mean that persistency is not supported. RediSearch does save the index definition to the RDB and index the data in the background after Redis is started. You can find out when the reindexing is finished by checking the indexing status using the [FT.INFO](https://oss.redis.com/redisearch/Commands/#ftinfo) command.

## The new API

The biggest update to the API is how indices are created. In RediSearch 2.0 the command [FT.CREATE](https://redis.io/commands/ft.create/) is used to create indices. The additions to the API are highlighted in yellow here:

```javascript
FT.CREATE {index}
    ON {structure} [PREFIX {count} {prefix} [{prefix} ..] [FILTER {filter}] [LANGUAGE_FIELD {lang_field}] [LANGUAGE {lang}] [SCORE_FIELD {score_field}] [SCORE {score}] [PAYLOAD_FIELD {payload_field}]
   [TEMPORARY {seconds}] 
   [MAXTEXTFIELDS]
   [NOOFFSETS] [NOHL] [NOFIELDS] [NOFREQS]
   [STOPWORDS {num} {stopword} ...]
   SCHEMA {field} [TEXT [NOSTEM] [WEIGHT {weight}] [PHONETIC {matcher}] | NUMERIC | GEO | TAG [SEPARATOR {sep}] ] [SORTABLE][NOINDEX] ...
```

Let’s dig into some of the details:

- ON {structure} currently supports only HASH
- PREFIX {count} {prefix} tells the index which keys it should index. You can add several prefixes to index. Since the argument is optional, the default is *** **(all keys)
- FILTER {filter} is a filter expression with the full RediSearch [aggregation expression language](https://redis.io/docs/stack/search/reference/aggregations/). It is possible to use @__key to access the key that was just added/changed
- LANGUAGE and SCORE let you override the default language and score for all documents that are indexed
- LANGUAGE_FIELD, SCORE_FIELD, and PAYLOAD_FIELD allow you to have document-specific language and scoring, and to use payload as a field within the document.

## Other limitations and changes

The RediSearch 2.0-M01 milestone also brings a few other updates:

- [NOSAVE](https://oss.redis.com/redisearch/Commands/#ftadd) is no longer supported.
- Updating hashes implies that the entire document will be indexed (keyspace notifications don’t address which fields were changed). So partial updates will be slower. Note that we are still investigating options to improve performance in these situations.
- Field names are now case sensitive, so declaring a field “FOO” and indexing it as “foo” will not work.
- The FT.ADD command will be mapped to hset as shown here:

FT.ADD idx doc1 1.0 LANGUAGE eng PAYLOAD payload FIELDS f1 v1 f2 v2

Is mapped to

HSET doc1 __score 1.0 __language eng __payload payload f1 v1 f2 v2

This means that the score, language, and payload fields on your index must be called __score, __language, __payload, accordingly, in order for the mapping to work as expected.

- FT.ADDHASH is no longer supported. Use HSET.
- FT.OPTIMIZE is no longer supported, the RediSearch [Garbage Collection](https://oss.redis.com/redisearch/Overview/#index_garbage_collection) function is responsible for optimizing the index.

## Conclusion

We are really excited about these changes because you can now [load RediSearch into your existing Redis database](https://oss.redis.com/redisearch/Quick_Start/#download_and_running_binaries) and index your existing data that resides in hashes, without having to update your application logic when manipulating these documents. You can try out this [milestone release](https://github.com/RediSearch/RediSearch/releases/tag/v1.99.1) by taking the source code from [GitHub](https://github.com/RediSearch/RediSearch) or by using the *1:99:1* [RedisSarch Docker image](https://oss.redis.com/redisearch/Quick_Start/#running_with_docker). This version is not yet production ready, but we wanted to share it with you now to gather your feedback. Please share any comments or issues on our [GitHub repository](https://github.com/RediSearch/RediSearch/) or in the [Redis Community forum](https://forum.redis.com/c/modules/redisearch/58).
