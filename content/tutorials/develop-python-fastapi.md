---
title: "Using Redis with FastAPI"
linkTitle: "Using Redis with FastAPI"
url: "/tutorials/develop/python/fastapi/"
description: "FastAPI is a Python web framework based on the Starlette microframework. With deep support for asyncio, FastAPI is indeed very fast. FastAPI also distinguishes itself with features like automatic..."
group: "For developers"
aliases:
- "/tutorials/develop-python-fastapi/"
date: 2026-02-25
lastmod: 2026-02-26
hidden: true
mirrored: true
---

*Published 25 February 2026 · updated 26 February 2026*

> **TL;DR:**
>
> In this tutorial, you'll build IsBitcoinLit, a FastAPI service that stores Bitcoin sentiment and price data in Redis Time Series, calculates rolling averages, and caches the results with async Python using redis-py.

## Introduction

[FastAPI](https://github.com/tiangolo/fastapi) is a Python web framework based on the [Starlette](https://www.starlette.io/) microframework. With deep support for asyncio, FastAPI is indeed very fast. FastAPI also distinguishes itself with features like automatic [OpenAPI (OAS)](https://openapis.org/) documentation for your API, easy-to-use data validation tools, and more.

Of course, the best way to **make your FastAPI service even faster** is to use Redis. Unlike most databases, Redis excels at low-latency access because it's an in-memory database. If you're new to using Redis with Python, check out the [redis-py getting started guide](https://redis.io/docs/latest/develop/clients/redis-py/) first.

In this tutorial, we'll walk through the steps necessary to use Redis with FastAPI. We're going to build IsBitcoinLit, an API that stores Bitcoin sentiment and price averages in [Redis](https://redis.io/docs/latest/develop/data-types/timeseries/) using a timeseries data structure, then rolls these averages up for the last three hours.

Next, let's look at the learning objectives of this tutorial.

## Learning Objectives

The learning objectives of this tutorial are:

1.  Learn how to install redis-py and connect to Redis asynchronously
2.  Learn how to integrate redis-py with FastAPI
3.  Learn how to use Redis to store and query timeseries data
4.  Learn how to use Redis as a cache with async Python

Let's get started!

## Pre-Tutorial Quiz

Want to check gaps in your knowledge of Redis and FastAPI before you continue? Take our short pre-tutorial quiz!

You can also [visit the quiz directly](https://forms.gle/eXiiVcgXqG9UNarG6).

## Set Up the IsBitcoinLit Project

You can achieve the learning objectives of this tutorial by reading through the text and code examples that follow.

However, we recommend that you set up the example project yourself, so that you can try out some of the code as you learn. The project has a permissive license that allows you to use it freely.

To get started, [fork the example project on GitHub](https://github.com/redis-developer/fastapi-redis-tutorial).

[Follow the README](https://github.com/redis-developer/fastapi-redis-tutorial/blob/master/README.md) to the project running.

## Why use Redis for time series data?

Redis supports time series data. Time series is a great way to model any data that you want to query over time, like in this case, the ever-changing price of Bitcoin.

You can get started by following the [setup instructions](https://redis.io/docs/latest/develop/data-types/timeseries/) in the Redis documentation.

## How does async Redis work with FastAPI?

The IsBitcoinLit project is completely async. That means we use an asyncio-compatible Redis client and FastAPI's async features. The modern [redis-py](https://github.com/redis/redis-py) library includes built-in async support via `redis.asyncio`, so you no longer need the separate aioredis package (which is now deprecated and merged into redis-py).

If you **aren't familiar with asyncio**, take a few minutes to watch this primer on asyncio before continuing:

[YouTube: https://www.youtube.com/embed/Xbl7XjFYsN4](https://www.youtube.com/embed/Xbl7XjFYsN4)

## How do you install the Redis client for Python?

We're going to start this tutorial assuming that you have a FastAPI project to work with. We'll use the IsBitcoinLit project for our examples.

[Poetry](https://python-poetry.org/) is the best way to manage Python dependencies today, so we'll use it in this tutorial.

IsBitcoinLit includes a `pyproject.toml` file that Poetry uses to manage the project's directories, but if you had not already created one, you could do so like this:

```bash
    poetry init
```

Once you have a `pyproject.toml` file, and assuming you already added FastAPI and any other necessary dependencies, you can add redis-py to your project like this:

```bash
    poetry add redis
```

> **NOTE**
>
> This tutorial uses [redis-py](https://github.com/redis/redis-py), the official Redis client for Python. It supports both synchronous and async usage. The async API lives under `redis.asyncio` and replaces the now-deprecated aioredis package.

The redis-py client is now installed. Time to write some code!

## How do you integrate redis-py with FastAPI?

We're going to use Redis for a few things in this FastAPI app:

1.  Storing 30-second averages of sentiment and price for the last 24 hours with Redis Time Series
2.  Rolling up these averages into a three-hour snapshot with Redis Time Series
3.  Caching the three-hour snapshot

Let's look at each of these integration points in more detail.

### Creating the time series

The data for our app consists of 30-second averages of Bitcoin prices and sentiment ratings for the last 24 hours. We pull these from the [SentiCrypt API](https://senticrypt.com/docs.html).

> **NOTE**
>
> We have no affiliation with SentiCrypt or any idea how accurate these numbers are. This example is **just for fun**!

We're going to store price and sentiment averages in a time series with Redis, so we want to make sure that when the app starts up, the time series exists.

We can use a [startup event](https://fastapi.tiangolo.com/advanced/events/) to accomplish this. Doing so looks like the following:

```python
@app.on_event('startup')
async def startup_event():
    keys = Keys()
    await initialize_redis(keys)
```

We'll use the `TS.CREATE` command to create the time series within our `initialize_redis()` function:

```python
async def make_timeseries(key):
    """
    Create a timeseries with the Redis key `key`.

    We'll use the duplicate policy known as "first," which ignores
    duplicate pairs of timestamp and values if we add them.

    Because of this, we don't worry about handling this logic
    ourselves -- but note that there is a performance cost to writes
    using this policy.
    """
    try:
        await redis.execute_command(
            'TS.CREATE', key,
            'DUPLICATE_POLICY', 'first',
        )
    except ResponseError as e:
        # Time series probably already exists
        log.info('Could not create time series %s, error: %s', key, e)
```

> **TIP**
>
> When you create a time series, use the `DUPLICATE_POLICY` option to specify how to handle duplicate pairs of timestamp and values.

### Storing Sentiment and Price Data in Redis

A /refresh endpoint exists in the app to allow a client to trigger a refresh of the 30-second averages. This is the entire function:

```python
@app.post('/refresh')
async def refresh(background_tasks: BackgroundTasks, keys: Keys = Depends(make_keys)):
    async with httpx.AsyncClient() as client:
        data = await client.get(SENTIMENT_API_URL)
    await persist(keys, data.json())
    data = await calculate_three_hours_of_data(keys)
    background_tasks.add_task(set_cache, data, keys)
```

As is often the case with Python, a lot happens in a few lines, so let's walk through them.

The first thing we do is get the latest sentiment and price data from SentiCrypt. The response data looks like this:

```json
[
    {
        "count": 7259,
        "timestamp": 1625592626.3452034,
        "rate": 0.0,
        "last": 0.33,
        "sum": 1425.82,
        "mean": 0.2,
        "median": 0.23,
        "btc_price": "33885.23"
    }
    //... Many more entries
]
```

Then we save the data into two time series in Redis with the `persist()` function. That ends up calling another helper, `add_many_to_timeseries()`, like this:

```python
    await add_many_to_timeseries(
        (
            (ts_price_key, 'btc_price'),
            (ts_sentiment_key, 'mean'),
        ), data,
    )
```

The `add_many_to_timeseries()` function takes a list of (time series key, sample key) pairs and a list of samples from SentiCrypt. For each sample, it reads the value of the sample key in the SentiCrypt sample, like "btc_price," and adds that value to the given time eries key.

Here's the function:

```python
async def add_many_to_timeseries(
    key_pairs: Iterable[Tuple[str, str]],
    data: BitcoinSentiments
):
    """
    Add many samples to a single timeseries key.

    `key_pairs` is an iteratble of tuples containing in the 0th position the
    timestamp key into which to insert entries and the 1th position the name
    of the key within th `data` dict to find the sample.
    """
    partial = functools.partial(redis.execute_command, 'TS.MADD')
    for datapoint in data:
        for timeseries_key, sample_key in key_pairs:
            partial = functools.partial(
                partial, timeseries_key, int(
                    float(datapoint['timestamp']) * 1000,
                ),
                datapoint[sample_key],
            )
    return await partial()
```

This code is dense, so let's break it down.

We're using the `TS.MADD` command to add many samples to a time series. We use `TS.MADD` because doing so is faster than `TS.ADD` for adding batches of samples to a time series.

This results in a single large `TS.MADD` call that adds price data to the price time series and sentiment data to the sentiment timeseries. Conveniently, `TS.MADD` can add samples to multiple time series in a single call.

## How do you calculate time series averages with Redis?

Clients use IsBitcoinLit to get the average price and sentiment for each of the last three hours. But so far, we've only stored 30-second averages in Redis. How do we calculate the average of these averages for the last three hours?

When we run `/refresh`, we call `calculate_three_hours_of_data()` to do so. The function looks like this:

```python
async def calculate_three_hours_of_data(keys: Keys) -> Dict[str, str]:
    sentiment_key = keys.timeseries_sentiment_key()
    price_key = keys.timeseries_price_key()
    three_hours_ago_ms = int((now() - timedelta(hours=3)).timestamp() * 1000)

    sentiment = await get_hourly_average(sentiment_key, three_hours_ago_ms)
    price = await get_hourly_average(price_key, three_hours_ago_ms)

    last_three_hours = [{
        'price': data[0][1], 'sentiment': data[1][1],
        'time': datetime.fromtimestamp(data[0][0] / 1000, tz=timezone.utc),
    }
        for data in zip(price, sentiment)]

    return {
        'hourly_average_of_averages': last_three_hours,
        'sentiment_direction': get_direction(last_three_hours, 'sentiment'),
        'price_direction': get_direction(last_three_hours, 'price'),
    }
```

There is more going on here than we need to know for this tutorial. As a summary, most of this code exists to support calls to `get_hourly_average()`.

That function is where the core logic exists to calculate averages for the last three hours, so let's see what it contains:

```python
async def get_hourly_average(ts_key: str, top_of_the_hour: int):
    response = await redis.execute_command(
        'TS.RANGE', ts_key, top_of_the_hour, '+',
        'AGGREGATION', 'avg', HOURLY_BUCKET,
    )
    # The response is a list of the structure [timestamp, average].
    return response
```

Here, we use the `TS.RANGE` command to get the samples in the timeseries from the "top" of the hour three hours ago, until the latest sample in the series. With the `AGGREGATE` parameter, we get back the averages of the samples in hourly buckets.

So where does this leave us? With **averages of the averages**, one for each of the last three hours.

## How do you cache data with Redis in FastAPI?

Let's review. We have code that achieves the following:

1.  Gets the latest sentiment and price data from SentiCrypt.
2.  Saves the data into two time series in Redis.
3.  Calculates the average of the averages for the last three hours.

The snapshot of averages for the last three hours is the data we want to serve clients when they hit the `/is-bitcoin-lit` endpoint. We could run this calculation every time a client requests data, but that would be inefficient. Let's cache it in Redis!

First, we'll look at **writing to the cache**. Then we'll see how FastAPI **reads from** the cache.

### How do you write cache data to Redis?

Take a closer look at the last line of the `refresh()` function:

```python
    background_tasks.add_task(set_cache, data, keys)
```

In FastAPI, you can run code outside of a web request after returning a response. This feature is called [background tasks](https://fastapi.tiangolo.com/tutorial/background-tasks/).

This is not as robust as using a background task library like [Celery](https://docs.celeryproject.org/en/stable/getting-started/introduction.html). Instead, Background Tasks are a simple way to run code outside of a web request, which is a great fit for things like updating a cache.

When you call `add_task()`, you pass in a function and a list of arguments. Here, we pass in `set_cache()`. This function saves the three-hour averages summary to Redis. Let's look at how it works:

```python
async def set_cache(data, keys: Keys):
    def serialize_dates(v):
        return v.isoformat() if isinstance(v, datetime) else v

    await redis.set(
        keys.cache_key(),
        json.dumps(data, default=serialize_dates),
        ex=TWO_MINUTES,
    )
```

First, we serialize the three-hour summary data to JSON and save it to Redis. We use the `ex` parameter to set the expiration time for the data to two minutes.

**TIP**: You need to provide a default serializer for the `json.dumps()` function so that `dumps()` knows how to serialize datetime objects.

This means that after every refresh, we've primed the cache. The cache isn't primed for long -- only two minutes -- but it's something!

### How do you read cached data from Redis?

We haven't even seen the API endpoint that clients will use yet! Here it is:

```python
@app.get('/is-bitcoin-lit')
async def bitcoin(background_tasks: BackgroundTasks, keys: Keys = Depends(make_keys)):
    data = await get_cache(keys)

    if not data:
        data = await calculate_three_hours_of_data(keys)
        background_tasks.add_task(set_cache, data, keys)

    return data
```

To use this endpoint, clients make a GET request to `/is-bitcoin-lit`. Then we try to get the cached three-hour summary from Redis. If we can't, we calculate the three-hour summary, return it, and then save it outside of the web request.

We've already seen how calculating the summary data works, and we just explored saving the summary data to Redis. So, let's look at the `get_cache()` function, where we read the cached data:

```python
def datetime_parser(dct):
    for k, v in dct.items():
        if isinstance(v, str) and v.endswith('+00:00'):
            try:
                dct[k] = datetime.datetime.fromisoformat(v)
            except:
                pass
    return dct

async def get_cache(keys: Keys):
    current_hour_cache_key = keys.cache_key()
    current_hour_stats = await redis.get(current_hour_cache_key)

    if current_hour_stats:
        return json.loads(current_hour_stats, object_hook=datetime_parser)
```

Remember that when we serialized the summary data to JSON, we needed to provide a default serializer for `json.dumps()` that understood datetime objects. Now that we're _deserializing_ that data, we need to give `json.loads()` an "object hook" that understands datetime strings. That's what `datetime_parser()` does.

Other than parsing dates, this code is relatively straightforward. We get the current hour's cache key, and then we try to get the cached data from Redis. If we can't, we return `None`.

## Summary

Putting all the pieces together, we now have a FastAPI app that can retrieve Bitcoin price and sentiment averages, store the averages in Redis, cache three-hour summary data in Redis, and serve the data to clients. Not too shabby!

Here are a few **notes to consider**:

1.  We manually controlled caching in this tutorial, but you can also use a library like [aiocache](https://github.com/aio-libs/aiocache) to cache data in Redis.
2.  We ran Redis commands like `TS.MADD` using the `execute_command()` method in redis-py. The same commands work in both synchronous and async contexts.

## Next steps

Now that you've built a FastAPI app with Redis, here are some ways to keep learning:

- **Try Redis OM for Python** — If you want a higher-level, declarative way to model and query data in Redis, check out the [Getting Started with Redis OM for Python](/tutorials/develop/python/redis-om/) tutorial.
- **Explore redis-py** — Dive deeper into the official Python client with the [redis-py documentation](https://redis.io/docs/latest/develop/clients/redis-py/).
- **Learn more about Redis Time Series** — Read the [Redis Time Series documentation](https://redis.io/docs/latest/develop/data-types/timeseries/) to explore advanced aggregation and filtering options.
- **Add session management** — Use Redis as a session store for your FastAPI app to handle user authentication at scale.
