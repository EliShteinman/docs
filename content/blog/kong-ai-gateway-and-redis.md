---
title: "Semantic processing and vector similarity search with Kong AI gateway and Redis"
linkTitle: "Semantic processing and vector similarity search with Kong AI gateway and Redis"
url: "/blog/kong-ai-gateway-and-redis/"
description: "Since its earliest versions, Kong has supported Redis. Today, Kong API Gateway and Redis integration is a powerful combination that enhances API management across three main groups of use cases:"
date: 2025-04-28
blogCategories:
- "Partners"
- "Tech"
authors:
- "Jim Allen Wallace"
- "Claudio Acquaviva"
lastmod: 2026-06-01
hidden: true
mirrored: true
---

*By Jim Allen Wallace, Claudio Acquaviva · Published 28 April 2025 · updated 1 June 2026*

![Blog tile image](/images/site-mirror/db8cbe65954bd9dd221702071004898a80a97f66-772x552.webp)

Since its earliest versions, Kong has supported Redis. Today, Kong API Gateway and Redis integration is a powerful combination that enhances API management across three main groups of use cases:

- **Kong API Gateway:** Kong integrates with Redis via plugins that enable it to leverage Redis capabilities for enhanced API functionality, including caching, rate limiting, and session management.
- **Kong AI Gateway:** Starting with Kong Gateway 3.6, several new AI-based plugins leverage Redis vector databases to implement AI use cases, such as rate limiting policies based on LLM tokens, semantic caching, semantic prompt guards, and semantic routing.
- **Retrieval-augment generation (RAG) and agent apps:** Kong AI Gateway and Redis can collaborate for AI-based apps using frameworks like LangChain and LangGraph.

