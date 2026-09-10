---
title: "Rate Limiting in .NET with Redis"
linkTitle: "Rate Limiting in .NET with Redis"
url: "/tutorials/rate-limiting-in-dotnet-with-redis/"
description: "Rate limiting your .NET APIs with Redis is the fastest way to protect against abuse, prevent resource starvation, and enforce usage quotas. By combining ASP.NET Core middleware with Redis's atomic..."
group: "For developers"
date: 2026-02-25
lastmod: 2026-02-26
hidden: true
mirrored: true
---

*Published 25 February 2026 · updated 26 February 2026*

Rate limiting your .NET APIs with Redis is the fastest way to protect against abuse, prevent resource starvation, and enforce usage quotas. By combining ASP.NET Core middleware with Redis's atomic Lua scripting and built-in TTL, you can add production-ready rate limiting that scales across distributed deployments with minimal latency overhead.

> **INFO**
>
> Learn how to [build all the rate limiting algorithms in Redis](/tutorials/howtos/ratelimiting/)

In this tutorial we'll explore several approaches to implement rate limiting in ASP.NET Core apps using Redis. We'll start with a basic fixed window implementation, move to a more precise sliding window approach, and finish with a fully configurable rate limiting middleware.

## What you'll learn

- How to build a **fixed window** rate limiter using Redis `INCR` and `EXPIRE` commands
- How to implement a **sliding window** rate limiter using Redis sorted sets
- How to create **configurable rate limiting middleware** that applies multiple rules across endpoints
- How to write and execute **Lua scripts** for atomic rate limiting operations with StackExchange.Redis

## What you'll build

You'll build three progressively more sophisticated rate limiters in ASP.NET Core, all backed by Redis:

1. **Fixed window limiter** — A simple counter that resets at the top of each time window, using `INCR` and `EXPIRE` in a Lua script.
2. **Sliding window limiter** — A more precise limiter that uses sorted sets to track individual requests and trims expired entries on each check.
3. **Configurable middleware** — A reusable middleware component that reads rate limit rules from `appsettings.json`, supports exact and regex path matching, and enforces multiple overlapping windows per endpoint.

Each approach builds on the previous one, so by the end you'll understand the trade-offs and be ready to pick the right strategy for your APIs.

## Fixed window vs sliding window

|                    | Fixed window                       | Sliding window                      |
| :----------------- | :--------------------------------- | :---------------------------------- |
| **Algorithm**      | Counter per time bucket            | Sorted set with rolling expiry      |
| **Accuracy**       | Can allow 2× burst at window edges | Precise per-second tracking         |
| **Redis commands** | `INCR`, `EXPIRE`                   | `ZADD`, `ZREMRANGEBYSCORE`, `ZCARD` |
| **Complexity**     | Lowest                             | Moderate                            |
| **Best for**       | Simple quotas, low-stakes limits   | Per-user API throttling             |
| **Drawback**       | Edge-of-window spikes              | Slightly more memory per key        |

## What is rate limiting?

Rate limiting entails techniques to regulate the number of requests a particular client can make against a networked service. It caps the total number and/or the frequency of requests. There are many reasons why you would want to add a rate limiter to your APIs, whether it is to prevent intentional or accidental API abuse, a rate limiter can stop the invaders at the gate. Let's think of some scenarios where a rate limiter could save your bacon:

- If you ever worked at an API-based startup, you know that to get anywhere you need a "free" tier. A free tier will get potential customers to try your service and spread the word. But without limiting the free tier users you could risk losing the few paid customers your startup has.
- Programmatic integrations with your API could have bugs. Sometimes resource starvation is not caused by a malicious attack. These FFDoS (Friendly-Fire Denial of Service) attacks happen more often than you can imagine.
- Finally, there are malicious players recruiting bots on a daily basis to make API providers' lives miserable. Being able to detect and curtail those attacks before they impact your users could mean the life of your business.

Rate limiting relies on three particular pieces of information:

