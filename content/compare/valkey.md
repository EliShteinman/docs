---
title: "Redis vs. Valkey"
linkTitle: "Redis vs. Valkey"
url: "/compare/valkey/"
description: "We’ve set the standard for in-memory performance. But how does Redis compare to Valkey? Learn why we continue to be the trusted choice for devs and enterprises around the world."
lastmod: 2026-09-01
---

*updated 1 September 2026*

## Fast data you can trust: Redis vs. Valkey

We’ve set the standard for in-memory performance. But how does Redis compare to Valkey? Learn why we continue to be the trusted choice for devs and enterprises around the world.

## Redis vs Redis Open Source vs Valkey 8

## Key Redis features and capabilities

### Active-active geo-distribution

Seamless global data distribution with strong consistency

### Management GUI

Easier management with our easy to use console

### High availability

99.999% uptime architecture with built-in replication and instant failover

### Multi-tenancy

Efficient resource utilization with support for multiple datastores in a single cluster

### Enhanced security

Enterprise-grade features like encryption, role-based access controls, and auditing

### Redis Insight

Visualize, optimize, and troubleshoot with Redis Insight

### Flex

Extend memory with SSDs to handle larger datasets cost-effectively

### Query and search

Scalable query and search capabilities make apps more dynamic and interactive

### Redis Data Integration

Automatically connect Redis with other data sources to move and sync data seamlessly across your architecture

## Frequently  asked questions

### What is Valkey?

Valkey is an in-memory data store that originated as a fork of Redis version 7.2.4. It shares the foundational key-value data storage principles of Redis but has begun to diverge with features contributed by AWS and experimental Remote Direct Memory Access (RDMA) support introduced in Valkey 8.0. These additions are aimed at improving throughput but remain in an early stage of development.

While Valkey benefits from open-source backing and a growing community, it does not yet match the maturity, extensive ecosystem, or enterprise-grade features that Redis provides. For organizations evaluating in-memory solutions, it’s important to weigh Valkey’s emerging capabilities against the proven reliability, scalability, and advanced functionality of Redis, particularly for demanding real-time applications.

### Does Valkey offer all of the features Redis provides?

No, Valkey does not offer the full range of features that Redis provides. While it shares foundational capabilities with Redis, it lacks advanced functionalities, such as the Redis Query Engine for powerful querying, secondary indexing, vector search and built-in time series support.

Additionally, Redis’s capabilities extend to Generative AI (GenAI) applications, enabling use cases like retrieval-augmented generation (RAG), AI-driven personalization, and advanced real-time analytics. These features make Redis a critical enabler for modern, AI-powered applications.

Redis Software (formerly Redis Enterprise) further extends the feature gap with enterprise-grade reliability, including automated scaling, high availability, advanced security features, and hybrid deployment options. These capabilities are essential for modern, real-time applications. While Valkey continues to evolve, its current capabilities remain more limited compared to Redis’s proven platform and future-focused innovations.

### How do performance and scalability compare between Redis and Valkey?

Redis Open Source and Valkey offer similar performance and scalability, sharing a common foundation. Since the fork, both projects have introduced performance improvements.

