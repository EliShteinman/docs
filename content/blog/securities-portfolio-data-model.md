---
title: "Exploring a Securities Portfolio Data Model Using Native JSON and Query Capabilities in Redis"
linkTitle: "Exploring a Securities Portfolio Data Model Using Native JSON and Query Capabilities in Redis"
url: "/blog/securities-portfolio-data-model/"
description: "This tutorial, which shows how to optimize a brokerage application, demonstrates what you can accomplish using Redis with its JSON data structure and enhanced query capabilities."
date: 2023-03-01
blogCategories:
- "How To and Tutorials"
- "Tech"
authors:
- "Prasanna Rajagopal"
- "Abhishek Srivastava"
lastmod: 2026-05-21
hidden: true
---

*By Prasanna Rajagopal, Abhishek Srivastava · Published 1 March 2023 · updated 21 May 2026*

![Blog tile image](/images/blog/31ab3a1ec07bc65b90d663de9a9599d05570f03a-772x550.webp)

**This tutorial, which shows how to optimize a brokerage application, demonstrates what you can accomplish using Redis with its JSON data structure and enhanced query capabilities.**

In the financial sphere, a brokerage’s success is tied to its investors’ engagement with the trading application it provides. Brokers are motivated to create better investor engagement because it leads to more assets under management, more trades, and (the brokerage’s favorite part, surely) more fees and commissions.

These mobile apps also serve as a useful way to demonstrate system design in general and technologies that Redis Enterprise provides in particular. The broker’s applications are all about timing, and that is the essence of Redis as a real-time data platform, allied with the documents store (JSON) and fast query capabilities. So let’s examine this as a case study for mobile developers who serve a financial services audience.

