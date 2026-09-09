---
title: "Connection Pools for Serverless Functions and Backend Services"
linkTitle: "Connection Pools for Serverless Functions and Backend Services"
url: "/blog/connection-pools-for-serverless-functions-and-backend-services/"
description: "When writing a server application that connects to a database, you often have to deal with connection pools, with problematic repercussions if you ignore the issue for too long. So, let’s dive into..."
date: 2019-10-10
blogCategories:
- "Tech"
authors:
- "Redis  "
lastmod: 2025-03-27
hidden: true
---

*By Redis   · Published 10 October 2019 · updated 27 March 2025*

![Blog tile image](/images/site-mirror/59a6269771994cd59bc450b5414a5c89486e2ae8-600x400.webp)

When writing a server application that connects to a database, you often have to deal with connection pools, with problematic repercussions if you ignore the issue for too long. So, let’s dive into the problem, and explore how connection pools address it.

## Too many connections

Server applications share a common requirement: they must respond to independent requests originating from multiple clients. A naively written server application that uses Redis (or any other database) will open a new connection to Redis for each request. Unfortunately, this approach doesn’t scale, because you can open only a limited number of connections at the same time before everything blows up. Opening and closing connections is also not cheap: not for the application and not for the database.

The good news is that this problem is entirely solvable by changing the code of your application. The bad news is that it’s not always trivial to do so by yourself, and this is where patterns such as connection pools can help.

## Serverless functions

