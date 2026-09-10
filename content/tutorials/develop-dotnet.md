---
title: ".NET and Redis"
linkTitle: ".NET and Redis"
url: "/tutorials/develop/dotnet/"
description: "To use Redis with .NET, install the StackExchange.Redis NuGet package, create a ConnectionMultiplexer, and call commands like StringSet and StringGet on the IDatabase object. StackExchange.Redis is..."
group: "For developers"
aliases:
- "/tutorials/develop-dotnet/"
date: 2026-02-24
lastmod: 2026-02-24
hidden: true
---

*Published 24 February 2026*

To use Redis with .NET, install the [StackExchange.Redis](https://github.com/StackExchange/StackExchange.Redis) NuGet package, create a `ConnectionMultiplexer`, and call commands like `StringSet` and `StringGet` on the `IDatabase` object. StackExchange.Redis is the most widely adopted C# Redis client, built by the team behind [StackOverflow](https://stackoverflow.com/).

## What you'll learn

- How to install the StackExchange.Redis NuGet package
- How to connect to Redis from a .NET application using `ConnectionMultiplexer`
- How to perform basic CRUD operations (strings, lists, sets, hashes)
- Best practices for managing Redis connections in production

## Prerequisites

- [.NET 6+ SDK](https://dotnet.microsoft.com/en-us/download/) (or .NET Core 3.1+)
- A running Redis instance — start one locally with [Docker](https://www.docker.com/products/docker-desktop) (`docker run -p 6379:6379 redis`) or use [Redis Cloud](https://redis.io/try-free/)
- An IDE such as Visual Studio, Rider, or VS Code

## How do I install StackExchange.Redis?

There are several ways to add the package to your project.

### .NET CLI

Run the following in the directory of the `.csproj` file you want to add the package to:

```bash
dotnet add package StackExchange.Redis
```

### Package Manager Console

Run the following command from the Package Manager Console:

```bash
Install-Package StackExchange.Redis
```

### Package Reference

You can also add the package directly to your `.csproj` file:

```xml
<ItemGroup>
  <PackageReference Include="StackExchange.Redis" Version="2.2.4" />
</ItemGroup>
```

### NuGet GUI

If you're using Visual Studio and prefer a graphical interface, follow the steps outlined by [Microsoft](https://docs.microsoft.com/en-us/nuget/consume-packages/install-use-packages-visual-studio) and search for **StackExchange.Redis**.

## How do I connect to Redis from .NET?

First, import the namespace:

```csharp
using StackExchange.Redis;
```

Then initialize the [ConnectionMultiplexer](https://stackexchange.github.io/StackExchange.Redis/Basics). This is the central object for communicating with Redis. Your application should maintain a **single instance** throughout its lifetime — it is thread-safe and designed to be reused.

A typical connection string follows the format `HOST:PORT,password=PASSWORD`:

```csharp
static readonly ConnectionMultiplexer _redis =
    ConnectionMultiplexer.Connect("localhost:6379,password=secret_password");
```

Once you have a multiplexer, get a reference to the database:

```csharp
var db = _redis.GetDatabase();
```

### ConnectionMultiplexer best practices

- Create **one** `ConnectionMultiplexer` and reuse it for the lifetime of the application.
- Register for the `ConnectionFailed` and `ConnectionRestored` events to monitor connectivity.
- In ASP.NET Core, register the multiplexer as a singleton in the dependency injection container.

## How do I perform CRUD operations with C# and Redis?

### Ping the database

```csharp
db.Ping();
```

### String operations — get and set

**Set a string value:**

```csharp
db.StringSet("foo", "bar");
```

**Get a string value:**

```csharp
Console.WriteLine(db.StringGet("foo"));
```

### List operations

**Push to a list:**

```csharp
db.ListLeftPush("simple-list", 1);
```

**Pop from a list:**

```csharp
var result = db.ListRightPop("simple-list");
Console.WriteLine(result);
```

### Set operations

**Add members to sets:**

```csharp
db.SetAdd("sample-set-1", new RedisValue[]{"apple", "banana", "tangerine", "kiwi"});
db.SetAdd("sample-set-2", new RedisValue[]{"apple", "banana", "orange", "blueberries"});
```

**Compute the union of two sets:**

```csharp
var union = db.SetCombine(SetOperation.Union, "sample-set-1", "sample-set-2");
Console.WriteLine(String.Join(", ", union));
```

### Hash operations

**Add fields to a hash:**

```csharp
db.HashSet("person:1", new HashEntry[]{
    new HashEntry("first-name", "John"),
    new HashEntry("last-name", "Smith")
});
```

**Get a single field:**

```csharp
var firstName = db.HashGet("person:1", "first-name");
Console.WriteLine(firstName);
```

**Get all fields:**

```csharp
var allFields = db.HashGetAll("person:1");
Console.WriteLine(string.Join(", ", allFields));
```

## Sample .NET and Redis applications

![Rate-limiting example app built with .NET and StackExchange.Redis](/images/site-mirror/7ae9af25e26aa4caa18655bb4c6b2c92a1c8d772-1268x1106.webp)

---

![Leaderboard example app using Redis sorted sets in .NET](/images/site-mirror/5fc7616acef5cb2146d4daabcb67cf718b0e2df2-1082x942.webp)

![API caching example with ASP.NET Core and Redis](/images/site-mirror/32d2f1b47c5f579b0ba6a035e47ea12dcb3f6e53-1094x956.webp)

---

![Basic chat app using Redis Pub/Sub in .NET](/images/site-mirror/4aa7f0f031b546b3d6efa7373c1cd3becde9ecfc-1082x950.webp)

## Next steps

Now that you have StackExchange.Redis set up, explore more advanced .NET and Redis topics:

- [API Caching with ASP.NET Core and Redis](/tutorials/develop/dotnet/aspnetcore/caching/basic-api-caching/) — reduce latency and external API costs with a Redis-backed cache
- [Getting Started with Redis Streams in .NET](/tutorials/develop/dotnet/streams/stream-basics/) — use Redis Streams for message brokering and event processing
- [Redis OM .NET](/tutorials/redis-om-dotnet-getting-started/) — map C# objects to Redis hashes and JSON documents with an object mapper
- [Using C# with Redis](https://redis.io/docs/latest/develop/clients/dotnet/) — official Redis client documentation for .NET