Some brokerage apps are designed to handle a certain number of client logins at any time. These apps [face scalability and performance challenges](https://www.investopedia.com/online-brokers-suffer-service-failures-as-markets-surge-on-election-and-vaccine-news-5086672) when trading activity surges. These technology failures and poor client experiences are bad for a brokerage’s revenue, profitability, and reputation.

Any brokerage application has a long list of technology must-haves, including high availability, low latency with fast response time, strong consistency, scalability, security, and consistent performance. Guaranteeing all these attributes is a challenge. Software developers often use a mix of technologies and databases, doing their best to balance all those parameters along with issues of interoperability and company budgets. Their application landscape comprises SQL databases, NoSQL databases, and caching to create a veneer of real-time performance and scalability.

The brokerage app we describe needs an in-memory database that can ensure high availability, seamless scalability, and diverse data modeling capabilities. Redis Enterprise is an in-memory database that supports JSON, graph, and time series data structures. Querying using the unique Redis index and search capabilities can meet these requirements for a brokerage application. Redis Enterprise offers plenty of features to support high availability and scalability, such as [Active-Active Geo-Distribution](/active-active/), which can meet the most demanding needs for a brokerage app.

Herein, we present a sample implementation of a brokerage application using JSON Data structure and Redis indexing to store and retrieve securities portfolios.

You can [follow along with the sample code](https://github.com/Redislabs-Solution-Architects/sample_trading_data_model) if you like.

## How the brokerage app’s data model

We modeled various brokerage entities (Exhibit 1) using JSON. Each investor’s personal details are modeled as a JSON document titled investor. This document stores information such as the investor’s legal name, address, date of birth, social security number (U.S.) or Aadhar (India) card number, and the taxpayer id (TIN in the U.S. and PAN in India).

(Although each investor can have multiple accounts within a brokerage, for this sample implementation, we model each investor owning a single account.)

**Exhibit 1: Securities Portfolio Data Model**

![sample implementation diagram](/images/blog/f9ccb96f0af76bb47666342c13333845660cee6d-318x349.webp)

Each JSON document has a corresponding key, the format of which would be:

```
trading:investor:<investorId>

```

A sample investor JSON document looks something like this:

```
{
      "id": "INV10001",
      "name": "John M.",
      "dob":"01-01-1980",
      "Address":"100 North Street"
      "uid": "35178235834",
      "pan": "AHUIOHO684"
}

```

The application can extend the data model to accommodate an investor’s ownership of multiple accounts.

Each account is modeled as [a JSON document](/blog/what-are-json-databases/) in Redis. The account document can also capture important data, such as the approved level of options trading and whether the account is permitted to trade on margin.

The key format for the Account JSON document looks like this:

```
trading:account:<accountNo>

```

The corresponding account JSON document is:

```
{
  "id": "ACC10001",
  "investorId": "INV10001",
  "accountNo": "ACC10001",
  "accountOpenDate": "01-01-2018",
  "accountCloseDate": "NA",
  "retailInvestor": true
}

```

Each account can have dozens of assets in its portfolio. These assets could be stocks, bonds, mutual funds, exchange-traded funds (ETFs), and options.

Each asset has unique data elements that are reflected in the JSON document. For example, an entry for a stock owned by an investor in an account would include the price paid, the purchase date, and the quantity. In contrast, a call option bought by an account needs the strike price, expiry date, and transaction type (sold or bought the option) along with the purchase date, the price paid, and the number of options purchased (quantity).

A typical investor purchases stocks in lots at a given date and time. Therefore a lot is unique to the account, security, and time of purchase. Investor accounts may also get new security lots assigned when dividends are paid as stock. For example, investors may register their brokerage account or individual security in the dividend reinvestment plan (DRIP). The brokerage creates new security lots for each stock that’s enrolled in a DRIP when the company pays dividends. That’s just a sample. There are many scenarios under which a brokerage can create new security lots, such as company spin-offs, mergers and acquisitions, and automatic investment plans.

The key format for each such security lot is as follows:

```
trading:securitylot:<accountNo>:<securityLotId>

```

A sample security lot JSON document looks like this:

```
{
  "id": "SC61239693",
  "accountNo": "ACC10001",
  "ticker": "RDB", 
  "purchasedate": 1665082800,
  "price": 14500.00,
  "quantity": 10, 
  "type": "EQUITY"     	
}

```

In Redis, the purchase date of the security in the lot is stored in Unix date/time format.

Finally, we store the details of each traded security in JSON, the key for which looks something like this:

```
trading:stock:<stockId>

```

The corresponding stock could have the following JSON elements:

```
{
      "id": "NSE623846333",
      "companyname": "RDBBANK",
      "isin": "INE211111034",
      "stockName": "RDB",
      "description": "Something about RDB bank",
      "dateOfListing": "08-11-1995",
      "active": true
}

```

This data model lays the foundation for a brokerage to handle millions of customer accounts.

## Set up Redis to work with the Python or Java API

Everything is set up. Let’s write some queries on Redis to implement a few scenarios of retrieving JSON objects and full-text capabilities.

To do so, we need to add data in Redis using the programming language of our choice. The JSON as data structure in Redis is supported by official Redis clients. For instance, for Python, we have [redis-py](https://github.com/redis/redis-py); in Java, we have [Jedis](https://github.com/redis/jedis). For accessing enterprise modules in Spring, we can use the [Redis OM Spring](https://redis.io/docs/stack/get-started/tutorials/stack-spring/) library.

Here’s the code snippet to create a document using the Python Redis API:

```python
# Python
import redis
connection = redis.Redis(host="127.0.0.1", port=6379)
account = {
  "id": "ACC10001", "investorId": "INV10001",
  "accountNo": "ACC10001", "accountOpenDate": "01-01-2018",
  "accountCloseDate": "NA", "retailInvestor": True
}
connection.json().set("trading:account:ACC10001", "$", account)

```

The corresponding code using Java and Jedis library is as follows:

```java
/* Java */
class Account {
    private String id;
    private String investorId;
    private String accountNo;
    private LocalDate accountOpenDate;
    private LocalDate accountCloseDate;
    private boolean retailInvestor;

    public Account(String id, String investorId, String accountNo, LocalDate openDate, LocalDate closeDate, boolean retailInvestor) {
        this.id = id;
        this.investorId = investorId;
        this.accountNo = accountNo;
        this.accountOpenDate = openDate;
        this.accountCloseDate = closeDate;
        this.retailInvestor = retailInvestor;
    }

    //...
}
//...
UnifiedJedis client = new UnifiedJedis(new HostAndPort("localhost", 6379));
Account firstAccount = new Account(
        "ACC10001", "INV10001", "ACC10001",
        LocalDate.of(2018, 1 , 1), null, true);

client.jsonSetWithEscape("trading:account:ACC10001", firstAccount);

```

## Query securities portfolios using indexing and search capabilities

Imagine that a retail investor wants to view a particular security or a subset of securities they hold. It’s a typical scenario. During peak trading hours, The underlying data platform has to handle these queries for millions of accounts concurrently.

Every query should return the result in real-time so the underlying application provides a consistent performance and user experience. This can be achieved using a Redis capability that enables querying, secondary indexing, and full-text search for Redis. For that, we need to create suitable secondary indexes on the JSON documents first.

In Redis, the Index has a unique capability to follow the data writing path, so as soon as you create the Index using [FT.CREATE](https://redis.io/commands/ft.create/) and define how the JSON document should be mapped using the SCHEMA, the secondary index is populated. New data coming, the index is updated, and you can query straight away the new documents.

Here’s the RediSearch index for the account documents:

```
FT.CREATE idx_trading_account 
   ON JSON 
      PREFIX 1 "trading:account:"
   SCHEMA 
      $.accountNo AS accountNo TEXT NOSTEM
      $.retailInvestor as retailInvestor TAG      
      $.accountOpenDate as accountOpenDate TEXT

```

And here’s the index for the security_lot documents:

```
FT.CREATE idx_trading_security_lot 
   ON JSON 
      PREFIX 1 "trading:securitylot:" 
   SCHEMA 
      $.accountNo AS accountNo TEXT 
      $.ticker AS ticker TAG 
      $.price AS price NUMERIC SORTABLE 
      $.quantity AS quantity NUMERIC SORTABLE
      $.purchaseDate AS purchaseDate NUMERIC SORTABLE

```

We created indexes on the documents of security lots(idx_trading_security_lot) and accounts (idx_trading_account). These indexes can be queried in different ways to serve an investor’s real-time, milliseconds needs.

Let’s build the queries for a few scenarios:

Let’s build the queries for a few scenarios:

- Get all the security lots by account number/id
- Get all the security lots by account number/id and ticker
- Get the total quantity of all securities inside investor’s security portfolio
- Get the total quantity of all securities inside an investor’s security portfolio at a particular time
- Get the average cost price of the owned security at a given date and time. The average cost price of the security, when combined with the current price, can provide the gain or loss information on a security.

### Security lots owned by an account

Retrieving all the security lots owned by an account may be the simplest query to display a portfolio. The query looks like this:

```
FT.SEARCH idx_trading_security_lot '@accountNo:(ACC10001)'

```

Its output appears thusly:

```
127.0.0.1:6379> FT.SEARCH idx_trading_security_lot '@accountNo:(ACC10001)'
 1) (integer) 172
 2) "trading:securitylot:ACC10001:TEGO12981200447"
 3) 1) "$"
    2) "{\"id\":\"TEGO12981200447\",\"accountNo\":\"ACC10001\",\"ticker\":\"RDBMOTORS\",\"date\":1648578600,\"price\":43845.0,\"quantity\":66,\"type\":\"EQUITY\"}"
 4) "trading:securitylot:ACC10001:UHZW18076572669"
 5) 1) "$"
    2) "{\"id\":\"UHZW18076572669\",\"accountNo\":\"ACC10001\",\"ticker\":\"RDBFOODS\",\"date\":1642012200,\"price\":1975000.0,\"quantity\":55,\"type\":\"EQUITY\"}"
 6) "trading:securitylot:ACC10001:QHSL13846265328"
 7) 1) "$"
    2) "{\"id\":\"QHSL13846265328\",\"accountNo\":\"ACC10001\",\"ticker\":\"RDBMOTORS\",\"date\":1647369000,\"price\":42705.0,\"quantity\":23,\"type\":\"EQUITY\"}"
  .
  .

```

### Retrieve all lots of a specific security in an account

It is easy for the investor to filter the view of their portfolio and view their position in a certain security.

```
FT.SEARCH idx_trading_security_lot '@accountNo:(ACC10001) @ticker:{RDBMOTORS}'

```

The output for the above command looks like this:

```
127.0.0.1:6379> FT.SEARCH idx_trading_security_lot '@accountNo: (ACC10001) @ticker:{RDBMOTORS}'
 1) (integer) 90
 2) "trading:securitylot:ACC10001:TEGO12981200447"
 3) 1) "$"
    2) "{\"id\":\"TEGO12981200447\",\"accountNo\":\"ACC10001\",\"ticker\":\"RDBMOTORS\",\"date\":1648578600,\"price\":43845.0,\"quantity\":66,\"type\":\"EQUITY\"}"
 4) "trading:securitylot:ACC10001:QHSL13846265328"
 5) 1) "$"
    2) "{\"id\":\"QHSL13846265328\",\"accountNo\":\"ACC10001\",\"ticker\":\"RDBMOTORS\",\"date\":1647369000,\"price\":42705.0,\"quantity\":23,\"type\":\"EQUITY\"}"
 6) "trading:securitylot:ACC10001:TIMW18620419852"
 7) 1) "$"
    2) "{\"id\":\"TIMW18620419852\",\"accountNo\":\"ACC10001\",\"ticker\":\"RDBMOTORS\",\"date\":1641321000,\"price\":48695.0,\"quantity\":30,\"type\":\"EQUITY\"}"
  .
  .

```

### Total quantity of each security in an account

For now, it’s focused on retrieving specific keys that match a query predicate and need. The Redis query capabilities don’t stop there. You can use [FT.AGGREGATE](https://redis.io/commands/ft.aggregate/) to group, sort, filter, and make arithmetic operations SUM. The application could get the total quantity of securities or the price paid using an aggregation query similar to the following:

```
FT.AGGREGATE idx_trading_security_lot '@accountNo: (ACC10001)' GROUPBY 1 @ticker REDUCE SUM 1 @quantity as totalQuantity

```

And its output looks like:

```
127.0.0.1:6379> FT.AGGREGATE idx_trading_security_lot '@accountNo: (ACC10001)' GROUPBY 1 @ticker REDUCE SUM 1 @quantity as totalQuantity
1) (integer) 2
2) 1) "ticker"
   2) "RDBMOTORS"
   3) "totalQuantity"
   4) "4502"
3) 1) "ticker"
   2) "RDBFOODS"
   3) "totalQuantity"
   4) "4581"

```

### Securities owned by an account at a particular date and time

A query like this may help an investor know the total quantity of securities owned at certain points in time, such as the end of the month or year.

```
FT.AGGREGATE idx_trading_security_lot '@accountNo: (ACC10001) @date:[0 1665082800]' GROUPBY 1 @ticker REDUCE SUM 1 @quantity as totalQuantity

```

Expect output that looks like this:

```
127.0.0.1:6379> FT.AGGREGATE idx_trading_security_lot '@accountNo: (ACC10001) @date:[0 1665082800]' GROUPBY 1 @ticker REDUCE SUM 1 @quantity as totalQuantity
1) (integer) 2
2) 1) "ticker"
   2) "RDBMOTORS"
   3) "totalQuantity"
   4) "4502"
3) 1) "ticker"
   2) "RDBFOODS"
   3) "totalQuantity"
   4) "4581"

```

### Average buying price of each security owned by an account at a given moment

To find the average cost price of each stock owned by an account at a particular date and time, we first calculate the lot value of all the securities held in an account. Then we aggregate the total quantities of these securities. Finally, we calculate the average cost price of these securities.

```
FT.AGGREGATE idx_trading_security_lot '@accountNo:(ACC10001) @date:[0 1665498506]' apply '(@price * @quantity)' as lotValue groupby 1 @ticker reduce sum 1 @lotValue as totalLotValue reduce sum 1 @quantity as totalQuantity apply '(@totalLotValue/(@totalQuantity*100))' as avgPrice

```

The output for the above command is as follows:

```
127.0.0.1:6379> FT.AGGREGATE idx_trading_security_lot '@accountNo:(ACC10001) @date:[0 1665498506]' apply '(@price * @quantity)' as lotValue groupby 1 @ticker reduce sum 1 @lotValue as totalLotValue reduce sum 1 @quantity as totalQuantity apply '(@totalLotValue/(@totalQuantity*100))' as avgPrice
1) (integer) 2
2) 1) "ticker"
   2) "RDBMOTORS"
   3) "totalLotValue"
   4) "205251865"
   5) "totalQuantity"
   6) "4502"
   7) "avgPrice"
   8) "455.912627721"
3) 1) "ticker"
   2) "RDBFOODS"
   3) "totalLotValue"
   4) "8496437015"
   5) "totalQuantity"
   6) "4581"
   7) "avgPrice"
   8) "18547.1229317"

```

## Show me the money

We hope this example piques your interest in these Redis Enterprise capabilities and encourages you to learn a little more about them.

[Redis](/json/) document store capability provides full support for JSON, a JSONPath syntax for manipulating the JSON elements, fast access to data, and atomic operations for JSON values. Multiple [benchmark tests](https://redis.io/docs/stack/json/performance/) suggest that RedisJSON performs better than its competitors on metrics such as latency and read-write throughput.

[The Query and Search on Redis ](/search/)allow you to quickly create indexes on HASH and JSON documents and use real-time indexing to query documents instantly. The indexes let you query the data at lightning speed, perform complex aggregations, and filter by properties, numeric ranges, and geographical distance.

## That’s just the beginning

Want to learn more? You can choose one of the following ways to install and get started with Redis Stack:

- Follow these [instructions](https://redis.io/docs/stack/get-started/install/) to install [Redis Stack](https://redis.io/download/) with RedisInsight GUI using Homebrew or Docker
- Download it from the [RedisInsight download page](/insight/#insight-form) for Windows, Mac, and Linux
- Create [a free database on Redis Enterprise Cloud](/try-free/), which contains all the latest features of Redis Stack
- Choose the client library in [the language of your choice](https://redis.io/docs/stack/get-started/clients/), and consult our [tutorials](https://redis.io/docs/stack/get-started/tutorials/)
