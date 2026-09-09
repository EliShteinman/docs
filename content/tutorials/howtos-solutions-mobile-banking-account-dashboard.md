---
title: "Mobile Banking Account Dashboard Using Redis"
linkTitle: "Mobile Banking Account Dashboard Using Redis"
url: "/tutorials/howtos/solutions/mobile-banking/account-dashboard/"
description: "An account dashboard is a page in a mobile banking app that instantly renders account highlights to users. A customer can click on any of the accounts on the dashboard to see the real-time account..."
aliases:
- "/tutorials/howtos-solutions-mobile-banking-account-dashboard/"
date: 2026-02-25
lastmod: 2026-02-26
hidden: true
---

*Published 25 February 2026 · updated 26 February 2026*

> **TL;DR:**
>
> Build a mobile banking account dashboard with Redis by caching account balances as JSON documents, tracking balance history with Time Series, ranking biggest spenders with sorted sets, and searching transactions with Search and Query. Redis delivers sub-millisecond reads so customers see real-time financial data the moment they open the app.

> **GITHUB CODE**
>
> Below is a command to the clone the source code for the application used in this tutorial
>
> git clone --branch v1.2.0 [https://github.com/redis-developer/mobile-banking-solutions](https://github.com/redis-developer/mobile-banking-solutions)

## What you'll learn

- How to cache account balances and transaction data as Redis JSON documents
- How to track balance over time using Redis Time Series
- How to rank biggest spenders with Redis sorted sets
- How to search and filter transactions using Redis Search and Query
- How to seed realistic banking data with a cron-based transaction generator

## What is a mobile banking account dashboard?

An account dashboard is a page in a mobile banking app that instantly renders account highlights to users. A customer can click on any of the accounts on the dashboard to see the real-time account details, such as latest transactions, mortgage amount they have left to pay, checking and savings, etc.

An account dashboard makes a customer's finances easily visible in one place. It reduces financial complexity for the customer and fosters customer loyalty.

The following diagram is an example data architecture for an account dashboard:

![Data architecture diagram showing how banks prefetch customer data from separate product databases into Redis Cloud via Redis Data Integration, enabling sub-millisecond account dashboard rendering](/images/site-mirror/4712b3132252c09d00f9e40ad8ddc7a01a36bb2c-1432x950.webp)

1.  Banks store information in a number of separate databases that support individual banking products
2.  Key customer account details (balances, recent transactions) across the banks product portfolio are prefetched into Redis Cloud using Redis Data Integration (RDI)
3.  Redis Cloud powers customer's account dashboards, enabling mobile banking users to view balances and other high-priority information immediately upon login

## Why should you use Redis for account dashboards in mobile banking?

- **Resilience**: Redis Cloud provides resilience with 99.999% uptime and Active-Active Geo Distribution to prevent loss of critical user profile data
- **Scalability**: Redis Cloud provides < 1ms performance at incredibly high scale to ensure apps perform under peak loads
- **JSON Support**: Provides the ability to create and store account information as JSON documents with the < 1ms speed of Redis
- **Querying and Indexing**: Redis Cloud can quickly identify and store data from multiple different databases and index data to make it readily searchable

## How do you build an account dashboard with Redis?

> **NOTE**
>
> Below is a command to the clone the source code for the application used in this tutorial
>
> git clone --branch v1.2.0 [https://github.com/redis-developer/mobile-banking-solutions](https://github.com/redis-developer/mobile-banking-solutions)

Download the above source code and run following command to start the demo application

```bash
docker compose up -d
```

After docker up & running, open [http://localhost:8080/](http://localhost:8080/) url in browser to view application

### How is the banking data seeded?

This application leverages **Redis core data structures, JSON, TimeSeries, Search and Query features**. The data seeded is later used to show a searchable transaction overview with realtime updates as well as a personal finance management overview with realtime balance and biggest spenders updates.

On application startup in `app/server.js`, a cron is scheduled to create random bank transactions at regular intervals and seed those transactions in to Redis.

```js
// app/server.js
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
// app/transactions/create-bank-transaction.js
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

![Redis Insight browser showing a seeded bank transaction stored as a JSON document with fields like fromAccountName, amount, and transactionDate](/images/site-mirror/9935751e0e2b00f31b3931cb14b0883bcecabe2d-900x355.webp)

![Expanded JSON view of a single bank transaction record in Redis Insight, showing nested fields and balance-after value](/images/site-mirror/acad0d24e2816152471d202e60e9e3a06637cb2e-1336x858.webp)

> **TIP**
>
> Download [**Redis Insight**](https://redis.io/insight/) to view your Redis data or to play with raw Redis commands in the workbench.

### How do you track balance over time with Redis Time Series?

Dashboard widget:
![Line chart widget showing account balance trends over time, powered by Redis Time Series data](/images/site-mirror/c0e50678004508acd393059669aedf48ac1da809-908x482.webp)

|               |                                   |
| ------------- | --------------------------------- |
| Endpoint      | /transaction/balance              |
| Code location | /routers/transaction-router.js    |
| Parameters    | none                              |
| Return value  | `[{x: timestamp, y: value}, ...]` |

The balance endpoint leverages [**Time Series**](https://redis.io/docs/latest/develop/data-types/timeseries/), It returns the range of all values from the time series object `balance_ts`. The resulting range is converted to an array of objects with each object containing an `x` property containing the timestamp and a `y` property containing the associated value. This endpoint supplies the time series chart with coordinates to plot a visualization of the balance over time.

```js
// app/routers/transaction-router.js
const BALANCE_TS = 'balance_ts';

/* fetch transactions up to sometime ago */
transactionRouter.get('/balance', async (req, res) => {
    //time series range
    const balance = await redis.ts.range(
        BALANCE_TS,
        Date.now() - 1000 * 60 * 5, //from
        Date.now(), //to
    );

    let balancePayload = balance.map((entry) => {
        return {
            x: entry.timestamp,
            y: entry.value,
        };
    });

    res.send(balancePayload);
});
```

### How do you identify the biggest spenders with Redis sorted sets?

Dashboard widget:

![Pie chart widget displaying the top five biggest spenders, ranked using a Redis sorted set](/images/site-mirror/b52b399488e0be8df2b227598f95e4157ac1735e-868x480.webp)

|               |                                |
| ------------- | ------------------------------ |
| Endpoint      | /transaction//biggestspenders  |
| Code Location | /routers/transaction-router.js |
| Parameters    | none                           |
| Return value  | `{labels:[...], series:[...]}` |

The biggest spenders endpoint leverages [**sorted sets**](https://redis.io/docs/latest/develop/data-types/sorted-sets/) as a secondary index, It retrieves all members of the sorted set `bigspenders` that have scores greater than zero. The top five or fewer are returned to provide the UI pie chart with data. The labels array contains the names of the biggest spenders and the series array contains the numeric values associated with each member name.

```js
// app/routers/transaction-router.js
const SORTED_SET_KEY = 'bigspenders';

/* fetch top 5 biggest spenders */
transactionRouter.get('/biggestspenders', async (req, res) => {
    const range = await redis.zRangeByScoreWithScores(
        SORTED_SET_KEY,
        0,
        Infinity,
    );
    let series = [];
    let labels = [];

    range.slice(0, 5).forEach((spender) => {
        series.push(parseFloat(spender.score.toFixed(2)));
        labels.push(spender.value);
    });

    res.send({ series, labels });
});
```

### How do you search existing transactions with Redis?

Dashboard widget:

![Full-text search widget for filtering bank transactions by description, account name, or type using Redis Search and Query](/images/site-mirror/25fa4ac1ae744c81d1093c8179c88ea7628bc0b4-1942x1100.webp)

|                  |                                |
| ---------------- | ------------------------------ |
| Endpoint         | /transaction/search            |
| Code Location    | /routers/transaction-router.js |
| Query Parameters | term                           |
| Return value     | array of results matching term |

The search endpoint leverages [**Search and Query**](https://redis.io/docs/latest/develop/ai/search-and-query/), It receives a `term` query parameter from the UI. A [Redis om Node](https://github.com/redis/redis-om-node) query for the fields `description`, `fromAccountName`, and `accountType` will trigger and return results.

```js
// app/routers/transaction-router.js
transactionRouter.get('/search', async (req, res) => {
    const term = req.query.term;

    let results;

    if (term.length >= 3) {
        results = await bankRepo
            .search()
            .where('description')
            .matches(term)
            .or('fromAccountName')
            .matches(term)
            .or('transactionType')
            .equals(term)
            .return.all({ pageSize: 1000 });
    }
    res.send(results);
});
```

### How do you fetch recent transactions?

Dashboard widget:

![Dashboard table showing the ten most recent bank transactions, sorted by date using Redis Search and Query](/images/site-mirror/af021fe7c6d964103f98476f46d1be424ea43a57-1948x1184.webp)

|               |                                |
| ------------- | ------------------------------ |
| Endpoint      | /transaction/transactions      |
| Code Location | /routers/transaction-router.js |
| Parameters    | none                           |
| Return value  | array of results               |

Even the transactions endpoint leverages [**Search and Query**](https://redis.io/docs/latest/develop/ai/search-and-query/). A [Redis om Node](https://github.com/redis/redis-om-node) query will trigger and return ten most recent transactions.

```js
// app/routers/transaction-router.js
/* return ten most recent transactions */
transactionRouter.get('/transactions', async (req, res) => {
    const transactions = await bankRepo
        .search()
        .sortBy('transactionDate', 'DESC')
        .return.all({ pageSize: 10 });

    res.send(transactions.slice(0, 10));
});
```

## What are the next steps?

Now that you've built a mobile banking account dashboard with Redis, consider exploring these related tutorials and resources:

- **[Mobile Banking Session Management](/tutorials/howtos/solutions/mobile-banking/session-management)**: Learn how to manage user sessions in your mobile banking app with Redis for secure, low-latency authentication
- **[Fraud Detection with Transaction Risk Scoring](/tutorials/howtos/solutions/fraud-detection/transaction-risk-scoring/)**: Add real-time fraud scoring to your banking transactions using Redis
- **[Redis YouTube channel](https://www.youtube.com/c/Redisinc)**: Video walkthroughs and deep dives on Redis features
- Clients like [Node Redis](https://github.com/redis/node-redis) and [Redis OM Node](https://github.com/redis/redis-om-node) help you to use Redis in Node.js apps
- **[Redis Insight](https://redis.io/insight/)**: Visualize your Redis data and experiment with commands in the workbench
- **[Try Redis Cloud for free](https://redis.io/try-free/)**: Get started with a free Redis Cloud instance
