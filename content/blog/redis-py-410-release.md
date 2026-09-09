---
title: "Hello redis-py, It’s Been a Minute"
linkTitle: "Hello redis-py, It’s Been a Minute"
url: "/blog/redis-py-410-release/"
description: "Python support for Redis has been growing for over a decade, reaching over 1 million downloads per week, and we’re proud to announce the latest release, redis-py 4.1.0!"
date: 2022-01-18
blogCategories:
- "Company"
- "Product Releases"
authors:
- "Chayim Kirshen"
lastmod: 2026-09-01
hidden: true
---

*By Chayim Kirshen, Software Team Leader · Published 18 January 2022 · updated 1 September 2026*

![Blog tile image](/images/blog/dd803210e9ea43497bf6c58b9d070cd550956aed-772x550.webp)

#### redis-py 4.1.0 is released!

Python support for Redis has been growing for over a decade, [reaching over 1 million downloads per week](https://pypistats.org/packages/redis), and we’re proud to announce the latest release, redis-py 4.1.0!

This release almost brings us within spitting distance of complete[ Redis command support](https://redis.io/docs/latest/commands/) in Redis 6.2. We’ve added support for missing options in existing commands, SSL support for Sentinel connections, and generally improved the developer experience. It also brings large structural changes such as a focus on Python 3.6, and even Python 3.10 support. We’ve revamped our [client documentation](https://redis.io/docs/latest/), making it easier to find Redis commands, and encouraging [everyone to get involved](https://github.com/redis/redis-py/blob/master/CONTRIBUTING.md)! More importantly, we’ve done it with minimal disruption, so you can upgrade without compatibility issues.

## Support for newest Redis commands

[Redis 6.2](/blog/redis-6-2-the-community-edition-is-now-available/#:~:text=The%20new%20version%20introduces%20dozens,also%20reverts%20several%20historical%20decisions.) brings with it a huge swath of new Redis commands, and it’s now easier than ever to use them with Python. From making it easier to fetch data and update its expiration in a single command with [GETEX](https://redis.io/commands/GETEX), to managing your Redis instances by disconnecting clients with [CLIENT INFO](https://redis.io/commands/client-info) and [CLIENT KILL](https://redis.io/commands/client-kill) redis-py 4.1.0 has you covered. Let’s look at two examples below of the over 30 commands added in redis-py 4.1.0!

```python
### GETEX
import redis
r = redis.Redis()
r.set('somekey', 'hello')
r.getex('somekey', ex=15) # returns 'Hello'
r.ttl('somekey') # returns 15
​
​
### CLIENT INFO AND KILL
import redis
r = redis.Redis()
r2 = redis.Redis()
r.client_setname('redis-py-c1')
r2.client_setname('redis-py-c2')
​
clients = [client for client in r.client_list()
                   if client.get('name') in ['redis-py-c1', 'redis-py-c2']]
clients_by_name = dict([(client.get('name'), client)
                                for client in clients])
r.client_kill_filter(laddr=clients_by_name['redis-py-c2'].get('laddr'))

```

## First class Redis module support

redis-py 4.0 was the first version of the Python library to bring first-class support for Redis modules. With the release of redis-py 4.1.0, we now have support for [RedisJSON](http://redisjson.io), [RediSearch](http://redisearch.io), [RedisTimeSeries](http://redistimeseries.io), [RedisGraph](https://redisgraph.io), and [RedisBloom](https://redisbloom.io). That’s right, you can easily store JSON data in Redis! You can operate on it – you can even search it! Just remember, when you store JSON data in Redis, you’re storing a new data type, so you need to use the JSON specific commands to manipulate it. Here are some examples:

```python
### STORING and RETRIEVING JSON
​
import redis
r = redis.Redis()
myDoc = {'hello', 'world', 'colours': ['red', 'blue', 'green'], 'hmm': {'hello': 'again'}}
r.json().set('colors', '$', myDoc)
r.json().get('colors')

```

What about documents like myDoc above? Did you know that you can fetch multiple keys by querying a portion of the document?

```python
### FETCHING ALL KEYS NAMED “hello” from the JSON document
r.json().get('colors', '$..hello')

```

You can even combine [RedisJSON and RediSearch](/blog/index-and-query-json-docs-with-redis/) for document capabilities or add your custom Redis modules support. It’s all there in redis-py 4.0.

## Redis cluster support with redis-py

Did you know that redis-py 4.1.0 also integrates redis-cluster support, with two easy ways to connect? The same great experience for interacting with standalone Redis nodes is now part of redis-py.

```python
### CONNECTING TO CLUSTER
from redis.cluster import RedisCluster
r = RedisCluster.from_url('redis://4.5.6.8:6379')
nodes = r.get_nodes()

```

Maybe you’d like to connect to your cluster via SSL or prefer the class init based approach, and want to run commands, targeting specific nodes. redis-py 4.1.0 supports those scenarios!

```python
### CONNECTING TO CLUSTER 2
from redis.cluster import RedisCluster
r = RedisCluster('4.5.6.8', port=6379, ssl=True)
r.ping(target_nodes='all')

```

## What’s next?

The work is never done and we’re moving full steam ahead! We will add support for more modules, such as [RedisAI](https://redisai.io), with the same first class experience. We’re going to add support for [RESP3](https://github.com/redis/redis-specifications/blob/master/protocol/RESP3.md) functions that will be released in Redis 7, and speed up the code base. We’re also working on developer tooling, to make contributing to and working with redis-py even better!
