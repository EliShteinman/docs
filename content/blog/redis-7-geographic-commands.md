---
title: "Speeding Up Geographic Commands in Redis 7"
linkTitle: "Speeding Up Geographic Commands in Redis 7"
url: "/blog/redis-7-geographic-commands/"
description: "Intel and Redis have made significant performance enhancements! Here we share the optimization techniques we used to evaluate and maximize Redis GEO command performance, such as reducing wasteful..."
date: 2023-02-21
blogCategories:
- "Company"
- "Guest Blogs"
- "Tech"
authors:
- "Filipe Oliveira"
lastmod: 2025-03-27
hidden: true
---

*By Filipe Oliveira, Performance Engineer · Published 21 February 2023 · updated 27 March 2025*

![Blog tile image](/images/blog/506c3acf7600ef6af7ee21c54908511b708bf001-772x550.webp)

**Intel and Redis have made significant performance enhancements! Here we share the optimization techniques we used to evaluate and maximize Redis GEO command performance, such as reducing wasteful computation and simplifying algorithms.**

All the work has paid off. Altogether, we improved Redis performance by up to four times the previous speed!

Redis’s GEO commands (formally [geospatial indices](/glossary/geospatial-indexing/)) are a powerful tool for working with geographic data. Redis can store an object’s geographic coordinates, such as store locations or delivery trucks on the move. Then Redis can perform math and coordinate-based operations on that data, such as determining the distance between two points (How far away is the delivery car with my lunch order?) or finding all registered points within a given radius of another point (Where is the closest pet store to my current location?).

Ultimately, those longitudes and latitudes are just data for your applications to access and update. And as with any database that is part of your critical business logic, you want the best possible performance – particularly when the systems accessing the data are moving around physically (that delivery truck) and thus need real-time responses. To accomplish that, it’s important to optimize the queries and algorithms you use to interact with GEO data.

To maximize the Redis GEO commands’ execution performance, we delved into performance analysis and workload characterization techniques. The goals were to identify bottlenecks, optimize resource utilization, and improve overall performance.

