---
title: "Understanding Redis Enterprise Software Support Packages "
linkTitle: "Understanding Redis Enterprise Software Support Packages "
url: "/blog/understanding-redis-enterprise-software-support-packages/"
description: "We ask for a lot of information when you contact our support teams. We’re not being capricious or demanding. There are good reasons why we ask for this information."
date: 2023-01-03
blogCategories:
- "Tech"
authors:
- "Vanessa Hoying"
lastmod: 2025-03-27
hidden: true
---

*By Vanessa Hoying, Contributor · Published 3 January 2023 · updated 27 March 2025*

![Blog tile image](/images/site-mirror/54d3ed914502893dc2d398b993c8ca280dff2d10-772x550.webp)

**We ask for a lot of information when you contact our support teams. We’re not being capricious or demanding. There are good reasons why we ask for this information.**

You’re driving down the road. The car’s “check engine” light turns on. Uh-oh.

![check engine icon in midnight blue](/images/site-mirror/3cd6d3c34218bfcb7477ecdda4ecd92ce68b9bf8-500x500.webp)

Naturally, since you’re a do-it-yourself technical person, your first thought is to go online to research the problem. The online advice suggests that you acquire an OBDII diagnostic tool to determine what the diagnostic code for that check engine light means. A bigger uh-oh: The diagnostic code suggests a dire problem with the catalytic converter, which might cost $2,500 to repair.

But the diagnostic test *also* suggests you take the car to a mechanic. When you do, the mechanic says the car has problems beyond your catalytic converter. Your brake calipers are shot, the brake pads are worn down, and the brake rotors are nearing the end of their life. While the mechanic’s bill may be high, it’s a lot worse than a car breakdown on the highway. You probably wouldn’t know about the extent of the car problem if you were not looking for it.

This process is comparable to the support package that you get with Redis Enterprise. You may find a few low-performance indicators on your own. However, our Customer Success team can dig deeper and look for underlying issues. When you send in the data, our team analyzes the proprietary Redis Enterprise software using our internal tools and extensive technical knowledge.

Maybe it seems like overkill. Why does the Redis Customer Success team request a support package after you provide screenshots and detailed reports about an issue? But the data we ask for truly does help us provide better answers faster.

A support package contains all the essential information to help troubleshoot reported issues within a cluster or to perform health checks. It contains three types of information bundled together (thus a “package”) in a tar.gz file:

- logs
- configuration files
- cluster statistics

![](/images/site-mirror/fdc21a3dc79158fd2b55e5d0e52661521b0c738c-226x470.webp)

*The logs that Customer Success analyzes*

We look at the overall health of your clusters. We aim to find areas for improvement, fix problems before they arise, and guide you on best practices. Your account success is our account success, and your business is our business.

Here is what we check from a support package:

- Shards and endpoint balance
- Node hardware configuration
- Slowlog entries
- Average key size
- Shards usage balance
- Optimal cluster topology
- Geo-distributed databases status and configuration
- Software version end of life
- Key performance metrics, including latency and consumed memory

## How does it work?

There are two ways to obtain a support package. You can do this through the Redis Enterprise GUI or the Redis command-line interface. Both accomplish exactly what you need; it’s only a matter of preference.

![Redis support hotline information](/images/site-mirror/7913595a0bed60e1ace10f41b9240c60d98c3564-748x389.webp)

If you ever have difficulty obtaining your support package, do not hesitate to create a support ticket to reach out to our phenomenal support team.

The easiest way to obtain the support package is using the Redis Enterprise GUI, as all the logs compile with a button click.

If you prefer to use your terminal or PowerShell, you can aggregate a support package by Redis command-line interface. When you create a support ticket, our support team may suggest creating a support package by this method.

## What do we do with the information?

When you submit a support ticket to our support team, our first step is to learn how you encountered the issue. Yes, screenshots and detailed information about the issue help; however, every issue has multiple ways of being diagnosed.

![support package review areas](/images/site-mirror/ef46a1aff7c8643ae5fb33136489b09fd3c8cc3d-671x413.webp)

*Areas we examine when reviewing support packages*

These logs provide further insight for the team to troubleshoot the issue. The logs help our support team to identify the issue and to make Redis Enterprise an even better product.

![log history chart](/images/site-mirror/41a8d93ae95d703be0b8edcc3b07fd6b800beb5b-624x279.webp)

*What we see in these logs that indicates failures within the cluster*

We do this all in a timely manner, so you don’t have to spend hours (or days!) looking at the logs and trying to guess what’s going on. Please do provide this information, as it helps us help you – and gives you the feedback to make your system run smoothly.

![redis enterprise support package healhty cluster view](/images/site-mirror/2c269aedc3286ccc26a103fd1091d50de9a9a15f-1150x1256.webp)

*What we see in a healthy cluster*

We have experts in this field to ensure you’re in good hands. Just as a car mechanic is an expert in their field, our Customer Success team works to find all the nooks and crannies that could be missed.

We understand that privacy and security are important to every business. We stress: *We never collect any database dumps or content*.

Interested in getting your diagnostics checked out? Read the documentation on how to create an updated support package.

Try Redis Cloud for free.
