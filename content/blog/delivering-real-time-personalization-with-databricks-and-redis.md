---
title: "Delivering Real-Time Personalization with Databricks and Redis"
linkTitle: "Delivering Real-Time Personalization with Databricks and Redis"
url: "/blog/delivering-real-time-personalization-with-databricks-and-redis/"
description: "A customer is browsing an e-commerce site. They search for running shoes, open a product, read reviews, and add an item to the cart. Every one of those actions is a signal about what they want..."
date: 2026-09-08
blogCategories:
- "Tech"
authors:
- "Philip Laussermair"
- "Anant Pingle"
lastmod: 2026-09-08
hidden: true
---

*By Philip Laussermair, Anant Pingle · Published 8 September 2026*

![Delivering Real-Time Personalization with Databricks and Redis](/images/blog/2863a881ca62cdf32c98c71f8509fa926cdaa299-1200x628.webp)

## Why real-time matters

A customer is browsing an e-commerce site. They search for running shoes, open a product, read reviews, and add an item to the cart. Every one of those actions is a signal about what they want right now. If the homepage they land on still shows this morning's generic promotions, the moment is gone. The value of a recommendation decays fast, often within the same session, or the 500 milliseconds it takes for a single page to load.

However, seizing a real-time opportunity is impossible on a traditional batch architecture that refreshes every few minutes. For data engineers and architects designing real-time pipelines, bridging the gap between analytics and action is the challenge. Traditional pipelines that refresh on a schedule, every few minutes or even every few seconds, are excellent at answering "what happened." But personalization, fraud scoring, and inventory decisions have to answer "what should happen next" while the customer is still on the page. That means computing fresh state as events arrive and serving it back to the application in milliseconds.

Two things have to be true at once: the processing has to be continuous, and the serving has to be instant. Historically, achieving this required maintaining a complex dual-engine architecture, often by bolting on a specialized engine like Apache Flink alongside existing batch frameworks.

## Why RTM and Redis are critical to real-time use cases

Real-Time Mode (RTM) handles the first of these: continuous processing. Structured Streaming is Apache Spark™'s engine for processing streams of events continuously, the same way you would query a table, except the table never stops updating. Its default execution mode is excellent for high-throughput ETL that can tolerate latencies from seconds to minutes, but not for in-the-loop decisions that must land in tens of milliseconds. Real-Time Mode is a newer execution mode within Structured Streaming that closes that gap. By using a continuous data flow that processes events as they arrive, RTM delivers sub-second performance with strict p99 latencies in the tens to low hundreds of milliseconds. It runs using the same Spark APIs you already write, eliminating codebase duplication and logic drift without standing up a separate engine such as Apache Flink.

Redis handles the second half: instant serving. Once RTM has computed the latest recommendation, fraud score, or session state, the application needs to read it from the request path at very high request rates in well under a millisecond. That is exactly what Redis is built for:

- Sub-millisecond reads and writes at high throughput
- Flexible data models such as Hashes, JSON, Streams, TimeSeries, and Sorted Sets, so data can be written in the shape an application needs
- Built-in Time to live (TTL) and eviction to keep data fresh and memory-efficient
- High-availability options for production serving, with Redis Cloud and Azure Managed Redis service commitments of 99.99% for eligible Multi-AZ deployments and 99.999% for eligible Active-Active deployments; the applicable commitment depends on the product, plan, and topology

For teams that already use Redis as an application cache, this pattern extends an existing component into a real-time serving layer instead of adding another technology for application teams to operate and integrate.

The division of labor is the whole point. Real-Time Mode continuously computes the latest operational state from streaming events. Redis materializes that state as a low-latency serving layer, so applications can make decisions and deliver personalized experiences in milliseconds. Compute and serving, each doing what it is best at.

iFood, Latin America’s leading food delivery platform processing millions of daily orders, relies on Databricks Real-Time Mode and Redis to power real-time decisions at massive scale across its machine learning platform. 

*“Real-Time Mode has made Databricks a core part of our real-time Feature Platform. Combined with Redis for online serving, we can continuously transform streaming data into production-ready features in under one second, while maintaining the scale and operational simplicity required by our machine learning workloads.”*

*— Willian Moreira, Lead Machine Learning Platform Engineer, iFood*

![Redis](/images/blog/74aea7a48db342e07335eeddd7df9b6313304d6e-90x48.svg)

## The use case: recommendations that adapt within the session

Let's make it concrete. We want product recommendations that update as the customer browses, so the next page they see reflects the last thing they did, not the last time a batch job ran.

The inputs are a clickstream: product views, searches, add-to-cart, and purchase events, one message per action. The output is a ranked list of recommended products per user, refreshed continuously, that the website reads on every page render. In between, we need to keep a little bit of per-user session state (what they have looked at recently) and turn it into a score for candidate products.

## How Databricks and Redis build it

### Architecture

