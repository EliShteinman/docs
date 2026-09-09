---
title: "Build AI agents with short-term & long-term memory in Redis"
linkTitle: "Build AI agents with short-term & long-term memory in Redis"
url: "/blog/build-smarter-ai-agents-manage-short-term-and-long-term-memory-with-redis/"
description: "AI agent memory is the system that lets an agent store, retrieve, and reuse information across interactions instead of starting over on every request. Getting there is one of the trickier parts of..."
date: 2026-07-01
blogCategories:
- "Tech DE"
authors:
- "Jim Allen Wallace"
lastmod: 2026-07-01
hidden: true
---

*By Jim Allen Wallace, Sr. Product Marketing Manager · Published 1 July 2026*

![Blog tile image](/images/site-mirror/2f24410ddbba1792c86c3e2e6905575e2a8a2852-1200x628.webp)

AI agent memory is the system that lets an agent store, retrieve, and reuse information across interactions instead of starting over on every request. Getting there is one of the trickier parts of building AI agents. Large language models (LLMs) are stateless at their core—the model itself doesn't retain information between API calls. Products like ChatGPT and Claude layer memory systems on top, which is why they remember your name and preferences. But when you're building your own agents, you need to implement that memory layer yourself.

Building memory that spans conversations, learns preferences over time, and retrieves relevant context when needed requires deliberate architectural decisions. The challenge is that agent memory isn't one thing. Most production agents need short-term context for coherent conversations, long-term storage for learned preferences, and semantic retrieval for surfacing relevant memories. All of this must be fast enough that users don't notice the overhead. Most teams underestimate this until they're deep into development.

