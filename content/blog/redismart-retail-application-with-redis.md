---
title: "RedisMart: A Fully-Featured Retail Application With Redis"
linkTitle: "RedisMart: A Fully-Featured Retail Application With Redis"
url: "/blog/redismart-retail-application-with-redis/"
description: "Do you remember RedisConf’s keynote demo? If yes, you might enjoy seeing the behind-the-curtain development of the retail application (RedisMart) that was presented. If not, then it’s time to watch..."
date: 2021-07-29
blogCategories:
- "How To and Tutorials"
- "Tech"
- "Uncategorized"
authors:
- "Dylan Kreisman"
lastmod: 2025-03-04
hidden: true
mirrored: true
---

*By Dylan Kreisman, Content Marketing Intern · Published 29 July 2021 · updated 4 March 2025*

![Blog tile image](/images/site-mirror/0cc3a30a638a86f16d616e5339454e5cd74e2b33-772x520.webp)

Do you remember RedisConf’s keynote demo? If yes, you might enjoy seeing the behind-the-curtain development of the retail application (RedisMart) that was presented. If not, then it’s time to watch Yiftach and Ash present it. Here’s the link to the video again:

[Click here to view video](https://www.youtube.com/embed/Q6LfMTNbQOs)

This article is the first of a series. It gives you some insights into the main requirements and the architecture of the RedisMart retail application by looking at how you can implement a product catalog, a distributed [real-time inventory](/solutions/real-time-inventory/), and an AI-powered product search. You’ll also see how Redis Enterprise powers all those functionalities.

## Requirements

As often in software development, let’s start by discussing some basic requirements. Here are some informally noted user stories:

- As a retail customer:
  - I want to have **fast **(<100ms end-to-end latency)** access to catalog and product details **by being able to find productsbased on a variety of criteria (e.g., full-text, price ranges, ratings of other customers, or faceted search). High response times result in high bounce rates.
  - If I don’t know a product’s brand name or want something similar to what I purchased before, I’d like to shop for products by image. It would be cool to find a camera that’s a close match or visually similar to what I have.
  - I want to have a **safe delivery** or be able to buy online and pick up in the store or curbside (click and collect).
- As an inventory manager:
  - I need to have an accurate, real-time view of my inventory to provide a superior fulfillment experience for my customers.
  - I want to optimize my inventory to keep high-demand items in stock and reduce stock of slow moving goods.
  - I need a near real-time view of inventories across different stores and/or fulfillment centers in order to optimize stock.

## Architecture

Now that we know the requirements, let me draw an idea of how Redis is able to help us:

- RediSearch enables rich product searches with numeric filters, full-text search, geo-indexing, scoring, and aggregations.
- Redis Enterprise’s Active-Active feature provides geo-replicated real-time updates across inventories out of the box.
- RedisAI, RedisGears, and RediSearch are leveraged for building a database-integrated machine-learning pipeline for real-time inference and vector-similarity search.

![RedisMart application blog post image](/images/site-mirror/1b4d78d0ff0564ab20c7af229a26620eb89d91a3-1024x715.webp)

From there, it wasn’t too hard to imagine the following design:

![RedisMart application blog post image](/images/site-mirror/c5ea6d99a0100dbd632d1fde7f4df25748900787-1024x664.webp)

*RedisMart application blog post image*

The blue boxes represent services. The red boxes show the databases that are used by those services.

We followed some microservices approaches like:

- **One datastore per service**: Each service has its own data store, and data is exchanged via the service interfaces rather than accessing the data store of another service directly.
- **Polyglot persistence**: Each service uses the data store that is the best fit based on its requirements. Talking about polyglot persistence: Redis is a data platform that allows you to combine the different features and data models offered by modules to build the data store that befits your requirements! It might not surprise that we used Redis and some of the Redis modules to implement the red boxes.

## Implementation

RedisMart offers a user interface that’s served by the web-shop web application. RedisMart has a frontend UI (the customer-facing retail website) and a backend UI (for managing the inventory). We implemented a bunch of services that are leveraged by the application behind the scenes.

- **Purchasing:** The purchase service (surprisingly) handles customer purchases.
- **Inventory:** The inventory service answers questions about the amount of stock within the inventory, and the amount decreases when a customer purchases items. Inventory updates are replicated in near real-time to inventories in other locations by leveraging Redis Enterprise’s Active-Active feature. Redis Enterprise leverages conflict-free replicated data types for dealing with concurrent updates. In this case, a resettable positive negative counter data type is used to prevent counter losses.
- **Product catalog**: The product catalog service provides product-related information and offers sophisticated ways to find products. It uses a Redis database that has the RediSearch + RedisJSON modules deployed. RedisJSON allows us to store the product details directly as JSON documents. RediSearch can index, query, and full-text search JSON documents. The product updates can easily be propagated across multiple sites by using Redis Enterprise’s Active-Active feature.
- **Image recognition**: Finally, the image recognition service offers an AI model-serving functionality for vector-similarity search on images. It uses a Redis database that has the RedisGears, RedisAI, and RediSearch modules installed. RedisGears allows us to build a data pipeline and execute it close to where the data lives. We took advantage of Redis AI for the AI model serving and inference. RediSearch is leveraged to perform the actual search for similar images based on the output of the AI model.

As mentioned before, this is the first article of a series. Please stay tuned to learn more about how we implemented the individual services.

## RedisMart

Now that we’ve looked behind the curtain, let’s see how the application looks on stage.

![](/images/site-mirror/e57eaac1a045f10135561fc5fb8459e3da53ec55-1024x581.webp)

The home page shows you the main product categories. A click on a category triggers a search query via the product catalog service by returning the first 16 products that belong to such a category.

The “Search products” field allows you to perform a full-text search for products. It leads to the following search results page:

![](/images/site-mirror/cc236d600a62334d389d702ee7d86e1f3b1db15b-1024x622.webp)

The search results page has two sections: Faceted search and the actual result list. The faceted search can be used to further limit the search results. You can do so by filtering through main category, sub-category, price, and rating. We’ll talk about the implementation details of how such a faceted search is realized with RediSearch in part two of the blog series. Let me give you a hint by letting you take a look at RedisMart’s debug view:

![](/images/site-mirror/14caf01a9f6fdba6047ad4ca9e2d32168a2f4c04-825x563.webp)

As you can see, tags and aggregation play a role.

Clicking on the little camera icon in the upper right corner allows you to take an image of something that you want to find within the product catalog. The following photo of Doug didn’t find any other Dougs in our database…

![](/images/site-mirror/d2dc68f0923caab978736eddfa0eb6febd71888d-821x478.webp)

…but it nicely found some headphones.

![](/images/site-mirror/1db0298c0308fa40328a15b74a0627b0fa26a67c-860x577.webp)

Let’s assume that you decide on a pair of headphones and want to purchase them. After making your choice, RedisMart allows you to add them to your shopping cart. During the checkout process, you can decide to get them delivered or collect them at a close-by location.

![](/images/site-mirror/0d46f82b01f81947d65f92418795dcda3b01f233-1024x620.webp)

RediSearch’s geo-search powers this local pickup feature. The debug view gives you again a hint of how this is realized behind the scenes.

![](/images/site-mirror/dfeacf761cb76fbad8897e8da53951eec963167b-1024x949.webp)

As soon as a customer completes the purchase, the inventory service gets involved by reducing the number of items in stock. This brings us directly to the backend of the application, which allows us to manage the inventory. RedisMart visualizes how immediate inventory updates are observed on each of the replicated sites. A purchase in the US (GCP us-central1) is replicated with a blink of an eye to Europe (Azure north-europe).

![](/images/site-mirror/449c66eeb79350f80a2929b96c42d68bf67189a1-1024x398.webp)

Once again, we’ll cover more details later. The main point here is that you can access the data from a close-by location at a very low network latency, while counter losses are prevented when data is modified concurrently across multiple sites.

You can see the application in action by watching the following video:

[Click here to view video](https://www.youtube.com/embed/Q6LfMTNbQOs)

## Summary

We hope you enjoyed reading this first part of the blog series about building a fully-featured retail application with Redis. As you can see, the Redis real-time data platform allows us to address requirements like immediate access (less than 100ms end-to-end latency) to product information by leveraging the document database capabilities of RediSearch + RedisJSON. A combination of RediSearch + RedisGears + RedisAI enables AI-powered image search for finding similar products within the product catalog. In addition, features like faceted and geo-search were covered. Last, but not least, we showed you that you can easily build a geo-replicated, real-time inventory based on Redis Enterprise’s Active-Active feature. With all that, the Redis real-time platform helps retail companies positively impact the overall buying experience, provide the best possible fulfillment experience for customers, and optimize inventories in the most cost-effective way.

Do you want to learn more about the individual services that we implemented for RedisMart? Then stay tuned for the next blog article of the series!

Want to try it yourself? Here are some links to get your hands dirty with Redis as a real-time data platform:

- [More about Modules](/redis-enterprise/modules/)
- [github.com/RediSearch](https://github.com/RediSearch/RediSearch)
- [github.com/RedisJSON](https://github.com/RedisJSON/RedisJSON)
- [github.com/RedisGears](https://github.com/RedisGears/RedisGears)
- [github.com/RedisAI](https://github.com/RedisAI/RedisAI)
- [Redis Enterprise Cloud](/redis-enterprise-cloud/overview/)
- [Active-Active Geo-Distribution](/active-active/)

## Credits

A big thank you to everyone who contributed to this demo application:

- Yiftach Shoolman and Ash Sahu for presenting the demo application during RedisConf
- The Redis Marketing team (and especially Udi Gotlieb, Ash Sahu, and Doug Tidwell, and Bryson Coles) for contributing to the demo application’s requirement list, organizing RedisConf, helping with the UI design and for contributing to this blog post
- The Technical Enablement team (and especially Martin Forstner, Greg Georges, and David Maier) for implementing, testing, and designing the demo application—and for contributing to this blog post
- CTO team (and especially Leibale Eidelman, Guy Korland) for developing the modules and the image recognition service
- The Product Management team (and especially Pieter Cailliau, Emmanuel Keller, Jonathan Salomon, and Amiram Mizne) for contributing to the demo application’s requirements list and for providing the product features
- And everyone we forgot to mention here

*We want to dedicate this blog series to the primary developer of the RedisMart application, Martin Forstner. It comes with great sadness to share that he recently passed away. Martin’s knowledge, talent, and sense of humor were second to none. He was much more than a Software Engineer for Redis—he was a colleague, teammate, mentor, and a friend. Rest in peace, Martin, we miss you!*
