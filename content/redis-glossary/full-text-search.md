---
title: "Full Text Search"
linkTitle: "Full Text Search"
url: "/glossary/full-text-search/"
description: "Full text search is a technique used in information retrieval that allows searching for documents or data based on the presence of keywords or phrases within the entire text of the document. Unlike..."
lastmod: 2025-06-30
mirrored: true
---

*updated 30 June 2025*

## What is Full Text Search?

Full text search is a technique used in information retrieval that allows searching for documents or data based on the presence of keywords or phrases within the entire text of the document. Unlike traditional search methods that rely on simple matching of keywords, full text search takes into account the context, synonyms, and word proximity to provide more relevant search results.

Full text search engines use algorithms to index the content of documents or data sources, and allow users to query the index using natural language queries or Boolean operators to filter and refine results. Full text search is commonly used in databases, search engines, content management systems, and other applications that require efficient and accurate searching of large volumes of text-based data.

## Redis Full Text Search best practices

*Prior to the advent of modules, full-text search was implemented using native Redis commands. The *[*RediSearch*](https://redis.io/search/)* module provides much higher performance than this pattern. However, in some environments, RediSearch is not available. Additionally, this pattern is very interesting and can be generalized to other workloads for which RediSearch may not be ideal.*

Let’s say you want to search a number of text documents—this may not be an obvious use case for Redis as it access via keys rather than tables. But on the contrary, Redis can be used to underpin a very novel full-text search engine.

First, let’s take some examples:

- “Redis is very fast”
- “Cheetahs are fast”
- “Cheetahs have spots”

Let’s break down these items into sets of words just limited by space for simplicity:

Notice that we’re giving each line its own set (ex1…) and then we’re adding multiple members to that set based on each word (even though it might looks we’re just adding the entire line, SADD is variadic, so accepts multiple members. We’ve also turned all the words lowercase.

Next we need to invert this index and show which word is located in which document. To do this, we’ll make a set for each word and then put the document set names as members.

For clarity, we’ve split this up into individual commands, but all the commands would normally be atomicly executed with a [MULTI/EXEC](https://redis.io/topics/transactions) block.

To query our tiny full-text search index, we will use the [SINTER](https://redis.io/commands/sinter) command (set intersect). To find the documents with “very” and “fast”

In a situation where we don’t have any documents that match the query, we’ll get an empty result:

If you wanted an logical or search, you can substitute [SUNION](https://redis.io/commands/sunion) (set union) for SINTER.

Deleting an item from the index is a little more involved. First, we’ll get the document index members from the document set (SMEMBERS) then remove the document IDs from the word indexes.

This cannot be completed in a single operation in Redis, so you’ll need to get the results of SMEMBERS then issue the SREM commands afterwards.

Of course, this is a very simple full-text search. You create a more reflective index by using Sorted Set commands instead of Set commands. This way, as example, if a document contains a word more than once, you can have it “rank” higher than a document that has only one occurrence. The patterns above stay more-or-less the same except use Sorted Set commands.
