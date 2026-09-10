---
title: "Building a Popup Store application using Redis"
linkTitle: "Building a Popup Store application using Redis"
url: "/tutorials/building-a-popup-store-application-using-redis/"
description: "Pop-up stores are becoming a popular channel for retailers to create a new revenue stream, generate buzz with customers, test product concepts, or unload excess inventory. Since the idea is to spin..."
group: "For developers"
date: 2026-02-25
lastmod: 2026-02-26
hidden: true
mirrored: true
---

*Published 25 February 2026 · updated 26 February 2026*

> **TL;DR:**
>
> Build a real-time popup store with Redis by using **Redis Streams** for event-driven order processing, **Redis time series** for live analytics, and a **Node.js** backend to simulate customer traffic. Visualize the entire data pipeline in Grafana with the Redis Datasource plugin. [Clone the repo](https://github.com/redis-developer/redis-pop-up-store/) and run `docker-compose up` to get started.

Pop-up stores are becoming a popular channel for retailers to create a new revenue stream, generate buzz with customers, test product concepts, or unload excess inventory. Since the idea is to spin up the store quickly and then close it shortly thereafter, it doesn't make sense to spend a lot of time on development. With the right Redis data structures, you can create a robust, real-time customer experience without a lot of development effort.

## What will you learn?

- How to use [Redis Streams](https://redis.io/docs/latest/develop/data-types/streams/) for real-time event processing in an e-commerce scenario
- How to track inventory and sales metrics with [Redis time series](https://redis.io/docs/latest/develop/data-types/timeseries/)
- How to visualize a live data pipeline using Grafana and the [Redis Datasource](/tutorials/explore/redisdatasource)
- How to process and complete orders in real time using stream consumers

## Prerequisites

- [Docker](https://www.docker.com/) and [Docker Compose](https://docs.docker.com/compose/) installed
- Basic familiarity with [Node.js](https://nodejs.org/)
- A basic understanding of [Redis Streams](https://redis.io/docs/latest/develop/data-types/streams/)

## What is a popup store application?

This pop-up store demo illustrates a company that sells a single product and has 10,000 units available for purchase. Each customer can purchase one unit and the sale lasts only 10 minutes, so order processing must be instantaneous. The demo shows how to visualize a data pipeline in real time using [Redis Streams](https://redis.io/docs/latest/develop/data-types/streams/), [Redis time series](https://redis.io/docs/latest/develop/data-types/timeseries/), and [Redis Datasource with Grafana](/tutorials/explore/redisdatasource).

![Animated diagram showing the popup store data flow between Node.js, Redis Streams, time series, and Grafana](/images/site-mirror/e5692c548a47793af0f4a6209abd8df6a663b444-400x172.gif)

> **NOTE**
>
> This demo originally used RedisGears for stream processing. RedisGears has been deprecated and is no longer available as a standalone module. The stream processing concepts demonstrated here can be implemented using [Redis triggers and functions](https://redis.io/docs/latest/develop/interact/programmability/triggers-and-functions/) or application-level stream consumers. The repository may require updates to run with current Redis versions.

## How do you clone and run the popup store?

### Step 1. Clone the repository

```bash
git clone https://github.com/redis-developer/redis-pop-up-store/
```

### Step 2. Run the application

```bash
docker-compose up -d
```

## How do you access the Grafana dashboard?

Open `http://localhost:3000` to access the Grafana dashboard.

![Grafana dashboard for the popup store showing real-time inventory counts, order queues, and completed sales charts](/images/site-mirror/f6c975e3277ef97946df8e9f48844a25c67d0bce-2000x870.webp)

Grafana queries Redis Streams and time series keys every 5 seconds to display live samples using the Grafana Redis Datasource. The dashboard displays:

- **Product Available**: the value of the `product` key, which decreases as orders complete
- **Customers Ordering, Orders Processing, and Orders Completed**: the length of `queue:customers`, `queue:orders`, and `queue:complete` streams
- **Customers Overflow**: the difference between customer-submitted orders and orders completed
- **Customers Ordering**: orders created in the last 5 seconds
- **Orders In Queue**: orders waiting to be processed
- **Completed Flow**: orders completed in the last 5 seconds

## How does the popup store architecture work?

![Architecture diagram showing the popup store components: Node.js producer, Redis Streams for customer and order queues, time series for metrics, and Grafana for visualization](/images/site-mirror/7b75422b4ece1e3b73b0e25b07bdafa88d2ce95b-2000x824.webp)

The application follows an event-driven architecture. The code samples below use the deprecated RedisGears API for reference; see the note above for modern alternatives.

1. A **Node.js script** adds random data to the customers and orders streams, simulating flash sale traffic.
2. A **stream processor** watches all `queue:` keys and adds time series samples for monitoring.

```python
# Add Time-Series
def tsAdd(x):
   xlen = execute('XLEN', x['key'])
   execute('TS.ADD', 'ts:len:'+x['key'], '*', xlen)
   execute('TS.ADD', 'ts:enqueue:' + x['key'], '*', x['value'])

# Stream Reader for any Queue
gb = GearsBuilder('StreamReader') # See RedisGears deprecation note above
gb.countby(lambda x: x['key']).map(tsAdd)
gb.register(prefix='queue:*', duration=5000, batch=10000, trimStream=False)
```

1. Another **stream processor** completes orders by:
    - Adding data to the `queue:complete` stream
    - Deleting the client's ordering entry
    - Decreasing the product amount
    - Trimming the orders queue

```python
# Complete order
def complete(x):
    execute('XADD', 'queue:complete', '*', 'order', x['id'],
            'customer', x['value']['customer'])
    execute('XDEL', 'queue:customers', x['value']['customer'])
    execute('DECR', 'product')

# Stream Reader for Orders queue
gb = GearsBuilder('StreamReader') # See RedisGears deprecation note above
gb.map(complete)
gb.register(prefix='queue:orders', batch=3, trimStream=True)
```

## Next steps

- Explore [available-to-promise inventory tracking with Redis](/tutorials/howtos-solutions-real-time-inventory-available-to-promise) for production-grade real-time inventory management
- Learn about [real-time local inventory search with Redis](/tutorials/howtos-solutions-real-time-inventory-local-inventory-search) for location-based product availability
- Build a full [shopping cart application using Node.js and Redis](/tutorials/how-to-build-a-shopping-cart-app-using-nodejs-and-redis)
- Read about [streaming LLM output with Redis Streams](/tutorials/howtos-solutions-streams-streaming-llm-output) for another Redis Streams use case
- Browse the [Redis Popup Store GitHub Repository](https://github.com/redis-developer/redis-pop-up-store) for the full source code
- Read [3 Real-Life Apps Built with Redis Data Source for Grafana](https://redis.io/blog/3-real-life-apps-built-with-redis-data-source-for-grafana/) for more Grafana integration examples
