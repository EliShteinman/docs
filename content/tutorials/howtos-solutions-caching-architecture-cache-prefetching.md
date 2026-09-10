---
title: "How to use Redis for Cache Prefetching Strategy"
linkTitle: "How to use Redis for Cache Prefetching Strategy"
url: "/tutorials/howtos/solutions/caching-architecture/cache-prefetching/"
description: "Cache prefetching is a proactive caching strategy where you load data into Redis before it's requested, eliminating cache misses for frequently accessed data like master data lookups. Use cache..."
group: "For developers"
aliases:
- "/tutorials/howtos-solutions-caching-architecture-cache-prefetching/"
date: 2026-02-26
lastmod: 2026-02-26
hidden: true
mirrored: true
---

*Published 26 February 2026*

> **GITHUB CODE**
>
> Below are the commands to clone the source code (frontend and backend) for the application used in this tutorial
>
> git clone [https://github.com/redis-developer/ebook-speed-mern-frontend.git](https://github.com/redis-developer/ebook-speed-mern-frontend.git)
>
> git clone [https://github.com/redis-developer/ebook-speed-mern-backend.git](https://github.com/redis-developer/ebook-speed-mern-backend.git)

Cache prefetching is a proactive caching strategy where you load data into Redis **before** it's requested, eliminating cache misses for frequently accessed data like master data lookups. Use cache prefetching when your data changes infrequently, is accessed across many application flows, and needs sub-millisecond response times.

**What you'll learn:**

- What cache prefetching is and how it differs from other caching strategies
- How to compare cache prefetching vs cache-aside vs write-through patterns
- How to prefetch master data from MongoDB into Redis using Redis OM for Node.js
- How to query prefetched data from Redis for fast lookups
- When to use cache prefetching to reduce cache misses and improve response times

## What is cache prefetching?

Cache prefetching is a technique used in database management systems (DBMS) to improve query performance by anticipating and fetching data from the storage subsystem before it is explicitly requested by a query. Unlike reactive strategies such as [cache-aside](/tutorials/howtos/solutions/microservices/caching/#what-is-the-cache-aside-pattern), where data is loaded into cache only after a cache miss, cache prefetching proactively warms the cache so data is ready before it's needed.

There are three main strategies for cache prefetching:

1.  **Sequential prefetching:** This approach anticipates that data will be accessed in a sequential manner, such as when scanning a table or index. It prefetches the next set of data blocks or pages in the sequence to ensure they are available in cache when needed.
2.  **Prefetching based on query patterns:** Some database systems can analyze past query patterns to predict which data is likely to be accessed in the future. By analyzing these patterns, the DBMS can prefetch relevant data and have it available in cache when a similar query is executed.
3.  **Prefetching based on data access patterns:** In some cases, data access patterns can be derived from the application logic or schema design. By understanding these patterns, the database system can prefetch data that is likely to be accessed soon.

This tutorial will cover the third strategy, **prefetching based on data access patterns**.

Imagine you're building a movie streaming platform. You need to be able to provide your users with a dashboard that allows them to quickly find the movies they want to watch. You have an extensive database filled with movies, and you have them categorized by things like country of origin, genre, language, etc. This data changes infrequently, and is regularly referenced all over your app and by other data. This kind of data that is long-lived and changes infrequently is called "master data."

One ongoing dev challenge is to swiftly create, read, update, and delete master data. You might store your master data in a system of record like a SQL database or document database, and then use Redis as a cache to speed up lookups for that data. Then, when an application requests master data, instead of coming from the system of record, the master data is served from Redis. This is called the "master data-lookup" pattern.

From a developer's point of view, "master data lookup" refers to the process by which master data is accessed in business transactions, in application setup, and any other way that software retrieves the information. Examples of master data lookup include fetching data for user interface (UI) elements (such as drop-down dialogs, select values, multi-language labels), fetching constants, user access control, theme, and other product configuration.

Below you will find a diagram of the data flow for prefetching master data using Redis with MongoDB as the system of record.

![Data flow diagram showing cache prefetching architecture: master data is read from MongoDB on startup, stored in Redis, and then served directly from Redis when the application requests it](/images/site-mirror/266dbbb20bb614b8348e9a86f08a109c79ec6ae0-1163x285.webp)

The steps involved in fetching data are as follows:

1.  Read the master data from MongoDB on application startup and store a copy of the data in Redis. This pre-caches the data for fast retrieval. Use a script or a cron job to regularly copy latest master data to Redis.
2.  The application requests master data.
3.  Instead of MongoDB serving the data, the master data will be served from Redis.

## How does cache prefetching compare to other caching strategies?

When choosing a caching strategy, it's important to understand how cache prefetching differs from cache-aside and write-through patterns:

| Feature                    | Cache prefetching                          | [Cache-aside](/tutorials/howtos/solutions/microservices/caching/#what-is-the-cache-aside-pattern) | Write-through                    |
| -------------------------- | ------------------------------------------ | ------------------------------------------------------------------------------------------------- | -------------------------------- |
| **When data enters cache** | Proactively, before it's requested         | Reactively, after a cache miss                                                                    | On every write operation         |
| **Cache misses**           | Minimal (data is pre-loaded)               | Common on first access or after eviction                                                          | None for written data            |
| **Data freshness**         | Depends on refresh schedule                | Always fetches latest on miss                                                                     | Always current                   |
| **Write overhead**         | Low (bulk load at intervals)               | None (read-only caching)                                                                          | High (every write goes to cache) |
| **Best for**               | Stable, frequently read data (master data) | Unpredictable read patterns                                                                       | Data that must stay in sync      |
| **Complexity**             | Moderate (scheduling, bulk loads)          | Low                                                                                               | Moderate (dual-write logic)      |

Cache prefetching works best when your data is relatively stable and accessed frequently across multiple application flows. For data with unpredictable access patterns, consider [cache-aside](/tutorials/howtos/solutions/microservices/caching/#what-is-the-cache-aside-pattern). For data that needs to stay current on every write, consider write-through or write-behind caching. You can also combine strategies; for example, use cache prefetching for master data while using [query caching](/tutorials/howtos/solutions/microservices/caching) for dynamic search results.

## Why should you use Redis for cache prefetching?

1.  **Serve prefetched data fast**: By definition, nearly every app requires access to master or other common data. Pre-caching such frequent data with Redis delivers it to users fast.
2.  **Support massive tables**: Master tables often have millions of records. Searching through them can cause performance bottlenecks. Use Redis to perform real-time search on the large tables to increase performance with sub-millisecond response.
3.  **Postpone expensive hardware and software investments**: Defer costly infrastructure enhancements by using Redis. Get the performance and scaling benefits without asking the CFO to write a check.

> **Tip**
>
> If you use **Redis Cloud**, cache prefetching is easier due to its support for JSON and search. You also get additional features such as fast performance, high scalability, resiliency, and fault tolerance. You can also call upon high-availability features such as Active-Active geo-redundancy.

## How do you implement cache prefetching in a Node.js app with Redis and MongoDB?

### Demo application

The demo application used in the rest of this tutorial showcases a movie application with basic create, read, update, and delete (CRUD) operations.

![Movie application dashboard showing a search bar at the top, a toggle between text and form-based search, and a grid of movie cards with edit and delete icons](/images/site-mirror/4d994e5ad41179b49f9bda73ba7d81a36e7f5ce5-2000x1031.webp)

The movie application dashboard contains a search section at the top and a list of movie cards in the middle. The floating plus icon displays a pop-up when the user selects it, permitting the user to enter new movie details. The search section has a text search bar and a toggle link between text search and basic (that is, form-based) search. Each movie card has edit and delete icons, which are displayed when a mouse hovers over the card.

> **GITHUB CODE**
>
> Below are the commands to clone the source code (frontend and backend) for the application used in this tutorial
>
> git clone [https://github.com/redis-developer/ebook-speed-mern-frontend.git](https://github.com/redis-developer/ebook-speed-mern-frontend.git)
>
> git clone [https://github.com/redis-developer/ebook-speed-mern-backend.git](https://github.com/redis-developer/ebook-speed-mern-backend.git)

Certain fields used in the demo application serve as master data, including movie language, country, genre, and ratings. They are master data because they are required for almost every application transaction. For example, the pop-up dialog (seen below) that appears when a user who wants to add a new movie clicks the movie application plus the icon. The pop-up includes drop-down menus for both country and language. In this case, Redis stores and provides the values.

![Pop-up dialog for adding a new movie with form fields for title, description, and drop-down menus for country and language populated from Redis cache](/images/site-mirror/6dc9d71fc91de3d04550362db7a21c470a4a5ce8-1304x557.webp)

### How do you prefetch data from MongoDB into Redis?

The code snippet below is used to prefetch MongoDB JSON documents and store them in Redis (as JSON) using the [Redis OM for Node.js](https://github.com/Redis/Redis-om-node) library.

```js
async function insertMasterCategoriesToRedis() {
  ...
  const _dataArr = await getMasterCategories(); //from MongoDb
  const repository = MasterCategoryRepo.getRepository();

  if (repository && _dataArr && _dataArr.length) {
    for (const record of _dataArr) {
      const entity = repository.createEntity(record);
      entity.categoryTag = [entity.category]; //for tag search
      //adds JSON to Redis
      await repository.save(entity);
    }
  }
  ...
}

async function getMasterCategories() {
  //fetching data from MongoDb
  ...
  db.collection("masterCategories").find({
    statusCode: {
      $gt: 0,
    },
    category: {
      $in: ["COUNTRY", "LANGUAGE"],
    },
  });
  ...
}
```

You can also check [Redis Insight](https://redis.io/insight/) to verify that JSON data is inserted, as seen below:

![Redis Insight interface showing a list of master data category keys stored as JSON documents in Redis](/images/site-mirror/66684305bb0f29c1ddf63696cf59ab40aea7234a-1012x594.webp)

![Expanded view of a single master data JSON document in Redis Insight, showing fields like category, statusCode, and categoryTag](/images/site-mirror/f2badce4880f59a116fa1b938510d77a4de8b752-1008x568.webp)

> **Tip**
>
> Redis Insight is the free redis GUI for viewing data in redis. [Click here to download.](https://redis.io/insight/)

### How do you query prefetched data from Redis?

Prior to prefetching with Redis, the application searched the static database (MongoDB) to retrieve the movie's country and language values. As more people started using the application, the database became overloaded with queries. The application was slow and unresponsive. To solve this problem, the application was modified to use Redis to store the master data. The code snippet below shows how the application queries Redis for the master data, specifically the country and language values for the dropdown menus:

```js
// With Redis
// Redis OM Node query
function getMasterCategories() {
  ...
  masterCategoriesRepository
    .search()
    .where("statusCode")
    .gt(0)
    .and("categoryTag")
    .containOneOf("COUNTRY", "LANGUAGE");
  ...
}
```

## Next steps

In this tutorial you learned how to use Redis for cache prefetching with a "master data lookup" example. Cache prefetching is a proactive caching strategy that reduces cache misses and delivers fast response times for stable, frequently accessed data.

To continue building your caching knowledge with Redis:

- Learn about [query caching in a microservices app](/tutorials/howtos/solutions/microservices/caching) to cache dynamic search results alongside prefetched master data
- Explore [cache-aside](/tutorials/howtos/solutions/microservices/caching/#what-is-the-cache-aside-pattern) for reactive caching on read

## Additional resources

- [Redis YouTube channel](https://www.youtube.com/c/Redisinc)
- Clients like [node-redis](https://github.com/redis/node-redis) and [Redis OM for Node](https://github.com/redis/redis-om-node) help you to use Redis in Node.js apps.
- [Redis Insight](https://redis.io/insight/): To view your Redis data or to play with raw Redis commands in the workbench
- [Try Redis Cloud for free](https://redis.io/try-free/)
