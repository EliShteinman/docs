---
title: "Redis Time Series"
linkTitle: "Redis Time Series"
url: "/tutorials/modules/redistimeseries/"
description: "Redis Time Series is a Redis module that enhances your experience managing time-series data with Redis. It simplifies the use of Redis for time-series use cases such as internet of things (IoT)..."
aliases:
- "/tutorials/modules-redistimeseries/"
date: 2026-02-25
lastmod: 2026-02-26
hidden: true
---

*Published 25 February 2026 · updated 26 February 2026*

> **TL;DR:**
>
> Redis Time Series is a Redis module purpose-built for ingesting, querying, and aggregating time-series data such as IoT sensor readings, stock prices, and application telemetry. It supports built-in downsampling, aggregation, and labeling so you can store millions of data points with a small memory footprint and query them at Redis speed.

> **NOTE**
>
> Redis now supports [time series data structures](https://redis.io/docs/latest/develop/data-types/timeseries/) natively without the need for a module

## What you'll learn

- What Redis Time Series is and when to use it
- How to create time series keys with `TS.CREATE`
- How to add data points with `TS.ADD`
- How to query ranges and get the latest value with `TS.RANGE` and `TS.GET`
- How to filter time series using labels with `TS.MGET`
- How to apply aggregation and downsampling to time-series queries

## What is Redis Time Series?

Redis Time Series is a Redis module that enhances your experience managing time-series data with Redis. It simplifies the use of Redis for time-series use cases such as internet of things (IoT) data, stock prices, and telemetry. With Redis Time Series, you can ingest and query millions of samples and events at the speed of Redis. Advanced tooling such as downsampling and aggregation ensure a small memory footprint without impacting performance. Use a variety of queries for visualization and monitoring with built-in connectors to popular monitoring tools like Grafana, Prometheus, and Telegraf.

Compared to general-purpose time-series databases, Redis Time Series offers sub-millisecond reads and writes, built-in downsampling rules that reduce storage without a separate ETL pipeline, and a label-based filtering system that makes it easy to query across thousands of keys at once.

## Step 1. Register and subscribe

Follow [this link to register](https://redis.io/try-free/) and subscribe to Redis Cloud

![Redis Cloud registration and subscription interface](/images/site-mirror/43b4d383a0d344d31a550320e9bdc871156454c7-1444x606.webp)

## Step 2. Create a database with Redis time series

![Creating a database with the Redis time series in Redis Cloud](/images/site-mirror/24bce7ff796638aa7ce52718ae55e97f0ba2a828-1240x836.webp)

## Step 3. Connect to a database

Follow [this](https://redis.io/insight/) link to learn how to connect to a database

## Step 4. Getting Started with Redis time series

This section will walk you through using some basic Redis time series commands. You can run them from the Redis command-line interface (redis-cli) or use the CLI available in Redis Insight. (See part 2 of this tutorial to learn more about using the Redis Insight CLI.) Using a basic air-quality dataset, we will show you how to:

- Create a new time series
- Add a new sample to the list of series
- Query a range across one or multiple time series

![Redis Insight dashboard displaying time series data graphs](/images/site-mirror/11b0cdfbea3615e864caa121818696d07619f142-1430x200.webp)

### Create a new time series

Let's create a time series representing air quality dataset measurements. To interact with Redis time series you will most often use the TS.RANGE command, but here you will create a time series per measurement using the TS.CREATE command. Once created, all the measurements will be sent using TS.ADD.

The sample command below creates a time series and populates it with three entries:

```bash
>> TS.CREATE ts:carbon_monoxide
>> TS.CREATE ts:relative_humidity
>> TS.CREATE ts:temperature RETENTION 60 LABELS sensor_id 2 area_id 32
```

In the above example, ts:carbon_monoxide, ts:relative_humidity and ts:temperature are key names. We are creating a time series with two labels (sensor_id and area_id are the fields with values 2 and 32 respectively) and a retention window of 60 milliseconds:

#### Add a new sample data to the time series

Let's start to add samples into the keys that will be automatically created using this command:

```bash
>> TS.ADD ts:carbon_monoxide 1112596200 2.4
>> TS.ADD ts:relative_humidity 1112596200 18.3
>> TS.ADD ts:temperature 1112599800 28.3
```

```bash
>> TS.ADD ts:carbon_monoxide 1112599800 2.1
>> TS.ADD ts:relative_humidity 1112599800 13.5
>> TS.ADD ts:temperature 1112603400 28.5
```

```bash
>> TS.ADD ts:carbon_monoxide 1112603400 2.2
>> TS.ADD ts:relative_humidity 1112603400 13.1
>> TS.ADD ts:temperature 1112607000 28.7
```

#### Querying the sample

Now that you have sample data in your time series, you're ready to ask questions such as:

#### How do you get the last sample from a Redis time series?

`TS.GET` is used to get the last sample. The returned array will contain the last sample timestamp followed by the last sample value, when the time series contains data:

```bash
>> TS.GET ts:temperature
1) (integer) 1112607000
2) "28.7"
```

#### How do you get the last sample matching a specific filter?

`TS.MGET` is used to get the last samples matching the specific filter:

```bash
>> TS.MGET FILTER area_id=32
1) 1) "ts:temperature"
   2) (empty list or set)
   3) 1) (integer) 1112607000
      2) "28.7"
```

#### How do you get samples with labels matching a specific filter?

```bash
>> TS.MGET WITHLABELS FILTER area_id=32
1) 1) "ts:temperature"
   2) 1) 1) "sensor_id"
         2) "2"
      2) 1) "area_id"
         2) "32"
   3) 1) (integer) 1112607000
      2) "28.7"
```

#### How do you query a range across one or more time series?

`TS.RANGE` is used to query a range in forward directions while `TS.REVRANGE` is used to query a range in reverse directions. They let you answer such questions as:

#### How do you get samples for a time range?

```bash
>> TS.RANGE ts:carbon_monoxide 1112596200 1112603400
1) 1) (integer) 1112596200
   2) "2.4"
2) 1) (integer) 1112599800
   2) "2.1"
3) 1) (integer) 1112603400
   2) "2.2"
```

#### How do you use aggregation with Redis time series?

You can use various aggregation types such as avg, sum, min, max, range, count, first, last etc. The example below shows how to use the `avg` aggregation type to downsample your data:

```bash
>> TS.RANGE ts:carbon_monoxide 1112596200 1112603400 AGGREGATION avg 2
1) 1) (integer) 1112596200
   2) "2.4"
2) 1) (integer) 1112599800
   2) "2.1"
3) 1) (integer) 1112603400
   2) "2.2"
```

## Next steps

- Learn more about Redis time series in the [Redis quick start](/tutorials/howtos/quick-start/#timeseries-data-and-queries-with-redis) tutorial
- Build a real-time API with time-series data using [FastAPI and Redis](/tutorials/develop/python/fastapi/)
- Explore the [time series data type documentation](https://redis.io/docs/latest/develop/data-types/timeseries/) for the full command reference
- Connect Redis Time Series to [Grafana](https://redis.io/docs/latest/integrate/grafana/) for real-time dashboards and monitoring
