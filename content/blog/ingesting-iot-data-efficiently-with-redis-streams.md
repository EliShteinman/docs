---
title: "Ingesting IoT Data Efficiently with Redis Streams"
linkTitle: "Ingesting IoT Data Efficiently with Redis Streams"
url: "/blog/ingesting-iot-data-efficiently-with-redis-streams/"
description: "Before joining Redis, I worked for a consultant firm working with technologies like the Internet of Things (IoT). If you’re not familiar with the concept, IoT is all about smart devices connected..."
date: 2020-04-27
blogCategories:
- "Tech"
authors:
- "Redis  "
lastmod: 2026-09-01
hidden: true
---

*By Redis   · Published 27 April 2020 · updated 1 September 2026*

![Blog tile image](/images/site-mirror/0073e867b4e64f59de9047fdcde04295ba647e5c-772x550.webp)

Before joining Redis, I worked for a consultant firm working with technologies like the Internet of Things (IoT). If you’re not familiar with the concept, [IoT](https://www.wired.co.uk/article/internet-of-things-what-is-explained-iot) is all about smart devices connected to the internet. Many of these devices include sensors that produce metrics about the real world. One notable IoT use case, for example, are bike sharing companies, where the bike itself is connected to the internet and constantly notifies its owners of its location and other conditions. But perhaps the biggest, most promising uses of IoT technology come in factories, or the industrial internet of things ([IIoT](https://www.zdnet.com/article/what-is-the-iiot-everything-you-need-to-know-about-the-industrial-internet-of-things/)).

While the IoT opens a window on a great range of possibilities, with market predictions topping $1 trillion within a few years, and some [41.6 billion IoT devices expected to generate 79.4 zettabytes of data](https://www.helpnetsecurity.com/2019/06/21/connected-iot-devices-forecast/), there are still challenges to be overcome when implementing services based on IoT, primarily around handling IoT data at scale.

## Handling IoT data at scale

Going back to my consultant experience, I remember meeting with a data science team from a company that had issues with its IoT solution. The main conundrum the team faced was about storing data in a NoSQL document-based database. They were trying to decide between two data models, where one would optimize for query speed, while the other would optimize for space efficiency.

The first model consisted in storing one datapoint per document, like this:

```javascript
{
    “Id”: “1-2-3”,
    “Time”: 123123123,
    “Longitude”: 0.123,
    “Latitude”: 0.123,
    “Battery”: 0.66
}
```

This approach would yield the fastest query speed, but on the downside it would take up a lot of storage space. The other model, designed to use space more efficiently, looked like this:

```javascript
{
    “ChunkId”: “abc”,
    “ChunkStartTime”: 123123123,
    “Chunk”:[
        [
            “1-2-3”,
            123123123,
            0.123,    
            0.123,
            0.66
        ],
        [
            “4-5-6”,
            456456456,
            0.456,
            0.456,
            0.99
        ],
        ...
    ]
}
```

As you can see, this second model is more complex: each document holds multiple data points in a single chunk. This model required more-complicated queries to account for the chunks, but in exchange it provided some space savings.

At the time I didn’t have a good solution to this problem, but now I realize that with Redis Streams the problem doesn’t exist in the first place.

## Ingesting IoT data in Redis Streams

When you have a stream of miscellaneous data that is time-directed and intrinsically immutable, as is usually the case with IoT data, Redis Streams are probably the right data structure for the initial ingestion.

A Redis Stream key contains an indexed list of entries. Each index ID is a millisecond-precise timestamp followed by a sequence number for events that happen within the same millisecond. Each entry is a sequence of field-value pairs, almost the same as a Redis Hash. “Almost” because Redis Hashes are a good way to visualize what you can put in a stream except for one small difference: a Redis Stream entry can have multiple instances of the same field, while fields in a Redis Hash are unique.

The following command shows how to add an entry to a Redis Stream. Check out [the documentation](https://redis.io/docs/latest/develop/) to learn more.

> XADD mystream * time 123123123 lon 0.123 lat 0.123 battery 0.66

Redis Streams are indexed using a [radix tree](https://en.wikipedia.org/wiki/Radix_tree) data structure that compresses index IDs and allows for constant-time access to entries.

## The hidden cost of field names

Redis Streams also employ another smart space-saving mechanism that applies to field names.

You might not think about it often, but the names that you choose for your entry fields impact how much space each entry takes. With SQL databases the problem doesn’t come up because the schema is fixed at the table level, but the downside is that you lose flexibility. With NoSQL, document-based databases you get more flexibility but then documents have the overhead of saving the strings representing field names over and over again.

In Redis Streams, each entry in a stream can have a different set of fields, so you can have as much flexibility as you need, but if you keep the set of fields stable, Redis will not store multiple copies of their names. Depending on the number of fields you have, the amount of overhead you avoid with this feature can be significant.

As a simple example, imagine you have 1 million entries, 20 fields each, with an average field-name length of 15 bytes. This translates to roughly 300 megabytes of overhead you avoid for each million items.

## Next steps

While Redis Streams are a perfect fit for internet of things use cases, they are hardly limited to only IoT. Inversely there are many more data structures in Redis that can help you save space when ingesting data at scale, including [probabilistic data structures](/blog/streaming-analytics-with-probabilistic-data-structures/), for example.

After you have mastered Redis Streams, consider using the [RedisTimeSeries](/blog/redistimeseries-version-1-2-is-here/) module for storing numeric time-series data derived from the raw data you ingested. If you want to learn more about both Redis Streams and [RedisTimeSeries](http://redistimeseries.io), sign up for our training day at [RedisConf](http://redisconf.com) [2020](http://redisconf.com)[* Takeaway*](http://redisconf.com)[, occuring online ](http://redisconf.com)on May 12-13.
