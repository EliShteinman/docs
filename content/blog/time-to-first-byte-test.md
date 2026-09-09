---
title: "How to test & reduce Time to First Byte (TTFB)"
linkTitle: "How to test & reduce Time to First Byte (TTFB)"
url: "/blog/time-to-first-byte-test/"
description: "If your pages feel sluggish, Time to First Byte (TTFB) is often where to look first. TTFB measures how long the browser waits before the server sends anything back. That wait sits at the front of..."
date: 2026-04-23
blogCategories:
- "Tech DE"
authors:
- "Jim Allen Wallace"
lastmod: 2026-04-23
hidden: true
---

*By Jim Allen Wallace, Sr. Product Marketing Manager · Published 23 April 2026*

![Redis](/images/site-mirror/a7cd51d27f21f7a352c619c97b9d2c3896badba5-1200x628.webp)

If your pages feel sluggish, Time to First Byte (TTFB) is often where to look first. TTFB measures how long the browser waits before the server sends anything back. That wait sits at the front of the loading chain: before rendering, before subresource discovery, before Largest Contentful Paint (LCP) can even begin. LCP tracks when the largest visible element on a page finishes rendering, and it can't start until that first byte arrives. A slow TTFB delays every metric that follows. This guide covers what TTFB measures, how to test it, what causes it to spike, and which fixes move the needle.

## What TTFB actually measures

TTFB is the elapsed time from the moment a browser initiates a navigation to the moment the server sends its first byte back. That single number is actually several phases stacked in sequence:

- **Redirect time:** Any HTTP redirects before the final request add a full round trip each.
- **Service worker startup:** If a service worker intercepts the request, its startup time adds to the wait.
- **Domain Name System (DNS) lookup:** The browser resolves the domain name to an IP address before it can open a connection.
- **Connection and Transport Layer Security (TLS) negotiation:** The Transmission Control Protocol (TCP) handshake and TLS handshake for HTTPS happen before a single byte of content is exchanged.
- **Server processing:** The time your server spends generating a response before it can start sending anything back.

Which phase is slow determines which fix applies, so measuring before optimizing matters.

### Google's TTFB thresholds

