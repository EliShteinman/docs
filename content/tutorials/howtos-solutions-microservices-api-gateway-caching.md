---
title: "How to use Redis for API Gateway Caching"
linkTitle: "How to use Redis for API Gateway Caching"
url: "/tutorials/howtos/solutions/microservices/api-gateway-caching/"
description: "So you're building a microservices application. But you find yourself struggling with ways to handle authentication that let you reuse code and maximize performance. Typically for authentication..."
aliases:
- "/tutorials/howtos-solutions-microservices-api-gateway-caching/"
date: 2026-02-25
lastmod: 2026-02-26
hidden: true
---

*Published 25 February 2026 · updated 26 February 2026*

> **TL;DR:**
>
> To cache API gateway data with Redis, decode the authorization token at the gateway layer, store the session in Redis using `SET`, and retrieve it on each request with `GET`. Pass the cached session to downstream microservices via a custom header (e.g. `x-session`), eliminating redundant auth lookups and reducing response times.

> **GITHUB CODE**
>
> Below is a command to the clone the source code for the application used in this tutorial
>
> git clone --branch v4.2.0 [https://github.com/redis-developer/redis-microservices-ecommerce-solutions](https://github.com/redis-developer/redis-microservices-ecommerce-solutions)

## What you'll learn

- What API gateway caching is and why it matters for microservices
- Why Redis is a strong choice for session and auth token caching
- How to store and retrieve session data in Redis at the gateway layer
- How to pass cached session information to downstream microservices
- How to structure an e-commerce microservices architecture with Redis caching

## What is API gateway caching?

So you're building a microservices application. But you find yourself struggling with ways to handle authentication that let you reuse code and maximize performance. Typically for authentication you might use sessions, OAuth, authorization tokens, etc. For the purposes of this tutorial, let's assume we're using an authorization token. In a monolithic application, authentication is pretty straightforward:

When a request comes in:

1.  Decode the `Authorization` header.
2.  Validate the credentials.
3.  Store the session information on the request object or cache for further use down the line by the application.

However, you might be puzzled by how to do this with microservices. Ordinarily, in a microservices application an API gateway serves as the single entry point for clients, which routes traffic to the appropriate services. Depending on the nature of the request, those services may or may not require a user to be authenticated. You might think it's a good idea to handle authentication in each respective service.

While this works, you end up with a fair amount of duplicated code. Plus, it's difficult to understand when and where slowdowns happen and to scale services appropriately, because you repeat some of the same work in each service. A more effective way to handle authentication is to deal with it at the API gateway layer, and then pass the session information down to each service.

Once you decide to handle authentication at the API gateway layer, you must decide where to store sessions.

Imagine you're building an e-commerce application that uses MongoDB/ any relational database as the primary data store. You could store sessions in primary database, but think about how many times the application needs to hit primary database to retrieve session information. If you have millions of customers, you don't want to go to database for every single request made to the API.

This is where Redis comes in. If you're also looking to speed up database reads, see the [query caching](/tutorials/howtos/solutions/microservices/caching/) tutorial for a complementary approach.

## Why should you use Redis for API gateway caching?

Redis is an in-memory datastore, which – among other things – makes it a perfect tool for caching session data. Redis allows you to reduce the load on a primary database while speeding up database reads. The rest of this tutorial covers how to accomplish this in the context of an e-commerce application.

## What does a microservices architecture with Redis caching look like?

The e-commerce microservices application discussed in the rest of this tutorial uses the following architecture:

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

The diagram illustrates how the API gateway uses Redis as a cache for session information. The API gateway gets the session from Redis and then passes it on to each microservice. This provides an easy way to handle sessions in a single place, and to permeate them throughout the rest of the microservices.

![Architecture diagram showing an API gateway caching session data in Redis and passing it to downstream microservices including orders, payments, and product services](/images/site-mirror/764717267bec355266148831d786c1142efc13c3-1663x1103.webp)

> **TIP**
>
> Use a **Redis Cloud Cluster** to get the benefit of linear scaling to ensure API calls perform under peak loads. That also provides 99.999% uptime and Active-Active geo-distribution, which prevents loss of authentication and session data.

## What does the e-commerce application frontend look like?

The e-commerce microservices application consists of a frontend, built using [Next.js](https://nextjs.org/) with [TailwindCSS](https://tailwindcss.com/). The application backend uses [Node.js](https://nodejs.org/). The data is stored in [Redis](https://redis.io/try-free/) and MongoDB/ Postgressql using [Prisma](https://www.prisma.io/docs/reference/database-reference/supported-databases). Below you will find screenshots of the frontend of the e-commerce app:

- `Dashboard`: Shows the list of products with search functionality

![E-commerce application dashboard built with Next.js showing a product grid with search functionality and category filters](/images/site-mirror/4f6a862752feff8ae6a946d92e5895906af325f3-1982x1500.webp)

`Shopping Cart`: Add products to the cart, then check out using the "Buy Now" button

![Shopping cart page in the e-commerce microservices demo app showing selected products with a Buy Now checkout button](/images/site-mirror/776a16cd58782fb2ff513b9271b2b00b6a5d2d60-2000x1076.webp)

> **GITHUB CODE**
>
> Below is a command to the clone the source code for the application used in this tutorial
>
> git clone --branch v4.2.0 [https://github.com/redis-developer/redis-microservices-ecommerce-solutions](https://github.com/redis-developer/redis-microservices-ecommerce-solutions)

## How do you implement API gateway caching with Redis?

What's nice about a microservice architecture is that each service is set up so it can scale independently. For more on how services communicate with each other, see the [interservice communication](/tutorials/howtos/solutions/microservices/interservice-communication/) tutorial. Now, seeing as how each service might require authentication, you likely want to obtain session information for most requests. Therefore, it makes sense to use the API gateway to cache and retrieve session information and to subsequently pass the information on to each service. Let's see how you might accomplish this.

In our sample application, all requests are routed through the API gateway. We use [Express](https://expressjs.com/) to set up the API gateway, and the `Authorization` header to pass the authorization token from the frontend to the API. For every request, the API gateway gets the authorization token and looks it up in Redis. Then it passes it along to the correct microservice.

This code validates the session:

```js
// File: server/src/api-gateway/src/index.ts

import {
  createProxyMiddleware,
  responseInterceptor,
} from "http-proxy-middleware";

//-----
const app: Express = express();

app.use(cors());
app.use(async (req, res, next) => {
  const authorizationHeader = req.header("Authorization");
  const sessionInfo = await getSessionInfo(authorizationHeader); //---- (1)

  //add session info to request
  if (sessionInfo?.sessionData && sessionInfo?.sessionId) {
    req.session = sessionInfo?.sessionData;
    req.sessionId = sessionInfo?.sessionId;
  }
  next();
});

app.use(
  "/orders",
  createProxyMiddleware({
    // http://localhost:3000/orders/bar -> http://localhost:3001/orders/bar
    target: "http://localhost:3001",
    changeOrigin: true,
    selfHandleResponse: true,
    onProxyReq(proxyReq, req, res) {
      // pass session info to microservice
      proxyReq.setHeader("x-session", req.session);
    },
    onProxyRes: applyAuthToResponse, //---- (2)
  })
);

app.use(
  "/orderHistory",
  createProxyMiddleware({
    target: "http://localhost:3002",
    changeOrigin: true,
    selfHandleResponse: true,
    onProxyReq(proxyReq, req, res) {
      // pass session info to microservice
      proxyReq.setHeader("x-session", req.session);
    },
    onProxyRes: applyAuthToResponse, //---- (2)
  })
);
//-----

const getSessionInfo = async (authHeader?: string) => {
  // (For demo purpose only) random userId and sessionId values are created for first time, then userId is fetched gainst that sessionId for future requests
  let sessionId = "";
  let sessionData: string | null = "";

  if (!!authHeader) {
    sessionId = authHeader.split(/\s/)[1];
  } else {
    sessionId = "SES_" + randomUUID(); // generate random new sessionId
  }

  const nodeRedisClient = getNodeRedisClient();
  if (nodeRedisClient) {
    const exists = await nodeRedisClient.exists(sessionId);
    if (!exists) {
      await nodeRedisClient.set(
        sessionId,
        JSON.stringify({ userId: "USR_" + randomUUID() })
      ); // generate random new userId
    }
    sessionData = await nodeRedisClient.get(sessionId);
  }

  return {
    sessionId: sessionId,
    sessionData: sessionData,
  };
};

const applyAuthToResponse = responseInterceptor(
  // adding sessionId to the response so that frontend can store it for future requests

  async (responseBuffer, proxyRes, req, res) => {
    // detect json responses
    if (
      !!proxyRes.headers["content-type"] &&
      proxyRes.headers["content-type"].includes("application/json")
    ) {
      let data = JSON.parse(responseBuffer.toString("utf8"));

      // manipulate JSON data here
      if (!!(req as Request).sessionId) {
        data = Object.assign({}, data, { auth: (req as Request).sessionId });
      }

      // return manipulated JSON
      return JSON.stringify(data);
    }

    // return other content-types as-is
    return responseBuffer;
  }
);
```

> **INFO**
>
> This example is not meant to represent the best way to handle authentication. Instead, it illustrates what you might do with respect to Redis. You will likely have a different setup for authentication, but the concept of storing a session in Redis is similar.

In the code above, we check for the `Authorization` header, otherwise we create a new one and store it in Redis. Then we retrieve the session from Redis. Further down the line we attach the session to the `x-session` header prior to calling the orders service.

Now let's see how the orders service receives the session.

```js
// File: server/src/services/orders/src/routes.ts

router.post(API_NAMES.CREATE_ORDER, async (req: Request, res: Response) => {
  const body = req.body;
  const result: IApiResponseBody = {
    data: null,
    error: null,
  };

  const sessionData = req.header('x-session'); // highlighted
  const userId = sessionData ? JSON.parse(sessionData).userId : "";
  ...
});
```

The highlighted line above shows how to pull the session out of the x-session header and get the userId.

## What are the next steps for Redis API gateway caching?

You now know how to use Redis for API gateway caching. By caching session data at the gateway layer, you avoid duplicating authentication logic across services and reduce response times for every request that flows through your microservices architecture.

To take your microservices architecture further, consider these next steps:

- **Add query caching**: Use Redis to [cache database query results](/tutorials/howtos/solutions/microservices/caching/) and reduce load on your primary database.
- **Improve interservice communication**: Learn how to use Redis Streams for [reliable messaging between microservices](/tutorials/howtos/solutions/microservices/interservice-communication/).
- **Apply the CQRS pattern**: Separate read and write workloads with the [CQRS pattern using Redis](/tutorials/howtos/solutions/microservices/cqrs/).
- **Scale with Redis Cloud**: Use a [Redis Cloud Cluster](https://redis.io/try-free/) for linear scaling, 99.999% uptime, and Active-Active geo-distribution.

### Additional resources

- [Redis YouTube channel](https://www.youtube.com/c/Redisinc)
- Clients like [Node Redis](https://github.com/redis/node-redis) and [Redis om Node](https://github.com/redis/redis-om-node) help you to use Redis in Node.js apps.
- [Redis Insight](https://redis.io/insight/) : To view your Redis data or to play with raw Redis commands in the workbench
- [Try Redis Cloud for free](https://redis.io/try-free/)
