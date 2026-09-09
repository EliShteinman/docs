---
title: "Introduction to RedisGears"
linkTitle: "Introduction to RedisGears"
url: "/blog/introduction-to-redisgears/"
description: "At RedisConf19, we announced the release of a new module called RedisGears. You may have already seen some other modules by either Redis or the community at large, but Gears will defy any..."
date: 2019-07-16
blogCategories:
- "Tech"
authors:
- "Redis  "
lastmod: 2025-03-27
hidden: true
---

*By Redis   · Published 16 July 2019 · updated 27 March 2025*

![Blog tile image](/images/blog/3b575e8f344a604c9bebbb5724d0a1ffe82754b7-3948x2627.webp)

At [RedisConf19](https://events.redis.com/redis-conf/redis-conf-2019/), we announced the release of a new module called RedisGears. You may have already seen some other modules by either Redis or the community at large, but Gears will defy any expectations you have. It really pushes the limits of what is possible with modules. The only caveat is that it’s still in Preview so, while you can already try it out, you will have to wait a bit more for it to get to General Availability and become officially supported.


## Gears scripts

At first glance, [RedisGears](/redis-enterprise/technology/gears/) looks like a general-purpose scripting language that can be used to query your data in Redis. Imagine having a few hashmaps in your Redis database with user-related information such as age and first/last name.

```python
> RG.PYEXECUTE "GearsBuilder().filter(lambda x: int(x['value']['age']) > 35).foreach(lambda x: execute('del', x['key'])).run('user:*')"

```

Here is the execution breakdown for the RedisGears script:

1. It is run on all keys that match the user:* pattern.
1. The script then filters out all keys that have the age hash field lower than (or equal to) 35.
1. It then runs all remaining keys through a function that calls DEL on them (i.e., the keys are deleted).
1. Finally, it returns both key names and key values to the client.

This simple example showcases how you can use a Gears script similar to how you would use the query language for any other database. But, in fact, RedisGears scripts can do much more because they **are Python functions running in a full-fledged Python interpreter inside Redis, with virtually no limitations.** Let me show you why that matters:

```python
> HSET vec:1 x 10 y 5 z 23
(integer) 3
> HSET vec:2 x 2 y 5 z 5
(integer) 3
> RG.PYEXECUTE 'import numpy; GearsBuilder().map(lambda x: [float(x["value"]["x"]), float(x["value"]["y"]), float(x["value"]["z"])]).accumulate(lambda a, x: x if a is None else numpy.mean([a, x], axis=0)).flatmap(lambda x: x.tolist()).run("vec:*")'
1) 1) "14.0"
   2) "5.0"
   3) "6.0"
2) (empty list or set)

```

In this example, I’ve installed numpy in my server using pip so I can use it inside my scripts. This means that all the Python libraries you love, and even your own code, can now be used to process data inside Redis. How neat is that?

[In this gist](https://gist.github.com/kristoff-it/ca3c9f4de23e9a536f9c6f43e1db4598), you can read how to install Python packages in our RedisGears Docker container.

## Gears executes full-fledged Python scripts

You might have noticed by now that one-liners inside redis-cli are not a super clear way to write RedisGears scripts. Thankfully, the [RG.PYEXECUTE](https://oss.redis.com/redisgears/commands.html#rgpyexecute) command is not limited to those. You can also feed it full-fledged Python source files. This also means that the script can contain normal Python functions, so you’re not forced to use lambdas if you don’t want to. Let me show a couple of ways to load a Python script. Here’s a more readable version of the previous example:

```python
# script.py
import numpy as np

def hash2list(redis_key):
  h = redis_key['value'] # redis_key contains 'key' and 'value'
  return [float(h['x']), float(h['y']), float(h['z'])]

def do_mean(acc, x):
  if acc is None:
    return x
  return np.mean([acc, x], axis=0)

GearsBuilder()\
.map(hash2list)\
.accumulate(do_mean)\
.flatmap(lambda x: x.tolist())\
.run("vec:*")

```

### With redis-cli

```python
$ redis-cli hset vec:1 x 10 y 5 z 23
$ redis-cli hset vec:2 x 2 y 5 z 5
$ cat script.py | redis-cli -x RG.PYEXECUTE
1) 1) "14.0"
   2) "5.0"
   3) "6.0"
2) (empty list or set)

```

### Using Python (or any other language)

```python
$ redis-cli hset vec:1 x 10 y 5 z 23
$ redis-cli hset vec:2 x 2 y 5 z 5
$ python3
>>> import redis
>>> r = redis.Redis(decode_responses=True) # decode_responses is useful in py3 
>>> script = open("path/to/script.py", 'r').read()
>>> r.execute_command("RG.PYEXECUTE", script)
[['14.0', '5.0', '6.0'], []]

```

## Gears is cluster-aware

RedisGears can also understand your cluster’s topology and propagate commands accordingly. We already made implicit use of that feature in our previous examples, since the scripts would behave as intended when run in a cluster (i.e., each shard would do its part of the job and finally aggregate all the partial results if necessary).

You’ll occasionally need more fine-grained control over how your computation is executed, especially for multi-stage pipelines where you have an intermediate aggregation/re-shuffle step. For this purpose, you have at your disposal [collect](https://oss.redis.com/redisgears/operations.html#collect) and [repartition](https://oss.redis.com/redisgears/operations.html#repartition). These will, respectively, go from a distributed sequence of values to a materialized list inside a single node and, inversely, back to a distributed stream sharded according to a strategy of your choice.

You can also launch a job that doesn’t require the client to stay connected, and wait for a result. When you add the optional UNBLOCKING argument to RG.PYEXECUTE, you’ll immediately get a token that can be used to check the state of the computation and eventually retrieve the final result. That said, know that RedisGears scripts are not limited to one-off executions when invoked from a client.

## Gears can react to streams and keyspace events

Have you ever had the need to launch operations inside Redis in response to a keyspace event, or to quickly process new entries in a stream for a situation where spinning up client consumers seems wasteful?

RedisGears enables reactive programming at the database level. It’s like using lambda functions, but with a dramatically lower latency, and with much less encoding/decoding overhead.

Here’s a script that records all commands run on keys that have an audited- prefix:

```python
GearsBuilder().filter(lambda x: x['key'].startswith('audited-')).foreach(lambda x: execute('xadd', 'audit-logs', '*', 'key', x['key'])).register()


```

This second script then reads the audit-logs stream and updates access counts in a sorted set called audit-counts:

```python
GearsBuilder('StreamReader').foreach(lambda x: execute('zadd', 'audit-counts', '1', x['key'])).register('audit-logs')


```

If you register both queries, you will see that both the stream and counts update in real time. This is a very simple example to show what can be done (clearly not a great audit logging system). If you want a more concrete example, take a look [at some recipes](/redis-enterprise/technology/gears/).

## Gears is asynchronous

Don’t be afraid to launch demanding jobs. RedisGears scripts run in a separate thread, so they don’t block your Redis instance. This also means that Gears queries can’t be embedded inside a Redis transaction. If you have a cluster constantly under memory pressure or running transactional workloads, Lua scripts will be your best choice to add custom transactional logic to your operations. For everything else, there’s Gears.

## Next steps

The quickest way to try out RedisGears is by launching a container. Keep in mind that our modules also work with open source Redis.

We have a Docker container [on DockerHub](https://hub.docker.com/u/redis) that contains all the Redis modules:

docker run -p 6379:6379 redis/redismod:latest

We also have a version that contains RedisGears only:

docker run -p 6379:6379 redis/redisgears:latest

[Read more about Redis programmability](https://redis.io/docs/interact/programmability/)
