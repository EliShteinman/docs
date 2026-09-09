---
title: "Mobile Banking Authentication and Session Storage Using Redis"
linkTitle: "Mobile Banking Authentication and Session Storage Using Redis"
url: "/tutorials/howtos/solutions/mobile-banking/session-management/"
description: "After a user has successfully entered their login credentials, mobile banking apps use a token and sessionId created by the server to represent a user's identity. The token is stored in Redis for..."
aliases:
- "/tutorials/howtos-solutions-mobile-banking-session-management/"
date: 2026-02-25
lastmod: 2026-02-26
hidden: true
---

*Published 25 February 2026 · updated 26 February 2026*

> **TL;DR:**
>
> Use Redis as your session store for mobile banking by pairing [`express-session`](https://www.npmjs.com/package/express-session) with [`connect-redis-stack`](https://www.npmjs.com/package/connect-redis-stack). Redis stores session data as JSON with automatic TTL-based expiry, giving you sub-millisecond reads, built-in session timeout via `ttlInSeconds`, and the ability to query or invalidate sessions instantly.

> **GITHUB CODE**
>
> Below is a command to the clone the source code for the application used in this tutorial
>
> git clone --branch v1.2.0 [https://github.com/redis-developer/mobile-banking-solutions](https://github.com/redis-developer/mobile-banking-solutions)

## What you'll learn

- How Redis stores and expires mobile banking sessions using TTL
- How to configure `express-session` with a Redis session store
- How session IDs and tokens flow between client and server
- How to attach real-time data (like account balances) to sessions
- How to seed and visualize banking transaction data in Redis

## What is authentication and session storage for mobile banking?

After a user has successfully entered their login credentials, mobile banking apps use a `token` and `sessionId` created by the server to represent a user's identity. The `token` is stored in Redis for the duration of a user session and also sent in the login response to the banking application client (mobile/ browser). The client application then sends the `token` with every request to server and server validates it before processing the request.

![Architecture diagram showing the authentication and session token flow between a mobile banking client, the server, and Redis](/images/site-mirror/723cde11b807329877b1991b3790dcc34fd07b2d-1610x1250.webp)

> **NOTE**
>
> Redis supports the **JSON** data type and allows you to [index and querying JSON](https://redis.io/docs/latest/develop/ai/search-and-query/). So your session store is not limited to simple key-value stringified data.

The session store houses critical information related to each user as they navigate an application for the duration of their session. Mobile banking session data may include, but is not limited to following information:

- User's profile information, such as name, date of birth, email address, etc.
- User's permissions, such as `user`, `admin`, `supervisor`, `super-admin`, etc.
- Other app-related data like recent transaction(s), balance etc.
- Session expiration, such as one hour from now, one week from now, etc.

## Why should you use Redis for mobile banking session management?

- **Resilience**: Redis Cloud offers incredible resilience with **99.999% uptime**. After all, authentication token stores must provide round-the-clock availability. This ensures that users get uninterrupted, 24/7 access to their apps.
- **Scalability**: Token stores need to be highly scalable so that they don't become a bottleneck when a **high volume of users** authenticate at once. Redis Cloud provides **< 1ms latency** at incredibly high throughput (up to **100MM ops/second**) which makes authentication and session data access much faster!
- **Integration with common libraries and platforms**: Since Redis open source is integrated into most session management libraries and platforms, Redis Cloud can seamlessly integrate when upgrading from open source Redis (e.g. `express-session` and `[connect-redis-stack](https://www.npmjs.com/package/connect-redis-stack)` libraries integration is demonstrated in this tutorial)

## How do you build session management with Redis?

> **GITHUB CODE**
>
> Below is a command to the clone the source code for the application used in this tutorial
>
> git clone --branch v1.2.0 [https://github.com/redis-developer/mobile-banking-solutions](https://github.com/redis-developer/mobile-banking-solutions)

Download the above source code and run following command to start the demo application

```bash
docker compose up
```

After docker up & running, open [http://localhost:8080/](http://localhost:8080/) url in browser to view application

### How is transaction data seeded into Redis?

This application leverages **Redis core data structures, JSON, TimeSeries, Search and Query features**. The data seeded is later used to show a searchable transaction overview with realtime updates as well as a personal finance management overview with realtime balance and biggest spenders updates.

On application startup in `app/server.js`, a cron is scheduled to create random bank transactions at regular intervals and seed those transactions in to Redis.

```js
//cron job to trigger createBankTransaction() at regular intervals

cron.schedule('*/10 * * * * *', async () => {
    const userName = process.env.REDIS_USERNAME;

    createBankTransaction(userName);

    //...
});
```

- The transaction generator creates a randomized banking debit or credit which will reflect on a (default) starting user balance of $100,000.00
- The **transaction data** is saved as a JSON document within Redis.
- To capture **balance over time**, the `balanceAfter` value is recorded in a TimeSeries with the key `balance_ts` for every transaction.
- To track **biggest spenders**, an associated `**fromAccountName**` member within the sorted set `bigspenders` is incremented by the transaction amount. Note that this amount can be positive or negative.

```js
let balance = 100000.0;
const BALANCE_TS = 'balance_ts';
const SORTED_SET_KEY = 'bigspenders';

export const createBankTransaction = async () => {
    //to create random bank transaction
    let vendorsList = source.source; //app/transactions/transaction_sources.js
    const random = Math.floor(Math.random() * 9999999999);

    const vendor = vendorsList[random % vendorsList.length]; //random vendor from the list

    const amount = createTransactionAmount(vendor.fromAccountName, random);
    const transaction = {
        id: random * random,
        fromAccount: Math.floor((random / 2) * 3).toString(),
        fromAccountName: vendor.fromAccountName,
        toAccount: '1580783161',
        toAccountName: 'bob',
        amount: amount,
        description: vendor.description,
        transactionDate: new Date(),
        transactionType: vendor.type,
        balanceAfter: balance,
    };

    //redis json feature
    const bankTransaction = await bankTransactionRepository.save(transaction);
    console.log('Created bankTransaction!');
    // ...
};

const createTransactionAmount = (vendor, random) => {
    let amount = createAmount(); //random amount
    balance += amount;
    balance = parseFloat(balance.toFixed(2));

    //redis time series feature
    redis.ts.add(BALANCE_TS, '*', balance, { DUPLICATE_POLICY: 'first' });
    //redis sorted set as secondary index
    redis.zIncrBy(SORTED_SET_KEY, amount * -1, vendor);

    return amount;
};
```

Sample bankTransaction data view using [Redis Insight](https://redis.io/insight/)

![Redis Insight JSON tree view of a bankTransaction document showing fields like id, fromAccount, amount, and balanceAfter](/images/site-mirror/9935751e0e2b00f31b3931cb14b0883bcecabe2d-900x355.webp)

![Expanded Redis Insight view of a single bank transaction record with all JSON fields visible](/images/site-mirror/acad0d24e2816152471d202e60e9e3a06637cb2e-1336x858.webp)

> **TIP**
>
> Download [**Redis Insight**](https://redis.io/insight/) to view your Redis data or to play with raw Redis commands in the workbench.

### How do you configure Redis as a session store?

Redis is integrated into many session management libraries, We will be using [connect-redis-stack](https://www.npmjs.com/package/connect-redis-stack) library for this demo which provides Redis session storage for your [express-session](https://www.npmjs.com/package/express-session) application.

The following code illustrates configuring Redis sessions and with `express-session`.

```js
// app/server.js
import session from 'express-session';
import { RedisStackStore } from 'connect-redis-stack';

/* configure your session store */
const store = new RedisStackStore({
    client: redis, //redis client
    prefix: 'redisBank:', //redis key prefix
    ttlInSeconds: 3600, //session expiry time
});

const app = express();

// ...

app.use(
    session({
        store: store, //using redis store for session
        resave: false,
        saveUninitialized: false,
        secret: '5UP3r 53Cr37', //from env file
    }),
);

//...
app.listen(8080, () => console.log('Listening on port 8080'));
```

### How does the login API generate a session ID?

![Mobile banking login screen with username and password fields and a sign-in button](/images/site-mirror/f6d716f142865be6a0bc32037c1a4a1e977b0433-900x674.webp)

Let's look at the `/perform_login` API code which is triggered on the click of Login button from [login page](http://localhost:8080/)

Since [connect-redis-stack](https://www.npmjs.com/package/connect-redis-stack) is an express middleware, a session is automatically created at the start of the request, and updated at the end of the HTTP(API) response if `req.session` variable is altered.

```js
app.post('/perform_login', (req, res) => {
    let session = req.session;
    console.log(session);
    /*
  Session {
    cookie: { path: '/', _expires: null, originalMaxAge: null, httpOnly: true }
  }
  */
    //hardcoded user for demo
    if (req.body.username == 'bob' && req.body.password == 'foobared') {
        //on successful login (for bob user)
        session = req.session;
        session.userid = req.body.username; //create session data
        res.redirect('/index.html');
    } else {
        res.redirect('/auth-login.html');
    }
});
```

In above code - `session.userid` variable is assigned with a value on successful login (for "bob" user), so a session is created in Redis with assigned data and only Redis key (sessionId) is stored in client cookie.

- Dashboard page after successful login

![Mobile banking dashboard after login showing recent transactions list and current account balance chart](/images/site-mirror/bd2e4798d8476d1e3af763998cee13cce0fc4c5e-1000x492.webp)

- Session entry in Redis

![Redis Insight showing the session JSON document stored under the redisBank prefix with cookie and userid fields](/images/site-mirror/1984f119d58de6b8136074d7a9c6f74f579c614b-900x402.webp)

- Open developer tools in Dashboard page to check client cookie `connect.sid` (containing only sessionId)

![Browser developer tools Application tab showing the connect.sid cookie containing the encrypted session ID](/images/site-mirror/99762ecf1e2bfdff17217f6dc6da129d8000a11d-900x375.webp)

Now on every other API request from client, [connect-redis-stack](https://www.npmjs.com/package/connect-redis-stack) library makes sure to load session details from redis to `req.session` variable based on the client cookie (sessionId).

### How do you store real-time balance data in sessions?

Consider the below `/transaction/balance` API code to demonstrate session storage.

We have to modify the `req.session` variable to update session data. Let's add more session data like current balance amount of the user .

```js
// app/routers/transaction-router.js
/* fetch all transactions up to an hour ago /transaction/balance */
transactionRouter.get('/balance', async (req, res) => {
    const balance = await redis.ts.range(
        BALANCE_TS,
        Date.now() - 1000 * 60 * 5,
        Date.now(),
    );

    let balancePayload = balance.map((entry) => {
        return {
            x: entry.timestamp,
            y: entry.value,
        };
    });

    let session = req.session;
    if (session.userid && balancePayload.length) {
        //adding latest BalanceAmount to session
        session.currentBalanceAmount =
            balancePayload[balancePayload.length - 1]; //updating session data
    }

    res.send(balancePayload);
});
```

- Updated session entry in Redis with `currentBalanceAmount` field ('x' denoting timestamp and 'y' denoting balance amount at that timestamp)

![Redis Insight showing the session document now includes a currentBalanceAmount object with timestamp and balance value](/images/site-mirror/897fe40d498ff706997afd68ae9e64eb0ef477c7-1326x666.webp)

- Verify the latest balance amount in the Dashboard UI

![Dashboard UI balance chart confirming the latest balance amount matches the value stored in the Redis session](/images/site-mirror/101ab30269936964d3caa72a26a6c06f74f6c9f8-966x950.webp)

## Ready to use Redis for secure session management?

Hopefully, this tutorial has helped you visualize how to use Redis for better session management, specifically in the context of mobile banking. For additional resources related to this topic, check out the links below:

### Next steps

- Build out the [account dashboard](/tutorials/howtos/solutions/mobile-banking/account-dashboard/) to display transaction history and financial insights alongside session data
- Explore [Redis Insight](https://redis.io/insight/) to inspect and debug your session store in real time
- Try [Redis Cloud for free](https://redis.io/try-free/) for a fully managed Redis deployment with 99.999% uptime

### Additional resources

- [Redis YouTube channel](https://www.youtube.com/c/Redisinc)
- Clients like [Node Redis](https://github.com/redis/node-redis) and [Redis OM Node](https://github.com/redis/redis-om-node) help you to use Redis in Node.js applications.
- [Redis Insight](https://redis.io/insight/): To view your Redis data or to play with raw Redis commands in the workbench
- [Try Redis Cloud for free](https://redis.io/try-free/)
