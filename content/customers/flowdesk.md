---
title: "Active-Active Redis Delivers Resiliency and High-Availability for Flowdesk’s Global Cryptocurrency Trading Platform"
linkTitle: "Active-Active Redis Delivers Resiliency and High-Availability for Flowdesk’s Global Cryptocurrency Trading Platform"
url: "/customers/flowdesk/"
description: "Flowdesk needs to facilitate sub-second access to order books that store financial data across the globe. This requires a high-availability, low-maintenance database service that integrates with..."
group: "Financial services"
lastmod: 2026-09-01
hidden: true
mirrored: true
---

*updated 1 September 2026*

###### The Challenge

Flowdesk needs to facilitate sub-second access to order books that store financial data across the globe. This requires a high-availability, low-maintenance database service that integrates with the Google Cloud ecosystem, supports Terraform, and enables VPC peering.

###### Solution

Redis Enterprise on Google Cloud maintains client trading sessions by caching data about orders, prices, and market movements while Active-Active Redis simplifies data storing and sharing across geographic regions.

###### Benefits

Using Redis Enterprise on Google Cloud, Flowdesk’s global financial infrastructure executes more than 1 million orders per day with sub-millisecond latency and zero downtime.

> “Flowdesk chose Redis Cloud because of its potential to sustain our growth. We haven’t been disappointed because we’ve been able to scale our services very economically.”

