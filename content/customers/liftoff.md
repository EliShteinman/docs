---
title: "Liftoff’s Ad Exchange Soars with Redis Cloud’s Low Latency"
linkTitle: "Liftoff’s Ad Exchange Soars with Redis Cloud’s Low Latency"
url: "/customers/liftoff/"
description: "Liftoff needed a high-availability, low-latency database that could meet the demands of thousands of app publishers and advertisers. The database had to be able to support a multi-cloud..."
group: "Advertising"
lastmod: 2026-09-01
hidden: true
---

*updated 1 September 2026*

###### Challenge

Liftoff needed a high-availability, low-latency database that could meet the demands of thousands of app publishers and advertisers. The database had to be able to support a multi-cloud architecture and cache an immense volume of data for fast, low-latency access.

###### Solution

Liftoff uses Redis Cloud to maintain data generated from billions of events and devices. This rapidly growing cache of key-value data allows Liftoff to deliver accurate, pertinent ad impressions.

###### Benefits

Liftoff’s popular ad tech services depend on Redis Cloud to complete more than 1 million operations per second. Redis technologies such as the Cuckoo Filter allow Liftoff to improve ad relevance and quality, improving ROI.

> "Reliability is very crucial for us! We maintain data on billions of devices and thousands of advertisers. Redis Cloud reduces the overhead required to deploy a database at scale and enables us to achieve stability within a short period of time."

Today’s mobile application developers face huge challenges due to the huge and incredibly diverse ecosystems. The challenge is further compounded by the ever-evolving privacy laws. Ultimately, the key to overcoming these challenges is to have effective ways to collect feedback from relevant customers and prospects, presenting them with ads that are most relevant and likely to resonate.

[Liftoff](https://liftoff.io/) has been at the forefront of changing how brands think about growing their app businesses. From being the first to develop an ROI-focused approach to optimizing users to finding new ways of helping mobile businesses get more from their apps, Liftoff’s goal has always been to help mobile app companies connect to their audiences.

[Redis Cloud](https://redis.io/cloud/) lies at the heart of Liftoff’s popular suite of ad tech solutions, where it maintains a cache of data generated from billions of events and devices. The cache stored in Redis serves as foundational data that allows Liftoff to improve ad relevance and quality which eventually lead to optimal ROI.

“Liftoff helps app owners and app publishers connect to their audiences by fueling the entire mobile app growth cycle across user acquisition, engagement, monetization, and analytics,” explains Surya Dharma, director of production engineering team for Liftoff’s [Direct Monetize and Vungle Exchange (DMX)](https://liftoff.io/products/). “Our goal is to connect people to the mobile apps and tools they love.”

### Surveying the landscape: Ad tech for dummies

When you are interacting with an app on your phone, at predetermined intervals the app developer wants to show an ad. This request is sent to Liftoff and an ad is returned in less than 300 milliseconds to be rendered on the app.

Liftoff receives millions of requests a second, and uses artificial intelligence (AI) to produce favorable results for both publishers and advertisers. A robust and high-performing ad-serving infrastructure is needed to achieve this.

Initially, Liftoff managed an on-prem version of Redis, but as the scale grew they began using Redis Cloud. “We needed a high-availability, low-latency database that could support a multi-cloud architecture,” Dharma recalls.

More recently, Liftoff has simplified its multi-cloud architecture to single-cloud architecture. Its popular ad tech services complete roughly over 1 million operations per second across its Redis Cloud instances, which requires the active management of a few terabytes of data.

“Reliability is very crucial for us!” Dharma says. “We maintain data that is used to serve billions of requests coming from billions of users and devices and thousands of app publishers and advertisers. Redis Cloud enabled us to reduce the overhead required to build database solutions at scale and achieve stability within a short period of time.”

### The cost of latency in mobile advertising

Liftoff will lose the impression if the request takes longer than the agreed-upon latency time. The cost of latency in mobile advertising is quite high, and the infrastructure choice is based on ensuring requests adhere to latency requirements.

High-quality contextual information available at low latency is essential to all of these use cases, and that’s where Redis Cloud shines. Liftoff stores contextual information in Redis Enterprise to be made readily available for low-latency access. The goal is to reduce wasted impressions and maximize the likelihood of a user seeing relevant ads.

Rocket Studio, one of the leading game developers in Southeast Asia, used Liftoff’s supply-side solution, Monetize, to increase its average revenue per daily active user (ARPDAU) by 38%. “We needed a solution that required less overhead, generated higher revenue, and improved the user experience by quickly filling all our ad requests,” said Thế Bảo Lương, Head of Monetization at Rocket Studio. “After we transitioned to in-app bidding [with Liftoff], we quickly saw a decrease in ads not showing to users. In fact, our fill rate jumped to 99%. A large part of this is due to reduced latency.”1

“In the ad tech space, latency is the key to everything,” Dharma emphasizes. “We need to be able to quickly determine the value of a bid request and if we should bid for it. Redis Cloud was the perfect choice because of the low latency in its key value lookup, which allows us to store and pull the necessary data that can be used by our machine learning models.”

### Leveraging probabilistic data structures

Liftoff uses the [Cuckoo filter](https://redis.io/probabilistic/) to look up key values quickly and accurately. A Cuckoo filter is a space-efficient probabilistic data structure that is used to test whether an element is a member of a set — in this case, whether a certain ad has been previously served or installed. A Cuckoo filter can also delete existing items in these sets, which helps Liftoff ensure that its records are always up to date. “It is a waste of an impression if we display ads on devices where the probability of conversion is low,” Dharma reiterates. “The Cuckoo filter allows us to achieve this functionality with low latency on a 1.5 TB database.”

This demonstrable efficiency is one of the key attributes of Liftoff’s success — and ongoing profitability.

“The conversion rate is very critical for us,” Dharma continues. “The fewer impressions it takes to result in a conversion, the better our margins will be. Our customers depend on us for accuracy. They want to know that they’re not wasting their money on an ad tech vendor that isn’t delivering ads correctly to the right people. Redis Cloud helps us efficiently serve billions of ad requests at low latency.”

### Simplifying deployments with AWS Marketplace

In addition to eliminating management overhead by running its instances in the cloud, Dharma appreciates the ease and flexibility of being able to purchase Redis Cloud through the [AWS Marketplace](https://redis.io/cloud-partners/aws/), which simplifies procurement, provisioning, and governance of many types of cloud-based software and services.

“Deploying our database in a cloud environment like AWS frees up our engineers from having to maintain and scale the Redis Enterprise infrastructure,” he says. “Our development team can move quickly since we don’t have to allocate resources to maintain the database. We can scale Redis Cloud very easily by subscribing to a higher AWS plan. The AWS environment optimizes things like shard distribution. It’s all taken care of, and Redis offers great support whenever we need it.”

1 [https://liftoff.io/resources/case-study/rocket-studio/](https://liftoff.io/resources/case-study/rocket-studio/)
