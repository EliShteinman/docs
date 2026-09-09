---
title: "Building a Real-Time Trading Platform with Redis"
linkTitle: "Building a Real-Time Trading Platform with Redis"
url: "/blog/real-time-trading-platform-with-redis-enterprise/"
description: "Portfolios form the foundation of the wealth and asset management industry. Ever since Harry Makowitz pioneered modern portfolio theory, asset and wealth management professionals have obsessed over..."
date: 2021-06-10
blogCategories:
- "Tech"
authors:
- "Prasanna Rajagopal"
lastmod: 2025-03-27
hidden: true
---

*By Prasanna Rajagopal · Published 10 June 2021 · updated 27 March 2025*

![Blog tile image](/images/site-mirror/d9f40511c3f5f0daed4185b7053b85916f8b9b64-772x520.webp)

Portfolios form the foundation of the wealth and asset management industry. Ever since Harry Makowitz pioneered [modern portfolio theory](https://www.investopedia.com/terms/m/modernportfoliotheory.asp), asset and wealth management professionals have obsessed over maximizing the returns on their portfolio for a given level of risk. Today, the professionals in the industry are joined by millions of retail investors, whom have forever changed the landscape of investing. These new entrants are creating huge ramifications for the technology underpinning the trading infrastructure of retail brokerages, exchanges, and clearing houses.

Take, for instance, the GameStop stock mania of January 2021. Retail investors started trading GameStop stock at record levels. These investors also piled into other meme stocks like AMC Entertainment, causing the overall market volatility to rise more than 76% in a matter of a few trading days as measured by the VIX. This volatility led to price pressure on thousands of securities. Millions of investors were frantically trying to access their portfolios at the same time, but were faced with apps that [couldn’t keep up with demand](https://www.wsj.com/articles/outages-continue-to-plague-online-brokerages-11611768827). Investors are not kind to companies whose apps do not perform well when they need it the most.

![](/images/site-mirror/b12590924433dcbd8791ae40786bd3413ecbada8-1024x571.webp)

*Exhibit: The rise in market volatility caused by retail investors during GameStop mania, January 2021*

During these frantic times, most investors are looking for two data points about their portfolio that they need access to at all times:

1. ***What is the total value of the portfolio at that time?***
1. ***What are the gains or losses of specific securities in their portfolio?***

The answers to these questions can lead an investor to buy, sell, or hold specific securities. In today’s fast-moving markets, any delays could mean lost opportunity and profits. You need real-time access to prices to answer these questions—yet there are two big challenges:

- Updating prices of thousands of securities simultaneously
- Answering millions of customer requests at once.

The prices of securities can quickly change based on the trading volume, volatility of a specific security, and the volatility in the market. On the other hand, a brokerage could have millions of customers, each of them with a couple dozen securities in their portfolio. As soon as the customer logs in, their portfolio needs to be updated with the latest prices—and keep them updated as the brokerage receives prices from the exchanges.

Essentially, we are creating a real-time stock chart. Many brokerage apps don’t try to do this at scale. Instead, these apps pull the latest prices rather than push the prices to millions of clients. For example, there might be a refresh button on their portfolio page.

These next-generation challenges are not trivial and cannot be easily solved with disk-based databases, which weren’t designed to handle millions of operations per second. The requirements of the financial industry need a database that can scale easily and handle hundreds of millions of operations each second. In comes [Redis Enterprise](/try-free/), an in-memory database platform, has the potential to tackle these myriad challenges.

[Watch the video](https://www.pexels.com/@anna-nekrashevich?utm_content=attributionCopyText&utm_medium=referral&utm_source=pexelshttps://www.pexels.com/@anna-nekrashevich?utm_content=attributionCopyText&utm_medium=referral&utm_source=pexels)

This is the first of a series of blogs covering various real-time use cases in the financial world. We will cover the details and business challenges of each use case and the role Redis Enterprise can play in solving those challenges. As part of the blog, we offer sample designs, data models, and code samples. We will also discuss the pros and cons of each approach.

In this blog post we will cover the following:

- A sample implementation of a high-performance and scalable securities portfolio data model on Redis Enterprise.
- Update prices of securities in the portfolio in real-time as the brokerage receives the latest prices from the exchanges.

Once the client app has retrieved the portfolio and is receiving the latest prices, it can:

- Calculate the total portfolio value of the portfolio.
- Calculate the gain or loss on each portfolio holding.

## Securities Portfolio Data Model

Let’s begin by modeling a holding in a portfolio. In the illustration below, CVS Health Corp. (NYSE: [CVS](https://seekingalpha.com/symbol/CVS)) is one of our example holdings. There were two separate lots of CVS—the first was acquired on January 4, 2021 and the second on March 1, 2021. The same number of shares were purchased during the **buy** trade for each lot. Both trades were for 10 shares, however at different **prices per share**—$68.3378 for the first lot and $68.82 for the second. The total quantity of the CVS holding in the portfolio is 20 with an average cost calculated as follows: (($68.3378 * 10) + ($68.82 * 10))/20 = $68.5789 per share.

![](/images/site-mirror/66669188c8cbcac451b17a9dfca41f44c4b6f341-1024x400.webp)

*Exhibit: Description of a holding in a securities portfolio (Source: E*Trade, Author annotations)*

## Implementing the requirements

![](/images/site-mirror/fb962cf131d547858b9a611ba9aa38c5e49479b3-303x449.webp)

Redis’ data representation is flat—one cannot embed Sets, for example, within another Set. Therefore the data model as described by an ER diagram cannot necessarily be implemented directly. Implementing the Entity Model directly might not have the desired performance characteristics, so you’ll have to think a little differently as you get down to implementation. In this section we cover some of the basic design principles required when designing a high-performance and scaling implementation using Redis.

The data model here mentions the following entities:

![](/images/site-mirror/9fb22c2ac0bb93b5b265cf566acf8fe33bc4cf8a-785x431.webp)

An ER diagram provides a visual representation which can help one see what’s going on.

What’s missing from the diagram above is the set of incoming prices although they are recorded in the security’s price history—and the calculation of the **instantaneous value and gains** as prices change. So, the ER diagram represents the comparatively static data that is the context in which portfolio valuation is performed.

## Overall architecture

Key points that need to be considered about this system include:

- Timeliness (i.e. latency) is critical. This is the overall driving property.
- The calculation of portfolio value combines account-specific data (i.e. the lot information) with data shared between accounts (i.e. security prices). The account-specific data is thus a context in which shared data is used.
- Portfolio value only needs to be calculated for those accounts where the investor is online (a fraction of the total number of accounts).
- Data flows through the system, from the exchanges where prices are produced out to the client machines (browers, mobile phone applications) presenting the portfolio values to the online investors.
- Particular areas with a high degree of dynamism include rate of input data flow and number of online investors.

Given these points, some general approaches are:

- Relying on Redis’ in-memory architecture for low latency access to both static and dynamic data.
- Optimizing data modeling by using Redis’ data structures to provide rapid access to the slowly changing contextual data.
- Using Redis’ communication structures (Streams, Consumer Groups, Pub/Sub) to handle dynamic data requirements.
- Reducing data storage to only what is necessary without impacting overall system performance.
- Implementing client-specific calculations on the clients themselves. This scales naturally and automatically with the number of online investors, greatly relieving the scale burden.

Here are the major computational components and the data flow:

![](/images/site-mirror/d658ed53110f3f4ed1eaf44bfe788d01613ad187-624x211.webp)

Note that Redis Enterprise consists of one or more nodes across many machines—deployed on-premises, Kubernetes, hybrid cloud deployment, managed service, or native first party cloud service—and there will be hundreds of thousands of investors online with their client(s) of choice.

## Redis Enterprise components

Security price updates will be absorbed by Redis Streams. Updates for securities will be mixed together in this stream and will need to be disaggregated to make the data useful. A consumer group will be used to perform that disaggregation, and to process data into two structures, per security:

- RedisTimeSeries database, to keep track of the history of price changes (as well as record the very latest price for any client just connecting)
- Pub/Sub broker channel to push price change notifications to clients that have subscribed to that channel (i.e. investors whose portfolio includes that security)

The following diagram details this part of the architecture:

![](/images/site-mirror/96635daeb8be0e6bbc7d6b4b3dc1a1c2d970ac23-623x473.webp)

The most important factor in our model is the account-specific data representing lots and the related security. We’ll compare two implementations as an example of how to think about modeling data in Redis, with a focus on performance. Other implementations are possible—our goal here is to introduce the overall design principles and thought processes when implementing data in Redis.

We’ll use the following information as a concrete example:

![](/images/site-mirror/5cb736ac7d84dc78effc993e61c0064daecf43a5-785x162.webp)

We are pricing in the lowest possible currency denomination to avoid floats and keep everything in integers. We can allow the client to handle transformation to dollars and cents. In this example, we are using the prices with precision of two decimal places.

## Data Model A

Our first implementation records the id’s of all the lots in the account using a SET, identified by account id, and then uses one Redis HASH per LOT, identified by LOT ID, with the ticker, quantity, and purchase price as the fields. In other words, we’re using the HASH to model the LOT entity structure, with each *attribute* of the LOT entity being a **field** in the Redis HASH.

With this data model we have a key for each account and a value containing all the LOT IDs for that account stored as a Redis SET:

lotids:<ACCOUNT_ID> SET <LOTID>

In addition, for each lotid, we’d have a HASH whose fields are the ticker, quantity, and purchase price:

lot:<LOTID> HASH <ticker TICKER> <quantity INTEGER> <price INTEGER>

Concretely, we’d create the keys like this:

```javascript
127.0.0.1:6379> SADD lotids:ACC-1001 LOT-9001 LOT-9002
(integer) 2
127.0.0.1:6379> HMSET lot:LOT-9001 ticker AAPL quantity 200 price 12556
OK
127.0.0.1:6379> HMSET lot:LOT-9002 ticker CAT quantity 1200 price 18063
OK
```

The [RedisTimeSeries](https://oss.redis.com/redistimeseries/) module allows the storage and retrieval of related pairs of times and values, along with high-volume inserts and low-latency reads. We are going to get the latest price for the tickers of interest the client would access when using the corresponding time series keys:

price_history:<TICKER> TIMESERIES <price INTEGER>

```javascript
127.0.0.1:6379> TS.GET price_history:APPL
1) (integer) 1619456853061
2) 12572
127.0.0.1:6379> TS.GET price_history:CAT
1) (integer) 1619456854120
2) 18021
```

and subscribe to the pricing channel for updates:

<TICKER> SUBSCRIPTION_CHANNEL

To get all the data, the client would perform the following operations:

1. 1 times [SMEMBERS](https://www.google.com/url?q=https://redis.io/commands/smembers&sa=D&source=editors&ust=1623273994270000&usg=AOvVaw01H9PH1M2QwJMNbVOafWE9) on the **lotids** key—time complexity O(N) with N being the number of lots
1. N times [HGETALL](https://www.google.com/url?q=https://redis.io/commands/HGETALL&sa=D&source=editors&ust=1623273994271000&usg=AOvVaw31irjNvtTMahqaw296OKFc) on the **lot** keys—time complexity N times O(1)
1. T times [TS.GET](https://www.google.com/url?q=https://oss.redis.com/redistimeseries/commands/%23tsget&sa=D&source=editors&ust=1623273994272000&usg=AOvVaw0FvYCFlcmwL3JjDp5WI_nb) on the **price_history** keys – time complexity T times O(1) with T being the number of tickers
1. 1 times SUBSCRIBE on the **<TICKER>** channels – time complexity O(T) (one can subscribe to all the channels in a single call to SUBSCRIBE)

The overall time complexity is O(N +T).

Concretely, operations one and two would be:

```javascript
127.0.0.1:6379> SMEMBERS lotids:ACC1001
1) "LOT-9001"
2) "LOT-9002"
127.0.0.1:6379> HGETALL lot:LOT-9001
1) "ticker"
2) "AAPL"
3) "quantity"
4) "200"
5) "price"
6) "12556"
127.0.0.1:6379> HGETALL lot:LOT-9002
1) "ticker"
2) "CAT"
3) "quantity"
4) "1200"
5) "price"
6) "18063"

```

We can minimize network latency by using [pipelining](https://www.google.com/url?q=https://redis.io/topics/pipelining&sa=D&source=editors&ust=1623273994277000&usg=AOvVaw3Ez9XrC5sBCcPWzYTewH5T) (a form of batching on the client side) and/or repeated use of LUA scripts (using [SCRIPT LOAD](https://www.google.com/url?q=https://redis.io/commands/script-load&sa=D&source=editors&ust=1623273994277000&usg=AOvVaw2K2x41TEW8vhz2kNat64qn) & [EVALSHA](https://www.google.com/url?q=https://redis.io/commands/evalsha&sa=D&source=editors&ust=1623273994277000&usg=AOvVaw29pZotJ7UgYyI468BAokG-)). Side note[: Transactions](https://www.google.com/url?q=https://redis.io/topics/transactions&sa=D&source=editors&ust=1623273994278000&usg=AOvVaw2loziQsU9wIkTOzDFSx38_) can be implemented using pipelines and can provide reduced network latency, but this is client specific and their goal is atomicity on the server, so they don’t really solve the network latency problem. Pipelines comprise commands whose inputs and outputs must be independent of one another. LUA scripts require all keys to be provided in advance **and** that all of the keys are hashed to the same slot (see the Redis Enterprise docs [on this topic](https://www.google.com/url?q=https://docs.redis.com/latest/rs/concepts/high-availability/clustering/%23multikey-operations&sa=D&source=editors&ust=1623273994278000&usg=AOvVaw03sVLJAlc7J2WdG6jWUz8G) for more details).

Given these constraints we can see that the assignment of operations to pipelines is:

- pipeline 1:The single command of operation #1
- pipeline 2: All N commands of operation #2
- pipeline 3: All N commands of operations #3 and #4

and that using LUA scripts isn’t possible because each operation uses different keys and those keys have no common part that can be hashed to the same slot.

In utilizing this model we have a time complexity of O(N+T) and three network hops.

## Data Model B

An alternative model is to flatten the LOT entity structure and to represent each entity attribute using a key identified by account id—one such key for each attribute (quantity, ticker, price) of a lot. The fields in each HASH will be the LOT ID and a corresponding value to either quantity, ticker, or price. Thus we’d have keys:

tickers_by_lot: <ACCOUNT_ID> HASH <LOTID TICKER>

quantities_by_lot:<ACCOUNT_ID> HASH <LOTID INTEGER>

prices_by_lot:<ACCOUNT_ID> HASH <LOTID INTEGER>

These hashes would replace the LOTID and LOT keys from Data Model A, while the **price_history** and **<TICKER>** keys would remain the same.

Creating the keys:

```javascript
HSET tickers_by_lot:ACC-1001 LOT-9001 AAPL LOT-9002 CAT
HSET quantities_by_lot:ACC-1001 LOT-9001 200 LOT-9002 1200
HSET prices_by_lot:ACC-1001 LOT-9001 125.56 LOT-9002 180.63

```

Retrieving the values:

```javascript
127.0.0.1:6379> HGETALL tickers_by_lot:ACC-1001
1) "LOT-9001"
2) "AAPL"
3) "LOT-9002"
4) "CAT"
127.0.0.1:6379> HGETALL quantities_by_lot:ACC-1001
1) "LOT-9001"
2) "200"
3) "LOT-9002"
4) "1200"
127.0.0.1:6379> HGETALL prices_by_lot:ACC-1001
1) "LOT-9001"
2) "12556"
3) "LOT-9002"
4) "18063"

```

The operations required by the client would now be:

1. 1 times HGETALL on the **lot_quantity** keys—time complexity N x O(1)
1. 1 times HGETALL on the **lot_ticker** keys—time complexity N x O(1)
1. 1 times HGETALL on the **lot_price** keys—time complexity N x O(1)
1. T times TS.GET on the **price_history** keys—time complexity T x O(1) with T being the number of tickers
1. 1 times SUBSCRIBE on the **<TICKER>** channels—time complexity 1 x O(T)

This has an overall time complexity of O(N+T)—same as before.

From a pipeline perspective this becomes:

- Pipeline one—all commands of operations #1, #2, and #3
- Pipeline two—all T commands of operations #4 and #5

So we’ve reduced the number of network hops by one—not a lot in absolute terms, but 33% in relative terms.

In addition, we can easily use LUA since we know the keys, and we can map all the keys for any specific account to the same slot. Given the simplicity of operations we’ll not dig into LUA further, but note that this design makes it at least possible!

In a simple benchmark, Data Model B ran 4.13 ms faster (benchmarked over thousands of runs). Given that this is only run once each time a client is initialized for an account, this likely has no impact on overall performance.

## Summary

In this blog, we’ve shown two possible implementations of the Entity model using Redis data types. We’ve also introduced the time complexity analysis that should be performed whenever choosing a Redis data type, along with a consideration of network performance improvements—a critical step when large scale and high performance are required. In subsequent blogs, we’ll expand further on these ideas as the data model is expanded.

We have introduced some of the business challenges in managing securities portfolios at scale and have shown the following:

- A Redis data model for implementing a real-time and scalable securities portfolio.
- A high-performance, real-time price update system that can be used to calculate the total value of a portfolio and the gains or losses of each holding.

With these two critical features in place, a brokerage app client can provide real-time portfolio updates that perform and scale to handle millions of accounts. This design can present the total value of the portfolio and the gain or loss across each holding in real-time. This data model and architecture can also be applied to use cases beyond securities to cover crypto, ad exchanges, etc.