Kong supports multiple types of Redis deployments for all use cases, including [Redis Community Edition](https://redis.io/docs/latest/get-started/) (including while using Redis Cluster for horizontal scalability or Redis Sentinel for high availability), [Redis Software](https://redis.io/software/) (which provides enterprise capabilities often needed for production workloads), and [Redis Cloud](https://redis.io/cloud/) (available on AWS, GCP, and as Azure-managed Redis in Azure).

In this post, we’ll focus on how Kong and Redis can be used to address semantic processing use cases, including similarity search and semantic routing across multiple LLM environments.

## Kong AI gateway reference architecture

To get started, let’s take a look at a high-level reference architecture of the Kong AI Gateway. As you can see, the Kong Gateway Data Plane, responsible for handling the incoming traffic, can be configured with two types of Kong plugins:

![](/images/site-mirror/68480c29f1124e50eaf0cd7d52976141a030fe83-952x537.webp)

### Kong API gateway plugins

One of the main capabilities the Kong Gateway provides is extensibility. An extensive list of plugins allows you to implement specific policies to protect and control the APIs deployed in the gateway. The plugins offload critical and complex processing usually implemented by backend services and apps. With the Gateway and its plugins in place, the backend services can focus on business logic only, leading to a faster app development processes. Each plugin is responsible for specific functionality, including:

- Authentication/authorization to implement security mechanisms such as basic authentication, LDAP, mutual TLS (mTLS), API key, open policy agent (OPA)-based access control policies, etc.
- Integration with Kafka-based data/event streaming infrastructures.
- Log processing to externalize all requests processed by the gateway to third-party infrastructures.
- Analytics and monitoring to provide metrics to external systems, including OpenTelemetry- based systems and Prometheus.
- Traffic control to implement canary releases, mocking endpoints, and routing policies based on request headers, etc.
- Transformations to transform requests before routing them to the upstreams and to transform responses before returning to the consumers.
- WebSockets Size Limit and WebSockets Validator plugins to control the events sent by the devices for IoT projects where MQTT over WebSockets connections are extensively used.

Also, Kong API Gateway provides plugins that implement several integration points with Redis, including:

- [Proxy Caching Advanced](https://docs.konghq.com/hub/kong-inc/proxy-cache-advanced/) and [GraphQ](https://docs.konghq.com/hub/kong-inc/graphql-proxy-cache-advanced/)[L](https://docs.konghq.com/hub/kong-inc/graphql-proxy-cache-advanced/)[ Proxy Caching Advanced](https://docs.konghq.com/hub/kong-inc/graphql-proxy-cache-advanced/) cache and serve requested responses.
- [Rate limiting](https://docs.konghq.com/hub/kong-inc/rate-limiting/), [rate limiting advanced](https://docs.konghq.com/hub/kong-inc/rate-limiting/), [service protection](https://docs.konghq.com/hub/kong-inc/service-protection/), and [GraphQL rate limiting advanced](https://docs.konghq.com/hub/kong-inc/graphql-rate-limiting-advanced/) – rate limit how many HTTP requests can be made in a given time frame.
- [OpenID Connect](https://docs.konghq.com/hub/kong-inc/openid-connect/) and [Upstream OAuth](https://docs.konghq.com/hub/kong-inc/upstream-oauth/) for session storage and token caching.
- [ACME](https://docs.konghq.com/hub/kong-inc/acme/) stores digital certificates.

### Kong AI gateway plugins

On the other hand, Kong AI Gateway leverages the existing Kong API Gateway extensibility model to provide specific AI-based plugins more precisely to protect LLM infrastructures, including:

- [AI Proxy](https://docs.konghq.com/hub/kong-inc/ai-proxy/) and [AI Proxy Advanced](https://docs.konghq.com/hub/kong-inc/ai-proxy-advanced/) plugins use multi-LLM capability to abstract and load balance multiple LLM models based on policies, including latency time, model usage, semantics, etc.
- Prompt engineering templates:
  - [AI Prompt Temp](https://docs.konghq.com/hub/kong-inc/ai-prompt-template/)[l](https://docs.konghq.com/hub/kong-inc/ai-prompt-template/)[ate](https://docs.konghq.com/hub/kong-inc/ai-prompt-template/) plugin is responsible for pre-configuring AI prompts to users.
  - [AI Prompt Decorator](https://docs.konghq.com/hub/kong-inc/ai-prompt-decorator/) plugin injects messages at the start or end of a caller’s chat history.
  - [AI Prompt Guard](https://docs.konghq.com/hub/kong-inc/ai-prompt-guard/) plugin lets you configure a series of PCRE-compatible regular expressions to allow and block specific prompts, words, phrases, etc and have more control over an LLM service.
  - [AI Semantic Prompt Guard](https://docs.konghq.com/hub/kong-inc/ai-semantic-prompt-guard/) plugin enables self-configurable semantic (or pattern-matching) prompt protection.
- [AI Semantic Cache](https://docs.konghq.com/hub/kong-inc/ai-semantic-cache/) plugin caches responses based on threshold to improve performance (and therefore end-user experience) while optimizing for cost.
- [AI Rate Limiting Advanced](https://docs.konghq.com/hub/kong-inc/ai-rate-limiting-advanced/) lets you tailor per-user or per-model policies based on the tokens returned by the LLM provider or craft a custom functions to count the tokens for requests.
- [AI Request Transformer](https://docs.konghq.com/hub/kong-inc/ai-request-transformer/) and [AI Response Transformer](https://docs.konghq.com/hub/kong-inc/ai-response-transformer/) plugins seamlessly integrate with LLMs, enabling introspection and transformation of a request’s body before proxying it to the upstream service prior to forwarding the response to the client.

By leveraging the same underlying core of Kong Gateway, and combining both categories of plugins, we can implement powerful policies and reduce complexity in deploying the AI Gateway capabilities as well.

The first use case we are going to focus on is semantic caching, where the AI Gateway plugin integrates with Redis to perform similarity search. Then, we’re going to explore how the AI Proxy Advanced Plugin can take advantage of Redis to implement semantic routing across multiple LLM models.

Two other noteworthy use cases for Kong and Redis are AI Rate Limiting Advanced and AI Semantic Prompt Guard Plugins, but we won’t cover them in detail in this post.

Before diving into the first use case, let’s highlight and summarize the main concepts Kong AI Gateway and Redis rely on.

### Embeddings

Embeddings, also known as vectors or even [vector embeddings](https://redis.io/glossary/vector-embeddings/), are a representation of unstructured data such as text, images, etc. In a LLM context, the dimensionality of embeddings refers to the number of characteristics captured in the vector representation of a given sentence—the more dimensions an embedding has, the better and more effective it is.

There are multiple ML-based embedding methods used in NLP like:

- [One-hot](https://en.wikipedia.org/wiki/One-hot)
- [word2vec](https://code.google.com/archive/p/word2vec/)
- Term frequency-inverse document frequency (TF-IDF)
- [Global Vectors for Word Representation](https://nlp.stanford.edu/projects/glove/) (GloVe)
- [Bidirectional Encoder Representations from Transformers](https://github.com/google-research/bert) (BERT)

Here’s an example of a Python script using [Sentence Transformers](https://sbert.net/) module (aka SBERT or Sentence-BERT maintained by [Hugging Face](https://huggingface.co/)) using the [“all-mpnet-base-v2”](https://huggingface.co/sentence-transformers/all-mpnet-base-v2) embedding model to encode a simple sentence into an embedding:

```python
from sentence_transformers import SentenceTransformer
from sentence_transformers.util import truncate_embeddings

model = SentenceTransformer('all-mpnet-base-v2', cache_folder="./")
embeddings = model.encode("Who is Joseph Conrad?")
embeddings = truncate_embeddings(embeddings, 3)
print(embeddings.size)
print(embeddings)


```

The “all-mpnet-base-v2” embedding model encodes sentences to a 768-dimensional vector. As an experiment, we have truncated the vector to 3 dimensions only.

The output should be like:

```python
3
[ 0.06030013 -0.00782523  0.01018228]

```

### Vector database

A vector database stores and searches vector embeddings. They are essential for AI-based apps supporting images, texts, etc. that provide vector stores, vector indexes, and—more importantly—algorithms to implement vector similarity searches.

We’ve created some introductions about using Redis for [vector embeddings](https://redis.io/glossary/vector-embeddings/) and [vector databases](/blog/vector-databases-101/). What makes us ideally suited to these use cases is Redis Query Engine—a in-built capability within Redis that provides vector search functionality (as well as other types of search such as full-text, numeric, etc.) and delivers [industry-leading performance](/blog/benchmarking-results-for-vector-databases/). Redis provides unmatched performance with sub-millisecond latency, leveraging in-memory data structures and advanced optimizations to power real-time apps at scale. This is critical for gateway use-cases where deployment happens in the “hot-path” of LLM queries.

Additionally, Redis can be deployed as as enterprise software and/or as a cloud service, thereby adding several enterprise capabilities, including:

- **Scalability**. Redis can easily scale horizontally and effortlessly handle dynamic workloads and manage massive datasets across distributed architectures.
- **High availability and persistence**. Redis supports high availability with built-in support for multi-AZ deployments, seamless failover, data persistence through backups and active-active architecture to enable robust disaster recovery and consistent app performance.
- **Flexibility**. Redis natively supports multiple data structures, such as JSON, hash, strings, streams, and more to suit diverse app needs.
- **Broad ecosystem.** As one of the world’s most popular databases, we offer a rich ecosystem of client libraries ([redisvl](https://www.redisvl.com/index.html) for GenAI use-cases), [developer tools](https://redis.io/docs/latest/develop/tools/), and integrations.

### Vector similarity search

With similarity search we can find, in a typically unstructured dataset, items similar (or dissimilar) to a certain presented item. For example, given a picture of a cell phone, try to find similar ones considering its shape, color, etc. Or, given two pictures, check the similarity score between them.

In our NLP context, we’re interested in similar responses returned by the LLM when apps send prompts to it. For example, these two following sentences, “Who is Joseph Conrad?” and “Tell me more about Joseph Conrad” should, semantically speaking, have a high similarity score.

We can extend our Python script to try that out:

```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-mpnet-base-v2', cache_folder="./")

sentences = [
    "Who is Joseph Conrad?",
    "Tell me more about Joseph Conrad.",
    "Living is easy with eyes closed.",
]

embeddings = model.encode(sentences)
print(embeddings.shape)

similarities = model.similarity(embeddings, embeddings)
print(similarities)

```

The output should look like this. The embeddings are:

```python
(3, 768)
tensor([[1.0000, 0.8600, 0.0628],
        [0.8600, 1.0000, 0.1377],
        [0.0628, 0.1377, 1.0000]])


```

The “shape” is composed of 3 embeddings of 768 dimensions each. The code asks to cross-check the similarity of all embeddings. The more similar they are, the higher the score. Notice that the “1.0000” score is returned, as expected, when self-checking a given embedding.

The [“similarity”](https://sbert.net/docs/sentence_transformer/usage/semantic_textual_similarity.html) method returns a [“Te](https://pytorch.org/docs/stable/tensors.html#torch.Tensor)[n](https://pytorch.org/docs/stable/tensors.html#torch.Tensor)[sor”](https://pytorch.org/docs/stable/tensors.html#torch.Tensor) object, which is implemented by [PyTorch](https://pytorch.org/), the ML library used by Sentence Transformer.

There are several techniques for similarity calculation, including distance or angle between the vectors. The most common methods are:

- [Euclidean Dist](https://redis.io/learn/howtos/solutions/vector/getting-started-vector#euclidean-distance-l2-norm)[a](https://redis.io/learn/howtos/solutions/vector/getting-started-vector#euclidean-distance-l2-norm)[nce](https://redis.io/learn/howtos/solutions/vector/getting-started-vector#euclidean-distance-l2-norm) based on linear distance between two points.
- [Cosine Similarity](https://redis.io/learn/howtos/solutions/vector/getting-started-vector#cosine-similarity) used by default by the “similarity” method and based on the angle between two vectors.
- [Dot Product](https://redis.io/learn/howtos/solutions/vector/getting-started-vector#inner-product) based on the product of vectors.

In a vector database context, [vector similarity search (VSS)](https://redis.io/learn/howtos/solutions/vector/getting-started-vector#what-is-vector-similarity) is the process of finding vectors in the vector database that are similar to a given query vector.

## Redis Query Engine and vector similarity search

In 2022, Redis launched [search](https://redis.io/docs/latest/develop/interact/search-and-query/administration/overview/)—a text search engine built on top of Redis data store with RedisVSS (vector similarity search).

To get a better understanding of how RedisVSS works, consider this Python script implementing a basic similarity search:

```python
import redis
from redis.commands.search.field import TextField, VectorField
from redis.commands.search.indexDefinition import IndexDefinition, IndexType
from redis.commands.search.query import Query
import numpy as np
import openai
import os

### Get environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")
host = os.getenv("REDIS_LB")

### Create a Redis Index for the Vector Embeddings
client = redis.Redis(host=host, port=6379)

try:
    client.ft('index1').dropindex(delete_documents=True)
except:
    print("index does not exist")


schema = (
    TextField("name"),
    TextField("description"),
    VectorField(
        "vector",
        "FLAT",
        {
            "TYPE": "FLOAT32",
            "DIM": 1536,
            "DISTANCE_METRIC": "COSINE",
        }
    ),
)

definition = IndexDefinition(prefix=["vectors:"], index_type=IndexType.HASH)
res = client.ft("index1").create_index(fields=schema, definition=definition)


### Step 1: call OpenAI to generate Embeddings for the reference text and stores it in Redis

name = "vector1"
content = "Who is Joseph Conrad?"
redis_key = f"vectors:{name}"

res = openai.embeddings.create(input=content, model="text-embedding-3-small").data[0].embedding

embeddings = np.array(res, dtype=np.float32).tobytes()

pipe = client.pipeline()
pipe.hset(redis_key, mapping = {
  "name": name,
  "description": content,
  "vector": embeddings
})
res = pipe.execute()


### Step 2: perform Vector Range queries with 2 new texts and get the distance (similarity) score

query = (
    Query("@vector:[VECTOR_RANGE $radius $vec]=>{$yield_distance_as: distance_score}")
     .return_fields("id", "distance_score")
     .dialect(2)
)

# Text #1
content = "Tell me more about Joseph Conrad"
res = openai.embeddings.create(input=content, model="text-embedding-3-small").data[0].embedding
new_embeddings = np.array(res, dtype=np.float32).tobytes()

query_params = {
    "radius": 1,
    "vec": new_embeddings
}
res = client.ft("index1").search(query, query_params).docs
print(res)

# Text #2
content = "Living is easy with eyes closed"
res = openai.embeddings.create(input=content, model="text-embedding-3-small").data[0].embedding
new_embeddings = np.array(res, dtype=np.float32).tobytes()

query_params = {
    "radius": 1,
    "vec": new_embeddings
}
res = client.ft("index1").search(query, query_params).docs
print(res)

```

Initially, the script creates an index to receive the embeddings returned by OpenAI. We are using the “text-embedding-3-small” OpenAI model, which has 1536 dimensions, so the index has a VectorField defined to support those dimensions.

Next, the script has two steps:

- Store the embeddings of a reference text generated by OpenAI Embedding Model.
- Perform vector range queries passing two new texts to check their similarity with the original one.

Here’s a diagram representing the steps:

![](/images/site-mirror/a8db2c088faacc73d95e2e8891cfccf2b5d906b1-952x537.webp)

The code assumes you have a Redis environment available. Please check the [Redis products docs](https://redis.io/docs/latest/operate/) to learn more about it. It also assumes you have two environment variables defined: OpenAI API key and load balancer address where Redis is available.

The script was coded using two main libraries:

- “Python client for Redis” ([redis-py](https://redis.io/docs/latest/develop/clients/redis-py/)) library to make Redis calls.
- [“OpenAI Python API”](https://github.com/openai/openai-python) to interact with OpenAI.

```python
While executing the code, you can monitor Redis with, for example, redis-cli monitor. The code line res = client.ft("index1").search(query, query_params).docs 

should log a message like this one:

"FT.SEARCH" "index1" "@vector:[VECTOR_RANGE $radius $vec]=>{$YIELD_DISTANCE_AS: score}" "RETURN" "2" "id" "score" "DIALECT" "2" 
"LIMIT" "0" "10" "params" "4" "radius" "1" "vec" "\xcb9\x9c<\xf8T\x18=\xaa\xd4\xb5\xbcB\xc0.=\xb5………."


```

Let’s examine the command. Implicitly, the [.ft(“index1”)](https://redis-py.readthedocs.io/en/stable/commands.html#redis.commands.cluster.RedisClusterCommands.ft)method call gives us support to [Redis Search Commands](https://redis-py.readthedocs.io/en/stable/redismodules.html#redisearch-commands) as the[*.search(query, query_params)*](https://redis-py.readthedocs.io/en/stable/redismodules.html#redis.commands.search.commands.SearchCommands.search)call sends an actual search query using the *FT.SEARCH* Redis command.

The *FT.SEARCH* command receives the parameters defined in both *query* and *query_params* objects. The *query parameter*, defined using the [*Query*](https://redis.io/docs/latest/develop/interact/search-and-query/query/)object*,* specifies the actual command as well as the return fields and dialect.

```python
query = (
    Query("@vector:[VECTOR_RANGE $radius $vec]=>{$yield_distance_as: distance_score}")
     .return_fields("id", "distance_score")
     .dialect(2)
)


```

We want to return the distance (similarity) score, so we must yield it via the *$yield_distance_as* attribute.

Query dialects enable enhancements to the query API, allowing the introduction of new features while maintaining compatibility with existing apps. For vector queries like ours, query dialect should be set with a value equal or greater than 2. Please check the specific [Query Dialect documentation](https://redis.io/docs/latest/develop/interact/search-and-query/advanced-concepts/dialects/) page to learn more about it.

On the other hand, the* query_params* object defines extra parameters, including the radius and the embeddings that should be considered for the search.

```python
query_params = {
    "radius": 1,
    "vec": new_embeddings
}


```

The final *FT.SEARCH *also includes parameters to define offset and number of results. Check our [documentation](https://redis.io/docs/latest/commands/ft.search/) to learn more about it.

In fact, the *FT.SEARCH* command sent by the script is just an example of [vector search](https://redis.io/docs/latest/develop/interact/search-and-query/query/vector-search/) supported by Redis. Basically, Redis supports two main types of searches:

- [KNN vector search](https://redis.io/docs/latest/develop/interact/search-and-query/advanced-concepts/vectors/#knn-vector-search). This [algorithm](https://en.wikipedia.org/wiki/K-nearest_neighbors_algorithm) finds the top “k-nearest neighbors” to a query vector.
- [Vector range query](https://redis.io/docs/latest/develop/interact/search-and-query/advanced-concepts/vectors/#vector-range-queries). In this query type, the script filters the index based on a radius parameter. Radius defines the semantic distance between the two vectors: the input query vector and indexed vector.

Our script’s intent is to examine the distance between the two vectors and not implement any filter. That’s why it has set the vector range query with *“radius”: 1*.

After running the script, its output should be:

```python
[Document {'id': 'vectors:vector1', 'payload': None, 'distance_score': '0.123970687389'}]
[Document {'id': 'vectors:vector1', 'payload': None, 'distance_score': '0.903066933155'}]


```

This means that, as expected, the stored embedding, related to the reference text, “Who is Joseph Conrad?” is closer to the first new text, “Tell me more about Joseph Conrad,” than to the second one, “Living is easy with eyes closed.”

Now that we have an introductory perspective of how we can implement vector similarity searches with Redis, let’s examine the Kong AI Gateway Semantic Cache plugin which is responsible for implementing semantic caching. We’ll see it performs similar searches to what we have done with the Python script.

## Kong AI Semantic Cache plugin

To get started, logically speaking, we can analyze the caching flow from two different perspectives:

- Request #1. We don’t have any data cached.
- Request #2. Kong AI Gateway has stored some data in the Redis vector database.

Here’s a diagram illustrating the scenarios:

![](/images/site-mirror/516a9704239a1ef9a296c8531b3bcb3512b249cd-952x537.webp)

### Konnect data plane deployment

Before exploring how the Kong AI Gateway Semantic Cache plugin and Redis work together we have to deploy a Konnect data plane (based on Kong Gateway). Please, refer to the [Konnect documentation](https://docs.konghq.com/konnect/) to register and spin your first data plane up.

### Kong Gateway objects creation

Next, we need to create Kong Gateway objects (Kong Gateway Services, Kong Routes, and Kong plugins) to implement the use case. There are several ways to do this, including Konnect RESTful APIs, Konnect GUI, etc. With [decK](https://docs.konghq.com/deck/latest/) (declarations for Kong), we can manage Kong Konnect configuration and create Kong objects in a declarative way. Please check the [decK documentation](https://docs.konghq.com/deck/latest/guides/getting-started/) to learn how to [use it with Konnect](https://docs.konghq.com/deck/latest/guides/konnect/).

### AI proxy and AI semantic cache plugins

Here’s the decK declaration we are going to submit to Konnect to implement the semantic cache use case:

```python
_format_version: "3.0"
_info:
  select_tags:
  - semantic-cache
_konnect:
  control_plane_name: default
services:
- name: service1
  host: localhost
  port: 32000
  routes:
  - name: route1
    paths:
    - /openai-route
    plugins:
    - name: ai-proxy
      instance_name: ai-proxy-openai-route
      enabled: true
      config:
        auth:
          header_name: Authorization
          header_value: Bearer <your_OPENAI_APIKEY>
        route_type: llm/v1/chat
        model:
          provider: openai
          name: gpt-4
          options:
            max_tokens: 512
            temperature: 1.0
    - name: ai-semantic-cache
      instance_name: ai-semantic-cache-openai
      enabled: true
      config:
        embeddings:
          auth:
            header_name: Authorization
            header_value: Bearer <your_OPENAI_APIKEY>
          model:
            provider: openai
            name: text-embedding-3-small
            options:
              upstream_url: https://api.openai.com/v1/embeddings
        vectordb:
          dimensions: 1536
          distance_metric: cosine
          strategy: redis
          threshold: 0.2
          redis:
            host: redis-stack.redis.svc.cluster.local
            port: 6379


```

The declaration creates the following Kong objects in the “default” Konnect control plane:

- Kong Gateway Service “service1”. It’s a fake service. In fact, the Kong AI Proxy plugin created next will determine the actual upstream destination.
- Kong Route “route1” with the path “/openai-route”. That’s the route which exposes the LLM model.
- AI proxy plugin. It’s configured to consume OpenAI’s “gpt-4” model. The “route_type” parameter, set as “llm/v1/chat”, refers to OpenAI’s “https://api.openai.com/v1/chat/completions” endpoint. Kong recommends storing the API Keys as secrets in a secret manager, such as AWS Secrets Manager or HashiCorp Vault. The current configuration, including the OpenAI API Key in the declaration, is for lab environments only and is not recommended for production. Please refer to the official [AI Proxy Plugin documentation page](https://docs.konghq.com/hub/kong-inc/ai-proxy/) to learn more about its configuration.
- AI Semantic Cache Plugin. It has two settings. Please check the [documentat](https://docs.konghq.com/hub/kong-inc/ai-semantic-cache/)[ion page](https://docs.konghq.com/hub/kong-inc/ai-semantic-cache/) to learn more about these and other configuration parameters.
  - *embeddings:* Consumed the “text-embedding-3-small” embedding model, the same model we used in our Python script.
  - *vectordb*: Refers to an existing Redis infrastructure to store the embeddings and process the VSS requests. Again, it’s configured with the same dimensions and distance metric as we used before. The threshold is going to be translated as the “radius” parameter in the VSS queries sent by the Kong Gateway Data Plane.

After submitting the decK declaration to Konnect, you should see the new Objects using the Konnect UI:


![](/images/site-mirror/1ad622d9bcf0a10d914da616729bf2f2d1c2cf2c-2044x1853.webp)

### Request #1

With the new Kong objects in place, the Kong data plane is refreshed with them and we are ready to start sending requests to it. Here’s the first one with the same content we used in the Python script:

```python
curl -i -X POST \
  --url $DATA_PLANE_LB/openai-route \
  --header 'Content-Type: application/json' \
   --data '{
   "messages": [
     {
       "role": "user",
       "content": "Who is Joseph Conrad?"
     }
   ]
 }'


```

You should get a response like this, meaning the gateway successfully routed the request to OpenAI which returned an actual message to us. From semantic caching and similarity perspectives, the most important headers are:

- *X-Cache-Status: Miss*, telling us the gateway wasn’t able to find any data in the cache to satisfy the request.
- *X-Kong-Upstream-Latency* and *X-Kong-Proxy-Latency*, showing the latency times.

```python
HTTP/1.1 200 OK
Content-Type: application/json
Connection: keep-alive
X-Cache-Status: Miss
x-ratelimit-limit-requests: 10000
CF-RAY: 8fce86cde915eae2-ORD
x-ratelimit-limit-tokens: 10000
x-ratelimit-remaining-requests: 9999
x-ratelimit-remaining-tokens: 9481
x-ratelimit-reset-requests: 8.64s
x-ratelimit-reset-tokens: 3.114s
access-control-expose-headers: X-Request-ID
x-request-id: req_29afd8838136a2f7793d6c129430b341
X-Content-Type-Options: nosniff
openai-organization: user-4qzstwunaw6d1dhwnga5bc5q
Date: Sat, 04 Jan 2025 22:05:00 GMT
alt-svc: h3=":443"; ma=86400
openai-processing-ms: 10002
openai-version: 2020-10-01
CF-Cache-Status: DYNAMIC
strict-transport-security: max-age=31536000; includeSubDomains; preload
Server: cloudflare
Content-Length: 1456
X-Kong-LLM-Model: openai/gpt-4
X-Kong-Upstream-Latency: 10097
X-Kong-Proxy-Latency: 471
Via: 1.1 kong/3.9.0.0-enterprise-edition
X-Kong-Request-Id: 36f6b41df3b74f78f586ae327af27075

{
  "id": "chatcmpl-Am6YEtvUquPHdHdcI59eZC3UfOUVz",
  "object": "chat.completion",
  "created": 1736028290,
  "model": "gpt-4-0613",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "Joseph Conrad was a Polish-British writer regarded as one of the greatest novelists to write in the English language. He was born on December 3, 1857, and died on August 3, 1924. Though he did not speak English fluently until his twenties, he was a master prose stylist who brought a non-English sensibility into English literature.\n\nConrad wrote stories and novels, many with a nautical setting, that depict trials of the human spirit in the midst of what he saw as an impassive, inscrutable universe. His notable works include \"Heart of Darkness\", \"Lord Jim\", and \"Nostromo\". Conrad's writing often presents a deep, pessimistic view of the world and deals with the theme of the clash of cultures and moral ambiguity.",
        "refusal": null
      },
      "logprobs": null,
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 12,
    "completion_tokens": 163,
    "total_tokens": 175,
    "prompt_tokens_details": {
      "cached_tokens": 0,
      "audio_tokens": 0
    },
    "completion_tokens_details": {
      "reasoning_tokens": 0,
      "audio_tokens": 0,
      "accepted_prediction_tokens": 0,
      "rejected_prediction_tokens": 0
    }
  },
  "system_fingerprint": null
}


```

#### Redis introspection

Kong Gateway creates a new index. You can check it with *redis-cli ft._list.* The index should be named like: *idx:vss_kong_semantic_cache:511efd84-117b-4c89-87cb-f92f9b74a6c0:openai-gpt-4*

And *redis-cli ft.search idx:vss_kong_semantic_cache:511efd84-117b-4c89-87cb-f92f9b74a6c0:openai-gpt-4 “*” return 1* – should return the id of OpenAI’s response. Something like:

*1*

*kong_semantic_cache:511efd84-117b-4c89-87cb-f92f9b74a6c0:openai-gpt-4:fcdf7d8995a227392f839b4530f8d8c3055748b96275fa9558523619172fd2a8*

The following* json.get* command should return the actual response received from OpenAI

*redis-cli json.get kong_semantic_cache:511efd84-117b-4c89-87cb-f92f9b74a6c0:openai-gpt-4:fcdf7d8995a227392f839b4530f8d8c3055748b96275fa9558523619172fd2a8 | jq ‘.payload.choices[].message.content’*

More importantly, *redis-cli monitor* tells us all commands the plugin sent to Redis to implement the cache. The main ones are:

1. *“FT.INFO”* to check if the index exists.
1. There’s no index, so create it. The actual command is the following. Notice the index is similar to the one we used in the Python script.

```python
"FT.CREATE" "idx:vss_kong_semantic_cache:511efd84-117b-4c89-87cb-f92f9b74a6c0:openai-gpt-4" "ON" "JSON" "PREFIX" "1" "kong_semantic_cache:511efd84-117b-4c89-87cb-f92f9b74a6c0:openai-gpt-4:" "SCORE" "1.0" "SCHEMA" "$.vector" "AS" "vector" "VECTOR" "FLAT" "6" "TYPE" "FLOAT32" "DIM" "1536" "DISTANCE_METRIC" "COSINE"


```

1. Run a VSS to check if there’s a key which satisfies the request. The command looks like this. Again, notice the command is the same we used in our Python script. The “range” parameter reflects the “threshold” configuration used in the decK declaration.

```python
"FT.SEARCH""idx:vss_kong_semantic_cache:511efd84-117b-4c89-87cb-f92f9b74a6c0:openai-gpt-4" "@vector:[VECTOR_RANGE $range $query_vector]=>{$YIELD_DISTANCE_AS: vector_score}" "SORTBY" "vector_score" "DIALECT" "2" "LIMIT" "0" "4" "PARAMS" "4" "query_vector" "\x981\x87<bE\xe4<b\xa3\..........\xbc" "range" "0.2"


```

1. Since the index has just been created, the VSS couldn’t find any key so the plugin sends a *“JSON.SET”* command to add a new index key with the embeddings received from OpenAI.
1. *“expire”* command to set the expiration time of the key as, by default, 300 seconds.

You can check the new index key using the Redis dashboard:

![](/images/site-mirror/5acc3a3e35b4699fa9cd1fda4520aa5afc3fb981-1933x2043.webp)

### Request #2

If we send another request with similar content, the gateway should return the same response, since it’s going to take from the cache, as noticed in the X-Cache-Status: Hit header. Besides, the response has a specific header related to the cache: X-Cache-Key and X-Cache-Ttl.

The response should be returned faster, since the gateway doesn’t have to route the request to OpenAI.

```python
curl -i -X POST \
  --url $DATA_PLANE_LB/openai-route \
  --header 'Content-Type: application/json' \
   --data '{
   "messages": [
     {
       "role": "user",
       "content": "Tell me more about Joseph Conrad"
     }
   ]
 }'
HTTP/1.1 200 OK
Date: Sun, 05 Jan 2025 14:28:59 GMT
Content-Type: application/json; charset=utf-8
Connection: keep-alive
X-Cache-Status: Hit
Age: 0
X-Cache-Key: kong_semantic_cache:511efd84-117b-4c89-87cb-f92f9b74a6c0:openai-gpt-4:fcdf7d8995a227392f839b4530f8d8c3055748b96275fa9558523619172fd2a8
X-Cache-Ttl: 288
Content-Length: 1020
X-Kong-Response-Latency: 221
Server: kong/3.9.0.0-enterprise-edition
X-Kong-Request-Id: eef1373a3a688a68f088a52f72318315

{"object":"chat.completion","system_fingerprint":null,"id":"fcdf7d8995a22…….


```

If you send another request with non-similar content, the plugin creates a new index key. For example:


```python
curl -i -X POST \
  --url $DATA_PLANE_LB/openai-route \
  --header 'Content-Type: application/json' \
   --data '{
   "messages": [
     {
       "role": "user",
       "content": "Living is easy with eyes closed"
     }
   ]
 }'


```

Check the index keys again with:


```python
redis-cli --scan
"kong_semantic_cache:511efd84-117b-4c89-87cb-f92f9b74a6c0:openai-gpt-4:fcdf7d8995a227392f839b4530f8d8c3055748b96275fa9558523619172fd2a8"
"kong_semantic_cache:511efd84-117b-4c89-87cb-f92f9b74a6c0:openai-gpt-4:22fbee1a1a45147167f29cc53183d0d2eef618c973e4284ad0179970209cf131"


```

## Kong AI Proxy Advanced plugin

Kong AI Gateway provides several semantic-based capabilities besides caching. A powerful one is semantic routing. With such a feature, we can let the gateway decide the best model to handle a given request. For example, you might have models trained in specific topics, like mathematics or classical music, so it’d be interesting to route the requests depending on the presented content. By analyzing the content of the request, the plugin can match it to the most appropriate model that is known to perform better in similar contexts. This feature enhances the flexibility and efficiency of model selection, especially when dealing with a diverse range of AI providers and models.

In fact, semantic routing is one of the load balancing algorithms supported by the [AI Proxy Advanced plugin](https://docs.konghq.com/hub/kong-inc/ai-proxy-advanced/). The other supported algorithms are:

- Round-robin
- Weight-based
- Lowest-usage
- Lowest-latency
- [Consistent-hashing](https://docs.konghq.com/gateway/latest/how-kong-works/load-balancing/#consistent-hashing) (sticky-session on given header value)

For the purpose of this blog post we are going to explore the semantic routing algorithm.

The diagram below shows how the AI Proxy Advanced plugin works:

- At the configuration time, the plugin sends requests to an embeddings model based on descriptions defined. The embeddings returned are stored in a Redis vector database.
- During request processing time, the plugin gets the request content and sends a VSS query to the Redis vector database. Depending on the similarity score, the plugin routes the request to the best targeted LLM model sitting behind the gateway.

![](/images/site-mirror/0c8824795a6c83bf47ddfc08562a2eaed2ff6e6e-952x537.webp)

Here’s the new decK declaration:


```python
_format_version: "3.0"
_info:
  select_tags:
  - semantic-routing
_konnect:
  control_plane_name: default
services:
- name: service1
  host: localhost
  port: 32000
  routes:
  - name: route1
    paths:
    - /openai-route
    plugins:
    - name: ai-proxy-advanced
      instance_name: ai-proxy-openai-route
      enabled: true
      config:
        balancer:
          algorithm: semantic
        embeddings:
          auth:
            header_name: Authorization
            header_value: Bearer <your_OPENAI_APIKEY>
          model:
            provider: openai
            name: text-embedding-3-small
            options:
              upstream_url: "https://api.openai.com/v1/embeddings"
        vectordb:
          dimensions: 1536
          distance_metric: cosine
          strategy: redis
          threshold: 0.8
          redis:
            host: redis-stack.redis.svc.cluster.local
            port: 6379
        targets:
        - model:
            provider: openai
            name: gpt-4
          route_type: "llm/v1/chat"
          auth:
            header_name: Authorization
            header_value: Bearer <your_OPENAI_APIKEY>
          description: "mathematics, algebra, calculus, trigonometry"
        - model:
            provider: openai
            name: gpt-4o-mini
          route_type: "llm/v1/chat"
          auth:
            header_name: Authorization
            header_value: Bearer <your_OPENAI_APIKEY>
          description: "piano, orchestra, liszt, classical music"


```

The main configuration sections are:

- *balancer* with *algorithm: semantic* telling the load balancer will be based on semantic routing.
- e*mbeddings* with the necessary setting to reach out the embedding model. The same observations made previously regarding the API Key remain here.
- *vectordb* with the Redis host and index configurations as well as the threshold to drive the VSS query.
- *targets:* each one of them represents a LLM model. Note the *description *parameter is used to configure the load balancing algorithm according to the topic the model has been trained for.

As you can see, for convenience’s sake, the configuration uses OpenAI’s model for embeddings and targets. Also, just for this exploration, we are also using the* gpt-4* and *gpt-4o-mini* OpenAI’s models for the targets.

After submitting the decK declaration to Konnect control plane, the Redis vector database should have a new index defined and a key for each target created. We can then start sending requests to the gateway. The first two requests have contents related to classical music, so the response should come from the related model, *gpt-4o-mini-2024-07-18.*

```python
% curl -s -X POST \
  --url $DATA_PLANE_LB/openai-route \
  --header 'Content-Type: application/json' \
  --data '{
    "messages": [ 
      { 
        "role": "user", 
        "content": "Who wrote the Hungarian Rhapsodies piano pieces?"
      } 
    ] 
  }' | jq '.model' 
"gpt-4o-mini-2024-07-18"

% curl -s -X POST \
  --url $DATA_PLANE_LB/openai-route \
  --header 'Content-Type: application/json' \
  --data '{
    "messages": [
      {
        "role": "user",
        "content": "Tell me a contemporary pianist of Chopin"
      }
    ]
  }' | jq '.model'
"gpt-4o-mini-2024-07-18"

```

Now, the next request is related to mathematics, therefore the response comes from the other model,

```python
"gpt-4-0613".

% curl -s -X POST \
  --url $DATA_PLANE_LB/openai-route \
  --header 'Content-Type: application/json' \
  --data '{
     "messages": [
       {
         "role": "user",
         "content": "Tell me about Fermat''s last theorem"
       }
     ]
   }' | jq '.model'
"gpt-4-0613"

```

## Conclusion

Kong has historically supported Redis to implement a variety of critical policies and use cases. The most recent collaborations, implemented by the Kong AI Gateway, focus on semantic processing where Redis vector similarity search capabilities play an important role.

This blog post explored two main semantic-based use cases: semantic caching and semantic routing. Check Kong’s and Redis’ documentation pages to learn more about the extensive list of API and AI gateway use cases you can implement using both technologies.