This guide covers how to build AI agents with memory that spans conversations, and how to unify these patterns on a single platform rather than stitching together separate vector databases, [caching layers](https://redis.io/solutions/caching/), and session stores. Agent memory spans multiple storage patterns simultaneously, and managing these across separate systems introduces additional latency and operational complexity.

## Why does AI agent memory matter?

Memory is what lets an agent learn from past interactions, retain information, and hold context across a task, producing more coherent and personalized responses. Without it, every interaction starts from zero.

Imagine an AI agent designed to plan and book work trips. Without memory, it won't remember personal preferences (e.g., "Do you like direct flights or flights with layovers?"); make procedural mistakes due to lack of understanding (e.g., booking a hotel that does not offer the amenities required for business trips, like meeting rooms or reliable Wi-Fi); and fail to recall previously provided details like passport information. This leads to a frustrating user experience with repetitive questions, inconsistent behaviour, and a lack of personalisation.

The impact shows up immediately in production. [Relevance AI](https://redis.io/customers/relevance-ai/) reduced vector search latency from 2 seconds to 10 milliseconds after migrating their vector search and caching to Redis—a 99.5% improvement in their environment.

## Short-term & long-term memory

Building AI agents requires implementing multiple memory types that work together. Short-term memory handles immediate conversational context, serving as working memory that maintains coherence within a single interaction. Long-term memory persists across conversations, allowing agents to learn from feedback and adapt to user preferences over time.

### Short-term memory

Short-term memory functions like RAM, holding relevant details for ongoing tasks but existing only briefly within a conversation thread. It faces two constraints: LLM context windows limit how much information can be actively maintained, and irrelevant information can pollute the context and degrade agent reasoning quality.

Managing short-term memory effectively requires frameworks that provide structured state management. [LangGraph](https://langchain-ai.github.io/langgraph/concepts/memory/) addresses this through Checkpointers, which are tools that maintain thread-specific context and enable agents to store conversational state in high-performance databases. Redis [can store agent state](/blog/langgraph-redis-build-smarter-ai-agents-with-memory-persistence/) with <1ms read/write latency in many workloads, helping agents retrieve conversational context quickly so users often experience no noticeable delay. This matters because agents make multiple context retrievals during complex reasoning loops, and latency compounds across these operations.

### Long-term memory

Long-term memory functions more like a hard drive, storing information that can be accessed later when contextually relevant. It divides into three distinct types, each serving different agent capabilities (for more on these distinctions, see the [CoALA framework](https://arxiv.org/pdf/2309.02427) paper):

- **Episodic memory** stores specific past events and experiences, creating a personal history of interactions. A travel agent might remember that a user previously booked a trip to London for a conference and prefers city-center hotels.
- **Procedural memory** stores learned skills and operational knowledge, forming the agent's repertoire of effective actions. An agent could learn the optimal process for booking flights, like ensuring appropriate layover times or avoiding specific airports based on past connection failures.
- **Semantic memory** stores general knowledge, facts, and relationships the agent draws on—often backed by a knowledge base (such as visa rules, policies, or FAQs) retrieved when contextually relevant.

Together, these memory types enable personalized recommendations grounded in past behavior, improved execution strategies through experience, and domain-specific reasoning retrieved when contextually relevant.

### Short-term vs. long-term memory at a glance

|  | Short-term memory | Long-term memory |
|---|---|---|
| Analogy | RAM | Hard drive |
| Lifespan | Single conversation thread | Persists across sessions |
| Storage in Redis | In-memory data structures (hash, JSON) with sub-millisecond read/write | Vector embeddings for semantic retrieval, plus structured stores for extracted facts |
| Example use case | Tracking steps in a multi-step booking request | Remembering a user's hotel preferences from a trip three months ago |

### The complexity most teams underestimate

Managing these memory types introduces challenges that surface during development, not planning. You need to decide which memory types your app actually requires, determine what information deserves persistence versus what can be discarded, implement decay strategies so older irrelevant memories don't pollute retrieval, and design retrieval mechanisms that surface the right memories for current contexts. These decisions shape both agent effectiveness and infrastructure costs.

## Key architectural decisions for agent memory

Four decisions shape your memory architecture: what to store, how to store it, how to retrieve it, and when to forget it.

### Choosing memory types

Not every agent needs all memory types. A customer support agent needs episodic memory for interaction history across tickets. A product recommendation agent needs semantic memory for product specs and relationships. A coding assistant needs procedural memory for learned debugging strategies. Match your architecture to your use case rather than adding complexity for theoretical requirements.

### Storing & updating memories

Context pollution, where irrelevant information degrades reasoning quality, means you need strategies to compress and organize memories. Three approaches commonly work well in production:

- **Summarization** condenses conversations using an LLM to extract key points. The memory module incrementally updates summaries as new data arrives, storing them as strings in Redis for retrieval during future queries. The [Redis Agent Memory Server](https://github.com/redis/agent-memory-server) demonstrates this pattern. The tradeoff: you risk losing details that seem irrelevant now but matter later.
- **Vectorization** converts memories into vector embeddings for semantic search based on conceptual similarity rather than keywords. Segment memories into [discrete chunks](/blog/llm-chunking/). [Semantic chunking](https://docs.llamaindex.ai/en/stable/examples/node_parsers/semantic_chunking/) that preserves natural boundaries often works better than fixed-length splits. Then use vector search to retrieve relevant memories.
- **Extraction** pulls key facts, entities, and preferences into structured formats. A document store like RedisJSON stores these extracted facts with context, producing compact representations that support exact matching and range queries. The LangChain team's [memory agent example](https://github.com/langchain-ai/memory-agent) demonstrates this approach.

Most production agents combine multiple techniques based on memory type and retrieval patterns.

### Retrieving memories

Many production systems use hybrid retrieval: structured lookups first (exact match on user IDs, preferences, timestamps) with vector search as a second pass for semantic relevance. Vector search provides the semantic foundation—embed the current context, then search for stored embeddings with high similarity. More sophisticated approaches like [MemGPT](https://arxiv.org/abs/2310.08560) implement hierarchical systems where agents explicitly decide when to pull from long-term memory, generating queries via function calls. For most apps, start with vector search and add complexity only when retrieval quality becomes a bottleneck.

### Managing memory decay

Without decay mechanisms, memory systems can grow unbounded and retrieval quality tends to degrade as irrelevant memories pollute results. Two practical approaches: add timestamps as metadata and weight recent memories higher during retrieval, or use Redis' built-in [eviction and expiration policies](https://redis.io/docs/latest/develop/reference/eviction/) to automatically remove old data. You can combine both by expiring stale memories automatically while using recency scoring for memories that persist.

## Why Redis is a strong choice for agent memory

Everything above describes patterns you can build yourself. Redis Iris is where those patterns become managed infrastructure. [Redis Iris](https://redis.io/iris/) is a real-time context engine for agents, and Redis Agent Memory is the component built for this problem: keeping short-term conversation context tight while persisting long-term details like user preferences and past decisions across sessions, channels, and agents.

Under that layer, Redis fits agent memory because it combines the storage patterns agents need in one platform:

- **Fast performance:** Reading and writing memories sits on the hot path of your app. Slow retrieval degrades UX or forces trade-offs against optimal performance. The in-memory architecture of Redis provides sub-millisecond latency for many workloads, and Iris reports under 250ms P95 query latency across production workloads.
- **Fast, fully featured vector search:** Redis provides native vector indexing and search for vector database workloads. Redis' [published benchmarks](/blog/benchmarking-results-for-vector-databases/) report higher throughput at recall ≥0.98 than the other vector databases included in those tests. Since memories are vectorized and retrieved by semantic similarity, vector performance matters when you pick a data platform.
- **Integrated with your AI stack:** Redis supports integrations across popular AI frameworks, including [LangGraph persistence](https://langchain-ai.github.io/langgraph/how-tos/persistence_redis/), [LlamaIndex vector store](https://docs.llamaindex.ai/en/stable/examples/vector_stores/RedisIndexDemo/), and a [Redis-backed AutoGen cache](https://microsoft.github.io/autogen/0.2/docs/reference/cache/redis_cache/). [RedisVL](https://docs.redisvl.com/en/latest/) gives Python devs high-level abstractions for GenAI apps, including managing conversational memory.
- **Scalability:** Storage needs, client counts, and retrieval frequency are hard to predict for agentic systems. Redis offers clustering, high availability, and persistence options for large-scale deployment. Redis Flex adds tiered storage across RAM and SSD to cut costs for less frequently accessed data.
- **Flexibility:** Redis offers several data structure options out of the box. [Data structures](https://redis.io/technology/data-structures/) like hash (for streamlined efficiency) or JSON (for nested documents) let devs implement memory however they prefer.

If you want to see the patterns in code first, the open source [Redis Agent Memory Server](https://github.com/redis/agent-memory-server) is the reference implementation that Redis Agent Memory productizes as a managed service.

## Example of agent memory using LangGraph & Redis

Here's how these patterns come together in practice using LangGraph and Redis.

### Short-term memory with checkpointing

LangGraph's checkpointing system maintains thread-specific state across agent reasoning loops. When an agent receives a message, performs reasoning, calls tools, and generates responses, the checkpointer persists state at each step. This enables graceful error recovery, allowing agents to resume from the last successful checkpoint rather than restarting. It also lets users pause and resume conversations without losing context.

The [LangGraph Redis checkpointer](https://github.com/redis-developer/langgraph-redis) provides RedisSaver to store checkpoints with automatic serialization. Each checkpoint includes conversation history, tool results, and intermediate reasoning artifacts. When users send new messages, the agent loads the latest checkpoint and continues from that point.

### Long-term memory with vector search

Long-term memory persists across conversation boundaries and needs semantic retrieval rather than sequential access. RedisVL provides high-level abstractions for storing memories as vector embeddings. You break memories into semantic chunks, generate embeddings with your chosen model, then store vectors with metadata like timestamps and user IDs that enable hybrid search combining similarity with exact filtering.

Retrieval embeds the current conversation context and searches for semantically similar stored memories. A user asking "Where did we decide to go last month?" retrieves memories based on meaning and temporal relevance rather than requiring exact keyword matches.

### Memory consolidation

Raw conversation transcripts can grow unbounded without active management. Consolidation strategies periodically extract salient information, merge redundant entries, and discard irrelevant details. Common approaches include using LLMs to summarize conversation clusters, or extracting factual claims into structured data separate from episodic memories.

### Manual vs. tool-based memory access

Manual management means your application code controls when to retrieve and store memories. This gives you tight control but requires explicit logic for each interaction. Tool-based access exposes memory operations as tools the agent can call autonomously, increasing flexibility at the cost of occasional suboptimal patterns.

Production implementations typically combine both: critical operations like checkpoint storage happen automatically, while optional operations like searching past conversations become tools the agent invokes when appropriate.

### Reference implementation

The [Redis Agent Memory Server](https://github.com/redis/agent-memory-server) demonstrates these patterns as an open-source reference. It integrates with LangGraph to manage conversational context via checkpointing and provides semantic memory retrieval through vector search. Deploy it as a standalone service or adapt the patterns for your own infrastructure.

## Starting your AI agent development journey

Building your first agent with proper memory management starts with the [LangGraph framework](https://langchain-ai.github.io/langgraph/concepts/persistence/), which provides structured patterns for stateful agent workflows. Start with basic checkpointing that maintains conversation history within single threads, then add long-term memory by storing conversation summaries as vector embeddings. Advanced implementations layer in procedural memory for learned operational strategies and semantic memory for domain knowledge bases.

The Redis ecosystem provides resources to accelerate development. The Redis Agent Memory Server offers ready-to-deploy memory management. [Redis AI resources](https://github.com/redis-developer/redis-ai-resources) include code samples and Jupyter notebooks for common agent scenarios. The [Redis AI documentation](https://redis.io/docs/latest/develop/ai/) covers vector search, semantic caching, and framework integrations.

Redis provides a unified infrastructure that makes agent memory architectures practical at scale: vector search, in-memory storage, flexible data structures, and built-in eviction policies in one platform.

Try [Redis Iris](https://redis.io/try-free/?rcplan=iris) to build agent memory on a managed real-time context engine, or [talk to Redis experts](https://redis.io/meeting/) about production agent memory systems.

## FAQs

### Why does memory management matter for AI agents?

Memory management lets AI agents retain context and learn from past interactions instead of operating statelessly on every request. Without it, agents can't offer personalized experiences grounded in history. Effective memory management allows agents to store and retrieve relevant information, delivering responses grounded in historical data and user preferences. This changes them from basic question-answering systems into adaptive assistants that improve through repeated interactions.

### How does Redis enhance AI agent memory capabilities?

Redis enhances agent memory by unifying vector search, in-memory storage, and flexible data structures on one real-time platform, instead of requiring separate tools for each function. This integration reduces latency and complexity compared to systems requiring separate tools for each memory function. Redis is designed to deliver sub-millisecond read and write performance for many workloads, enabling fast retrieval during complex decision-making. Its native support for vector embeddings simplifies semantic search, allowing accurate retrieval of relevant memories without extensive custom configuration.

### What's the difference between short-term and long-term memory in AI agents?

Short-term memory holds context for a single conversation, while long-term memory persists across sessions so an agent can learn and adapt over time. With Redis, short-term memory typically uses in-memory storage with sub-millisecond latency for quick retrieval. Long-term memory uses Redis' vector search capabilities, breaking information into semantic vectors for retrieval through conceptual similarity rather than exact keywords.

### How do vector embeddings enable semantic search in agent memory?

Vector embeddings let an agent retrieve memories by conceptual similarity instead of exact keyword matching. When an agent receives a query, it generates an embedding and compares it with stored embeddings using similarity measures like cosine similarity. A query about "traveling to Paris" might retrieve memories about "visiting France" based on embedded semantic relationships, ensuring contextually appropriate responses.

### What architectural decisions should I consider when building AI agents with Redis?

Building AI agent memory with Redis comes down to four decisions: which memory types you need, how to store and compress them, how to retrieve them, and how to manage decay. Determine the memory types your app requires: short-term for conversational context or long-term forms like episodic, procedural, and semantic memory. Design strategies for summarizing and vectorizing interactions to avoid data bloat and ensure rapid retrieval. Choose effective memory retrieval methods, leveraging vector search for semantic similarity or hierarchical retrieval systems. Consider memory decay management using Redis' eviction policies.
