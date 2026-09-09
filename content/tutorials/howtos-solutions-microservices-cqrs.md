---
title: "How to Build an E-Commerce App Using Redis with the CQRS Pattern"
linkTitle: "How to Build an E-Commerce App Using Redis with the CQRS Pattern"
url: "/tutorials/howtos/solutions/microservices/cqrs/"
description: "Command Query Responsibility Segregation (CQRS) is a critical pattern within a microservice architecture. It decouples reads (queries) and writes (commands), which permits read and write workloads..."
aliases:
- "/tutorials/howtos-solutions-microservices-cqrs/"
date: 2026-02-25
lastmod: 2026-02-25
hidden: true
---

*Published 25 February 2026*

> **TL;DR:**
>
> CQRS (Command Query Responsibility Segregation) separates read and write operations so each can scale independently. Redis serves as the fast read-side query store in a CQRS architecture, letting you cache data as JSON documents and search them in real time while your primary database handles durable writes.

> **GITHUB CODE**
>
> Below is a command to the clone the source code for the application used in this tutorial
>
> git clone --branch v4.2.0 [https://github.com/redis-developer/redis-microservices-ecommerce-solutions](https://github.com/redis-developer/redis-microservices-ecommerce-solutions)

## What you'll learn

- What CQRS is and why it matters for microservices
- How to separate read and write paths in an e-commerce application
- How to store and query order data in Redis using Redis OM
- How to use Change Data Capture (CDC) to keep Redis in sync with a primary database
- How Redis Streams enable [interservice communication](/tutorials/howtos/solutions/microservices/interservice-communication) in a CQRS architecture

## What is command and query responsibility segregation (CQRS)?

Command Query Responsibility Segregation (CQRS) is a critical pattern within a microservice architecture. It decouples reads (queries) and writes (commands), which permits read and write workloads to work independently.

Commands (writes) focus on higher durability and consistency, while queries (reads) focus on performance. This enables a microservice to write data to a slower system-of-record disk-based database, while pre-fetching and caching that data in a cache for real-time reads.

The idea is simple: you separate commands such as "Order this product" (a write operation) from queries such as "Show me my order history" (a read operation). CQRS apps are often messaging-based and rely on [eventual consistency](https://en.wikipedia.org/wiki/Eventual_consistency).

The sample data architecture that follows demonstrates how to use Redis with CQRS:

![CQRS architecture diagram showing how Change Data Capture (CDC) replicates writes from a system-of-record database to Redis as the read-optimized query store](/images/site-mirror/2d453efbf583db41aa3478e302e1431087936b89-1313x1399.webp)

The architecture illustrated in the diagram uses the Change Data Capture pattern (noted as "Integrated CDC") to track the changed state on the command database and to replicate it to the query database (Redis). This is a common pattern used with CQRS.

Implementing CDC requires:

1.  Taking the data snapshot from the system of record
2.  Performing an ETL operation finalized to load the data on the target cache database
3.  Setting up a mechanism to continuously stream the changes in the system of record to the cache

> **TIP**
>
> While you can implement your own CDC mechanism with Redis using Triggers and Functions, Redis Cloud comes with its own integrated CDC mechanism to solve this problem for you.

## Why should you use the CQRS pattern?

To improve app performance, scale your read and write operations separately.

Consider the following scenario: You have an e-commerce app that allows a customer to populate a shopping cart with products. The site has a "Buy Now" button to facilitate ordering those products. When first starting out, you might set up and populate a product database (perhaps a SQL database). Then you might write a backend API to handle the processes of creating an order, creating an invoice, processing payments, handling fulfillment, and updating the customer's order history… all in one go.

This method of synchronous order processing seemed like a good idea. But you soon find out that your database slows down as you gain more customers and have a higher sales volume. In reality, most apps have significantly more reads than writes. You should scale those operations separately.

You decide that you need to process orders quickly so the customer doesn't have to wait. Then, when you have time, you can create an invoice, process payment, handle fulfillment, etc.

So you decide to separate each of these steps. Using a microservices approach with CQRS allows you to scale your reads and writes independently as well as aid in decoupling your microservices. With a CQRS model, a single service is responsible for handling an entire command from end to end. One service should not depend on another service in order to complete a command.

## What does a CQRS microservices architecture look like?

Let's take a look at the architecture of the demo app:

1.  `products service`: handles querying products from the database and returning them to the frontend
2.  `orders service`: handles validating and creating orders
3.  `order history service`: handles querying a customer's order history
4.  `payments service`: handles processing orders for payment
5.  `api gateway`: unifies the services under a single endpoint — see the [API gateway caching](/tutorials/howtos/solutions/microservices/api-gateway-caching) tutorial for more on this layer
6.  `mongodb/ postgresql`: serves as the write-optimized database for storing orders, order history, products, etc.

> **INFO**
>
> You don't need to use MongoDB/ Postgresql as your write-optimized database in the demo application; you can use other [prisma supported databases](https://www.prisma.io/docs/reference/database-reference/supported-databases) as well. This is just an example.

## How does Redis fit into a CQRS architecture?

Note that in the current architecture all the services use the same underlying database. Even though you're technically separating reads and writes, you can't scale the write-optimized database independently. This is where Redis comes in. If you put Redis in front of your write-optimized database, you can use it for reads while writing to the write-optimized database. The benefit of Redis is that it's fast for reads and writes, which is why it's the best choice for caching and CQRS.

> **INFO**
>
> For the purposes of this tutorial, we're not highlighting how communication is coordinated between our services, such as how new orders are processed for payment. That process uses Redis Streams, and is outlined in our [interservice communication guide](/tutorials/howtos/solutions/microservices/interservice-communication).

> **TIP**
>
> When your e-commerce app eventually needs to scale across the globe, Redis Cloud provides Active-Active geo-distribution for reads and writes at local latencies as well as availability of 99.999% uptime.

Let's look at some sample code that helps facilitate the CQRS pattern with Redis and a primary database (MongoDB/ PostgreSQL).

## What does the e-commerce app frontend look like?

The e-commerce microservices app consists of a frontend, built using [Next.js](https://nextjs.org/) with [TailwindCSS](https://tailwindcss.com/). The app backend uses [Node.js](https://nodejs.org/). The data is stored in [Redis](https://redis.io/try-free/) and MongoDB/ PostgreSQL using [Prisma](https://www.prisma.io/docs/reference/database-reference/supported-databases). Below you will find screenshots of the frontend of the e-commerce app:

- `Dashboard`: Shows the list of products with search functionality

![E-commerce dashboard displaying a product catalog with search bar, product thumbnails, prices, and Add to Cart buttons](/images/site-mirror/4f6a862752feff8ae6a946d92e5895906af325f3-1982x1500.webp)

- `Shopping Cart`: Add products to the cart, then check out using the "Buy Now" button

![Shopping cart page listing selected products with quantities, subtotals, and a Buy Now checkout button](/images/site-mirror/9f9deeb554a22a16af87671c88606ac922b8e2e7-2000x1401.webp)

- `Order history`: Once an order is placed, the Orders link in the top navigation bar shows the order status and history

![Order history page showing a list of past orders with order IDs, statuses, and timestamps](/images/site-mirror/776a16cd58782fb2ff513b9271b2b00b6a5d2d60-2000x1076.webp)

> **NOTE**
>
> Below is a command to the clone the source code for the application used in this tutorial
>
> git clone --branch v4.2.0 [https://github.com/redis-developer/redis-microservices-ecommerce-solutions](https://github.com/redis-developer/redis-microservices-ecommerce-solutions)

## How do you build the CQRS write side (commands)?

Let's look at the sample code for the order service and see the CreateOrder command (a write operation). Then we look at the order history service to see the ViewOrderHistory command (a read operation).

### Create order command API

The code that follows shows an example API request and response to create an order.

#### Create order request

```bash
POST http://api-gateway/orders/createOrder
{
  "products": [
    {
      "productId": "11002",
      "qty": 1,
      "productPrice": 4950
    },
    {
      "productId": "11012",
      "qty": 2,
      "productPrice": 1195
    }
  ]
}
```

#### Create order response

```json
{
    "data": "d4075f43-c262-4027-ad25-7b1bc8c490b6", //orderId
    "error": null
}
```

When you make a request, it goes through the API gateway to the orders service. Ultimately, it ends up calling a createOrder function which looks as follows:

```js
// File: server/src/services/orders/src/service-impl.ts
const createOrder = async (
  order: IOrder
  //...
) => {
  if (!order) {
    throw "Order data is mandatory!";
  }

  const userId = order.userId || USERS.DEFAULT; // Used as a shortcut, in a real app you would use customer session data to fetch user details
  const orderId = uuidv4();

  order.orderId = orderId;
  order.orderStatusCode = ORDER_STATUS.CREATED;
  order.userId = userId;
  order.createdBy = userId;
  order.statusCode = DB_ROW_STATUS.ACTIVE;
  order.potentialFraud = false;

  order = await validateOrder(order);

  const products = await getProductDetails(order);
  addProductDataToOrders(order, products);

  await addOrderToRedis(order);

  await addOrderToPrismaDB(order);

  //...

  return orderId;
};
```

> **INFO**
>
> For tutorial simplicity, we add data to both primary database and Redis in the same service (double-write). As mentioned earlier, a common pattern is to have your services write to one database, and then separately use a CDC mechanism to update the other database. For example, you could write directly to Redis, then use **RedisGears** to handle synchronizing Redis and primary database in the background. For the purposes of this tutorial, we don't outline exactly how you might handle synchronization, but instead focus on how the data is stored and accessed in Redis.

> **TIP**
>
> If you're using **Redis Cloud**, you can take advantage of the **integrated CDC** mechanism to avoid having to roll your own.

### How does Redis OM store orders?

Note that in the previous code block we call the addOrderToRedis function to store orders in Redis. We use [Redis OM for Node.js](https://github.com/redis/redis-om-node) to store the order entities in Redis. This is what that function looks like:

```js
// File: server/src/services/orders/src/service-impl.ts
import { Schema, Repository } from "redis-om";
import { getNodeRedisClient } from "../utils/redis/redis-wrapper";

//Redis Om schema for Order
const schema = new Schema("Order", {
  orderId: { type: "string", indexed: true },

  orderStatusCode: { type: "number", indexed: true },
  potentialFraud: { type: "boolean", indexed: false },
  userId: { type: "string", indexed: true },

  createdOn: { type: "date", indexed: false },
  createdBy: { type: "string", indexed: true },
  lastUpdatedOn: { type: "date", indexed: false },
  lastUpdatedBy: { type: "string", indexed: false },
  statusCode: { type: "number", indexed: true },
});

//Redis OM repository for Order (to read, write and remove orders)
const getOrderRepository = () => {
  const redisClient = getNodeRedisClient();
  const repository = new Repository(schema, redisClient);
  return repository;
};

//Redis indexes data for search
const createRedisIndex = async () => {
  const repository = getRepository();
  await repository.createIndex();
};

const addOrderToRedis = async (order: OrderWithIncludes) => {
  if (order) {
    const repository = getOrderRepository();
    //insert Order in to Redis
    await repository.save(order.orderId, order);
  }
};
```

Sample **Order** view using [Redis Insight](https://redis.io/insight/)

![Redis Insight interface displaying an Order JSON document with fields like orderId, orderStatusCode, userId, and product details](/images/site-mirror/0af33d20c69c938f737437cd86336abc4785ae14-1126x1448.webp)

> **TIP**
>
> Download [**Redis Insight**](https://redis.io/insight/) to view your Redis data or to play with raw Redis commands in the workbench.

## How do you query order history from Redis (the read side)?

The code that follows shows an example API request and response to get a customer's order history.

### Order history request

```bash
GET http://api-gateway/orderHistory/viewOrderHistory
```

### Order history response

```json
{
    "data": [
        {
            "orderId": "d4075f43-c262-4027-ad25-7b1bc8c490b6",
            "userId": "USR_22fcf2ee-465f-4341-89c2-c9d16b1f711b",
            "orderStatusCode": 4,
            "products": [
                {
                    "productId": "11002",
                    "qty": 1,
                    "productPrice": 4950,
                    "productData": {
                        "productId": "11002",
                        "price": 4950,
                        "productDisplayName": "Puma Men Race Black Watch",
                        "variantName": "Race 85",
                        "brandName": "Puma",
                        "ageGroup": "Adults-Men",
                        "gender": "Men",
                        "displayCategories": "Accessories",
                        "masterCategory_typeName": "Accessories",
                        "subCategory_typeName": "Watches",
                        "styleImages_default_imageURL": "http://host.docker.internal:8080/images/11002.jpg",
                        "productDescriptors_description_value": "<p>This watch from puma comes in a heavy duty design. The assymentric dial and chunky..."
                    }
                },
                {
                    "productId": "11012",
                    "qty": 2,
                    "productPrice": 1195,
                    "productData": {
                        "productId": "11012",
                        "price": 1195,
                        "productDisplayName": "Wrangler Women Frill Check Multi Tops",
                        "variantName": "FRILL CHECK",
                        "brandName": "Wrangler",
                        "ageGroup": "Adults-Women",
                        "gender": "Women",
                        "displayCategories": "Sale and Clearance,Casual Wear",
                        "masterCategory_typeName": "Apparel",
                        "subCategory_typeName": "Topwear",
                        "styleImages_default_imageURL": "http://host.docker.internal:8080/images/11012.jpg",
                        "productDescriptors_description_value": "<p><strong>Composition</strong><br /> Navy blue, red, yellow and white checked top made of 100% cotton, with a jabot collar, buttoned ..."
                    }
                }
            ],
            "createdBy": "USR_22fcf2ee-465f-4341-89c2-c9d16b1f711b",
            "lastUpdatedOn": "2023-07-13T14:11:49.997Z",
            "lastUpdatedBy": "USR_22fcf2ee-465f-4341-89c2-c9d16b1f711b"
        }
    ],
    "error": null
}
```

When you make a request, it goes through the API gateway to the `order history service`. Ultimately, it ends up calling a `viewOrderHistory` function, which looks as follows:

```js
// File: server/src/services/order-history/src/service-impl.ts
const viewOrderHistory = async (userId: string) => {
  const repository = OrderRepo.getRepository();
  let orders: Partial<IOrder>[] = [];
  const queryBuilder = repository
    .search()
    .where("createdBy")
    .eq(userId)
    .and("orderStatusCode")
    .gte(ORDER_STATUS.CREATED) //returns CREATED and PAYMENT_SUCCESS
    .and("statusCode")
    .eq(DB_ROW_STATUS.ACTIVE);

  console.log(queryBuilder.query);
  orders = <Partial<IOrder>[]>await queryBuilder.return.all();
};
```

> **INFO**
>
> Note that the `order history service` only needs to go to Redis for all orders. This is because we handle storage and synchronization between Redis and primary database within the `orders service`.

You might be used to using Redis as a cache and both storing and retrieving stringified JSON values or perhaps hashed values. However, look closely at the code above. In it, we store orders as **JSON** documents, and then use [Redis OM](https://github.com/redis/redis-om-node) to search for the orders that belong to a specific user. Redis operates like a search engine, here, with the ability to speed up queries and scale independently from the primary database (which in this case is MongoDB/ PostgreSQL).

## Next steps

This tutorial demonstrated how to use Redis with the CQRS pattern to separate read and write workloads in an e-commerce microservices application. Redis reduces the load on your primary database while giving you fast, searchable JSON document storage on the read side.

To continue building out your microservices architecture with Redis, explore these related tutorials:

- [Interservice communication with Redis Streams](/tutorials/howtos/solutions/microservices/interservice-communication) — learn how services coordinate events like order processing and payment
- [Query caching with Redis](/tutorials/howtos/solutions/microservices/caching) — implement the cache-aside pattern to speed up database reads
- [API gateway caching with Redis](/tutorials/howtos/solutions/microservices/api-gateway-caching) — cache session data and authentication at the gateway layer

### Additional resources

- [Redis YouTube channel](https://www.youtube.com/c/Redisinc)
- Clients like [Node Redis](https://github.com/redis/node-redis) and [Redis OM Node](https://github.com/redis/redis-om-node) help you to use Redis in Node.js apps.
- [Redis Insight](https://redis.io/insight/) : To view your Redis data or to play with raw Redis commands in the workbench
- [Try Redis Cloud for free](https://redis.io/try-free/)
