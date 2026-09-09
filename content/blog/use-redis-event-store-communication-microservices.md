---
title: "How to Use Redis as an Event Store for Communication Between Microservices"
linkTitle: "How to Use Redis as an Event Store for Communication Between Microservices"
url: "/blog/use-redis-event-store-communication-microservices/"
description: "Click here to get started with Redis Enterprise. Redis Enterprise lets you work with any real-time data, at any scale, anywhere."
date: 2019-02-11
blogCategories:
- "How To and Tutorials"
authors:
- "Martin Forstner"
lastmod: 2025-03-27
hidden: true
---

*By Martin Forstner, Solution Architect · Published 11 February 2019 · updated 27 March 2025*

![Blog tile image](/images/site-mirror/0073e867b4e64f59de9047fdcde04295ba647e5c-772x550.webp)

[*Click here to get started with Redis Enterprise. Redis Enterprise lets you work with any real-time data, at any scale, anywhere.*](/try-free/)

In my experience, certain applications are easier to build and maintain when they are broken down into smaller, loosely coupled, self-contained pieces of logical business services that work together. Each of these services (a.k.a. microservices) manages its own technology stack that is easy to develop and deploy independently of other services. There are countless well-documented benefits of using this architecture design that have already been covered by others at length. That said, there is one aspect of this design that I always pay careful attention to because when I haven’t it’s led to some interesting challenges.

