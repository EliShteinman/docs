---
title: "Managing Microservices"
linkTitle: "Managing Microservices"
url: "/blog/managing-microservices/"
description: "Understand your microservice deployment options, including automations to save your team precious time and other practical advice for saving systems from unexpected failures."
date: 2023-05-31
blogCategories:
- "Uncategorized"
authors:
- "Redis  "
lastmod: 2025-03-27
hidden: true
---

*By Redis   · Published 31 May 2023 · updated 27 March 2025*

![Blog tile image](/images/blog/13d990f789287b75b37ec4fd401c68271cd711a4-772x550.webp)

**Understand your microservice deployment options, including automations to save your team precious time and other practical advice for saving systems from unexpected failures.**

After kicking things off with [Microservice Architecture Key Concepts](/blog/microservice-architecture-key-concepts/), followed by [The Principles of Designing Microservices](/blog/implementing-designing-microservices/), we continue our series on working with containerized microservice applications. Herein: a microservice management overview, covering deployment strategies, the importance of versioning, and configuration methods that keep teams from launching full redeployments for simple changes outside the codebase.

## Deployment strategies for microservices

You’re already sold on the benefits of converting your applications to use a microservices approach. However, questions arise as to how to make the transition. Consider these elements as you design the structure you expect to use for managing microservices and familiarize yourself with the concepts. It’ll save you a lot of confusion in the long run.

### Containers

