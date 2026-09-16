---
title: "Redis Hashes"
linkTitle: "Redis Hashes"
url: "/glossary/redis-hashes/"
description: "Hashes are a type of data structure that stores a mapping of keys to values, similar to a miniature version of Redis itself. Unlike lists and sets, hashes can store values that can be incremented..."
lastmod: 2025-06-30
mirrored: true
---

*updated 30 June 2025*

Hashes are a type of data structure that stores a mapping of keys to values, similar to a miniature version of Redis itself. Unlike lists and sets, hashes can store values that can be incremented or decremented if they can be interpreted as numbers.

Hashes are mutable, meaning we can add, change, increment, or remove field-value pairs at any time, not just at the initial declaration. They store field values as strings, which means they are flat, and there are no nested arrays or objects. We do not need to predefine field names of Redis hashes, and as such, we can add and remove fields as needed.

While Redis hashes are schemeless, we can still think of them as lightweight objects or rows in a relational database table.

Related resource: [Probabilistic Data Structures: The Most Useful Thing in Redis (you probably aren’t using)](https://redis.io/events/probabilistic-data-structures-useful-thing-redis-probably-arent-using/)
Join Kyle Davis and Loris Cro for a webinar covering P11c data structure concepts, trade offs, and advantages. You’ll hear about hyperloglog, Bloom filters, and cuckoo filters, and how to wield them in Redis. You’ll also hear about common use cases that can leverage these data structures.

## Redis Hash basic commands

- HSET: Sets the value of one or more fields on a hash.
- HGET: Returns the value at a given field.
- HMGET: Returns the values at one or more given fields.
- HINCRBY: Increments the value of a particular hash field.

## Redis Hash Example Case

In a role-playing game, players live, die, and are reborn, and this cycle of life is reflected in health points, armor, abilities, and battles. We will store this information in a hash with every player getting their own hash instance. We will update this player hash with new information, create temporary fields, and use built-in functionality to increment numerical values and update strings.

## Creating Hashes

For the first example, we’ll create a hash starting off with the fields: name, race, level, health points, and gold. To create this hash, we’ll use the command

The first argument to the

command is the key name we’ll use to access the hash. In this case, it’s

Here, we’re using a common Redis key naming convention. We start with the word “player” to indicate what type of thing we’re storing. We then follow with a colon and the id of this player. The colon separates the various parts of the key name going from least specific on the left to most specific on the right. After specifying the key, we add as many field-value pairs as we want. When we run this command, Redis returns 5, indicating the number of fields saved to the hash. We’ve now created a Redis hash for our first player for the mages and minotaurs.

Now, let’s see how to update and delete fields within a Redis hash. Imagine the player Texius is having an epic battle with a wizard and received a thunderbolt spell to the head. In the game, he’ll have a status of “dazed” to reflect this game state in the Redis hash. We will add the field-value pair

to the player hash instance. Here again, we’ll use the

command to add a new field-value pair. So the command we’ll run is

What happens when our player no longer has the status of “dazed”? We’ll want to remove the status field from the hash instance. To delete a field-value pair from a Redis hash, we use the command

The command is

Now, the

hash instance no longer has a “dazed” status, and our Texius lives to quest another day.

## Getting Hashes

Getting data from a hash is just as easy as setting it. Suppose we need to retrieve our Texius’s level. For that, we’ll need to use the

command. The command is

## Performance

Redis hashes store field values as strings, which means that they are flat, and there are no nested arrays or objects. Redis hashes are schemeless, but you can still think of them as lightweight objects or as rows in a relational database table. Hashes provide efficient access to individual fields, making them ideal for storing and retrieving complex objects. Hashes can also be used to implement counters, as well as caching and session management. Redis hashes are fast and efficient, making them an excellent choice for many use cases.
