---
title: "CQRS"
linkTitle: "CQRS"
url: "/solutions/microservices/cqrs/"
description: "Optimize queries to reduce costs in microservice applications"
aliases:
- "/solutions/microservices-cqrs/"
lastmod: 2025-08-13
---

*updated 13 August 2025*

Optimize queries to reduce costs in microservice applications

## What is CQRS?

Command Query Responsibility Segregation (CQRS) is a pattern within microservice architectures that decouples reads (queries) from writes (commands). This enables an application to optimize database writes to a slower disk-based SQL database, while pre-fetching and caching that data using Redis Enterprise’s integrated Change Data Capture (CDC) capability for read-optimized querying. Doing so enables the data to be shared with other microservices without breaking isolation and coupling their deployments.

## What is a CQRS pattern in microservices?

CQRS is a microservices design pattern that separates read and update operations for a data store to optimize its performance, scalability, and security.

## How it works in a payment app

1. Data is written to the system-of-record database within a microservice sub-domain (payment approval).
1. Data is pre-fetched to the Redis Enterprise cache from the system of record. The cache uses its own data schema optimized for queries and can perform dynamic indexing for searches.
1. Another microservice (payment history) reads directly from the cache with no coupling to the system of record command (write) database.
1. The Redis integrated Change Data Capture (CDC) capability tracks the updates in the command database transaction log, transforms row level change data into a read-optimized Redis data structure or model, and replicates the updates to the query database in near real time.

## When to use CQRS pattern

- Data from one domain needs to be queried by a different service without creating dependencies.
- The command database has complex business logic and must persist data for long term recordkeeping, but the read microservice just needs to query the data.
- Services have significantly more reads than writes.
- Read performance and scalability are critical requirements.
- The read data store is updated in near real time with changes in the write database (eventually consistent).

## Benefits of implementing CQRS pattern

- Improved read performance of repetitive queries.
- Independent scaling and optimization of write and read operations.
- Support of multiple data structures and models on unified data platform.
- Decreased burden on the command database (systems of record) saving infrastructure costs.
- Reduced developer resources due to simplicity of deploying Redis Enterprise cache and integrated CDC capability.

## Learn more

## Related resources

## FAQs

### What are microservice domains?

Typically in microservices architectures, Domain-Driven Design (DDD) refers to the application’s business function as the domain. A domain consists of multiple subdomains, which corresponds to a different part of the business. As an example, in an retail eCommerce website domain may consist of several subdomains including product catalog, shopping cart, checkout, inventory and order management, etc.

### How does the CQRS pattern differ from traditional CRUD-based architectures?

[CRUD](https://dzone.com/articles/data-management-patterns-for-microservices) stands for Create, Read, Update, and Delete and is the most common pattern for traditional data operations for applications. It uses the same data store and model for read and write operations as opposed to Command Query Responsibility Segregation (CQRS) which separates the read and write data models. One of the primary advantages of CRUD design is its simplicity, you can use the same set of classes for all functions. For applications which employ simple business logic, e.g. a user registration app for managing registration, storing a list of users, updating user information, and removing users, CRUD is the best fit. However, as your application become increasingly complex, say in a financial services app with payments, fraud detection, settlement, and compliance domains using a microservice architecture with dozens or hundreds of services each with different databases and access requirements, a CQRS pattern could be a better match in this scenario.

### What is CDC?

Change data capture (CDC) refers to the tracking of all changes in a data source so they can be replicated and sync’d to the destination systems. CDC provides data integrity and consistency across domains and services.

### What are Advantages and Disadvantages of CQRS?

One of the main advantages of using the CQRS design pattern is that it allows for better scalability and performance. Since the read and write operations are separated, they can be optimized independently, resulting in faster response times for read operations. However, the CQRS pattern can also add complexity to an application. Developers need to be careful to maintain consistency between the read and write models, and the additional complexity can make the application harder to maintain.

### How do Event Sourcing and CQRS work together?

Event Sourcing is a technique that can capture every change made to an application’s state as a series of events. Instead of storing the current state of an application, Event Sourcing stores the history of all the events that led up to the current state. This means that at any point in time, you can reconstruct the state of the application by replaying the events that led up to it. Event Sourcing can be used in conjunction with CQRS to provide a scalable and efficient way to have separate read and write data models to optimize performance of specific microservices. When you use Event Sourcing with CQRS, the write model can use an event store like Redis Streams to capture data updates. The read model then uses this update event stream to maintain eventual consistency, making it easier to scale the read model independently from the write model. Another option is to use Change Data Capture solutions like Oracle Goldengate, Kafka Connect, or Redis Enterprise integrated CDC capability that are designed for this use case with multiple source and sink connectors to different database vendors.

### What is Integration of CQRS with DDD?

CQRS can be integrated with Domain Driven Design (DDD), which is an approach to software development that focuses on the business domain and its processes. The synergy between CQRS and DDD creates a powerful combination that allows for efficient and scalable software development. CQRS also allows for a better separation of concerns. The domain model can focus on the business logic, while the read model can focus on querying and reporting. This separation makes the application easier to understand and maintain. Another advantage of using CQRS in DDD is that it simplifies testing and debugging. Since the read and write operations are separated, they can be tested independently, making it easier to isolate and fix issues.
