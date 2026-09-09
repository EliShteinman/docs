---
title: "GraphQL and Redis: Build Your Own Haunted House Tracker Microservice"
linkTitle: "GraphQL and Redis: Build Your Own Haunted House Tracker Microservice"
url: "/blog/graphql-and-redis/"
description: "In a three-part video series, Guy Royse, Senior Developer Advocate at Redis, uses Apollo GraphQL, Redis, and Node.js to build a microservice that exposes data on haunted places."
date: 2023-06-07
blogCategories:
- "Uncategorized"
authors:
- "Alex Patino"
lastmod: 2025-03-27
hidden: true
---

*By Alex Patino · Published 7 June 2023 · updated 27 March 2025*

![Blog tile image](/images/blog/95ec19107540963769b9ed28e5464189a8dba48f-772x550.webp)

**In a three-part video series, Guy Royse, Senior Developer Advocate at Redis, uses Apollo GraphQL, Redis, and Node.js to build a microservice that exposes data on haunted places.**

GraphQL is a querying language that delivers a holistic and easy-to-parse description of data stored using an API. Let’s see how Guy Royse uses GraphQL alongside Redis to track down spooky locations with simplicity, speed, and accuracy.

## Ghost Hunting With Redis and Apollo GraphQL, Part 1

Part one of this three-part series begins with showing the data stored in Redis, which includes information on states, cities, and haunted places. GraphQL works best with structured data, so this is an ideal dataset for illustrating how the query language works.

![Guy Royse working with GraphQL](/images/blog/f90b1cb509d2a980d8d0ce50e40b92dd7ea3f0b7-1999x1048.webp)

Guy installs the necessary packages and positions the code for the Apollo server, defining the type definitions, resolvers, and data sources. He demonstrates querying for states, cities, and coordinates, showcasing the GraphQL server’s functionality, and wrapping things up by successfully retrieving the data on these haunted locales by ID.

> Follow along with Part 1 of this series to start building your simple microservice.

## Ghost Hunting With Redis and Apollo GraphQL, Part 2

Guy Royce’s haunted places exploration using Redis and Apollo GraphQL continues with help from RediSearch.

Here, Guy explains the process of creating indexes for cities, states, and places using Redis. He demonstrates how to perform full-text searches on indexed fields such as location and description and mentions using tags for categorizing places.

![a graphql demo of haunted Walmart locations.](/images/blog/42d0bd1552ecfa101f8dd6c036043ae64c8ce8a6-1999x1125.webp)

In the demonstration, Guy adds two queries for retrieving places by ID and finding places containing specific text. He creates corresponding resolvers for these queries and showcases the results obtained from the search operations.

> View the entire demonstration.

## Ghost Hunting With Redis and Apollo GraphQL, Part 3

Guy Royse concludes his ghost-hunting expedition with a demonstration of how to use a data loader, which is a caching mechanism, to improve the speed and efficiency of the process of finding haunted places, as the data loader also reduces duplicate requests to Redis.

![GraphQL demonstration](/images/blog/9bd5d892d07738fac07df38dfc9092d7f41e39fb-1999x1122.webp)

Guy wraps things up with additional examples, such as querying for cities, states, and places using the data loader, and he explains how it optimizes the retrieval process. He also discusses applying a data loader to search operations, improving performance by minimizing redundant searches.

Watch the final chapter of this ghostbusting expedition with Guy Royse.

Continue your learning journey with Redis by diving into our Youtube playlist for Operate Redis at Scale (for DevOps).
