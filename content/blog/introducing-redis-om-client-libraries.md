---
title: "Introducing the Redis OM Client Libraries"
linkTitle: "Introducing the Redis OM Client Libraries"
url: "/blog/introducing-redis-om-client-libraries/"
description: "Today, we’re pleased to announce a preview release of four new high-level client libraries for Redis. We’re calling these libraries Redis OM: Object Mapping, and more, for Redis. Our goal is to..."
date: 2021-11-23
blogCategories:
- "New Product Announcements"
- "Tech"
authors:
- "Kyle Banker"
lastmod: 2025-03-27
hidden: true
---

*By Kyle Banker, Sr. Director, Field Engineering · Published 23 November 2021 · updated 27 March 2025*

![Blog tile image](/images/blog/810bef849496afee9b50c636cdd983676789ff0f-928x628.webp)

## Intuitive Object Mapping and Fluent Queries for Redis

Today, we’re pleased to announce a preview release of four new high-level client libraries for Redis. We’re calling these libraries Redis OM: Object Mapping, and more, for Redis. Our goal is to make it as easy as possible to use Redis and the Redis modules from your applications.

We’re launching with support for .NET, Node.js, Python, and Java (Spring). If you’re a software developer keen to see why we’re so excited about this launch, you can try one of our new libraries right now:

[Redis OM for .NET](https://github.com/redis/redis-om-dotnet)
[Redis OM for Node.js](https://github.com/redis/redis-om-node)
[Redis OM for Python](https://github.com/redis/redis-om-python)
[Redis OM for Spring](https://github.com/redis/redis-om-spring)

Each Redis OM library includes a comprehensive README and tutorial to help you get started quickly.

Just want a high-level overview for now? Read on!

## Why Redis OM?

As programmers and CS geeks, we love the elegance of a good data structure. And, as we all know, Redis provides rock-solid, distributed data structures in spades. There’s a kind of [Unix philosophy](https://en.wikipedia.org/wiki/Unix_philosophy) that runs through Redis: you can compose a well-built collection of primitives to solve any problem at hand. This composability has allowed Redis users to create a wide variety of tools, including caches, distributed locks, [message queues](/solutions/messaging/), rate limiters, pub/sub systems, background task executors, de-duplicators, and permissions systems, to name several.

The challenge is that not everyone has the time to reinvent these tools on their own. Not everyone has the bandwidth to build their own rate limiter or to figure out how to map a Redis hash to Java class (and vice versa!). We’ve built (and continue to build) Redis OM so that you can get the performance of Redis even if you don’t have time to compose your own abstractions using the core data structures that Redis provides.

Redis OM (pronounced “ōm”) is [object mapping](/blog/object-relational-mapping-misconceptions/) (and more) for Redis. Our aim is to furnish you with a toolbox of high-level abstractions that make it easy to work with Redis data in the programming environments you call home. The first abstraction we’re providing is object mapping. If you’re modeling any domain, you’re likely representing that domain in an object-oriented fashion. The Redis OM libraries let you transparently persist your domain objects in Redis and query them using a fluent, language-centric API.

## What can I do with Redis OM?

For this first preview release, we focused on object mapping and fluent queries. Since Python is a sort of *lingua franca* for us programmers, let’s explore a few examples from Redis OM for Python to get a sense of what’s possible here.

### Object Mapping

First, we can define a simple domain object. In this case, the object represents a customer:

```python
class Customer(HashModel):
    first_name: str
    last_name: str
    email: EmailStr
    join_date: datetime.date
    age: int
    bio: Optional[str]

```

Now we create a new Customer instance like this:

```python
andrew = Customer(
    first_name="Andrew",
    last_name="Brookins",
    email="andrew.brookins@example.com",
    join_date=datetime.date.today(),
    age=38,
    bio="Python developer, works at Redis, Inc."
)

```

And then we can write this new customer instance to Redis by calling save() on it:

```python
andrew.save()

```

The Redis OM libraries automatically generate a unique ID for any new object. For this, we’re using [ULID](https://github.com/ulid/spec)s (Universally Unique Lexicographically Sortable Identifiers). You can think of a ULID as a kind of user-friendly UUID. ULIDs are sortable, globally unique, URL-safe, and fairly human-readable when base32-encoded.

Want an example? A typical ULID looks like this: 01ARZ3NDEKTSV4RRFFQ69G5FAV

Anyway, once you’ve saved one of these objects to Redis, you can retrieve it by providing its unique ID. In Python, you can access that unique ID with the pk property (pk, of course, refers to “primary key”).

Pass the unique ID to Customer.get(), and you’ll get your object back:

```python
Customer.get(andrew.pk)

```

With the Redis OM libraries, you can serialize your domain objects in two ways. We’re serializing this Customer object as a Redis hash, as it’s a simple object with a flat structure. But if you have objects with a large number of fields or nested objects, you’ll probably want to serialize them as JSON instead (and for this you’ll need the source-available [RedisJSON](https://oss.redis.com/redisjson/) module).

### Querying

If you’re mapping domain objects to Redis, you probably want to be able to query them. [RedisJSON](/blog/redisjson-public-preview-performance-benchmarking/) (and, by proxy, [RediSearch](/search/)) provides indexing and querying for Redis. The Redis OM libraries take advantage of these features to give you a fluent query API over your domain objects.

Let’s take a quick example. With the Redis OM Python library, you can construct fluent expressions to query your data. For example, here’s a query that retrieves all customers whose last name is either “Javayant” or “Jagoda”:

```python
Customer.find((Customer.last_name == "Javayant") | (Customer.last_name == "Jagoda")).all()


```

The beauty of these queries is that they’re always indexed, so they’re efficient by default. See our [recent benchmarking blog](/blog/redisjson-public-preview-performance-benchmarking/) to get an idea of the performance benefits you’re likely to see.

## A Family of Libraries

The Redis OM libraries are a bit like a family; they’re united in their purpose of making it as easy as possible to use Redis and the Redis modules. At the same time, each library has its own language-specific emphases, all designed to delight the .NET, Node.js, Python, and Java/Spring software engineers we wrote them for. Some examples?

[Redis OM for Node.js](https://github.com/redis/redis-om-node) is written in TypeScript, providing first-class support for TypeScript and JavaScript.

[Redis OM for .NET](https://github.com/redis/redis-om-dotnet) lets you query your Redis domain objects using [LINQ](https://github.com/redis/redis-om-spring).

[Redis OM Spring](https://github.com/redis/redis-om-spring) integrates natively with Spring, extends [Spring Data Redis](https://spring.io/projects/spring-data-redis) (to provide a familiar interface), and even adds some support for [RedisBloom](https://oss.redis.com/redisbloom/) (which gives you probabilistic data structures).

[Redis OM Python](https://github.com/redis/redis-om-python) [integrates natively with the popular FastAPI framework](https://github.com/redis/redis-om-python/blob/main/docs/fastapi_integration.md). Combining [FastAPI](https://fastapi.tiangolo.com/) with Redis is a great way to build high-performance web services. Redis OM Python also supports both sync and async usage.

## What’s Next for Redis OM?

We’re thrilled to announce this preview release for the Redis OM libraries, and we can’t wait to get your feedback. Pull requests and Github issues are great, but we’d also love to chat directly. Find us on the [Redis Discord server](https://discord.gg/redis). Come say hi, and let us know what you need next! As we continue to develop and improve the Redis OM libraries in earnest, we welcome your ideas, questions, and contributions.
