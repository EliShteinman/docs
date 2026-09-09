---
title: "RediSearch Update: Aggregation & New Features"
linkTitle: "RediSearch Update: Aggregation & New Features"
url: "/blog/redisearch-update-aggregation-new-features/"
description: "One of the key announcements at RedisConf was the aggregation engine for RediSearch (version 1.1.0). Aggregations are an incredibly powerful feature for a real-time search engine like RediSearch...."
date: 2018-05-30
blogCategories:
- "Announcements"
- "New Product Announcements"
- "Product Releases"
authors:
- "Redis  "
lastmod: 2025-03-27
hidden: true
---

*By Redis   · Published 30 May 2018 · updated 27 March 2025*

![Blog tile image](/images/blog/0073e867b4e64f59de9047fdcde04295ba647e5c-772x550.webp)

One of the key announcements at RedisConf was the aggregation engine for [RediSearch](/redis-enterprise/technology/redis-search/) (version 1.1.0). Aggregations are an incredibly powerful feature for a real-time search engine like RediSearch. They allow for data to not only be queried, but summarized mathematically to gain analytical insight. RediSearch aggregations come with the standard toolkit of reducers:

- Counts
- Sums
- Minimum
- Maximum
- Standard Deviation
- Quantile

Conceptually, aggregations are comprised of a pipeline of operations. Each operation can be used in any logical order and can be repeated. The basic operations are:

- Group & Reduce
- Sort
- Transform (Apply)
- Limit
- Filter

For example, take shipments in an e-commerce scenario wherein you have a timestamp and total box size (box_area) for millions of shipments over the past ten years. Let’s say you want to find the top three years with the most shipments of boxes that have an area greater than 300. We don’t care about the exact number; we just want rough figures and it should be nicely formatted. Our aggregation query would look like this:

```python
FT.AGGREGATE shipments "@box_area:[300 +inf]" 
  APPLY "year(@shipment_timestamp / 1000)" AS shipment_year 
  GROUPBY 1 @shipment_year REDUCE COUNT 0 AS shipment_count 
  SORTBY 2 @shipment_count DESC 
  LIMIT 0 3 
  APPLY "format(\"%sk+ Shipments\",floor(@shipment_count / 1000))" AS shipment_count

```

This probably looks unlike any Redis command you’ve ever seen, but when you break it down it’s not that complicated.

| FT.AGGREGATE shipments "@box_area:[300 +inf]" | In the index “shipments,” find the items with box_area greater than 300. This uses the same query syntax as the rest of RediSearch. |
|---|---|
| APPLY "year(@shipment_timestamp)" AS shipment_year | This transforms shipment_timestamp into a year with the included function. This result will now be accessible as shipment_year. |
| GROUPBY 1 @shipment_year REDUCE COUNT 0 AS shipment_count | Group all the shipment_year results together and count them. Refer to this result as shipment_count. |
| SORTBY 2 @shipment_count DESC | We’ll sort these values in the descending order of our calculated counts from the previous step. |
| LIMIT 0 3 | We’re only interested in the first three values. |
| APPLY "format("%sk+ Shipments",floor(@shipment_count / 1000))" AS shipment_count | Transform the count again. Starting from the inner expression (inside floor), we’ll do some arithmetic to shorten numbers since we don’t care about exact values. Then we’ll use floor to drop anything after the decimal. Finally, we’ll format it using the printf style formatting and refer to it as (again) shipment_count. |

This outputs the following results:

```javascript
1) (integer) 10
2) 1) "shipment_year"
   2) "2014"
   3) "shipment_count"
   4) "10k+ Shipments"
3) 1) "shipment_year"
   2) "2017"
   3) "shipment_count"
   4) "9k+ Shipments"
4) 1) "shipment_year"
   2) "2015"
   3) "shipment_count"
   4) "9k+ Shipments"

```

By arranging these operations together you can rapidly analyze your data in ways previously not possible. It’s a very deep and expansive feature, larger than can be easily summed in this blog post, so it’s best to see it in action. Watch this video to see Dvir demoing aggregations:

[Click here to view video](https://www.youtube.com/embed/9h3Qco_x0QE)

Soon after RedisConf, we released RediSearch 1.2.0, which included a raft of new features:

## Query Attributes

Make a sub-query modify the clauses of a query. This allows for:

```javascript
~(ice cream sandwich) => { $weight: 0.5; }
```

The above command results in any document with “ice”, “cream” and “sandwich” to have a weight of 0.5. You can also modify the slop ($slop) and “in order” requirements ($inorder) based on a sub-query.

## Fuzzy Matching

Match any items with a single character distance. For example, “%redis%” would match not only ‘redis’ but also ‘jedis’ and ‘predis.’

## Conditional Updates

Update a document only if a condition is met, such as:

```javascript
FT.ADD idx myDoc 1.0 
   REPLACE PARTIAL
   IF "@timestamp < 12313134523" 
   FIELDS 
       title "new title"
```

This code would update the document ‘myDoc’ when the timestamp is below 12313134523. It would *only* update the title.

## Backslash Escaping

Use a backslash as an escape so that control characters are processed as normal text. This query would look for both “hello-world” and “world” in the indexed documents:

```javascript
FT.SEARCH idx "hello-world world"
```

## Synonym Support

In a situation where you have complete equivalents with different spellings, matching can be tricky. With FT.SYNADD and FT.SYNUPDATE you can add terms that are equivalents, and subsequently added documents will be matched. Given the following:

```javascript
FT.SYNADD idx hello hola hej bonjour
```

Any new documents with any of those terms would be matched on a query like this:

```javascript
FT.SEARCH idx hej
```

Lastly, version 1.2.0 was the last version of RediSearch being led by Dvir. We’re sad to [see him go](https://medium.com/@dvirsky/saying-goodbye-to-redisearch-7b1f888c4059) but we wish him well on his new adventures at a new organization (building something, we understand is very cool and very different from RediSearch). Don’t fret though, RediSearch is being developed by a full team of people here at [Redis](/) that will continue to innovate and push RediSearch forward.
