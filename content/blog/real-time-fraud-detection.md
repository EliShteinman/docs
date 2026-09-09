---
title: "Real-time fraud detection for financial transactions"
linkTitle: "Real-time fraud detection for financial transactions"
url: "/blog/real-time-fraud-detection/"
description: "When a customer taps \"pay,\" a clock starts that your fraud system can't pause. The payment authorization resolves in a fixed window whether your model has scored the transaction or not. If it..."
date: 2026-06-10
blogCategories:
- "Tech DE"
authors:
- "Jim Allen Wallace"
lastmod: 2026-06-10
hidden: true
---

*By Jim Allen Wallace, Sr. Product Marketing Manager · Published 10 June 2026*

![Real-time fraud detection for financial transactions](/images/site-mirror/d0920fc00731711f60a4fb2a10b38a80b6648e3c-2400x1256.webp)

When a customer taps "pay," a clock starts that your fraud system can't pause. The payment authorization resolves in a fixed window whether your model has scored the transaction or not. If it hasn't, the payment either gets declined or clears without a fraud check. Most of that window goes to network hops and issuer processing you don't control, and fraud scoring gets what's left.

That makes fraud detection different from most ML inference problems: latency isn't a quality metric to optimize, it's a hard constraint.

This article covers how real-time feature stores and sliding-window data structures fit into the scoring pipeline, what it takes to scale to billions of events, and why high availability matters when downtime lets fraud through.

## Fraud detection is a latency problem first

