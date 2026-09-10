---
title: "Utilizing Auto Tiering requires only 30% of the expensive DRAM storage previously used"
linkTitle: "Utilizing Auto Tiering requires only 30% of the expensive DRAM storage previously used"
url: "/customers/ekata/"
description: "Ekata’ proprietary Identity GraphTM solution makes an average of 150,000 to 200,000 calls per second to the company’s 3TB database—and can even surpass this number during peak hours. Being able to..."
group: "Security"
aliases:
- "/customers/ekata-3/"
lastmod: 2026-09-01
hidden: true
---

*updated 1 September 2026*

###### The Challenge

Ekata’ proprietary Identity GraphTM solution makes an average of 150,000 to 200,000 calls per second to the company’s 3TB database—and can even surpass this number during peak hours. Being able to handle this load without impacting performance is critical.

###### Solution

As Ekata expands its identity dataset around the world, Redis Cloud helps the company maintain less than 100ms end-to-end latency of its application—and provide a consistent end-user experience for its digital identity verification services for businesses and consumers.

###### Benefits

By leveraging Auto Tiering, Ekata requires only 30% of the expensive DRAM storage it previously used, saving hundreds of thousands of dollars in infrastructure investment costs each year.

> “We now only use 30% of the DRAM storage we previously used, with no sacrifice in latency. That equates to hundreds of thousands of dollars in infrastructure savings each year.”

Finding contact information is critical to many personal and business endeavors, and Ekata is often the first destination to look for this data. With more than 5 billion records searched by 35 million people a month, Ekata makes it easy for businesses and individuals to find contact information and run background checks.

Ekata’s [proprietary Identity GraphTM](https://www.whitepages.com/blog/whitepages-identity-graph/) [solution](https://www.whitepages.com/blog/whitepages-identity-graph/) helps consumers find old family and friends and learn more about their backgrounds, and enterprise businesses address fraud and identity verification. The solution makes on average 150,000 to 200,000 calls per second to the 3terabyte database and can even surpass this number during peak hours. 

“Our applications are extremely latency sensitive,” says Varun Kumar, Senior Vice President of Engineering at Ekata. “For example, when customers call our API for identity verification in the middle of an e-commerce purchase, it’s just one of many calls being made for that transaction. In this way, latency quickly multiplies and with our customer SLAs promising sub-hundred millisecond latency, there’s no room for error.”

As Ekata expands its identity dataset to achieve global reach, it realized it needed a better solution to handle this load without impacting performance and keeping operational costs low.

### Turning to Redis Cloud

Initially, Ekata housed the IDs to all that data in a key-value store on Amazon ElastiCache. Ekata tested the performance and reliability of other solutions, including MongoDB, Cassandra, Couchbase, Amazon ElastiCache, and others, but found that none could handle the full dataset size and still provide the single-digit latency that Redis could deliver. [Redis Cloud](https://redis.io/cloud/), chosen as a primary database, helps Ekata maintain sub-hundred millisecond end-to-end latency of its application and provide a consistent end-user experience of its digital identity verification services for businesses and consumers.

“A single name query can give rise to 100 additional calls as it works its way through our connected graph database, expanding into date of birth, relatives, phone numbers, addresses, and so on,” says Jason Frazier, Software Engineering Manager at Ekata. “At peak volumes, this easily translates into upwards of 200,000 calls to Redis per second.”

Auto Tiering stores hot values and keys in DRAM and cold values in cost-effective Flash-based SSDs. This breakthrough approach of tiering data access drastically reduces an application’s operational costs—without compromising performance. “We now only use 30% of the DRAM storage we previously used, with no sacrifice in latency,” Kumar says. “That equates to hundreds of thousands of dollars in infrastructure savings each year.”
