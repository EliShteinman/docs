---
title: "How Inovonics Uses Redis Enterprise to Drive Real-time IoT Data Analytics"
linkTitle: "How Inovonics Uses Redis Enterprise to Drive Real-time IoT Data Analytics"
url: "/blog/inovonics-uses-redis-enterprise-drive-real-time-iot-data-analytics/"
description: "Over the past 30 years, Inovonics has risen to become a leading provider of industrial wireless IoT technology. We’ve deployed tens of millions of devices in challenging commercial environments..."
date: 2019-04-17
blogCategories:
- "Guest Blogs"
authors:
- "Lalit Pandit"
lastmod: 2025-03-04
hidden: true
---

*By Lalit Pandit, Software Development Manager · Published 17 April 2019 · updated 4 March 2025*

![Blog tile image](/images/site-mirror/af8cd92e892e69cbe569f72942c141bfc9cf8b7f-800x800.webp)

Over the past 30 years, Inovonics has risen to become a leading provider of industrial wireless IoT technology. We’ve deployed tens of millions of devices in challenging commercial environments across a wide variety of critical applications—from life safety to intrusion alerting to multi-family submetering.

And while we work tirelessly every single day to improve the reliability and ingenuity of our wireless infrastructure and IoT solutions, we’ve come to realize that we have an equally compelling product to offer… data!

The massive—and unique—sets of data collected by our wireless devices and sensors have tremendous application. For example, we can:

- Analyze anomalies in energy usage patterns to predict maintenance needs for our submetering customers
- Aggregate data from intrusion detection systems to determine periods of increased break-in risk or illuminate trending illegal entry methods
- Analyze daily living patterns for senior citizens under senior care and alert the facility by identifying any abnormalities for any emergency help.

### Transitioning from Desktop to Cloud

Our previous generation system was based on desktop applications connecting to a gateway directly at the customer site (i.e. no cloud). This gateway also served as a data repository based on a relational database for the IoT devices. Customers needed a desktop computer to access the data and it was very challenging for us as a vendor to detect issues with the end point(remote devices), and maintain and troubleshoot the gateway remotely.

When we designed the new generation of our gateway and application, our goal was to consolidate all data from IoT devices in a central repository—and to future proof the architecture with respect to performance and reliability. Providing ubiquitous access to the data and insights in markets such as life safety was also a key requirement. These non-negotiables, along with the desire to keep operational footprint costs as low as possible, led us to build our new generation system in the cloud.

![](/images/site-mirror/4797bf23e80f03e5767e395608461e38587a0432-1754x434.webp)

Today, we’re running Redis Enterprise Cloud Pro, a fully-automated database-as-a-service, on Google Cloud Platform (GCP). Redis Enterprise acts as a data ingest, storing the millions of daily messages coming from Inovonics’ sensor networks and providing a central view from which data can be analyzed in the aggregate. Redis Enterprise also stores the application data model so that incoming messages can be correlated with representational information such as sensor location. (Our on-premises gateways have open-source Redis repositories that buffer the messages coming from IoT endpoints before they are sent to the cloud.)

Our original intent was to use Redis Enterprise Cloud Pro as a cache only for incoming IoT device data and systematically age out the data to other, slower data stores. But due to the programmatic ease of interfacing with Redis Enterprise and Redis’ invaluable managed services which ensure uptime, we’ve been able to extend Redis Enterprise to serve as a primary repository of our data. We still intend to implement data archiving as data volume grows, but can do so at our own pace.

### We’ve Only Just Scratched the Surface

The high reliability and performance of Redis Enterprise have enabled us to focus on building end user solutions for our target domains rather than optimizing database access. Our initial launch of the application built on top of Redis Enterprise was in the submetering market. We are now expanding the application in other markets, and, as more data emanating from our IoT devices gets consolidated in the cloud, we see opportunities for providing additional value based on predictive data analysis and aggregations.

I hope you’ve enjoyed learning a little about Inovonics’ application of Redis Enterprise. In my next blog post, I’m looking forward to sharing more details on our IoT and Redis use case.
