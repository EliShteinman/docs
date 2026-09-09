---
title: "How HolidayMe Uses Redis Enterprise As Its Primary Database"
linkTitle: "How HolidayMe Uses Redis Enterprise As Its Primary Database"
url: "/blog/how-holidayme-uses-redis-enterprise-as-its-primary-database/"
description: "Nadia is looking to take a summer holiday to Switzerland from her home in Bangalore, India. To plan her trip, she heads online to HolidayMe.com, an online travel agency based in Dubai, Riyadh, and..."
date: 2019-12-20
blogCategories:
- "Company"
authors:
- "Miguel Allende"
lastmod: 2025-03-27
hidden: true
---

*By Miguel Allende, Customer Advocacy Manager · Published 20 December 2019 · updated 27 March 2025*

![Blog tile image](/images/site-mirror/a6db1ade24912daa6cbde4e558985316c524a9db-396x203.webp)

Nadia is looking to take a summer holiday to Switzerland from her home in Bangalore, India. To plan her trip, she heads online to [HolidayMe.com](https://www.holidayme.com/home/en-ww), an online travel agency based in Dubai, Riyadh, and Pune that curates thousands of expert-designed itineraries for customers to personalize. Juggling logistics for airfare, lodging, and attractions in an unfamiliar country can be complicated, and Nadia hopes HolidayMe will make it easier to organize everything in one place.

But there are a number of inhibitors that can make the booking process aggravating. If Nadia can’t remember the name of a particular attraction she’s interested in visiting and HolidayMe’s autocomplete lags, or if the website lags and her search results don’t load instantly, she might grow frustrated and turn to another website to book her travels.

To minimize these issues and ensure a great user experience for all its customers, HolidayMe relies on Redis Enterprise as its primary database, not just a database cache. To learn more about how Redis Enterprise helped HolidayMe speed up its data output by 50 to 60 times and move toward a more modern microservices architecture, read the [case study](/customers/holidayme/) and listen to [The New Stack’s podcast](https://thenewstack.io/redis-labs-on-why-nosql-is-a-safe-bet-for-todays-multi-environment-deployments/) with HolidayMe CTO Rajat Panwar.

## Redis beyond the cache

The online travel agency has been using open source Redis since the company was founded in 2014, originally as a caching system. Hoping to speed data output, the team transitioned to using Redis Enterprise as its primary database for all its customer-facing interactions. The company uses Redis’ Hashes, Sets, and Lists to process data and update geographic information, and even created its own key structures for specific queries.

HolidayMe also wanted to build a search autocomplete mechanism. But the team wasn’t satisfied with the latency yielded by its original toolchain that included MongoDB, Apache Lucene, and Elasticsearch, so it turned to RediSearch to create that functionality.

**Read the **[**full HolidayMe case study**](/blog/how-holidayme-uses-redis-enterprise-as-its-primary-database/)

But that’s not all. You can hear HolidayMe Chief Technology Officer Rajat Panwar discuss using RediSearch in a new episode of [The New Stack Makers podcast](https://thenewstack.io/redis-labs-on-why-nosql-is-a-safe-bet-for-todays-multi-environment-deployments/), in conversation with Redis Chief Product Officer Alvin Richards and The New Stack’s [Alex Williams](https://twitter.com/alexwilliams) and [B. Cameron Gain](https://thenewstack.io/author/bruce-gain/). “We were able to migrate our in-house autocomplete (function) that we managed previously and we took that completely to RediSearch,” Panwar says. “Honestly, it didn’t take us more than two days in terms of having a complete transformation, and it was up and running. And it’s giving us the best latency.”

**See **[**Redis on Why NoSQL Is a Safe Bet for Today’s Multi-Environment Deployments**](https://thenewstack.io/redis-labs-on-why-nosql-is-a-safe-bet-for-todays-multi-environment-deployments/)** on **[**The New Stack**](https://thenewstack.io)** to learn more about the podcast, or listen below:**
