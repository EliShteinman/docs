---
title: "Expanding the Database Trigger Features in Redis"
linkTitle: "Expanding the Database Trigger Features in Redis"
url: "/blog/database-trigger-features/"
description: "Among the features of RedisGears 2.0 is the V8 JavaScript Engine. You can experiment with it in the RedisGears 2.0. Here’s what to expect."
date: 2022-11-09
blogCategories:
- "Tech"
authors:
- "Thomas Caudron"
lastmod: 2025-03-27
hidden: true
mirrored: true
---

*By Thomas Caudron, Contributor · Published 9 November 2022 · updated 27 March 2025*

![Blog tile image](/images/site-mirror/cba9ee764ac0a560e5fb01f99c8014dd6b580d1a-772x550.webp)

**Among the features of RedisGears 2.0 is the V8 JavaScript Engine. You can experiment with it in the RedisGears 2.0. Here’s what to expect.**

Redis is famous for its ease of use, its low latency – and the company’s dedication to improving product features and code quality. For example, we added [scripting](https://redis.io/docs/manual/programmability/eval-intro/) and [functions](https://redis.io/docs/manual/programmability/functions-intro/) so programmers could execute business logic within a database, with triggers called by an external service or user. Now it’s time to add more.

With *triggered functions* in [RedisGears](/modules/redis-gears/), you can register business logic that reacts to Redis keyspace notifications. Triggered functions are similar to stored procedures that run when specific actions occur, such as when changes are made to data. An event, such as adding a key-value, fires the trigger’s execution. The difference between a triggered function and a user-defined function is that a trigger is automatically invoked when a triggering event occurs.

RedisGears brings the trigger and execution of your business logic into your database, so it does not have to be duplicated across multiple services and applications. The functions are executed synchronously and without latency.

For example, when an order is placed in an e-commerce application, RedisGears can react to the changed data and update the number of available items in inventory. Or when a database receives data from multiple applications, a developer can embed the transformation logic in RedisGears to normalize the data. That ensures all those feeder applications apply the exact same logic. Consistency is a good thing, especially for code maintenance.

## A new feature – and you can experiment with it!

With the [second milestone release](https://github.com/RedisGears/RedisGears/releases/tag/v2.0.0-m02) of RedisGears 2.0, we are introducing support for the V8 JavaScript engine. [V8](https://v8.dev/docs) is Google’s open source high-performance JavaScript and WebAssembly engine, written in C++. This JavaScript Engine, once generally available (GA), will be available in Redis Cloud and will become part of Redis Stack. It will make triggered functions available by default for Redis Cloud instances.

V8 enables you to use Redis to run code where your data is without network overhead using JavaScript. In the coming weeks, we will publish several blog posts in which we introduce RedisGears’s new capabilities and concepts as we work towards RedisGears 2.0’s general availability.

### RedisGears 2.0 milestone release

The initial milestone release focuses on functions that are executed on database triggers so that your code can react when Redis fires an event. The most common events that are apt to trigger a function are [Redis keyspace notifications](https://redis.io/docs/manual/keyspace-notifications/#events-generated-by-different-commands). But its usefulness goes far beyond that; most advanced data structures in Redis Stack also publish their events.

Two special events are not always triggered by a command:

- Expiration: when a key expires from the database
- Eviction: when a key is evicted from the database

## Deploying functions: An easy start

To deploy a function, the developer provides a single JavaScript file. This is easy enough for small projects, but it gets harder to maintain as projects grow and become more complex. Happily, the JavaScript community has excellent deployment tools, as explained in a tutorial on [how to set up webpack](https://github.com/RedisGears/RedisGears/blob/master/docs/docs/Development.md) for RedisGears2.0.

Make sure you use JavaScript libraries that are compatible with the V8 engine. [Browser](https://developer.mozilla.org/en-US/docs/Glossary/Global_object) and [nodejs](https://nodejs.org/api/globals.html)-specific global objects are not available in the V8 engine.

## Hello, world!

We start with the prototypical Hello World example. We use a simple script with the [shebang (#!)](https://en.wikipedia.org/wiki/Shebang_(Unix)) that defines the library name and a function where we define the logic.

```javascript
#!js name=lib

redis.register_function('hello_world', function(){
    return 'hello_world';
});

```

Now, load that data into Redis:

```bash
> redis-cli -x RG.FUNCTION LOAD < ./example.js

```

And execute it with the library and method name:

```bash
> redis-cli RG.FCALL lib hello_world

```

## Change events

We need to register a notification consumer with Redis before the software can react with a function on a database event.

The consumer expects three arguments:

- A consumer name: a logical description
- The prefix for the keys we track
- The callback for the function to execute

The callback function can include two arguments:

- Client: the Redis client to communicate with the Redis server
- Data: information about the event that was fired; the event_name, key, and key_raw

The key_raw provides an ArrayBuffer for the key that triggered the event, when the key_raw can be decoded to a string the key is filled in. The event type is returned in event_name.

The full signature looks like this:

```javascript
redis.register_notifications_consumer(‘consumer_example_name’, ‘keyprefix’, function(client, data){
	// function logic
});

```

To run a function on all changes, we include an empty string in the keyprefix.

```javascript
redis.register_notifications_consumer(‘consumer_add_version’, ‘’, function(client, data) {
	if(client.call(‘type’, data.key) != ‘hash’) {
		return;
}

client.call(‘hincrby’, data.key, ‘__version__’, 1);
});

```

In this example, we make sure that the event was fired for a hash data type. If not, we stop the function. If it is a hash data type, we use the hincrby command to create or increment the value of the version property on the hash.

This shows that we can retrieve information from the key and command that was executed to trigger the function and execute Redis commands within RedisGears functions.

## Start testing

[Redis v7.0.3 or above](https://redis.io/) is required to start using RedisGears2.0. A [Docker image](https://hub.docker.com/r/redislabs/redisgears) is available, so you can begin using it immediately.

```javascript
docker pull redislabs/redisgears:edge
docker run -p 6379:6379 redislabs/redisgears:edge

```

If you encounter an issue or potential improvements in the milestone release, please get in touch via the [RedisGears GitHub repository](https://github.com/RedisGears/RedisGears/issues). We want to hear about your experiences!

Experience Redis Enterprise Cloud for free.
