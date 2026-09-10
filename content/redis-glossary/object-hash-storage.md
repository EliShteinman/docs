---
title: "Object->Hash Storage"
linkTitle: "Object->Hash Storage"
url: "/glossary/object-hash-storage/"
description: "The native Redis datatype hash(map) may, at first glance, seem very similar to a JSON object or other record data type. It is actually quite a bit simpler, allowing only for each field to be either..."
lastmod: 2025-06-30
mirrored: true
---

*updated 30 June 2025*

The native Redis datatype hash(map) may, at first glance, seem very similar to a JSON object or other record data type. It is actually quite a bit simpler, allowing only for each field to be either a string or number and not allowing for sub-fields. However, by pre-computing the ‘path’ of each field, you can flatten an object and store it in a Redis Hashmap.

Take the this example:

Using [JSONPath](http://goessner.net/articles/JsonPath/) we can represent each item in one level with a hashmap.

*(Shown as individual commands for clarity, in a script you would want to variadicly use HSET)*

This provides a way to can get the entire object:

Or individual parts of the object:

While this can provide a quick, useful method to access store objects in Redis, it does have downsides:

- Different languages and libraries may have slightly different implementations of JSONPath causing incompatibilities. To this point, you should serialize and deserialize with the same library.
- Arrays support can be spotty
  - Sparse arrays can be problematic
  - It’s not possible to do many operations such as inserting an item in the middle of the array
- There is some unnecessary overhead in the JSONPath keys

This pattern has significant overlap with ReJSON. If ReJSON is available, it is very often a better choice. Storing objects this way does have one advantage over ReJSON of being integrated with another Redis command: [SORT](https://redis.io/commands/sort). However, the SORT command is both a complex topic (beyond the scope of this pattern) and computationally complex which can be wielded in ways that don’t scale well if not very carefully managed.
