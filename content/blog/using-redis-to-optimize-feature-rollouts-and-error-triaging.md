---
title: "Using Redis to Optimize Feature Rollouts and Error Triaging"
linkTitle: "Using Redis to Optimize Feature Rollouts and Error Triaging"
url: "/blog/using-redis-to-optimize-feature-rollouts-and-error-triaging/"
description: "In an effort to run, run, run… you don’t want to make the $460 million dollar mistake that Knights Capital made back in 2012. This single-day computer system failure of a leading financial market-..."
date: 2019-04-24
blogCategories:
- "Tech"
authors:
- "Shabih Syed"
lastmod: 2025-03-04
hidden: true
---

*By Shabih Syed, Shabih is a Sr. Director of Product Marketing at Redis Labs. He has 13+ years of experience with software development, product management and marketing of cloud-based data management & application integration platforms. Most recently he led product marketing at Liaison Technologies (now OpenText) and has worked for HP and IBM before that. Shabih is based out of NYC. · Published 24 April 2019 · updated 4 March 2025*

![Blog tile image](/images/site-mirror/eabfb3ea2a46b84ad0a382ee404ffc6af26df241-1150x1052.webp)

In an effort to run, run, run… you don’t want to make the $460 million dollar mistake that Knights Capital made back in 2012. This single-day computer system failure of a leading financial market-maker offers several lessons for the broader IT community, including the critical importance of your system components’ design, implementation and DevOps details. In this two-part blog, I’ll share some ideas to help development teams keep their continuous integration and continuous deployment (CI/CD) processes fool-proof. In particular, I’ll show how you can manage continuous updates by using feature toggles and feature context to dictate code routing, store log data for easy access and create an error database with fast lookups — all with the help of Redis.

Imagine, you are a director of engineering managing a team of several developers responsible for the front-end of a web app with thousands of concurrent users. Your app is deployed in AWS and you push weekly updates. The business cannot afford to have any disruptions to the web app, so if an error occurs, your team has to roll-back its latest update instantly.

You have to identify the culprit code quickly, have the appropriate developer fix it and make the change part of a subsequent release. Also, the product team is always requesting new features to be made generally available asap. So, how can you react to errors swiftly, and deploy feature requests safely at the speed the business demands?

At the 2019 Game Developers Conference (GDC), I attended a session that described a well-thought-out process to perform weekly software releases reliably. The session was titled “Debugging in the Large: Cross-Platform Stability at 70M+ Monthly Active Users” and it was co-presented by Chris Swiedler from Roblox, a Redis customer. Chris shared an interesting insight into how his team modifies application behavior at Roblox without changing code in case they run into production issues. They use feature flags, which is very similar to [Martin Fowler’s “feature toggle” approach](https://martinfowler.com/articles/feature-toggles.html).

### Example CI/CD Process for New Feature Releases

![Redis - Figure 2: Feature development and promotion](/images/site-mirror/e20738af7521a43ff634e75047e77c26f556172c-1024x595.webp)

*Figure 2: Feature development and promotion*

Let’s breakdown Figure 2, which outlines an approach that could be part of your CI/CD and triage process.

1. A developer starts working on a new feature.
1. The developer and product management team decide which scenarios will use the new features (perhaps for a subset of users).
1. The developer then comes up with a toggle strategy where new code and old code is separated by “if and else” blocks.
1. Once the developer finishes working on new feature code, they promote a canary release to production (with the help of DevOps).
1. People use the app for a time period, and based on their persona and toggle setting, they are either hitting the new code or the old code.
1. If issues arise, the toggle can be set to false to divert all users to the old code.
1. After some time, the feature is promoted to general availability (GA).

This strategy can be helpful for:

1. Shipping canary releases to production for testing with real-time traffic and real users instead of simulations;
1. Disabling features on the fly without rolling back any code;
1. Enabling features or feature combinations through toggle flags; and
1. Fingerprinting code to easily identify the responsible developer (for large development teams) through metadata stored in toggle flags.

But this approach can be taken one step further to help distributed development teams release new features safely and roll them back when required with minimal impact.

### CI/CD with Redis Enterprise

![Redis - Figure 3: Managing toggles, context, errors & logs with Redis Enterprise](/images/site-mirror/a032d90a223412a4f321a1c26b115b6dd121cefd-1024x472.webp)

*Figure 3: Managing toggles, context, errors & logs with Redis Enterprise*

[Redis Enterprise](/redis-enterprise/) fits the bill when you need a fast, persistent database. Its capabilities include:

- A fully managed Redis database-as-a-service with persistent network storage that guards against the ephemerality of instance storage.
- CRDBs, or conflict-free replicated databases, created across multiple Redis Enterprise clusters that reside in different data centers across the planet. This provides [high availability](/active-active/) in the form of both active-active and active-passive deployments.
- Powerful search capabilities (through the RediSearch module) to run search queries across database clusters.

![Redis - Figure 4: CRDB deployment of Redis Enterprise](/images/site-mirror/ecf70b88e7f0d014327296df1c241826d8e566d3-1024x419.webp)

*Figure 4: CRDB deployment of Redis Enterprise*

In my next installment for this series, I’ll offer more details and code snippets to show specifically how feature toggling, feature context, error databases and log databases built with Redis can make your CI/CD triage process more effective and efficient.
