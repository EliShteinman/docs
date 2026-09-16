---
title: "How We Increased Garbage Collection Performance with RediSearch 1.4.1"
linkTitle: "How We Increased Garbage Collection Performance with RediSearch 1.4.1"
url: "/blog/increased-garbage-collection-performance-redisearch-1-4-1/"
description: "With version 4.0, Redis exposed a new modules API that allows programmers to extend the database’s capabilities via new commands and data types. RediSearch uses this to allow full-text search of..."
date: 2018-10-29
blogCategories:
- "Tech Redis Modules"
authors:
- "Meir Shpilraien"
lastmod: 2025-03-04
hidden: true
mirrored: true
---

*By Meir Shpilraien, Developer · Published 29 October 2018 · updated 4 March 2025*

![Blog tile image](/images/site-mirror/eb01cdc97175aed400d1e1a5a9133974a370207c-1600x840.webp)

### Background

With version 4.0, Redis exposed a new modules API that allows programmers to extend the database’s capabilities via new commands and data types. [RediSearch](https://oss.redis.com/redisearch/) uses this to allow full-text search of data stored in Redis. The data is saved inside Redis as a hash (a core Redis data type), and each data record is called a document. The document’s data is also indexed inside RediSearch’s internal data structures. It is possible to tell RediSearch not to store the data inside a hash, in which case the document will only be indexed inside RediSearch’s internal data structures (this mode is called NOSAVE).

### Garbage Collection (GC) challenges

One main challenge search engines have to deal with is deleting and updating documents. In order to understand the problem, we first need to understand how RediSearch indexes the data. Let’s take, for example, the following document:

Doc1:
Name: “test”
Body: “this is an example”
RediSearch will create the following [inverted index](https://en.wikipedia.org/wiki/Inverted_index):

| Term | DocId |
|---|---|
| Test | Doc1 |
| This | Doc1 |
| is | Doc1 |
| an | Doc1 |
| example | Doc1 |

When a user searches for the term ‘example’, RediSearch immediately finds that term in the inverted index and returns Doc1 as the query’s result.

Now imagine that we need to delete Doc1 from the index by scanning all the terms in Doc1 and deleting its record from each term. The problem is that when running in NOSAVE mode, we do not have the data inside Doc1 and we do not know which terms need to be cleaned. It would be possible to keep track of each term in the document, but this can significantly increase the overall memory footprint.

The only other solution is to create a “Garbage Collection” (GC) mechanism that scans the entire index in the background and removes the deleted document from the inverted index. RediSearch [previously used this approach](https://oss.redis.com/redisearch/design/gc/). However, as the product evolved, we found that it could be extremely slow because it required scanning the entire index. In addition, since Redis is single-threaded, during the scan we had to acquire a global (single) lock, which made it impossible to perform queries or updates to the entire data set.

### The solution

To solve these problems, we came up with a new GC approach that leverages the advantages of the Linux fork process. Our goal was to acquire the global lock in as little time as possible, i.e. by not acquiring it during the scan but rather during actual memory releases only. Each time the GC starts, it creates a fork process, which scans the index in the background while the main process continues performing queries and updates. The fork process notifies the main process about what needs to be deleted, and then the main process acquires the lock for a very short time (that’s sufficient for deleting the relevant documents from the inverted index).

### Benchmark

We compared this new GC implementation with our prior approach by inserting 5 million records into the database, and then continuously updating all of them.

Note: This comparison was done over a simple laptop configuration using the following specs: MacBook Pro (Retina, 15-inch, Mid 2015), OS 10.11.6, CPU 2.2 GHz Intel Core i7, 16 GB memory at 1600 MHz DDR3. We could have run it over a stronger server configuration and probably gotten more impressive results, but decided these specs were good enough to demonstrate the advantages of our new approach.

|  | Old GC | New GC |
|---|---|---|
| Total bytes collected by GC | 908 KB | 80,727 KB |
| Insertion phase time (in seconds) | 484.657 | 447.099 |
| Update/delete phase time (in seconds) | 627.632 | 615.326 |
| Memory usage after insertion phase | 1.73 Gb | 1.73 Gb |
| Memory usage after update/delete phase | 1.84 Gb | 1.74 Gb |

As you can see, the main advantage of our new GC approach is that RediSearch can now collect 80,727 KB as opposed to 908 KB using the old GC mechanism, which is close to a 100X improvement. The old GC’s probabilistic approach of choosing an inverted index randomly and cleaning it took significantly more time. Our new GC approach runs on the entire index in each iteration, so it can clean all the garbage by the time we finish an update. Furthermore, the new approach doesn’t need to acquire the global lock while scanning the index.

### Enabling the new GC

The new GC mechanism is available today in our latest RediSearch release – version 1.4.1. It’s turned off by default, but can be activated by sending “GC_POLICY FORK” in the command line arguments when loading the module. Keep in mind that this is an experimental GC version, so we do not recommend using it in production just yet. However, if your use case requires lots of updates, you are welcome to try this new GC and give us your feedback. We intend to make this it the default configuration for RediSearch in a future release.

### Future work

We plan to extend our GC mechanism over time to increase GC performance even more. One approach we’re considering is using a heuristics mechanism to indicate which terms are more likely to have garbage, and clean those first.
