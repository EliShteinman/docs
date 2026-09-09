---
title: "Plivo optimizes infrastructure and performance with Active-Active Redis"
linkTitle: "Plivo optimizes infrastructure and performance with Active-Active Redis"
url: "/customers/plivo/"
description: "Plivo’s streaming microservices architecture supports a large volume of small, high-frequency data writes. If an Amazon ElastiCache region were ever to fail, it could not keep up with the volume..."
lastmod: 2026-01-29
hidden: true
---

*updated 29 January 2026*

###### Challenge

Plivo’s streaming microservices architecture supports a large volume of small, high-frequency data writes. If an Amazon ElastiCache region were ever to fail, it could not keep up with the volume and maintain data consistency across regions. Plivo’s engineers needed to build a custom failover.

###### Solution

Plivo chose Redis Cloud after tests indicated it could handle the requirements of their Voice API platform. Because they were migrating to a managed solution from the company behind open source Redis, almost no code changes were required. The initial migration succeeded in minutes, and the complete move happened within a month.

###### Benefits

Data integrity improved immediately. In addition, Plivo’s engineers were able to uncover additional benefits to optimize the service across regions. Active-Active, an exclusive Redis Enterprise capability, allows them to make the most effective use of their infrastructure across all regions to maximize the investments made throughout their architecture.

> "We wanted to ensure we could meet uptime and scalability requirements through Active-Active Redis. We tried to simulate these capabilities with Amazon ElastiCache, but realized this was something we didn’t want to solve ourselves. We chose Redis Cloud, which delivered this functionality within a fully managed solution."

Not all databases can meet the performance requirements of every use case. For [Plivo](https://www.plivo.com/), a leading cloud-based communications platform (CPaaS), which helps businesses engage and communicate with their customers, low-latency reads and writes are critical to their Voice API platform.

“Postgres and other relational database models do not do a good job in handling high-frequency data writes,” says Manish Chand Kaushik, Software Development Engineer and Architect, Voice Platform for Plivo. “We migrated all our caching use cases to Redis, because relational databases have proven to be suboptimal for our applications.”

Plivo’s Voice API team turned to Redis for its low-latency performance, especially for data writes. Plivo’s use cases include rate limiting calls within a given time period, queuing call status (ringing, executed, hang-up, et al.), and maintaining call queues by region (with only 1-2 milliseconds latency). The data is stored as hashes and keys, and sorted sets are used for rate limiting.

Because Plivo tries to leverage managed services wherever possible, they initially deployed Amazon ElastiCache where they needed low-latency performance in their systems. This proved not to be the ideal managed Redis service for Plivo, as ElastiCache doesn’t provide fallback as an out-of-the-box capability if a failure in a region occurs.

### Seamless Migration to a Geo-Distributed Database

According to Rajat Dwivedi, Director, API Engineering, “We wanted to ensure we could meet uptime and scalability requirements through [Active-Active Redis](https://redis.io/active-active/). We tried to simulate these capabilities with Amazon ElastiCache, but realized this is something we didn’t want to solve ourselves. We chose Redis Cloud, which delivered this functionality within a fully managed solution.”

Because the initial data Plivo was migrating was 24 hours old, the migration was set up with Amazon ElastiCache as the primary system and Redis Cloud as the secondary, and all writes were being made to both systems. If anything went wrong the process could be rolled back to the primary and restarted. Plivo made the move within a planned maintenance window and called out that writes could be missed in this window, so they could easily initiate a rollback if there was an error within the process.

This methodical planning ended up being prophetic when a small issue occurred where an old set of data was overlooked and caused a data stream disconnect. Plivo’s engineers saw the issue, cleared the system, and rolled back to restart the process in only eight minutes.

Ultimately the migration to Redis Cloud was completed in approximately a month.

### Cross-Region Optimization and Fault-Tolerance

“Active-Active Redis has helped us protect latency across regions, but we found added value in the way it optimizes system infrastructure. There is never a situation in which we are wasting resources, and we never underutilize our assets,” Kaushik says.

Plivo engineers try to fully utilize all system resources and components. With Active-Active Redis, even with extraordinary linear scalability, not only is everything working as it should, but the entire environment is also running at peak efficiency.

Deployment of Active-Active Redis was almost mundane. Redis’ Solution Architects helped Plivo engineers in the initial phase with the help of clear, well-written documentation. And the benefits came almost immediately.

Shortly after deployment, one entire region suffered a communication disruption. No major alarms went off because the system simply reallocated resources in an intelligent way so that Plivo’s customers saw little if any impact. There were no major performance issues for the entire hour that region was down.

Kaushik notes what was remarkable about the disruption, “Active-Active Redis just works. Our system kept working, customers noticed little if any connectivity problems and we didn’t have to do anything in the way of damage control. The entire 60-minute episode was almost a non-event.”

### Peace of Mind Without Managing a Data Platform

The first real test of Redis Cloud proved its value and provided Plivo peace of mind because so much of their data needs to be synchronized for complex use cases across their distributed architecture.

Dwivedi notes that the roadmap for further migration of Plivo systems to Redis Cloud are planned, with one already underway for a financial data system. Assessments throughout the year will be made to migrate most of their caching and low-latency use cases “because we can confidently go with Active-Active Redis.”
