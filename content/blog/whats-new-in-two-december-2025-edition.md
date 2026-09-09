---
title: "What’s new in two: December 2025 edition"
linkTitle: "What’s new in two: December 2025 edition"
url: "/blog/whats-new-in-two-december-2025-edition/"
description: "Click here to view video"
date: 2026-01-08
blogCategories:
- "Tech"
authors:
- "Talon Miller"
lastmod: 2026-05-21
hidden: true
---

*By Talon Miller, Principal Technical Marketer · Published 8 January 2026 · updated 21 May 2026*

![What’s new in two – December 2025 edition](/images/blog/833729160c1fbb396db3434dc12d029c7c2eb79f-1200x628.webp)

[Click here to view video](https://www.youtube.com/embed/_LCCgLbQz6M?si=Z65L1cQaG0Nc8Egp)

Welcome to “What’s new in two,” your quick hit of Redis releases you might have missed in the past month. If you blinked, you missed it—so here’s the recap. We’re covering the latest developments from December and expanding on what I covered in our latest video. Press play to watch it instead.

## Redis Cloud Cost Report API is now GA

Redis Cloud now offers a Cost Report API, giving you direct, automated access to your billing data without relying on manual UI downloads.

Built on the FinOps Open Cost and Usage Specification (FOCUS), the API integrates cleanly with FinOps platforms, internal dashboards, and analytics workflows. You can generate reports on demand, filter by date, subscription, database, region, or tags, and export results in JSON or CSV through a single endpoint. This gives finance, procurement, and engineering teams consistent, structured cost data they can actually act on, making it easier to track spend, automate reporting, and scale usage without billing becoming a blocker. Learn more on [the docs](https://redis.io/docs/latest/operate/rc/api/examples/generate-cost-report/).

## AWS PrivateLink for Redis Cloud Pro enters public preview

AWS PrivateLink for Redis Cloud Pro is now available in public preview, enabling private connectivity between your applications and Redis Cloud directly from your AWS VPC.

With PrivateLink, traffic stays entirely within the AWS network, removing the need for public endpoints, VPNs, NAT gateways, or transit gateways. This simplifies network architecture while meeting stricter security and compliance requirements, helping teams move forward on deployments that were previously blocked by networking or security reviews. If you want to get into the preview, reach out to us to see if there are any spots left.

## Redis Software 8.0.6 adds SAML SSO support

Redis Software 8.0.6 adds SAML based single sign on for the Cluster Manager UI. Redis Software now supports both IdP initiated and SP initiated SSO using SAML 2.0, letting teams authenticate through their existing identity provider instead of managing separate usernames and passwords. Check out the [docs here](https://redis.io/docs/staging/DOC-5854/operate/rs/security/access-control/saml-sso/).

## New self-paced GenAI labs in Redis University

Redis University released two new hands-on GenAI labs designed to help you build real AI applications with Redis. Check them out!

### Vector Search with RedisVL

This [beginner-friendly lab](https://university.redis.io/course/1npvvtfft2agew?tab=details) walks you through using Redis as a vector database with the RedisVL library. You’ll work with a real JSON movie dataset, define schemas, store and index vectorized data, and run multiple search techniques, including KNN, filtered vector search, and range queries.

### Build a production RAG chatbot

[In this lab](https://university.redis.io/course/ihjs7iip0gpkrw?tab=details), you’ll build a working RAG chatbot backed by Redis. You’ll prepare, embed, index, and retrieve real-world data, connect an LLM to generate grounded responses, and then productionize the app using semantic caching and memory. You finish with a cost-efficient, production-ready chatbot rather than a disposable demo.

### New learning path: Operate Redis Software

Redis University also introduced a [new Operate Redis Software learning path](https://university.redis.io/learningpath/uobc5j9rrhalce?tab=details) for teams running Redis in self-managed or on-prem environments.

The path covers core operational concepts, including clusters, nodes, databases, and day-two operations. It is designed to help teams run Redis Software with confidence, improving reliability and predictability as deployments scale across environments.

That’s a wrap on November updates. And if you missed [last month’s update](https://youtu.be/eZgTtMguUPU), two minutes is all you need to catch up. Whether you prefer watching or reading, catch more valuable updates in my next two-minute episode. See you next time.