Google evaluates TTFB at the [75th percentile](https://developer.chrome.com/docs/crux/guides/pagespeed-insights) per origin in Chrome User Experience Report (CrUX) data, using these thresholds:

- **Good:** 800ms or less
- **Needs improvement:** 800ms–1,800ms
- **Poor:** over 1,800ms

If you're in the "needs improvement" or "poor" range, users are waiting for your server before the page has done any work at all.

## Why TTFB matters for later metrics

TTFB isn't a Core Web Vital, but it sets the clock for the ones that are. Google measures page experience through three [Core Web Vitals](https://developer.chrome.com/docs/crux/guides/pagespeed-insights): Largest Contentful Paint (LCP), which tracks how long it takes for the main content to appear on screen; Interaction to Next Paint (INP), which measures how quickly the page responds when a user clicks or taps; and Cumulative Layout Shift (CLS), which captures how much the page jumps around while it's still loading.

None of those things can happen until the browser receives that first byte from the server. If the server takes 2 seconds to respond, the browser spends 2 seconds doing nothing, and every other metric starts its clock 2 seconds late.

The field data shows the gap clearly: sites with poor LCP have a [75th-percentile TTFB](https://web.dev/blog/common-misconceptions-lcp) of 2,270ms, while sites with good LCP have a [median TTFB around 600ms](https://almanac.httparchive.org/en/2024/performance). Faster server response doesn't guarantee good scores across the board, but a slow one makes them nearly impossible.

## How to run a TTFB test

Two types of data are useful here. Field data reflects real user conditions (varying networks, devices, and locations) and shows what your actual audience experiences. Lab data runs under controlled conditions you define, which makes it repeatable and useful for debugging. The most reliable picture comes from using both.

[PageSpeed Insights](https://pagespeed.web.dev/) shows both in one report. [Chrome DevTools](https://developer.chrome.com/docs/devtools/network/reference) breaks down per-request timing in the Network tab, including a dedicated TTFB row. [WebPageTest](https://docs.webpagetest.org/metrics/page-metrics/) lets you test from specific regions, which helps identify content delivery network (CDN) coverage gaps. For real-user monitoring in production, the Navigation Timing API and Google's web-vitals library both expose TTFB from actual sessions.

One thing to know: [TTFB includes redirects](https://web.dev/articles/ttfb) in most definitions, so field data may show higher numbers than synthetic tools for the same page.

## What causes slow TTFB

TTFB is a sum of phases, so the cause determines the fix. The four most common culprits are:

- **Database query latency:** [Slow queries](https://developers.google.com/speed/docs/insights/Server) are a primary cause of server response times exceeding 200ms. The N+1 problem, where fetching a list triggers a separate query for every item in it, can stack dozens of small queries into hundreds of milliseconds of wait time.
- **Server-side rendering (SSR):** The page has to be fully generated before any bytes can be sent. The more work the server does per request, the later the first byte arrives.
- **Redirect chains:** Each hop adds at least one full round trip, plus fresh DNS, TCP, and TLS overhead if the redirect crosses origins. A three-hop chain can cost several hundred milliseconds before the actual request even starts.
- **TLS version & geographic distance:** [TLS 1.2](https://web.dev/articles/content-delivery-networks) requires two round trips for the handshake; [TLS 1.3](https://web.dev/articles/content-delivery-networks) cuts that to one. HTTP Archive data shows [108ms vs 289ms](https://almanac.httparchive.org/en/2024/cdn) for CDN TLS negotiation at the 90th percentile. Geographic distance compounds this: physical infrastructure adds latency that can only be reduced by moving content closer to users.

Each of these maps directly to a fix in the next section.

## How to reduce TTFB

Once you've identified which phase is slow, the fix becomes clearer. The highest-impact changes tend to address the phases with the most headroom.

- **Deploy a CDN:** CDNs cut TTFB two ways: edge nodes closer to users reduce connection latency, and edge caching can serve responses without hitting your origin server at all. For sites with a global audience, this alone can move TTFB from "poor" to "good."
- **Eliminate redirect chains:** Every hop in a redirect chain adds a full round trip. Consolidating multi-hop chains into a single redirect reclaims that time before the actual request even starts.
- **Optimize database queries:** Unindexed queries and the N+1 pattern are common sources of server processing time. Reducing the number of queries per request, or the cost of each one, directly reduces the server-processing phase of TTFB.
- **Use streaming SSR:** Instead of waiting for the full page to generate before sending anything, streaming SSR sends HTML in chunks as it's ready. The browser starts work sooner.
- **Adopt HTTP/3 & TLS 1.3:** [TLS 1.3](https://web.dev/articles/content-delivery-networks) cuts the handshake from two round trips to one. HTTP/3 over QUIC reduces head-of-line blocking at the connection level. Both are available through most CDNs.

In-memory caching sits across several of these: it reduces server processing time, cuts database round trips, and can serve cached responses without touching the origin at all.

### Use in-memory caching

[Memory-caching](https://developer.chrome.com/docs/lighthouse/performance/server-response-time) is a primary server response time optimization. When database or session lookups sit on your critical path, serving that data from RAM instead of disk can cut the server-processing phase from hundreds of milliseconds to single digits.

Redis is built for exactly this. Redis is a real-time data platform built for sub-millisecond data access, and capabilities like the [cache-aside pattern](https://redis.io/solutions/caching/) can help keep the data layer from dominating TTFB. Common use cases include [query caching](https://redis.io/glossary/database-row-caching/) (storing frequently requested results in memory), session storage (avoiding a database round trip on every authenticated request), and API response caching (serving repeated responses without regenerating them). [Redis 8](/blog/redis-8-ga/) introduced hash-field expiration for advanced session-management scenarios, letting you set time-to-live values on individual fields within a hash rather than expiring the entire key.

## Most of the web still has a TTFB problem

With those fixes in mind, it's worth zooming back out to the bigger picture. In 2025, 55% of desktop sites and [44% of mobile sites](https://almanac.httparchive.org/en/2025/performance) have good TTFB, which means more than half of all mobile sites still fall short. The share of sites achieving good TTFB increased by 1% on desktop and by 2% on mobile since 2024, but the gap between mobile and desktop remains at 11 percentage points.

Getting your TTFB under 800ms across real-user traffic puts you ahead of the majority of mobile sites, where progress has been slow.

## Faster server response starts with faster data

TTFB affects every performance metric that follows. A slow server response delays First Contentful Paint (FCP), delays LCP, and delays when the browser can start working with the page.

One of the biggest levers for reducing the server-processing component of TTFB is data retrieval speed. Redis is a real-time data platform that keeps frequently accessed data in memory, reducing the disk I/O that slows server response times. Cache-aside patterns, session stores, and API response caching can help keep your data layer within its latency budget rather than consuming it on every request.

Redis combines caching, session management, and data retrieval in a single platform, so you don't need to stitch together multiple tools to keep server response times low. [Try Redis free](https://redis.io/try-free/) to see how it handles your caching workload, or [talk to our team](https://redis.io/meeting/) about reducing server response times across your infrastructure.
