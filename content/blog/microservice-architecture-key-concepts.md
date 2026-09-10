---
title: "Microservice Architecture Key Concepts"
linkTitle: "Microservice Architecture Key Concepts"
url: "/blog/microservice-architecture-key-concepts/"
description: "What role do microservices play in creating applications? We offer a foundational understanding of what microservices are, how they differ from monolithic structures, and what to consider when you..."
date: 2023-04-05
blogCategories:
- "Tech"
authors:
- "Redis  "
lastmod: 2025-03-27
hidden: true
mirrored: true
---

*By Redis   · Published 5 April 2023 · updated 27 March 2025*

![Blog tile image](/images/site-mirror/7ba94e54dd715cc098b35f5ed780af06089b9466-772x550.webp)

**What role do microservices play in creating applications? We offer a foundational understanding of what microservices are, how they differ from monolithic structures, and what to consider when you evaluate microservices for your own adoption.**

[Microservice architecture](/solutions/microservices/) is a framework that represents different parts of a workflow or process, usually involving one area of a business. For instance — take a [retail](/industries/retail/) app that involves a shopping cart, order management, payments, checkout, product catalogs, back-end [finance](/industries/financial-services/)/accounting integration, and customer services support. These services are uncoupled, representing different knowledge domains, though they do need to intersect with one another to have a fully-functional microservices application.

Independent, autonomous software development teams manage, test, and deploy these uncoupled services without affecting the rest of the overall system. The result of these independent-yet-connected services is a framework that works as a larger architecture. When it is implemented well, this compartmentalization makes operations more flexible by allowing teams to create their own release cycles, quickening production, and reducing time-to-market by simplifying operations with reusable artifacts.

### Microservice architecture vs. monolithic architecture

A monolith is a single massive unit. Think Ayer’s Rock in Australia (its aboriginal name, “Uluru,” means “giant monolith”), the Great Sphinx, or Michelangelo’s “La Pieta.” The point is: monoliths often are *hefty* structures.

In that vein, a monolithic architecture is one that connects all the different business units of an entire application into one single stack that shares the same code base. This structure makes it particularly difficult to scale any separate components independently. Take a publishing site, for instance, where users request articles very frequently, but new articles are published infrequently by comparison. In a monolith, you can’t effectively isolate and scale article reading from publishing.

A microservice architecture will segment disparate business domains, allowing independent teams to choose the tech stack they believe they need for continuous successful releases.

## Microservice architecture characteristics

Microservices enable teams to scale their entire application and to answer customer demands faster with updates that don’t require entire stack overhauls. These are some of the key characteristics that define how developers can establish microservices.

### Service independence and autonomy

In any company, each business unit has its own set of business challenges and objectives associated with that specific application. In most cases, each development team has the autonomy to choose the tools, technology, and resources that help them achieve their scope of work within their bounded context. This architecture works perfectly well with a polyglot technology stack, so developers have ample flexibility when building microservice applications the way they want in order to meet the performance, availability, continuous release cycle, and automated testing goals. In microservices, the “master of your domain” adage rings especially true, as each team is segmented by functions and ultimately responsible for what they build. Creating modular teams working on specific services within the overall microservice application helps to accelerate time to market**.**

