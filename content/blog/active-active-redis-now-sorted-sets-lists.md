---
title: "Active-Active Redis – Now with Sorted Sets and Lists"
linkTitle: "Active-Active Redis – Now with Sorted Sets and Lists"
url: "/blog/active-active-redis-now-sorted-sets-lists/"
description: "We’re delighted to announce the availability of Redis Enterprise v5.2, with much-anticipated features such as:"
date: 2018-06-26
blogCategories:
- "Announcements"
- "New Product Announcements"
- "Product Releases"
authors:
- "Paz Yanover"
lastmod: 2025-03-27
hidden: true
---

*By Paz Yanover, Principal Product Manager · Published 26 June 2018 · updated 27 March 2025*

![Blog tile image](/images/site-mirror/0073e867b4e64f59de9047fdcde04295ba647e5c-772x550.webp)

We’re delighted to announce the availability of [Redis Enterprise v5.2](/redis-enterprise/software/downloads/), with much-anticipated features such as:

- Active-active support with Conflict-free Replicated Data Types (CRDTs) for Sorted Sets and Lists
- Causal Consistency
- Enhanced security capabilities (including an admin action audit trail)

These features simplify application development and allow greater security for your Redis Enterprise deployments. Read on for more details below.

#### Active-active support with CRDTs for Sorted Sets and Lists

With this release, all major data types of Redis are now supported with CRDTs. This makes Redis Enterprise the only database to support complex data types with seamless automated conflict resolution. All major Redis use cases are now addressed by Redis Enterprise in an active-active manner.

Several of our customers have remarked that CRDTs save them many person-years of application development time. Given the popularity of Sorted Sets and Lists, we expect many will benefit from these new features. [Click here](/redis-enterprise-documentation/developing/crdbs/) for more information about how to develop active-active applications with CRDTs.

#### Causal Consistency

Causal Consistency in active-active Redis CRDTs delivers a strong consistency model that captures causal relationships between operations across replicas. With Causal Consistency, all Redis Enterprise Conflict-free Replicated Database (CRDB) instances agree upon and maintain the order of causally related operations. This is an important capability for applications like e-commerce transactions and chat (so the order of messages doesn’t get mixed up). [Click here](/redis-enterprise-documentation/administering/database-operations/causal-consistency-crdb/) for more information about Causal Consistency in active-active Redis CRDTs.

#### Enhanced security capabilities

Redis Enterprise’s new **admin action audit trail** accomplishes two major objectives. It ensures that system management tasks are appropriately performed and monitored by the Administrator(s), and facilitates compliance with customers’ regulatory standards, such as HIPAA, SOC 2 and PCI. Redis Enterprise audit records now contain the following information about all management actions:

- **Who:** Who performed the action
- **What:** What exactly was performed
- **When:** When the action was performed
- **Result:** Whether the action succeeded or not

Another new security feature of Redis Enterprise is the ability to set a **minimum TLS version**. This lets you require the TLS version that can be used for encrypting both data and control paths, using the REST API or rladmin command. In addition, with **HTTPS enforcement**, you can disable users from accessing the REST API via HTTP, ensuring they access it via HTTPS only.

Finally, we added **support for Redis 4.0.9, **which contains numerous bug fixes, and maintains our policy of strong sync with open source versions of Redis. Redis Enterprise 5.2 also contains the **LUA vulnerability fix**, which is available in open source Redis version 4.0.10, following massive tests to verify the fix.

If you’re interested in a more detailed view of what’s new in **Redis Enterprise 5.2**, please visit our [technical documentation](/resources/documentation/) or check out the [release notes](/redis-enterprise-documentation/release-notes/rs-5-2-june-2018/). For questions/comments on our newest release or feedback for Redis in general, please email us at [pm.group@redis.com](mailto:pm.group@redis.com)
