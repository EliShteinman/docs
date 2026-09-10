---
title: "How to use Redis for Transaction risk scoring (in Fraud Detection)"
linkTitle: "How to use Redis for Transaction risk scoring (in Fraud Detection)"
url: "/tutorials/howtos/solutions/fraud-detection/transaction-risk-scoring/"
description: "\"Transaction risk scoring\" is a method of leveraging data science, machine learning, and statistical analysis to continuously monitor transactions and assess the relative risk associated with each..."
group: "For developers"
aliases:
- "/tutorials/howtos-solutions-fraud-detection-transaction-risk-scoring/"
date: 2026-02-25
lastmod: 2026-02-26
hidden: true
---

*Published 25 February 2026 · updated 26 February 2026*

> **TL;DR:**
>
> Build a real-time transaction risk scoring system with Redis by using Redis Streams for event-driven microservice orchestration, Bloom filters for behavioral profiling, and an in-memory feature store for low-latency ML model serving. This tutorial walks through a complete e-commerce checkout pipeline that calculates identity and profile scores to flag potential fraud before processing payment.

> **GITHUB CODE**
>
> Below is a command to the clone the source code for the application used in this tutorial
>
> git clone --branch v3.0.0 [https://github.com/redis-developer/redis-microservices-ecommerce-solutions](https://github.com/redis-developer/redis-microservices-ecommerce-solutions)

## What you'll learn

- What transaction risk scoring is and why it matters for fraud detection
- How to use Redis Streams to orchestrate a multi-service transaction pipeline
- How to use Redis Bloom filters as lightweight behavioral transaction filters
- How to leverage Redis Cloud as an in-memory feature store for real-time risk scoring
- How to assess and finalize orders based on combined identity and profile risk scores

## What is transaction risk scoring?

"Transaction risk scoring" is a method of leveraging data science, machine learning, and statistical analysis to continuously monitor transactions and assess the relative risk associated with each transaction. By comparing transactional data to models of known fraud, the risk score can be calculated, and the closer a transaction matches fraudulent behaviour, the higher the risk score.

The score is typically based on a statistical analysis of historical transaction data to identify patterns and trends associated with fraudulent activity. The score can then be used to trigger alerts or to automatically decline transactions that exceed a certain risk threshold. It can also be used to trigger additional authentication steps for high-risk transactions. Additional steps might include a one-time password (OTP) sent via text, email, or biometric scan.

> **TIP**
>
> Transaction risk scoring is often combined in a single system with other fraud detection methods, such as [**digital identity validation**](/tutorials/howtos/solutions/fraud-detection/digital-identity-validation). For a broader overview, see the [fraud detection system tutorial](/tutorials/howtos/frauddetection/).

## Why should you use Redis for transaction risk scoring?

A risk-based approach must be designed to create a frictionless flow and **avoid slowing down** the transaction experience for legitimate customers while simultaneously preventing fraud. If your risk-based approach is too strict, it will **block legitimate transactions** and frustrate customers. If it is too lenient, it will **allow fraudulent transactions** to go through.

### How do you avoid false positives with rules engines?

Rules-based automated fraud detection systems operate on simple "yes or no" logic to determine whether a given transaction is likely to be fraudulent. An example of a rule would be "block all transactions over $500 from a risky region". With a simple binary decision like this, the system is likely to block a lot of genuine customers. Sophisticated fraudsters easily fool such systems, and the complex nature of fraud means that simple "yes or no" rules may not be enough to assess the risk of each transaction accurately.

More accurate risk scoring with **AI/ML** addresses these issues. Modern fraud detection systems use machine learning models trained on large volumes of different data sets known as "features"(user profiles, transaction patterns, behavioural attributes and more) to accurately identify fraudulent transactions. These models have been designed to be flexible, so they can adapt to new types of fraud. For example, a neural network can examine suspicious activities like how many pages a customer browses before making an order, whether they are copying and pasting information or typing it in manually and flag the customer for further review.

The models use historical as well as most recent data to create a risk profile for each customer. By analyzing past behaviour it is possible to create a profile of what is normal for each customer. Any transactions that deviate from this profile can be flagged as suspicious, reducing the likelihood of false positives. The models are very fast to adapt to changes in normal behaviour too, and can quickly identify patterns of fraud transactions.

This is exactly where **Redis Cloud** excels in transaction risk scoring.

### How does Redis Cloud enable real-time transaction risk scoring?

People use Redis Cloud as the **in-memory** online feature store for online and **fast access** to feature data as part of a transaction risk scoring system. By serving online features with low latency, Redis Cloud enables the risk-scoring models to return results fast, thereby allowing the whole system to achieve high accuracy and **instant response** on approving legitimate online transactions.

Another very common use for Redis Cloud in transaction risk scoring is for **transaction filters**. A transaction filter can be implemented as a **Bloom** filter that stores information about user behaviours. It can answer questions like "Have we seen this user purchase at this merchant before?" Or, "Have we seen this user purchase at this merchant in the X to Y price range before?" Being a probabilistic data structure, Redis Bloom filters do, indeed, sacrifice some accuracy, but in return, they get a very low memory footprint and response time.

> **TIP**
>
> You might ask why not use a Redis Set to answer some of the questions above. Redis Sets are used to store unordered collections of unique strings (members). They are very efficient, with most operations taking O(1) time complexity. However, the `SMEMBERS` command is O(N), where N is the cardinality of the set, and can be very slow for large sets and it would also take a lot of memory. This presents a problem both in single instance storage as well as geo-replication, since more data will require more time to move. This is why Redis Bloom filters are a better choice for transaction filters. Apps undergo millions of transactions every day, and Bloom filters maintain a speedy response time at scale.

## How does transaction risk scoring work in a microservices architecture?

The e-commerce microservices app discussed in the rest of this tutorial uses the following architecture:

1.  `products service`: handles querying products from the database and returning them to the frontend
2.  `orders service`: handles validating and creating orders
3.  `order history service`: handles querying a customer's order history
4.  `payments service`: handles processing orders for payment
5.  `digital identity service`: handles storing digital identity and calculating identity score
6.  `api gateway`: unifies services under a single endpoint
7.  `mongodb/ postgresql`: serves as the primary database, storing orders, order history, products, etc.
8.  `redis`: serves as the **stream processor** and caching database

> **INFO**
>
> You don't need to use MongoDB/ Postgresql as your primary database in the demo application; you can use other [prisma supported databases](https://www.prisma.io/docs/reference/database-reference/supported-databases) as well. This is just an example.

## What happens during the transaction risk scoring checkout procedure?

When a user goes to checkout, the system needs to check the user's digital identity and profile to determine the risk of the transaction. The system can then decide whether to approve the transaction or to trigger additional authentication steps. The following diagram shows the flow of transaction risk scoring in the e-commerce app:

![Flow diagram showing how Redis Streams orchestrate transaction risk scoring during e-commerce checkout, including identity scoring, profile scoring, and risk assessment steps](/images/site-mirror/7f3525b217aaa9f33daf9005a7255bafcb285057-989x1500.webp)

The following steps are performed in the checkout procedure:

1.  The customer adds an item to the cart and proceeds to checkout.
2.  The `order service` receives the checkout request and creates an order in the database.
3.  The `order services` publishes a `CALCULATE_IDENTITY_SCORE` event to the `TRANSACTIONS` Redis stream.
4.  The `identity service` subscribes to the `TRANSACTIONS` Redis stream and receives the `CALCULATE_IDENTITY_SCORE` event.
5.  The `identity service` [calculates the identity score](/tutorials/howtos/solutions/fraud-detection/digital-identity-validation) for the user and publishes a `CALCULATE_PROFILE_SCORE` event to the `TRANSACTIONS` Redis stream.
6.  The `profile service` subscribes to the `TRANSACTIONS` Redis stream and receives the `CALCULATE_PROFILE_SCORE` event.
7.  The `profile service` calculates the profile score by checking the products in the shopping cart against a known profile for the customer.
8.  The `profile service` publishes a `ASSESS_RISK` event to the `TRANSACTIONS` Redis stream.
9.  The order service subscribes to the TRANSACTIONS Redis stream and receives the ASSESS_RISK event.
10. The `order service` determines if there is a likelihood of fraud based on the identity and profile scores. If there is a likelihood of fraud, the `order service` triggers additional authentication steps. If there is no likelihood of fraud, the `order service` approves the order and proceeds to process payments.

## What does the e-commerce app frontend look like?

The e-commerce microservices app consists of a frontend, built using [Next.js](https://nextjs.org/) with [TailwindCSS](https://tailwindcss.com/). The app backend uses [Node.js](https://nodejs.org/). The data is stored in [Redis](https://redis.io/try-free/) and MongoDB/ Postgressql using [Prisma](https://www.prisma.io/docs/reference/database-reference/supported-databases). Below you will find screenshots of the frontend of the e-commerce app:

- `Dashboard`: Shows the list of products with search functionality

![E-commerce app dashboard built with Next.js and Tailwind CSS showing a product grid with search functionality](/images/site-mirror/4f6a862752feff8ae6a946d92e5895906af325f3-1982x1500.webp)

`Shopping Cart`: Add products to the cart, then check out using the "Buy Now" button

![Shopping cart page showing added items with a Buy Now checkout button that triggers the transaction risk scoring pipeline](/images/site-mirror/e8c8b3e8e3266c53acb54c2c72675cf27f599bca-1038x727.webp)

`Order history`: Once an order is placed, the Orders link in the top navigation bar shows the order status and history

![Order history view showing transaction statuses and fraud detection results for recent orders](/images/site-mirror/776a16cd58782fb2ff513b9271b2b00b6a5d2d60-2000x1076.webp)

> **GITHUB CODE**
>
> Below is a command to the clone the source code for the application used in this tutorial
>
> git clone --branch v3.0.0 [https://github.com/redis-developer/redis-microservices-ecommerce-solutions](https://github.com/redis-developer/redis-microservices-ecommerce-solutions)

## How do you implement transaction risk scoring with Redis?

Now that you understand the steps involved in the checkout process for transaction risk scoring, let's look at the code for the `order service` and `profile service` to facilitate this process:

> **NOTE**
>
> To see the code for the `identity service` check out the [digital identity validation](/tutorials/howtos/solutions/fraud-detection/digital-identity-validation) solution.

### How does the order service initiate the checkout process?

When the `order service` receives a checkout request, it creates an order in the database and publishes a `CALCULATE_IDENTITY_SCORE` event to the `TRANSACTIONS` Redis stream. The event contains information about the order as well as the customer, such as the browser fingerprint, IP address, and persona (profile). This data will be used during the transaction by the `identity service` and `profile service` to calculate the identity and profile scores. The `order service` also specifies the transaction pipeline, meaning it determines the order of events called so that the `identity service` and `profile service` do not need to be aware of each other. The `order service` ultimately owns the transaction. The sample code below shows the `createOrder` function in the `order service`. The code example below is highly simplified. For more detail please see the source code linked above:

```js
// File: server/src/services/orders/src/service-impl.ts

const TransactionPipelines = {
  CHECKOUT: [
    TransactionStreamActions.CALCULATE_IDENTITY_SCORE,
    TransactionStreamActions.CALCULATE_PROFILE_SCORE,
    TransactionStreamActions.ASSESS_RISK,
    TransactionStreamActions.PROCESS_PAYMENT,
    TransactionStreamActions.PAYMENT_PROCESSED,
  ],
};

async function createOrder(
  order: IOrder,
  browserAgent: string,
  ipAddress: string,
  sessionId: string,
  sessionData: ISessionData
) {
  order = await validateOrder(order);

  const orderId = await addOrderToRedis(order);
  order.orderId = orderId;

  await addOrderToMongoDB(order);

  // Log order creation to the LOGS stream
  await streamLog({
    action: "CREATE_ORDER",
    message: `[${REDIS_STREAMS.CONSUMERS.ORDERS}] Order created with id ${orderId} for the user ${userId}`,
    metadata: {
      userId: userId,
      persona: sessionData.persona,
      sessionId: sessionId,
    },
  });

  let orderAmount = 0;
  order.products?.forEach((product) => {
    orderAmount += product.productPrice * product.qty;
  });

  const orderDetails: IOrderDetails = {
    orderId: orderId,
    orderAmount: orderAmount.toFixed(2),
    userId: userId,
    sessionId: sessionId,
    orderStatus: order.orderStatusCode,
    products: order.products,
  };

  // Initiate the transaction by adding the order details to the transaction stream and sending the first event
  await addMessageToTransactionStream({
    action: TransactionPipelines.CHECKOUT[0],
    logMessage: `[${REDIS_STREAMS.CONSUMERS.IDENTITY}] Digital identity to be validated/ scored for the user ${userId}`,
    userId: userId,
    persona: sessionData.persona,
    sessionId: sessionId,
    orderDetails: orderDetails ? JSON.stringify(orderDetails) : "",
    transactionPipeline: JSON.stringify(TransactionPipelines.CHECKOUT),

    identityBrowserAgent: browserAgent,
    identityIpAddress: ipAddress,
  });

  return orderId;
}
```

Let's look at the `addMessageToTransactionStream` function in more detail:

```js
// File: server/src/common/utils/redis/redis-streams.ts

async function addMessageToStream(message, streamKeyName) {
  try {
    const nodeRedisClient = getNodeRedisClient();
    if (nodeRedisClient && message && streamKeyName) {
      const id = "*"; //* = auto generate
      await nodeRedisClient.xAdd(streamKeyName, id, message);
    }
  } catch (err) {
    LoggerCls.error("addMessageToStream error !", err);
    LoggerCls.error(streamKeyName, message);
  }
}

async function addMessageToTransactionStream(
  message: ITransactionStreamMessage
) {
  if (message) {
    const streamKeyName = REDIS_STREAMS.STREAMS.TRANSACTIONS;
    await addMessageToStream(message, streamKeyName);
  }
}
```

### How does the profile service check an order against a known profile?

So you can see above, the transaction pipeline follows `CALCULATE_IDENTITY_SCORE` -> `CALCULATE_PROFILE_SCORE` -> `ASSESS_RISK`. Let's now look at how the `profile service` subscribes to the `TRANSACTIONS` Redis stream and receives the `CALCULATE_PROFILE_SCORE` event. When the `profile service` starts, it subscribes to the `TRANSACTIONS` Redis stream and listens for events.

```js
// File: server/src/services/profile/src/service-impl.ts

function listen() {
    listenToStreams({
        streams: [
            {
                streamKeyName: REDIS_STREAMS.STREAMS.TRANSACTIONS,
                eventHandlers: {
                    [TransactionStreamActions.CALCULATE_PROFILE_SCORE]:
                        calculateProfileScore,
                },
            },
        ],
        groupName: REDIS_STREAMS.GROUPS.PROFILE,
        consumerName: REDIS_STREAMS.CONSUMERS.PROFILE,
    });
}
```

A highly simplified version of the `listenToStreams` method looks as follows. It takes in a list of streams with an associated object that maps events on the stream to a callback for processing the events. It also takes a stream group and a consumer name. Then it handles the subscription to the stream and calling on the appropriate method when an event comes in:

```js
// File: server/src/common/utils/redis/redis-streams.ts

interface ListenStreamOptions {
  streams: {
    streamKeyName: string,
    eventHandlers: {
      [messageAction: string]: IMessageHandler,
    },
  }[];
  groupName: string;
  consumerName: string;
  maxNoOfEntriesToReadAtTime?: number;
}

const listenToStreams = async (options: ListenStreamOptions) => {
  /*
   (A) create consumer group for the stream
   (B) read set of messages from the stream
   (C) process all messages received
   (D) trigger appropriate action callback for each message
   (E) acknowledge individual messages after processing
  */

  const nodeRedisClient = getNodeRedisClient();
  if (nodeRedisClient) {
    const streams = options.streams;
    const groupName = options.groupName;
    const consumerName = options.consumerName;
    const readMaxCount = options.maxNoOfEntriesToReadAtTime || 100;
    const idInitialPosition = "0"; //0 = start, $ = end or any specific id
    const streamKeyIdArr: {
      key: string,
      id: string,
    }[] = [];

    streams.map(async (stream) => {
      LoggerCls.info(
        `Creating consumer group ${groupName} in stream ${stream.streamKeyName}`
      );

      try {
        // (A) create consumer group for the stream
        await nodeRedisClient.xGroupCreate(
          stream.streamKeyName,
          groupName,
          idInitialPosition,
          {
            MKSTREAM: true,
          }
        );
      } catch (err) {
        LoggerCls.error(
          `Consumer group ${groupName} already exists in stream ${stream.streamKeyName}!`
        ); //, err
      }

      streamKeyIdArr.push({
        key: stream.streamKeyName,
        id: ">", // Next entry ID that no consumer in this group has read
      });
    });

    LoggerCls.info(`Starting consumer ${consumerName}.`);

    while (true) {
      try {
        // (B) read set of messages from different streams
        const dataArr = await nodeRedisClient.xReadGroup(
          commandOptions({
            isolated: true,
          }),
          groupName,
          consumerName,
          //can specify multiple streams in array [{key, id}]
          streamKeyIdArr,
          {
            COUNT: readMaxCount, // Read n entries at a time
            BLOCK: 5, //block for 0 (infinite) seconds if there are none.
          }
        );

        // dataArr = [
        //   {
        //     name: 'streamName',
        //     messages: [
        //       {
        //         id: '1642088708425-0',
        //         message: {
        //           key1: 'value1',
        //         },
        //       },
        //     ],
        //   },
        // ];

        //(C) process all messages received
        if (dataArr && dataArr.length) {
          for (let data of dataArr) {
            for (let messageItem of data.messages) {
              const streamKeyName = data.name;

              const stream = streams.find(
                (s) => s.streamKeyName == streamKeyName
              );

              if (stream && messageItem.message) {
                const streamEventHandlers = stream.eventHandlers;
                const messageAction = messageItem.message.action;
                const messageHandler = streamEventHandlers[messageAction];

                if (messageHandler) {
                  // (D) trigger appropriate action callback for each message
                  await messageHandler(messageItem.message, messageItem.id);
                }
                //(E) acknowledge individual messages after processing
                nodeRedisClient.xAck(streamKeyName, groupName, messageItem.id);
              }
            }
          }
        } else {
          // LoggerCls.info('No new stream entries.');
        }
      } catch (err) {
        LoggerCls.error("xReadGroup error !", err);
      }
    }
  }
};
```

The `processTransactionStream` method is called when a new event comes in. It validates the event, making sure it is the `CALCULATE_PROFILE_SCORE` event, and if it is then it calculates the profile score. It uses a Redis Bloom filter to check if the user has ordered a similar set of products before. It uses a pre-defined persona for the purposes of this demo, but in reality you would build a profile of the user over time. In the demo application, each product has a "master category" and "subcategory". Bloom filters are setup for the master categories as well as the master+subcategories. The scoring logic is highlighted below:

```js
// File: server/src/services/profile/src/service-impl.ts

async function calculateProfileScore(
  message: ITransactionStreamMessage,
  messageId
) {
  LoggerCls.info(`Incoming message in Profile Service ${messageId}`);
  if (!(message.orderDetails && message.persona)) {
    return false;
  }

  await streamLog({
    action: TransactionStreamActions.CALCULATE_PROFILE_SCORE,
    message: `[${REDIS_STREAMS.CONSUMERS.PROFILE}] Calculating profile score for the user ${message.userId}`,
    metadata: message,
  });

  // check profile score
  const { products }: IOrderDetails = JSON.parse(message.orderDetails);
  const persona = message.persona.toLowerCase();
  let score = 0;
  const nodeRedisClient = getNodeRedisClient();

  if (!nodeRedisClient) {
    return false;
  }

  const categories = products.reduce((cat, product) => {
    const masterCategory = product.productData?.masterCategory?.typeName;
    const subCategory = product.productData?.subCategory?.typeName;

    if (masterCategory) {
      cat[`${masterCategory}`.toLowerCase()] = true;

      if (subCategory) {
        cat[`${masterCategory}:${subCategory}`.toLowerCase()] = true;
      }
    }

    return cat;
  }, {} as Record<string, boolean>);

  const categoryKeys = Object.keys(categories);
  const checks = categoryKeys.length;

  LoggerCls.info(
    `Checking ${checks} categories: ${JSON.stringify(categoryKeys)}`
  );

  await Promise.all(
    categoryKeys.map(async (category) => {
      const exists = await nodeRedisClient.bf.exists(
        `bfprofile:${category}`.toLowerCase(),
        persona
      );

      if (exists) {
        score += 1;
      }
    })
  );

  LoggerCls.info(`After ${checks} checks, total score is ${score}`);
  score = score / (checks || 1);

  await streamLog({
    action: TransactionStreamActions.CALCULATE_PROFILE_SCORE,
    message: `[${REDIS_STREAMS.CONSUMERS.PROFILE}] Profile score for the user ${message.userId} is ${score}`,
    metadata: message,
  });

  await nextTransactionStep({
    ...message,
    logMessage: `[${REDIS_STREAMS.CONSUMERS.PROFILE}] Requesting next step in transaction risk scoring for the user ${message.userId}`,
    profileScore: `${score}`,
  });

  return true;
}
```

The `nextTransactionStep` method is called after the profile score has been calculated. It uses the `transactionPipeline` setup in the `order service` to publish the `ASSESS_RISK` event. The logic for this is below:

```js
// File: server/src/common/utils/redis/redis-streams.ts

async function nextTransactionStep(message: ITransactionStreamMessage) {
  const transactionPipeline: TransactionStreamActions[] = JSON.parse(
    message.transactionPipeline
  );
  transactionPipeline.shift();

  if (transactionPipeline.length <= 0) {
    return;
  }

  const streamKeyName = REDIS_STREAMS.STREAMS.TRANSACTIONS;
  await addMessageToStream(
    {
      ...message,
      action: transactionPipeline[0],
      transactionPipeline: JSON.stringify(transactionPipeline),
    },
    streamKeyName
  );
}
```

In short, the `nextTransactionStep` method pops the current event off of the `transactionPipeline`, then it publishes the next event in the pipeline, which in this case is the `ASSESS_RISK` event.

### How does the order service finalize an order with risk scoring?

The `order service` is responsible for finalizing the order prior to payment. It listens to the `ASSESS_RISK` event, and then checks the calculated scores to determine if there is potential fraud.

> **NOTE**
>
> The demo app keeps things very simple, and it only sets a "potentialFraud" flag on the order. In the real world, you need to choose not only what scoring makes sense for your app, but also how to handle potential fraud. For example, you may want to request additional information from the customer such as a one-time password. You may also want to send the order to a human for review. It depends on your business and your risk appetite and mitigation strategy.

The logic to process and finalize orders in the `order service` is below:

```js
// File: server/src/services/orders/src/service-impl.ts

async function checkOrderRiskScore(message: ITransactionStreamMessage) {
  LoggerCls.info(`Incoming message in Order Service`);
  if (!message.orderDetails) {
    return false;
  }

  const orderDetails: IOrderDetails = JSON.parse(message.orderDetails);

  if (!(orderDetails.orderId && orderDetails.userId)) {
    return false;
  }

  LoggerCls.info(
    `Transaction risk scoring for user ${message.userId} and order ${orderDetails.orderId}`
  );

  const { identityScore, profileScore } = message;
  const identityScoreNumber = Number(identityScore);
  const profileScoreNumber = Number(profileScore);
  let potentialFraud = false;

  if (identityScoreNumber <= 0 || profileScoreNumber < 0.5) {
    LoggerCls.info(
      `Transaction risk score is too low for user ${message.userId} and order ${orderDetails.orderId}`
    );

    await streamLog({
      action: TransactionStreamActions.ASSESS_RISK,
      message: `[${REDIS_STREAMS.CONSUMERS.ORDERS}] Order failed fraud checks for orderId ${orderDetails.orderId} and user ${message.userId}`,
      metadata: message,
    });

    potentialFraud = true;
  }

  orderDetails.orderStatus = ORDER_STATUS.PENDING;
  orderDetails.potentialFraud = potentialFraud;

  updateOrderStatusInRedis(orderDetails);
  /**
   * In real world scenario : can use RDI/ redis gears/ any other database to database sync strategy for REDIS-> Store of record data transfer.
   * To keep it simple, adding  data to MongoDB manually in the same service
   */
  updateOrderStatusInMongoDB(orderDetails);

  message.orderDetails = JSON.stringify(orderDetails);

  await streamLog({
    action: TransactionStreamActions.ASSESS_RISK,
    message: `[${REDIS_STREAMS.CONSUMERS.ORDERS}] Order status updated after fraud checks for orderId ${orderDetails.orderId} and user ${message.userId}`,
    metadata: message,
  });

  await nextTransactionStep(message);

  return true;
}
```

## How can you visualize transaction risk scoring data in Redis Insight?

> **TIP**
>
> Redis Insight is the free redis GUI for viewing data in redis. [Click here to download.](https://redis.io/insight/)

Now that you understand some of the code involved in processing transactions, let's take a look at the data in Redis Insight. First let's look at the `TRANSACTION_STREAM` key, which is where the stream data is held for the checkout transaction:

![Redis Insight GUI showing the TRANSACTION_STREAM key with calculated identity and profile risk scores for fraud detection](/images/site-mirror/5ecbdf56d7ebe54cebe3b574b2f21258aab25090-638x753.webp)

You can see the `action` column shows the transaction pipeline discussed earlier. Another thing to look at in Redis Insight is the Bloom filters:

![Redis Insight showing Bloom filter keys used for behavioral profiling across product categories and customer personas](/images/site-mirror/fe42004b0bcadda7712b23e43a06dc6f5338f7a5-1036x546.webp)

These filters are pre-populated in the demo application based on a feature store. Redis is also storing the features, which in this case is the profiles of each of the personas. Below is an example of one of the profile features:

![Redis Insight displaying a customer persona profile feature stored as a JSON object in the Redis feature store](/images/site-mirror/94aa4c02a9144b0edf2b626f018b3ecf542b7c66-698x581.webp)

## Conclusion

In this tutorial, you learned how to use Redis Streams to build a transaction risk scoring pipeline for real-time fraud detection. You also learned how to use Redis Cloud as an in-memory feature store and Redis Bloom filters to calculate behavioral profile scores. Every app is unique, so this tutorial is meant to be a starting point for you to build your own transaction risk scoring pipeline.

## Next steps

Now that you understand how to build a transaction risk scoring system with Redis, here are some ways to go further:

- **Add digital identity validation**: Combine transaction risk scoring with [digital identity validation](/tutorials/howtos/solutions/fraud-detection/digital-identity-validation) for a more comprehensive fraud detection system.
- **Build a complete fraud detection system**: Follow the [fraud detection system tutorial](/tutorials/howtos/frauddetection/) to understand the full architecture.
- **Explore microservices patterns**: Learn more about [interservice communication with Redis](/tutorials/howtos/solutions/microservices/interservice-communication) to improve your event-driven architecture.
- **Try Redis Cloud**: [Get started with Redis Cloud for free](https://redis.io/try-free/) to deploy your risk scoring pipeline in production.

### Additional resources

Redis Streams

- Explore streams in detail in the [Redis University course on Redis Streams](https://university.redis.io/learningpath/grnomm8jaglgcu?tab=details)
- Check out our e-book on [Understanding Streams in Redis and Kafka: A Visual Guide](https://redis.io/resources/understanding-streams-in-redis-and-kafka-a-visual-guide/)

Fraud detection with Redis

- [Digital identity validation](/tutorials/howtos/solutions/fraud-detection/digital-identity-validation)
- [Fraud detection system overview](/tutorials/howtos/frauddetection/)
- [Microservices with Redis](/tutorials/howtos/solutions/microservices/interservice-communication)

General

- [Redis YouTube channel](https://www.youtube.com/c/Redisinc)
- Clients like [Node Redis](https://github.com/redis/node-redis) and [Redis om Node](https://github.com/redis/redis-om-node) help you to use Redis in Node.js apps.
- [Redis Insight](https://redis.io/insight/): To view your Redis data or to play with raw Redis commands in the workbench
- [Try Redis Cloud for free](https://redis.io/try-free/)
