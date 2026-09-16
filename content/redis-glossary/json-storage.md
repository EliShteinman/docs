---
title: "JSON Storage"
linkTitle: "JSON Storage"
url: "/glossary/json-storage/"
description: "JSON storage refers to storing data in a format called JSON (JavaScript Object Notation), which is a lightweight and widely used data interchange format. JSON is a text-based format that is easy..."
lastmod: 2026-05-21
mirrored: true
---

*updated 21 May 2026*

## JSON Storage Defined

JSON storage refers to storing data in a format called JSON (JavaScript Object Notation), which is a lightweight and widely used data interchange format. JSON is a text-based format that is easy for humans to read and write, and it is also easy for computers to parse and generate.

JSON storage is popular in web development because many web applications are built using JavaScript, which can easily manipulate JSON data. JSON can be used to store and transmit data between servers and clients, and it can also be used as a format for storing data in databases.

JSON storage is often used in combination with NoSQL databases, which are non-relational databases that are designed to handle large volumes of unstructured or semi-structured data. [NoSQL databases](https://redis.io/nosql/what-is-nosql/) are a good match for JSON data because they are schemaless and can handle flexible and dynamic data structures.

## JSON Storage Best Practices

A few options exist for storing JSON in Redis. The most basic form is to take a pre-serialized and simply store it at a specific key:

This, while seemingly simple, has some very real drawbacks:

- The serialization takes client computational resources during read and write.
- The JSON format adds size to the data
- Redis has only indirect ways to manipulate the actual JSON data.

The first couple of points may be negligible on small amounts of data, but can definitely add up. Especially with multi-megabyte JSON stores. The third point is more critical, however.

Prior to Redis 4.0, the only method to work with JSON data inside of Redis was to use a [Lua script through the cjson module](https://github.com/RedisJSON/RedisJSON/blob/master/benchmarks/lua/json-get-path.lua). This partially solved the JSON problem although it still was a bottleneck and added the extra burden of learning Lua.

Worse yet, many applications would just GET the entire JSON string, deserialize it, manipulate it, re-serialize and SET it again at the application.** This is an anti-pattern.** There is a very real risk of losing data with this method. Take for example:

The results from line 5 would only show the update from instance #2 and setting the colour in instance #1 would be lost.

Redis 4.0+ have the ability to use modules. [RedisJSON](https://docs.redis.com/latest/modules/redisjson/redisjson-quickstart/) is a module that provides a special datatype and direct manipulation commands. RedisJSON stores the data in a binary format which removes the storage overhead from JSON, provides quicker access to elements without de-/re-serialization times.

To use RedisJSON you need to install it in your Redis server or enable it in your Redis Enterprise database.

Taking our previous example, using RedisJSON instead of storing JSON as a string would look like this:

RedisJSON provides a generally safer, faster, and more intuitive way of manipulating JSON in your datastore, especially where sub-element atomic manipulation is needed.
