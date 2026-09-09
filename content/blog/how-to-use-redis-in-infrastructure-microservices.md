---
title: "How to Use Redis in Infrastructure Microservices"
linkTitle: "How to Use Redis in Infrastructure Microservices"
url: "/blog/how-to-use-redis-in-infrastructure-microservices/"
description: "Back in 2019, I wrote about how to create an event store in Redis. I explained that Redis Streams are a good fit for an event store, because they let you store events in an immutable append-only..."
date: 2020-11-24
blogCategories:
- "Tech"
authors:
- "Martin Forstner"
lastmod: 2026-09-01
hidden: true
---

*By Martin Forstner, Solution Architect · Published 24 November 2020 · updated 1 September 2026*

![Blog tile image](/images/site-mirror/05ab753c22c0e8a39798f318e8ea5d39427d1f04-1440x738.webp)

Back in 2019, I wrote about how to [create an event store in Redis](/blog/use-redis-event-store-communication-microservices/). I explained that Redis Streams are a good fit for an event store, because they let you store events in an immutable append-only mechanism like a transaction log. Now, with an update of the sample OrderShop application introduced in that blog, I’m going to demonstrate how to [use Redis as a message queue](/solutions/messaging/), further demonstrating Redis Enterprise’s many use cases [beyond caching](/blog/goodbye-cache-redis-as-a-primary-database/).

## A quick look at microservices, infrastructure services, and distributed systems

Redis is a great solution for creating infrastructure services like message queues and event stores, but there are a few things you need to take into account when using a microservices architecture to create a distributed system. Relational databases were often good for monolithic applications, but only NoSQL databases like Redis can provide the scalability and availability requirements that are needed for a microservices architecture.

