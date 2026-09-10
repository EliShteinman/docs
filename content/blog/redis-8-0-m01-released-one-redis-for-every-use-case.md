---
title: "Redis 8.0-M01 released – One Redis for every use case"
linkTitle: "Redis 8.0-M01 released – One Redis for every use case"
url: "/blog/redis-8-0-m01-released-one-redis-for-every-use-case/"
description: "We have announced Redis 8, the most advanced and performant Redis offering yet. Today, we’re happy to announce that the first milestone of Redis 8 is available in the Community Edition for you to try."
date: 2024-09-19
blogCategories:
- "Announcements"
- "Product Releases"
- "Tech DE"
authors:
- "Mirko Ortensi"
- "Pieter Cailliau"
lastmod: 2026-08-13
hidden: true
mirrored: true
---

*By Mirko Ortensi, Pieter Cailliau · Published 19 September 2024 · updated 13 August 2026*

![Blog tile image](/images/site-mirror/e8056277925e8c4d8c5ecb7cef67d0e285e0cff3-772x552.webp)

We have announced [Redis 8](/blog/introducing-another-era-of-fast/), the most advanced and performant Redis offering yet. Today, we’re happy to announce that the first milestone of Redis 8 is available in the Community Edition for you to try.

Redis 8 introduces seven new data structures —JSON, time series, and five probabilistic types— along with the fastest and most scalable Redis query engine to date. These capabilities, previously only available separately through Redis Stack or our Software and Cloud offerings, are now built natively into Redis Community Edition. The technical advancements continue to make Redis a great choice for real-time databases, especially for those needing robust search, query, and data analysis capabilities. This release introduces advanced capabilities like vector search, secondary indexing for full-text search, exact matching, geospatial queries, numeric data handling, and data processing. Additional key features will be revealed in upcoming milestone releases, further enhancing Redis’ real-time capabilities.

What does this mean for our community? You can leverage Redis’s latest data capabilities, using it as a document store for managing JSON documents or as a vector database to power GenAI applications.

As we work towards the GA release of Redis 8, we’ll provide a sneak peek into the new things you can do with it, including how Redis 8 transforms traditional use cases like session management, caching, and recommendation systems, making apps built on Redis even richer and more versatile.

## Flexible session management

Sessions are traditionally modeled as strings or hashes. While string serialization and deserialization offer a naive instant solution, session managers must extract and store the entire session from the database, causing extraneous data processing that leads to suboptimal performance and data transfer costs.

