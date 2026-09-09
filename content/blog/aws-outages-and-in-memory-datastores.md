---
title: "AWS Outages and In-Memory Datastores"
linkTitle: "AWS Outages and In-Memory Datastores"
url: "/blog/aws-outages-and-in-memory-datastores/"
description: "For the second time during June 2012, the AWS us-east-1 region failed, this time due to a power outage caused by extreme weather conditions, according to Amazon. For those of you who use an in-..."
date: 2012-07-02
blogCategories:
- "Tech"
authors:
- "Redis  "
lastmod: 2025-03-04
hidden: true
---

*By Redis   · Published 2 July 2012 · updated 4 March 2025*

![Blog tile image](/images/blog/4231a3252493fa7d33258cf05692ac82d174e069-550x400.webp)

For the second time during June 2012, the AWS us-east-1 region failed, this time due to a power outage caused by extreme weather conditions, according to Amazon. For those of you who use an in-memory data store like Memcached or a service like AWS’ ElastiCache, the result of such power outage is **losing your entire Memcached dataset**. The implications are that all database queries are now directed to your main database, which most times is not built for such load. This means your app may suffer dramatic performance degradation and in extreme cases may even crash. Recovering from a Memcached failure can take days and sometimes weeks. Furthermore, many of today’s applications and dev-platforms like Magento, WordPress, Drupal and Django store users’ sessions in Memcached. Losing such data typically means forcing all of your users to immediately logout, and if you are running an ecommerce site, flushing all your users’ shopping carts. Both events may have adverse effect on your business. In Garantia Data, we took a different approach towards operating in-memory NoSQL data stores like Memcached & Redis, making sure a dataset is never lost, while maintaining the high-throughput and low-latency of these extremely fast platforms. Our built-in replication and auto-failover processes helped us to survive the June 15 AWS outage with zero downtime! – switching in-memory datasets from all the failed nodes to the healthy nodes of our cluster in the affected zone. Although replication is a very effective way to recover from a node failure event, the latest June 30 AWS power outage affected multiple cluster nodes of our service simultaneously. However, thanks to our robust data-persistence mechanism we were able to recover from this failure without damage. Our users maintained replicas of their datasets in persistent storage (EBS) using either Append Only File (AOF) or Snapshot methods. By the way, this capability too comes without any application performance degradation. We also allowed daily S3 backups, which proved to be very effective in case of impaired EBS volumes, as occurred in the latest AWS outage. Bottom line – our robust data persistence mechanisms enabled us to successfully recover ALL of our users’ datasets from the June 30 AWS outage ! Future improvements:

- We are working on adding automation tools to our recovery process in order to shorten the recovery time from a fatal zone failure.
- We plan to provide multi-zone replication capability in the coming months. This will allow our users to access their in-memory resources from multiple zones of an AWS region, in a highly-available and consistent manner.