Valkey [implemented features](https://valkey.io/blog/valkey-8-0-0-rc1/) like asynchronous I/O threading and experimental RDMA support, aiming to enhance throughput and reduce latency.

Redis [introduced optimizations](/blog/redis-8-0-m02-the-fastest-redis-ever/) such as improved data structures and reduced latency, resulting in significant performance gains.

Redis Software (formerly Redis Enterprise) further enhances performance and scalability with enterprise-grade features, including [advanced clustering](https://redis.io/technology/redis-enterprise-cluster-architecture/) and a [zero-latency proxy](/blog/redis-enterprise-proxy/) with request pipelining and connection multiplexing. These capabilities ensure Redis Software delivers consistent, high performance at scale, even under demanding workloads, making it a preferred choice for mission-critical real-time applications.

### What kind of support is available for Redis and Valkey?

Redis offers a wide range of support options tailored to different needs. For Redis Open Source, support is available through the active Redis community, including forums (such as [StackOverflow](https://stackoverflow.com/questions/tagged/redis)), [GitHub](https://github.com/redis/redis), and [Discord](https://redis.io/learn/community/discord). Redis Software (formerly Redis Enterprise) provides enterprise-grade support, including 24/7 expert assistance, SLA-backed guarantees, and proactive monitoring. Customers also benefit from advanced resources such as detailed documentation, training, and the Redis University learning platform.

Valkey, as an open-source project, relies primarily on its community for support. While it has a growing base of contributors and discussions on [GitHub](https://github.com/valkey-io/valkey), it does not offer the enterprise-level support, SLAs, or advanced resources that Redis Software provides. Organizations requiring robust, production-grade support will find Redis Software to be the only suitable option.

### How do Redis and Valkey compare in terms of their ecosystems for development and operations?

Redis has a mature and extensive ecosystem, supported by a wide range of tools and integrations that streamline both development and operations. Developers can leverage popular client libraries for languages like Python, Java, Node.js, Go, StackExchange.Redis, and more, ensuring seamless integration into virtually any tech stack. Redis is also supported by major frameworks like Laravel, Spring Data Redis, Django, and .NET, as well as orchestration platforms like Kubernetes and Terraform. Developer tools like [Redis Insight](https://redis.io/insight/) provide powerful data modeling, visualization, and debugging capabilities, enabling efficient application development and optimization.

Additionally, Redis integrates seamlessly with AI development platforms like LangChain, LlamaIndex, Amazon Bedrock, NVIDIA NeMo, Relevance AI, and DocArray. These integrations enable advanced use cases like vector search, retrieval-augmented generation (RAG), semantic caching and AI-powered personalization, making Redis a key enabler for cutting-edge applications.

For operations, Redis integrates with observability platforms like Prometheus, Grafana, and Datadog, making monitoring and management straightforward. Redis Software (formerly Redis Enterprise) further enhances operational capabilities with features like cluster management and automated failover ensuring reliability and high performance in production environments.

Valkey, as a newer fork, has a smaller and less mature ecosystem. While it supports many of the same client libraries and basic integrations due to its Redis-based origins, its ecosystem lacks the breadth of operational tools, advanced integrations, and resources that Redis offers. For organizations seeking a well-established ecosystem that supports both development and production needs, Redis remains the clear leader.

### How should you choose between Redis and Valkey for your needs?

The choice between Redis and Valkey depends on your specific requirements and priorities. Redis is the more established and feature-rich option, offering a mature ecosystem, enterprise-grade reliability, and advanced capabilities such as built-in JSON support, secondary indexing, and the Redis Query Engine. If your use case demands high performance, scalability, robust operational tools, and extensive support options, Redis is likely the better choice—particularly for production-grade, real-time applications.

Valkey, on the other hand, may appeal to organizations looking for a simpler or more experimental solution that aligns with its community-driven development. However, its smaller ecosystem, limited operational tools, and less proven features may pose challenges for more complex or critical workloads.

For most organizations, Redis provides the flexibility, reliability, and advanced features needed to support both development and production environments, making it the preferred option for long-term success.

### What are the risks of choosing Valkey over Redis?

Choosing Valkey over Redis involves several risks, particularly for organizations with demanding or complex use cases. As a newer fork, Valkey lacks the maturity and proven track record of Redis, making it less suitable for mission-critical applications. Its smaller ecosystem means fewer tools, integrations, and community resources to support development and operations.

Valkey’s divergence from Redis also introduces uncertainty. Features and APIs may evolve in ways that are incompatible with Redis, potentially creating challenges for applications that rely on Redis functionality. Additionally, Valkey does not offer enterprise-grade support, SLAs, or robust operational features like automated failover, advanced clustering, or hybrid deployment models, which are crucial for production-grade environments.

For organizations prioritizing reliability, scalability, and long-term innovation, Redis remains the safer and more strategic choice.

### What is Redis Open Source?

Redis Open Source is the free and openly licensed version of Redis, starting with Redis 8.0. It is available under the GNU Affero General Public License v3 (**AGPLv3) **license, making it an official open source project. Both RSALv2 and SSPLv1 licenses are also available, but they are considered source-available licenses.

The [AGPL license](https://opensource.org/license/agpl-v3) permits free use, modification, and distribution of software over a network, with a provision that distributed, derivative works of the software including the source code are released under the same license. This provision, called the copyleft provision, ensures that modifications remain open and discourages cloud vendors from easily reselling Redis without our consent. Redis Open Source includes core Redis functionality along with features previously part of Redis Stack, such as JSON, time series, probabilistic data structures (Bloom, Cuckoo, top-k, etc.), and powerful search capabilities including full-text and vector search.

Redis Open Source is suitable for development, experimentation, and many production use cases, but does not include Redis Software’s operational tooling, Active-Active replication, Flex, or Redis Data Integration.
