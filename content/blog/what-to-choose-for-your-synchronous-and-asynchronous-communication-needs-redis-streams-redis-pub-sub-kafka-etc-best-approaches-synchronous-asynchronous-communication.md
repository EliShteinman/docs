---
title: "What to Choose for Your Synchronous and Asynchronous Communication Needs—Redis Streams, Redis Pub/Sub, Kafka, etc."
linkTitle: "What to Choose for Your Synchronous and Asynchronous Communication Needs—Redis Streams, Redis Pub/Sub, Kafka, etc."
url: "/blog/what-to-choose-for-your-synchronous-and-asynchronous-communication-needs-redis-streams-redis-pub-sub-kafka-etc-best-approaches-synchronous-asynchronous-communication/"
description: "Let’s talk about communication tools and patterns. With the introduction of Streams in Redis, we now have another communication pattern to consider in addition to Redis Pub/Sub and other tools like..."
date: 2019-05-03
blogCategories:
- "Tech"
authors:
- "Redis  "
lastmod: 2026-09-01
hidden: true
---

*By Redis   · Published 3 May 2019 · updated 1 September 2026*

![Blog tile image](/images/blog/cf158c174f42fcf8888ac4679f389f38a3c5fef0-4500x3000.webp)

Let’s talk about communication tools and patterns. With the introduction of Streams in Redis, we now have another communication pattern to consider in addition to Redis Pub/Sub and other tools like [Kafka](https://redis.io/compare/redis-enterprise-and-kafka/) and RabbitMQ. In this article, I will guide you through the defining characteristics of various communication patterns, and I’ll briefly introduce the most popular tools used to implement each. Finally, I’ll leave you with a small take-away that will hopefully help you build better solutions faster.

## Synchronous communication

In this context, synchronous means that all parties need to be active at the same time to be able to communicate. The simplest form is Service A and Service B doing direct remote procedure calls (RPC), by invoking Service B’s HTTP REST endpoint from Service A, for example. If Service B went offline, Service A would not be able to communicate with B, and so A would need to implement an internal failure recovery procedure, which most of the time means doing graceful degradation. For example, Netflix’s “watch next” section could display a random sample of shows if the recommendation service was unreachable.

These services only do graceful degradation because for more sensitive use cases (e.g., a payment service asking an order service to start processing a paid order), other asynchronous mechanisms I’ll describe below are more common. And while the RPC paradigm works well for one-to-one communication, you will occasionally need to support one-to-many or many-to-many. At that point, you have two main options: brokerless or brokered tools.

### Brokerless

Brokerless means that participants are still connected directly but have the option of employing a different pattern than RPC. In this category, we have libraries such as [ZeroMQ](http://zeromq.org/) and the more recent [nanoMsg](https://nanomsg.org/). They are rightfully described as “TCP sockets on steroids.” In practice, you import the library into your code and use it to instantiate a connection that can employ various built-in message routing mechanisms, such as Pub/Sub, Push/Pull, Dealer/Router, etc.

### Brokered

Brokered means that participants connect to the same service, which acts, as the name suggests, as a central broker to implement the whole message-routing mechanism. While this architecture is usually described as star-shaped, with the broker being the center of the star, the broker itself can be (and often is) a clustered system.

In this category, Redis Pub/Sub stands alone as far as I know. You can still use tools with persistence like NATS or RabbitMQ for this use case, as they do allow you to turn off persistence, but the only pure synchronous messaging broker that I know of is Redis. The difference is not just in persistence, but in the general idea of reliable delivery (i.e., application level acks) vs. fire-and-forget. RabbitMQ defaults to the former behavior while Redis Pub/Sub focuses on just doing the bare minimum amount of work for fire-and-forget. As you can imagine, this has implications in performance (there’s no such thing as a free lunch after all), but reliable delivery does apply to a wider range of use cases.

Since Streams was not available before Redis version 5, some people opted to use Pub/Sub in situations where they would have preferred better delivery guarantees, and are now making the switch. So, if you’re building a new application or unsatisfied with a current one that uses Pub/Sub, consider Redis Streams if what you need is “Pub/Sub, but with the ability to resume on disconnection without losing messages.”

### Pros and cons

Brokerless tools are the fastest communication methodology you can think of, even faster than Redis Pub/Sub. They unfortunately cannot abstract away all complexity — such as the need for each participant to know the location of all others in order to connect to them, or complex failure scenarios that you don’t generally have to deal with in brokered systems (e.g., the case where a participant dies mid-fanout).

The beauty of using Redis Pub/Sub, in this case, lies in not having to give up too much throughput and getting in return a simple, ubiquitous infrastructure with a small integration surface. You only need a Redis client for your language, and can use [PUBLISH](https://redis.io/commands/publish) and [(P)SUBSCRIBE](https://redis.io/commands/subscribe) to move messages around.

## Asynchronous communication

Of course, asynchronous means communication can still happen even if not all participants are present at the same time. To enable this pattern, persisting messages is mandatory, otherwise there would be no way to guarantee delivery in the face of failures. Tools in this category mainly consist of queue-based or stream-based solutions.

### Queue-based async communication

This is the “traditional” way of doing asynchronous communication and the base for most service oriented architectures (SOAs). The idea is that when a service needs to communicate with another, it leaves a message in a central system that the other service will pick up later. In practice, these message inboxes are like task queues.

Another expectation for these systems is that tasks be independent from one another. This means that they can be (and almost always are) processed in parallel by multiple identical consumers, usually referred to as workers. This property also enables independent failure, which is a good feature for many workloads. As an example, being unable to process a payment from one user (maybe because of missing profile information or other trivial problems) would not stop the whole payment processing pipeline for all users.

The most well-known tool in this category is RabbitMQ, followed by a plethora of other tools and cloud services that mostly speak AMQP (Rabbit’s native protocol) or MQTT (a similar open standard). It is common practice to use RabbitMQ through frameworks that offer an easy way to implement various retry policies (e.g., exponential backoff and dead-letter) plus a sugared interface that makes handling messages more idiomatic in specific client ecosystems. Some of these frameworks are “humble” task queues such as [Sidekiq](https://sidekiq.org/) (Ruby), [Celery](http://www.celeryproject.org/) (Python), [Dramatiq](https://dramatiq.io/) (Python), etc. Others are “more serious” enterprise service buses (ESBs), like [NServiceBus](https://particular.net/nservicebus) (C#), [MassTransit](https://masstransit-project.com/) (C#), [Apache Synapse](https://synapse.apache.org/) (Java) or [Mulesoft](https://www.mulesoft.com/) (Java).

The simpler version of this pattern (task queues) can also be implemented using Redis Lists directly. Redis has blocking and atomic operations that make building bespoke solutions very easy. A special mention goes to [Kue](https://github.com/Automattic/kue), which uses Redis in a nifty implementation of task queues for JavaScript.

### Stream-based async communication

First of all, it’s worth noting that the simplest way of using streams is just as a form of storage. Streams are an immutable, append-only series of time-directed entries, and many types of data fit naturally into that format. For example, sensor readings or logs contain values that by nature are indexed by creation time and are append-only (you can’t change the past). They also have fairly regular structure (since they tend to keep the same set of fields), a property that streams can exploit for better space efficiency. This type of data fits well in a stream because the most direct way of accessing the data is by retrieving a given time range, which streams can do in a very efficient way.

Back to our communication use case, all streams implementations also allow clients to tail a stream, receiving live updates as new entries get added. This is sometimes called observing or subscribing to the stream. The simplest way to use Streams as a communication tool is to push to a stream what you would otherwise publish over Pub/Sub, basically creating a resumable Pub/Sub. Every subscriber just needs to remember the last entry-id it processed, so it can easily resume if there’s a crash or disconnection.

It is also possible – and sometimes preferable – to implement service-to-service communication over streams, entering the realm of **streaming architectures**. The main concept here is that what we previously described as tasks/messages, would now be an event. With a queue-based design, tasks get pushed to a service’s queue by another service that wants it to do something, but in a streaming architecture, the inverse happens: every service pushes state updates to its own stream, which is in turn observed by other services.

There are many subtle implications from this change in design. As an example, you can add new services later and have them go through the whole stream history. In queues, this is not possible because tasks get deleted once completed and the way communication is generally expressed in those systems does now allow for this (think imperative vs. functional).

Streams have a dual nature: data structure and communication pattern. Some data fits into this naturally (e.g., logs) and communication between services doesn’t necessarily have to be based on task queues. The practice of fully embracing this dual nature is called [event sourcing](https://martinfowler.com/eaaDev/EventSourcing.html).

With **event sourcing**, you define your business models as an endless stream of events and let the business logic and other services react to it. It’s not always easy to do this translation, but the benefits can be great when dealing with hard questions such as “what was the state of object X at time Y?”, which would otherwise be very hard to answer or straight impossible without proper audit logging.

Maybe your run-of-the-mill mobile application doesn’t need event sourcing, but for enterprise software that has to deal with customers’ personal data, shipping, and other “messy” domains, it can be of great help.

To implement these kinds of patterns, there are plenty of tools you can use. Of course, we should start with the elephant in the room: Apache Kafka, as well as alternatives like Apache Pulsar (from Yahoo) and re-implementations of Kafka in other languages, plus a few SaaS offerings. Finally, there’s also a newcomer: Redis Streams.

### Apache Kafka vs. Redis Streams

First of all, note that what Redis calls a “stream,” Kafka calls a “topic partition,” and in Kafka, streams are a completely different concept that revolves around processing the contents of a Kafka topic.

That said, in terms of expressiveness, both systems are equivalent: you can implement the same application on either without any substantial change in how you model your data. The differences start once you dive into the practical details, and they are many and substantial.

Kafka has been around for a long time and people have successfully built reliable streaming architectures where it is the single source of truth. However, if you’re open to trying new technology, value simplicity in both development and operations, and need sub-millisecond latency, then Redis Streams can fill a very similar spot in your architecture.

When I say simplicity, I mean it. If you never tried Redis Streams, even if you plan to go with Kafka in production, I suggest you try prototyping your application with Redis Streams, as it literally takes a couple of minutes to get up and running on your laptop.

### Use cases for each pattern

Let’s consider a few examples to see which problems are best solved by each pattern.

### Brokerless synchronous communication

If you’re trying to make a couple of client devices (e.g., phone, Arduino) talk in a LAN to each other or to a program that’s running on a computer, the shortest path to a working solution is probably a “TCP connection on steroids.”

### Brokered synchronous communication

An IRC-style chat application (i.e., without history), or a plug-and-play real-time processing pipeline for volatile logs/events works well with a brokered approach. [Benjamin Sergeant talked about this last use case at RedisConf19 in San Francisco](https://www.youtube.com/watch?v=o8CC8qYfRQE) ([slides](https://bsergean.github.io/)).

### Queue-based asynchronous communication

Web crawlers very often rely on this pattern, as well as many web services with operations that can’t be completed immediately in response to a request. Think, for example, about video encoding in YouTube.

### Stream-based asynchronous communication

This technique works best for log processing, Internet of Things (IoT) devices and microservices, in addition to Slack-style chat applications (i.e., with history).

## Redis vs. the world

I want to leave you with one last consideration before concluding. The real super-power of Redis is that it’s not **just** a Pub/Sub messaging system, queue, nor stream service. It’s also not just a general-purpose database. Actually, with enough perseverance, you could implement every single pattern described above on top of a relational DBMS, but there are practical reasons why that would be a bad idea.

Redis offers a **real** Pub/Sub fire-and-forget system, as well as a **real** Stream data type. Furthermore, with Redis modules, Redis also supports real implementations of many different data types. Let me map this assertion back to our persisted and non-persisted chat application use cases.

### IRC-style chat app

Above, I concluded that Pub/Sub would have been the right choice since this type of chat application only needs to send messages to connected clients. However, to implement even a simple version of this application, you still have to think about a global channel list and a user presence list for each channel. Where do you store that state? How do you keep it up to date, especially when a service instance dies unexpectedly? In Redis, the answer is easy: sorted sets, expiring keys and atomic operations. If you were using RabbitMQ, you would need a DBMS.

### Slack-style chat app

Conversations can be very naturally expressed as a stream of messages. We don’t even have to bring event sourcing into the mix here, as it is already the native structure of this data type. So why Redis over Kafka for this example? Just as before, your chat system is not going to be only a stream of messages. There’s channels and other state that is best represented in different ways. There’s also the “User X is typing…” feature: that information is volatile, you want to send it to all participants, but only when they’re connected. If you were using Kafka, you would need to spin up a Pub/Sub system regardless.

### The take-away

**In distributed systems, when you need coordination, you often need shared state, and vice versa.** Ignoring this fact can quite often lead to over-complicated solutions. Redis understands this very well and it’s one of the reasons behind its unique design. If you embrace this principle, you will find that hard problems can occasionally be solved in few commands, given the right primitives, and that’s exactly what Redis gives you. For example, this is how you can transactionally append an entry to a stream, push a task to (the beginning of) a queue, and publish to Pub/Sub:

MULTI

XADD logs:service1 * level error req-id 42 stack-trace "..."

LPUSH actions-queue "RESTART=service1"

PUBLISH live-notifs "New error event in service1!"

EXEC

![](/images/blog/015fb5174f0fb5ab73f02c857b226bbceda3d312-1024x547.webp)

*To get to a working solution, you’ll need to defeat seven evil concurrency problems.*
*Plot of *[*Redis Pilgrim vs. The World*](https://www.imdb.com/title/tt0446029/)

I hope this gives you an understanding of the main patterns for communication that are commonly employed by distributed systems. Next time you need to connect two services together, this should help you navigate your options. If you enjoy talking about TCP connections on steroids and streaming architectures, feel free to reach me on Twitter [@croloris](https://twitter.com/croloris).

The Redis Streams data type is a great feature of Redis and will become a building block of many applications, especially now that Redis has a pool of modules that add new full-fledged capabilities for [time-series](http://redistimeseries.io/), [graph](http://redisgraph.io/) and [search](https://oss.redis.com/redisearch/index.html). To learn more about Redis Streams, check out this [introductory blog post by Antirez](http://antirez.com/news/114), as well as the [official documentation](https://redis.io/docs/latest/develop/). But don’t forget that streams are not the right tool for *every* job: sometimes you need Pub/Sub, or simply humble blocking operations on Redis Lists (or Sorted Sets, [Redis has that too](https://redis.io/commands/bzpopmax)).
