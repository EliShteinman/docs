---
title: "Downtime reduced 20% and application performance improved by nearly 90%"
linkTitle: "Downtime reduced 20% and application performance improved by nearly 90%"
url: "/customers/simility/"
description: "Simility processes several hundreds of millions of transactions each day for its cloud customers and billions of transactions every day in its on-premises deployments. Given the extremely high..."
group: "Financial services"
lastmod: 2025-09-12
hidden: true
mirrored: true
---

*updated 12 September 2025*

###### The Challenge

Simility processes several hundreds of millions of transactions each day for its cloud customers and billions of transactions every day in its on-premises deployments. Given the extremely high volume of transactions, the team was finding it difficult to meet end-user latency requirements.

###### Solution

Simility initially chose Redis Enterprise for caching, and found immediate relief for its throughput and latency challenges. Since Redis Enterprise scales easily with very little overhead, Simility’s IT team was able to effortlessly extend the solution to other use cases, including high speed transactions, job and queue management, and real-time data ingest.

###### Benefits

By using Redis Enterprise, Simility was able to cut IT costs by up to 30%, achieve up to 30% faster delivery of application functionality, reduce system downtime by up to 20%, and improve application performance by nearly 90%—all while reducing the need for specialized internal IT resources.

> “Before moving to Redis Enterprise, our IT team constantly worried about how to handle millions of connections and billions of transactions each day, and whether we would have to build and handle queues. We are now able to handle this huge workload without breaking a sweat.”

Fraud and abuse—including fake accounts, payment fraud, scams, fake reviews, and account takeovers—are constant challenges for today’s businesses. While there are many third-party solutions targeting only credit card fraud prevention, companies have to sacrifice their time and resources to build their own systems for holistic user and transaction fraud and abuse management.

That’s where Simility comes in. [Acquired by PayPal in 2018](https://www.reuters.com/article/us-simility-m-a-paypal-hldg/paypal-to-acquire-fraud-prevention-company-simility-for-120-million-idUSKBN1JH35Y), the Palo Alto-based company provides a highly scalable, cloud-based fraud prevention software solution that combines machine learning and human analysis to protect SMBs and enterprise clients from the most sophisticated types of fraud. The Simility solution empowers analysts to quickly adapt to fraudsters’ evolving tactics—all without having to write code.

Simility has grown rapidly since its founding in 2014, and its fraud detection systems process several hundreds of millions of transactions each day for its cloud customers, and billions of transactions every day in its on-premises deployments. Simility had been using DataStax for its main datastores, but given the extremely high volume of transactions, the IT team was finding it difficult to meet end-user latency requirements. Handling millions of connections became a challenge.

“While writing to the Cassandra database is fast, reads do not always show the latest data because Cassandra replicas are eventually consistent and slow,” explained Ravi Sandepudi, Head of Engineering at Simility.

### Choosing Redis Enterprise

Simility made the decision to use Redis Enterprise initially for caching and found immediate relief for its throughput and latency challenges. Since Redis Enterprise scales easily with very little overhead, Simility’s IT team was then able to extend the solution effortlessly to other use cases, including high speed transactions, job and queue management, and real-time data ingest.

Simility is now storing many different types of data in Redis Enterprise—some persistent and some transient. The application architecture includes several replicas of servers in containers, processing data in parallel. Since Simility utilizes real-time data from many sources, the application is subject to hundreds and thousands of connections. Redis Enterprise handles the company’s high throughput low latency needs gracefully. Simility also uses several of Redis’ signature features, including built-in key expiry features, TTL, and HyperLogLog for probabilistic estimates of counts.

“Using Redis Enterprise in our fraud-detection service was an excellent decision for our organization,” Sandepudi says. “It is enabling us to easily manage billions of transactions per day, keep pace with our exponential growth rate, and speed fraud detection for all of our clients.”

### Lower costs, higher performance

By using Redis Enterprise, Simility was able to cut IT costs by up to 30%, achieve up to 30% faster delivery of application functionality, reduce system downtime by up to 20%, and improve application performance by nearly 90%—all while reducing the need for specialized internal IT resources substantially.

“We really like the ability to seamlessly scale up and down using Redis Pack,” noted Sandepudi. “The built-in high availability reduces the amount of operational effort required in-house to run the solution, enabling our technical resources to focus on other, more strategic projects. Before moving to Redis Enterprise, our IT team constantly worried about how to handle millions of connections and billions of transactions each day, and whether we would have to build and handle queues. We are now able to handle this huge workload without breaking a sweat.”

As its clients’ data volumes and processing needs rapidly expand, Simility will continually increase its usage of Redis Enterprise. The team is now planning to move additional workloads from DataStax over to Redis Enterprise to be able to easily scale the environment to multiple sites and serve clients’ fraud detection needs faster and more efficiently.