In this post, we share those optimization techniques, such as reducing wasteful computation and simplifying algorithms, as well as the results of our analysis. The takeaway: We can reach four times the throughput on GEOSEARCH queries, and that enhancement has already been released as part of [Redis 7](https://github.com/redis/redis/releases/tag/7.0.7).

## Performance analysis and the geographic use case

Performance analysis and workload characterization are important techniques for understanding applications’ performance characteristics. These techniques involve collecting and analyzing data about the application’s behavior and its resource usage to identify bottlenecks, optimize resource utilization, and improve overall performance.

Whatever application we’re trying to speed up, we use deterministic, concise, and methodical ways to monitor and analyze performance. To do so yourself, you can adopt any of a number of [performance methodologies](https://www.brendangregg.com/methodology.html), some more suited than others, depending on the class of issues and analysis you want to make.

In broad terms, when you want to improve a program’s efficiency, this generic checklist applies to most situations:

1. **Determine the performance goals:** Before you start, you need a clear understanding of what you want to achieve. The goals might include improving response time, reducing resource utilization, or increasing throughput. In this case, we want to both improve the response time of each individual operation and consequently to increase the achievable throughput.

**2. Identify the workload:** Next, determine the workload that you will analyze. This might involve identifying the specific tasks or actions that the application will perform, as well as the expected load and usage patterns. For the GEO commands use case, we used a dataset with 60 million data points based on [OpenStreetMap (PlanetOSM)](https://wiki.openstreetmap.org/wiki/Planet.osm) data and a set of geodistance queries for the benchmark.

3. **Collect data:** Once you identify the workload, collect data about the application’s performance and its resource utilization for each use case. You might use profilers, debuggers, or performance analysis tools. Gather data about the program’s memory usage, CPU utilization, and other metrics. Profiling CPU usage by sampling stack traces at a timed interval is a fast and easy way to identify performance-critical code sections (also called hot spots). Our findings are precisely based upon using the Linux [perf tool](https://man7.org/linux/man-pages/man1/perf.1.html) for that goal. Our [documentation about identifying performance regressions](https://redis.io/docs/management/optimization/cpu-profiling/) and potential on-CPU performance improvements includes a full list of tools and deeper methodologies.

4. **Analyze the data: **Once you collect the data, you can use various techniques to analyze it and identify areas of the application that may affect performance. Some of those techniques are analyzing performance over time, comparing different workloads, and looking for patterns in the data. We find it easy to improve on CPU-related use cases by analyzing the recorded profile information using [perf report](https://man7.org/linux/man-pages/man1/perf-report.1.html#NAME), when you have the coding context of the application you’re profiling. The more experience you have with the application’s code, the easier it is to optimize it.

**5. Optimize the application:** Based on your analysis, you can then identify areas of the application that may be causing performance issues. Then take steps to optimize the code, such as changing to a more efficient algorithm, reducing the amount of memory used, or making other code adjustments. In the scenarios we showcase next, we focus on the efficiency of the algorithms and reducing the amount of duplicate computation.

**6. Repeat the process:** Performance analysis and workload characterization are ongoing processes, so it’s important to regularly review and analyze the application’s performance. This allows you to identify and address new bottlenecks or issues that may arise in updates or usage situations.

## Context on the Redis geospatial indices distance calculation

You can’t make software run faster if you don’t know what it’s doing. In this case, it means a short introduction to the process of working with geospatial data.

Most commands to query [Redis Geospatial Indices](https://redis.io/commands/?group=geo) calculate the distance between two coordinates, so it makes sense to examine how that’s done algorithmically. The [Haversine distance](https://www.igismap.com/haversine-formula-calculate-geographic-distance-earth/) is a useful measure, as it takes into account the curvature of the Earth, with more accurate results than a [Euclidean distance ](https://www.cuemath.com/euclidean-distance-formula/)calculation.

To calculate the Haversine distance on a sphere (such as the Earth), you need the latitude and longitude of the two points, as well as the radius of the sphere. The Haversine formula calculates the distance between the points in a straight line, following the shortest path across the surface of the sphere.

These calculations rely heavily on trigonometric functions to compute the Harvesive distance, and calling trigonometric functions is expensive in terms of CPU cycles. In a bottleneck analysis of a simple GEOSEARCH command, around 55% of the CPU cycles are spent within those functions, as shown in Figure 1. That means it’s worth the time to optimize those code blocks, or as [Amhdal](http://www.umsl.edu/~siegelj/CS4740_5740/Overview/Amdahl's.html) would say, “The overall performance improvement gained by optimizing a single part of a system is limited by the fraction of time that the improved part is actually used.”

So, let’s focus on the largest possible optimization.

## The first optimization round: reduce wasteful computation

As the profile data above demonstrates, 54.78% of CPU cycles are generated by geohashGetDistanceIfInRectangle. Within it, we call geohashGetDistance three times. The first two times, we call the routine to produce intermediate results (such as to check if a point is out of range in longitude or latitude). This avoids CPU-expensive distance calculations if the conditions are false. It makes sense to check that data is in range, but we don’t need to do so repeatedly.

Our first optimization attempt to reduce the wasteful computation of intermediate results in two steps (and described in detail in the [PR #11535](https://github.com/redis/redis/pull/11535)):

- Reduce expensive computation on intermediate geohashGetDistance calculations.
- Avoid the expensive longitude distance calculation if the latitude distance condition fails.

That optimization made a significant difference. For that GEOSEARCH query, using a single benchmark client with no pipeline, we decreased the average latency (including round trip time) from 93.598ms to 73.046ms, representing a latency drop of approximately 22%.

## The second round: wasteful computation

The same performance analysis of GEOSEARCH queries also showed that, in some cases, Redis performs spurious calls to sdsdup and sdsfree. These commands allocate and deallocate strings’ memory, respectively. This happens with large datasets, where many elements are outside the search’s range.

The performance improvement we proposed in [PR 11522](https://github.com/redis/redis/pull/11522) was simple: Instead of pre-allocating the string’s memory, we changed the role of geoAppendIfWithinShape to let the caller create the string only when needed. This resulted in approximately 14% latency drop and 25% improvement in the achievable ops/sec.

## The third round: simplifying algorithms

To optimize geographic index querying, we focused on data pattern information. The intent is to simplify the number of calculations required for the Haversine distance. This is purely a mathematics exercise.


When the longitude difference is 0:

- Given a longitude difference of zero, the asin(sqrt(a)) on the Haversine is asin(sin(abs(u))).
- Set arcsin(sin(x)) equal to x when x ∈[−𝜋/2,𝜋/2].
- Given a latitude between [−𝜋/2,𝜋/2] we can simplify arcsin(sin(x)) to abs(x).

The [PR #11579](https://github.com/redis/redis/pull/11579) describes the optimization and obtained performance improvement of this simplification. The bottom line: It resulted in 55% increase in the achievable operations per sec of the Redis GEOSEARCH command.

## The fourth round: a representation issue

All use cases that heavily rely on converting a double to a string representation (such as the conversion of a double-precision floating point number (1.5) to a string (“1.5”), can benefit by replacing the call to snprintf(buf,len,”%.4f“,value) with an equivalent fixed-point double to string optimized version.

The GEODIST command, shown in Figure 3, is a good example. About a quarter of the CPU time is devoted to the type conversion.

[PR 11552](https://github.com/redis/redis/pull/11552) describes in detail the optimization we suggested, which resulted in a 35% increase in the achievable operations per second of the GEODIST command.

## Putting it all together in Redis 7.0

A primary reason for Redis’s popularity as a database is its performance. We generally measure queries in sub-millisecond response time – and we want to keep improving it!

The cumulative effect of the optimizations we describe in this blog post: We increased the performance of Redis geospatial commands by up to four times their previous speed. You can already benefit from these enhancements, as they are part of Redis 7.0.7. And that should get you where you’re going, faster than you did before.

| Command | Test case | Achievable ops/sec Redis 7.0.5 | Achievable ops/sec Redis 7.0.7 | Improvement factor |
|---|---|---|---|---|
| GEODIST key … | geo-60M-elements-geodist-pipeline-10 | 775524 | 993632 | 1.3 X |
| GEOSEARCH … FROMLONLAT … BYRADIUS | geo-60M-elements-geosearch-fromlonlat | 11.8 | 13.8 | 1.2 X |
| GEOSEARCH … FROMLONLAT … BYBOX | geo-60M-elements-geosearch-fromlonlat-bybox | 13.2 | 49.6 | 3.8 X |

| Command | Test case | Overall p50 latency including RTT (ms) Redis 7.0.5 | Overall p50 latency including RTT (ms) Redis 7.0.7 | Improvement factor |
|---|---|---|---|---|
| GEODIST key … | geo-60M-elements-geodist-pipeline-10 | 2.575 | 2.007 | 1.3 X |
| GEOSEARCH … FROMLONLAT … BYRADIUS | geo-60M-elements-geosearch-fromlonlat | 679.935 | 598.097 | 1.1 X |
| GEOSEARCH … FROMLONLAT … BYBOX | geo-60M-elements-geosearch-fromlonlat-bybox | 605.739 | 161.791 | 3.7 X |

Note that this is not an isolated performance improvement – quite to the contrary. This set of improvements is a real-life example of the impact of the performance efforts that we call the “Redis benchmarks specifications.” We are constantly pushing for greater visibility and better performance across the entire Redis API.

## Going the distance

Want to learn more about geospatial computing? This five-minute video gives you the lay of the land.

[Click here to view video](https://www.youtube.com/embed/qftiVQraxmI)

Find out more about in the performance blogs in this series, most of them co-written with Intel:

- [Making the Fast, Faster! Methodically Improving Redis Performance](/blog/improving-redis-performance/), describing how we improved stream’s ingest performance by around 20%.
- [Performance Testing, Profiling, and Analysis](/blog/redis-intel-performance-testing/) describing our “zero-touch” performance and profiling automation.
- [The Gorilla in the Room: Exploring RedisTimeSeries Performance Optimizations](/blog/redistimeseries-performance-optimizations/) investigating potential performance optimizations for the RedisTimeSeries compression/decompression algorithm.
- [Optimizing Redis’ Default Compiler Flags](/blog/optimizing-redis-compiler-flags/) about changing the compiler behavior in Redis OSS.

**Intel, the Intel logo, and other Intel marks are trademarks of Intel Corporation or its subsidiaries.*