Containers are pre-packaged software bundles comprised of all the components necessary to run software – which may mean anything from a standalone application to a database in an orchestration system environment. Containers support [infrastructure as code](https://learn.microsoft.com/en-us/devops/deliver/what-is-infrastructure-as-code) and are popular among DevOps teams. Containers’ operational efficiency features help by automating frequent commands, extending databases to include [Active-Active configuration](/blog/announcing-active-active-kubernetes/), and establishing automatic failover protocols for clusters or nodes that go offline. If each microservice operates in its own container, teams can launch their own releases and eliminate workflow dependencies on other teams.

> See how teams are using [operators to get the most out of Kubernetes](/blog/redis-enterprise-operator-for-kubernetes/).

### A/B testing

A/B testing is a means of testing multiple versions of a microservices application or service by infusing different variables into each version in a controlled manner – features, user interface differences, server configuration, whatever – to determine which elements generate the most success in performance terms – whatever success looks like in the appropriate domain. To gauge multiple approaches, web traffic is split between Test A and Test B to monitor how users respond and interact with new implementations or removed features of each isolated product being tested, using logs, traces, and monitoring.

> Learn [How to Build a Real-Time A/B Testing Tool Using Redis](/blog/how-to-build-a-real-time-a-b-testing-tool-using-redis/).

### Blue-green deployment

Blue-green deployment is a helpful strategy for migrating data, testing it, reacting to the changes with contained exposure, and reducing downtime. As explained in [Data Ingestion: 6 Ways to Speed Up Your Application](/blog/data-ingestion-speed-up-your-application/), blue-green deployment is a way to perform data migrations. With this premise, you ingest data in parallel. The application continues to use a “blue” legacy database while a new “green” cloud-native database is deployed in parallel for live-production testing and cut-over of this new data pipeline with the assurance of a rollback.

> There are lots of ways for DevOps teams to migrate data. [Redis Enterprise Cloud services ](/redis-enterprise-cloud/migrate/)are ready to help you unify hybrid and multicloud data layers.

### Canary releases

Historically, [miners used canaries as an early-warning system](https://www.smithsonianmag.com/smart-news/story-real-canary-coal-mine-180961570/) to let them know of low oxygen levels. A canary release has the same idea – to help identify problems before they become critical. The incremental deployment strategy tests a microservice release by distributing it to a small subset of users before unveiling it to an entire user base. This way, a development team can test user experience issues, hone in on defective code, and respond to honest user feedback that can then be implemented into a final product.

### Continuous integration and continuous deployment (CI/CD)

Microservices and their respective applications rarely stay stagnant. Updates, refreshes, and general coding tweaks have to be implemented occasionally.

As its name suggests, continuous integration (CI) is an automated process that deploys new code into an existing deployment environment. For CI to benefit developers and DevOps teams, it needs a solid testing and deployment automation strategy to ensure a fast turnaround of production-quality releases.

Continuous deployment (CD) typically promotes new deployments into a production environment after undergoing automated tests.

> Learn how the [Redis Developer Hub Expands to Support the Needs of DevOps Teams](/blog/redis-developer-hub-expansion/) by making databases a part of the CI/CD pipeline.

## Configuration management of microservices

Configuration management ensures that each microservice’s corresponding configuration files are correct and immediately accessible. Configuration management keeps developers and IT from changing the application code when a microservice needs modifications. Keeping the code intact and merely updating configuration files also saves teams from having to initiate a rebuild of the application.

[Microservice architecture](/blog/microservice-architecture-key-concepts/) is a dynamic framework that encapsulates components of a workflow or process, typically focusing on specific business areas. For example, a retail application encompasses essential functionalities such as shopping cart management, order processing, payment handling, checkout processes, product catalogs, seamless integration with back-end finance and accounting systems, and robust customer service support.

In setting up microservices architecture, DevOps is tasked with applying the guidelines that make a microservice function a certain way in the overall application infrastructure. These settings can include database connection details, API endpoints, logging levels, runtime configurations, and feature toggles, also known as “feature flags.”

The proper configuration values for a microservice, often stored ins JSON or YAML files, depend on the application’s security requirements, the database it runs on, its state in the development cycle, and its deployment environment, among other factors. Besides JSON and YAML files, configuration sources are also found within the parameters set in the command-line arguments.

### Centralized configuration management

A centralized configuration store is a server or repository from which one can manage all microservices’ configurations, regardless of their environments. The configuration features from one microservice to the other can vary greatly, and juggling such a disparate set of parameters and secrets without a globally available single record “[can make things over-complicated very quickly](https://www.codemotion.com/magazine/devops/cloud/centralized-configuration-management/).” Apart from being a dedicated hub for configuration, it simplifies and accelerates the uptime process for new releases.

### Dynamic configuration updates

Dynamic configuration management (DCM) addresses configuration changes in an application without initiating a redeployment. Touching the application code triggers the automatic need for running a full regression suite with all functional and integration tests.

These pre-banked tests are typically executed via a centralized configuration store.

### Security and secrets management

[Secrets share sensitive data](/blog/kubernetes-secret/) such as passwords, keys, credentials, and authentication tokens. Secrets keep secret data separated from an application’s code, allowing for the management of secrets without needing code changes.

In Kubernetes, secrets are “by default, stored unencrypted in the API server’s underlying data store (etcd). Anyone with API access can retrieve or modify a Secret, and so can anyone with access to etcd. Additionally, anyone who is authorized to create a Pod in a namespace can use that access to read any Secret in that namespace; this includes indirect access such as the ability to create a Deployment.”

To maintain secure user authentication, development teams may use an external secrets operator, such as the HashiCorp Vault, to maintain secure user authentication. Secrets operators authorize all access before sharing sensitive information.

### Versioning and change management

Versioning is a way for DevOps teams to track the historical configuration changes made to a microservice’s attributes, including “key-value pairs, software bill of material (SBOMs), common vulnerabilities and exposures (CVEs), licenses, swagger details, consuming applications, and deployment metadata.”

That helps DevOps to verify that all namespaces and clusters have the versioned release they’re supposed to be operating with and allows quick implementation of configuration rollbacks when previously used functions or settings are required. As a result, anyone working on an organization’s microservices can accommodate new features, bug fixes, and other changes.

## Service mesh, service discovery, and load balancing

Service mesh, service discovery, and load balancing are all related concepts that work together to enhance microservices’ observability and reliability..

### Service mesh

A service mesh is a pattern inserted in the infrastructure layer that controls the delivery of service-to-service messaging. In the case of large-scale applications with many growing microservices, a service mesh keeps requests clear and streamlined and routes pertinent information to the corresponding service while keeping the application performance robust.

A service mesh consists of a data plane and a control plane. The difference between both planes is that “[the control plane decides how data is managed, routed, and processed](https://www.snaplogic.com/blog/data-plane-vs-control-plane-whats-the-difference), while the data plane is responsible for the actual moving of data.” Ethernet, Wi-Fi, cellular, and satellite networks are examples of data planes. The control plane that tracks the multiple services is also known as “service discovery.”

### Service discovery

Service discovery facilitates service-to-service communication by highlighting available instances ready for communication without configuration changes. A service registry storing the IP addresses, port, and health status of available services becomes a centralized hub for discovering which services are ready for communication.

### Load balancing

In any networking scenario, load balancing is the process of distributing workloads and computing resources across servers, splitting up the work to enable better resource utilization, and system response time.

A load balancer is one of the built-in capabilities of a service mesh. It uses algorithms to decide where to route traffic, dynamically distributing traffic without the need for external load-balancing devices on other networks. When a request reaches a microservice, that request is intercepted and relegated to the appropriate instance. Which instance handles the traffic is essentially decided by the service discovery or control plane, using tests and health checks.

## Autoscaling microservices

Autoscaling uses predefined system thresholds to scale a service up or scale down. Suppose a site is expecting a massive surge in traffic because of a sale, a popular sporting event, or due to a highly-anticipated new product release. In that case, autoscaling includes as many instances as necessary to fulfill the demand and to keep the microservices based application running at peak performance.

## Handling microservice failures

System failures sometimes occur, and it’s vitally important to prepare for the possibility of a failed node or cluster.

Anticipate these issues at the implementation level. In [The Principles of Designing Microservices](/blog/implementing-designing-microservices/), we briefly cover the importance of designing microservices for resiliency with tactics such as the [Circuit Breaker pattern](https://learn.microsoft.com/en-us/azure/architecture/patterns/circuit-breaker), introducing [fault-tolerant patterns](https://itnext.io/5-patterns-to-make-your-microservice-fault-tolerant-f3a1c73547b3), and implementing asynchronous communication with an event-driven message broker to promote eventual consistency.

For more on eventual consistency, read [Database Consistency Explained](/blog/database-consistency/).

Want to find more information on microservices? Discover our dedicated [microservices playlist](https://www.youtube.com/playlist?list=PL83Wfqi-zYZFJfj6bOxP-TG-sQc-t64P8) on our Youtube channel.
