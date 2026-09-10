---
title: "Axis Bank’s mobile app revamp skyrockets UX satisfaction"
linkTitle: "Axis Bank’s mobile app revamp skyrockets UX satisfaction"
url: "/customers/axis-bank/"
description: "Axis Bank’s mobile app was supposed to let users see all of their latest account info, including the changes in the products they use and people they authorize to access their account. But when..."
group: "Financial services"
lastmod: 2025-10-21
hidden: true
---

*updated 21 October 2025*

###### The Challenge

Axis Bank’s mobile app was supposed to let users see all of their latest account info, including the changes in the products they use and people they authorize to access their account. But when customers were making these changes offline at the branch, they weren’t being reflected in the app—which had an infrastructure based on an outstanding traditional database at the time. As expected, this lack of reliable, real-time data led to customer complaints and dissatisfaction in UX.

### Redis as a Database

To fix this, Axis Bank created a new solution, known as Runtime Account Authorization. This innovative approach uses the capabilities of Redis, a real-time data platform, to deliver fast account visibility to more than six million daily users. By using Redis Axis’ mobile app can provide seamless, current information on customer relationships, accounts, and in-branch transactions. This slashes their response times, completely removes the need for manual intervention, and makes sure customers have access to accurate and timely account information.

### Redis Data Integration (RDI)

Axis used the Core Banking Table Replication feature to replicate the core banking tables to the local traditional database using Golden Gate Syncing. This is how they made sure the mobile banking channel had access to the most up-to-date customer relationship and product info.

Then, they developed an innovative capability that uses Redis as a fast database for their mobile banking app to read from. But they still needed a simple way to sync the data from the previous database. With RDI, Axis was able to simply ingest relevant records into Redis without complex code or expensive ETL tools. RDI continuously monitors the source tables for any changes and captures the changed data records immediately. These records are then processed using RDI, where filter conditions are applied to reject unwanted change records. Only the accepted records are ingested in near real-time and transformed into the appropriate hash schema in the target Redis DB.

> “At Axis Bank, prioritizing our customers’ needs is paramount, and integrating Redis has been instrumental. By leveraging Redis, we have achieved rapid data retrieval, improved performance, elevated user experience and enhanced stability for over 10 million daily users. This highlights our commitment to innovation and excellence in financial services. Our customers now enjoy a seamless and efficient digital banking experience, reaffirming our dedication to excellence.”

### High availability with Pacemaker

To make sure customer service was seamless, Axis used RDI to implement a high availability failover mechanism using primary-replica nodes, managed by Pacemaker. So even in the event of a node failure, the mobile banking channel is accessible and operational.

### Redis Query Engine and RDI

They also used Redis Pipelining to execute Redis Queries concurrently across nine different tables. This allows them to fetch customer data efficiently, resulting in faster response times and improved UX.

With RDI, Axis can instantly capture and process real-time changes in data from nine large traditional tables. This means they can provide an impressive 4.25x faster response time, compared to retrieving data directly from core banking tables—which is a huge improvement in system performance and overall efficiency.

### Axis Bank: Before and after

![Redis](/images/site-mirror/7e123d0d57b130d471f6a31f393ff8337f1369d0-3840x2160.webp)

### So what?

Axis is the perfect example of a customer-centered bank. They saw a problem and used Redis’ capabilities to improve system performance and reliability. Not only did they optimize their mobile banking UX—but they showed their commitment to meeting the changing needs of their customers. This shift has strengthened Axis’ position as a leader in the South Asian banking industry—showing how powerful it can be to innovate with customers in mind.
