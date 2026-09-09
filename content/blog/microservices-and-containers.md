---
title: "Microservices and Containers Explained… Using LEGOs"
linkTitle: "Microservices and Containers Explained… Using LEGOs"
url: "/blog/microservices-and-containers/"
description: "Just as a LEGO set consists of multiple pieces that you put together to build different structures, microservices are small, independent components that you can combine to build larger..."
date: 2023-06-05
blogCategories:
- "Uncategorized"
authors:
- "Angel Camacho"
lastmod: 2025-03-27
hidden: true
---

*By Angel Camacho, Contributor · Published 5 June 2023 · updated 27 March 2025*

![Blog tile image](/images/site-mirror/7a381b4cafcc78f73333778e4542dd57ed3666e2-772x550.webp)

**Just as a LEGO set consists of multiple pieces that you put together to build different structures, microservices are small, independent components that you can combine to build larger applications. This is a stark departure from the traditional monolithic architecture, where an application is developed as a single unit, often leading to less flexible and harder-to-maintain monolithic apps.**

Developers are familiar with the concept of designing their applications in modules, where each routine is responsible for doing one thing well. That’s a useful starting point for understanding the role of [microservices](/solutions/microservices/) in a modern software architecture, wherein applications are structured as a collection of independent, small, and loosely coupled services.

