---
title: "How fast is flash?"
linkTitle: "How fast is flash?"
url: "/blog/how-fast-is-flash/"
description: "With Redis Enterprise, we recently enabled the ability to extend your RAM based storage into Flash memory. Don’t confuse this with some form of persistence– this is a way to let Redis break out of..."
date: 2017-10-20
blogCategories:
- "Company"
- "Tech"
authors:
- "Redis  "
lastmod: 2025-03-27
hidden: true
mirrored: true
---

*By Redis   · Published 20 October 2017 · updated 27 March 2025*

![Blog tile image](/images/site-mirror/00a45a3e0e033dc16f1ef61ab4c854ea99c0c4e4-1324x132.webp)

## Exploring the performance of Redis Enterprise with Flash memory extension.

With Redis Enterprise, we recently enabled the ability to extend your RAM based storage into Flash memory. Don’t confuse this with some form of persistence– this is a way to let Redis break out of the bounds of the server RAM and into Flash storage as needed. With the advances in Flash memory (NVMe-based SSD storage), the performance becomes very viable, although not quite as quick as RAM alone. This allows you to have hybrid storage -in which data moves between fast RAM and Flash as needed, all managed by Redis Enterprise and without changes to your code.

Let’s take a look at the performance characteristics of Redis Enterprise on Flash and how you can test the performance yourself. We suggest installing Redis Enterprise directly [as described in our documentation](/redis-enterprise-documentation/administering/installing-upgrading/downloading-installing/). While we offer instructions on how to use Docker to install Redis Enterprise to test out the product, in this case that method will not yield the highest performance.

To best utilize the Flash memory capabilities, we suggest using i3.2xlarge AWS instances. These instances have Non-Volatile Memory Express (NVMe) SSD drives that are key to high-performance hybrid memory extension. The test setup is as follows:

- 2 x i3.2xlarge for serving data
- 1 x m4.large as a quorum node
- 1 x c4.8xlarge as a load generator

Load generation is provided by the [memtier_benchmark](https://github.com/RedisLabs/memtier_benchmark). This should be in the same region/zone/subnet of your cluster, but should be in a dedicated instance.

For this benchmark, we’ll focus on a cluster with replication. Here are some more specifications of our test setup:

| Memory Limit | 100 GB | The limit of the storage in RAM+Flash. |
|---|---|---|
| RAM Limit | 30% | Keys and “hot values” are always stored in RAM. |
| Data Persistence | None | Persistence is not enable to simplify the setup and reduce variables in the test. |
| Clustering / Shards | Yes – 2 Shards | One master shard and one slave shard on each node. |
| Replication | Yes (checked) | Replication is typical in deployments and is thus included in this benchmark, although not required for Redis Enterprise with Flash. |


Everything else should use the default settings.

## Populate the dataset

We’ll use memtier_benchmark to fill the database using these arguments:

```javascript
$ memtier_benchmark -s your-nodes-fully-qualified-name-or-ip-endpoint -p your-endpoint-port --hide-histogram --key-maximum=75000000 -n allkeys -d 500 --key-pattern=P:P --ratio=1:0
```

You will need to alter the values of the two items in red. You can find the endpoint address and port on the Redis Enterprise dashboard by selecting your database on the Database page and then clicking on the Configuration tab; the table should have a line that looks similar to this:

![](/images/site-mirror/00a45a3e0e033dc16f1ef61ab4c854ea99c0c4e4-1324x132.webp)

This benchmark will fill the database with 75 million keys each with a 500 byte payload.

The next step is centralization of your keys – effectively, we’ll be loading keys around the median into RAM with the rest being in Flash. This process allows for simulating a more realistic access pattern and controls for the otherwise random nature of the benchmark (which wouldn’t reflect realistic access patterns). This will also mean that subsequent tests will be more consistent. You can [read more about this feature on a previous blog post about memtier_benchmark](/blog/new-in-memtier_benchmark-pseudo-random-data-gaussian-access-pattern-and-range-manipulation/).

To centralize, we’ll generate about 20.5 million items in RAM by running:

```javascript
$ memtier_benchmark -s your-nodes-fully-qualified-name-or-ip-endpoint -p your-endpoint-port --hide-histogram --key-minimum=27250000 --key-maximum=47750000 -n allkeys --key-pattern=P:P --ratio=0:1
```

Now that we have prepped the database, let’s generate some load now that we’ve prepped the database.

```javascript
$ memtier_benchmark -s your-nodes-fully-qualified-name-or-ip-endpoint -p your-endpoint-port --pipeline=11 -c 20 -t 1 -d 500 --key-maximum=75000000 --key-pattern=G:G --key-stddev=5125000 --ratio=1:1 --distinct-client-seed --randomize --test-time=600 --run-count=1 --out-file=test.out
```

Once you’ve got your test running you’ll be able to monitor the results in the Redis Enterprise dashboard. You should see about 115,000 ops/sec with sub-millisecond latency in this access pattern. It’s also important to note that you may see lower values if you’re looking at the output of memtier_benchmark itself, but this takes the network latency into account, so it’s not really measuring Redis Enterprise directly.

This experiment shows that you can achieve an average throughput of more than 100,000 ops/sec at a sub-millisecond latency with only four shards running on a three-node cluster with two serving nodes, which meets the performance requirements of many real world database use cases. In case more throughput or memory is needed, you can scale your cluster by adding more shards and nodes.

If you wanted to build a RAM-only version of this database, you’d need three times the number of nodes. Which, in turn, would translate to three times the infrastructure cost for running the database. Using F lash as a RAM extension provides quite the savings.

To get started with Redis Enterprise Flash please visit the quick setup instructions [here](https://docs.redis.com/latest/rs/databases/redis-on-flash/rof-quickstart/). To find out more about Redis Flash architecture, refer to the [Redis Enterprise Flash Architecture blog post](/blog/hood-redis-enterprise-flash-database-architecture/). You can start a [Redis Enterprise Flash free trial here](/redis-enterprise/technology/redis-on-flash/). Finally to find out more about the performance characteristics of Redis Enterprise with Flash memory extension, [contact us](/meeting/).
