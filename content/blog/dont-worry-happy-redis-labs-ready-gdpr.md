---
title: "Don’t Worry, Be Happy. Redis Labs Has You Ready for GDPR!"
linkTitle: "Don’t Worry, Be Happy. Redis Labs Has You Ready for GDPR!"
url: "/blog/dont-worry-happy-redis-labs-ready-gdpr/"
description: "There is hardly anyone on the planet that hasn’t heard the acronym “GDPR” in the last couple of months. But just in case, we’ll explain it briefly, and then outline what Redis has done to support..."
date: 2018-07-23
blogCategories:
- "Announcements"
- "Tech"
authors:
- "Tal Dagan"
lastmod: 2025-03-27
hidden: true
---

*By Tal Dagan, Vice President of Product Management · Published 23 July 2018 · updated 27 March 2025*

![Blog tile image](/images/site-mirror/0073e867b4e64f59de9047fdcde04295ba647e5c-772x550.webp)

There is hardly anyone on the planet that hasn’t heard the acronym “GDPR” in the last couple of months. But just in case, we’ll explain it briefly, and then outline what Redis has done to support GDPR, and what it means to our customers.

GDPR (General Data Protection Regulation) is a European Union (EU) [regulation](https://en.wikipedia.org/wiki/Regulation_(European_Union)) regarding [data protection](https://en.wikipedia.org/wiki/Data_protection) and privacy for individuals. GDPR primarily aims to give EU citizens and residents control over their personal data, but it also addresses the export of personal data outside the EU.

The regulation applies to three different types of entities with varying levels of liability:

1. **Data Owner **– An individual that owns his or her personal data (email, phone, preferences, etc.)
1. **Data Controller** – An organization that collects data from EU residents
1. **Data Processor** – An organization that processes data on behalf of a Data Controller

What does this mean for you?

First of all, if your applications do not handle personal information, or you do not collect personal information from EU residents, GDPR might not apply to you (that said, if you’re not sure, we highly recommend you consult a GDPR legal expert). If you use one of Redis’ DBaaS services (either the Redis Enterprise Cloud or the Redis Enterprise VPC service), then Redis is considered your **Data Processor**.

The Redis service is built on top of our software. And we’ve taken steps to govern data and achieved [SOC 2 compliance. This means ](/blog/redis-labs-soc-2-compliant/)Redis puts you on a fast track towards GDPR compliance.

On the other hand, if you use Redis’ on-premises solution (Redis Enterprise Software), then Redis is not considered a Data Processor, and the GDPR does not specify any special actions you need to take with us. We do, however, recommend that you gain a deep understanding of how data is accessed, stored and protected and whether or not your applications and data storage policies comply with GDPR regulations. We discussed some of the data considerations for your database in a [previous blog post](/blog/clock-ticking-ready-gdpr/).

GDPR Flow Chart:

![](/images/site-mirror/707cd5e0c08f8e78fa73cd26ff99eb6b7b4e8059-801x616.webp)

Resources for Redis Customers:

1. Added a Data Processing Addendum (DPA) to our [Terms of Use](/terms/services-terms/)
1. [Updated Privacy and Cookie Policy](/privacy/)

Redis has DPA agreements in place with our own sub-processors.

At Redis we are committed to the highest level of trust, transparency, standards and regulatory compliance. We strive to deliver the best customer experience while earning the trust of thousands of Redis customers globally.If you have any questions, you can contact us at [privacy@redis.com](mailto:privacy@redis.com).
