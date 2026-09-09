---
title: "Introducing Redis OM .NET"
linkTitle: "Introducing Redis OM .NET"
url: "/blog/introducing-redis-om-net/"
description: "Redis is an awesome technology loved by millions of developers for two reasons: speed and simplicity. Redis provides an intuitive native interface logically organized into data structures that..."
date: 2021-12-08
blogCategories:
- "How To and Tutorials"
- "New Product Announcements"
- "Tech"
authors:
- "Steve Lorello"
lastmod: 2026-09-01
hidden: true
---

*By Steve Lorello, Developer Advocate · Published 8 December 2021 · updated 1 September 2026*

![Blog tile image](/images/blog/3317475c449f3066691f0e8f9e1b2b562c195f99-772x550.webp)

## A fluent API and object model for .NET and Redis

Redis is an awesome technology loved by millions of developers for two reasons: speed and simplicity. Redis provides an intuitive native interface logically organized into data structures that programmers already know. Moreover, those structures are simple to use and terrifically optimized. It’s this ultimate blend of speed and simplicity that we are angling at with the release of a new client library for .NET, Redis OM.

## What is Redis OM .NET?

Redis OM is object mapping and more for Redis. The motivation behind Redis OM is to answer the question “How can developers get amazing leverage out of Redis without learning all the [Redis commands](https://redis.io/docs/latest/commands/)?” For this first preview release, we’re looking to address the question, “How can we store and find our domain objects in Redis?” The preview release of Redis OM .NET is an object mapper, a secondary index builder, and a simplified and powerful query builder. All of this is geared towards helping you store and find your domain objects with Redis.

## Redis modules

The [Module API](https://redis.io/docs/latest/develop/reference/modules/) has been a game changer for Redis. The modules add a tremendous amount of flexibility to the platform while providing some essential features for Redis. [RedisJSON](https://redisjson.io/), in particular, unlocks an enormous amount of functionality, particularly around secondary indexing and document modeling. While Redis OM works well with core Redis, Redis OM really hits its stride when you add RedisJSON, taking full advantage of RedisJSON to create a rich and powerful API for modeling objects and querying them in Redis.

## Capabilities

The preview version of Redis OM .NET has four primary capabilities:

1. Object modeling
1. Index creation
1. Fluent queries
1. Fluent aggregations

## How it works

Before getting up and running with Redis OM, you need to install the package in your project. To do so, just run dotnet add package Redis.OM. The primary connection logic within the Redis OM library exists in the RedisConnectionProvider. This provider gives access to three different objects you can use to communicate with Redis:

1. The IRedisConnection lets you interface directly with Redis using the Execute and ExecuteAsync methods.
1. The RedisCollection<T> is a generically typed collection of objects. This interface provides the fluent query API.
1. The RedisAggregationSet<T> allows you to build and execute aggregation pipelines in Redis using a Fluent API.

## Connecting to Redis

To connect Redis OM to Redis in ASP.NET Core, you should inject an instance of the RedisConnectionProvider instance as a singleton. To do this, you’ll use a Redis URI. If you’re using .NET 6, this means opening your program.cs file and adding:

```python
builder.Services.AddSingleton(new RedisConnectionProvider("redis://localhost:6379"));

```

For .NET 5, which uses the Startup.cs file, you can add the following to Startup.ConfigureServices:

```python
services.AddSingleton(new RedisConnectionProvider("redis://localhost:6379"));

```

## Modeling and searching for objects

RedisJSON lets you store JSON objects in Redis natively and query those objects. But to query your JSON, you need to first define your indexes. To make this process easier, we’ve introduced a declarative model in Redis OM .NET to allow you to define these indexes through a declarative interface. If you want to declare a class to store in Redis and index its properties, you decorate the class with a Document attribute and then dress the individual properties with the Indexed or the Searchable attributes. Indexed implies a standard index, whereas Searchable applies only to strings and means that the property will be queryable with full-text search. Next, you can create the index in Redis by passing your newly decorated type into the IRedisConnection.CreateIndex method. So, for example, if you wanted to declare a Customer class with an index, you would do something like the following:

```python
// declare index
[Document(StorageType = StorageType.Json)]
public class Customer
{
   [Indexed]
   public string FirstName { get; set; }
   [Searchable(Aggregatable=true)]
   public string LastName { get; set; }
   [Searchable(Aggregatable=true)]
   public string PersonalStatement { get; set; }
   [Indexed(Aggregatable=true)]
   public int Age { get; set; }
}

// create index
connection.CreateIndex(typeof(Customer));

```

## Querying

With an index created, you can now use RedisCollection<T> to query objects in Redis. So, if you had John stored in Redis as a Customer object, you can then query him:

```python
var customers = provider.RedisCollection<Customer>();
var john = customers.First(x => x.FirstName == "John");

```

You can also easily do range queries. For example, let’s find all the Customers who have not reached retirement age:

```python
var customersNotOldEnoughToRetire = customers.Where(x => x.Age < 65);

```

With the RedisCollection and RedisJSON, you can build rich and complex queries as you ordinarily would in LINQ, and Redis OM will manage the translation to Redis’ query language for you.

## Aggregations

In addition to querying, you can use [Redis Aggregations](https://redis.io/docs/stack/search/reference/aggregations/) to build aggregation pipelines that can do all sorts of things. For example, suppose you want to find the age of each customer in 3 years, you can do so with a straightforward arithmetic operation inside an Apply expression, which will translate to a properly formatted aggregation pipeline in Redis:

```python
var customerAggregations = provider.AggregationSet<Customer>();

```

```python
customerAggregations.Apply(x =>x.RecordShell.Age + 3,
    "AgeInThreeYears");

```

You can also group records together and calculate summary statistics on them. So if you want to group customers by their last name, you can then calculate summary statistics. For example, here’s how you can calculate average age:

```python
var averageAgeOfFamilies = customerAggregations.GroupBy(x=>    x.RecordShell.LastName).Average(x=>x.RecordShell.Age);

```

## Wrapping up

This is just a brief overview of the capabilities of Redis OM for .NET. If you want to learn more, you can check out the [tutorial](https://redis.github.io/redis-om-dotnet/articles/intro.html) and look through the [API docs](https://redis.github.io/redis-om-dotnet/). We plan on adding more features to Redis.OM soon, and, to that end, we would love some community feedback. Come and try it out. If you find a problem or think of something you’d like to see added to the library, open an [issue](https://github.com/redis-developer/redis-om-dotnet/issues/new) in GitHub. And naturally, we always love contributions from the community, so PRs are always welcome :).
