---
title: "P95 latency: What it is, why averages lie & how to reduce it"
linkTitle: "P95 latency: What it is, why averages lie & how to reduce it"
url: "/blog/p95-latency/"
description: "Average latency is easy to measure and easy to misread. A healthy-looking mean can coexist with a significant share of requests that are far slower, and those are the ones users actually notice...."
date: 2026-04-20
blogCategories:
- "Tech DE"
authors:
- "Jim Allen Wallace"
lastmod: 2026-04-23
hidden: true
---

*By Jim Allen Wallace, Sr. Product Marketing Manager · Published 20 April 2026 · updated 23 April 2026*

![Redis](/images/blog/adf78da87506da26bce2baf0d7bf013adc22cf40-1200x628.webp)

Average latency is easy to measure and easy to misread. A healthy-looking mean can coexist with a significant share of requests that are far slower, and those are the ones users actually notice. P95 cuts through that. It's the threshold below which 95% of your requests complete, which means the slowest 5% show up instead of disappearing into the average. At any real traffic volume, that 5% is enough users to care about.

P95 is one of a family of percentile metrics built to surface exactly this. The slow outliers tend to cluster around specific causes: connection pool exhaustion, garbage collection pauses, and upstream dependency slowdowns. At scale, those are the requests where users feel the difference between a fast app and a slow one.

This guide covers what p95 latency is, why it matters more than averages, what causes it to spike, and how to measure and reduce it in production systems.

## What p95 latency means & how it's calculated

P95 belongs to a family of metrics called tail latency: high-percentile measurements (p95, p99, p99.9) that capture the slow outlier requests sitting at the tail of your latency distribution.

The calculation sorts all requests in a time window by duration and finds the value at the 95th percentile position. Everything above it is the slow tail.

In practice, production systems don't sort millions of raw measurements per window. They use bucketed histograms that group latency measurements into ranges and interpolate from there. The result is an approximation, but close enough for alerting and service-level objective (SLO) tracking.

One constraint worth knowing: you can't average percentiles across instances. If 10 servers each report their own p95, the mean of those values is not a valid fleet-wide p95. You need to aggregate the underlying histogram data first, then recompute.

## Why averages lie about your users' experience

That definition matters because of what it exposes that averages don't. Averages mask slow requests because outliers get diluted in the sum. A latency spike contributes to the total but stays rare enough to fade in aggregate, which is exactly why p95 exists. It catches the degradation that averages can't.

This gets concrete at scale. A service that averages 100ms latency can still have a meaningful share of requests taking several seconds. At any significant request rate, that's a real problem for real users, invisible behind a healthy-looking average.