The money explains why fraud detection exists: U.S. consumers reported [$15.9 billion](https://www.ftc.gov/news-events/news/press-releases/2026/03/ftc-testifies-joint-economic-committee-agencys-efforts-combat-fraud) lost to fraud in 2025, across 3 million reports and up sharply from the year before. Latency explains why it's hard to build. A fraud model that answers late is the same as no fraud model at all.

Instant payment rails raise the stakes further. They move the fraud decision into the moment of payment itself, and once an instant payment settles, it's irreversible. The review window that used to be hours or days is now part of the transaction.

## How much time do you have to score a transaction?

Less than the full window suggests, because much of it is spent before fraud scoring even begins. High-performance systems score fraud risk in the [10-50ms range](/blog/ai-in-payment-processing/) within authorization thresholds of roughly 100ms, and the rest of the budget goes to steps you don't run. A card-not-present authorization passes through several hands:

- **Network transmission to the payment service provider (PSP):** the PSP connects the customer to the rest of the payment flow
- **Feature retrieval & model inference:** your model pulls features and scores the transaction
- **Routing & acquirer submission:** the request moves toward the card network
- **Issuer authorization:** the issuing bank makes its decision, often the longest single step
- **Response transmission:** the result travels back to the merchant

The issuer's decision and the network hops on either side of it consume most of the budget, leaving much less time for the parts you actually control: feature retrieval, fraud scoring, and routing.

The biggest players have pushed scoring to extremes. One major card network's authorization system evaluates up to [500 risk attributes](https://www.jisem-journal.com/download/102_HP-5035.pdf) in about 1ms. Most teams don't need to match that, but the principle holds at any scale: every millisecond saved in scoring is a millisecond returned to the rest of the pipeline.

Batch approaches struggle to meet that bar. Batch pipelines introduce ingestion lag between when a transaction occurs and when data becomes available, and if upstream freshness lags behind your backend APIs, the model ends up scoring with stale context.

## What does a feature store do in a fraud detection pipeline?

A feature store serves the context your fraud model needs at scoring time. Without it, the model only sees the transaction in front of it, not the signal that actually matters.

### The context problem

That context is everything. How many times has this card been used in the past hour? What's the account's average transaction amount over the last 30 days? Is this merchant category unusual for this cardholder? A feature store exists to answer questions like these fast enough to matter.

### Why training & inference need different data stores

Feature stores exist because training and inference want incompatible things from your data. Training needs historical depth: large batch reads, point-in-time correctness, feature values as they existed at each moment in history. Inference needs the opposite: current values, individual entity lookups, millisecond responses. One system can't do both well, so the standard answer is a dual-database architecture. A columnar store handles offline training. A [key-value store](https://redis.io/nosql/key-value-databases/) handles online inference. Explicit synchronization keeps them aligned.

### The training-serving skew problem

Training-serving skew is a silent killer: the model performs great offline and drops in production, and the metrics rarely tell you why. It happens when features get computed one way during training and a different way at inference.

The mismatches are usually small and easy to miss. Maybe your batch SQL computes a rolling average differently than your streaming job, or timezone handling shifts a window boundary by an hour. The model is technically working, just looking at slightly different data than it was trained on.

The fix is structural, not statistical. Teams reduce skew by centralizing feature definitions and separating just-in-time, near-real-time, and batch features so each is computed on the right path.

### How Redis fits the online inference layer

Redis is a real-time data platform built for low latency across AI and operational workloads, and it fits this layer well. Holding features in RAM keeps retrieval fast enough to stay inside a tight scoring budget, which is why in-memory feature stores are a common choice for fraud scoring at scale. Actual latency depends on your deployment, data size, and access patterns, so benchmark against your own workload. Redis also supports vector search alongside its core data structures, so behavioral similarity lookups can sit on the same platform as feature serving instead of fanning out to a separate system.

## Sliding-window velocity counts & why data structures matter

Velocity features are some of the strongest signals in fraud detection, and the data structure you pick to compute them shapes whether you can serve them in time. "How many transactions has this card made in the past 10 minutes?" is a [valuable signal](https://arxiv.org/html/2604.13125v1) that static features often miss, but only if you can answer it inside the scoring budget.

That's a sliding window question. A sliding window always covers the most recent stretch of time, like the last 10 minutes as of right now, so it moves with the clock and can be queried at any moment. Tumbling windows, by contrast, chop time into [fixed, non-overlapping blocks](https://nightlies.apache.org/flink/flink-docs-stable/docs/concepts/time): useful for hourly rollups, but "the past 10 minutes" rarely lines up with a block boundary. Fraud velocity counting needs the moving version.

### Sorted sets for exact velocity counts

When you need an exact count, Redis sorted sets are the structure most teams reach for. Each transaction goes in with a timestamp as its score, expired entries get trimmed off the back, and the remaining members give you the current window count. It's the same [sliding-window rate-limiting pattern](https://redis.io/docs/latest/develop/data-types/sorted-sets), applied to fraud velocity, and it scales to billions of keys in production fraud systems that run velocity checks across many transaction attributes at once.

Per-entity windows also tend to score better than coarser aggregates. In one [sliding-window study](https://research.chalmers.se/publication/545685/file/545685_Fulltext.pdf), individual cardholder windows outperformed methods based on average quantities across larger transaction sets. Exact counts at the entity level are worth the memory when the signal is this directly tied to fraud risk.

### Probabilistic structures for memory-efficient counting

Not every fraud signal needs to be exact. When the question is "have I seen this device fingerprint before?" or "how many distinct merchants has this card touched today?", probabilistic structures get you a useful answer in a fraction of the memory.

Three patterns cover most of these cases:

- **Bloom filters** answer membership questions in O(1) time with a fixed memory footprint. False positives trigger a second look. False negatives don't happen in the standard model.
- **HyperLogLog** estimates cardinality using about 12KB of memory with a [standard error](https://redis.io/docs/latest/develop/data-types/probabilistic/hyperloglogs/) under 1%. Spotting a card that hit 47 unique merchants in an hour versus a baseline of 3-5 doesn't need exact precision.
- **Count-Min Sketch** estimates point frequency, like how many times a specific (card, merchant) pair has shown up. It can overestimate but never underestimate, which is the right direction of error for fraud detection where missed counts cause [false negatives](https://users.cs.duke.edu/~reif/courses/alglectures/jain.lectures/StreamingAlgorithms.pdf).

Redis covers both ends of this spectrum. Sorted sets, HyperLogLog, Bloom filters, and Count-Min Sketch are all available in Redis Open Source, so you can pick the right tradeoff between accuracy, memory, and speed for each signal.

## How to scale fraud detection to billions of events

Once the per-entity counting patterns work, volume becomes the next constraint. Fraud at production scale means scoring most of your transaction traffic, not a sample of it.

The architecture that handles that volume usually splits into three layers. Event ingestion through Kafka, or an equivalent system, captures transactions with minimal buffering latency. Stream processing maintains per-card state, runs the windowed aggregations, and writes the computed features into a low-latency state store. Scoring then pulls from that store instead of rebuilding state on every request.

That separation is what keeps the hot path fast: the online side only fetches, it never recomputes. Redis is built for that shape of workload. In one benchmark, Redis reported [100 million operations](/blog/redis-enterprise-extends-linear-scalability-200m-ops-sec/) per second at sub-millisecond latency on a 20-node AWS cluster, scaling to 200 million on a 40-node cluster. That's the headroom in that specific benchmark, not a universal production number, but it shows the layer can grow with the event stream.

This pattern already runs at the top of the industry. Some of the largest card and payment companies use Redis as a real-time feature store to score [700,000 transactions](/blog/how-leading-financial-institutions-use-redis-to-drive-growth/) per second, holding billions of keys across sorted sets, hashes, and strings, with probabilistic structures keeping memory and compute in check as the key space grows. It's the same architecture described above, just with more shards behind it.

## High availability when "down" means fraud gets through

When fraud detection sits in the authorization path, downtime isn't a degraded experience. It's a risk decision. Operators have to choose between blocking transactions or letting them through with reduced screening, and neither option is good.

The cost of that choice shows up quickly. A 2018 outage at a major card network [caused 5 million failures](https://www.federalreserve.gov/econres/notes/feds-notes/offline-payments-implications-for-reliability-and-resiliency-in-digital-payment-systems-20240816.html) during a 10-hour disruption, and the same Federal Reserve note describes other payment outages that left merchants unable to accept electronic payments at all. When the fraud layer goes down, the whole authorization flow is exposed.

### Why fraud detection uptime is a compliance concern

Regulators treat fraud detection downtime as an operational resilience issue. The [Basel Committee](https://www.bis.org/bcbs/publ/d558.pdf) addresses digital fraud within its operational risk and operational resilience frameworks, and the Payment Card Industry Data Security Standard (PCI DSS) requires entities that process cardholder data to [monitor system access](https://www.pcisecuritystandards.org/pdfs/pci_ssc_quick_guide.pdf) and cardholder data, with ongoing security monitoring central to PCI SSC guidance. An outage isn't only a revenue event. It can create incident-reporting and resilience obligations too.

### What does payment-grade uptime require?

Payment-grade systems often target 99.999% uptime, and hitting that number takes more than redundancy. It usually means active-active multi-region architectures with automated failover, because a failover that waits on a human burns through the downtime budget before anyone joins the call. BIS/CPMI resilience standards generally call for payment infrastructures to support [two-hour recovery](https://www.bis.org/cpmi/publ/brief6.pdf) after a disruptive incident.

Latency degradation is the version of downtime that doesn't trigger alerts. A system that's technically up but missing the fraud scoring [latency threshold](/blog/p99-latency/) creates the same problem as an outage: in some payment flows, riskier transactions continue without the screening you intended.

## Build your fraud hot path on Redis

Latency, accuracy, and availability are three ways the same fraud system fails. Too slow, and the score misses the authorization. Too stale, and the score stops being trustworthy. Down entirely, and teams choose between blocking good traffic and accepting more risk.

Redis fits into that architecture as a hot-path data layer for feature serving, sliding-window counting, state handling, and low-latency risk checks. Sorted sets handle exact velocity counts. Hashes and strings store behavioral profiles. Probabilistic structures, vector search, and the access patterns fraud pipelines depend on all sit on the same platform.

If you're building or scaling a fraud detection pipeline, [try Redis free](https://redis.io/try-free/) to test feature retrieval latency against your actual workload. Or [talk to our team](https://redis.io/meeting/) about architecting for the throughput and availability your fraud system requires.
