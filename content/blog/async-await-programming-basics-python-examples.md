---
title: "Async/Await Programming Basics with Python Examples"
linkTitle: "Async/Await Programming Basics with Python Examples"
url: "/blog/async-await-programming-basics-python-examples/"
description: "In recent years, many programming languages have made an effort to improve their concurrency primitives. Go has goroutines, Ruby has fibers and, of course, Node.js helped popularize async/await,..."
date: 2019-09-09
blogCategories:
- "Tech"
authors:
- "Redis  "
lastmod: 2025-03-27
hidden: true
---

*By Redis   · Published 9 September 2019 · updated 27 March 2025*

![Blog tile image](/images/blog/195c9500372c23ac887a1b57add2ff17c9d8807e-4512x3008.webp)

In recent years, many programming languages have made an effort to improve their concurrency primitives. Go has goroutines, Ruby has fibers and, of course, Node.js helped popularize async/await, which is today’s most widespread type of concurrency operator. In this post, I will talk about the basics of async/await, using Python as an example. I chose Python, since this capability is relatively recent in Python 3, and many users might not yet be familiar with it (especially considering how long it took for Python 2.7 to get to end of life).

The main reason to use async/await is to improve a program’s throughput by reducing the amount of idle time when performing I/O. Programs with this operator are implicitly using an abstraction called an event loop to juggle multiple execution paths at the same time. In some ways, these event loops resemble multi-threaded programming, but an event loop normally lives in a single thread—as such, it can’t perform more than one computation at a time. Because of this, an event loop alone can’t improve the performance of computation-intensive applications. However, it can drastically improve performance for programs that do a lot of network communication, like applications connected to a Redis database.

Every time a program sends a command to Redis, it has to wait for Redis to formulate a reply, and, if Redis is hosted on another machine, there’s also network latency. A simple, single-threaded application that doesn’t use an event loop sits idle while it waits for the reply to come in, which wastes a lot of CPU cycles. Keep in mind that network latency is measured in milliseconds, while CPU instructions take nanoseconds to execute. That’s a difference of six orders of magnitude.

As an example, here’s a code sample that tracks wins for a hypothetical game. Each stream entry contains the winner’s name, and our program updates a Redis Sorted Set that acts as the leaderboard. The code is not very robust, but we don’t care about that for now, because we’re focusing on the performance of blocking versus non-blocking code.

```python
import redis


# The operation to perform for each event
def add_new_win(conn, winner):
    conn.zincrby('wins_counter', 1, winner)
    conn.incr('total_games_played')

def main():
    # Connect to Redis
    conn = redis.Redis()
    # Tail the event stream
    last_id = '$' 
    while True:
        events = conn.xread({'wins_stream': last_id}, block=0, count=10)
        # Process each event by calling `add_new_win`
        for _, e in events:
            winner = e['winner']
            add_new_win(conn, winner)
            last_id = e['id']

if __name__ == '__main__':
    main()

```

