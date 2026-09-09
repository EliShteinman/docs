---
title: "Announcing vector sets, a new Redis data type for vector similarity "
linkTitle: "Announcing vector sets, a new Redis data type for vector similarity "
url: "/blog/announcing-vector-sets-a-new-redis-data-type-for-vector-similarity/"
description: "Redis is excited to announce the introduction of vector sets, a groundbreaking data type designed for vector similarity. Inspired by the core principles of Redis and developed by the original..."
date: 2025-04-08
blogCategories:
- "Announcements"
- "Tech"
authors:
- "Rowan Trollope"
lastmod: 2026-06-01
hidden: true
---

*By Rowan Trollope, CEO · Published 8 April 2025 · updated 1 June 2026*

![Blog tile image](/images/blog/a642b80311aea52001260a31f050ff3949d59de7-1544x1104.webp)

Redis is excited to announce the introduction of vector sets, a groundbreaking data type designed for vector similarity. Inspired by the core principles of Redis and developed by the original creator of Redis, Salvatore Sanfilippo, vector sets enhance Redis’s capabilities as a versatile solution for modern AI applications. Vector sets complement the existing powerful vector search in Redis (Redis Query Engine) by offering a Redis-friendly alternative for specific use-cases. Vector sets will be available [in beta in Redis 8 Community Edition](https://hub.docker.com/_/redis). This means that depending on your feedback, we may change, or even break, the features and the API in future versions.

Salvatore Sanfilippo (aka ‘antirez’), the creator of Redis, recently rejoined the company and is the creator of this innovative data type; his expertise has led to the creation of an API that is both simple and intuitive, reflecting Redis’s philosophy of delivering high-performance solutions with minimal complexity.

## What are vector sets?

Vector sets take inspiration from sorted sets, one of Redis’s fundamental data types known for its efficiency in handling ordered collections. Vector sets extend this concept by allowing the storage and querying of high-dimensional vector embeddings, which are crucial for various AI and machine learning applications. Like a sorted set, a vector set has string elements that are associated with a vector instead of a score. The fundamental goal of vector sets is to make it possible to add items, and later get a subset of the added items that are the most similar to a specified vector.

Consider a scenario where you want to store and retrieve vector embeddings for various text descriptions or images. With vector sets, you can easily store these embeddings and perform efficient similarity searches. vector sets also implements some exciting additional capabilities including:

- **Quantization: **In a vector set, the vectors are quantized by default to 8 bit values. However, this can be modified to no quantization or binary quantization when adding the first element.
- **Dimensionality Reduction**: The number of dimensions in a vector can be reduced by random projection by specifying the option and the number of dimensions.
- **Filtering**: Each element of the vector set can be associated with a set of attributes specified as a JSON blob via the VADD or VSETATTR command. This allows the ability to filter for a subset of elements using VSIM that are verified by the expression.

## Vector set commands

Below are some examples of commands you can use with a vector set. For a full list, see our documentation [here](https://redis.io/docs/latest/commands/?group=vector_set).

```
# Add keys to the vector set 
VADD myset VALUES 4 0.5 1.2 0.75 3.8 element1  
VADD myset VALUES 4 0.9 1.5 0.66 4.5 element2  
VADD myset VALUES 4 0.4 1.9 0.92 3.6 element3  
VADD myset VALUES 4 0.7 1.3 0.85 4.1 element4  

# Retrieve the top 3 most similar keys to a given query vector with similarity scores
VSIM myset ELE element4 WITHSCORES COUNT 3

# Remove a key from the set
VREM myset element1



# Count the number of elements in the vector set
VCARD myset


# Show info about a vector set including stored elements, vector dimensions, quantization etc. 

VINFO myset


```

## Redis Query Engine and vector sets

Redis now offers two complementary search capabilities—the Redis Query Engine for comprehensive, enterprise-grade search & querying, and the new vector set as a native data-type that is lightweight and specialized vector similarity search.

Redis Query Engine excels at fast full-text, numerical, vector, and hybrid queries over large scalable datasets, while vector sets provide a streamlined alternative with a simple API. Together, they reinforce Redis’s commitment to performance, flexibility, and developer-friendly search solutions.

Vector sets may be a great choice when your application **primarily focuses on vector similarity use-cases** without the need for advanced search and querying, particularly those involving full-text, or hybrid queries. If you’re building **AI-driven applications** and want a **lightweight, efficient** way to store and query high-dimensional embeddings, vector sets can offer a **simple, streamlined** alternative.

Meanwhile, Redis Query Engine, which is included in [Redis 8](/blog/introducing-another-era-of-fast/) is the fastest search and vector database on the market delivering enterprise-grade solutions for a number of scenarios including:

- **Comprehensive search and querying**: Support for diverse query types enables powerful combinations of vector similarity, full-text search, numerical filtering, and geospatial operations. RQE also seamlessly indexes Redis data-structures such as Hash and JSON for flexible and adjustable query needs.
- **Scalability**: Redis Query Engine offers a horizontally scalable solution (with automatic sharding and management of the distributed architecture) to support large datasets. In addition, it offers multi–threaded search to deliver strong throughput, low latency and fast indexing that makes Redis the fastest vector database solution on the market.
- **GenAI ecosystem**: Strong ecosystem support including integrations with popular frameworks such as Langchain (and LangGraph), and LllamaIndex, as well as our dedicated python library for GenAI apps (RedisVL).

## Getting started with vector sets

Getting started with vector sets is straightforward. Simply deploy the latest version of Redis to get started. For comprehensive instructions on storing and querying vectors, configuration options, and best practices, visit [our documentation here](https://redis.io/docs/latest/develop/data-types/vector-sets/).

Finally, we will also be adding support to various Redis client libraries starting with support in redis-py.

We are immensely excited to see what the developer community will build using vector sets. We look forward to your feedback and innovations, as we continue to evolve Redis to meet the ever-changing needs of the tech landscape. We also encourage you to share your feedback through our GitHub issues or community forums. Have a fun time building.
