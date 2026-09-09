---
title: "What’s new in two – December edition"
linkTitle: "What’s new in two – December edition"
url: "/blog/whats-new-in-two-december-edition/"
description: "Click here to view video"
date: 2025-01-06
blogCategories:
- "Tech"
authors:
- "Talon Miller"
lastmod: 2025-07-03
hidden: true
---

*By Talon Miller, Principal Technical Marketer · Published 6 January 2025 · updated 3 July 2025*

![Blog tile image](/images/blog/b62fa2068a852ccd3a777c9ef8c0d1459d73a0c2-772x552.webp)

[Click here to view video](https://www.youtube.com/embed/K6uFvHgEZhQ?si=gRsXmiZVUOm8w8w0)

Welcome to “What’s new in two,” your quick hit of Redis releases you might have missed in the past month. We’re covering the latest developments from December, expanding on what I covered in our latest video—press play above if you’re more of a watcher than a reader. Let’s get started.

## Welcome back Salvatore Sanfilippo

![](/images/blog/51c15abd4b722cff5c7060fe43d9b3353e71f447-751x364.webp)

The creator of Redis, Salvatore Sanfilippo, is back at Redis Inc. as of December 10. There’s a lot in his recent blog post about what he’s been up to, why he’s coming back, his opinion on the license change, AI trends, and more. I particularly enjoyed reading about the connecting points between the early days of Redis and the license change. Read his [blog post here](https://lnkd.in/g5jQpzTj).

## General availability of Redis 7.4 for Pro tier & Active-Active

Good news for our Cloud users—Redis 7.4 is now generally available in our Pro tier subscription, which also includes support for Active-Active, the ability to geo-replicate data in real-time across globally distributed regions.

## Private Service Connect support for Active-Active

Here’s another update for our Cloud Pro users—support for Private Service Connect (PSC) is now supported for Active Active plans deployed to Google Cloud.

## API backup to ad-hoc location

The Cloud API now supports ad-hoc backups. This not only lets you programmatically trigger backups rather than depending on scheduled jobs, but also define custom backup destinations like incorporating a timestamp.

## Logs Viewer role added

Redis Cloud users can now run the API with reduced permissions by creating an API key for users with the “Viewer” or the newly introduced “Logs Viewer” roles. This makes it easier to meet security and compliance needs. Log Viewers can only use the [Redis Cloud API](https://redis.io/docs/latest/operate/rc/api/) and [GET /logs](https://api.redislabs.com/v1/swagger-ui/index.html?_gl=1*gb1h6a*_gcl_aw*R0NMLjE3MzM3ODYzNDcuQ2owS0NRaUF4OXE2QmhDREFSSXNBQ3dVeHU0ZGZnMXViNkliN2xRZHRFZF9WWlZVNlBKNTFGM2hoSlRSd19KX1lsaldNek5yeU9ZbFhqZ2FBc3puRUFMd193Y0I.*_gcl_au*ODM1NzU2MDE0LjE3MzAxNzE1MzI.#/Account/getAccountSystemLogs) endpoint.

That wraps up this month’s “What’s new in two.” We’ve covered the latest Redis features and improvements from December. Whether you prefer watching or reading, catch more valuable updates in my next two-minute episode. And if you missed [last month’s update](https://www.youtube.com/watch?v=F_sXNogoV_U), two minutes is all you need to catch up. Happy Holidays and we’ll see you in the New Year.