![Architecture](/images/blog/1e374de4cf33e3a722deeb33e569b858eed1757f-2054x1870.webp)

The clickstream lands in Kafka. An RTM pipeline reads it, maintains per-user session state, scores candidate products against that state, and writes the ranked results into Redis. The website reads one Redis key per page render.

### Step 1: read the clickstream

Ordinary Structured Streaming. Nothing RTM-specific here yet.

```python
events = (spark.readStream.format("kafka")
    .option("subscribe", "clickstream")
    .option("kafka.bootstrap.servers", BROKERS)
    .load()
    .select(from_json(col("value").cast("string"), EVENT_SCHEMA).alias("e"))
    .select("e.*"))    # user_id, event_type, product_id, category, ts

```

### Step 2: sessionize and score

We keep a small amount of state per user: a recency-weighted score for each product they have touched. Every event bumps the product it involved, weighted by intent (a purchase counts more than a view), and every score decays over time so recent interest outranks old. It is a single keyed stateful operator, one shuffle on the real-time path.

```python
EVENT_WEIGHTS = {"view": 1.0, "search": 1.5, "cart": 4.0, "purchase": 8.0}


def decay(score, last_seen_ms, now_ms):          # halves every HALF_LIFE_SECONDS
    return score * 0.5 ** ((now_ms - last_seen_ms) / 1000 / HALF_LIFE_SECONDS)


class ProductAffinity(StatefulProcessor):
    def init(self, handle):
        # the user's whole affinity map, held as one JSON-encoded state value
        self.state = handle.getValueState("affinity", "payload STRING")


    def handleInputRows(self, key, rows, timerValues):     # once per row in RTM
        now = timerValues.getCurrentProcessingTimeInMs()
        v = self.state.get()
        m = json.loads(v[0]) if v else {}                  # 1 state read: whole map
        for r in rows:
            old = m.get(r.product_id)
            score = (decay(old[0], old[1], now) if old else 0.0) + EVENT_WEIGHTS[r.event_type]
            m[r.product_id] = [score, now]
        ranked = sorted(((p, decay(s, ts, now)) for p, (s, ts) in m.items()),
                        key=lambda kv: kv[1], reverse=True)
        ranked = [(p, s) for p, s in ranked if s >= SCORE_FLOOR][:MAX_TRACKED]
        self.state.update((json.dumps({p: [s, now] for p, s in ranked}),))   # 1 state write
        yield emit(key[0], ranked[:TOP_N], now)            # per-event: top-10 to Redis


recommendations = (events
    .groupBy("user_id")
    .transformWithState(ProductAffinity(), OUTPUT_SCHEMA,
                        outputMode="update", timeMode="processingTime"))

```

The scoring here is deliberately simple: it weights recent activity and ranks products, and a full model would slot into the same place. In production these affinity scores typically feed, or are replaced by, an ML ranking model plus a candidate-generation step that surfaces items the shopper has not seen yet. For the benchmarks below we ran this pipeline against Azure Event Hubs through its Kafka interface; the companion repo includes that Kafka pipeline.

### Step 3: write to Redis with a ForeachWriter

Here is the one integration detail that matters. There are two ways to write to Redis from Spark. The Redis Spark Connector is the simplest way to use classic Structured Streaming with Redis. Real-Time Mode is newer, and today the connector does not yet cover it, so under RTM, you write through a ForeachWriter, the standard Spark sink for custom destinations (the foreach sink, not foreachBatch, which is inherently micro-batch). We store each user's recommendations as two keys that share a slot: a sorted set (product to score) for the ranking, and a hash with each product's title and price. Both get a short TTL, so stale sessions clear themselves. We buffer users and write them in pipelined batches to keep round-trip times down.

```python
class RedisSink:
    def open(self, partition_id, epoch_id):
        import redis
        self.r = redis.Redis(host=HOST, port=PORT, password=PWD, ssl=True)
        self.buffer = []
        return True


    def _queue(self, pipe, user_id, recs):           # stage one user's full replace
        key = f"recs:{{{user_id}}}"                   # {..} = Redis Cluster hash tag
        meta = f"{key}:meta"
        pipe.delete(key, meta)
        pipe.zadd(key, {r.product_id: r.score for r in recs})
        pipe.hset(meta, mapping={r.product_id: f"{r.title}|{r.price}" for r in recs})
        pipe.expire(key, TTL); pipe.expire(meta, TTL)




    def process(self, row):
        self.buffer.append((row.user_id, list(row.recs)))
        if len(self.buffer) >= FLUSH_EVERY:
            self._flush()


    def _flush(self):
        pipe = self.r.pipeline(transaction=False)
        for user_id, recs in self.buffer:
            self._queue(pipe, user_id, recs)
        pipe.execute()
        self.buffer = []


    def close(self, error):
        if self.buffer:
            self._flush()
        self.r.close()


query = (recommendations.writeStream
    .foreach(RedisSink())
    .trigger(realTime="5 minutes")   # enables RTM (Scala: RealTimeTrigger.apply("5 minutes"))
    .outputMode("update")            # RTM requires update mode
    .start())

```