To write an equivalent async version of the code above, we’ll use [aio-libs/aioredis](https://github.com/aio-libs/aioredis).

The aio-libs community is rewriting many Python networking libraries to include support for asyncio, Python’s standard library implementation of an event loop. Here’s a non-blocking version of the code above:

```python
import asyncio
import aioredis


async def add_new_win(pool, winner):
    await pool.zincrby('wins_counter', 1, winner)
    await pool.incr('total_games_played')

async def main():
    # Connect to Redis
    pool = await aioredis.create_redis_pool('redis://localhost', encoding='utf8')
    # Tail the event stream
    last_id = '$'
    while True:
        events = await pool.xread(['wins_stream'], latest_ids=[last_id], timeout=0, count=10)
        # Process each event by calling `add_new_win`
        for _, e_id, e in events:
            winner = e['winner']
            await add_new_win(pool, winner)
            last_id = e_id

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

```

This code is mostly the same, other than a few await keywords sprinkled around. The biggest difference is what happens in the last couple of lines. In Node.js, the environment loads an event loop by default, while, in Python, you have to start it explicitly — that’s what those final lines do.

After the rewrite, we might think we improved performance just by doing this much. Unfortunately, the non-blocking version of our code does not improve performance yet. The problem here lies with the specifics of how we wrote the code, not with the general idea of using async / await.

## Limiting the use of await

The main issue with our rewrite is that we overused await. When we prefix an asynchronous call with await, we do two things:

1. Schedule it for execution.
1. Wait for it to complete.

Sometimes, that’s the right thing to do. For example, we won’t be able to iterate on each event until we are done reading from the stream on line 15. In that case, the await keyword makes sense, but look at add_new_win:

```python
async def add_new_win(pool, winner):
    await pool.zincrby('wins_counter',  1, winner)
    await pool.incr('total_games_played')

```

In this function, the second operation doesn’t really depend on the first. We would be fine with the second command being sent along with the first, but await blocks the execution flow as soon as we send the first. We would like a way to schedule both operations immediately. For that, we need a different synchronization primitive.

```python
async def add_new_win(pool, winner):
    task1 = pool.zincrby('wins_counter', 1, winner)
    task2 = pool.incr('total_games_played')
    await asyncio.gather(task1, task2)

```

First of all, calling an async function directly won’t execute any of its code. Instead, it will just instantiate a “task.” Depending on your language of choice, this might be called coroutine, promise, future or something else. Without getting into the weeds, for us, a task is an object representing a value that will be available only after using await or another synchronization primitive, like asyncio.gather.

In Python’s official documentation, [you can find more information about asyncio.gather](https://docs.python.org/3/library/asyncio-task.html). In short, it allows us to schedule multiple tasks at the same time. We need to await its result because it creates a new task that completes once all the input tasks are completed. Python’s asyncio.gather is equivalent to JavaScript’s [Promise.all](https://developer.mozilla.org/en/docs/Web/JavaScript/Reference/Global_Objects/Promise/all), C#’s [Task.WhenAll](https://docs.microsoft.com/en-us/dotnet/api/system.threading.tasks.task.whenall?view=netframework-4.7.2), Kotlin’s [awaitAll](https://kotlin.github.io/kotlinx.coroutines/kotlinx-coroutines-core/kotlinx.coroutines/await-all.html), etc.

## Improving our main loop

The same thing we did for add_new_win can be also done for the main stream event processing loop. Here’s the code I’m referring to:

```python
last_id = '$'
while True:
    events = await pool.xread(['wins_stream'], latest_ids=[last_id], timeout=0, count=10)
    for _, e_id, e in events:
        winner = e['winner']
        await add_new_win(pool, winner)
        last_id = e_id

```

Given what we have learned so far, you will notice that we are processing each event sequentially. We know that for sure because on line 6 the use of await both schedules and waits for the completion of add_new_win. Sometimes that’s exactly what you want to happen, because the program logic would break if you were to apply changes out of order. In our case, we don’t really care about ordering because we’re just updating counters.

```python
last_id = '$'
while True:
    events = await pool.xread(['wins_stream'], latest_ids=[last_id], timeout=0, count=10)
    tasks = []
    for _, e_id, e in events:
        winner = e['winner']
        tasks.append(add_new_win(pool, winner))
        last_id = e_id
    await asyncio.gather(*tasks)

```

We are now also concurrently processing each batch of events, and our change of code was minimal. One last thing to keep in mind is that sometimes programs can be performant even without the use of asyncio.gather. In particular, when you’re writing code for a web server and using an asynchronous framework like [Sanic](https://github.com/huge-success/sanic), the framework will call your request handlers in a concurrent way, ensuring great throughput even if you await every asynchronous function call.

## In conclusion

Here’s the complete code example after the two changes we presented above:

```python
import asyncio
import aioredis


async def add_new_win(pool, winner):
    # Creating tasks doesn't schedule them
    # so you can create multiple and then 
    # schedule them all in one go using `gather`
    task1 = pool.zincrby('wins_counter', 1, winner)
    task2 = pool.incr('total_games_played')
    await asyncio.gather(task1, task2)
    
async def main():
    # Connect to Redis
    pool = await aioredis.create_redis_pool('redis://localhost', encoding='utf8')
    # Tail the event stream
    last_id = '$'
    while True:
        events = await pool.xread(['wins_stream'], latest_ids=[last_id], timeout=0, count=10)
        tasks = []
        for _, e_id, e in events:
            winner = e['winner']
            # Again we don't actually schedule any task,
            # and instead just prepare them
            tasks.append(add_new_win(pool, winner))
            last_id = e_id
        # Notice the spread operator (`*tasks`), it
        # allows using a single list as multiple arguments
        # to a function call.
        await asyncio.gather(*tasks)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

```

In order to exploit non-blocking I/O, you need to rethink how you approach networked operations. The good news is that it’s not particularly difficult, you just need to know when sequentiality is important and when it’s not. Try experimenting with aioredis or an equivalent asynchronous Redis client, and see how much you can improve the throughput of your applications.
