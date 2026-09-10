---
title: "Blip powers global messaging platform with Azure Managed Redis"
linkTitle: "Blip powers global messaging platform with Azure Managed Redis"
url: "/customers/blip/"
description: "Blip processes nearly 1.5 billion messages each month across WhatsApp, Instagram, and Messenger. Every conversation depends on fast, consistent coordination behind the scenes."
group: "Tech (digital natives)"
lastmod: 2026-04-28
hidden: true
---

*updated 28 April 2026*

### Scaling real-time orchestration at global scale

Blip processes nearly 1.5 billion messages each month across WhatsApp, Instagram, and Messenger. Every conversation depends on fast, consistent coordination behind the scenes.

As Blip expanded internationally, Redis became an important component for its conversational platform. A central orchestration service manages metadata, session state, and message routing across 20+ internal apps. With growing traffic and additional regions, performance differences between environments became more visible. Latency behavior varied under load, and scaling predictably across regions became more difficult.

Blip needed a unified platform that could deliver predictable latency, stable tail performance, and high availability at sustained throughput. Uptime requirements were strict, and small latency variations began to compound across distributed services. Consistency, not just raw speed, became the priority.

### Redis as the backbone of real-time messaging

Redis manages active session state, high-frequency metadata reads, and the state transitions required for complex, multi-step conversations across messaging channels.

Blip standardized on Azure Managed Redis to support its most demanding apps. Each core app runs on 11 Redis clusters, each managing approximately 24 GB of data. Each Redis service sustains around 100,000 operations per second, resulting in ~1 million operations per second per app.

Redis is used to cache:

- **Client session data: **Preserves active user context across the Blip platform and messaging channels.
- **Metadata required for fast reads: **Supports high-frequency access patterns needed to orchestrate requests across internal services.
- **State needed to coordinate complex, multi-step conversations: **Enables orchestration server to manage real-time interactions across chatbots, analytics, and other platform tools.

![Redis Case Study Blip Diagram](/images/site-mirror/c058c414fd5cdc361e3b69dfc76e8a64800801a6-842x474.svg)

This architecture enables near-instant access to user context and ensures real-time message delivery across multiple regions and channels. At this scale, latency distribution matters as much as average response time. Any variance propagates through dependent services and directly affects message delivery timing.

### Latency distribution under load

Standardizing on Azure Managed Redis simplified the architecture, but the most visible impact was performance. After migrating 132 services across 11 apps and 12 global clusters, Blip benchmarked production workloads.

In the main apps—Server, Gateways, Billing, and Active Campaign—average latency dropped from 1.5 ms on its legacy platform and 1 ms on Azure Cache to below 0.2 ms on Azure Managed Redis. On the Server, average service time decreased from 1 ms to 0.09 ms. Gateway services performing heavier routing logic dropped from over 2 ms to 0.244 ms.

Tail latency improved significantly. Blip observed a 73% improvement in P99 latency compared to its legacy platform while maintaining the same memory configuration. This reduced variability across chained service calls and stabilized response times across regions.

Under overload conditions, the performance difference remained measurable. When comparing Azure Cache P2 at 13 GB with Azure Managed Redis Compute X10 at 12 GB, average latency decreased from 1.19 ms to 0.44 ms while sustaining peak demand.

These results were observed under live production traffic. The improvements translated directly into tighter coordination between services and more consistent message routing across global deployments.

### High availability & scalability with Azure Managed Redis

Azure Managed Redis provides built-in high availability with automatic failover, aligning with Blip’s active–passive disaster recovery strategy, which mirrors approaches already used for other core services such as SQL Server.

Blip’s architecture allows the team to balance resilience with operational efficiency without maintaining fully active secondary clusters.

> Any issue with Redis has a direct impact on our platform, our clients, and ultimately the customers they serve. That’s why Redis is truly mission critical for us.

In production, this design is validated under sustained load. The platform regularly absorbs traffic peaks exceeding 350,000 requests per second without manual scaling events or emergency infrastructure changes. Previous environments required reactive intervention during prolonged spikes. With Azure Managed Redis, peak load is handled within the standard operating model, and latency distribution remains stable.

Blip runs Redis-backed workloads across Brazil, Europe, the United States, and the Middle East, supporting multi-tenant clusters deployed across four continents. Performance remains consistent across regions, even during overload conditions.

### Reducing cost & operational complexity

By consolidating Redis workloads onto Azure Managed Redis, Blip significantly reduced total cost of ownership while simplifying operations. This reduced operational overhead associated with maintaining separate tuning strategies, scaling procedures, and failure handling models across regions. Engineering effort shifted away from reactive infrastructure management toward platform development.

Cost savings were measurable, but the primary outcome was improved performance consistency and reduced operational variability across global workloads.

### A modern foundation for real-time workloads

By standardizing on Azure Managed Redis, Blip has established a resilient foundation for real-time messaging today, while gaining operational headroom for future platform evolution.

With lower average latency, tighter P99 distribution, and stable performance at sustained throughput exceeding 350,000 requests per second, the platform now operates with greater headroom. Blip is well positioned to explore additional Redis capabilities over time, including advanced data models and caching strategies, as its conversational workloads and use cases continue to evolve.