1. **Who's making the request**: Identifying the source of abuse is the most important part of the equation. If the offending requests cannot be grouped and associated with a single entity you'll be fighting in the dark.
2. **What's the cost of the request**: Not all requests are created equal. For example, a request that's bound to a single account's data can likely only cause localized havoc, while a request that spans multiple accounts or broad spans of time is much more expensive.
3. **What is their allotted quota**: How many total requests and/or what's the rate of requests permitted for the user.

## Why Redis for rate limiting?

Redis is especially positioned as a platform to implement rate limiting for several reasons (see also the [comprehensive rate limiting algorithms guide](/tutorials/howtos/ratelimiting/) for a deeper look at the theory):

- **Speed**: The checks and calculations required by a rate limiting implementation will add to the total request-response times of your API. You want those operations to happen as fast as possible.
- **Centralization and distribution**: Redis can seamlessly scale your single server/instance setup to hundreds of nodes without sacrificing performance or reliability.
- **The right abstractions**: Redis provides optimized data structures to support several of the most common rate limiter implementations and with its built-in TTL (time-to-live controls) it allows for efficient management of memory. Counting things is a built-in feature in Redis and one of the many areas where Redis shines above the competition.

## Prerequisites

- [.NET 5+ SDK](https://dotnet.microsoft.com/download/dotnet/5.0) installed
- Some way of running Redis; for this tutorial we'll use [Docker Desktop](https://www.docker.com/products/docker-desktop)
- IDE for writing C#: [VS Code](https://code.visualstudio.com/download), [Visual Studio](https://visualstudio.microsoft.com/), or [Rider](https://www.jetbrains.com/rider/)

## Start Redis

Before we begin, start Redis. For this example, we'll use the [Redis docker image](https://hub.docker.com/_/redis):

```bash
docker run -dp 6379:6379 redis
```

## Fixed window rate limiting with Redis and ASP.NET Core

The simplest approach to build a rate limiter is the "fixed window" implementation in which we cap the maximum number of requests in a fixed window of time. For example, if the window size is 1 minute, we can "fix" it at the top of the minute, like 12:00-12:59, 1:00-1:59, and so forth.

The procedure to implement a fixed window rate limiter is:

1. **Identify the requester**: This might be an API key, a token, a user's name or id, or even an IP address.
2. **Find the current window**: Use the current time to find the window. For example, with 1 minute windows at 3:15 PM, the window would be labeled "3:15".
3. **Find the request count**: Look up the count under a key like `route:apiKey:timeWindow`.
4. **Increment the request count**: Increment the counter for this window+user key.
5. **Rate limit if applicable**: If the count exceeds the user's quota, deny the request; otherwise, allow it to proceed.

This simple implementation minimizes CPU and I/O utilization but comes with some limitations. It is possible to experience spikes near the edges of the window, since API users might send a burst of requests at the end of one window and the start of the next.

### Create the project

In your terminal, navigate to where you want the app to live and run:

```bash
dotnet new webapi -n FixedRateLimiter --no-https
```

Change directory to `FixedRateLimiter` and run:

```bash
dotnet add package StackExchange.Redis
```

Open the project in your IDE and in the `Controllers` folder, add an API controller called `RateLimitedController`:

```csharp
namespace FixedRateLimiter.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class RateLimitedController : ControllerBase
    {

    }
}
```

### Initialize the multiplexer

To use Redis, initialize an instance of the `ConnectionMultiplexer` from StackExchange.Redis. Go to the `ConfigureServices` method inside `Startup.cs` and add the following line:

```csharp
services.AddSingleton<IConnectionMultiplexer>(ConnectionMultiplexer.Connect("localhost"));
```

### Inject the ConnectionMultiplexer

In `RateLimitedController.cs`, inject the `ConnectionMultiplexer` into the controller and pull out an `IDatabase` object:

```csharp
private readonly IDatabase _db;
public RateLimitedController(IConnectionMultiplexer mux)
{
    _db = mux.GetDatabase();
}
```

### Add a simple route

We will add a POST request route that uses [Basic auth](https://en.wikipedia.org/wiki/Basic_access_authentication). Each request expects a header of the form `Authorization: Basic <base64encoded>` where the base64 encoded value is a string of the form `apiKey:apiSecret`. This route will parse the key out of the header and return an OK result.

```csharp
[HttpPost("simple")]
public async Task<IActionResult> Simple([FromHeader]string authorization)
{
    var encoded = string.Empty;
    if(!string.IsNullOrEmpty(authorization)) encoded = AuthenticationHeaderValue.Parse(authorization).Parameter;
    if (string.IsNullOrEmpty(encoded)) return new UnauthorizedResult();
    var apiKey = Encoding.UTF8.GetString(Convert.FromBase64String(encoded)).Split(':')[0];
    return Ok();
}
```

With that setup, run the project with `dotnet run`, and issue a POST request with apiKey `foobar` and password `password`:

```bash
curl -X POST -H "Content-Length: 0" --user "foobar:password" http://localhost:5000/api/RateLimited/simple
```

You should get a 200 OK response back.

### Fixed window Lua script

We are going to build a fixed window rate limiting script. Given the apiKey `foobar` hitting our route `api/ratelimited/simple` at 12:00:05 with a 60-second window and a limit of ten requests, we need to:

1. Format a key from our info, e.g. `route:apiKey:time-window` &mdash; in our case, `api/ratelimited/simple:foobar:12:00`
2. Increment the current value of that key
3. Set the expiration for that key to 60 seconds
4. If the current value is less than the max requests allowed, return 0 (not rate limited)
5. Otherwise, return 1 (rate limited)

The issue we need to contend with is that this rate limiting requires atomicity for all our commands. Because of this, we will run everything on the server through a [Lua script](https://redis.io/commands/eval). StackExchange.Redis contains support for a [more readable mode of scripting](https://stackexchange.github.io/StackExchange.Redis/Scripting.html) that lets you name arguments to your script:

```lua
local requests = redis.call('INCR',@key)
redis.call('EXPIRE', @key, @expiry)
if requests < tonumber(@maxRequests) then
    return 0
else
    return 1
end
```

### Loading the script

Add a new file `Scripts.cs` to the project with a static class called `Scripts`. This will contain the script string and a getter property to prepare the script for execution:

```csharp
using StackExchange.Redis;
namespace FixedRateLimiter
{
    public static class Scripts
    {
        public static LuaScript RateLimitScript => LuaScript.Prepare(RATE_LIMITER);

        private const string RATE_LIMITER = @"
            local requests = redis.call('INCR',@key)
            redis.call('EXPIRE', @key, @expiry)
            if requests < tonumber(@maxRequests) then
                return 0
            else
                return 1
            end
            ";
    }
}
```

### Executing the script

Build the key, run the script, and check the result. Add the following just ahead of the `return` in the `Simple` method:

```csharp
var script = Scripts.RateLimitScript;
var key = $"{Request.Path.Value}:{apiKey}:{DateTime.UtcNow:hh:mm}";
var res = await _db.ScriptEvaluateAsync(script, new {key = new RedisKey(key), expiry = 60, maxRequests = 10});
if ((int) res == 1)
    return new StatusCodeResult(429);
```

The complete `Simple` route should look like this:

```csharp
[HttpPost("simple")]
public async Task<IActionResult> Simple([FromHeader]string authorization)
{
    var encoded = string.Empty;
    if(!string.IsNullOrEmpty(authorization)) encoded = AuthenticationHeaderValue.Parse(authorization).Parameter;
    if (string.IsNullOrEmpty(encoded)) return new UnauthorizedResult();
    var apiKey = Encoding.UTF8.GetString(Convert.FromBase64String(encoded)).Split(':')[0];
    var script = Scripts.RateLimitScript;
    var key = $"{Request.Path.Value}:{apiKey}:{DateTime.UtcNow:hh:mm}";
    var res = await _db.ScriptEvaluateAsync(script, new {key = new RedisKey(key), expiry = 60, maxRequests = 10});
    if ((int) res == 1)
        return new StatusCodeResult(429);
    return new JsonResult(new {key});
}
```

### Test the fixed window limiter

Start the server with `dotnet run` and try running:

```bash
for n in {1..21}; do echo $(curl -s -w " HTTP %{http_code}, %{time_total} s" -X POST -H "Content-Length: 0" --user "foobar:password" http://localhost:5000/api/ratelimited/simple); sleep 0.5; done
```

You will see some requests return a 200, and at least one return a 429. How many depends on the time at which you start sending the request. The requests are time-boxed on single-minute windows, so if you transition to the next minute in the middle of the 21 requests, the counter will reset. You should expect to receive somewhere between 10 and 20 OK results and between 1 and 11 429 results:

```shell
HTTP 200, 0.002680 s
HTTP 200, 0.001535 s
HTTP 200, 0.001653 s
HTTP 200, 0.001449 s
HTTP 200, 0.001604 s
HTTP 200, 0.001423 s
HTTP 200, 0.001492 s
HTTP 200, 0.001449 s
HTTP 200, 0.001551 s
{"status":429,"traceId":"00-16e9da63..."} HTTP 429, 0.001803 s
{"status":429,"traceId":"00-3d2e4e8a..."} HTTP 429, 0.001521 s
```

## Sliding window rate limiting with Redis and ASP.NET Core

### What is a sliding window rate limiter?

A sliding window rate limiter, unlike a fixed window, restricts requests for a discrete window prior to the current request under evaluation. For example, if you have a 10 req/minute rate limiter using a fixed window, you could encounter a case where the limiter allows 20 requests within a single minute: if the first 10 requests arrive at the end of one window and the next 10 at the start of the next, both buckets have capacity. A sliding window rate limiter considers all requests within the last 60 seconds regardless of window boundaries, so only 10 would make it through.

Using sorted sets and Lua scripts, implementing a sliding window rate limiter in Redis is straightforward.

### Create the project

In your terminal, run:

```bash
dotnet new webapi -n SlidingWindowRateLimiter --no-https
```

Change directory to `SlidingWindowRateLimiter` and run:

```bash
dotnet add package StackExchange.Redis
```

Set up the controller, multiplexer, and route the same way as the fixed window example:

```csharp
namespace SlidingWindowRateLimiter.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class RateLimitedController : ControllerBase
    {
        private readonly IDatabase _db;
        public RateLimitedController(IConnectionMultiplexer mux)
        {
            _db = mux.GetDatabase();
        }

        [HttpPost]
        [HttpGet]
        [Route("sliding")]
        public async Task<IActionResult> Sliding([FromHeader]string authorization)
        {
            var encoded = string.Empty;
            if(!string.IsNullOrEmpty(authorization)) encoded = AuthenticationHeaderValue.Parse(authorization).Parameter;
            if (string.IsNullOrEmpty(encoded)) return new UnauthorizedResult();
            var apiKey = Encoding.UTF8.GetString(Convert.FromBase64String(encoded)).Split(':')[0];
            return Ok();
        }
    }
}
```

Don't forget to register the `ConnectionMultiplexer` in `Startup.cs`:

```csharp
services.AddSingleton<IConnectionMultiplexer>(ConnectionMultiplexer.Connect("localhost"));
```

### Sliding window Lua script

To implement this pattern we will:

1. Create a key of the format `route:apiKey` that maps to a sorted set in Redis
2. Check the current time, and remove entries that fall outside the window
3. Check the cardinality of the sorted set
4. If the cardinality is less than our limit, add a new member with a score of the current time in seconds and a member value of the current time in microseconds, then set the expiration and return 0
5. If the cardinality is greater than or equal to our limit, return 1

Everything needs to happen atomically, which makes this a perfect place to use a Lua script. Using the StackExchange.Redis script preparation engine:

```lua
local current_time = redis.call('TIME')
local trim_time = tonumber(current_time[1]) - @window
redis.call('ZREMRANGEBYSCORE', @key, 0, trim_time)
local request_count = redis.call('ZCARD',@key)

if request_count < tonumber(@max_requests) then
    redis.call('ZADD', @key, current_time[1], current_time[1] .. current_time[2])
    redis.call('EXPIRE', @key, @window)
    return 0
end
return 1
```

Create a `Scripts.cs` file to hold this script:

```csharp
using StackExchange.Redis;

namespace SlidingWindowRateLimiter
{
    public static class Scripts
    {
        public static LuaScript SlidingRateLimiterScript => LuaScript.Prepare(SlidingRateLimiter);
        private const string SlidingRateLimiter = @"
            local current_time = redis.call('TIME')
            local trim_time = tonumber(current_time[1]) - @window
            redis.call('ZREMRANGEBYSCORE', @key, 0, trim_time)
            local request_count = redis.call('ZCARD',@key)

            if request_count < tonumber(@max_requests) then
                redis.call('ZADD', @key, current_time[1], current_time[1] .. current_time[2])
                redis.call('EXPIRE', @key, @window)
                return 0
            end
            return 1
            ";
    }
}
```

### Update the controller

Back in the `Sliding` method, replace the `return` statement with the rate limiting check:

```csharp
[HttpPost]
[HttpGet]
[Route("sliding")]
public async Task<IActionResult> Sliding([FromHeader] string authorization)
{
    var encoded = string.Empty;
    if(!string.IsNullOrEmpty(authorization)) encoded = AuthenticationHeaderValue.Parse(authorization).Parameter;
    if (string.IsNullOrEmpty(encoded)) return new UnauthorizedResult();
    var apiKey = Encoding.UTF8.GetString(Convert.FromBase64String(encoded)).Split(':')[0];
    var limited = ((int) await _db.ScriptEvaluateAsync(Scripts.SlidingRateLimiterScript,
        new {key = new RedisKey($"{Request.Path}:{apiKey}"), window = 30, max_requests = 10})) == 1;
    return limited ? new StatusCodeResult(429) : Ok();
}
```

### Test the sliding window limiter

Start the server with `dotnet run` and try:

```bash
for n in {1..20}; do echo $(curl -s -w " HTTP %{http_code}, %{time_total} s" -X POST -H "Content-Length: 0" --user "foobar:password" http://localhost:5000/api/ratelimited/sliding); sleep 0.5; done
```

You will see the first 10 requests return a 200, and the remaining 10 return a 429. If you wait and run the command again you may see every other request go through, because the window slides every second and only the previous 30 seconds of requests are considered:

```bash
HTTP 200, 0.081806 s
HTTP 200, 0.003170 s
HTTP 200, 0.002217 s
HTTP 200, 0.001632 s
HTTP 200, 0.001508 s
HTTP 200, 0.001928 s
HTTP 200, 0.001647 s
HTTP 200, 0.001656 s
HTTP 200, 0.001699 s
HTTP 200, 0.001667 s
{"status":429,"traceId":"00-4af32d65..."} HTTP 429, 0.012612 s
{"status":429,"traceId":"00-7b24da24..."} HTTP 429, 0.001688 s
```

## Configurable rate limiting middleware

Let's consider the case where we have multiple endpoints to rate limit. It doesn't make sense to embed rate-limiting logic in each route. Instead, we can build middleware that intercepts requests and checks whether the request is rate-limited before forwarding it to the appropriate endpoint. With some configuration work, we can make this middleware handle a configurable set of limits.

### Create the project

```bash
dotnet new webapi -n RateLimitingMiddleware --no-https
```

Change directory to `RateLimitingMiddleware` and run:

```bash
dotnet add package StackExchange.Redis
```

### Create the configuration object

We'll define configuration objects of the following form in our application configuration:

```json
{
    "RedisRateLimits": [
        {
            "Path": "/api/ratelimited/limited",
            "Window": "30s",
            "MaxRequests": 5
        },
        {
            "PathRegex": "/api/*",
            "Window": "1d",
            "MaxRequests": 1000
        }
    ]
}
```

The parameters are:

| **Parameter Name** | **Description**                                                                                     |
| :----------------- | :-------------------------------------------------------------------------------------------------- |
| Path               | Literal path to be rate-limited; if the path matches completely, it will trigger a rate limit check |
| PathRegex          | Path regex to be rate-limited; if path matches, it will trigger a rate limit check                  |
| Window             | The sliding window to rate limit on, matching the pattern `([0-9]+(s\|m\|d\|h))`                    |
| MaxRequests        | The maximum number of requests allowable over the period                                            |

### Build the config object

Create a new class called `RateLimitRule` with the logic for rule matching and time parsing:

```csharp
public class RateLimitRule
{
    private static readonly Regex TimePattern = new ("([0-9]+(s|m|d|h))");

    private enum TimeUnit
    {
        s = 1,
        m = 60,
        h = 3600,
        d = 86400
    }

    private static int ParseTime(string timeStr)
    {
        var match = TimePattern.Match(timeStr);
        if (string.IsNullOrEmpty(match.Value))
            throw new ArgumentException("Rate limit window was not provided or was not " +
                                        "properly formatted, must be of the form ([0-9]+(s|m|d|h))");
        var unit = Enum.Parse<TimeUnit>(match.Value.Last().ToString());
        var num = int.Parse(match.Value.Substring(0, match.Value.Length - 1));
        return num * (int) unit;
    }

    public string Path { get; set; }
    public string PathRegex { get; set; }
    public string Window { get; set; }
    public int MaxRequests { get; set; }
    internal int _windowSeconds = 0;
    internal string PathKey => string.IsNullOrEmpty(Path) ? Path : PathRegex;
    internal int WindowSeconds
    {
        get
        {
            if (_windowSeconds < 1)
            {
                _windowSeconds = ParseTime(Window);
            }
            return _windowSeconds;
        }
    }

    public bool MatchPath(string path)
    {
        if (!string.IsNullOrEmpty(Path))
        {
            return path.Equals(Path, StringComparison.InvariantCultureIgnoreCase);
        }
        if (!string.IsNullOrEmpty(PathRegex))
        {
            return Regex.IsMatch(path, PathRegex);
        }
        return false;
    }
}
```

### Writing the Lua script

We need a Lua script that considers all the rules applicable to a particular user on a specific endpoint. We'll use sorted sets to check the rate limits for each rule and user. On each request, for each applicable rule, it will:

1. Check the current time
2. Trim off entries that fall outside the window
3. Check if another request violates the rule &mdash; if so, return 1
4. For each applicable rule, add a new entry to the sorted set with the score of the current time in seconds and a member name of the current time in microseconds
5. Return 0

```lua
local current_time = redis.call('TIME')
local num_windows = ARGV[1]
for i=2, num_windows*2, 2 do
    local window = ARGV[i]
    local max_requests = ARGV[i+1]
    local curr_key = KEYS[i/2]
    local trim_time = tonumber(current_time[1]) - window
    redis.call('ZREMRANGEBYSCORE', curr_key, 0, trim_time)
    local request_count = redis.call('ZCARD',curr_key)
    if request_count >= tonumber(max_requests) then
        return 1
    end
end
for i=2, num_windows*2, 2 do
    local curr_key = KEYS[i/2]
    local window = ARGV[i]
    redis.call('ZADD', curr_key, current_time[1], current_time[1] .. current_time[2])
    redis.call('EXPIRE', curr_key, window)
end
return 0
```

This script has an undetermined number of arguments and keys ahead of time. As such, it's important to make sure that all the keys are on the same shard, so when we build the keys (of the form `path_pattern:apiKey:window_size_seconds`) we surround the common part of the key `apiKey` with braces: `{apiKey}`.

### Build the middleware

Add a new file `SlidingWindowRateLimiter.cs` with two classes:

```csharp
public static class SlidingWindowRateLimiterExtensions
{
    public static void UseSlidingWindowRateLimiter(this IApplicationBuilder builder)
    {
        builder.UseMiddleware<SlidingWindowRateLimiter>();
    }
}
```

In the `SlidingWindowRateLimiter` class, add the script and constructor:

```csharp
public class SlidingWindowRateLimiter
{
    private const string SlidingRateLimiterScript = @"
        local current_time = redis.call('TIME')
        local num_windows = ARGV[1]
        for i=2, num_windows*2, 2 do
            local window = ARGV[i]
            local max_requests = ARGV[i+1]
            local curr_key = KEYS[i/2]
            local trim_time = tonumber(current_time[1]) - window
            redis.call('ZREMRANGEBYSCORE', curr_key, 0, trim_time)
            local request_count = redis.call('ZCARD',curr_key)
            if request_count >= tonumber(max_requests) then
                return 1
            end
        end
        for i=2, num_windows*2, 2 do
            local curr_key = KEYS[i/2]
            local window = ARGV[i]
            redis.call('ZADD', curr_key, current_time[1], current_time[1] .. current_time[2])
            redis.call('EXPIRE', curr_key, window)
        end
        return 0
        ";

    private readonly IDatabase _db;
    private readonly IConfiguration _config;
    private readonly RequestDelegate _next;

    public SlidingWindowRateLimiter(RequestDelegate next, IConnectionMultiplexer muxer, IConfiguration config)
    {
        _db = muxer.GetDatabase();
        _config = config;
        _next = next;
    }
}
```

#### Extract the API key

We use [Basic auth](https://en.wikipedia.org/wiki/Basic_access_authentication), so we'll extract the username from the Basic auth header as the API key:

```csharp
private static string GetApiKey(HttpContext context)
{
    var encoded = string.Empty;
    var auth = context.Request.Headers["Authorization"];
    if (!string.IsNullOrEmpty(auth)) encoded = AuthenticationHeaderValue.Parse(auth).Parameter;
    if (string.IsNullOrEmpty(encoded)) return encoded;
    return Encoding.UTF8.GetString(Convert.FromBase64String(encoded)).Split(':')[0];
}
```

#### Extract applicable rules

Pull out the `RedisRateLimits` configuration section, filter to rules matching the current path, group by window size and path key, and take the most restrictive rule for each group:

```csharp
public IEnumerable<RateLimitRule> GetApplicableRules(HttpContext context)
{
    var limits = _config.GetSection("RedisRateLimits").Get<RateLimitRule[]>();
    var applicableRules = limits
        .Where(x => x.MatchPath(context.Request.Path))
        .OrderBy(x => x.MaxRequests)
        .GroupBy(x => new{x.PathKey, x.WindowSeconds})
        .Select(x=>x.First());
    return applicableRules;
}
```

#### Check limitation

Build the keys and arguments for the Lua script, evaluate it, and check the result:

```csharp
private async Task<bool> IsLimited(IEnumerable<RateLimitRule> rules, string apiKey)
{
    var keys = rules.Select(x => new RedisKey($"{x.PathKey}:{{{apiKey}}}:{x.WindowSeconds}")).ToArray();
    var args = new List<RedisValue>{rules.Count()};
    foreach (var rule in rules)
    {
        args.Add(rule.WindowSeconds);
        args.Add(rule.MaxRequests);
    }
    return (int) await _db.ScriptEvaluateAsync(SlidingRateLimiterScript, keys, args.ToArray()) == 1;
}
```

#### Block or allow

In the `InvokeAsync` method, glue everything together. Parse the API key, check the rate limits, and either throttle or proceed:

```csharp
public async Task InvokeAsync(HttpContext httpContext)
{
    var apiKey = GetApiKey(httpContext);
    if (string.IsNullOrEmpty(apiKey))
    {
        httpContext.Response.StatusCode = 401;
        return;
    }
    var applicableRules = GetApplicableRules(httpContext);
    var limited = await IsLimited(applicableRules, apiKey);
    if (limited)
    {
        httpContext.Response.StatusCode = 429;
        return;
    }
    await _next(httpContext);
}
```

### Build the controller

Under the Controllers folder, add a `RateLimitedController` with two routes:

```csharp
[ApiController]
[Route("api/[controller]")]
public class RateLimitedController : ControllerBase
{
    [HttpGet]
    [HttpPost]
    [Route("limited")]
    public async Task<IActionResult> Limited()
    {
        return new JsonResult(new {Limited = false});
    }

    [HttpGet]
    [HttpPost]
    [Route("indirectly-limited")]
    public async Task<IActionResult> IndirectlyLimited()
    {
        return new JsonResult(new {NeverLimited = true});
    }
}
```

### Add middleware to the app

Open `Startup.cs`. In the `ConfigureServices` method, add:

```csharp
services.AddSingleton<IConnectionMultiplexer>(ConnectionMultiplexer.Connect("localhost"));
```

In the `Configure` method, add:

```csharp
app.UseSlidingWindowRateLimiter();
```

### Configure the rate limits

In `appsettings.json` or `appsettings.Development.json`, add:

```json
"RedisRateLimits":[
    {
      "Path":"/api/RateLimited/limited",
      "Window":"30s",
      "MaxRequests": 5
    },
    {
      "PathRegex":"^/api/*",
      "Window":"1h",
      "MaxRequests": 50
    }
]
```

### Test the middleware

Run `dotnet run` and hit the endpoints. First, test the directly limited endpoint:

```bash
for n in {1..7}; do echo $(curl -s -w " HTTP %{http_code}, %{time_total} s" -X POST -H "Content-Length: 0" --user "foobar:password" http://localhost:5000/api/ratelimited/limited); sleep 0.5; done
```

This will send seven requests, two of which will be rejected. After that, test the indirectly limited endpoint:

```bash
for n in {1..47}; do echo $(curl -s -w " HTTP %{http_code}, %{time_total} s" -X POST -H "Content-Length: 0" --user "foobar:password" http://localhost:5000/api/ratelimited/indirectly-limited); sleep 0.5; done
```

It should reject another two requests as throttled, since the `/api/*` regex rule applies to both endpoints and the earlier requests against `/limited` count toward the hourly quota.

## Next steps

Now that you have rate limiting working in .NET with Redis, here are some directions to explore:

- **Compare all rate limiting algorithms** — The [Build 5 Rate Limiters with Redis](/tutorials/howtos/ratelimiting/) tutorial covers fixed window, sliding window, token bucket, and leaky bucket algorithms with detailed trade-off analysis.
- **Rate limiting in Java** — If your team also runs Java services, see [Rate Limiting in Java with Redis](/tutorials/rate-limiting-in-java-spring-with-redis/) for a Spring-based implementation.
- **Add response headers** — Return `X-RateLimit-Remaining`, `X-RateLimit-Limit`, and `Retry-After` headers so clients can self-throttle.
- **Distributed deployment** — Move from a single Redis instance to Redis Cluster and ensure your hash tags (`{apiKey}`) route related keys to the same shard.
- **Dynamic rate limits** — Store per-user or per-tier limits in Redis hashes and load them dynamically in the middleware instead of using static configuration.

## Resources

- [Fixed window rate limiter source code](https://github.com/redis-developer/fixed-rate-limiter-aspnet-core)
- [Sliding window rate limiter source code](https://github.com/redis-developer/sliding-window-rate-limiter-aspnet)
- [Rate limiting middleware source code](https://github.com/redis-developer/rate-limiting-middleware-aspnetcore)