While building loosely coupled microservices is an extremely lightweight and rapid development process, inter-services communication models to share state, events and data between these services is not as trivial. The easiest communication model I have used is direct inter-service communication. However, as [explained](https://www.google.com/url?q=https://dzone.com/articles/using-redis-to-deal-with-inter-service-communicati&sa=D&ust=1550075590808000) eloquently by Fernando Dogio, it fails at scale—causing crashed services, retry logics and significant headaches when load increases—and should be avoided at all costs. Other communication models range from generic Pub/Sub to complex Kafka event streams, but most recently I have been using Redis for communication between microservices.

### Redis to the rescue!

Microservices distribute state over network boundaries. To keep track of this state, events should be stored in, let’s say, an event store. Since these events are usually an immutable stream of records of asynchronous write operations (a.k.a. transaction logs), the following properties apply:

1. Order is important (time-series data)
1. Losing one event leads to a wrong state
1. The replay state is known at any given point in time
1. Write operations are easy and fast
1. Read operations require more effort and should therefore be cached
1. High scalability is required, as each service is decoupled and doesn’t know the other

With Redis, I have always easily implemented [pub-sub](https://www.google.com/url?q=https://redis.io/topics/pubsub&sa=D&ust=1550075590810000) patterns. But now that the new [Stream](https://www.google.com/url?q=https://redis.io/topics/streams-intro&sa=D&ust=1550075590811000)s data type is available with [Redis 5.0](https://www.google.com/url?q=/blog/redis-5-0-is-here/&sa=D&ust=1550075590811000), we can model a log data structure in a more abstract way—making this an ideal use case for time-series data (like a transaction log with at-most-once or at-least-once delivery semantics). Along with Active-Active capabilities, easy and simple deployment, and in-memory super fast processing, Redis Streams is a must-have for managing microservices communication at scale.

The basic pattern is called Command Query Responsibility Segregation ([CQRS](/solutions/microservices/cqrs/)). It separates the way commands and queries are executed. In this case commands are done via HTTP, and queries via RESP (Redis Serialization Protocol).

Let’s use an example to demonstrate how to create an event store with Redis.

### OrderShop sample application overview

I created an application for a simple, but common, e-commerce use case. When a customer, an inventory item or an order is created/deleted, an event should be communicated asynchronously to the CRM service using RESP to manage OrderShop’s interactions with current and potential customers. Like many common application requirements, the CRM service can to be started and stopped during runtime without any impact to other microservices. This necessitates that all messages sent to it during its downtime be captured for processing.

The following diagram shows the inter-connectivity of nine decoupled microservices that use an event store built with [Redis Streams](https://www.google.com/url?q=https://redis.io/topics/streams-intro&sa=D&ust=1550075590813000) for inter-services communication. They do this by listening to any newly created events on the specific event stream in an event store, i.e. a Redis instance.

![OrderShop Architecture](/images/site-mirror/d3f988e4704ce8fbe1e950c57ecb1a297d939f87-720x405.webp)

*Figure 1: OrderShop Architecture*

The domain model for our OrderShop application consists of the following five entities:

1. Customer
1. Product
1. Inventory
1. Order
1. Billing

By listening to the domain events and keeping the entity cache up to date, the aggregate functions of the event store has to be called only once or on reply.

![OrderShop Domain Model](/images/site-mirror/c697b978771bbeaeac46e958487a40280627b6ba-720x405.webp)

*Figure 2: OrderShop Domain Model*

### Install and run OrderShop

To try this out for yourself:

1. Clone the repository from [https://github.com/Redislabs-Solution-Architects/ordershop](https://www.google.com/url?q=https://github.com/Redislabs-Solution-Architects/ordershop&sa=D&ust=1550075590817000)
1. Make sure you have already installed both [Docker Engine](https://www.google.com/url?q=https://docs.docker.com/install/&sa=D&ust=1550075590817000) and [Docker Compose](https://www.google.com/url?q=https://docs.docker.com/compose/install/&sa=D&ust=1550075590817000)
1. Install Python3 ([https://python-docs.readthedocs.io/en/latest/starting/install3/osx.html](https://www.google.com/url?q=https://python-docs.readthedocs.io/en/latest/starting/install3/osx.html&sa=D&ust=1550075590818000))
1. Start the application with ***docker-compose up***
1. Install the requirements with ***pip3 install -r client/requirements.txt***
1. Then execute the client with ***python3 -m unittest client/client.py***
1. Stop the CRM-service with ***docker-compose stop crm-service***
1. Re-execute the client and you’ll see that the application functions w/o any error

### Under the hood

Below are some sample test cases from [client.py](https://github.com/Redislabs-Solution-Architects/ordershop/blob/master/client/client.py), along with corresponding Redis data types and keys.

| Test Case | Description | Types | Keys |
|---|---|---|---|
| test_1_create_customers | Creates 10 random customers | Set   Stream Hash | customer_ids   events:customer_created customer_entity:customer_id |
| test_2_create_products | Creates 10 random product names | Set   Stream Hash | product_ids   events:product_created product_entity:product_id |
| test_3_create_inventory | Creates inventory of 100 for all products | Set   Stream Hash | inventory_ids   events:inventory_created inventory_entity:inventory_id |
| test_4_create_orders | Creates 10 orders for all customers | Set   Stream Hash | order_ids   events:order_created order_product_ids:<> |
| test_5_update_second_order | Updates second order | Stream | events:order_updated |
| test_6_delete_third_order | Deletes third order | Stream | events:order_deleted |
| test_7_delete_third_customer | Deletes third customer | Stream | events:customer_deleted |
| test_8_perform_billing | Performs billing of first order | Set   Stream Hash | billing_ids   events:billing_created billing_entity:billing_id |
| test_9_get_unbilled_orders | Gets unbilled orders | Set   Hash | billing_ids, order_ids   billing_entity:billing_id, order_entity:order_id |

I chose the ***Streams*** data type to save these events because the abstract data type behind them is a transaction log, which perfectly fits our use case of a continuous event stream. I chose different keys to distribute the partitions and decided to generate my own entry ID for each stream, consisting of the timestamp in seconds “-” microseconds (to be unique and preserve the order of the events across keys/partitions).

```python
127.0.0.1:6379> XINFO STREAM events:order_created
 1) “length”
 2) (integer) 10
 3) “radix-tree-keys”
 4) (integer) 1
 5) “radix-tree-nodes”
 6) (integer) 2
 7) “groups”
 8) (integer) 0
 9) “last-generated-id”
10) “1548699679211-658”
11) “first-entry”
12) 1) “1548699678802-91”
    2) 1) “event_id”
       2) “fdd528d9-d469-42c1-be95-8ce2b2edbd63”
       3) “entity”
       4) “{\”id\”: \”b7663295-b973-42dc-b7bf-8e488e829d10\”, \”product_ids\”:
[\”7380449c-d4ed-41b8-9b6d-73805b944939\”, \”d3c32e76-c175-4037-ade3-ec6b76c8045d\”,
\”7380449c-d4ed-41b8-9b6d-73805b944939\”, \”93be6597-19d2-464e-882a-e4920154ba0e\”,
\”2093893d-53e9-4d97-bbf8-8a943ba5afde\”, \”7380449c-d4ed-41b8-9b6d-73805b944939\”],
\”customer_id\”: \”63a95f27-42c5-4aa8-9e40-1b59b0626756\”}”
13) “last-entry”
14) 1) “1548699679211-658”
    2) 1) “event_id”
       2) “164f9f4e-bfd7-4aaf-8717-70fc0c7b3647”
       3) “entity”
       4) “{\”id\”: \”1ea7f394-e9e9-4b02-8c29-547f8bcd2dde\”, \”product_ids\”:
[\”2093893d-53e9-4d97-bbf8-8a943ba5afde\”], \”customer_id\”:
\”8e8471c7-2f48-4e45-87ac-3c840cb63e60\”}”

```

I choose ***Sets*** to store the IDs (UUIDs) and ***Lists*** and ***Hashes*** to model the data, since it reflects their structure and the entity cache is just a simple projection of the domain model.

```python
127.0.0.1:6379> TYPE customer_ids
set

127.0.0.1:6379> SMEMBERS customer_ids
1) “3b1c09fa-2feb-4c73-9e85-06131ec2548f”
2) “47c33e78-5e50-4f0f-8048-dd33efff777e”
3) “8bedc5f3-98f0-4623-8aba-4a477c1dd1d2”
4) “5f12bda4-be4d-48d4-bc42-e9d9d37881ed”
5) “aceb5838-e21b-4cc3-b59c-aefae5389335”
6) “63a95f27-42c5-4aa8-9e40-1b59b0626756”
7) “8e8471c7-2f48-4e45-87ac-3c840cb63e60”
8) “fe897703-826b-49ba-b000-27ba5da20505”
9) “67ded96e-a4b4-404e-ace6-3b8f4dea4038”

127.0.0.1:6379> TYPE customer_entity:67ded96e-a4b4-404e-ace6-3b8f4dea4038
hash

127.0.0.1:6379> HVALS customer_entity:67ded96e-a4b4-404e-ace6-3b8f4dea4038
1) “67ded96e-a4b4-404e-ace6-3b8f4dea4038”
2) “Ximnezmdmb”
3) “ximnezmdmb@server.com”

```

### Conclusion

The wide variety of data structures offered in Redis—including Sets, Sorted Sets, Hashes, Lists, Strings, Bit Arrays, HyperLogLogs, Geospatial Indexes and now [Streams—](https://www.google.com/url?q=https://redis.io/topics/streams-intro&sa=D&ust=1550075590850000)easily adapt to any data model. Streams has elements that are not just a single string, but are objects composed of fields and values. Range queries are fast, and each entry in a stream has an ID, which is a logical offset. Streams provides solutions for use cases such as time series, as well as streaming messages for other use cases like replacing generic Pub/Sub applications that need more reliability than fire-and-forget, and for completely new use cases.

Because you can scale Redis instances through sharding (by clustering several instances) and offer persistence options for disaster recovery, Redis is an enterprise-ready choice.

Please, feel free to reach out to me with any questions or to share your feedback.

ciao
