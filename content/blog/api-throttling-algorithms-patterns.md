---
title: "API throttling: Algorithms, patterns & mistakes to avoid"
linkTitle: "API throttling: Algorithms, patterns & mistakes to avoid"
url: "/blog/api-throttling-algorithms-patterns/"
description: "Most teams add rate limiting once and never revisit it. They pick a fixed window counter because it's simple, deploy it with local counters, and move on. Then a misbehaving client gets through at..."
date: 2026-04-14
blogCategories:
- "Tech DE"
authors:
- "Jim Allen Wallace"
lastmod: 2026-04-15
hidden: true
---

*By Jim Allen Wallace, Sr. Product Marketing Manager · Published 14 April 2026 · updated 15 April 2026*

![API throttling: Algorithms, patterns & mistakes to avoid](/images/site-mirror/f1e68e751263ded65e5ea02e4a1636cb80596728-2400x1256.webp)

Most teams add rate limiting once and never revisit it. They pick a fixed window counter because it's simple, deploy it with local counters, and move on. Then a misbehaving client gets through at 5x the configured threshold and the post-mortem reveals the rate limiter was never actually doing what they thought. This guide covers five rate limiting algorithms and their trade-offs, deployment patterns, and the [common mistakes](https://www.infoq.com/articles/seven-uservices-antipatterns/) that let traffic through anyway.

## What API throttling & rate limiting actually mean

Before getting into algorithms, it helps to separate two terms teams often blur together. Rate limiting restricts how many requests a client can make within a specific time window. Exceed the threshold and the API rejects additional requests, typically with an [HTTP 429 response](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/429). Limits can be scoped per IP address, per user, per API key, or per authenticated application.

Throttling is the broader flow-control mechanism applied when demand exceeds capacity. Where rate limiting usually rejects excess requests at a hard count ceiling, throttling controls how the system responds. It may slow, queue, or delay requests rather than immediately rejecting them.

In practice, the terms overlap. Some gateway throttling models cover both burst limits and steady-state requests-per-second limits under a unified policy. The distinction matters most when you're designing client retry behavior and gateway policy architecture.

APIs often need both mechanisms for three reasons: protection against abuse and distributed denial-of-service (DDoS) floods, prevention of resource exhaustion from runaway scripts or misconfigured clients, and consumer fairness.

## Rate limiting algorithms

The algorithm you pick shapes your memory footprint, accuracy under load, and burst tolerance — and it determines what your backing store needs to do atomically.

### Fixed window counter