Founded in 2020, [Flowdesk](https://www.flowdesk.co/) is a financial technology (fintech) company that combines significant experience in traditional markets with acute knowledge of algorithmic trading and cryptocurrencies. Flowdesk’s global trading network integrates more than 100 centralized and decentralized exchanges into an advanced technology infrastructure that brings cutting-edge crypto services to a worldwide client base. This proprietary technology platform, based on [Redis Cloud](https://redis.io/cloud/), allows clients to trade and actively manage their own liquidity—a valuable capability for digital asset issuers who want to retain control of their assets.

Flowdesk’s initial financial services setup was based on a database infrastructure from Cockroach Labs, together with Google Cloud Memorystore. However, as its trading service grew, the Flowdesk infrastructure team realized they needed a more robust database and cache system to support real-time trading and market-making activity. They wanted a cloud-based database with a global footprint that could easily synchronize data among multiple international regions.

“As we evaluated the need to hyperscale our database infrastructure, we determined that we wanted a database-as-a-service option to accommodate the scalability of our systems and the rapid growth of our client base,” says Julien Tocci, head of infrastructure at Flowdesk. “Flowdesk chose Redis Cloud because of its potential to sustain our growth. We haven’t been disappointed because we’ve been able to scale our services very economically. With other database options, there’s a tendency to overscale, which costs more money.”

### High-availability architecture boosts data processing efficiency

Flowdesk’s low-latency trading infrastructure allows clients to execute trades from more than 70 token issuers. These financially savvy clients rely on Flowdesk for improving the market liquidity of their tokens while maintaining control over the assets in a safe and transparent environment. “Redis aggregates price data for a lot of exchanges,” Tocci says. “Currently, the infrastructure team uses 10 Redis Enterprise databases.”

To maximize availability and efficiency, Flowdesk stores Redis data in three regions: Japan, Europe, and the western United States. For each crypto exchange, a microservice aggregates data into a regional order book—an electronic list of buy and sell orders for a specific security or financial instrument.

Flowdesk uses order books to list the number of tokens that clients wish to bid on or offer at each price point. Redis maintains the state of these sessions by caching data about orders, prices, and market movements. Live data is generated as clients update their order books, which are routed via an open-source messaging queue.

The infrastructure team maintains rigorous standards for data availability among regions with the expectation of 99.999 percent uptime. “We’re managing two billion data points per day and passing two millions orders per day,” Tocci says. “The resiliency and availability of the Redis Enterprise system is very important for us. During the two years I’ve been at Flowdesk, we have had no downtime on the Redis Enterprise instances.”

### Easy integration with Google Cloud ecosystem maximizes options for the infrastructure team

Flowdesk hosts its technology infrastructure in Google Cloud. Redis Enterprise is a key component of a software environment that relies on Google Kubernetes Engine (GKE), a managed Kubernetes service for containers and container clusters, in conjunction with a BigQuery data lake for reporting and analytics.

Within this Google Cloud environment, Flowdesk has established a virtual private cloud (VPC)—a logically isolated, virtual network that permits servers to route traffic using private IP addresses. VPC peering allows Tocci and his team to define virtual networks of cloud resources. This allows Redis Enterprise instances to communicate with each other as if they were within the same network, and enables data to be transferred easily and securely.

[Microservices](https://redis.io/solutions/microservices/) that execute GKE and Redis Enterprise are spread across multiple geographic regions. According to Tocci, Redis Enterprise makes it easy to securely connect [Google Cloud](https://redis.io/cloud-partners/google/) applications to live data sources, and to use VPC peering to optimize performance and improve security. This versatile architecture gives Flowdesk a virtual private network for its cloud-based services that is global, scalable, and extremely flexible. “Within this private network, we have complete transparency between the Redis Enterprise instances and the production environment, along with very low latency,” he explains. “This is just one aspect of the ease of integration between Google Cloud and Redis Enterprise.”

Redis Enterprise automatically scales to utilize Google Cloud resources, making it easy to support usage peaks of 60,000 IOPS (inputs/outputs per second) during large market movements. Alerts on each Redis database track the volume of IOPS, and automatically request more infrastructure resources as necessary.

Tocci likes Redis Cloud’s architecture because it is self-managed and effortless. “Other than making the initial connections to the database, we don’t have to do anything on the infrastructure side to manage the Redis Enterprise environment,” he notes. “This allows us to focus on business needs rather than managing a database. Redis Cloud auto-scaling works as intended, so we can always count on it as we hyperscale our client base.”

### Active-Active Redis anchors global trading network

As Flowdesk expands globally, [Active-Active Redis](https://redis.io/active-active/) simplifies the process of storing and sharing data. Active-Active databases allow read and write operations to and from multiple copies of the database. Each write operation is distributed to all three regions, currently 30,000 writes per second. Regional apps connect to their own local Redis Enterprise instances, and the data is synchronized among regions. 

“We’ve been migrating customers from the Japan region to the Active-Active subscription, which spans all three regions,” Tocci says. “As we expand our multi-region clusters, Active-Active Redis is a perfect match for what we need.”

By distributing data across multiple regions of the world, Redis Enterprise reduces latency for nearby users, improving performance and user experience.

“Using Redis Enterprise in this context is a no-brainer,” Tocci says. “With VPC peering, it’s very easy to connect every region to a local Redis database. Data in the order books is always accessible, no matter which region users connect from.”

### Versatile, cloud-based architecture simplifies international expansion

Redis Cloud also works well with Terraform, an open-source tool that Flowdesk uses to configure, provision, and manage infrastructure as code. Using [Active-Active Redis Terraform](/blog/now-you-can-deploy-active-active-redis-databases-with-terraform/) resources, the infrastructure team can create, update, and delete databases in any region with a couple of clicks. Previously, managing data across regions was complicated. Now the team can easily define different database configurations in each region. For example, the northeast Asia instance might consume 50,000 IOPS, while the U.S. instance consumes 10,000 IOPS.

Flowdesk is in the process of expanding its financial services into two additional regions: Singapore and another in the United States. The company plans to launch new financial services in the futures market, which will significantly increase the size of its Redis Enterprise footprint. Despite rapid growth and rigorous customer demands, Tocci and his team are confident that Redis Enterprise will sustain their operation for many years to come.

“We’re expecting to have a lot more updates, and a lot more IOPS on the Redis Enterprise instances,” he concludes. “Redis offers great technology, and they’re quick to respond whenever we have questions. We are very happy with the technology and the support that we’ve received.”