One successful practice is [domain-driven design](https://martinfowler.com/bliki/DomainDrivenDesign.html), which encourages developers to understand their domains in-depth so that the software development serves their users’ needs. In this case, the users are not always other humans, though; other related services need to be served, too. While a development team may have a lot of autonomy, it does need to work seamlessly with other development teams.

The pieces have to fit together, and they need consistent interfaces. Many companies implement decentralized governance to ensure that software stays in compliance across the organization, often with the help of subject matter experts (SMEs), such as enterprise architects.

#### Practical advice: Establish a fault tolerance strategy early on

Sometimes, parts of a large microservice application fail. Even with loosely coupled functions deployed as multiple microservices, it is important to keep the communication lines open. If a single microservice fails, the microservice architecture needs a fallback behavior that is implemented at the code level to account for this disruption. Otherwise, a “minor” failure can create [a domino effect of failures](https://simpleflying.com/british-airways-us-flights-it-chaos/) with all other microservices.

A fault can arise from any number of causes, from an unavailable server to an inaccessible database. Fortunately, there are ways to sidestep these challenges. Among them: [replicating instances](/blog/what-is-data-replication/), adding timeouts on requests, and using [libraries](/blog/introducing-redis-om-client-libraries/) that use fault-tolerant [design patterns](https://itnext.io/5-patterns-to-make-your-microservice-fault-tolerant-f3a1c73547b3/) to fortify the resiliency of a microservices application. One way or another, design your microservices with the assumption that things will fail at the worst possible time – and ideally, only one component goes down.

#### Practical advice: Keep domains loosely-coupled

According to [Conway’s Law](https://www.atlassian.com/blog/teamwork/what-is-conways-law-acmi/), coined by computer scientist Melvin Edward Conway, “Any organization that designs a system (defined broadly) will produce a design whose structure is a copy of the organization’s communication structure.” Expect your stack to reflect how your company is organized and factor that into your design process.

In particular, do your best to keep systems in your microservices architecture as loosely coupled as possible. You don’t want changes to the design, implementation, or behavior of one element to cause changes in another. It’s [a bad idea](https://www.capitalone.com/tech/software-engineering/how-to-avoid-loose-coupled-microservices/) to change to one microservice to enforce an almost immediate change to all other microservices that collaborate with it directly or indirectly.

If multiple microservices are built with the heavy dependencies that occur at an organizational level, domains lose their autonomy and, with that, the ability to produce their own release cycles. It’s important to strike the right balance.

### Communication via APIs and messages

The inter-service communication methods between a monolithic and a microservice architecture are quite different. Components are hard to scale independently in monolithic applications and are highly coupled. Microservices are loosely coupled, and they can use different inter-service communication mechanisms to exchange information, such as REST APIs or some type of message queue system.

A monolithic architecture already has all components working together with possibly one or two primary databases. Each microservice has its own instance, and they don’t necessarily share the same data stores; that’s part of domain-driven design and polyglot persistence — you can select the right data store for each microservice.

Microservices use either synchronous or asynchronous communication, meaning the component waits for a reply (synchronous) or it doesn’t (asynchronous). An example of a synchronous communication scenario would be an authentication service for validating a login and password; the service requires a response in order to allow the user into the microservices-based application.

On the other hand, asynchronous communication isn’t bound by time, and the sending service requires no reply from another service(s) For example, in e-commerce, when a customer checks out, you want them to go about the rest of their day. They don’t need to wait for you to process the order, receive payment, and eventually fulfill the order. This is all done asynchronously, and the customer is informed of progress through notifications (in-app push notifications, emails, or an order status page).

#### Practical advice: API design and service registry

Generally, you can use a [message broker](/solutions/messaging/) for asynchronous communication between services, though it’s important to use one that doesn’t add complexity to your system and possible latency if it doesn’t scale as the messages grow.

**Version** **your APIs**: Keep an ongoing record of the attributes and changes you make to each of your services. “Whether you’re using REST API, gRPC, messaging…” wrote [Sylvia Fronczak for OpsLevel](https://www.opslevel.com/blog/the-ultimate-guide-to-microservices-versioning-best-practices/), “the schema will change, and you need to be ready for that change.” A typical pattern is to embed the API (application programming interface) version into your data/schema and gracefully deprecate older [data models](/blog/nosql-data-modeling/). For example, for your service product information, the requestor can ask for a specific version, and that version will be indicated in the data returned as well.

**Less chit-chat, more performance**: Synchronous communications create a lot of back and forth between services. If synchronous communication is really needed, this will work okay for a handful of microservices, but when dozens or even hundreds of microservices are in play, synchronous communication can bring scaling to a grinding halt. Perform a microservices audit to determine where synchronous is required and where it isn’t. Asynchronous methods, such as using a message broker, will help reduce dependencies, improve overall fault tolerance, and alleviate performance sluggishness.

**Note every change (and keep tidy)**: A service registry is a manifest that notes the locations (through IP addresses, for example) of any available instances. IP addresses are amorphous – they can change with rapid cadence, from one minute to the next – so document the system and its changes.

## Build in security even more fervently

A monolithic application has only a couple of entry points, notes Prabath Siriwardena and Nuwan Dias, the authors of [Microservices Security in Action](https://www.manning.com/books/microservices-security-in-action). But applications written with a microservices architecture offer far more. “As the number of entry points to the system increases, the attack surface broadens too,” they write. “This situation is one of the fundamental challenges in building a security design for microservices. Each entry point to each microservice must be protected with equal strength. The security of a system is no stronger than the strength of its weakest link.”

Writing secure code is important for even the most trivial application, but it’s even more of an issue with a microservices architecture. The broader the attack surface, the higher the risk of attack.

Unlike in a monolithic application, each deployed microservice has to carry out independent security screening – and that has an effect on performance, the book authors point out.

#### Practical advice: Put security parameters in place,

**Test in a controlled environment**: A [sandbox](https://codesandbox.io/examples/package/redis) is a safe and controlled environment where developers can test their code before it goes into production. That makes a difference in security testing as well as helps you discover hiccups in the connection between services.

**Deploying with Kubernetes? Use an operator**: Kubernetes is a popular choice for deploying containerized applications and spinning up additional microservice instances but can require extensive configuration from DevOps to properly deploy and secure. Having a Level III [Kubernetes operator](/blog/redis-enterprise-operator-for-kubernetes/) for a particular software component, e.g. database can help automate and secure deployment. Even [Kubernetes Secrets](/blog/kubernetes-secret/), which help keep sensitive information separate from an application’s code, are stored unencrypted in the API’s data store, readily accessible for anyone with authorization to create a pod in that same namespace.

## What’s next?

Hopefully, the above serves as a decent primer for understanding the basic concepts of microservices. We covered how a microservices architecture differs from monolithic applications, how software development teams communicate under both models, and the autonomy microservices enable for developers and best practices for fortifying data with proper API design practices.

If you’re new to working with microservice architectures, read our [5 Microservices Misconceptions](/blog/5-microservices-misconceptions/) post to help you sidestep the most common microservice trappings in application development.