But an even better analogy may be LEGOs, the stackable plastic blocks that have become [a ubiquitous children’s toy](https://amzn.to/3IqBmVg) and a [hobbyists’ dream](https://www.mentalfloss.com/article/27963/10-geekiest-lego-creations). You can accomplish quite a bit with the simplest elements but also do amazing things when you [master the tools](https://www.careeraddict.com/become-lego-master). Similarly, mastering container technology opens up new possibilities in software development.

Each microservice can be developed, deployed, and scaled independently, so developers can build and maintain complex applications efficiently. Microservices can communicate with each other through APIs, which enables the application to function as a cohesive whole. This allows for a more streamlined process of application development.

To visualize the relationships, think of microservices as if they are a LEGO set. Just as a LEGO set consists of multiple pieces that you put together to build different structures, microservices are small, independent components that you combine to build a larger application.

And, just as a LEGO set allows builders to swap pieces in and out, developers can replace or update microservices without affecting the entire application or having to deal with a complex monolithic application. This modularity and flexibility are among the reasons that microservices are so popular in software development. In 2022, for example, [more than a third of software developers employed microservices](https://www.jetbrains.com/lp/devecosystem-2022/microservices/).

Microservices are:

- **Small and focused** on doing one thing well
- Designed to **communicate through APIs** or other lightweight mechanisms
- Developed and **deployed independently**
- Typically organized around business capabilities, to **solve** **individual user stories**
- **Technology agnostic**, supportingmost programming languages
- Designed for **resilience** and fault-tolerance

## What containers are

An ongoing computing problem is the need to get software to run reliably when it’s moved from one computing environment to another. Maybe it’s as simple as the desire to migrate from a developer’s laptop to a test environment, or to move from a staging environment into production, where the operating system versions and server configurations are [not exactly the same](https://blog.codinghorror.com/the-works-on-my-machine-certification-program/). With a larger corporate scope, though, the issue comes up when a development team needs to shift from a physical machine in a data center to a virtual machine in a private or public cloud.

Containers are a way to package and run applications in a portable and isolated environment. They have become the de facto standard way to deploy software applications, allowing them to run reliably and consistently across different environments. A container image includes the application and all its dependencies, packaged into a single deployable unit.

Again, consider a LEGO set that has lots of pieces. You want to build a few different things: a car, a plane, and a Star Wars [Millennium Falcon](https://www.lego.com/en-us/product/millennium-falcon-75192?consent-modal=show). Instead of throwing all the pieces in one big pile and trying to sort through them every time you build something new, you sort pieces into smaller containers based on what they’re used for: big blocks in one container, small blocks in another, and so on.

Think of the LEGO pieces as though they represent the code and resources that make up a microservice, and the containers represent the isolated environment where the microservice runs. Using containers to separate the microservices makes it easier to manage and deploy them independently, just as sorting the LEGO pieces into containers makes it easier to build different models without having to search for the right pieces each time. Or [step on one](https://tinybeans.com/science-reveals-why-stepping-on-lego-bricks-hurts-so-much/).

Components of containers:

- Containers **use the host operating system’s kernel** to run, which allows them to be lightweight and efficient.
- Containers include **the application code and all its dependencies**, including libraries and system tools, into a single package.
- The **container engine manages the lifecycle of containers**, including starting, stopping, and removing them.

## Benefits of pairing microservices and containers

This concept of managing and deploying containers, known as container orchestration, has revolutionized the way developers work, allowing for the easy handling of containerized applications. A container orchestration platform like Kubernetes can manage multiple containers at once, making it easier to handle large applications made up of many microservices. This type of platform is essential in cloud computing, where applications often need to scale rapidly to meet demand.

The combination of microservices and containers simplifies the management of individual services, ensures fault isolation, enables seamless scaling, facilitates customization and rapid deployment, and promotes overall efficiency and reliability. This approach also lends itself to a continuous integration and continuous delivery (CI/CD) model, where updates can be frequently released with minimal impact on the application’s functionality.

Much like the containerization of LEGOs enhances your creations and the process by which you build them, pairing microservices with containers brings benefits to application architecture. The combination simplifies the management of individual services, ensures fault isolation, enables seamless scaling, facilitates customization and rapid deployment, and promotes overall efficiency and reliability. This approach also lends itself to a continuous delivery model, where updates can be frequently released with minimal impact on the application’s functionality.

- Microservices architecture allows for the **scaling of individual services**, while containers provide the ability to **easily spin up or down new instances** of those services as demand requires.
- Containers can be easily moved between environments, making it **simple to deploy microservices** across different infrastructure configurations.
- Containers provide **fault isolation**, so if one microservice fails, it doesn’t bring down the entire application.
- Microservices and containers can **help teams iterate faster** by allowing developers to work on smaller, more manageable services and deploy updates quickly.
- Containers allow for **better resource utilization**, as they can run multiple microservices on a single host.

## Redis Enterprise and containers

Redis Enterprise uses containers such as Kubernetes to facilitate the deployment, scaling, and management of containerized applications. This can be viewed as a managed service, where much of the complexity of managing a microservices application is handled by the platform. By running Redis Enterprise on Kubernetes, organizations can benefit from automatic scalability, persistent storage volumes, simplified database endpoint management, zero downtime upgrades, and secure containerized applications. Kubernetes provides a robust foundation to deploy Redis Enterprise clusters, offering dedicated functions like anti-affinity, persistent volumes, and StatefulSets for running share-nothing nodes.

To facilitate the management of Redis Enterprise clusters on Kubernetes, Redis developed the Redis Enterprise Operator, which automates the configuration and execution of many Kubernetes functions and uses Redis-specific controls to automate the operation of the data platform, including deployment patterns such as Active-Active databases. The Redis Enterprise Operator ensures that the Redis cluster and Kubernetes orchestration system work together seamlessly. Organizations using Kubernetes can leverage Redis’ expertise in running Redis-as-a-Service and rely on the Redis Enterprise Operator to handle the complex operations of the data platform.

Thinking back to our LEGO analogy, the Redis Enterprise Operator acts as a master blueprint that guides you through a project. Redis Enterprise Operator ensures that projects are built consistently and reliably without missing parts.

Organizations using Kubernetes in production environments can rely on Redis’ expertise in running Redis-as-a-Service, just as a novice LEGO builder can rely on the master builders’ instructions to create a complex structure.

Redis Enterprise on Kubernetes can be deployed on-premises using Red Hat OpenShift, any major cloud vendors, or a combination of them for a true hybrid and multicloud experience. It is also available on the Microsoft Azure Kubernetes Service (AKS) and Google Kubernetes Engine (GKE) marketplaces, enabling organizations to unify their cloud billing and deploy clusters in any region, including their local data center.

## Next Steps

Learn how Redis enhances messaging, storage, and caching, facilitates interservice communication, and synchronizes data across clusters. Download the e-Book [Redis Microservices for Dummies](/docs/redis-microservices-for-dummies/) now to unlock the full potential of microservices.
