---
title: "The Holiday Shopping Season Is Here. Are You Ready?"
linkTitle: "The Holiday Shopping Season Is Here. Are You Ready?"
url: "/blog/holiday-shopping-season/"
description: "Another year has flown by, and Black Friday/CyberMonday (and the holidays!) are right around the corner. If forecasts are accurate, shoppers and retailers are going to be busier than ever...."
date: 2021-11-03
blogCategories:
- "Tech"
authors:
- "Henry Tam"
lastmod: 2025-03-27
hidden: true
mirrored: true
---

*By Henry Tam · Published 3 November 2021 · updated 27 March 2025*

![Blog tile image](/images/site-mirror/cd9b1e07587511b81a84b901837e8cc758c07c7d-935x628.webp)

Another year has flown by, and Black Friday/CyberMonday (and the holidays!) are right around the corner. If forecasts are accurate, shoppers and retailers are going to be busier than ever. Historically, purchases in November and December represent 20% of annual retail sales. This year, [NRF](https://nrf.com/topics/holiday-and-seasonal-trends/winter-holidays) predicts 57% of shopping will be done online—and consumer expectations are higher than ever. Unfortunately, 75% of the retailers experienced increased latency and downtime during last year’s holiday season (Retail Holiday Reality [Report](https://inthecloud.withgoogle.com/harris-research/the-impact-of-covid-19-on-holiday-shopping.html) 2020 by GCP Harris Poll). According to [Akamai](https://www.liveseysolar.com/website-speed-study-finds-1-second-delay-in-website-load-time-means-a-7-reduction-in-conversions/), one-second delay in response time can cut conversions by 7% and customer satisfaction by 16%.

This year retailers will face even more challenges from supply chain disruptions, frictionless omnichannel experiences, and continued cost and margin optimizations. It’s vital for retailers to accelerate their digital initiatives to meet the holiday deluge and differentiate themselves at the same time. However, per Deloitte’s [2021 Retail Industry Outlook](https://www2.deloitte.com/us/en/pages/consumer-business/articles/retail-distribution-industry-outlook.html) report, only three in ten executives rated their organizations as having mature digital capabilities.

But it’s not only about a fast responsive e-commerce website. Retailers need to provide personalized omnichannel experiences that support “buy online, pickup in-store”(BOPIS), accurate views of what products are in stock, and durable shopping carts, all of which require real-time applications. Underlying a great shopping experience is the ability to use and present the latest product and customer data effectively and consistently across all sales channels. Below are three specific use cases for leveraging Redis Enterprise and retail data in real-time to enhance the customer shopping experiences and become a [real-time retailer](/industries/retail/):

## Seamless shopping

Time is precious, and waiting for a website to respond hurts your brand and sales. What do we mean by slow? At Redis, we define a real-time user request and response as happening in under 100ms, which means your database has to provide the relevant data in 1ms or less while under heavy load (hello holiday shopping). And it has to happen at all stages of the customer journey—browsing of product catalog, online search, accurate and up-to-date information on products in stock, or shopping cart process—to offer a seamless, user-friendly, and fast shopping experience.

Redis Enterprise improves response time by [caching](/solutions/caching/) frequently used data from a slow disk-based database attached to the network with minimal resources and overhead. Or it can be the primary database with built-in [search engine](/search/) that supports fast continuous indexing of the product catalog and full-text search support—especially critical when you have hundreds or thousands of SKUs. Redis is not only ideal for caching because of its speed, but because it natively supports a variety of modern highly optimized [data structures](/redis-enterprise/data-structures/) such as Hash, List, Sorted Sets, streams, and GeoSpatial indexes, as well as [data models](/redis-enterprise/modules/) like JSON, graph, time series, and artificial intelligence (AI). This multi-model integration enables Redis Enterprise to work as a search engine, graph database, time-series database, document store, and more—all in a single database platform. Redis Enterprise’s in-memory architecture offers performance that scales linearly and high availability (99.999%) under heavy load with diskless replication, instant failure detection, and single-digit-second failover.

> *“RediSearch has allowed us to make the online shopping experience for our customers absolutely seamless. Aggregate searches bring faster, more accurate results so that a customer finds exactly what they need right away. We were facing scalability issues before, but the secondary indexes that are utilized now with our dynamic product offerings mean we can create a convenient and effective buyer journey that keeps customers returning for the healthy and natural products that they have grown to love since our inception.”*
*—Ferry Wijaya, VP Engineering, Lemonilo*

![](/images/site-mirror/dc7289b200df97d617d3bcaf4e7956289297cfe2-300x60.webp)

## Real-time inventory management

According to a Square [report](https://squareup.com/us/en/townsquare/future-of-retail), 74% of retailers plan on using real-time inventory technology this year. Without [real-time inventory](/solutions/real-time-inventory/), retailers can’t optimize inventory, improve yield management, fine-tune supply-chain logistics, reduce shipping costs, and more. For example, if a customer orders an item online or at their favorite store, the retailer can speed up the process and reduce costs by having the item delivered from a closer store or warehouse, or even let the customer know when there’s an item at a dropbox or micro-store near them available for immediate pickup. It’s all about making sure items are in the right place, at the right time, at the right price.

Delayed or inaccurate inventory information can frustrate customers, leading to shopping cart abandonment and order cancellations, lost revenues, higher costs, and brand damage. Redis Enterprise can provide data consistency and bilateral updates between stores, distribution centers, and other channels in real-time, while elastically scaling on-demand with zero downtime to support increased traffic during seasonal events like Black Friday. A [real-time inventory management system](/solutions/real-time-inventory/) can even support the use of predictive data analytics to send the appropriate stock to stores before it’s needed.

![Holiday shopping with an omnichannel experience](/images/site-mirror/75ac3c522c912a040033a27e4377d63f7cf0ee13-1024x575.webp)

## Personalized omnichannel experience

Retailers need to sell and fulfill in more channels than ever: in-store, online, mobile, email, 3rd party marketplaces, and even via social media. Retail customers want the convenience of online shopping with the instant gratification of having the item in hand, like with the ability to buy online and pick up in-store, or have items shipped to their home, office, or other site, then return via mail. To tie all this together, retailers need to build an integrated end-to-end digital touchpoint that enables a personalized omnichannel experience.

Retailers looking for new revenue streams are looking at models like subscriptions and memberships. They’re also using personalization for tailored promotions and recommendations, say, with a monthly box of new clothing curated for a specific customer based on past browsing, purchases, or shopping cart history. Redis Enterprise can cache, manage, and search user sessions to provide a seamless and personalized journey across different e-commerce platforms. For deeper insight into customers’ habits and preferences, RedisAI can utilize AI and machine-learning models directly to data stored in Redis for real-time inferencing and analysis.

## Delight your customers and maximize revenue with Redis Enterprise

If you’re not ready for the holiday season, put a powerful real-time in-memory NoSQL database like Redis Enterprise on your wish list—one that can scale up to handle Black Friday and peak holiday shopping. But it’s about more than speed. Redis can help maximize revenue and profits, retain customer loyalty, and delight your customers. Personally, I wish for all my favorite retailers to get ready and avoid those midnight calls from angry customers—especially me.

### Find out how to transform customer journeys with Redis Enterprise.
Read the [Retail in the Era of Real-Time Everything](/docs/real-time-retail/) ebook.

——

### Then go even deeper with these resources

#### Redis Enterprise
for Retail

Retailers today face pressure to modernize systems and deliver personalized experiences. Find out how to transform your applications with Redis Enterprise.

#### Redis Retail
Data Sheet

Accelerate your retail transformation with Redis Enterprise in critical areas like delivery speed, product selection, and personalization.
