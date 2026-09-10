---
title: "Message Broker Pattern for Microservices Interservice Communication"
linkTitle: "Message Broker Pattern for Microservices Interservice Communication"
url: "/solutions/message-broker-pattern-for-microservices-interservice-communication/"
description: "Simplify messaging between microservices"
lastmod: 2026-05-21
mirrored: true
---

*updated 21 May 2026*

Simplify messaging between microservices

Microservices rely on interservice communication to share events, state, and data as well as to maintain isolation and decoupling. Many developers implement an asynchronous event-driven publish-subscribe [message broker](https://redis.io/solutions/messaging/) for interservice communication, but doing so is complicated.

Here’s a better way: Redis Streams acts as both a native log data structure and communication channel that can publish an event without requiring an immediate response. It is simple to deploy, supports message persistence, and offers scalability through consumer groups.

## How Redis Stream works as a message broker

1. A microservice domain publishes an event into its own stream and its name reflects the event topic.
1. Each event is a stream entry. The event timestamp acts as the entry-id.
1. Other microservices subscribe to specific event streams.
1. The subscriber acknowledges the event was successfully processed and remembers the last entry-id it processed to easily recover from a failure or disconnect.
1. Redis Streams inspects the status of unprocessed messages and reassigns an event to another subscriber after a specified period of time.

## When to use an event-driven message broker

- [Asynchronous communication](/blog/what-to-choose-for-your-synchronous-and-asynchronous-communication-needs-redis-streams-redis-pub-sub-kafka-etc-best-approaches-synchronous-asynchronous-communication/) use cases where all services in an app do not need to be present to process messages; or some services only need a subset of the information from another service.
- You need to reliably store and transmit transient data as an immutable, append-only series of time-stamped events.
- One-to-many communications are required but using message queues are inefficient and requires the location and status of all receiving services.
- Messages require low latency and persistence, acknowledgement, and they can easily handle failure scenarios.

## Why use Redis Enterprise

- Lightweight design and implementation enable faster time to market. You can get started prototyping in minutes.
- Increase microservices scalability and responsiveness, even under intense message loads.
- 99.999% uptime SLA and resiliency (Active-Active geo distribution) help to prevent app downtime.
- Apps can easily handle retries, failure scenarios, and the addition of new subscribing services.
- Simpler integration with support for a range of platforms and programming languages, as well as for on-premises and managed services in the cloud.

## Learn more

## Related resources

## FAQ

### What is a message broker?

A message broker is software that facilitates the exchange of messages among apps, systems, and services. In a microservices architecture, services can communicate with each other using the message broker, even if they’re built using different technologies or deployed on separate platforms.

### What is the difference between synchronous and asynchronous communication patterns?

Synchronous communication means that all participants in a channel, senders and receivers, need to be active at the same time to be able to communicate. A simple example is Service A and Service B doing direct remote procedure calls (RPC), by invoking Service B’s HTTP REST endpoint from Service A, However, if Service B went offline, Service A would not be able to communicate with B, and so A would need to implement an internal failure recovery procedure. Asynchronous means communication can still happen even if not all participants are present at the same time. e.g. Service A does not wait on response from Sender B.

### What are some common methods of interservice communication?

APIs, task queues, messaging queues (RabbitMQ), event streams (Kafka), and message brokers.

### What is a brokerless and brokered communications?

In brokerless communication, all participants are connected directly. Brokered communications means that all participants connect to the same service via a message broker, which acts, as the name implies, as a centralized broker to implement the message-routing mechanism. Message brokers can work with both synchronous and asynchronous communications, but is typically associated with asynchronous.

### What is an event-driven architecture (EDA)?

Event-driven architectures use events to trigger and communicate between decoupled services and are common in modern apps built with microservices. An event is a change in state, or an update, like an item being ordered on an ecommerce website causing the inventory management system to decrease the in-stock value by one. Event-driven architecture is ideal for real-time apps that need to ingest and process large volumes of data with very low latency or when different subsystems or microservices must perform different types of processing on the same event data. EDA can use a publish/subscribe (pub/sub) model or an event streaming model.
