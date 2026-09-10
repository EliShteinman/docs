---
title: "Bullet-Proofing Lua Scripts in RedisPy"
linkTitle: "Bullet-Proofing Lua Scripts in RedisPy"
url: "/blog/bullet-proofing-lua-scripts-in-redispy/"
description: "Lua scripting is a hugely powerful feature of Redis. At the same time, though, Lua scripting can be tricky to “get right.”"
date: 2020-02-19
blogCategories:
- "Tech"
authors:
- "Redis  "
lastmod: 2025-03-27
hidden: true
mirrored: true
---

*By Redis   · Published 19 February 2020 · updated 27 March 2025*

![Blog tile image](/images/site-mirror/0a0b80066c9fd0a9566eda189f09220e2e6f3010-1280x744.webp)

Lua scripting is a hugely powerful feature of Redis. At the same time, though, Lua scripting can be tricky to “get right.”

There are many ways to run a script that *works most of the time, *which can also be articulated as a script that *fails some of the time*. Let’s take a look at a Lua scripting corner case in Python with RedisPy where your script can fail despite doing what looks correct. Of course, at the end, we’ll show you the bullet-proof way to do it when you need everything to *always* work.

## Lua script handling fundamentals

We need to review Redis’ Lua scripting engine and how you run a script. First and most basic is [EVAL](https://redis.io/commands/eval). This command accepts the *full Lua source* followed by the keys count, keys, and finally any arguments that are passed into the script. Sending the source code over and over is a waste of bandwidth, so [SCRIPT LOAD](https://redis.io/commands/script-load) lets you send the Lua source once and receive a SHA-1 digest that you can use later to identify and run this script with [EVALSHA](https://redis.io/commands/evalsha). This command functions just like EVAL, but points to the SHA-1 digest. Redis uses an entirely separate, keyspace-less cache for the scripts: both EVAL and SCRIPT LOAD take the source code, compile it, and store the byte code representation in the cache, but EVAL first checks the script cache so it won’t trigger recompilation of the script if it is already stored in the script cache.

The problem with EVALSHA is that if you try to run a script that doesn’t exist in the script cache, you’ll get the following error:

(error) NOSCRIPT No matching script. Please use EVAL.

If you don’t want to immediately run the script, you can use the [SCRIPT EXISTS](https://redis.io/commands/script-exists) command to see if a given SHA-1 digest represents a cached script. In effect, an application that uses Lua scripting in Redis always needs to be ready to supply Redis with the full Lua source at any given time, and there is no way to ensure that a given script is never evicted from the script cache.

## A slice of Lua RedisPy

RedisPy is a full featured client library that improves Lua’s ergonomics in Redis—let’s see what it does to make your life easier. For one thing, you don’t have to manage SHA-1 hashes or loading scripts on your own most of the time—RedisPy abstracts this away in a clean, Pythonic style. Let’s look at it from the Python REPL:

>> import redis

>>> r = redis.Redis()

>>> mylua = """

... return "hello world"

... """

>>> hello = r.register_script(mylua)

>>> hello()

b'hello world'



What is happening here from the Redis perspective? If you run [MONITOR](https://redis.io/commands/monitor) while inputing this script line-by-line, you’ll see activity only when you invoke hello(). The output should look something like this (if your script cache is empty):

"EVALSHA" "0a4e337ee79a86930eb054981e3acc8a22d0674d" "0"

"SCRIPT" "LOAD" "nreturn "hello world"n"

"EVALSHA" "0a4e337ee79a86930eb054981e3acc8a22d0674d" "0"



This shows what RedisPy is doing: trying to run the script, getting a NOSCRIPT error, loading the script, then running EVALSHA again. If you run hello() again, it will show only a single EVALSHA. So, you can see this abstraction is saving you a little bit of code and making your code more readable.

RedisPy also gives you an abstraction around pipelining and transactions. You create a pipeline object, then just perform your operations normally. To demonstrate, first, I’m going to run [SCRIPT FLUSH](https://redis.io/commands/script-flush) (which empties the entire script cache) from redis-cli then back to the REPL:

>> import redis

>>> mylua = """

... return "hello world"

... """

>>> r = redis.Redis()

>>> mypipeline = r.pipeline()

>>> mypipeline.get('foo')

Pipeline<ConnectionPool<Connection<host=localhost,port=6379,db=0>>>

>>> hello = mypipeline.register_script(mylua)

>>> hello()

Pipeline<ConnectionPool<Connection<host=localhost,port=6379,db=0>>>

>>> mypipeline.execute()

[None, b'hello world']



A possible point of confusion is that pipelines and transactions are two very different things, yet RedisPy uses the same construct for both: despite the word “pipeline,” the commands in the script above will run as a MULTI/EXEC transaction. If you were to change r.pipeline() to r.pipeline(transaction=False), you would have a pipeline. (That is not how I would have chosen to do this, but countless lines of Python have already worn this path.)

So, what is happening on the Redis side? When you press Return on mypipeline.execute(), the following will be shown by MONITOR:

"SCRIPT" "EXISTS" "0a4e337ee79a86930eb054981e3acc8a22d0674d"

"SCRIPT" "LOAD" "nreturn "hello world"n"

"MULTI"

"GET" "foo"

"EVALSHA" "0a4e337ee79a86930eb054981e3acc8a22d0674d" "0"

"EXEC"



Something more sophisticated is going on here than in our previous example. Indeed, if you look at the [source code to RedisPy](https://github.com/andymccurdy/redis-py/blob/ff69f0d77284643909462ee6d1e37233c6677672/redis/client.py#L3924), it’s doing something quite smart. Because in either a pipeline or a transaction you can’t get a reply back until it’s all over, RedisPy is checking for the existence (SCRIPT EXISTS) of scripts that will be executed *before* it starts the transaction. If the script doesn’t yet exist in the cache, then RedisPy uses SCRIPT LOAD to cache the script for later execution. Only after this dance is finished will it start the transaction. In the middle of the transaction, we’re using EVALSHA to invoke the script.

## Sneaky concurrency

Now, we all know that many, many clients can connect to a single Redis server. While Redis is single threaded for the most part, it uses an event loop, so it’s doing only one thing at a time—but that thing may not be *your* one thing. Outside of a MULTI/EXEC transaction or commands *inside* a Lua script, there is no guarantee that commands sent rapidly by your application will be executed atomically by Redis. Other connected clients could sneak in commands *between* what is sent by your application.

Let’s take a look at what is really going on with the script check/load sequence in RedisPy:

1. Python sends “SCRIPT EXISTS” and arguments
1. Redis executes the command and returns 0 to Python
1. Redis does other stuff while Python is evaluating the return
1. Python sends “SCRIPT LOAD” and arguments
1. Redis executes the command and returns the SHA-1 hash
1. Redis does other stuff while Python evaluates the return and prepares to send the MULTI/EXEC block
1. Python sends the MULTI/EXEC block
1. Redis executes the block and returns the results of the MULTI/EXEC block

Note that at steps 3 and 6 Redis is “doing other stuff.” That could be just an idle loop or it could be serving other commands to other applications. The place where Redis cannot do anything else is during step 8. Now, steps 3 and 6 typically consume a very short amount of time—micro- or milliseconds—but still a non-zero value.

It is possible that other ‘things’ can happen during this process since Redis is doing other stuff.

For example, imagine you’re running a chaotic script connected to the same Redis server. This script, for some unknown reason, is running a tight loop of SCRIPT FLUSH commands. So in our stepwise example above, it’s possible that the “other stuff” mentioned in step 6 could be a SCRIPT FLUSH. Despite just doing a SCRIPT LOAD, the MULTI/EXEC block could start running with a missing script.

A chaotic SCRIPT FLUSHing script is not the only scenario where this could be an issue. Imagine that you are running a great many Lua scripts (not usually a best practice, but it does happen) and are tight on space in your script cache. Then another application comes along and does a similar process and SCRIPT LOADs its scripts and evicts your script from the cache before your MULTI/EXEC runs. You’re in the same situation as the tight-loop SCRIPT FLUSH.

It’s important to note that RedisPy is doing nothing wrong here. There is no mechanism to use EVALSHA in a MULTI/EXEC transaction and be sure that the script exists before starting.

Nevertheless, the end result of all these scenarios is that you’re left with a Lua script that *sometimes *works and *sometimes* fails, which is pretty scary. However, this doesn’t mean that you should never run Lua in a transaction. There is a bullet-proof way to do this—incur the bandwidth penalty and run EVAL with the full Lua source *inside* the transaction.

Let’s see how this approach looks in Python:

>> mypipeline = r.pipeline()

>>> mypipeline.get('foo')

Pipeline<ConnectionPool<Connection<host=localhost,port=6379,db=0>>>

>>> mypipeline.eval("""

... return "hello world"

... """, 0)

Pipeline<ConnectionPool<Connection<host=localhost,port=6379,db=0>>>

>>> mypipeline.execute()

[None, b'hello world']



One note: if you’re running the same Lua script multiple times within a single transaction, you can safely use EVALSHA on subsequent invocations of the same script within the MULTI/EXEC block. Remember, EVAL will still cache the script. This will save you a little bandwidth in what is, for sure, a very unusual circumstance.

Up until this point we’ve talked about MULTI/EXEC *transactions—*what about Lua scripts within a *pipeline*? In that case the risk is perhaps even more pronounced. Remember, pipelines do not provide any atomic guarantees so there are more opportunities for chaotic SCRIPT FLUSHing or cache fills and evictions to occur.

## What’s the RedisPy/Lua script verdict?

So, should you avoid using the ergonomic register_script function of RedisPy with transactions or pipelines?

I wouldn’t go that far. The real answer, though unsatisfying, is that it depends.

If your Lua script is doing something mission-critical, then yes, bite the bullet, accept the bandwidth penalty, and stick with good old EVAL. But if the script is doing something you can account for later by looking at your transaction or pipeline response, then go for it. And remember, outside these pipeline and transaction scenarios, the register_scriptprovides tons of value to your code in a way that isn’t really risky.
