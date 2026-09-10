---
title: "Improves messaging system reliability without adding complexity to developers"
linkTitle: "Improves messaging system reliability without adding complexity to developers"
url: "/customers/mitto/"
description: "Mitto’s customers rely on instantly delivered messages, so it needs to ensure low latency, high availability, and high throughput even over global deployments, with no outages even for scheduled..."
group: "Telecommunications"
lastmod: 2025-09-12
hidden: true
---

*updated 12 September 2025*

###### Challenge

Mitto’s customers rely on instantly delivered messages, so it needs to ensure low latency, high availability, and high throughput even over global deployments, with no outages even for scheduled maintenance. Plus, the company needed to start thinking about its future scaling needs.

###### Solution

While Mitto has been using OSS Redis since the company was founded in 2013, Redis Enterprise was the clear choice for Mitto to fulfill its need for commercial support and future scaling. It’s currently used as a cache in Mitto’s tech stack.

###### Benefits

Moving to Redis Enterprise made it seamless for Mitto to prepare for future scaling needs. Plus, it was so easy for Mitto to migrate from a single OSS Redis shard to the new Redis Enterprise cluster that Mitto’s developers weren’t even aware of the change! And with support from Redis Enterprise and Redis, Mitto has been able to dramatically improve reliability of the platform.

> "It was so easy to migrate from a single shard of an open source Redis installation, without further changes in the application at all, to the new Redis Enterprise cluster."

In today’s world, there’s no such thing as delayed communication—consumers expect everything, especially texts, to be delivered instantly. That’s where Mitto comes in. The Zug, Switzerland-based company is a CPaaS (Communications-Platform-as-a-Service) and wholesale A2P (application-to-person) communications provider, focused on delivering automated messages—including SMS, chat app communications, two-factor authentication notices, RCS, and voice connectivity—from enterprises large and small, cloud application providers, and mobile network operators to their customers.

Mitto’s secret sauce is its globally enabled network, where it is able to constantly monitor the message routes it offers to customers and partners, providing the appropriate level of service for the various kinds of messages it receives and processes. Because Mitto can connect directly to many mobile network operators—as well as global operator partners like Saudi Arabia’s Etisalat, Germany’s Deutsche Telekom, and Spain’s Telefónica—it can provide extremely low latency and high quality of service, so messages are delivered almost instantly.

Given the need for instantly delivered text messages, Mitto’s biggest challenge is providing and maintaining its low latency—especially critical as Mitto scales its global platform to handle even more messages. “We must ensure that the systems we are operating are available at any given time,” including dealing with scheduled maintenance and outages, said Anton Dollmaier, Senior Site Reliability Engineer at Mitto. “Which means we need to keep the infrastructure especially focused on reliability and high availability.”

### Selecting Redis Enterprise

Mitto has been using OSS Redis as a cache almost since its inception in 2013, but as the company grew, it became clear that the team needed more support to provide the high availability and reliability it’s known for. “If we do have a problem with our product or with the infrastructure, then we definitely need to be able to reach out to our partners and get the support for the problem at hand to get the infrastructure back up and running as fast as possible in as short time as possible,” Dollmaier said.

Since the team was happy with OSS Redis, it was an easy call to adopt Redis Enterprise to fulfill its need for commercial support and plan for future scaling. “We were relying on OSS Redis, so it was easy to go forward with Redis Enterprise for increased support and to make scaling easier, Dollmaier said.

Mitto uses Redis Enterprise to store information about the processing of messages, including cached and previously retrieved information about which numbers to use (is it still in service, which network does the destination number belong to, etc.), how to route a message the shortest, fastest-possible way, and how to decide which supplier to use. Redis Enterprise also stores information about the content and senders of messages—for example, if a number is classified as spam it will get blocked.

Redis Enterprise is a key part of Mitto’s diverse tech stack, which also includes: HAProxy servers (to receive and process HTTP requests; RabbitMQ clusters (to process messages to the Message Service Platform, or MSP); redundant clusters of Percona Server for MySQL (to keep relational data); and finally Elasticsearch (to archive messages).

### Benefits of Redis Enterprise

Besides the enterprise support—which has helped reduce outages and shorten recovery times—the Mitto team has been impressed with the architecture of Redis Enterprise. “It was so easy to migrate from a single shard of an open source Redis installation, without further changes in the application at all, to the new Redis Enterprise cluster,” Dollmaier said. “That definitely was a surprise, it was so easy to set up.” So easy, in fact, that Mitto’s developers didn’t even realize the team switched to Redis Enterprise—they continued to use it locally just like the open source version. “It couldn’t get any easier from a developer standpoint,” Dollmaier said.

Mitto is now looking to scale its Redis Enterprise deployment, as it’s nearing the memory capacity of its current shard allocation as it handles 50K – 100K ops/sec. The team is also interested in Redis Enterprise’s [Active-Active replication](https://redis.io/active-active/), as it would give Mitto flexibility to synchronize the data it has in its Frankfurt, Germany, data center with local deployments all over the globe.
