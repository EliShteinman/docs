---
title: "How Redis Enterprise Powers TransNexus’ Microservices Architecture to Help Fight Robocallers"
linkTitle: "How Redis Enterprise Powers TransNexus’ Microservices Architecture to Help Fight Robocallers"
url: "/blog/how-redis-enterprise-powers-transnexus-microservices-architecture-to-help-fight-robocallers/"
description: "(As organizations look to modernize their applications, many are turning to a microservices architecture to deconstruct their legacy apps into collections of loosely coupled services. This profound..."
date: 2020-05-21
blogCategories:
- "Company"
authors:
- "Haley Kim"
lastmod: 2025-09-17
hidden: true
---

*By Haley Kim, Associate Content Producer · Published 21 May 2020 · updated 17 September 2025*

![Blog tile image](/images/site-mirror/0073e867b4e64f59de9047fdcde04295ba647e5c-772x550.webp)

*(As organizations look to modernize their applications, many are turning to a microservices architecture to deconstruct their legacy apps into collections of loosely coupled services. This profound change inspired us to reach out to Redis users in various stages of this journey to microservices architectures. We are telling their microservices stories in a series of blog posts, which *[*began in late 2019*](/blog/how-mutualink-uses-redis-to-support-a-life-saving-microservices-architecture/)*.)*

![](/images/site-mirror/88755ea974252595572a2cb04767edac411e4b0b-400x160.svg)

You’re on the way to the grocery store when your phone rings. It’s a number you don’t recognize. Do you pick up?

If the idea of ignoring your phone—even for an unknown caller—invokes apprehension and concern, congratulations: you’re a normal 21st Century human being, and also a great target for robocallers.

Last year the average U.S. consumer received [178 robocalls](https://www.forbes.com/sites/kenrickcai/2020/02/11/twilio-jeff-lawson-robocalls/#7842c8ff7161). And as everyone who’s ever experienced one understands, robocalls are huge annoyances, and they have real negative consequences. When consumers grow frustrated with constant robocalls, for example, they may stop picking up the phone altogether for numbers they don’t recognize. That means they could miss important connections, and legitimate businesses can’t contact their customers.

Fortunately, disruptive companies on the front lines of the robocall wars are building new technologies designed to restore our trust in telephone services. [Alec Fenichel](https://www.linkedin.com/in/fenichelar), Senior Software Architect at telecom software provider [TransNexus](https://transnexus.com/), is one such superhero working to modernize telecom services for consumers, enterprises, and telephone service providers around the world. In an industry known for its complexity, TransNexus’ telephone software simplifies critical functions like preventing robocalls, denial-of-service attacks, and toll fraud as well as enabling least-cost routing, call authentication, and more.

TransNexus—founded in 1997—provides telcos with two products: [NexOSS](https://transnexus.com/nexoss/), on-premises VoIP telecom applications, and [ClearIP](https://transnexus.com/clearip/), a telecom software platform hosted in the cloud. Key technologies to drive the elimination of robocalls include:

1. Call analytics for robocall mitigation
1. STIR/SHAKEN for caller ID authentication and verification (known as Secure Telephone Identity to prevent robocallers from altering their caller ID numbers)
1. Blacklists to prevent neighbor-spoofing (robocalls using calling numbers similar to the called party’s number, including area and code and exchange)

Redis Enterprise is critical to TransNexus’ success, as a real-time database for the cloud product. “When we receive a telephone call, we need to make a decision on how a call should be routed, like whether it should be allowed or blocked. All of that process is done via interactions with Redis,” Fenichel says, “and it has to be done in real time.”

## Reliability, security, and performance

Reliability, security, and high performance were the focus of ClearIP’s design, Fenichel explains, and are inherent features of microservices architectures. TransNexus’ call processing, which includes a significant amount of work, is typically completed in about 20 milliseconds. The aim is to do the work quickly, so users never notice.

From the beginning, TransNexus’ ClearIP was designed to perform complex call processing within a microservices architecture. “Microservices architecture makes it very easy to scale as needed, and it’s also very easy to maintain and be reliable. If a server fails, it will be automatically replaced and no one even notices,” he says.

## Redis is the most important database

TransNexus currently has hundreds of millions of keys in Redis databases. Some of TransNexus’ customers are making thousands of calls per second. Since performance is so critical for TransNexus’ operations, the team has been careful to limit the extent of Redis’ operations. The team relies almost exclusively on Strings and Hashes but uses Lists in a few instances and Sorted Sets for one particular use case.

Redis Enterprise acts as a real-time database, storing configuration data and helping ensure that TransNexus’ services can respond instantly to meet the company’s aggressive application requirements. “Redis is the only database we need online to perform call processing. It is the number-one most important database,” Fenichel says. “Our other databases are used to power the user interfaces and things of that nature. But when a call is processed, it never touches anything but the Redis database. This is by design to minimize the impact of any other database failure. That makes Redis the most important database by far.”

But that’s not all. Redis also acts as an intermediary queueing system that assigns jobs to cloud servers: Once a record is processed, it’s placed in a queue in Redis, which is then flushed into a data warehouse. Redis is also a historical information store for call histories and accounts. “For example, if these incoming calls are abnormal for whatever reason, Redis stores information important for making determinations going forward from an [anomaly detection](/redis-enterprise/use-cases/fraud-mitigation/) standpoint,” Fenichel says.

*Looking to learn more about microservices? Check out how* [*Mutualink*](/blog/how-mutualink-uses-redis-to-support-a-life-saving-microservices-architecture/)* uses Redis for a life-saving microservices architecture and how software agency* [*Z3 Works*](/blog/redis-powered-microservices-architecture-proves-its-worth-in-two-very-different-projects-for-z3-works/)* uses it for a variety of projects across a variety of industries. Hear Redis Developer Advocates Kyle Davis and Loris Cro discuss their new free e-book, “*[*Redis Microservices for Dummies*](/docs/redis-microservices-for-dummies/)*,” on* [*The New Stack podcast*](/blog/redis-microservices-for-dummies-podcast-kyle-davis-loris-cro-the-new-stackj/)*.*
