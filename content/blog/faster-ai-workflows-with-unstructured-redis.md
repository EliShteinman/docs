---
title: "Faster AI workflows with Unstructured & Redis"
linkTitle: "Faster AI workflows with Unstructured & Redis"
url: "/blog/faster-ai-workflows-with-unstructured-redis/"
description: "We’re thrilled to announce our partnership with Unstructured, combining their powerful data preprocessing expertise with Redis’ real-time AI capabilities. Together, we’re making it easier than ever..."
date: 2025-04-22
blogCategories:
- "Tech"
authors:
- "Jim Allen Wallace"
- "Rini Vasan"
- "Maria Khalusova"
lastmod: 2025-06-11
hidden: true
---

*By Jim Allen Wallace, Rini Vasan, Maria Khalusova · Published 22 April 2025 · updated 11 June 2025*

![Blog tile image](/images/site-mirror/b9e98d00955ea9cb0782fba33be4242561c8eb11-772x552.webp)

We’re thrilled to announce our partnership with Unstructured, combining their powerful data preprocessing expertise with Redis’ real-time AI capabilities. Together, we’re making it easier than ever for organizations to make their AI workflows faster by simplifying how data is ingested, transformed, and retrieved. This integration provides an optimized, end-to-end solution for building retrieval augmented generation (RAG) pipelines and other AI-driven apps.

**Unstructured transforms complex, unstructured data into clean, structured data**
Unstructured, a leader in data preprocessing, offers advanced tools to extract, clean, and format unstructured data for AI apps. By simplifying the challenge of preparing diverse data sources, from PDFs and Word documents to emails and images, they make it easier for companies to build high-quality machine learning models and apps. Unstructured transforms messy data into streamlined formats, making it immediately usable for AI and machine learning tasks.

**Redis speeds up your apps with fast data retrieval and vector search**
Redis is the real-time data platform that powers AI-driven apps with unmatched speed, flexibility, and scalability. Our high-performance, highly scalable architecture allows businesses to process and retrieve data instantly, making AI models more responsive and intelligent. From vector search to real-time analytics, Redis provides the backbone for high-performance AI solutions that need fast data processing and retrieval.


*“One of the biggest challenges with GenAI applications is delivering low-latency, high-relevance results—especially at scale. With Redis, teams get extremely fast retrieval and flexible vector search capabilities out of the box. Combined with Unstructured’s ability to prep diverse and messy data, this integration unlocks the performance needed to build truly real-time AI experiences.”*

— Mike Moss, SVP Worldwide Partner Sales

**Together, you get seamless, powerful AI apps**
When you combine Unstructured’s preprocessing capabilities with Redis’ fast database and vector search, users can efficiently turn raw, unstructured data into clean, AI-ready inputs.. This integration helps teams build smarter, more responsive apps that drive real-time insights and innovation.

*“As organizations are taking Gen AI from prototyping into production – we’re seeing great synergy between Unstructured and Redis. Unstructured provides the capability to tap into the 80% of data that’s trapped in unstructured formats like PDFs, Word docs, Powerpoints, etc. The data seamlessly flows from enterprise systems like Sharepoint into Unstructured and ultimately lands in Redis allowing our customers to deliver on their data product(s). These products power all kinds of things for our mutual customers – more intelligent decision making, revenue, faster speed to innovation.. you name it, someone is probably building it!”*

— Cassie Pless, Head of Sales at Unstructured

For companies building AI apps and RAG pipelines, this partnership delivers:

• **End-to-end efficiency:** Data preprocessing through Unstructured seamlessly integrates with Redis’ real-time vector search, optimizing the entire retrieval process.

• **Scalability:** Redis’ horizontal scalability keeps your AI apps growing without sacrificing performance.

• **Real-time insights:** Achieve rapid, relevant search results with Redis’ vector search, powered by the most up-to-date, preprocessed data from Unstructured.

## Setting up the integration

Here’s how to configure the [Redis Cloud integration](https://docs.unstructured.io/platform/destinations/redis) in Unstructured:

### Using the Unstructured UI

1. Navigate to the “Connectors” section in the sidebar and click “Destinations”
1. Click “[New](https://platform.unstructured.io/connectors/editor/new/destinations)” and provide a unique name for your connector
1. Choose “Redis” as the Provider and fill out the following configuration details:
- Connection URI, or hostname/port/username/password
- Database index (typically 0-15)
- SSL settings (if applicable)
- Batch size for uploads

Screenshots of a sample Redis Cloud destination connector configuration:

![Redis Unstructured Blog 1](/images/site-mirror/23dd6fe816b9818fbd4bc52b830fc28d8ec102a7-1412x1384.webp)

![Redis Unstructured Blog 2](/images/site-mirror/07214498bf44167c6e2fd5f6326d644ab7562b5c-1398x880.webp)

![Redis Unstructured Blog 3](/images/site-mirror/2bb1cbf51ef0a351dec2d4340e9ea17b637f5078-1400x788.webp)

![Unstructured Blog 4](/images/site-mirror/d5ac869917aa39ba7ea766b389d1938f05952bac-1398x1110.webp)

### Using the Unstructured API

For those who prefer programmatic setup, here’s how to create a Redis Cloud destination connector using our API

With curl:

```
curl --request 'POST' \
--location "$UNSTRUCTURED_API_URL/destinations" \
--header 'accept: application/json' \
--header "unstructured-api-key: $UNSTRUCTURED_API_KEY" \
--header 'content-type: application/json' \
--data '{
    "name": "&lt;name>",
    "type": "redis",
    "config": {
        "database": &lt;database>,
        "ssl": &lt;true|false>,
        "batch_size": &lt;batch-size>,
        # For URI authentication:
        "uri": "&lt;uri>"
        # For password authentication:
        "host": "&lt;host>",
        "port": &lt;port>,
        "username": "&lt;username>",
        "password": "&lt;password>"   
    }
}'

```

With Python SDK:

```python
import os

from unstructured_client import UnstructuredClient
from unstructured_client.models.operations import CreateDestinationRequest
from unstructured_client.models.shared import (
    CreateDestinationConnector,
    DestinationConnectorType,
    RedisDestinationConnectorConfigInput
)

with UnstructuredClient(api_key_auth=os.getenv("UNSTRUCTURED_API_KEY")) as client:
    response = client.destinations.create_destination(
        request=CreateDestinationRequest(
            create_destination_connector=CreateDestinationConnector(
                name="<name>",
                type=DestinationConnectorType.REDIS,
                config=RedisDestinationConnectorConfigInput(
                    database="<database>",
                    ssl=<True|False>,
                    batch_size=<batch-size>,

                    # For URI authentication:
                    uri="<uri>"
                
                    # For password authentication:
                    host="<host>",
                    port=<port>,
                    username="<username>",
                    password="<password>"   
                )
            )
        )
    )

```

**Get started today**
Check out the connector in [Unstructured](https://unstructured.io/developers) and explore the [docs](https://docs.unstructured.io/platform/destinations/redis) to see how this integration can supercharge your AI workflows.
