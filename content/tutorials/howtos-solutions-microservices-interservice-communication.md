---
title: "Microservices Communication with Redis Streams"
linkTitle: "Microservices Communication with Redis Streams"
url: "/tutorials/howtos/solutions/microservices/interservice-communication/"
description: "When building a microservices application, people use a variety of options for communication between services. Among them:"
group: "For developers"
aliases:
- "/tutorials/howtos-solutions-microservices-interservice-communication/"
date: 2026-02-25
lastmod: 2026-03-20
hidden: true
---

*Published 25 February 2026 · updated 20 March 2026*

> **TL;DR:**
>
> Use Redis Streams as a lightweight message broker for interservice communication in microservices. Each service produces events to a named stream using `XADD`, and downstream services consume them via consumer groups with `XREADGROUP`. Redis Streams gives you message persistence, consumer groups for load balancing, and message acknowledgment—making it a simpler alternative to Kafka for event-driven architectures.

> **GITHUB CODE**
>
> Below is a command to the clone the source code for the application used in this tutorial
>
> git clone --branch v1.0.0 [https://github.com/redis-developer/redis-microservices-ecommerce-solutions](https://github.com/redis-developer/redis-microservices-ecommerce-solutions)

## What you'll learn

- What interservice communication is and why streaming beats pub/sub for microservices
- How Redis Streams compares to Kafka and Redis Pub/Sub for message brokering
- How to produce events to a Redis Stream with `XADD`
- How to consume events using consumer groups with `XREADGROUP` and `XACK`
- How to build a complete order-to-payment event flow between two microservices

## What is interservice communication?

When building a microservices application, people use a variety of options for communication between services. Among them:

1.  **Publish/Subscribe** model: In the pub/sub model (fire and forget), a publisher produces messages, and subscribers that are active at the time consume those messages. Inactive subscribers cannot receive the messages at a later point in time.
2.  **Streaming**: Most microservices apps use an event-streaming solution because of:
3.  **Message persistence**: Unlike the pub/sub model, messages stored in streams can be read by multiple consumers at any time; they fan out. So consumers can read messages at a later point in time, even if they were not active when the message was originally appended to the stream.
4.  **Inherent replayability**: Even if a subscriber crashes during the message processing, it can re-read the exact same unacknowledged message from the stream. For example, say the crashed subscriber never comes back online; the consumer group feature allows consumers to process unacknowledged messages of other consumers after a specified time.
5.  **Separation of concerns**: Producers can produce messages to stream at **high speed** separately and consumers can process messages at their own speed separately. This separation of concerns solves both the "fast producer -> slow consumer" and "slow producer -> fast consumer" problem, allowing for the scaling of those services independently.

In an event-driven microservices architecture, you might have some services that publish an API, and other services that are simply producers and consumers of events with no external API.

## Why should you use Redis for interservice communication?

Consider the following scenario: You have an e-commerce application with an architecture that is broken down into different microservices including as `create an order`, `create an invoice`, `process a payment`, `fulfill and order`, and so on. Microservices allow you to separate these commands into different services to scale independently, enabling more customers to get their orders processed quickly and simultaneously, which results in a better user experience, higher sales volume, and less-cranky customer service staff.

When you use microservices, you need a tool for interservice communication. Initially, you might consider using a product like **Kafka** for streaming, but setting it up is rather complicated. What many people don't know about Redis is that it supports streams in the same way Kafka does. Given that you are likely already using Redis for caching, it makes sense to also use it for stream processing. To reduce the complexity of application architecture and maintenance, **Redis** is a great option for interservice communication. Here we break down the process of using Redis with streams for interservice communication.

## How do Redis Streams, Pub/Sub, and Kafka compare?

When choosing a messaging layer for microservices, it helps to understand the trade-offs between Redis Streams, Redis Pub/Sub, and Apache Kafka:

| Feature                    | Redis Pub/Sub                     | Redis Streams                              | Apache Kafka                                                          |
| -------------------------- | --------------------------------- | ------------------------------------------ | --------------------------------------------------------------------- |
| **Message persistence**    | No — messages are fire-and-forget | Yes — messages are stored in a log         | Yes — messages are stored in partitions                               |
| **Consumer groups**        | No                                | Yes — built-in consumer group support      | Yes — partition-based consumer groups                                 |
| **Message replay**         | No — missed messages are lost     | Yes — consumers can re-read from any point | Yes — offset-based replay                                             |
| **Delivery guarantees**    | At-most-once                      | At-least-once (with `XACK`)                | At-least-once or exactly-once                                         |
| **Operational complexity** | Low — built into Redis            | Low — built into Redis                     | High — requires ZooKeeper/KRaft, brokers, and separate infrastructure |
| **Latency**                | Sub-millisecond                   | Sub-millisecond                            | Low milliseconds                                                      |
| **Best suited for**        | Real-time notifications, chat     | Event-driven microservices, task queues    | High-throughput log processing, large-scale event streaming           |

**Redis Streams** sits in a sweet spot for many microservices architectures: it provides message persistence, consumer groups, and replay capability with the operational simplicity of Redis. If you're already running Redis for caching, adding Streams requires no additional infrastructure. Kafka remains the better choice for extremely high-throughput scenarios (millions of events per second) or when you need exactly-once semantics, but for most microservices communication patterns, Redis Streams delivers comparable functionality with significantly less complexity.

## What does a microservices architecture look like for an e-commerce application?

The e-commerce microservices application discussed in the rest of this tutorial uses the following architecture:

1.  `products service`: handles querying products from the database and returning them to the frontend
2.  `orders service`: handles validating and creating orders
3.  `order history service`: handles querying a customer's order history
4.  `payments service`: handles processing orders for payment
5.  `digital identity service`: handles storing digital identity and calculating identity score
6.  `api gateway`: unifies services under a single endpoint
7.  `mongodb`: serves as the primary database, storing orders, order history, products, etc.
8.  `redis`: serves as the **stream processor** and caching database

This diagram illustrates how Redis Streams is used as the message broker between the `orders service` and the `payments service`:

![Architecture diagram showing Redis Streams as a message broker for interservice communication between the orders service and payments service in a microservices e-commerce application](/images/site-mirror/28f327ec2a91c1f12dab156323f43ded6b1094d7-1757x777.webp)

> **TIP**
>
> Redis Streams is more cost-effective than using Kafka or other similar technologies. With sub-millisecond latency and a lightweight Streams log data structure, Redis is easier to deploy, develop, and operate.

## How does Redis enable interservice communication in an event-driven architecture?

The following event flow diagram illustrates how the orders service and payments service communicate through Redis with streams:

![Event flow diagram showing how the orders service produces events to ORDERS_STREAM and the payments service consumes them using Redis Streams consumer groups](/images/site-mirror/1821c57265cdc4b4df928de82d0659fa65d6e755-1161x1235.webp)

Let's outline the streams and events used below:

1.  The `orders service` inserts order data into the database.

```json
//sample order data
{
    "orderId": "01GTP3K2TZQQCQ0T2G43DSSMTD",
    "products": [
        {
            "productId": 11000,
            "qty": 3,
            "productPrice": 3995,
            "productData": {
                "productDisplayName": "Puma Men Slick 3HD Yellow Black Watches",
                "variantName": "Slick 3HD Yellow",
                "brandName": "Puma",
                "ageGroup": "Adults-Men",
                "gender": "Men"
                //...
            }
        },
        {
            "productId": 11001,
            "qty": 2,
            "productPrice": 5450,
            "productData": {
                "productDisplayName": "Puma Men Top Fluctuation Red Black Watches",
                "variantName": "Top Fluctuation Red",
                "brandName": "Puma",
                "ageGroup": "Adults-Men",
                "gender": "Men"
                //...
            }
        }
    ],
    "userId": "USR_4e7acc44-e91e-4c5c-9112-bdd99d799dd3",
    "orderStatusCode": 1, //order created
    "createdBy": "USR_4e7acc44-e91e-4c5c-9112-bdd99d799dd3",
    "statusCode": 1
}
```

2\. The `orders service` also appends minimal data (orderId, orderAmount, and userId) to the `ORDERS_STREAM` to signal new order creation (i.e., it acts as `PRODUCER` of the `ORDERS_STREAM`).

![Redis Insight screenshot displaying ORDERS_STREAM entries with orderId, orderAmount, and userId fields produced by the orders service](/images/site-mirror/68742bd821e5ba098df10a41132078bcf331e22c-2000x668.webp)

3\. The `payments service` listens to the `ORDERS_STREAM` and processes payments for new orders, then inserts payment data into the database (i.e, it acts as the `CONSUMER` of the `ORDERS_STREAM`).

```json
//sample payment data
{
    "paymentId": "6403212956a976300afbaac1",
    "orderId": "01GTP3K2TZQQCQ0T2G43DSSMTD",
    "orderAmount": 22885,
    "paidAmount": 22885,
    "orderStatusCode": 3, //payment successful
    "userId": "USR_4e7acc44-e91e-4c5c-9112-bdd99d799dd3",
    "createdOn": {
        "$date": {
            "$numberLong": "1677926697841"
        }
    },
    "createdBy": "USR_4e7acc44-e91e-4c5c-9112-bdd99d799dd3",
    "statusCode": 1
}
```

4\. The `payments service` appends minimal data (orderId, paymentId, orderStatusCode, and userId) to the `PAYMENTS_STREAM` to signal a new payment (i.e., it acts as the `PRODUCER` of the `PAYMENTS_STREAM`).

![Redis Insight screenshot displaying PAYMENTS_STREAM entries with orderId, paymentId, and orderStatusCode fields produced by the payments service](/images/site-mirror/7f79b074b581896971500faf102c8fdc5bf9a8e4-2000x572.webp)

5\. The `orders service` listens to the `PAYMENTS_STREAM` and updates the orderStatus and paymentId for orders in the database accordingly as the order payment is fulfilled (i.e., it acts as the `CONSUMER` of the `PAYMENTS_STREAM`).

```json
{
    //order collection update
    "orderId": "01GTP3K2TZQQCQ0T2G43DSSMTD",
    "paymentId": "6403212956a976300afbaac1",
    "orderStatusCode": 3 //payment success
    //...
}
```

## What does the e-commerce application frontend look like?

The e-commerce microservices application consists of a frontend, built using [Next.js](https://nextjs.org/) with [TailwindCSS](https://tailwindcss.com/). The application backend uses [Node.js](https://nodejs.org/). The data is stored in [Redis](https://redis.io/try-free/) and MongoDB. Below you will find screenshots of the frontend of the e-commerce app:

- `Dashboard`: Shows the list of products with search functionality

![E-commerce microservices application dashboard showing a product catalog with search functionality built with Next.js and TailwindCSS](/images/site-mirror/4f6a862752feff8ae6a946d92e5895906af325f3-1982x1500.webp)

`Shopping Cart`: Add products to the cart, then check out using the "Buy Now" button

![Shopping cart interface in the e-commerce microservices app showing selected products and a Buy Now checkout button](/images/site-mirror/9f9deeb554a22a16af87671c88606ac922b8e2e7-2000x1401.webp)

`Order history`: Once an order is placed, the Orders link in the top navigation bar shows the order status and history

![Order history view displaying order status and payment processing results driven by Redis Streams interservice communication](/images/site-mirror/776a16cd58782fb2ff513b9271b2b00b6a5d2d60-2000x1076.webp)

> **GITHUB CODE**
>
> Below is a command to the clone the source code for the application used in this tutorial
>
> git clone --branch v1.0.0 [https://github.com/redis-developer/redis-microservices-ecommerce-solutions](https://github.com/redis-developer/redis-microservices-ecommerce-solutions)

## How do you build an interservice communication application with Redis?

We use Redis to broker the events sent between the orders service and the payments service.

### Producer 1 (orders service)

Let's look at some of the code in the orders service to understand how it works:

1.  Orders are created.
2.  After order creation, the `orders service` appends minimal data to the `ORDERS_STREAM` to signal new order creation.

```js
// File: server/src/services/orders/src/service-impl.ts

const addOrderIdToStream = async (
  orderId: string,
  orderAmount: number,
  userId: string
) => {
  const nodeRedisClient = getNodeRedisClient();
  if (orderId && nodeRedisClient) {
    const streamKeyName = "ORDERS_STREAM";
    const entry = {
      orderId: orderId,
      orderAmount: orderAmount.toFixed(2),
      userId: userId,
    };
    const id = "*"; //* = auto generate
    //xAdd adds entry to specified stream
    await nodeRedisClient.xAdd(streamKeyName, id, entry);
  }
};
```

### Consumer 1 (payments service)

3\. The `payments service` listens to the `ORDERS_STREAM`

```js
// File: server/src/services/payments/src/service-impl.ts
// Below is some code for how you would use Redis to listen for the stream events:

async function listenToStream(
  onMessage: (message: any, messageId: string) => Promise<void>
) {
  // using node-redis
  const redis = getNodeRedisClient();
  const streamKeyName = "ORDERS_STREAM"; //stream name
  const groupName = "ORDERS_CON_GROUP"; // listening consumer group name (custom)
  const consumerName = "PAYMENTS_CON"; // listening consumer name (custom)
  const readMaxCount = 100;

  // Check if the stream group already exists
  if (!(await redis.exists(streamKeyName))) {
    const idPosition = "0"; //0 = start, $ = end or any specific id
    await nodeRedisClient.xGroupCreate(streamKeyName, groupName, idPosition, {
      MKSTREAM: true,
    });
  }

  // setup a loop to listen for stream events
  while (true) {
    // read set of messages from different streams
    const dataArr = await nodeRedisClient.xReadGroup(
      commandOptions({
        isolated: true,
      }),
      groupName,
      consumerName,
      [
        {
          // you can specify multiple streams in array
          key: streamKeyName,
          id: ">", // Next entry ID that no consumer in this group has read
        },
      ],
      {
        COUNT: readMaxCount, // Read n entries at a time
        BLOCK: 0, // block for 0 (infinite) seconds if there are none.
      }
    );

    for (let data of dataArr) {
      for (let messageItem of data.messages) {
        // process the message received (in our case, perform payment)
        await onMessage(messageItem.message, messageItem.id);

        // acknowledge individual messages after processing
        nodeRedisClient.xAck(streamKeyName, groupName, messageItem.id);
      }
    }
  }
}

// `listenToStream` listens for events and calls the `onMessage` callback to further handle the events.
listenToStream({
  onMessage: processPaymentForNewOrders,
});

const processPaymentForNewOrders: IMessageHandler = async (
  message,
  messageId
) => {
  /*
   message = {
      orderId: "",
      orderAmount: "",
      userId: "",
    }
    */
  // process payment for new orderId and insert "payments" data to database
};
```

> **TIP**
>
> There are a few important things to note here:
>
> - Make sure the stream group doesn't exist prior to creating it.
> - Use `isolated: true`, in order to use the blocking version of `XREADGROUP` in [isolated execution](https://github.com/redis/node-redis/blob/master/docs/isolated-execution.md) mode.
> - Acknowledge individual messages after you process them to remove the messages from the pending orders queue and to avoid processing them more than once.

### Producer 2 (payments service)

4\. The payments service appends minimal data to PAYMENTS_STREAM to signal that a payment has been fulfilled.

```js
// File: server/src/services/payments/src/service-impl.ts

const addPaymentIdToStream = async (
  orderId: string,
  paymentId: string,
  orderStatus: number,
  userId: string
) => {
  const nodeRedisClient = getNodeRedisClient();
  if (orderId && nodeRedisClient) {
    const streamKeyName = "PAYMENTS_STREAM";
    const entry = {
      orderId: orderId,
      paymentId: paymentId,
      orderStatusCode: orderStatus.toString(),
      userId: userId,
    };
    const id = "*"; //* = auto generate
    //xAdd adds entry to specified stream
    await nodeRedisClient.xAdd(streamKeyName, id, entry);
  }
};
```

### Consumer 2 (orders service)

5\. The orders service listens to the PAYMENTS_STREAM and updates the order when payments are fulfilled.

```js
// File: server/src/services/orders/src/service-impl.ts
//Below is some code for how you would use Redis to listen for the stream events:

async function listenToStream(
  onMessage: (message: any, messageId: string) => Promise<void>
) {
  // using node-redis
  const redis = getNodeRedisClient();
  const streamKeyName = "PAYMENTS_STREAM"; //stream name
  const groupName = "PAYMENTS_CON_GROUP"; //listening consumer group name (custom)
  const consumerName = "ORDERS_CON"; //listening consumer name (custom)
  const readMaxCount = 100;

  // Check if the stream group already exists
  if (!(await redis.exists(streamKeyName))) {
    const idPosition = "0"; //0 = start, $ = end or any specific id
    await nodeRedisClient.xGroupCreate(streamKeyName, groupName, idPosition, {
      MKSTREAM: true,
    });
  }

  // setup a loop to listen for stream events
  while (true) {
    // read set of messages from different streams
    const dataArr = await nodeRedisClient.xReadGroup(
      commandOptions({
        isolated: true,
      }),
      groupName,
      consumerName,
      [
        {
          // you can specify multiple streams in array
          key: streamKeyName,
          id: ">", // Next entry ID that no consumer in this group has read
        },
      ],
      {
        COUNT: readMaxCount, // Read n entries at a time
        BLOCK: 0, // block for 0 (infinite) seconds if there are none.
      }
    );

    for (let data of dataArr) {
      for (let messageItem of data.messages) {
        //process the message received (in our case, updateOrderStatus)
        await onMessage(messageItem.message, messageItem.id);

        // acknowledge individual messages after processing
        nodeRedisClient.xAck(streamKeyName, groupName, messageItem.id);
      }
    }
  }
}

// `listenToStream` listens for events and calls the `onMessage` callback to further handle the events.
listenToStream({
  onMessage: updateOrderStatus,
});

const updateOrderStatus: IMessageHandler = async (message, messageId) => {
  /*
   message = {
      orderId: "",
      paymentId: "",
      orderStatusCode:"",
      userId: "",
    }
    */
  // updates orderStatus and paymentId in database accordingly for the order which has fulfilled payment
  // updateOrderStatusInRedis(orderId,paymentId,orderStatusCode,userId)
  // updateOrderStatusInMongoDB(orderId,paymentId,orderStatusCode,userId)
};
```

> **TIP**
>
> It's a best practice to validate all incoming messages to make sure you can work with them.

For the purposes of our application, we make a call to update the order status in both Redis and primary database in the same service (For simplicity, we are not using any synchronization technique between databases rather focusing on how the data is stored and accessed in Redis). Another common pattern is to have your services write to one database, and then separately use a CDC mechanism to update the other database. For example, you could write directly to Redis, then use **Triggers and Functions** to handle synchronizing Redis and primary database in the background.

> **TIP**
>
> If you use **Redis Cloud**, you will find that Redis Streams is available on the same multi-tenant data platform you already use for caching. Redis Cloud also has high availability, message persistence, support for multiple clients, and resiliency with primary/secondary data replication… all built in.

## What are the next steps for using Redis Streams in microservices?

You now know how to use Redis Streams for interservice communication as both a producer and a consumer. Here are some ways to continue building on what you've learned:

### Next steps

- **Try the CQRS pattern with Redis**: Learn how to separate read and write models in your microservices using Redis in the [CQRS tutorial](/tutorials/howtos/solutions/microservices/cqrs).
- **Explore Redis Streams in .NET**: If you work with .NET, see [How to use Redis Streams with .NET](/tutorials/develop/dotnet/streams/stream-basics/) for a hands-on guide to stream basics with C#.
- **Add caching to your microservices**: Improve performance with [query caching](/tutorials/howtos/solutions/microservices/caching) or [API gateway caching](/tutorials/howtos/solutions/microservices/api-gateway-caching).
- **Get started with Redis Cloud**: [Try Redis Cloud for free](https://redis.io/try-free/) to get managed Redis Streams with built-in high availability and data replication.

### Additional resources

Redis Streams

- Explore streams in detail in the [Redis University course on Redis Streams](https://university.redis.io/learningpath/grnomm8jaglgcu?tab=details)
- Check out our e-book on [Understanding Streams in Redis and Kafka: A Visual Guide](https://redis.io/resources/understanding-streams-in-redis-and-kafka-a-visual-guide/)

General

- [Redis YouTube channel](https://www.youtube.com/c/Redisinc)
- Clients like [Node Redis](https://github.com/redis/node-redis) and [Redis om Node](https://github.com/redis/redis-om-node) help you to use Redis in Node.js apps.
- [Redis Insight](https://redis.io/insight/) : To view your Redis data or to play with raw Redis commands in the workbench
