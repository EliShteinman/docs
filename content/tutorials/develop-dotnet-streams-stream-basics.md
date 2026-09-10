---
title: "How to use Redis Streams with .NET"
linkTitle: "How to use Redis Streams with .NET"
url: "/tutorials/develop/dotnet/streams/stream-basics/"
description: "Redis Streams are a powerful data structure that allows you to use Redis as a message bus to transport messages between different application components. Streams are fast and memory efficient,..."
group: "For developers"
aliases:
- "/tutorials/develop-dotnet-streams-stream-basics/"
date: 2026-02-25
lastmod: 2026-02-26
hidden: true
mirrored: true
---

*Published 25 February 2026 · updated 26 February 2026*

> **TL;DR:**
>
> To use Redis Streams in .NET, install the `StackExchange.Redis` package, connect with `ConnectionMultiplexer`, and use `StreamAddAsync` to produce messages and `StreamReadGroupAsync` to consume them through consumer groups. The full working example below covers producing, reading, and acknowledging stream messages.

Redis Streams are a powerful data structure that allows you to use Redis as a message bus to transport messages between different application components. Streams are fast and memory efficient, making them ideal for event-driven architectures in .NET. This tutorial provides a hands-on guide to using Redis Streams with StackExchange.Redis in a C# console application.

## What you'll learn

- How to add messages to a Redis Stream with `XADD` via `StreamAddAsync`
- How to read the most recent stream entry with `XRANGE` via `StreamRangeAsync`
- How to create and use consumer groups for reliable message processing
- How to acknowledge processed messages with `StreamAcknowledgeAsync`

## Prerequisites

