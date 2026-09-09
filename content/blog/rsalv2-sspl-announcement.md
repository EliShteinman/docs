---
title: "Redis Stack and Our Redis Modules Are Now Standardized Under a Dual License: RSALv2 and SSPL"
linkTitle: "Redis Stack and Our Redis Modules Are Now Standardized Under a Dual License: RSALv2 and SSPL"
url: "/blog/rsalv2-sspl-announcement/"
description: "It’s been almost four years since we introduced the Redis Source Available License 1.0 (RSALv1) for our Redis modules. During this time, we’ve held an open dialogue with the Redis community about..."
date: 2022-11-15
blogCategories:
- "Announcements"
- "Company"
- "Product Releases"
authors:
- "Redis  "
lastmod: 2025-03-27
hidden: true
---

*By Redis   · Published 15 November 2022 · updated 27 March 2025*

![Blog tile image](/images/blog/a98878bd61760a63d5bec9fbf397bf9814af6c6f-772x550.webp)

It’s been almost four years since we introduced the Redis Source Available License 1.0 (RSALv1) for our Redis modules. During this time, we’ve held an open dialogue with the Redis community about our approach to licensing. Most users like our license’s permissive, non-[copyleft](https://en.wikipedia.org/wiki/Copyleft) spirit. But we’ve also seen a couple of challenges: first, it’s hard for many users to understand the practical implications of the text of the RSAL license; second, we have not standardized on any widely-used source-available license.

Today, we’re pleased to offer the Redis community more freedom and clarity by releasing [Redis Stack](https://redis.io/docs/stack/get-started/) and our [Redis modules](/modules/) under a dual license: a new version of our Redis Source Available License ([RSALv2](/legal/rsalv2-agreement/)) and the Server Side Public License ([SSPLv1](https://www.mongodb.com/licensing/server-side-public-license)).

The new RSALv2 license is simple to read and makes its permissions and limitations clear. And, for those users who require a more standardized license, we hope that the added option to use our software under the SSPL opens Redis Stack and our Redis modules to an even wider audience. Created by MongoDB and adopted by Elastic and many others, SSPL is becoming the de facto standard for source available licenses and is being used by millions of developers worldwide.

***We want to highlight that this change doesn’t affect ***[***Redis open source core***](https://github.com/redis/redis)*** in any way, which remains licensed under the 3-clause BSD license.***

***This change also doesn’t affect our customers who use Redis Enterprise Software or Redis Enterprise Cloud.***

## Redis Source Available License 2.0 (RSALv2)

[RSALv2](/legal/rsalv2-agreement/) is a permissive non-copyleft license, allowing the right to “use, copy, distribute, make available, and prepare derivative works of the software” and has only two primary limitations. Under RSALv2, you may not:

- Commercialize the software or provide it to others as a managed service
- Remove or obscure any licensing, copyright, or other notices

For example:

- “I’m building a SaaS business that’s powered by Redis Stack on the back end.”
The license permits this.
- “I’m building a DBaaS that lets developers deploy instances of Redis Stack.”
The license prohibits this.

We worked closely on the updated RSALv2 with [Heather Meeker](https://heathermeeker.com/about-me/), who is well known for helping to draft many OSS licenses, including the Mozilla Public License 2.0 and source-available licenses like the Confluent Community License, SSPL, Elastic License 2.0, and others. We hope this change clarifies our intent and addresses the questions we’ve received about the RSALv1 license over the past few years.

## Dual licensing: RSALv2 + SSPLv1

We believe that the permissive approach of RSALv2 and the standard wording we use to define its limitations solve many of the challenges raised by our community, but we are also aware that, like any newly created license, it will take time for some users (and their legal teams) to digest it. For this reason, we’ve also added an option to use the [SSPL](https://www.mongodb.com/licensing/server-side-public-license).

This dual-license approach will allow users to choose between a permissive but less well-known license, RSALv2, or a more standardized but copyleft license, such as SSPL.

### How does dual licensing work?

Starting today, November 15th, 2022, our default binary distributions of Redis Stack and our Redis modules will be licensed under RSALv2, and when using the source code, users can apply either RSALv2 or SSPLv1. More details are in the table below:

| Redis Stack | <= 6.2.4 | >= 6.2.6 |
|---|---|---|
| RediSearch | <= 2.4 | >= 2.6 |
| RedisJSON | <= 2.2 | >= 2.4 |
| RedisGraph | <=2.8 | >=2.10 |
| RedisTimeSeries | <=1.6 | >= 1.8 |
| RedisBloom | <= 2.2 | >=2.4 |
| RedisGears | <=1.2 | >= 2.0 |

Please note that any fixes for previously released versions of any of Redis Stack or our modules will be made under RSALv1.

See our [FAQs](/legal/licenses/#faqs) for more information about RSALv2 and our dual licensing approach.

## Closing remarks

To be clear, neither RSALv2 nor SSPL is an OSI-approved license, and each has its restrictions. Simply put, RSALv2 places some limits on commercializing the software. SSPL requires that if you provide the product as a service, you must publicly release any modifications and the source code of your management layers under SSPL.

The necessity of source-available licenses in the cloud era has been discussed many times, and we are proud to contribute to this effort by adopting standards developers already know and use. We believe the dual license provides clarity and flexibility for Redis Stack developers in how they can leverage our latest technologies.
