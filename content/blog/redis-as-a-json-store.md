---
title: "RedisJSON: A Redis JSON Store"
linkTitle: "RedisJSON: A Redis JSON Store"
url: "/blog/redis-as-a-json-store/"
description: "Redis modules are bundled and packaged as part of Redis Enterprise Software. Download the modules (including RedisJSON) to upgrade Redis Enterprise Software with the latest module version."
date: 2017-03-21
blogCategories:
- "Tech"
authors:
- "Itamar Haber"
lastmod: 2025-03-27
hidden: true
---

*By Itamar Haber, Technology Evangelist · Published 21 March 2017 · updated 27 March 2025*

![Blog tile image](/images/blog/8eb9a9de52722aee5008486cbd3147e2eed1d252-90x90.webp)

*Redis modules are bundled and packaged as part of Redis Enterprise Software. *[*Download the modules (including RedisJSON)*](https://app.redislabs.com/#/rlec-downloads)* to upgrade Redis Enterprise Software with the latest module version.*

![redis json image with Redis Stack](/images/blog/d56870aa72f223b3876239f89d83bb0a340b9693-870x180.webp)

*Ready to jump right into RedisJSON? Check out *[*Getting Started with RedisJSON*](https://redis.io/docs/data-types/json/)* on the Redis Developer site!*

——

[RedisJSON](/json/) is a Redis module that provides native JSON capabilities—simply run the [Docker Image](https://hub.docker.com/r/redislabs/rejson/) for Redis with RedisJSON, visit the [GitHub repository,](https://github.com/RedisJSON/RedisJSON) or read the [docs online](https://github.com/RedisJSON/RedisJSON).

Both JSON and Redis need no introduction; the former is the standard data interchange format *between* modern applications, whereas the latter is ubiquitous wherever performant data management is needed *by* them. That being the case, I was shocked when a couple of years ago I learned that the two don’t get along.

Redis isn’t a one-trick pony–it is, in fact, quite the opposite. Unlike general purpose one-size-fits-all databases, Redis (a.k.a the “Swiss Army Knife of Databases,” “Super Glue of Microservices.” and “Execution context of Functions-as-a-Service”) provides specialized tools for specific tasks. Developers use these tools, which are exposed as abstract data structures and their accompanying operations, to model optimal solutions for problems. And that is exactly the reason why using Redis for managing JSON data is unnatural. So how do we use the RedisJSON module?

Fact: despite its multitude of core data structures, Redis had none that fit the requirements of a JSON value. Sure, you can work around that by using other data types: Strings are great for storing raw serialized JSON, and you can represent flat JSON objects with Hashes. But these workaround patterns impose limitations that make them useful only in a handful of use cases, and even then the experience leaves an un-Redis-ish aftertaste. Their awkwardness clashes sharply with the simplicity and elegance of using Redis normally.

But all that changed during the last year after [Salvatore Sanfilippo’s @antirez](https://twitter.com/antirez) visit to Redis’ Tel Aviv office, and with [Redis modules](http://www.redismodules.com) becoming a reality. Suddenly the sky wasn’t the limit anymore. Now that modules let anyone do anything, it turned out that I could be that particular anyone. Picking up on C development after more than a two decades hiatus proved to be less of a nightmare than I had anticipated, and with [Dvir Volk’s @dvirsky](https://twitter.com/dvirsky) loving guidance we birthed RedisJSON.

While you may not be thrilled about its name (I know that I’m not—suggestions are welcome), RedisJSON itself should make any Redis user giddy with JSON joy. The module provides a new data type that is tailored for fast and efficient manipulation of JSON documents. Like any Redis data type, RedisJSON’s values are stored in keys that can be accessed with a specialized subset of commands. These commands, or the API that the module exposes, are designed to be intuitive to users coming to Redis from the JSON world and vice versa. Consider this example that shows how to set and get values:

```javascript
127.0.0.1:6379> JSON.SET scalar . '"Hello JSON!"'
OK
127.0.0.1:6379> JSON.SET object . '{"foo": "bar", "ans": 42}'
OK
127.0.0.1:6379> JSON.GET object
"{"foo":"bar","ans":42}"
127.0.0.1:6379> JSON.GET object .ans
"42"
127.0.0.1:6379> ^C
~$ 

```

Like any well-behaved module, RedisJSON’s commands come prefixed. Both JSON.SET and JSON.GET expect the key’s name as their first argument. In the first line we set the root (denoted by a period character: “.”) of the key named *scalar* to a string value. Next, a different key named *object* is set with a JSON object (which is first read whole) and then a single sub-element by path.

What happens under the hood is that whenever you call JSON.SET, the module takes the value through a streaming lexer that parses the input JSON and builds tree data structure from it:

![redis json commands](/images/blog/fdfb1191599bd30d68687153010ec15f7d473866-621x242.webp)

RedisJSON stores the data in binary format in the tree’s nodes, and supports a subset of [JSONPath](http://goessner.net/articles/JsonPath/) for easy referencing of subelements. It boasts an arsenal of atomic commands that are tailored for every JSON value type, including: JSON.STRAPPEND for appending strings; JSON.NUMMULTBY for multiplying numbers; and JSON.ARRTRIM for trimming arrays… and making pirates happy. All with RedisJSON.

Because RedisJSON is implemented as a Redis module, you can use it with any Redis client that: a) supports modules (ATM none) or b) allows sending raw commands (ATM most). For example, you can use a RedisJSON-enabled Redis server from your Python code with [redis-py](https://github.com/andymccurdy/redis-py) like so:

```javascript
import redis
import json

data = {
    'foo': 'bar',
    'ans': 42
}

r = redis.StrictRedis()
r.execute_command('JSON.SET', 'object', '.', json.dumps(data))
reply = json.loads(r.execute_command('JSON.GET', 'object'))

```

But that’s just half of it. RedisJSON isn’t only a pretty API, it’s also a powerhouse in terms of performance. Initial performance benchmarks already demonstrate that, for example:

![ReJSON json.lua msgpack lua rate graph ](/images/blog/ca5e0ef7e5eddd8eb8cf993aa8ef58433c32f313-600x371.webp)

![REJSON json.lua msgpack lua average latency graph](/images/blog/3c95bd8884df2c5ae977d0150a5fbe4be8c63bd9-600x371.webp)

The above graphs compare the rate (operations/sec) and average latency of read and write operations performed on a 3.4KB JSON payload that has three nested levels. RedisJSON is pitted against two variants that store the data in Strings. Both variants are implemented as Redis server-side Lua scripts with the json.lua variant storing the raw serialized JSON, and msgpack.lua using MessagePack encoding.

If you have 21 minutes to spare, here’s the RedisJSON presentation from [Redis Day TLV](/blog/redisday-tlv-2017/):

[Click here to view video](https://www.youtube.com/embed/NLRbq2FtcIk)

You can start playing with RedisJSON today!

- Using Docker simply run with the [Docker Image](https://hub.docker.com/r/redislabs/rejson/);

```javascript
# docker run -d -p 6379:6379 --name redis-rejson redis/rejson:latest
```

- Get it from the [GitHub repository](https://github.com/RedisJSON/RedisJSON)
- Read the [docs online](https://github.com/RedisJSON/RedisJSON).

There are still many features that we want to add to it, but over all RedisJSON is pretty neat. If you have feature requests or have spotted an issue, feel free to use the repo’s issue tracker. You can always [email](mailto:itamar@redis.com) or [tweet](https://twitter.com/itamarhaber) at me—I’m highly-available 🙂

*Ready to jump into RedisJSON? Check out *[*Getting Started with RedisJSON*](https://redis.io/docs/data-types/json/)* on the Redis Developer site!*