A counter increments for each request within a fixed window. When the window expires, the counter resets. Time complexity is [O(1) for INCR](https://redis.io/docs/latest/commands/incr/), and you only need a single INCR operation.

The catch: a client can send their full quota right before a window boundary and again right after, effectively bursting above quota through the limiter. This boundary-burst problem makes fixed windows a weaker fit for resource-intensive endpoints, though they can work well for billing and quota enforcement where discrete accounting periods are required.

### Sliding window log

Every request timestamp gets stored in a sorted set log. On each new request, you remove expired timestamps, count what's left, and reject if the count exceeds the limit. In the algorithmic model, this is designed to avoid the boundary-burst problem by continuously evaluating the window relative to the current moment.

The trade-off is memory. Space complexity is O(N) per identity, where N equals requests within the window. It's best suited for security-sensitive endpoints like auth flows where approximation error is unacceptable.

### Sliding window counter

For many high-traffic APIs, this is a practical choice. It approximates a rolling window using just two fixed-window counters plus a weighted interpolation: the previous window's count is multiplied by its overlap fraction with the current rolling window, then added to the current window's count.

One implementation requires only GET, SET, and INCR, making it viable for distributed deployments without Lua scripts.

### Token bucket

Each identity maintains a bucket with a maximum capacity and a refill rate. Tokens accumulate continuously up to the bucket's ceiling. Each request costs one or more tokens. If enough tokens are available, the request is allowed and tokens are deducted. Otherwise, it's rejected.

The key feature is burst tolerance by design. Accumulated tokens absorb legitimate traffic spikes without triggering rate-limit responses.

### Leaky bucket

Requests enter a [request processing queue](https://redis.io/glossary/redis-queue/) and are processed at a fixed, constant output rate. If the queue fills up, incoming requests are dropped. Where token bucket shapes input rate, accepting bursts up to capacity, leaky bucket shapes output rate, enforcing a more uniform request cadence regardless of how bursty the input is. That makes it useful when protecting backend services that need smoother request arrival patterns.

### Probabilistic counting

At extreme scale, with millions of distinct keys tracked simultaneously, exact per-key counters can become memory-prohibitive. Count-Min Sketch provides approximate counts with bounded error at a fraction of the memory cost.

### The atomicity constraint

The algorithm you land on also determines what your backing store needs to do atomically.

Lua scripts [execute atomically](https://redis.io/docs/latest/develop/programmability/eval-intro/) on the Redis server, which helps avoid interleaved reads and writes during script execution. This matters for algorithms like token bucket and leaky bucket that require read-modify-write operations a simple INCR can't handle. Redis' STRING, SORTED SET, and HASH data structures cover the storage needs of these algorithms, and built-in key expiration handles window cleanup without manual management. In [single-instance mixed workloads](/blog/redis-82-ga/), Redis 8.2 reported 1 million operations per second.

## Distributed throttling patterns

Once algorithm choice is set, the next question is where decisions get made. Several patterns show up in production, and the trade-offs usually come down to consistency requirements, per-request latency budget, and how much complexity you're willing to manage.

### Centralized with a shared store

All rate-limit decisions route through a single shared in-memory data store. Every API node increments the same counter atomically. In this design, you get a consistent shared view, but you also add a synchronous round-trip to every request.

### PoP-local with eventual consistency

If a centralized design adds too much coordination cost, teams often move decisions closer to the edge. Instead of routing all updates to a single global store, you maintain local counters per node or per Point of Presence (PoP), with periodic synchronization. Nodes accept that their view of global request counts may be temporarily incomplete.

The trade-off is temporary over-admission during propagation delay—a client can potentially exploit this by distributing requests across multiple nodes simultaneously.

### Local + global hybrid

Between those two extremes sits a hybrid model. It's the highest-complexity pattern in this list, but it can offer a strong balance between latency and accuracy.

### API gateway-level throttling

Another way to simplify enforcement is to move it up the stack. API gateways can centralize rate limiting at the network edge, before requests hit your application services. This offloads enforcement from application code and gives you a unified policy control plane. The constraint: gateway-level enforcement only has access to HTTP request attributes, not application-layer business logic. Premium-user limits need to be encoded in verifiable request attributes like JSON Web Token (JWT) claims.

## Anti-patterns that cause real damage

Getting those patterns wrong can make outages, retry storms, and unfair quota distribution actively worse. These are the most common mistakes.

### Decentralized throttling without coordination

When each service in a [microservices architecture](https://redis.io/glossary/microservices/) implements its own throttling independently, limits aren't consistent across your API surface — a client rejected by one service can still consume full quota through another. A related but distinct failure shows up at the instance level within a single service.

### Local counters on multi-instance deployments

Rate-limit counters in each server's local memory mean the effective limit becomes your configured limit multiplied by the number of running instances. A distributed client can exploit this to exceed your intended threshold before any single instance rejects.

### Retrying without backoff or jitter

When clients retry immediately at full rate after getting throttled, they can [block recovery efforts](https://learn.microsoft.com/en-us/azure/architecture/antipatterns/retry-storm/) and intensify the original problem. Synchronized retries from multiple clients can turn a brief overload into a sustained outage.

### Rate limiting only by request count

Requests-per-second limits treat all requests as equivalent, but endpoints vary significantly in cost. A client that stays within the request count can still overwhelm the system if those requests hit expensive operations.

### Not telling clients what's happening

When a rate-limited API returns a generic 500 error, clients can't distinguish a rate limit from an infrastructure failure. A client that reads a 500 as a transient error [retries immediately](https://www.infoq.com/articles/aws-lambda-avoid-throttling/), compounding the original overload rather than backing off.

### No per-consumer isolation

A single global rate limit shared across all consumers can mean one high-volume client [drains shared quota](https://learn.microsoft.com/en-us/azure/architecture/antipatterns/noisy-neighbor/noisy-neighbor) for everyone else. The most active consumers effectively set the ceiling for the rest of the platform.

## Rate limiting is infrastructure — Redis is built for it

If there's one takeaway here, it's that rate limiting is a design decision, not a patch. The algorithm you pick determines which failure modes you're exposed to. The deployment pattern determines whether your limits hold under distribution. And the anti-patterns—decentralized enforcement, local-only counters, and missing client communication—can make rate limiting actively harmful.

All three of those decisions come down to counting, timing, and atomicity. Redis' data structures and Lua scripting cover the implementation side; built-in clustering and key expiration handle the distributed deployment side.

[Try Redis free](https://redis.io/try-free/) to build rate limiting into your API infrastructure, or [talk to our team](https://redis.io/meeting/) about distributed deployments.

## FAQ

### What's the difference between throttling & rate limiting?

Rate limiting rejects at a hard count ceiling. Throttling is broader — it can also queue, delay, or degrade requests rather than rejecting them outright. The distinction matters most when designing client retry logic: a queued delay needs different handling than a hard rejection with a Retry-After header.

### Which rate limiting algorithm should you start with?

That depends on what matters most in your system. Fixed windows are simple, sliding windows improve fairness, token buckets handle bursts well, and leaky buckets help smooth traffic before it reaches sensitive backends.

### Why does atomicity matter in distributed rate limiting?

Distributed rate limiting often depends on read-modify-write operations. Without atomic execution, concurrent requests can interleave updates and produce incorrect counts or token state.

### When do local counters break down?

As soon as you have more than one app instance. Each instance enforces the limit independently, so a client that spreads requests across instances can exceed your intended threshold by a factor of your instance count before any single instance rejects. If clients are hitting limits at a rate significantly higher than your configured threshold, and you're running multiple instances, this is a likely cause.

### Why return HTTP 429 instead of a generic error?

A 429 signals a recoverable, expected condition — the client should back off and retry later. A generic 500 looks like an infrastructure failure and triggers immediate retry logic, which compounds the original overload rather than relieving it.