One production note: the demo's pipe.execute() sends the buffered commands and waits for Redis to confirm the writes. Don't replace that with fire-and-forget under load; unacknowledged writes drop silently, which for a serving layer means stale recommendations no one notices.

### Step 4: the application reads

The website does one pipelined round trip per render: the ranked ids from the sorted set and their titles and prices from the hash. No Spark query, no table scan, just Redis in sub-millisecond time.

```python
key  = f"recs:{{{user_id}}}"
top  = r.zrevrange(key, 0, 9, withscores=True)   # ranked product ids + scores
meta = r.hgetall(f"{key}:meta")                  # product_id -> "title|price"

```

A customer clicks and the next page reflects it. The e-commerce details are just the setting. What we are really showing is compute and serving working together end to end.

### Performance

We ran the pipeline continuously against Azure Managed Redis, sustaining 100,000 clickstream events per second across 10,000 active users on a 10-worker cluster (160 vCPU), with no backlog. Per-user state stayed bounded, and Redis absorbed the write load comfortably at roughly 530,000 operations per second with no evictions.

***From click to recommendation served: under 160 ms at p99***

| Metric | 10k events/s | 100k events/s |
|---|---|---|
| p50 | 56 ms | 62 ms |
| p90 | 87 ms | 99 ms |
| p95 | 117 ms | 119 ms |
| p99 | 139 ms | 157 ms |

![From click to recommendation served: under 160 ms at p99](/images/blog/00caef3436dba4c9bafc1f9c2194905985985427-2018x1817.webp)

## The universe of use cases

The same pattern (RTM computes the latest state, Redis serves it in milliseconds) shows up across industries. Swap the events and the scoring logic, and the shape stays the same.

- Payment fraud detection: RTM enriches transactions and computes a fraud score; Redis serves the latest score to the payment gateway before authorization.
- Multi-agent coordination: RTM continuously processes agent events, tool results, and workflow updates to derive shared state; Redis makes that state immediately available so agents can coordinate, hand off work, and avoid conflicting actions.
- Real-time ML feature serving: RTM continuously computes rolling features (recent spend, click rate, session activity), and Redis serves the latest feature vector for online inference.
- Dynamic inventory: orders, returns, and warehouse updates continuously change stock; Redis exposes the latest availability to web and mobile.
- Fleet tracking and ETA: RTM processes GPS updates and recomputes ETAs; Redis serves the latest vehicle state to dispatch and customer apps.
- Security operations: RTM correlates events into active incidents; Redis holds the latest threat state for analysts and automated response.
- Operational dashboards: RTM continuously updates KPIs; Redis lets dashboards read the latest metrics without querying the streaming engine.

## Run it anywhere

This pattern is not tied to a single cloud or a single Redis deployment model, so it fits wherever your stack already lives. Databricks runs on AWS, Azure, and GCP, and Redis meets it in whichever form suits the environment:

- Redis Cloud: fully managed on AWS, GCP, or Azure, for teams that want zero operational overhead.
- Redis Software: self-managed on-prem or in your own VMs and Kubernetes, for strict data residency or air-gapped requirements.
- Azure Managed Redis: a first-party Azure service powered by Redis Enterprise, with native Azure billing, MACC burn-down, Entra ID auth, and deep Azure integration.

Wherever Databricks runs, Redis can serve as the real-time layer.

## Call to action

Real-time personalization is one instance of a broader pattern: continuous compute with RTM, instant serving with Redis. If you are building latency-sensitive experiences on Databricks, this pairing gets you from event to decision in milliseconds without a separate streaming engine. Everything in this walkthrough runs end to end: clone it, point it at your Kafka and Redis, and watch recommendations update as events arrive.

- **Get the code: **[https://github.com/redis-developer/redis-rtm-personalization-demo](https://github.com/redis-developer/redis-rtm-personalization-demo)
- **Redis Spark Connector (GitHub):** [redis-field-engineering/redis-spark](https://github.com/redis-field-engineering/redis-spark)
- **Databricks Real-Time Mode Docs:** [docs.databricks.com](https://docs.databricks.com/aws/en/structured-streaming/real-time)
- **Try Redis Cloud for free:** [redis.io/cloud](https://redis.io/cloud/)
- **Azure Managed Redis:** [azure.microsoft.com/en-us/products/managed-redis](https://azure.microsoft.com/en-us/products/managed-redis)

*Philip Laussermair is the Global Microsoft Technical Lead at Redis, with a focus on Azure Managed Redis and AI/ML integrations. Anant Pingle is a Sr. Specialist Solutions Engineer at Databricks. This post reflects an emerging pattern that both teams are seeing in the field and a growing collaboration between Redis and Databricks.*
