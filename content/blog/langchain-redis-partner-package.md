---
title: "LangChain Redis Package: Smarter AI apps with advanced vector storage and faster caching"
linkTitle: "LangChain Redis Package: Smarter AI apps with advanced vector storage and faster caching"
url: "/blog/langchain-redis-partner-package/"
description: "Introducing langchain-redis, our new partner package integrating Redis capabilities with the LangChain ecosystem. This collaboration gives developers the tools they need to build fast AI apps,..."
date: 2024-09-11
blogCategories:
- "Tech DE"
authors:
- "Brian Sam-Bodden"
lastmod: 2026-06-01
hidden: true
---

*By Brian Sam-Bodden, Principal Applied AI Engineer · Published 11 September 2024 · updated 1 June 2026*

![Blog tile image](/images/site-mirror/987201315c1d3724d9c52a12121b972b3a9c29f6-772x552.webp)

Introducing [langchain-redis](https://github.com/langchain-ai/langchain-redis), our new partner package integrating Redis capabilities with the LangChain ecosystem. This collaboration gives developers the tools they need to build fast AI apps, especially those powered by Retrieval Augmented Generation (RAG).

[LangChain](https://www.langchain.com/langchain) is an open-source framework used by 1M+ developers to build their GenAI applications. With its community-driven integrations, LangChain lets users flexibly choose their chat model providers, vector stores, embedding models, retrievers, and other tools. LangChain v0.2 introduced **partner packages**, co-maintained integrations with technology partners. The latest one, langchain-redis, brings Redis features to LangChain users.

## Why Redis for AI apps?

Redis is a top choice for AI apps, especially when it comes to real-time RAG. Here’s why:

1. **Memory-first efficiency: **Built for real-time processing with versatile data structures
1. **High-performance vector features: **Fast vector search and robust built-in search engine
1. **Advanced caching: **Efficient LLM memory and semantic caching for improved performance
1. **Scalability: **Scales with your AI apps as data and compute needs grow
1. **Flexible deployment: **Easy switching between on-premise and fully-managed cloud options

## How langchain-redis works

Our new package taps into Redis’ strengths to provide three core features:

### 1. RedisVectorStore: Fast similarity searches with advanced vector storage

The RedisVectorStore class uses Redis’ vector similarity capabilities for:

- Efficient storage and retrieval of high-dimensional vector embeddings
- Support for multiple distance metrics (Cosine, L2, Inner Product)
- Advanced metadata filtering for refined searches
- Maximum marginal relevance search for enhanced result diversity

### 2. RedisCache and RedisSemanticCache: Cut costs and improve response times

To make your Language Model interactions faster and more cost-effective, we’re rolling out two caching mechanisms:

- RedisCache: A standard key-value cache for exact matches
- RedisSemanticCache: An advanced cache using semantic similarity for flexible retrieval

### 3. RedisChatMessageHistory: Boost conversational context for a better user experience

The RedisChatMessageHistory class gives you a Redis-powered way to handle chat history:

- Persistent storage of chat messages across sessions
- Support for various message types (Human, AI, System)
- Efficient message searching capabilities
- Automatic expiration with TTL support

LLM memory keeps track of context across conversations and sessions for:

- **Improved personalization: **The system understands user preferences and tailors responses accordingly.
- **Enhanced context awareness:** LLMs connect current queries with previous chats for more accurate and relevant responses.
- **Continuity in conversations: **By referencing past interactions, the system creates a more natural and engaging user experience.

## Practical Examples

Here are some practical examples that show what langchain-redis can do:

### Setting Up

First, install the necessary packages:

```python
pip install langchain-redis langchain-openai redis

```

Set up your Redis connection:

```python
import os

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
print(f"Connecting to Redis at: {REDIS_URL}")

```

### RedisVectorStore Example

Let’s create a vector store and populate it with some sample data:

```python
from langchain_redis import RedisVectorStore
from langchain_openai import OpenAIEmbeddings
from langchain.docstore.document import Document

# Initialize RedisVectorStore
embeddings = OpenAIEmbeddings()
vector_store = RedisVectorStore(embeddings, redis_url=REDIS_URL, index_name="my_docs")

# Add documents
docs = [
    Document(page_content="Redis is a powerful in-memory data structure store", metadata={"source": "redis_intro"}),
    Document(page_content="LangChain is a framework for developing applications powered by language models", metadata={"source": "langchain_intro"}),
]
vector_store.add_documents(docs)

# Perform a similarity search
query = "What is Redis?"
results = vector_store.similarity_search(query)
print(f"Search results for '{query}':")
for doc in results:
    print(f"- {doc.page_content} (Source: {doc.metadata['source']})")


```

### Efficient caching with Redis: Traditional and semantic approaches

Caching is a key for making RAG systems faster, cheaper, and more responsive. The LangChain Redis partner package gives you two powerful caching mechanisms: RedisCache and RedisSemanticCache.

1. RedisCache: a traditional key-based caching system for LLM responses that stores exact matches between queries and their corresponding LLM outputs.

Benefits:

- Cuts down on API calls for repeated queries
- Speeds up response times for cached queries
- Lets you build more complex RAG pipelines without proportional cost increases

2. RedisSemanticCache: Intelligent similarity-based caching that uses the semantic meaning of queries to find similar past requests, even when the wording is different.

Benefits:

- Recognizes and serves responses for semantically similar queries (e.g., “What’s the capital of France?” and “Tell me the capital city of France”)
- Boosts cache hit rates by capturing variations of the same question
- Lightens loads on retrieval systems and language models

### Adding Traditional Caching

Let’s see how easy it is to add traditional caching to your LLM interactions:

```python
from langchain_redis import RedisCache
from langchain_openai import OpenAI
from langchain.globals import set_llm_cache
import time

# Initialize RedisCache
redis_cache = RedisCache(redis_url=REDIS_URL)
set_llm_cache(redis_cache)

# Initialize the language model
llm = OpenAI(temperature=0)

# Function to measure execution time
def timed_completion(prompt):
    start_time = time.time()
    result = llm.invoke(prompt)
    end_time = time.time()
    return result, end_time - start_time

# First call (not cached)
prompt = "Explain the concept of caching in three sentences."
result1, time1 = timed_completion(prompt)
print(f"First call (not cached):\nResult: {result1}\nTime: {time1:.2f} seconds\n")

# Second call (should be cached)
result2, time2 = timed_completion(prompt)
print(f"Second call (cached):\nResult: {result2}\nTime: {time2:.2f} seconds\n")

print(f"Speed improvement: {time1 / time2:.2f}x faster")


```

### Adding Semantic Caching

Here’s howRedisSemanticCache can intelligently reuse LLM responses against semantically similar queries:

```python
from langchain_redis import RedisSemanticCache
from langchain_openai import OpenAIEmbeddings

# Initialize RedisSemanticCache
embeddings = OpenAIEmbeddings()
semantic_cache = RedisSemanticCache(redis_url=REDIS_URL, embeddings=embeddings, distance_threshold=0.2)
set_llm_cache(semantic_cache)

# Test semantic caching
original_prompt = "What is the capital of France?"
result1, time1 = timed_completion(original_prompt)
print(f"Original query:\nPrompt: {original_prompt}\nResult: {result1}\nTime: {time1:.2f} seconds\n")

similar_prompt = "Can you tell me the capital city of France?"
result2, time2 = timed_completion(similar_prompt)
print(f"Similar query:\nPrompt: {similar_prompt}\nResult: {result2}\nTime: {time2:.2f} seconds\n")

print(f"Speed improvement: {time1 / time2:.2f}x faster")


```

### Chat message history: Contextual understanding in RAG

Chat history is key for maintaining context and making AI conversations flow naturally, especially in RAG systems. By storing and referencing past interactions, a RAG system can deliver responses that feel more coherent and relevant. Searching within this history adds another layer of sophistication.

For instance, if a user mentions something discussed earlier, the system can quickly retrieve relevant parts of the conversation, and combine it with this new information to give smarter answers. This leads to a more natural, continuous conversation flow and allows the RAG system to build on previous interactions, just like a human would.

Let’s put RedisChatMessageHistory to work:

```python
from langchain_redis import RedisChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory

# Initialize RedisChatMessageHistory
message_history = RedisChatMessageHistory("user_123", redis_url=REDIS_URL)

# Create a conversational chain
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful AI assistant."),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}")
])
chain = prompt | llm

# Function to get or create a RedisChatMessageHistory instance
def get_redis_history(session_id: str):
    return RedisChatMessageHistory(session_id, redis_url=REDIS_URL)

# Create a runnable with message history
chain_with_history = RunnableWithMessageHistory(
    chain,
    get_redis_history,
    input_messages_key="input",
    history_messages_key="history"
)

# Use the chain in a conversation
response1 = chain_with_history.invoke(
    {"input": "Hi, my name is Alice."},
    config={"configurable": {"session_id": "alice_123"}}
)
print("AI Response 1:", response1.content)

response2 = chain_with_history.invoke(
    {"input": "What's my name?"},
    config={"configurable": {"session_id": "alice_123"}}
)
print("AI Response 2:", response2.content)


```

## Your AI apps just got faster, smarter

The langchain-redis partner package is a big leap forward in Redis’ mission to give developers the tools they need to build powerful AI apps. With Redis’ speed, flexibility, and scalability, we’re making it easier to create AI apps that can handle complex, real-time interactions with ease.

Here’s what you get with langchain-redis:

1. **Efficient information retrieval**: The vector store gives you quick access to relevant information from large datasets.
1. **Improved response time**: Caching cuts down API calls for similar or repeated queries.
1. **Contextual understanding**: The chat history lets AI reference previous parts of the conversation, making the interactions smoother and more natural.
1. **Scalability**: With Redis as the backend, the system can handle large amounts of data and high traffic smoothly.

We’re just getting started with this integration, and we can’t wait to see where it leads. From smarter caching to advanced vector search algorithms, the LangChain and Redis combination is ready to push the boundaries of AI.

Explore this new package, experiment with its features, and send us your feedback. Your insights and use cases will shape the future of this integration, making sure it meets the evolving needs of the AI development community.

Check out the langchain-redis package repository at [https://github.com/langchain-ai/langchain-redis](https://github.com/langchain-ai/langchain-redis) and the pre-packaged library on PyPi at [https://pypi.org/project/langchain-redis/](https://pypi.org/project/langchain-redis/).

Stay tuned and keep coding. Let’s build fast AI apps even faster with Redis and LangChain.