Storing session data as hashes represents a logical evolution. Still, it’s only when hashes are adopted together with cross-session searches that they reveal the otherwise unexploited value hidden in the active sessions. For the first time, with Redis 8, you can search through active sessions to provide real-time insights, automatically drive operational decisions, detect usage patterns, and run various queries directly on the session data. Furthermore, with the recent addition of [hash-field expiration](https://redis.io/docs/latest/develop/data-types/hashes/#field-expiration) in Redis Community Edition 7.4, it’s possible to manage temporary data within a session.

But that’s not all. You can take session management even further with JSON session modeling, which supports a flexible way to store and retrieve data from user sessions. Serialization and deserialization are no longer required, which helps speed up operations and reduce the bandwidth of data transfer, thus reducing the associated costs.

In addition to single-session data retrieval using the JSONPath syntax, performing real-time search operations across active sessions provides live information to improve the user experience. It accelerates data analysis, thus adding value to inventory management, distribution chains, reservation systems, and more.

### Session modeling with the string data structure is a standard approach many ecosystems adopt

While it represents the simplest implementation (popular in frameworks like Laravel or Flask), it is not optimal, as it requires serializing and deserializing the entire session for every read or write operation.

```python
> SETEX "sf_s82099723004b48095935cddc89b29fa2" 1440 "_sf2_attributes|a:1:{s:15:\"sym-session-key\";s:17:\"sym-session-value\";}_sf2_meta|a:3:{s:1:\"u\";i:1722251396;s:1:\"c\";i:1722251264;s:1:\"l\";i:0;}"
"OK"

> GET sf_s82099723004b48095935cddc89b29fa2
"_sf2_attributes|a:1:{s:15:\"sym-session-key\";s:17:\"sym-session-value\";}_sf2_meta|a:3:{s:1:\"u\";i:1722251396;s:1:\"c\";i:1722251264;s:1:\"l\";i:0;}"2.

```

### You can unlock flexible session modeling with hashes to avoid entire session serialization/deserialization

This reduces bandwidth consumption and computational overhead. Frameworks like Spring take this approach: retrieving one or multiple entries from the session with a single network operation.

```python
> HSET session:ab6094d4-ba19-407d-b6c2-f7643f171fcf id mortensi sessionAttr:promo ABC-abc-1234
(integer) 2

> HMGET session:ab6094d4-ba19-407d-b6c2-f7643f171fcf id
1) "mortensi"

```

### Hash session modeling grants more control

Hash session modeling plus hash-field expiration introduced in Redis 7.4 grants more control over user session data. With hash-field expiration, session data can be expired while the session is still active. This greatly simplifies bookings and reservations, where the user must complete an action within a time frame.

```python
> HEXPIRE session:ab6094d4-ba19-407d-b6c2-f7643f171fcf 7200 FIELDS 1 sessionAttr:promo
1) "1"

> HTTL session:ab6094d4-ba19-407d-b6c2-f7643f171fcf FIELDS 1 sessionAttr:promo
1) "7185"

```

### You can unlock hash-searchable sessions with Redis 8

The embedded query engine enables cross-session searches to retrieve vital information for your business. Search by any data like the location and timestamp and get a user’s active sessions to discover what is happening and provide insights to improve user experience.

```python
> FT.CREATE session_idx ON HASH PREFIX 1 session: SCHEMA sessionAttr:promo AS promo TAG
"OK"

> FT.SEARCH session_idx '@promo:{ABC\-abc\-1234}' RETURN 1 id
1) "1"
2) "session:ab6094d4-ba19-407d-b6c2-f7643f171fcf"
3) 1) "id"&nbsp;&nbsp;&nbsp;
   2) "mortensi"

```

### Unlock session modeling with JSON

Unlock session modeling with JSON with Redis 8 and model sessions to represent hierarchical data with arrays, objects, and a set of commands to interact with the session. Use JSONPath for session lookups and to access specific elements and enjoy the interoperability for the web, microservices, programming languages and more, granted by the de facto standard for data transmission.

```python
> JSON.SET session:a30d0c64-4cad-4088-a9ef-f1889d182df4 $ '{"lastAccessedTime":1672475765650,"creationTime":1672475765649,"user":{"name":"John","last":"Doe"},"visited":["www.redis.io","www.google.com"], "location": "34.638,31.79", "cart":[{"itemId":"hp-2341","itemCost":1990.99,"quantity":3},{"itemId":"MacBook","itemCost":2990.99,"quantity":15}]}'
"OK"

> JSON.GET session:a30d0c64-4cad-4088-a9ef-f1889d182df4 $.user.name
"[\"John\"]"

```

### Unlock JSON-searchable sessions

Redis 8 supports secondary indexing so you can create indexes at arbitrary depth and perform real-time searches and data analysis. You can perform either in-session searches with JSONPath or cross-session searches to discover vital data from the active sessions. Impossible to miss the data you are looking for.

```python
> FT.CREATE session_idx ON JSON PREFIX 1 session: SCHEMA $.lastAccessedTime AS lastAccessedTime NUMERIC SORTABLE $.creationTime AS creationTime NUMERIC SORTABLE $.visited AS visited TEXT $.cart[*].itemId AS itemid TAG $.location AS loc GEO
"OK"

> FT.SEARCH session_idx '@itemid:{MacBook}' RETURN 0
1) "1"
2) "session:a30d0c64-4cad-4088-a9ef-f1889d182df4"

```

Redis is often used to manage sessions in retail and eCommerce applications. Redis 8 gives you more control and flexibility over these sessions. Imagine tracking how many units of a certain product are in shopping carts, in what geography, and the activity of shopping carts over time. Real-time data analysis will open new business opportunities by enabling timely decisions on inventory management, discounts and opportunities for larger shopping carts, offers to pick up an item in a nearby store, and more.

Redis query engine supports [several types of indexes](https://redis.io/docs/latest/develop/interact/search-and-query/) that enable real-time search over session data.

- The NUMERIC index can sort the latest active users over a timespan or just return the latest active sessions
- The TAG index tracks the visited items or pages across all the active sessions using exact match and faceted search
- The TAG index can also provide an aggregate view of how many shopping carts contain an item. Or even spot premium shopping carts with the most valuable items in it. And find all the open sessions for the same user from different devices
- GEO or GEOSHAPE index to enable geographic research per area
- Finally, if you are feeling creative about the data you’d like to store in the session, you can leverage full-text and vector search with the TEXT and VECTOR indexes

In addition, filtering on multiple indexes simultaneously enables different views of the active sessions by selecting the desired facets.

Thinking beyond retail, session management is crucial for many industries, including banking, gaming, travel and hospitality, and more. Whatever the session data is, Redis 8 offers flexible data modeling and search capabilities.

## Search all your (cached) data with a single API

Not everything is session management when it comes to speeding up your application. Caching is one of the most popular use cases where Redis offers a range of structures to help model data for real-time retrieval. The most popular ecosystems and development frameworks abstract cache management by offering simple APIs, often storing the cached data in strings.

While caches are typically designed for direct or primary key access, the ability to perform real-time search and processing on cached data from a single repository or, as in the following example, in the case of federated data, is crucial.

The data structure desired to model the cache influences how optimal data is retrieved and transferred over the network. Similar to what was described for session management, choosing the hash or JSON data structures over the string enables a more efficient data modeling approach, supporting faster operations over the cached data.

Once more, the Redis query engine enables real-time search and analytics that can enrich the user experience or help build aggregated views of the dataset, especially when the entire dataset from the data source is cached in its entirety (with [Redis Data Integration](https://redis.io/data-integration/), [RIOT](https://redis.io/docs/latest/integrate/riot/), or other synchronization technologies). The Redis query engine provides fast results, otherwise prohibitive for relational or generally slower systems of records.

You can use Redis 8 with all of our announcements from our [latest Summer Release](https://redis.io/release/), including Redis Flex that lets you cache 5X more data for the same price.

## Semantic caching finds relevant data faster

Everybody knows the power of caching. But while caching is the perfect answer to application demand for speed, traditional caching methods are best designed for structured data. So, what happens if data is semi-structured or unstructured? The ability to store data as a vector and the capabilities to index and search have evolved traditional caching into [semantic caching](/blog/what-is-semantic-caching/). Thanks to the Redis query engine delivered in Redis 8.0, modeling unstructured data as vectors offers a unique capability to enhance the traditional deterministic search methods with vector search, the foundation of semantic caching.

In particular, semantic caching is core to the next generation of GenAI-assisted chatbots. The semantic cache stores the results of previously-answered questions, allowing for quicker retrieval of similar future queries. By leveraging Redis’s built-in caching capabilities and vector search, responses are efficiently stored and reused, reducing the number of requests and tokens sent to LLM services, thus reducing the costs generated by LLM services and improving the application throughput to generate responses.

## One Redis for every use case

We are excited to help you build the next generation of applications. Redis 8 provides new capabilities to manage your data and modernize your apps. And there’s more to come with the next Redis 8 milestones to follow.
Try it out yourself and download [Redis 8 Docker Image from Docker Hub](https://hub.docker.com/_/redis/tags) and [Redis Insight](https://redis.io/insight/) or our [official client libraries](https://redis.io/docs/latest/develop/connect/clients/) from [redis.io](https://redis.io).
