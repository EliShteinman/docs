---
title: "iFood relies on Redis Cloud as foundation for ML operations"
linkTitle: "iFood relies on Redis Cloud as foundation for ML operations"
url: "/customers/ifood/"
description: "Watch the video"
group: "E-Commerce"
lastmod: 2026-09-01
hidden: true
mirrored: true
---

*updated 1 September 2026*

###### Watch the case study video

[Watch the video](https://www.youtube.com/watch?v=OXNTzhPnJU8)

###### The Challenge

For iFood’s popular food ordering and delivery applications, success is a by-product of performance: iFood’s machine learning (ML) models must be able to process data quickly to reduce costs, increase revenue, and positively influence user behavior during real-time interactions.

###### Solution

To ensure consistency for ML engineers and create an optimal experience for users, iFood uses Redis Cloud on AWS at the foundation of its rapidly evolving ML feature store. Redis on Flash maximizes data-processing throughput while reducing overall data storage costs.

###### Benefits

iFood’s Redis-based infrastructure delivers sub-millisecond performance for ML operations, powering a highly efficient microservices architecture that optimizes the user experience, allows for massive scalability, and enables rapid corporate growth.

> “We have a small team, so we don’t want to get bogged down with infrastructure management. Redis Cloud really helps us with this. It saves us a lot of money on infrastructure.”

The COVID-19 pandemic presented unique opportunities for e-commerce firms, especially online delivery services that were prepared to handle an escalating volume of orders. At iFood, one of the largest food delivery companies in Latin America, the technology team shifted into high gear as millions of new users began relying on its service, and thousands of new restaurants joined its growing platform. In the first three months of 2021 alone, more than 30,000 new restaurants, grocery stores, and convenience stores signed up to deliver food through iFood’s digital platform, and its monthly orders surged by tens of millions of deliveries.1

Despite this surge in business volume, and the rising revenue that accompanied it, iFood held fast to the values that had propelled the rapidly growing company to success. “It’s not just about putting in a food order,” sums up Daniel Galinkin, Head of Machine Learning Engineering at iFood. “It’s about providing an optimal experience for our customers. That’s one of the things that distinguishes our company, and keeps people coming back.”

### Concierge Service: Using AI to Optimize the User Experience

Today, iFood serves a network of about 320,000 restaurants, and aims to increase its base of 30,000 supermarkets.2 It also recently added delivery for pharmacies and liquor stores. To fulfill these lofty growth objectives, Daniel Galinkin and the other members of iFood’s Data&AI team use artificial intelligence (AI) and machine learning to better understand users, such as tracking how many orders have they placed in the last month, which restaurants and stores they prefer, their chosen payment mechanisms, and many other variables. These facts are maintained as *features*—unique attributes and variables that serve as inputs to iFood’s ML models.

To ensure an optimal user experience, iFood must be able to run these models as orders are placed to influence the split-second decisions that customers make. “A single feature may incorporate several business rules, each of which is constantly evolving,” Galinkin explains. “All that logic and all those definitions must be consistently shared among applications, or a user may be treated differently at different places in the app. If you don’t centralize this knowledge in a feature store, the team efforts become fragmented.”

iFood has more than 100 ML models in production. Most of these models help bring in revenue, such as the ones that power its recommendation engine (which helps users decide which restaurants to consider and what food to order). Other models determine which types of vouchers and coupons to present to users at each navigational juncture. Still other models help iFood reduce costs by detecting fraudulent transactions such as chargebacks, in which users place orders, receive those orders, and then attempt to receive a refund on their credit cards.

“Our business succeeds to the extent that we can deliver ML features quickly,” Galinkin says. “Our ML models deliver multiple recommendations during a single user session. We need a high-performance database in order to handle these read and write operations. Redis Cloud solves this issue very well for us.”

### Secret Sauce: Redis Cloud Encourages Consistency for ML Platform Team

A [feature store](https://redis.io/solutions/feature-store/) is a database management system that is optimized to store and serve feature data in a key-value database. Feature stores let engineers reuse ML features across data discovery, training, production, and other phases of the data science lifecycle.

To ensure consistency among developers and create an optimal experience for users, iFood uses Redis Cloud on AWS as the foundation of its rapidly evolving feature store. “One of the main aspects of having a feature store is shared knowledge,” Galinkin says. “Redis Cloud helps our team collaborate. It encourages reusability so we don’t have to ‘invent the wheel’ multiple times.”

Successful machine learning initiatives depend on getting the right data at the right time to the correct models. [Redis Cloud](https://redis.io/cloud/) makes feature data available to dozens of models in production, and it includes essential capabilities such as a registry, data pipeline, and monitoring tools to streamline feature engineering activities. This allows iFood’s Data & AI team to search, reuse, and serve features in production, at scale. “A feature store allows you to implement knowledge once and share the calculations multiple times,” Galinkin adds. 

Galinkin and his team were positively influenced by their fellow ML engineers at DoorDash, another popular food fulfillment and delivery service that uses Redis for its feature store. They especially liked the open, standards-based architecture of the Redis environment, which works well with Databricks, Amazon SageMaker, Terraform, Apache Airflow, Python, and other key software tools that help automate their efforts.

### Recipe for Success: Redis on Flash Powers Feature Engineering Workloads

Back in 2020, as business escalated during the Covid pandemic, iFood’s ML Platform team started building a feature store from scratch. At the time, there weren’t any packaged solutions that suited them, either commercial or open source. They initially ran their feature store on Amazon ElastiCache, however over time, it became too expensive to put all of their feature data into memory on AWS. “ElastiCache was relatively stable but really expensive,” Galinkin admits. “When we heard about the Redis on Flash offering, we decided to take a closer look.”

Redis worked closely with iFood to implement [Redis on Flash](https://redis.io/auto-tiering/) and integrate the fully managed service into iFood’s microservices architecture. “We had to migrate a huge volume of data, but the transition was successful,” Galinkin continues. “We’ve never closed a deal and done a migration this fast.”

Today, whenever a user initiates an action, such as querying a restaurant or placing an order, it triggers several microservices. According to Galinkin, the combined latency for all those microservices can’t exceed 200 milliseconds. “Every millisecond counts,” he emphasizes, “so we conducted some benchmarks. Amazon DynamoDB offers somewhere around 10 millisecond per Read operation. Redis Cloud offers less than one millisecond per Read operation. It makes a difference. That’s one of the main drivers that led us to Redis Cloud.”

The key to this exceptional performance is the way Redis on Flash [orchestrates data between the DRAM and Flash Storage tiers](https://redis.io/auto-tiering/). Frequently accessed or “hot” data resides in the fast DRAM tier, along with the keys and the Redis dictionary. Less frequently accessed “cold” data stays in the local Flash storage tier. “Redis on Flash makes it seamless for the user,” Galinkin reports. “We simply issue requests and Redis delivers the data. It’s transparent for the client, and it’s really, really fast—with sub-millisecond performance. Plus it’s a lot cheaper [than our previous solution].”

iFood was also influenced by the exceptional stability and reliability of Redis Cloud, which utilizes a shared-nothing cluster architecture to automate failover operations at the process level, for individual nodes, and across infrastructure availability zones. iFood also uses [Redis Cloud as a cache layer](https://redis.io/solutions/caching/) to store the results of queries, so that repeated database requests can be served instantly. 

“Fault tolerance is really important for our feature store application, and Redis Cloud works really well as our main database as well,” Galinkin concludes. “We have a small team, so we don’t want to get bogged down with infrastructure management. Redis Cloud really helps us with this. It saves us a lot of money on infrastructure.”

1 “Brazilian food tech’s behemoth iFood delivers 60 million monthly orders amid the pandemic,” Latin American Business Stories (LABS), April 12, 2021.

2 “Brazil Delivery App IFood Focusing on Growth,” U.S. News and World Report, Sept. 1, 2022.