Serverless functions are a relatively recent addition to cloud offerings, but in many ways they resemble old [CGI scripts](https://en.wikipedia.org/wiki/Common_Gateway_Interface): a small snippet of code that gets invoked per-request. If each invocation is independent from all others, does that mean it’s impossible to share connections? Not exactly.

Normally, when an application calls a serverless function, the process remains active for a while before being shut down, in case more requests come in. As long as the process remains active, it can maintain a long-running connection with Redis, but it’s up to you to implement that correctly.

In general, it’s easy to create a persistent connection, you just have to instantiate it outside of the main function’s body. Here’s an example with [AWS Lambda](https://aws.amazon.com/lambda/) using JavaScript:

```python
// Connection info, a URI with this shape:
// [redis[s]:]//[[user][:password@]][host][:port][/db-number][?db=db-number[&password=bar[&option=value]]]
const REDIS_URI = process.env.REDIS_URI;

// Redis client library
const redis = require('redis');

// Client instance
const r = redis.createClient(REDIS_URI);

// Promisify get and set
const { promisify } = require('util');
const setAsync = promisify(r.set).bind(r);
const getAsync = promisify(r.get).bind(r);

// This is the lambda function:
exports.handler =  async function(event, context) {
  console.log("EVENT: \n" + JSON.stringify(event, null, 2))
  
  // Set a key
  await setAsync("mykey", "hello world");
  
  // Return the value to the caller
  return getAsync("mykey");
}

```

Note that you will need to upload this script in a Zip archive that includes node_redis, a Redis client for Node.js ([the AWS documentation](https://docs.aws.amazon.com/lambda/latest/dg/nodejs-create-deployment-pkg.html#nodejs-package-dependencies) explains this in more detail).

The same concept can be applied to other languages and Function-as-a-Service (FaaS) cloud offerings ([Google Cloud Functions](https://cloud.google.com/functions/), [Microsoft Azure Functions](https://azure.microsoft.com/en-us/services/functions/), and so on).

In the case of JavaScript, the client doesn’t offer a connection pool because of the single-threaded nature of Node.js. In the example above, we were trying to reuse the same connection across more than one request, but if you were to use a function in Go, or in another language that has multi-threaded concurrency, the client would need also a connection-locking scheme, such as a connection pool.

## How do connection pools work?

The basic principle is simple: a client that implements a connection pool opens *n* connections to the database and then has a mechanism to mark connections as “available” or “in use,” and use only the free ones. Many connection pools work as in-place replacements for single connections, so calling .connect() will pluck a connection from the pool (i.e. mark it as “in use” and return the real connection to the caller), while .close() will simply put it back (without actually closing it).

If you’re using a multi-threaded language like Go, make sure to choose a client that supports connection pooling. [Go-redis](https://github.com/go-redis/redis) is a good choice from this perspective, as you can [read in the documentation](https://godoc.org/github.com/go-redis/redis#Client).

Some clients also let you send commands directly without first plucking a connection from the pool. While handy, there are some things to keep in mind when using a pool this way (more on this below).

## Services

With serverless functions, the whole application architecture is extremely simple: it’s just a function. When dealing with “serverful” services, though, sharing a connection becomes more burdensome when concurrency is involved.

A simple socket connection can’t be directly used by more than one thread, as some degree of coordination is required to avoid sending bits and pieces of multiple requests at the same time, which would result in a mix incomprehensible to the receiver.

In such cases, connection pools are a good way to make each sub-component seem like it is the only one using a connection, but even connection pools can’t completely abstract away every detail of connection management.

## Preventing connections from leaking

When a connection is plucked from the pool, your code must ensure the connection eventually gets put back. Connection pools implement an upper limit on how many connections can be open at any time (remember, limiting the total amount of connections is part of the goal), so leaking connections will eventually deadlock your service when the last .connect() hangs forever, refusing to open a new connection and waiting in vain for an existing one to return to the pool.

Occasionally, code that was not designed to be long-running gets incorporated in a bigger project and starts leaking connections. To prevent leaks, you just have to make sure to .close() the connection once you don’t need it anymore, but it’s not always easy to implement that in practice, especially in big, messy projects.

Let’s see a good way to use a connection pool and ensure proper cleanup in Python.

## A Python example: aio-redis

To show you some sample code, I’ll use [aio-redis](https://github.com/aio-libs/aioredis), a Redis client for Python [that supports asyncio](/blog/async-await-programming-basics-python-examples/). With aio-redis is possible to use a connection pool directly without plucking a connection first, as shown here:

```python
import asyncio, aioredis

async def main():
   pool = await aioredis.create_redis_pool('localhost',
      db=0, password=None, ssl=False, minsize=4, maxsize=10, encoding='utf8')

   # No need to pluck a single connection
   # aioredis will schedule your command to
   # a random connection inside the pool.
   await pool.set("key", "hello world")
   await pool.incrby("counter", 3)
 
if __name__ == '__main__':
    loop = asyncio.main_loop()
    loop.run_until_complete(main())

```

As mentioned earlier, this works fine for simple usage, but explicitly plucking a connection from the pool is preferable in some situations, particularly when an operation takes a long time to complete, such as in blocking operations on Streams, Lists, Sorted Sets, or [WAIT](https://redis.io/commands/wait).

## Blocking operations

While Redis commands tend to be very fast, some commands are designed to be blocking, meaning that they will not return an answer until certain conditions are met. For example, blocking reads on Streams ([XREAD](https://redis.io/commands/xread)) will wait for new entries to get into the stream when used with the BLOCK option (without it, XREAD would immediately return with an empty result-set). Keep in mind that these operations block the client, not the server. Redis will still be able to respond to commands sent through other connections.

Those types of commands are a problem for the usage pattern that we previously showed, because aio-redis doesn’t know for how long a given command will run and could decide to enqueue a new command to a connection that’s busy with a blocking command. This means that in the previous example, if there was another async function using the pool to do a blocking XREAD, our SET and INCRBY commands might have taken a surprisingly long time to complete, or might even timeout.

In those cases, you need to pluck a connection from the pool explicitly and also make sure to return it once you’re done. Python helps with the last part with a language feature called context managers, which you can access using a with block. The context manager block is created around a resource that must always be cleaned up (connections, file descriptors). At the end of the block, regardless of whether we are exiting successfully or by throwing an exception, the context manager triggers the appropriate cleanup procedure, which in our case consists of returning the connection to the pool, as shown here:

```python
import asyncio, aioredis

async def main():
   pool = await aioredis.create_redis_pool('localhost',
      db=0, password=None, ssl=False, minsize=4, maxsize=10, encoding='utf8')
    
   # Assuming we're not the only ones using the pool
   start_other_coroutines_that_use_redis(pool)
   
   # We reserve a connection for a blocking operation
   with await pool as conn:
      items = await conn.xread(['stream'], latest_ids=['$'], timeout=0)
      await process_items(items)
 
if __name__ == '__main__':
    loop = asyncio.main_loop()
    loop.run_until_complete(main())

```

(If you’re familiar with context managers and asyncio, you might notice that the with await pool … part is a bit odd, as this is usually expressed as async with pool … . This is a small quirk of the implementation of aio-redis, so everything still works as expected. You can find [more information on this issue here](https://github.com/aio-libs/aioredis/issues/443).)

## MULTI/EXEC transactions

Here’s another special case: MULTI/EXEC transactions. Make no mistake, transactions aren’t client-blocking operations, but they do make special use of the connection.

When you send MULTI the connection changes state and Redis starts enqueueing all commands, instead of executing them immediately. When a command is successfully enqueued (i.e., [it doesn’t contain blatant formatting errors](/blog/on-types-and-transactions/)), Redis replies with OK. This means that the connection is not literally blocked, but it can’t really be used to multiplex commands from multiple sub-parts of the program that are unaware of the fact that there is a transaction taking place.

Once you call EXEC or DISCARD, the whole transaction will respectively succeed or fail, and the connection will be returned to a normal state.

For this reason many clients have dedicated objects that represent a transaction. Normally transaction objects don’t even send the commands until you conclude the transaction. This improves performance without changing the semantics, since, as mentioned earlier, the commands will be enqueued by Redis only until the transaction is finalized:

```python
import asyncio, aioredis

async def main():
   pool = await aioredis.create_redis_pool('localhost',
      db=0, password=None, ssl=False, minsize=4, maxsize=10, encoding='utf8')
    
   # Assuming we're not the only ones using the pool
   start_other_coroutines_that_use_redis(pool)
   
   # This time we do a transaction 
   tr = pool.multi_exec()
   tr.set("key", "hello")
   
   # `execute` must be awaited, and be careful, 
   # awaiting the set command would deadlock the program
   # as you would never be able to commit the transaction!
   await tr.execute()
 
if __name__ == '__main__':
    loop = asyncio.main_loop()
    loop.run_until_complete(main())

```

## Connection management can’t be ignored

Connection management is an important part of any server-side application because it’s often a sensitive path, given the one-to-many relationship between servers and clients. The promise of infinite scalability in serverless functions can cause problems when you’re not properly managing connections, but fortunately the solution is easy to implement.

For more complex architectures, connection pools allow you to think about connection management only at the local (sub-component) level, but you can’t completely forego connection management, especially when doing operations that make special use of the connection, such as transactions or blocking operations.
