---
title: "Announcing RedisGears 1.0: A Serverless Engine for Redis"
linkTitle: "Announcing RedisGears 1.0: A Serverless Engine for Redis"
url: "/blog/redisgears-serverless-engine-for-redis/"
description: "We are happy to announce the general availability of RedisGears, a serverless engine that provides infinite programmability in Redis. Developers can use RedisGears to improve application..."
date: 2020-05-19
blogCategories:
- "Product Releases"
- "Redis Modules"
authors:
- "Pieter Cailliau"
- "Meir Shpilraien"
lastmod: 2025-07-03
hidden: true
---

*By Pieter Cailliau, Meir Shpilraien · Published 19 May 2020 · updated 3 July 2025*

![Blog tile image](/images/site-mirror/b640163838128b5e6330d2317abbc3ca57ac617c-601x601.webp)

We are happy to announce [the general availability of RedisGears](/press/redis-labs-delivers-powerful-data-platform-for-next-wave-of-ai-applications), a serverless engine that provides infinite programmability in Redis. Developers can use [RedisGears](/redis-enterprise/redis-gears/) to improve application performance and process data in real time, while architects can leverage it to drive architectural simplicity.

As a dynamic framework for the execution of [functions](https://oss.redis.com/redisgears/functions.html) that implement data flows in Redis, RedisGears abstracts away the data’s distribution and deployment to speed data processing using multiple models in Redis. RedisGears lets you program everything you want in Redis, deploy functions to every environment, simplify your architecture and reduce deployment costs, and run your serverless engine where your data lives.

RedisGears can be deployed for a variety of use cases:

- **Real-time data processing,** since it runs embedded in Redis
- **Reliable event processing**, such as new messages in streams or updates of entities in Redis, and
- **Operations across multiple data structures** and data models in a transparent manner across shards.

## RedisGears is GA

In addition to announcing RedisGears, we’re also unveiling its first recipe. A “recipe” is a set of functions—and any dependencies they might have—that together address a higher-level problem or use case. Our first recipe is **rgsync**. Also referred to as **write-behind**, this capability lets you treat Redis as your frontend database, while RedisGears guarantees that all changes are written to your existing databases or data warehouse systems.

To help you understand the power of RedisGears, we’ll begin with an explanation of RedisGears architecture and its benefits. Then we’ll discuss how these benefits apply to write-behind and we’ll demonstrate its behavior via a demo application we created.

## RedisGears architecture

At the core of RedisGears is an engine that executes user-provided flows, or functions, through a programmable interface. Functions can be executed by the engine in an ad-hoc map-reduce fashion, or triggered by different events for event-driven processing. The data stored in Redis can be read and written by functions, and a built-in coordinator facilitates processing distributed data in a cluster.

In broad strokes, this diagram depicts RedisGears’ components:

![](/images/site-mirror/80b46c9873a71902d48ef035a672819dcdb4e997-1024x582.webp)

*RedisGears architecture and data flow*

RedisGears has three main components:

1. **GearsCoordinator** orchestrates the distributed execution of your functions on each shard in your database.
1. **GearsExecuter** schedules and triggers the execution of your functions. Functions can be triggered ad-hoc, by new entries in a stream, or by keyspace notification. In the latter, the function can be [synchronously executed](https://oss.redis.com/redisgears/functions.html#register) with the notification. (The GearsExecutor is not visible in the above diagram, but implied by the events/trigger section.)
1. **GearsEngine** is the runtime execution environment of RedisGears.

On top of these three core components, RedisGears includes a fast low-level C-API for programmability. You can integrate this C-API via Python today, with more languages in the works.

RedisGears minimizes the execution time and the data flow between shards by running your functions as close as possible to your data. By putting your serverless engine in memory, where your Redis data lives, it eliminates the time-consuming round trips needed to fetch data, speeding processing of events and streams.

RedisGears lets you “write once, deploy anywhere.” You can write your functions for a standalone Redis database and deploy them to production without having to adapt your script for a clustered database.

Combining real-time data with a serverless engine lets you process data across data structures and data models without the overhead of multiple clients and database connectors. This simplifies your architecture and reduces deployment costs.

## Write-behind

The ability to cope with sudden spikes in the number of users/requests is something modern companies and organizations must consider. Black Friday and Cyber Monday traffic, for example, can dwarf that of ordinary days.

Failure to plan for such peaks can lead to poor performance, unexpected downtime, and ultimately lost revenue. On the other hand, over-scaling your solution to these peaks can also be expensive. The key is to find a cost-efficient solution that can meet your demands and requirements.

Traditional relational/disk-based databases are often unable to deal with significant increases in load. This is where RedisGears comes into play. RedisGears’ write-behind capability relies on Redis to do the heavy lifting, asynchronously managing the updates and easing the load and diminishing the spikes on the backend database. RedisGears also guarantees that all changes are written to your existing databases or data warehouse systems, protecting your application from database failure and boosting the performance of your application to the speed of Redis. This simplifies your application logic drastically since it now only needs to talk to a single frontend database, Redis. The write-behind capability comes initially with support for Oracle, MySQL, SQL, SQLite, Snowflake, and Cassandra.

![](/images/site-mirror/f63a39371ae28de90a67858d0aacd7057cd22095-1024x473.webp)

*RedisGears helps flatten the curve of your database workload.*

## Write-behind implementation

The diagram below displays the architecture of RedisGears’ write-behind capability:

![](/images/site-mirror/8b1aeb89b0cf43d555b7a70471c7426952f887c3-1024x601.webp)

*Mapping Redis data structures and RedisGears functions to the write-behind capability.*

It operates as follows:

1. A write operation happens to a Redis hash key.
1. This write triggers the execution of a *first RedisGears function* that synchronously records the change in a Redis Stream.
1. When and only when the event is successfully added to the stream, an acknowledgement is returned to the client.
1. A *second RedisGears function* is executed asynchronously in the background and batches the changes to the target database. This function is triggered by the new messages in the stream.

Together those two functions make up what we call a “recipe” for RedisGears. (Note that the recipe for write-behind is bundled in the [rgsync](https://github.com/RedisGears/rgsync/) (RedisGears sync) package, along with several other database-syncing recipes.)

As noted above, step three happens only when the event was successfully added to the stream. This means that if something goes wrong after the client gets the acknowledgement of the write operation, Redis replication, auto-failover, and data persistence mechanisms guarantee that the update event will not be lost. By default, the write-behind RedisGears capability provides the *at least once delivery* property for writes, meaning that data will be written once to the target, but possibly more than that in case of failure. It is possible to set the RedisGears function to provide *exactly onc*e delivery semantics if needed, ensuring that any given write operation is executed only once data is on the target database.

**Improving application performance with write-behind**

To showcase the benefits of write-behind, we developed a [demo application](https://github.com/RedisGears/WriteBehindDemo) in which we’ve added endpoints to enable two scenarios:

1. The application server writes directly to the backend database.
1. The application treats Redis as a frontend database and RedisGears does the write-behind to the backend database.

In this example, we used MySQL as the backend database for ease of testing and reproduction.

![](/images/site-mirror/ebb132bb07faee79d4f98982ab3c79daf3f925f2-827x892.webp)

*What your application looks like with and without write-behind.*

To simulate peaks in the application, we’ve created a spike test with [k6](https://k6.io/), in which we simulate a short burst going from 1 to 48 concurrent users.

To check how the overall system handled the spike, we tracked the achieved HTTP load and latency on the application as well as the underlying database system performance. The graph below showcases both scenarios—the left interval presents results for the MySQL-only solution, while the right interval presents results for the write-behind scenario with RedisGears.

![Redis](/images/site-mirror/96fad5013179ce0f2af3ff2fda3970892637f03d-960x540.webp)

This chart displays some important findings:

1. At the application level, the application requests chart shows that we’ve passed from serving up to 5K requests per second to **serving up to 4X more requests**, with the same underlying hardware.
1. The database chart indicates a rise in MySQL’s number of inserts/updates per second. This is because write-behind batches updates to the backend database into a single request (this is possible only because in this scenario, the frontend application is decoupled from the backend database). This is a win-win situation, since your HTTP application doesn’t have to wait for the database-write operation to finish, and you can also do more with the resources that you originally sized your backend database for—you’re getting more out of it “for free.”
1. As expected, and directly related to the removal of synchrony between your fast application and your slow backend database with the addition of RedisGears, we’ve moved from 95th quantile application latencies values of 32 milliseconds to latencies below 10 milliseconds. Instead of waiting an average of 8 milliseconds for an application reply, it takes just 2 milliseconds. Not only will your applications run faster, but—even more important—they will also be more stable and resilient.

## Get started with RedisGears

We are really excited about RedisGears and write-behind. We believe that the write-behind use case is only the beginning of the infinite problems that RedisGears can solve.

We hope that this blog post has encouraged you to try RedisGears. Please check out [RedisGears.io](http://redisgears.io), which contains tons of examples and hints on how to get started. You can find more cool demos here:

- [Prophet Gears](https://github.com/RedisGears/ProphetGears), using [Facebook prophet](https://facebook.github.io/prophet/) and RedisTimeSeries for batch process of time series data prediction
- [Animal Recognition Demo](https://github.com/RedisGears/AnimalRecognitionDemo) is an example of using Redis Streams, RedisGears, and RedisAI for real-time video analytics (i.e. detecting cats in your webcam stream).
- [Edge Real-Time Video Analytics](https://github.com/RedisGears/EdgeRealtimeVideoAnalytics) is a demo combining Redis Streams, RedisAI, and RedisTimeSeries, glued together with RedisGears.

A new version of RedisInsight will be released soon and will contain support for RedisGears to execute functions and to view the registered functions in RedisGears. We’ll leave you with a quick GIF of what you can expect:

![Redis](/images/site-mirror/aab4f0d4865be08232b3436b1e0cff3f1936554b-800x533.gif)

Happy coding!
