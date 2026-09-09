---
title: "LangGraph & Redis: Build smarter AI agents with memory & persistence"
linkTitle: "LangGraph & Redis: Build smarter AI agents with memory & persistence"
url: "/blog/langgraph-redis-build-smarter-ai-agents-with-memory-persistence/"
description: "Today, we’re excited to introduce langgraph-checkpoint-redis, a new integration bringing Redis’ powerful memory capabilities to LangGraph. This collaboration gives developers the tools to build..."
date: 2025-03-28
blogCategories:
- "Tech"
authors:
- "Brian Sam-Bodden"
lastmod: 2026-06-01
hidden: true
---

*By Brian Sam-Bodden, Principal Applied AI Engineer · Published 28 March 2025 · updated 1 June 2026*

![Blog tile image](/images/site-mirror/411fd9c5d030cee0c49817321dedefaed6346e8a-772x552.webp)

Today, we’re excited to introduce [langgraph-checkpoint-redis](https://github.com/redis-developer/langgraph-redis), a new integration bringing Redis’ powerful memory capabilities to LangGraph. This collaboration gives developers the tools to build more effective AI agents with persistent memory across conversations and sessions.

[LangGraph](https://www.langchain.com/langgraph) is an open-source framework for building stateful, agentic workflows with LLMs. With this Redis integration, developers can now leverage both thread-level persistence and cross-thread memory to create agents that remember context, learn from experiences, and make better decisions over time.

## Why Redis for AI agents?

When building effective AI agents, memory is crucial. The most successful implementations use simple, composable patterns that manage memory effectively. Redis is perfect for this role:

1. **High-performance persistence**: Ultra-fast read/write operations (<1ms latency) for storing agent state
1. **Flexible memory types**: Support for both short-term (thread-level) and long-term (cross-thread) memory
1. **Vector capabilities**: Built-in vector search for semantic memory retrieval
1. **Scalability**: Linear scaling for production deployments with increasing memory needs
1. **Developer-friendly**: Simple implementation that complements LangGraph’s focus on composable patterns

## How langgraph-checkpoint-redis works

The langgraph-checkpoint-redis package offers two core capabilities that map directly to memory patterns in agentic systems:

### 1. Redis checkpoint savers: Thread-level “short-term” memory

RedisSaver and AsyncRedisSaver provide thread-level persistence, allowing agents to maintain continuity across multiple interactions within the same conversation thread:

- **Preserves conversation state**: Perfect for multi-turn interactions where context matters
- **Efficient JSON storage**: Optimized for fast retrieval of complex state objects
- **Synchronous and async APIs**: Flexibility for different application architectures

### 2. Redis Store: Cross-thread “long-term” memory

RedisStore and AsyncRedisStore enable cross-thread memory, letting agents access and store information that persists across different conversation threads:

- **Vector search capabilities**: Retrieve semantically relevant information using embeddings
- **Metadata filtering**: Find specific memories based on user IDs, categories, or other attributes
- **Namespaced organization**: Structure memories for different users and use cases

## Memory in practice: Building a chat agent with persistence

Let’s see how easy it is to add memory to a simple chatbot using Redis persistence:

```python
from typing import Literal

from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.redis import RedisSaver

# Define a simple tool
@tool
def get_weather(city: Literal["nyc", "sf"]):
    """Use this to get weather information."""
    if city == "nyc":
        return "It might be cloudy in nyc"
    elif city == "sf":
        return "It's always sunny in sf"
    else:
        raise AssertionError("Unknown city")

# Set up model and tools
tools = [get_weather]
model = ChatOpenAI(model="gpt-4o-mini", temperature=0)

# Create Redis persistence
REDIS_URI = "redis://localhost:6379"
with RedisSaver.from_conn_string(REDIS_URI) as checkpointer:
    # Initialize Redis indices (only needed once)
    checkpointer.setup()
    
    # Create agent with memory
    graph = create_react_agent(model, tools=tools, checkpointer=checkpointer)
    
    # Use the agent with a specific thread ID to maintain conversation state
    config = {"configurable": {"thread_id": "user123"}}
    res = graph.invoke({"messages": [("human", "what's the weather in sf")]}, config)

```

This simple setup allows the agent to remember the conversation history for “user123” across multiple interactions. The thread ID acts as a conversation identifier, and all state is stored in Redis for fast retrieval.

## Cross-thread memory: Remembering user information

For more advanced use cases, you might want agents to remember information about users across different conversation threads. Here’s a simplified example using RedisStore for cross-thread memory:

```python
import uuid

from langchain_anthropic import ChatAnthropic
from langchain_core.runnables import RunnableConfig

from langgraph.checkpoint.redis import RedisSaver
from langgraph.graph import START, MessagesState, StateGraph
from langgraph.store.redis import RedisStore
from langgraph.store.base import BaseStore

# Set up model
model = ChatAnthropic(model="claude-3-5-sonnet-20240620")

# Function that uses store to access and save user memories
def call_model(state: MessagesState, config: RunnableConfig, *, store: BaseStore):
    user_id = config["configurable"]["user_id"]
    namespace = ("memories", user_id)
    
    # Retrieve relevant memories for this user
    memories = store.search(namespace, query=str(state["messages"][-1].content))
    info = "\n".join([d.value["data"] for d in memories])
    system_msg = f"You are a helpful assistant talking to the user. User info: {info}"
    
    # Store new memories if the user asks to remember something
    last_message = state["messages"][-1]
    if "remember" in last_message.content.lower():
        memory = "User name is Bob"
        store.put(namespace, str(uuid.uuid4()), {"data": memory})
    
    # Generate response
    response = model.invoke(
        [{"role": "system", "content": system_msg}] + state["messages"]
    )
    return {"messages": response}

# Build the graph
builder = StateGraph(MessagesState)
builder.add_node("call_model", call_model)
builder.add_edge(START, "call_model")

# Initialize Redis persistence and store
REDIS_URI = "redis://localhost:6379"
with RedisSaver.from_conn_string(REDIS_URI) as checkpointer:
    checkpointer.setup()
    
    with RedisStore.from_conn_string(REDIS_URI) as store:
        store.setup()
        
        # Compile graph with both checkpointer and store
        graph = builder.compile(checkpointer=checkpointer, store=store)

```

When using this agent, we can maintain both conversation state (thread-level) and user information (cross-thread) simultaneously:

```python
# First conversation - tell the agent to remember something
config = {"configurable": {"thread_id": "convo1", "user_id": "user123"}}
response = graph.invoke(
    {"messages": [{"role": "user", "content": "Hi! Remember: my name is Bob"}]},
    config
)

# Second conversation - different thread but same user
new_config = {"configurable": {"thread_id": "convo2", "user_id": "user123"}}
response = graph.invoke(
    {"messages": [{"role": "user", "content": "What's my name?"}]},
    new_config
)
# Agent will respond with "Your name is Bob"

```

## Memory types and agentic systems

In their article on memory in agentic workflows, Turing Post categorizes AI memory into long-term and short-term components:

- **Long-term memory** includes:

  - Explicit (declarative) memory for facts and structured knowledge
  - Implicit memory for learned patterns and procedures
- **Short-term memory** consists of:

  - Context window (amount of information available in current interaction)
  - Working memory (dynamic information used for current reasoning)

Redis excels at supporting both memory types for agentic workflows:

- Thread-level persistence with RedisSaver handles working memory and context
- Cross-thread storage with RedisStore provides long-term explicit memory
- Vector search through Redis enables efficient retrieval of relevant memories

## Implementation details

Under the hood, langgraph-checkpoint-redis uses several Redis features to provide efficient memory:

1. **Redis JSON data structure**: Stores nested JSON data structures representing agent state
1. **Redis Query Engine**: Provides indexing capabilities for fast state retrieval
1. **Vector search**: The Redis Query Engine provides high-performance vector operations that enable semantic retrieval when using RedisStore

The implementation includes both synchronous and asynchronous APIs to support different application architectures:

```python
# Synchronous API
with RedisSaver.from_conn_string(REDIS_URI) as checkpointer:
    checkpointer.setup()
    # ... use synchronously ...

# Asynchronous API
async with AsyncRedisSaver.from_conn_string(REDIS_URI) as checkpointer:
    await checkpointer.asetup()
    # ... use asynchronously ...

```

## Available implementations

The package provides multiple implementations to suit different needs:

1. **Standard implementations**: RedisSaver and AsyncRedisSaver for full checkpoint history
1. **Shallow implementations**: ShallowRedisSaver and AsyncShallowRedisSaver for storing only the latest checkpoint
1. **Store implementations**: RedisStore and AsyncRedisStore for cross-thread memory with vector search

## Building better agents with memory

Successful agentic systems are built with simplicity and clarity, not complexity. The Redis integration for LangGraph adopts this philosophy by providing straightforward, performant memory solutions that can be composed into sophisticated agent architectures.

Whether you’re building a simple chatbot that remembers conversation context or a complex agent that maintains user profiles across multiple interactions, langgraph-checkpoint-redis gives you the building blocks to make it happen efficiently and reliably.

## Getting started

To start using Redis with LangGraph today:

```
pip install langgraph-checkpoint-redis

```

Check out the GitHub repository at [https://github.com/redis-developer/langgraph-redis](https://github.com/redis-developer/langgraph-redis) for comprehensive documentation and examples.

By combining LangGraph’s agentic workflows with Redis’s powerful memory capabilities, you can build AI agents that feel more natural, responsive, and personalized. The agent’s ability to remember and learn from interactions makes all the difference between a mechanical tool and an assistant that truly understands your needs over time.
