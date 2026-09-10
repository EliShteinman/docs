---
title: "Microservices and the Data Layer—a New IDC InfoBrief"
linkTitle: "Microservices and the Data Layer—a New IDC InfoBrief"
url: "/blog/microservices-and-the-data-layer-new-idc-infobrief/"
description: "If you still harbored any doubt that microservice architectures are dominating today’s application development, it’s time to get over it. According to IDC’s new InfoBrief on The Impact of..."
date: 2021-01-07
blogCategories:
- "Company"
authors:
- "Mike Anand"
lastmod: 2025-03-27
hidden: true
mirrored: true
---

*By Mike Anand, Former Chief Marketing Officer · Published 7 January 2021 · updated 27 March 2025*

![Blog tile image](/images/site-mirror/702f35df7badbb3eb031f036b2672df05c6ab8aa-772x520.webp)

![](/images/site-mirror/1d1bf72ff5f5a3d65c73e359ad54eedb51010c4d-250x175.webp)

If you still harbored any doubt that [microservice architectures](/blog/microservice-architecture-key-concepts/) are dominating today’s application development, it’s time to get over it. According to IDC’s new InfoBrief on [**The Impact of Application Modernization on the Data Layer**](/docs/application-modernizaton-impact-on-data-layer/), sponsored by Redis, 89% of some 300 North American enterprise survey respondents are already using microservices. And that comes on top of [IDC’s 2019 prediction](https://www.idc.com/research/viewtoc.jsp?containerId=US44403818) that “By 2022, 90% of all new apps will feature microservices architectures.”

Microservices’ momentum is now undeniable, driven by enterprises’ need to more rapidly develop, deploy, and update high-quality apps and services to meet ever-rising customer and business requirements. According to the InfoBrief, “microservices apps are already used in business-critical roles, with 24% of microservices apps identified as business-critical.” For almost half of microservices apps (42%), for example, downtime leads to lost revenue.

But that doesn’t mean the microservices revolution is complete. In fact, it’s just getting started. According to the IDC survey, all those enterprises embracing microservices are doing so with just 17% of their app portfolios already migrated away from the monolith. The InfoBrief authors, Carl W. Olofson and Gary Chen, explain the situation succinctly: “Although development of microservices-based applications is still in an early phase, its significance in future development is clear.”

***Learn more:**** Read the *[*Redis Microservices for Dummies*](/docs/redis-microservices-for-dummies/)* e-book*

## Data layer compounds complexity for microservice architectures

So what will it take to fulfill the promise of microservice architectures, and what challenges are enterprises facing as they embrace microservices? Microservices adoption can add significant complexity, especially when it comes to the data layer. According to the survey, nearly half of enterprise microservices apps (47%) rely on a database, but nearly a third of respondents (31.5%) cite database management as a top-three challenge. “Decomposing applications exponentially increases the number of logical components that have to be managed,” the authors note.

That can leave data siloed, more complex, and expensive, leading many enterprises to conclude that orchestration is essential to deploying microservices. So it’s not surprising that around a third of respondents named reducing management costs and increased operational efficiency (35.6%) and supporting new, modern cloud-native or microservices applications (33.2%) as top-three drivers of orchestration deployment.

## Choosing the right database for your microservice architecture

An e-commerce solution, for example, might employ a number of services—application server, content cache, session store, product catalog, search and discovery, order processing, order fulfillment, analytics, and many more—and each service may have its own database, as shown in the diagram below:

![](/images/site-mirror/eaa6fbe95841d0037f21694240faf8129137bc15-1024x685.webp)

*A microservice architecture in a sample e-commerce solution.*

So, how do you choose and build applications with the right architecture? What characteristics do you need to look for? Research suggests focusing on four key must-haves. Let’s take a closer look:

## 1. The importance of performance

As IDC noted, “over 95% of respondents favor database type or performance as criteria” and almost half of survey respondents (45%) cited performance as a top-three factor (trailing only database type) when selecting a database. It’s no surprise that performance is so important, since in a microservice environment you need both real-time performance and the ability to scale in order to fully deliver on the promise of distributed architecture.

![](/images/site-mirror/1fad114de0a493e57dec3624dc80d74fa9515445-1024x621.webp)

Named the [most loved-database](/blog/redis-is-the-most-loved-database-for-the-4th-year-in-a-row/) four years running, Redis is well known for delivering sub-millisecond performance. With Redis Enterprise’s [low-latency database](/docs/latency-is-the-new-outage/), you can create instant user experiences or perform real-time analytics while keeping a small footprint with the ability to scale on-demand. As the InfoBrief notes, “This indicates that how the database works and performs is critical to microservices application development success.”

***Learn more: ****See our new *[*Latency Is the New Outage*](/docs/latency-is-the-new-outage/)* white paper*

## 2. Always available

![](/images/site-mirror/29b4184b6483b8f9634926fa57802a09c83eeb30-798x644.webp)

The IDC survey revealed that almost a quarter (24%) of enterprise microservice applications are already being used in business-critical roles, where high availability is critical. More generally, “for 42% of microservices apps, experiencing downtime results in direct loss of revenue for the organization,” the InfoBrief notes, while downtime in the remaining 58% of apps leads to loss of productivity.

That’s a big potential issue, because even though a microservice architecture incorporates many connected services, it faces the same performance and reliability demands as other development approaches. Ensuring your data is always available around the world is another challenge, for example. To ensure your applications remain available at all times, you need a database that is fault tolerant at all levels.

***Learn more: ****See how Redis Enterprise’s *[*high-availability technologies*](/redis-enterprise/technology/highly-available-redis/)* guarantee four-nines (99.99%) uptime—and five-nines (99.999%) in *[*Active-Active*](/active-active/)* geo-distributed deployments.*

## 3. Leveraging multiple data models to build modern applications

Developers leverage microservice architectures to build better apps. Selecting the right data model is essential for speeding time to market, and more importantly it optimizesdata-access patterns and performance requirements. This way, each service can use a database purpose-built for its own data model.

A microservice may employ a data model based on [key-value](/redis-enterprise/data-structures/), [JSON](/json/),[ time ser](/timeseries/)[ies](/modules/redis-graph/), and [search engines](/search/), among other things. But that means “many microservices will use a database per service,” the InfoBrief notes, which “increases the number of databases, the number of software components accessing databases, and the need for databases to be included in modern workflows.” That’s why, as noted above, database management with microservice apps is a top-three challenge for nearly a third (32%) of respondents.

![](/images/site-mirror/82029da13341946e60dc0ee5c0b3d4c62fda1db5-948x760.webp)

To minimize this complexity, your database should support [multiple data models](/redis-enterprise/multi-model/). That makes it easy for enterprise architects to choose the right data model for each service without sacrificing performance or having to learn and maintain multiple different databases, which simplifies operations and helps limit technology sprawl.

***Learn more: ****See our white **paper on *[*Strategic Data Flexibility*](/docs/strategic-data-flexibility/)

## 4. Deploy anywhere

Even as [DBaaS](/blog/what-is-dbaas/) gains momentum, a great deal of enterprise data remains on-premises, leading many enterprises to use multiple clouds and hybrid infrastructures, as shown in the IDC survey. In a microservices environment, you need the ability to optimize the data layer to give you the flexibility to run your database without silos or data loss.

![](/images/site-mirror/d3108d031053b934819c07a1f7756dd0bb852612-1024x733.webp)

But as the IDC authors point out, “Many databases were not designed to be cloud-native, compatible with containers, or orchestrated by Kubernetes.” Merely packaging a database within a container, for example, doesn’t make it right for a microservice architecture; the database must be lightweight and tunable to meet your data needs.

Enterprises need a database platform that offers flexible deployment models to run wherever it’s needed, whether that’s on-premises or in any cloud, in a multi-cloud or a hybrid-cloud architecture, in containers, or as a Kubernetes Pod.

***Learn more: ****Check out *[*Redis Enterprise Software Deployment Options*](/enterprise/deployment/)

## Redis Enterprise and microservices

According to the report, the rise of microservice architectures significantly impacts the data layer architecture used to support these services, so enterprises looking to develop applications using microservice architectures should pay special attention to technical excellence and fit for purpose. That is precisely where Redis Enterprise shines.

Redis Enterprise offers performance at microservices scale, delivers sub-millisecond latency for all Redis data types and modules, and [the ability to scale instantly and linearly](/redis-enterprise/technology/linear-scaling-redis-enterprise/) to almost any throughput needed. Designed for fault tolerance and resilience, Redis Enterprise uses a [shared-nothing cluster architecture](/redis-enterprise/technology/redis-enterprise-cluster-architecture/) and offers automated failover at the process level, for individual nodes, and even across infrastructure availability zones, as well as tunable persistence and disaster recovery. Redis Enterprise also makes it easy for developers to choose the data model best suited to the performance and data access requirements for their microservice architecture deployment, while retaining a unified operational interface to limit technology sprawl and simplify operations. Critically, [Redis Enterprise can be deployed anywhere](/deployment/method/)—on any cloud platform, on-premises, or in a multi-cloud or hybrid cloud architecture.

To learn more about the importance of the data layer in microservice deployments, download the full IDC InfoBrief—[**The Impact of Application Modernization on the Data Layer**](/docs/application-modernizaton-impact-on-data-layer/). And check out the microservice architecture resources below to more insight into the many ways Redis Enterprise is uniquely suited for microservice deployments:

- [Redis Enterprise for Microservices](/solutions/microservices/)
- [Redis Microservices for Dummies](/docs/redis-microservices-for-dummies/) e-book
- [Latency Is the New Outage ](/docs/latency-is-the-new-outage/)white paper
- [Strategic Data Flexibility](/docs/strategic-data-flexibility/) white paper
- [Redis Enterprise Software Deployment Options](/enterprise/deployment/)
- [How Redis Simplifies Microservices Design Patterns](https://thenewstack.io/how-redis-simplifies-microservices-design-patterns/)—The New Stack blog post