Distributed systems imply a distributed state. According to the [CAP theorem](https://en.wikipedia.org/wiki/CAP_theorem), a software implementation can deliver only two out of these three attributes: [consistency, ](https://en.wikipedia.org/wiki/Consistency_model)[availability](https://en.wikipedia.org/wiki/Availability), and [partition tolerance](https://en.wikipedia.org/wiki/Network_partition) (hence CAP). So, in order to make your implementation fault tolerant, you must choose between availability and consistency. If you choose availability, you’ll end up having eventual consistency, which means that the data will be consistent but only after a period of time has passed. Choosing consistency impacts performance because of the need to synchronize and isolate write operations throughout the distributed system.

[Even](https://microservices.io/patterns/data/event-sourcing.html)[t](https://microservices.io/patterns/data/event-sourcing.html)[ sourcing](https://microservices.io/patterns/data/event-sourcing.html), which persists the state of a business entity such as an order, or a customer, as a sequence of state-changing events, goes for availability instead of consistency. It allows write operations to be trivial, but read operations are more costly because, in case they span multiple services, they may require an additional mechanism such as a read model.

Communication in a distributed system can be brokered or brokerless. Brokerless styles are well known, with HTTP as its most famous instance. The brokered approach has, as the name implies, a broker between the sender and the receiver of a message. It decouples the sender and receiver, enabling synchronous and asynchronous communication. This results in more resilient behavior as the message consumer does not have to be available at the moment when the message is sent. Brokered communication also allows independent scaling of sender and receiver.

(For more information, see our post on [What to Choose for Your Synchronous and Asynchronous Communication Needs—Redis Streams, Redis Pub/Sub, Kafka, etc.](/blog/what-to-choose-for-your-synchronous-and-asynchronous-communication-needs-redis-streams-redis-pub-sub-kafka-etc-best-approaches-synchronous-asynchronous-communication))

## OrderShop: a sample e-commerce implementation

The “Hello World” of a microservice architecture is the [OrderShop](https://github.com/martinez099/ordershop), a simple implementation of an e-commerce system using an event-based approach. This sample application uses a simple [domain model](https://martinfowler.com/eaaCatalog/domainModel.html), but it fulfils the application’s purpose.

OrderShop is orchestrated using [Docker Compose](https://docs.docker.com/compose/). All network communication is done over [gRPC](https://grpc.io). The central components are the [event store](https://github.com/redislabs-training/demo-eventstore) and the [message queue](https://github.com/redislabs-training/demo-redismq): each and every service is connected to and only to them over gRPC. OrderShop is a sample implementation in Python. You can see the [OrderShop source code on GitHub](https://github.com/redislabs-demos/ordershop-v2).

**(Note: **This code is *not* production-ready and is for demo purposes only!)

## Run and fun

- Clone the GitHub repository: [https://github.com/redislabs-demos/ordershop-v2](https://github.com/redislabs-demos/ordershop-v2)
- Run OrderShop v2 in a simple five-step process:
1. Start the application with **docker-compose up**
1. Open your browser and go to [http://localhost:5000/](http://localhost:5000/)
  1. Watch events and browse state
1. Run the client with **python -m unittest tests/unit.py**
1. Open another tab in your browser to [http://localhost:8001/](http://localhost:8001)
  1. Use **redis:6379** to connect to the test database
1. Stop the application with **docker-compose down**

## OrderShop v2 architecture

In this case, the server architecture consists of multiple services. The state is distributed over several domain services but stored in a single event store. The **Read model** component concentrates the logic for reading and caching the state, as shown here:

[Watch the video](/wp-content/uploads/2020/11/ordershop-1.png)

Commands and queries are communicated via the **Message queue** component, whereas events are communicated via the **Event store** component, which also acts as an event bus.

## Infrastructure services

In OrderShop v2, all unicast communication happens over the **Message queue** component. For this, I’ll be using [Redis Lists](https://redis.io/commands#list), and in particular, two lists combined into a so-called “[rel](https://redis.io/commands/rpoplpush#pattern-reliable-queue)[i](http://redis.io/commands/rpoplpush#pattern-reliable-queue)[able queue](https://redis.io/commands/rpoplpush#pattern-reliable-queue)”. It processes simple commands (e.g. single entity operations) synchronously, but long-running ones (e.g. batches, mails) asynchronously and supports responses to synchronous messages out of the box.

The [Event store](https://github.com/redislabs-demos/eventstore) is based on [Redis Streams](https://redis.io/docs/latest/develop/). Domain services (which are just dummies to demonstrate OrderShop’s functionality) are subscribed to event streams named after the event topic (i.e the entity name) and publish events onto these streams. Each event is a stream-entry with the event timestamp acting as the ID. The sum of the published events in the streams results in the state of the overall system.

## Application services

The **Read model** caches deduced entities from the **Event store** in Redis using the domain model. Disregarding the cache, it’s stateless.

The **API gateway** is stateless as well, and serves the REST-API on port 5000. It terminates HTTP connections and routes them either to the read model for reading state (queries) or to dedicated domain service for writing state (commands). This conceptual separation between read and write operations is a pattern called Command Query Responsibility Segregation ([CQRS](/solutions/microservices/cqrs/)).

## Domain services

The domain services receive write operations over the **Message queue** from the **API gateway**. After successful execution, they publish an event for each of them to the **Event store**. In contrast, all read operations are handled by the **Read model** which gets its state from the **Event store**.

The **CRM service** (Customer Relation Management service) is stateless—it’s subscribed to domain events from the event store and sends emails to customers using the **Mail service**.

The central domain entity is the order. It has a field called ‘status’ which transitions are performed using a state machine, as shown in the diagram below.

[Watch the video](/wp-content/uploads/2020/11/ordershop-2.png)

These transitions are done in several event handlers, which are subscribed to domain events ([SAGA](https://microservices.io/patterns/data/saga.html) pattern), for example:

```python
def order_created(self, _item):
        if _item.event_action != 'entity_created':
            return

        order = json.loads(_item.event_data)
        rsp = send_message('read-model', 'get_entity', {'name': 'cart', 'id': order['cart_id']})
        cart = rsp['result']
        result = self._decr_from_cart(cart)
        order['status'] = 'IN_STOCK' if result else 'OUT_OF_STOCK'
        self.event_store.publish('order', create_event('entity_updated', order))

```

```python
def billing_created(self, _item):
        if _item.event_action != 'entity_created':
            return

        billing = json.loads(_item.event_data)
        rsp = send_message('read-model', 'get_entity', {'name': 'order', 'id': billing['order_id']})
        order = rsp['result']
        if order['status'] != 'IN_STOCK':
            return

        order['status'] = 'CLEARED'
        self.event_store.publish('order', create_event('entity_updated', order))

```

## Clients

Clients are simulated using the [Unit testing framework](https://docs.python.org/3/library/unittest.html) from Python. There are currently 10 unit tests implemented. Take a look at tests/unit.py for further details.

A simple UI is served on port 5000 to watch events and browse state (using [WebSockets](https://en.wikipedia.org/wiki/WebSocket)).

A [RedisInsight](/redis-enterprise/redis-insight) container is also available to inspect the Redis instance. Open the web browser to [http://localhost:8001/](http://localhost:8001/) and use redis:6379 to connect to the test database.

[Watch the video](/wp-content/uploads/2020/11/ordershop-3.gif)

## Conclusion

Redis is not only a powerful tool in the domain layer (e.g. a catalog search) and application layer (e.g. a HTTP session store) but also in the infrastructure layer (e.g. an event store or message queue). Using Redis throughout these layers reduces operational overhead and lets developers reuse technologies they already know.

Take a peek at the code and try your hand at implementing it. I hope this helps demonstrate Redis’ versatility and flexibility in domain and infrastructure services and proves how it can be used beyond caching.

Let me know how it goes on Twitter: [@m](https://twitter.com/martinez099)[a](https://twitter.com/martinez099)[rtinez099](https://twitter.com/martinez099).