Production service-level objectives (SLOs) show the same failure mode. For example, one service set its objective based on a [synthetic well-behaved client](https://sre.google/sre-book/service-level-objectives/), but the worst 5% of requests were 5–10× slower than the rest. Real users experienced degradation the SLO didn't catch. Separate [latency measurements](https://www.usenix.org/system/files/conference/nsdi15/nsdi15-paper-suresh.pdf) confirmed the gap: p95 sat materially above median. That's the practical reason tail metrics matter. Median tells you what a typical request looked like, while p95 shows whether a meaningful slice of users had a much worse experience.

## Fan-out amplification: how tail latency compounds

Tail latency gets worse when a single user request depends on multiple backend services completing in parallel. Even if each individual service is slow only rarely, the probability that at least one of them is slow on any given request compounds quickly with the number of services involved.

The practical result is that a backend p99 that looks acceptable in isolation can become a common user-visible problem at the frontend. [Research from Google](https://research.google/pubs/the-tail-at-scale/) found that a request with a p99 of 10ms ballooned to 140ms under real fan-out conditions, a 14× amplification. That's not a backend problem anymore. That's what users feel.

This is why percentile metrics matter more than averages in distributed systems. Your backend tail becomes your frontend's typical experience once fan-out is in the picture.

## P50 vs p95 vs p99: choosing the right percentile

Because fan-out changes what users actually feel, the next step is choosing which percentile matches the problem you're trying to catch.

- **P50 (median)** shows the typical single-request experience. It's useful for understanding baseline performance but systematically understates session-level pain. If each request independently has a 99% chance of completing below a threshold, the probability that all 10 requests in a session are fast drops to about 90%.
- **P90** catches roughly 1 in 10 slower requests and can be one baseline for production alerting on API gateway latency.
- **P95** is a widely used SLO threshold. It catches real contention pathologies with enough statistical sample to be actionable at moderate request rates.
- **P99** exposes architectural problems p95 can hide. At 5,000 requests per second, p99 means about 50 requests per second fall into the slowest 1%, which is often enough volume to reveal issues like rare lock contention or intermittent dependency timeouts that p95 smooths over.
- **P99.9 and beyond** catches extreme tail events, but optimizing past the 99.9th percentile typically hits diminishing returns relative to the engineering effort required.

A useful approach is [dual-threshold SLOs](https://sre.google/workbook/implementing-slos/) that capture both typical and tail experience. A pairing like p50 for baseline responsiveness plus p95 or p99 for user-visible pain gives you a better read on the system than either number alone.

In practice, p95 is often the default starting point because it balances sensitivity to bad outliers with enough sample volume to alert on reliably. The right percentile depends on how much tail pain your users actually feel and how much fan-out your system introduces.

## Common causes of p95 spikes

Knowing which percentile to watch is only useful if you know what drives it up. P95 spikes rarely come from every request getting a little slower. They usually come from a smaller slice of requests hitting a queue, pause, or dependency slowdown that gets lost in average latency.

- **Connection pool exhaustion** slows only the requests that arrive when the pool is saturated. Most requests may still look fine, while the unlucky ones wait long enough to drag up p95.
- **Garbage collection pauses** create bursts of latency rather than a steady shift in baseline performance. That makes them easy to miss in averages and obvious in tail metrics.
- **Upstream dependency slowdowns** often appear first in p95 because only some calls hit the slow path. If your service depends on another service, your tail often inherits theirs.
- **Thread pool saturation** shows up the same way. Once workers are busy, queued requests wait longer even if the median request still looks healthy.
- **Fan-out across backends** amplifies small tail problems. A dependency that is only occasionally slow can become a frequent user-visible issue when one frontend request needs many backend calls to finish.

The practical takeaway: p95 is often less about raw compute speed and more about contention, coordination, and shared resources. When p95 rises while p50 stays mostly flat, that's a strong hint that a subset of requests is getting stuck behind one of these bottlenecks instead of the whole system getting uniformly slower.

## How to reduce p95 latency

Once you've identified the bottleneck, the fixes tend to be more targeted than you'd expect. Because p95 spikes come from a subset of requests rather than every request getting uniformly slower, you're usually pulling on one lever, not rebuilding your stack.

Before any of the approaches below are useful, you need to be measuring the right things. If you're not already emitting p95 and p99 as discrete metrics alongside averages in your observability stack, that's where to start.

A few approaches consistently move the needle:

- **Eliminate data layer variability first.** Disk-based reads produce tail spikes whenever input/output (I/O) queues back up or a cache miss forces a full query. [In-memory data access](https://redis.io/solutions/caching/) removes that variable from the equation. If your p95 is consistently higher than your p50 during read-heavy traffic, the data layer is a likely contributor.
- **Right-size your connection pools.** Pool exhaustion is a pure p95 problem: most requests sail through, and the unlucky ones wait. Matching pool size to actual peak concurrency flattens the tail without meaningfully affecting average latency.
- **Set hard timeouts on upstream dependencies.** A slow dependency inflates your tail every time it's called. Hard timeouts let you fail fast and retry rather than letting one sluggish call drag p95 upward. The timeout threshold should be informed by your actual p99 for that dependency under normal conditions.
- **Use hedged requests for read fan-out.** Sending a duplicate request to a second instance after a short delay and using whichever responds first reduces tail exposure in exchange for some additional backend load. This is most practical in read-heavy, idempotent call patterns.

None of these fixes require a full stack overhaul. P95 spikes are usually localized, and the right instrumentation will tell you which lever to pull.

## Tail latency is where performance work starts

With the right percentile tracked and the causes understood, p95 becomes a clear signal rather than a number you check after users complain. It shows the slow requests that average latency smooths over and points toward the specific bottlenecks causing them.

That makes p95 useful as both a debugging tool and a product health signal. It helps you spot requests affected by contention, pauses, and dependency slowdowns before they disappear into a healthy-looking average.

Tail latency matters at every layer, not just at the app edge, but in the data infrastructure behind it. A slow data layer is a common p95 contributor, and it's one of the most fixable: in-memory data access removes the disk I/O variability that can cause p95 spikes under load. Redis is built for that layer. If you're working on latency-sensitive infrastructure, [try Redis free](https://redis.io/try-free/) or [talk to our team](https://redis.io/meeting/).