- [Docker](https://www.docker.com/) (or an existing Redis instance)
- [.NET SDK](https://dotnet.microsoft.com/download) 6.0 or later
- A code editor or IDE that supports C#

## How do I start Redis for .NET development?

The first thing we'll want to do is start Redis. If you already have an instance of Redis, you can ignore this bit and adjust the connection step below to connect to your instance of Redis. Redis is straightforward to get up and running; you can do so using docker:

```bash
docker run -p 6379:6379 redis
```

## How do I create a .NET app for Redis Streams?

For simplicity's sake, we'll stick to a simple console app, from which we'll spin out a few tasks that will perform the various add/read operations that we'll use. Create a new console app with the `dotnet new` command:

```bash
dotnet new console -n RedisStreamsBasics
```

## How do I add the StackExchange.Redis package?

Next, we'll need to add the client library that we will use to interface with Redis StackExchange.Redis is the canonical package, thus, we will use that in this example. First cd into the RedisStreamsBasics directory and then run the `dotnet add package` directory:

```bash
cd RedisStreamsBasics
dotnet add package StackExchange.Redis
```

## How do I initialize the ConnectionMultiplexer?

StackExchange.Redis centers more or less around the `ConnectionMultiplexer`, which handles the routing and queuing of all commands that you send to Redis. So our first step that's code-related is to initialize the Multiplexer. Creating the Multiplexer is pretty straightforward; open up `Program.cs` in your IDE and add the following bit to it:

```csharp
using StackExchange.Redis;

var tokenSource = new CancellationTokenSource();
var token = tokenSource.Token;

var muxer = ConnectionMultiplexer.Connect("localhost");
var db = muxer.GetDatabase();

const string streamName = "telemetry";
const string groupName = "avg";
```

We're also initializing a `CancellationToken` and `CancellationTokenSource` here. We'll set these up towards the end of this tutorial so that this application does not run endlessly. Also, we're creating a couple of constants, the stream's name and the group's name, that we'll use later, and we are also grabbing an `IDatabase` object from the Multiplexer to use

## How do I create a consumer group in Redis Streams?

A Consumer Group in a Redis Stream allows you to group a bunch of consumers to pull messages off the stream for the group. This functionality is excellent when you have high throughput workloads, and you want to scale out the workers who will process your messages. To use a consumer group, you first need to create it. To create a consumer group, you'll use the `StreamCreateConsumerGroupAsync` method, passing in the `streamName` and `groupName`, as well as the starting id - we'll use the `0-0` id (the lowest id allowable in Redis Streams). Before invoking this call, it's wise to validate that the group doesn't exist yet, as creating an already existing user group will result in an error. So first, we'll check if the stream exists; if it doesn't, we can create the group. Next, we'll use the stream info method to see if any groups match the `avg` `groupName`.

```csharp
if (!(await db.KeyExistsAsync(streamName)) ||
    (await db.StreamGroupInfoAsync(streamName)).All(x=>x.Name!=groupName))
{
    await db.StreamCreateConsumerGroupAsync(streamName, groupName, "0-0", true);
}
```

## How do I produce messages with XADD in .NET?

Three tasks will run in parallel for our program. The first is the `producerTask`. This Task will write a random number between 50 and 65 as the `temp` and send the current time as the `time`.

```csharp
var producerTask = Task.Run(async () =>
{
    var random = new Random();
    while (!token.IsCancellationRequested)
    {
        await db.StreamAddAsync(streamName,
            new NameValueEntry[]
                {new("temp", random.Next(50, 65)), new NameValueEntry("time", DateTimeOffset.Now.ToUnixTimeSeconds())});
        await Task.Delay(2000);
    }
});
```

## How do I parse stream entries in StackExchange.Redis?

The results retrieved from Redis will be in a reasonably readable form; all the same, it is helpful for our purposes to parse the result into a dictionary. To do this, add an inline function to handle the parsing:

```csharp
Dictionary<string, string> ParseResult(StreamEntry entry) => entry.Values.ToDictionary(x => x.Name.ToString(), x => x.Value.ToString());
```

> **Note**
>
> Stream messages enforce no requirement that field names be unique. We use a dictionary for clarity sake in this example, but you will need to ensure that you are not passing in multiple fields with the same names in your usage to prevent an issue using a dictionary.

## How do I read the most recent stream entry?

Next, we'll need to spin up a task to read the most recent element off of the stream. To do this, we'll use the `StreamRangeAsync` method passing in two special ids, `-` which means the lowest id, and `+`, which means the highest id. Running this command will result in some duplication. This redundancy is necessary because the `StackExchange.Redis` library does not support blocking stream reads and does not support the special `$` character for stream reads. For this tutorial, you can manage these most-recent reads with the following code:

```csharp
var readTask = Task.Run(async () =>
{
    while (!token.IsCancellationRequested)
    {
        var result = await db.StreamRangeAsync(streamName, "-", "+", 1, Order.Descending);
        if (result.Any())
        {
            var dict = ParseResult(result.First());
            Console.WriteLine($"Read result: temp {dict["temp"]} time: {dict["time"]}");
        }

        await Task.Delay(1000);
    }
});
```

## How do I read and acknowledge messages with a consumer group?

The final Task we'll spin up is the read task for the consumer group. Due to the nature of consumer groups, you can spin this Task up multiple times to scale out the processing as needed. It's the responsibility of Redis to keep track of which messages it's distributed to the consumer group. As well as tracking which messages Consumers have acknowledged. Acknowledging messages adds a layer of validation that all messages were processed. If something happens to one of your processing tasks or processes, you can more easily know what messages you missed.

We'll check to see if we have a recent message-id to handle all of this. If we do, we will send an acknowledgment to the server that the id was processed. Then we will grab the next message to be processed from the stream, pull out the data and the id and print out the result.

```csharp
double count = default;
double total = default;

var consumerGroupReadTask = Task.Run(async () =>
{
    string id = string.Empty;
    while (!token.IsCancellationRequested)
    {
        if (!string.IsNullOrEmpty(id))
        {
            await db.StreamAcknowledgeAsync(streamName, groupName, id);
            id = string.Empty;
        }
        var result = await db.StreamReadGroupAsync(streamName, groupName, "avg-1", ">", 1);
        if (result.Any())
        {
            id = result.First().Id;
            count++;
            var dict = ParseResult(result.First());
            total += double.Parse(dict["temp"]);
            Console.WriteLine($"Group read result: temp: {dict["temp"]}, time: {dict["time"]}, current average: {total/count:00.00}");
        }
        await Task.Delay(1000);
    }
});
```

## How do I set a timeout and run all tasks?

Finally, we need to set the timeout and await the tasks at the end of our program:

```csharp
tokenSource.CancelAfter(TimeSpan.FromSeconds(20));
await Task.WhenAll(producerTask, readTask, consumerGroupReadTask);
```

## How do I run the app?

You can now run this app with the `dotnet run` command.

## Redis Streams vs Pub/Sub: when should I use which?

Both Redis Streams and [Redis Pub/Sub](https://redis.io/docs/latest/develop/interact/pubsub/) enable messaging, but they serve different use cases:

- **Pub/Sub** is fire-and-forget. Messages are delivered to all connected subscribers in real time, but if a subscriber is offline it misses the message. Use Pub/Sub when you need low-latency fan-out and can tolerate message loss (e.g., live notifications, chat).
- **Streams** persist messages in an append-only log. Consumer groups track which messages each consumer has processed, enabling reliable delivery, replay, and horizontal scaling of workers. Use Streams when you need message durability, backpressure handling, or the ability to reprocess historical events (e.g., event sourcing, task queues, telemetry pipelines).

If your .NET application requires guaranteed delivery or needs to process messages after a restart, Redis Streams are the better choice. For simple real-time broadcasting where persistence isn't needed, Pub/Sub is lighter weight.

## Next steps

- Explore the [source code for this tutorial](https://github.com/redis-developer/redis-streams-with-dotnet/tree/main/RedisStreamsStackExchange) on GitHub
- Learn how Redis Streams power [microservices interservice communication](/tutorials/howtos/solutions/microservices/interservice-communication/) in production architectures
- Get started with [Redis OM .NET](/tutorials/redis-om-dotnet-getting-started/) for object mapping and data persistence
- Add [API caching to your ASP.NET Core application](/tutorials/develop/dotnet/aspnetcore/caching/basic-api-caching/) with Redis
- Take the Redis University [Streams course](https://university.redis.io/learningpath/grnomm8jaglgcu?tab=details) for a deep dive into consumer groups, trimming, and more
- Read the official [Redis Streams documentation](https://redis.io/docs/latest/develop/data-types/streams/) for the full command reference
