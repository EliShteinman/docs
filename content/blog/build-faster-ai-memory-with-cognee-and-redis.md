---
title: "Build faster AI memory with Cognee & Redis"
linkTitle: "Build faster AI memory with Cognee & Redis"
url: "/blog/build-faster-ai-memory-with-cognee-and-redis/"
description: "Large language models are powerful, but they forget quickly. For AI agents and assistants to be truly useful, they need memory: the ability to retain instructions, recall facts, and carry context..."
date: 2025-07-08
blogCategories:
- "Tech"
authors:
- "Rini Vasan"
- "Hande Kafkas"
lastmod: 2026-06-01
hidden: true
mirrored: true
---

*By Rini Vasan, Hande Kafkas · Published 8 July 2025 · updated 1 June 2026*

![Build faster AI memory with Cognee & Redis](/images/site-mirror/8a851d6329fca22ec8dd40add23868615a74b01a-772x552.webp)

Large language models are powerful, but they forget quickly. For AI agents and assistants to be truly useful, they need memory: the ability to retain instructions, recall facts, and carry context over time. [Cognee](https://github.com/topoteretes/cognee) is an open-source memory engine that addresses this challenge by organizing unstructured content into structured memory using both semantic vectors and graph-based relationships.

Now, with [Redis as a supported integration](https://github.com/topoteretes/cognee-community/tree/main/packages/vector/redis), Cognee pipelines can run on a memory backend that is fast, accurate, and scalable. Whether you are building autonomous agents, chatbots, or retrieval-augmented generation (RAG) systems, Cognee and Redis together offer a powerful foundation for structured and persistent memory.

## Faster memory for AI workflows

Cognee is built around a modular Extract, Cognify, and Load (ECL) pipeline. In the extract phase, developers ingest raw content from sources such as APIs, databases, or documents. The cognify phase enriches that content by splitting it into chunks, generating embeddings, identifying key entities, and mapping relationships. Finally, the load step writes both the vector representations and the graph connections to memory backends.

With the Redis integration, Cognee users can now store both types of memory, semantic vectors and structured relationships, using a single system. Vectors are indexed through Redis’ vector database using RedisVL, the Redis Vector Library.

Here’s a look at the high-level architecture of Cognee.

![High-level architecture of Cognee](/images/site-mirror/e35be297d4b077bac5a5eb3f727e007af2294178-2980x1273.webp)

## How it works

Cognee’s memory pipeline is designed to connect with a variety of backends through lightweight adapters. Redis fits naturally into this model, acting as both a vector database and an interface for storing structured relationships.

As embeddings are generated during the cognify step, they are stored in Redis through RedisVL, which handles index setup and similarity search. For graph-based relationships—such as reply chains, topic links, or entity associations—Cognee supports writing to external graph databases. One option currently supported is [Kuzu](https://kuzudb.com), a high-performance, open-source graph database purpose-built for analytical workloads and optimized for knowledge graph use cases.

By combining Redis for vector memory and Kuzu for structured relationships, developers can build memory systems that support both fast semantic search and deep contextual reasoning across connected knowledge.

## Here’s an example

The script below helps demonstrate how Cognee works with a simple example. It introduces Cognee’s default pipelines add() and cognify(), core concepts like NodeSets to isolate information in graphs, and search functionality for querying memory.

```
import os
import asyncio
import pathlib
from os import path

# Provide your OpenAI API Key
os.environ["LLM_API_KEY"]=""

node_set_a = ["AI", "FinTech"]
node_set_b = ["AI"]
node_set_c = ["MedTech"]

async def main():
    from cognee import config, prune, add, cognify, search, SearchType
    from cognee.modules.engine.models import NodeSet


    # NOTE: Import register module to let cognee use the Redis vector adapter
    from cognee_community_vector_adapter_redis import register

    # Provide your Redis instance url
    config.set_vector_db_config({
        "vector_db_provider": "redis",
        "vector_db_url": "redis://localhost:6379",
        "vector_db_key": "",
    })

    await prune.prune_data()
    await prune.prune_system()

    doc_a = """
    AI is revolutionizing financial services through intelligent 
    fraud detection and automated customer service platforms.
    """

    doc_b = """
    Advances in AI are enabling smarter systems that learn and adapt 
    over time.
    """

    doc_c = """
    MedTech startups have seen significant growth in recent years, driven
    by innovation in digital health and medical devices.
    """

    await cognee.add(doc_a, node_set=node_set_a)
    await cognee.add(doc_b, node_set=node_set_b)
    await cognee.add(doc_c, node_set=node_set_c)

    await cognify()

    answer_1 = await cognee.search(
        query_text="Which industries are affected by the tech  advancements?",
        query_type=SearchType.GRAPH_COMPLETION,
        node_type=NodeSet,
        node_name=node_set_c,
    )

    print("-------Answer with NodeSet------")
    print(answer_1)

    answer_2 = await cognee.search(
            query_text="Which industries are affected by the tech advancements?",
            query_type=SearchType.GRAPH_COMPLETION,
        )
    print("----Answer without NodeSet--------")
    print(answer_2)
    
if __name__ == "__main__":
    asyncio.run(main())

```

The output of this simple example will be as follows:

```
-------Answer with NodeSet------
['The industries affected by tech advancements include MedTech, digital health, and medical devices.']

----Answer without NodeSet--------
['The industries affected by tech advancements include:\n1. MedTech (Medical Technology)\n2. Financial Services\n3. Digital Health\n4. Customer Service Automation']

```

![Making sense of node sets](/images/site-mirror/a85af6b14a3e3ce8f98166e67601a081be323b1f-789x741.webp)

#### Making sense of node sets

One detail tucked into the example above is the NodeSet argument, and it’s worth pausing on why it matters. Node Sets act like labels you can pin on any incoming document (“AI”, “FinTech”, “MedTech”, …). When Cognee stores the content, it automatically creates belongs_to_set() edges that connect each fact, chunk, or entity back to its set label. Later, you can pass that same label into cognee.search() to fence your query to just that thematic island—or widen the scope by leaving the filter off. In short, Node Sets give you topic isolation without spinning up separate databases or clusters—it’s tagging that actually understands graph structure.

#### Associative Memory

Under the hood, every piece of information in Cognee is born as a DataPoint—a strongly typed Pydantic object that doubles as both a node schema and an edge schema. The moment you feed a DataPoint into cognify pipeline, Cognee:

1. Assigns a UUID, version, and timestamp.
1. Recursively unpacks nested DataPoints (e.g., a Company that references many Person founders).
1. Deduplicates identical entities and indexes the fields you mark as important (index_fields = ["name"]).
1. Embeds those fields so they’re instantly searchable via vectors.

Because every DataPoint can reference any other, Cognee builds associative memory on the fly—capturing not just what something is, but how it connects to everything else.

#### Mix and match your backend

Cognee is deliberately poly-store. You can choose:

- Graphs → Neo4j for rich production graphs, KuzuDB for embedded analytics, FalkorDB if you love Redis-based speed, or even NetworkX when you’re prototyping in-memory.
- Vectors → Redis, Qdrant, Weaviate, Milvus, PGVector, Chroma, or LanceDB (the zero-setup default).
- Relational metadata → SQLite for local work or Postgres when you need concurrency and persistence.

## Why Redis

Cognee pipelines require a memory layer that’s fast, accurate, and scalable. Redis provides all three. With millisecond response times and support for high-throughput workloads, Redis ensures that memory retrieval stays efficient even at production scale. Redis also supports features like hybrid filtering, full-text indexing, and time-based expiration, which makes it easy to manage both short-term and persistent memory.

RedisVL simplifies integration by offering a declarative interface for defining schemas, loading embeddings, and running queries. It removes setup complexity and allows developers to quickly plug Redis into any AI workflow.

Together, Cognee and Redis provide a high-performance memory stack that supports both flexible reasoning and real-time access, ideal for powering modern AI applications.

### Use Redis for short-term memory in Cognee

Because Cognee’s graph enrichment takes a moment to run, there’s value in handing new information over to a temporary “waiting room.” One simple pattern is to stream every fresh chunk straight into Redis the moment it arrives. Redis then serves as a lightning-fast, short-term cache— agents can query the latest chat turns or events in real time, long before those facts are fully parsed and woven into the knowledge graph.

Once the pipeline finishes extracting entities and relationships, the enriched data is promoted to long-term graph storage and the transient copy in Redis can be safely evicted. This staging-plus-handoff approach keeps conversations immediately searchable while still giving Cognee the breathing room it needs to build durable, structured memory. One use case is chat messages between the agent and the human. The agent needs to be aware of the current conversation, and with Redis that conversation will be remembered instantly.

## What’s next

The Redis integration is available now in the [Cognee community repository](https://github.com/topoteretes/cognee-community/tree/main/packages/vector/redis) and is being actively developed. Future updates will include enhanced support for hybrid search, time-based memory expiration, and richer examples that show how Redis can work alongside frameworks like LangChain and LlamaIndex.

This integration gives developers a clear and maintainable way to combine semantic embeddings with graph-based structures, using Redis as a unified backend for AI memory.

## Try it out

**Build your own AI memory app**: [Book a meeting with the Redis team](https://redis.com/contact/) to talk through use cases or architecture.

**Sign-up for early access to enjoy hosted Cognee:** [Cognee SaaS Beta is launching soon](https://www.cognee.ai/waitlist)

**Explore Cognee**: Clone [cognee repo](https://github.com/topoteretes/cognee) and learn how to build pipelines, define memory tasks, and use adapters at [docs.cognee.ai](https://docs.cognee.ai).

**View the Redis adapter**: Check out the open-source integration in the Cognee community repo [here](https://github.com/topoteretes/cognee-community/tree/main/packages/vector/redis).

**Use Redis for vector search**: Install and configure [RedisVL](https://github.com/redis/redis-vl-python) to manage embeddings, indexing, and queries.

**Ask your questions: **Join Cognee [Discord community](https://discord.com/invite/cqF6RhDYWz), [the Redis Discord server](https://discord.com/invite/redis), and bring your thoughts to the [AI memory subreddit](https://www.reddit.com/r/AIMemory/)
