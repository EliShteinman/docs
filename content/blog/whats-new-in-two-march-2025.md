---
title: "What’s new in two: March 2025"
linkTitle: "What’s new in two: March 2025"
url: "/blog/whats-new-in-two-march-2025/"
description: "Click here to view video"
date: 2025-04-02
blogCategories:
- "Tech"
authors:
- "Talon Miller"
lastmod: 2025-06-10
hidden: true
---

*By Talon Miller, Principal Technical Marketer · Published 2 April 2025 · updated 10 June 2025*

![Blog tile image](/images/blog/fe6014f000320eb2bc67e486e4bcf41f33b44687-772x552.webp)

[Click here to view video](https://www.youtube.com/embed/wqn1eCzgmXI?si=_eQ9ytwISHR9nn93)

Welcome to “What’s new in two,” your quick hit of Redis releases you might have missed in the past month. We’re covering the latest developments from March and expanding on what I covered in our latest video. Press play above if you’d rather watch than read. Let’s get started.

## Redis Insight updates

### Redis Insight 2.68 adds an ability to preconfigure database connections

Preconfigure database connections using environment variables or a JSON file, enabling centralized and efficient configuration of your Redis databases.

### Test source database connections in Redis Data Integration (RDI)

When setting up an RDI data pipeline in Redis Insight, you can now test the connectivity to your source database. This will help ensure that RDI can connect to the source database and keep your Redis cache updated with changes from the source database.

## Private Service Connect updates

### Support for Active-Active Redis Cloud subscriptions

Private Service Connect (PSC) connectivity is now supported for Active-Active subscriptions. For those who don’t know, Active-Active is our ability to replicate data across multiple regions to enable 99.999% uptime and local latency no matter where the user is.

### Support with CAPI and Terraform

PSC supports configuring through the Cloud API and Terraform to help customers automate their configurations. Terraform support is included with version 2.1.0 and Terraform PSC module version 1.0.0.

### CAPI support for session logs

Our Cloud API now allows customers to extract user session logs through /session-logs API calls in addition to the service logs through the /logs call. We’re looking to introduce other log categories as well so keep your eyes out for that.

That wraps up this month’s “What’s new in two.” We’ve covered the latest Redis features and improvements from March. Whether you prefer watching or reading, catch more valuable updates in my next two-minute episode. And if you missed [last month’s update](https://youtu.be/y7MYsSnb4Yc), two minutes is all you need to catch up. See you next time.
