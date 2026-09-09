---
title: "Introducing the Redis Vector Library for Enhancing GenAI Development"
linkTitle: "Introducing the Redis Vector Library for Enhancing GenAI Development"
url: "/blog/introducing-the-redis-vector-library-for-enhancing-genai-development/"
description: "Redis Vector Library simplifies the developer experience by providing a streamlined client that enhances Generative AI (GenAI) application development. Redis Enterprise serves as a real-time vector..."
date: 2024-02-27
blogCategories:
- "Tech DE"
authors:
- "Tyler Hutcherson"
lastmod: 2025-10-01
hidden: true
---

*By Tyler Hutcherson, Manager, Applied AI Engineering · Published 27 February 2024 · updated 1 October 2025*

![Blog tile image](/images/site-mirror/a794680f4b66e07ff222a595491e646485f38b7d-772x552.webp)

[**Redis Vector Library**](https://github.com/redis/redis-vl-python)** simplifies the developer experience by providing a streamlined client that enhances Generative AI (GenAI) application development. Redis Enterprise serves as a real-time vector database for vector search, LLM caching, and chat history.**

Taking advantage of Generative AI (GenAI) has become a central goal for many technologists. Since ChatGPT launched in November 2022, organizations have set new priorities for their teams to apply GenAI. The expectations are high: AI can compose written language, construct images, answer questions, and write code. But several hurdles remain:

1. AI must overcome hallucinations or made-up results.
1. Teams must translate demos into live, production applications.
1. Businesses must scale up projects efficiently and cost-effectively.

Countless techniques and tools have been developed to help mitigate these challenges. For example, Retrieval Augmented Generation (RAG) has gained prominence for the ability to blend domain-specific data stored in a [vector database](/blog/vector-databases-101/) with the expansive capabilities of Large Language Models (LLMs). What began as a relatively simple method has evolved into a comprehensive suite of strategies to enhance conversational AI quality. This evolution reflects a broader trend toward more technical nuance, underscored by this [fascinating deep-dive into RAG](https://blog.langchain.dev/deconstructing-rag/) published by LangChain.

[Redis](https://redis.io) isn’t just a standalone vector database for RAG. It boosts GenAI application performance by serving as a real-time data layer for many essential tasks: vector search, LLM semantic caching, and session management (e.g., user chat histories). We’ve been listening to our customers, users, and community members. We want to make this easier. To that end, we’ve developed [Redis Vector Library](https://github.com/redis/redis-vl-python), which offers a streamlined client that enables the use of Redis in AI-driven tasks, particularly focusing on vector embeddings for search.

## Getting Started

The Python Redis Vector Library (redisvl) is built as an extension of the well-known [redis-py](https://github.com/redis/redis-py) client. Below we will walk through a simple example. Alternatively, try [this hands-on tutorial](https://github.com/redis-developer/financial-vss/blob/main/redisvl-02.ipynb) on Google Colab that covers RAG *from scratch* with redisvl.

### Setup requirements

Ensure you’re working within a Python environment version 3.8 or higher. Then, use pip for [installation](https://www.redisvl.com/overview/installation.html):

```
pip install redisvl>=0.1.0

```

Deploy Redis following one of these convenient paths:

- [Redis Cloud](/try-free) – Jumpstart your project for FREE with a fully managed Redis service.
- [Redis Stack Docker Image](https://redis.io/docs/install/install-stack/docker/) – Ideal for local development. Get Redis running swiftly using the following Docker command:

```
docker run -d -p 6379:6379 -p 8001:8001 redis/redis-stack:latest

```

redisvl also ships with a dedicated CLI tool called rvl. You can learn more about using the CLI in the [docs](https://www.redisvl.com/overview/cli.html).

### Define a schema

*Black box search applications rarely get the job done in production.*

Redis optimizes production search performance by letting you explicitly configure index settings and dataset schema. With redisvl, defining, loading, and managing a custom schema is straightforward.

Consider a dataset composed of 10k [SEC](https://www.investopedia.com/terms/1/10-k.asp#:~:text=Key%20Takeaways-,A%2010%2DK%20is%20a%20comprehensive%20report%20filed%20annually%20by,detailed%20than%20the%20annual%20report.) filings PDFs, each broken down into manageable text chunks. Each record in this dataset includes:

- **Id**: A unique identifier for each PDF chunk.
- **Content**: The actual text extracted from the PDF.
- **Content Embedding**: A vector representation of the section’s text.
- **Company**: The name of the associated company.
- **Timestamp**: A numeric value representing the last update time.

First, define a schema that models this data’s structure in an index named sec-filings. Use a YAML file for convenience:

```yaml
index:
  name: sec-filings
  prefix: chunk

fields:
  - name: id
    type: tag
    attrs:
      sortable: true
  - name: content
    type: text
    attrs:
      sortable: true
  - name: company
    type: tag
    attrs:
      sortable: true
  - name: timestamp
    type: numeric
    attrs:
      sortable: true
  - name: content_embedding
    type: vector
    attrs:
      dims: 1024
      algorithm: hnsw
      datatype: float32
      distance_metric: cosine

```

The schema.yaml file provides a clear, declarative expression of the schema. By default, the index will use a [Hash data structure](https://redis.io/docs/data-types/hashes/) to store the data in Redis. [JSON is also ](https://www.redisvl.com/user_guide/hash_vs_json_05.html)available along with support for different [field types](https://www.redisvl.com/api/schema.html).

Now, load and validate this schema:

```python
from redisvl.schema import IndexSchema

schema = IndexSchema.from_yaml("schema.yaml")

```

### Create an index

Now we’ll create the index for our dataset by passing a Redis Python client connection to a SearchIndex:

```python
from redis import Redis
from redisvl.index import SearchIndex

# Establish a connection with Redis
client = Redis.from_url("redis://localhost:6379")

# Link the schema with our Redis client to create the search index
index = SearchIndex(schema, client)

# Create the index in Redis
index.create()

```

### Simplify embedding generation

The [vectorizer](https://www.redisvl.com/user_guide/vectorizers_04.html) module provides access to popular embedding providers like [Cohere](https://cohere.com/), [OpenAI](https://openai.com/), [VertexAI](https://cloud.google.com/vertex-ai?hl=en), and [HuggingFace](https://huggingface.co/), letting you quickly turn text into dense, semantic vectors.

Below is an example using the Cohere vectorizer, assuming you have the cohere Python library installed and your COHERE_API_KEY set in the environment:

```python
from redisvl.utils.vectorize import CohereTextVectorizer

# Instantiate the Cohere text vectorizer
co = CohereTextVectorizer()

# Generate an embedding for a single query
embedding = co.embed(
    "How much debt is the company in?", input_type="search_query"
)

# Generate embeddings for multiple queries
embeddings = co.embed_many([
    "How much debt is the company in?",
    "What do revenue projections look like?"
], input_type="search_query")

```

Learn more about working with Redis & Cohere in this dedicated [integration guide](https://docs.cohere.com/docs/redis-and-cohere)!

### Load data

Before querying, use the vectorizer to create text embeddings and populate the index with your data. If your dataset is a collection of dictionary objects, the .load() method simplifies insertion. It batches upsert operations, efficiently storing your data in Redis and returning the keys for each record:

```python
# Example dataset as a list of dictionaries
data = [
    {
        "id": "doc1",
        "content": "raw SEC filing text content",
        "company": "nike",
        "timestamp": 20230101,
        "content_embedding": co.embed(
            "raw SEC filing text content",  input_type="search_document", as_buffer=True
        )
    },
    # More records...
]

# Insert data into the index
keys = index.load(data)

```

### Run queries

The VectorQuery is a simple abstraction for performing KNN/ANN style vector searches with *optional* filters.

Imagine you want to find the 5 PDF chunks most semantically related to a user’s query, such as "How much debt is the company in?". First, convert the query into a vector using a text embedding model (see below section on [vectorizers](https://docs.google.com/document/d/1Y4MQrucHZu9kHy1DcKDmYSQlZ-R8E72KWETWa_mjfzU/edit#heading=h.es779y22axu9)). Next, define and execute the query:

```python
from redisvl.query import VectorQuery

query = "How much debt is the company in?"

query_vector = co.embed(query, input_type="search_query", as_buffer=True)

query = VectorQuery(
    vector=query_vector, 
    vector_field_name="content_embedding",
    num_results=5
)

results = index.query(query)

```

To further refine the search results, you can apply various metadata filters. For example, if you’re interested in documents specifically related to “Nike”, use a Tag filter on the company field:

```python
from redisvl.query.filter import Tag

# Apply a filter for the company name
query.set_filter(Tag("company") == "nike")

# Execute the filtered query
results = index.query(query)

```

Filters allow you to combine searches over structured data (metadata) with vector similarity to improve retrieval precision.

The VectorQuery is just the starting point. For those looking to explore more advanced querying techniques and data types (text, tag, numeric, vector, geo), [this dedicated user guide](https://www.redisvl.com/user_guide/hybrid_queries_02.html) will get you started.

### Boost performance with semantic caching

redisvl goes beyond facilitating vector search and query operations in Redis; it aims to showcase practical use cases and common LLM design patterns.

[Semantic Caching](https://www.redisvl.com/user_guide/llmcache_03.html) is designed to boost the efficiency of applications interacting with LLMs by caching responses based on semantic similarity. For example, when similar user queries are presented to the app, previously cached responses can be used instead of processing the query through the model again, significantly reducing response times and API costs.

To do this, use the SemanticCache interface. You can store user queries and response pairs in the semantic cache as follows:

```python
from redisvl.extensions.llmcache import SemanticCache

# Set up the LLM cache
llmcache = SemanticCache(
    name="llmcache",                     # underlying search index name
    redis_url="redis://localhost:6379",  # redis connection url string
    distance_threshold=0.2               # semantic cache distance threshold
)

# Cache the question, answer, and arbitrary metadata
llmcache.store(
    prompt="What is the capital city of France?",
    response="Paris",
    metadata={"city": "Paris", "country": "france"}
)

```

When a new query is received, its embedding is compared against those in the semantic cache. If a sufficiently similar embedding is found, the corresponding cached response is served, bypassing the need for another expensive LLM computation.

```python
# Check for a semantically similar result
question = "What actually is the capital of France?"

llmcache.check(prompt=question)[0]['response']

```

```bash
>>> 'Paris'

```

We’ll be adding additional abstractions shortly, including patterns for LLM session management and LLM contextual access control. Follow and ⭐ the redisvl [GitHub repository](https://github.com/redis/redis-vl-python) to stay tuned!

## Bringing it all together

If you’re following along so far, you’ll want to take a look at our [end-to-end RAG tutorial](https://github.com/redis/redis-vl-python) that walks through the process of PDF data preparation (extraction, chunking, modeling), indexing, search, and question answering with an LLM.

This particular use case centers around processing and extracting insights from public 10k filings PDFs, as introduced above. It’s been optimized for use on Google Colab so that you won’t need to worry about dependency management or environment setup!

## Learn with additional resources

We hope you’re as excited as we are about building real-time GenAI apps with Redis. Get started by installing the client with pip:

```
pip install redisvl>=0.1.0

```

We’re also providing these additional resources to help you take your learning to the next level:

| Resource | Description | Link |
|---|---|---|
| Documentation | Hosted documentation for redisvl. | https://redisvl.com |
| GitHub | The GitHub repository for redisvl. | https://github.com/RedisVentures/redisvl |
| Tutorial | A step-by-step guide to using redisvl in a RAG pipeline from scratch. | https://github.com/redis-developer/financial-vss |
| Application | An end-to-end application showcasing Redis as a vector database for a document retrieval application with multiple embedding models. | https://github.com/redis-developer/redis-arXiv-search |

[Connect with experts at Redis](/vector-meeting/) to learn more. [Download the Redis vector search cheat sheet](/docs/vss-cheat-sheet/) and register for our upcoming [webinar with LangChain](/events/the-future-of-rag-exploring-advanced-llm-architectures-with-langchain-and-redis/) on February 29, 2024!

Stay tuned for more updates on our AI ecosystem integrations, clients, and developer-focused innovations.
