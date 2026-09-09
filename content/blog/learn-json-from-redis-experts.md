---
title: "Learn JSON From Redis Experts"
linkTitle: "Learn JSON From Redis Experts"
url: "/blog/learn-json-from-redis-experts/"
description: "These videos can bring you up to speed swiftly on using JSON with Redis."
date: 2023-04-03
blogCategories:
- "Tech"
authors:
- "Redis  "
lastmod: 2025-03-27
hidden: true
---

*By Redis   · Published 3 April 2023 · updated 27 March 2025*

![Blog tile image](/images/site-mirror/921d735ad99239e317f0409f046deb9a98691f51-772x550.webp)

**These videos can bring you up to speed swiftly on using JSON with Redis.**

What makes [JSON](/json/) such a popular choice for building applications? Its user-friendliness and its ability to be parsed by both humans and computer systems have made it a fan-favorite among developers. Though, of course, it’s not without its [pratfalls](/blog/json-web-tokens-jwt-are-dangerous-for-user-sessions/), and it’s a good idea to learn both the basics and advanced features.

These webinars, livestreams, and demonstrations illustrate JSON’s core concepts. They also even put those concepts into practice so you can apply what you learn.

## JSON explained

JavaScript Object Notation (JSON) is JavaScript-native text-based syntax used to exchange and describe data in applications. One reason developers use JSON is that it uses conventions similar to popular programming languages, such as [Java](/blog/jedis-vs-lettuce-an-exploration/) and [Python](/blog/how-to-build-a-powerful-search-engine-using-redis-python/).

[In this video](https://youtu.be/I-ohlZXXaxs), Justin Castilla, a senior developer advocate at Redis, shows a simple, real-time demo of creating various JSON objects. He does so by organizing his favorite food trucks in Oakland, “but adding some extra spice with JSON path syntax and querying documents with search,” he says.

![JSON code with a city graphic in foreground](/images/site-mirror/9bf2818e3b342b0770b950e45c42d23d8ed879e3-1999x1090.webp)

Castilla sets out to map his favorite food trucks in Oakland by creating and storing JSON objects for vendors, locations, and events. “Each food truck JSON object, known as a vendor, has a name, an array of cuisines offered, a primary cuisine, and an address,” he explains. Castilla uses that information, along with location, event, and vendor data, to show how to use JSON object types. And then Castilla puts it together to demonstrate how you can use JSON to discover which food trucks will be at certain locations during specific events.

It’s a simple and concise walkthrough for anyone looking to efficiently query and index JSON documents.

Also, if you’re hungry and don’t want to write a new application from scratch, note that there’s an entire website to help you [find Oakland food trucks](https://streetfoodfinder.com/c/CA/Oakland).

## When to use JSON

This session, recorded during [RedisDays](/redisdays/atlanta/) Seattle 2020, was presented by Jay Won of [Coupang](https://www.aboutcoupang.com/), who unpacked the question: Why JSON?

![json code](/images/site-mirror/a43244110b4da6af42e1592a135bd7ed839cf72b-1999x1198.webp)

Though this session covers how Asian e-commerce vendor Coupang has benchmarked RedisJSON and its findings, Won does a wonderful job of navigating the conversation to show how the company uses JSON to assist Coupang with properly executing its advertising platform. He then goes into how JSON works, including when to choose popular commands, such as Strings versus. Hashes when using JSON to build applications.

“Our data model is JSON-formatted, so if you ask ‘Why JSON,’ the answer would be simple – because JSON is human-readable and it’s a universal format,” Won explains. “So most of the programming languages and tools support JSON; [it’s] very convenient to carry around.”

[Watch the video](https://youtu.be/zpgGkxL6ozU) to hear the key findings from Won’s benchmarking exercise.

## How to build a self-hosted JSON document store

[Redis Launchpad](https://marketplace.redis.com/) is an application hub for developers and architects in the Redis community to explore high-quality sample applications that operate various “architectures, data modeling, data storage, and commands, allowing you to start building fast apps faster,” we noted in our [introductory blog post](/blog/introducing-redis-launchpad/). Many of the applications in this hub were built using JSON.

![an orange background with a logo for a Redis Store application](/images/site-mirror/b3422199df6378c465ecd635718dbaa8f218f3d9-988x406.webp)

This [Redis Launchpad video](https://youtu.be/5WgloZdQm3g) demonstrates how to build a self-hosted, real-time JSON document store (cheekily named Redis Store for the purposes of the demonstration). It has the same functionalities as Firebase’s Firestore, a tool that helps build applications without a single line of server code.

The caveat, the speaker notes, is that “Firebase is a great tool as long as you structure your code to avoid exorbitant bills, and even then, your project and data are permanently locked into Google Cloud.”

![a computer interface for coding with json](/images/site-mirror/97f917de6e3f9a93ce543146f5f697cdb4001efb-1900x998.webp)

Looking to replicate your own cost-saving solution? Follow along to create a JSON document store where “you can build a basic real-time chat app from scratch in less than five minutes.”

## Accelerate your applications with a real-time JSON document store

How many of today’s applications are restricted by the strict schemas of relational database management systems (RDBMS) and the sluggish speed of disk-based document databases? [RedisDays London 2022](/blog/redisdays-london-2022-recap/) was all about showcasing the advancements and new use cases for real-time data, with one session, in particular, focusing on the evolution of JSON document stores.

![pieter cailliau and a redisjson presentation for redis](/images/site-mirror/caeec175f0fee56350cc1070528e48397f9b6a13-1899x907.webp)

In this [RedisDays London session](https://youtu.be/fNwrV1_ibLY), Ash Sahu joins Pieter Cailliau, Senior Director of Product Management at Redis, to demonstrate common JSON usage patterns. Among them: real-time inventory management for product cataloging, [financial services](/industries/financial-services/) for [fraud detection](/solutions/fraud-detection/), online [gaming](/industries/gaming/) for establishing user profiles, digital mobility to match drivers with riders, and cybersecurity to establish endpoint protection. They also point out the [object mapping libraries](/blog/introducing-redis-om-client-libraries/) that can be used in conjunction with JSON to build applications.

Hear about different ways you can solve business needs using a query accelerator (used to store frequently accessed JSON data), how developers can use a JSON document store as a front-end database (to accelerate read and write queries), or as a primary database (as a distributed, in-memory JSON document database).

## Do birds dream in JSON?

As a fun JSON bonus, watch this [livestream](https://www.youtube.com/live/LpdShJOZuwA?feature=share) demo in which Justin Castilla takes a large group of data containing bird sightings, with species and location data points, and converts it into an easy-to-digest document database.

![search results for loons](/images/site-mirror/cf71e7ed24454dc9f45ade15d3cf18653be841c4-1999x1121.webp)

## Continuing your JSON journey

Need a solid JSON primer to keep on your bookmark tab? Take a look at [A Cat Lover’s Guide to Understanding JSON Databases](/blog/what-are-json-databases/), which breaks down how JSON databases function and how they’ve simplified the application development process – with examples from a cat’s viewpoint!

If you’re ready to experiment with JSON, give this tutorial a try: [Exploring a Securities Portfolio Data Model Using Native JSON and Query Capabilities](/blog/securities-portfolio-data-model/); it demonstrates how to fine-tune a brokerage app using a JSON data structure. Or try your hand at [Building a Fast, Flexible, and Searchable Product Catalog with JSON](/blog/redismart-real-time-json-product-catalog-service/).
