---
title: "Getting Started with Redis Iris"
linkTitle: "Getting Started with Redis Iris"
url: "/tutorials/getting-started-with-redis-iris/"
description: "Redis Iris consists of five core tools that work together:"
group: "For AI"
date: 2026-06-16
lastmod: 2026-06-20
hidden: true
mirrored: true
---

*Published 16 June 2026 · updated 20 June 2026*

> **TL;DR:** Redis Iris is a purpose-built context and memory platform designed to bridge the gap between AI agents and fragmented enterprise data. It acts as a foundational layer in the AI stack, providing AI agents with live, accurate, and navigable data so they can operate reliably in production.
>
> This tutorial walks through three of its tools using free Redis Cloud and Google Colab notebooks. For each tool you create the service in the Redis Cloud console, set Colab secrets, run a notebook walkthrough, inspect data in Redis Insight, then clean up.

Redis Iris consists of five core tools that work together:

| Tool                                                                   | Description                                                                                                                                                                                                                                                                                     |
| ---------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **[Redis Context Retriever](https://redis.io/context-retriever/)**     | Defines a semantic model of your business entities (e.g., customers, tickets, policies) and automatically generates Model Context Protocol (MCP) tools. Instead of querying databases blindly, agents can dynamically discover and execute these tools with scoped keys and row-level security. |
| **[Redis Agent Memory](https://redis.io/agent-memory/)**               | Manages both short-term session state and long-term durable memory across multiple interactions.                                                                                                                                                                                                |
| **[Redis Data Integration (RDI)](https://redis.io/data-integration/)** | Continuously ingests and synchronizes data from external systems (such as relational databases and data warehouses) into Redis so agents always act on fresh context.                                                                                                                           |
| **[Redis LangCache](https://redis.io/langcache/)**                     | A semantic caching service that stores and reuses LLM responses for similar queries, drastically reducing API costs and latency.                                                                                                                                                                |
| **[Redis Search](https://redis.io/search/)**                           | The core data layer powering the platform, enabling fast retrieval across structured, unstructured, and vector data.                                                                                                                                                                            |

This tutorial will cover LangCache, Agent Memory, and Context Retriever.

> **NOTE:** This tutorial uses the code from the following Google Colab notebooks:
>
> - [LangCache](https://colab.research.google.com/github/redis-developer/getting-started-with-redis-iris/blob/main/colab/langcache.ipynb)
> - [Agent Memory](https://colab.research.google.com/github/redis-developer/getting-started-with-redis-iris/blob/main/colab/agent_memory.ipynb)
> - [Context Retriever](https://colab.research.google.com/github/redis-developer/getting-started-with-redis-iris/blob/main/colab/context_retriever.ipynb)

## Prerequisites

- Redis Cloud account
- Redis Insight (optional, for inspecting data)
- Google Colab

## Setup

### 1. Create a database

From the Redis Cloud console, select **New Database.** Then click **Try 30 MB for free** to create a free Redis database in the cloud.

![01-create-db](/images/site-mirror/d5bc7fe6f0d43d968aa2648d540c0b18316a6568-2332x1188.webp)

#### Cloud settings

| Setting              | Description                                       |
| -------------------- | ------------------------------------------------- |
| **Name**             | Name of your database.                            |
| **Database version** | Version of your cloud database, leave as default. |
| **Cloud vendor**     | The cloud infrastructure service provider.        |
| **Region**           | The region where your database will be hosted.    |

Name your database and click **Create database.**

### 2. Redis Insight

You can use the web version of Redis Insight or optionally [download the desktop app](https://cloud.redis.io/#/rlec-downloads). The Redis Insight desktop app will allow for faster bulk loading of data, but this tutorial will cover how to load data with both.

In the Redis Cloud console in your database's **Configuration** page, click **Connect**.

Choose either **Open in desktop** or **Launch Redis Insight web**.

![01-connect-db](/images/site-mirror/f76e78a208382e5ba9a657860869d5dea465ddf9-986x856.webp)

## Redis LangCache

### 1. Create a LangCache Service

From the Redis Cloud console, select **LangCache** from the left-hand menu. This takes you to the **Create LangCache service** page.

![02-create-langcache](/images/site-mirror/8edd30f5dc1e74d69c8b2c4c0650725e9a17f173-2050x1748.webp)

#### General settings

| Setting                   | Description                                                                     |
| ------------------------- | ------------------------------------------------------------------------------- |
| **Service name**          | A name that describes your service's purpose.                                   |
| **Select database**       | The Redis Cloud database to use for this service.                               |
| **TTL**                   | Time to live for cache entries, in milliseconds. Default: no expiration.        |
| **User for this service** | Database access user. Only the default user is supported during public preview. |

#### Embedding settings

| Setting                        | Description                                                                                           |
| ------------------------------ | ----------------------------------------------------------------------------------------------------- |
| **Embedding Provider**         | Choose between Redis, OpenAI, or Bring your own. Any provider must support the OpenAI embeddings API. |
| **Embedding provider API key** | Your provider's API key (OpenAI and Bring your own only).                                             |
| **Embedding provider URL**     | Your provider's API URL (Bring your own only).                                                        |
| **Model**                      | The embedding model to use.                                                                           |
| **Similarity threshold**       | Minimum similarity score to consider a cached response a match. Range: 0.5–1.0. Default: 0.92.        |

> **NOTE:** Higher values mean more precise matches; lower values increase match rate but may include less relevant results.

#### Attributes settings (optional)

Attributes provide scoping capabilities for your cache operations — think of them as tags that help organize cached data.

You can define up to 5 custom attributes:

1. Select **Add attribute**.
2. Enter a descriptive name and select the checkmark to save.
3. Repeat to add additional attributes (up to 5).

#### Create the service

When you have finished configuring your service, select **Create**.

A window will display your **LangCache service key**. Select **Copy** to save it.

> **WARNING:** This is the only time the service key is shown. Save it to a secure location before closing the dialog. If you lose it, you will need to generate a new key.

### 2. Configure your environment

This notebook runs in Google Colab and reads its configuration from Colab secrets.

Open [LangCache Colab notebook](https://colab.research.google.com/github/redis-developer/getting-started-with-redis-iris/blob/main/colab/langcache.ipynb).

In the Colab sidebar, select the **Secrets** tab and add the following secrets, making sure **Notebook access** is enabled for each:

| Secret name          | Value                                                                                             |
| -------------------- | ------------------------------------------------------------------------------------------------- |
| `LANGCACHE_ENDPOINT` | Your LangCache endpoint URL. For `LANGCACHE_ENDPOINT`, copy the URL of the region closest to you. |
| `LANGCACHE_ID`       | Your LangCache ID.                                                                                |
| `LANGCACHE_KEY`      | The service key you copied when creating the service.                                             |

Find `LANGCACHE_ENDPOINT` and `LANGCACHE_ID` on your service's **Configuration** page in the Redis Cloud console under **Connectivity**.

![03-langcache-vars](/images/site-mirror/810a69a907d10511972dbed9b9b3c9e05dff532f-2506x1104.webp)

### 3. Notebook Walkthrough

#### Install dependencies

```python
%pip install langcache
```

#### Import libraries

```python
from langcache import LangCache
from google.colab import userdata
```

#### Load secrets and initialize the client

```python
langcache_endpoint = userdata.get("LANGCACHE_ENDPOINT")
langcache_id = userdata.get("LANGCACHE_ID")
langcache_key = userdata.get("LANGCACHE_KEY")

llm_cache = LangCache(
    server_url=langcache_endpoint,
    cache_id=langcache_id,
    api_key=langcache_key
)
```

#### Save a cache entry

```python
save_response = await llm_cache.set_async(
    prompt="How does semantic caching work?",
    response="Semantic caching stores and retrieves data based on meaning, not exact matches."
)

print(save_response.model_dump_json())
```

#### Search for a cached entry

```python
search_response = await llm_cache.search_async(prompt="What is semantic caching?")

print(search_response.model_dump_json(indent=2))
```

Even though the search prompt differs slightly from the saved prompt, the semantic similarity is high enough that LangCache returns the cached response — no LLM call required.

#### View data in Redis Insight

Open Redis Insight and connect to your database to browse the cached entries stored by LangCache.

![04-langcache-insight](/images/site-mirror/bb2f651da40f8c98e8eedb8fe41e9811bfa5e3aa-1534x892.webp)

### 4. Clean up

Go to the LangCache configuration page in the Redis Cloud console. Scroll down to Actions, click Delete next to Delete service.

## Redis Agent Memory

### 1. Create an Agent Memory Service

From the Redis Cloud console, select **Agent Memory** from the left-hand menu. Select **Create custom** and configure the service settings.

![05-create-agent-memory](/images/site-mirror/e720caece503c172f4dbf7fa418c67ea69edb8e0-2048x1122.webp)

#### General settings

| Setting                   | Description                                                                     |
| ------------------------- | ------------------------------------------------------------------------------- |
| **Service name**          | A name that describes your service's purpose.                                   |
| **Select database**       | The Redis Cloud database to use for this service.                               |
| **User for this service** | Database access user. Only the default user is supported during public preview. |

#### Memory configuration

| Setting            | Description                                                                                                    |
| ------------------ | -------------------------------------------------------------------------------------------------------------- |
| **Short-term TTL** | Time to live for session (short-term) memory. Can be set in seconds, minutes, hours, or days. Default: 1 hour. |
| **Long-term TTL**  | Time to live for long-term memory. Default: 365 days.                                                          |

#### Create the service

When you have finished configuring your service, select **Create**.

A window will display your **Agent Memory service key**. Select **Copy** to save it.

> **WARNING:** This is the only time the service key is shown. Save it to a secure location before closing the dialog. If you lose it, you will need to generate a new key.

### 2. Configure your environment

This notebook runs in Google Colab and reads its configuration from Colab secrets.

Open [Agent Memory Colab notebook](https://colab.research.google.com/github/redis-developer/getting-started-with-redis-iris/blob/main/colab/agent_memory.ipynb).

In the Colab sidebar, select the **Secrets** tab and add the following secrets, making sure **Notebook access** is enabled for each:

| Secret name             | Value                                             |
| ----------------------- | ------------------------------------------------- |
| `AGENT_MEMORY_ENDPOINT` | Your Agent Memory endpoint.                       |
| `AGENT_MEMORY_STORE_ID` | Your Agent Memory store ID.                       |
| `AGENT_MEMORY_KEY`      | The service key you just copied in the last step. |

Find `AGENT_MEMORY_ENDPOINT` and `AGENT_MEMORY_STORE_ID` on your service's **Configuration** page in the Redis Cloud console.

![06-agent-memory-vars](/images/site-mirror/651be121c88a56a30e3c27918f14b139a5379c09-2506x842.webp)

### 3. Notebook Walkthrough

#### Install dependencies

```python
%pip install redis-agent-memory
```

#### Import libraries

```python
import time

from redis_agent_memory import AgentMemory, models
from google.colab import userdata
```

#### Load secrets and initialize the client

```python
agent_memory_endpoint = userdata.get("AGENT_MEMORY_ENDPOINT")
agent_memory_store_id = userdata.get("AGENT_MEMORY_STORE_ID")
agent_memory_key = userdata.get("AGENT_MEMORY_KEY")

agent_memory = AgentMemory(
    agent_memory_endpoint,
    store_id=agent_memory_store_id,
    api_key=agent_memory_key,
)

health_response = await agent_memory.health_async()
print(health_response.model_dump_json())
```

#### Add a session (short-term) memory event

```python
add_session = await agent_memory.add_session_event_async(
    session_id="session-1",
    actor_id="user-123",
    role=models.MessageRole.USER,
    content=[{"text": "My favorite chill anime is Frieren: Beyond Journey's End"}],
    created_at=int(time.time() * 1000),
)

print(add_session.model_dump_json(indent=2))
```

#### Retrieve session memory

```python
session_memory = await agent_memory.get_session_memory_async(session_id="session-1")

print(session_memory.model_dump_json(indent=2))
```

#### Add a long-term memory

```python
create_ltm = await agent_memory.bulk_create_long_term_memories_async(memories=[
    {"id": "memory-1", "owner_id": "user-123", "text": "Semantic memory stores facts and knowledge for later retrieval."},
])

print(create_ltm.model_dump_json())
```

#### Get long-term memory by `memory_id`

```python
get_ltm = await agent_memory.get_long_term_memory_async(memory_id="memory-1")

print(get_ltm.model_dump_json(indent=2))
```

#### Search all long-term memories by `owner_id`

```python
search_ltm = await agent_memory.search_long_term_memory_async(request={
    "text": "",
    "filter":{
        "owner_id": {
            "eq": "user-123"
        }
    }
})

print(search_ltm.model_dump_json(indent=2))
```

> **NOTE:** Agent Memory automatically creates long-term memories from session memory (e.g. "User prefers non-stop flights"). You might have to wait a few minutes and re-run the search query see the auto-created long-term memories.

#### View data in Redis Insight

Open Redis Insight and connect to your database to browse the session and long-term memory entries stored by Agent Memory.

![07-agent-memory-insight](/images/site-mirror/c1bed98f6d7a410f048a27612b47acf733a9baf1-1546x1264.webp)

### 4. Clean up

Go to the Agent Memory configuration page in the Redis Cloud console. Scroll down to Actions, click Delete next Delete service.

## Redis Context Retriever

### 1. Load data into Redis

In the Redis Cloud console, open your `redis-iris` database confiuration page create during the Setup step and click **Connect**.

Choose either **Open in desktop** for the desktop app or **Launch Redis Insight web**.

![01-connect-db](/images/site-mirror/f76e78a208382e5ba9a657860869d5dea465ddf9-986x856.webp)

#### If using Redis Insight Desktop

Click **Bulk Actions** then **Upload Data** tab.

Drag and drop the [`data.redis`](https://github.com/redis-developer/getting-started-with-redis-iris/blob/main/data.redis) file from [this repo](https://github.com/redis-developer/getting-started-with-redis-iris/) into Redis Insight and click **Upload** to load in the hospital management dataset.

![08-load-data-desktop](/images/site-mirror/2525108fb10dba05455fa373889e3c940caff00c-1548x1506.webp)

#### If using Redis Insight Web

Click on the **Workbench** tab and paste in the contents of [`data.redis`](https://github.com/redis-developer/getting-started-with-redis-iris/blob/main/data.redis). Then click **Run** to load in the hospital management dataset.

![08-load-data-web](/images/site-mirror/ccebcb15aa01bfc502fe2a1a96bf92be26892cb4-2894x1236.webp)

### 2. Create a Context Retriever Service

From the Redis Cloud console, select **Context Retriever** from the left-hand menu.

If this is your first service, you'll see an introduction page. Otherwise, select **New service**. From the introduction page, select **Create custom service** to manually configure your settings.

![09-create-context-retriever](/images/site-mirror/d2ed1b7a0ea76cb242d830d9b926f229a518633b-2054x832.webp)

#### General settings

| Setting             | Description                                       |
| ------------------- | ------------------------------------------------- |
| **Service name**    | A name that describes your service's purpose.     |
| **Select database** | The Redis Cloud database to use for this service. |
| **Description**     | A description of your context retriever.          |

Select **Entities** to continue.

#### Define entities

Entities map to the business objects stored in your Redis database.

1. Select **Add Entity**.
2. In the **Entity name** field, enter the name of a business object (e.g., `Treatment`).
3. In the **Key Template** field, enter the Redis key pattern, using `{id}` to denote the ID location (e.g., `treatment:{id}`).
4. Optionally add a description.
5. Select the checkmark to confirm the entity.
6. Repeat for all 5 entities, then select **Fields** to continue.

> **NOTE:** I recommend creating all 5 entities but for this tutorial you will only need a minimum of the `Treatement` and `Appointment` entities mapped.

| Entity Name     | Key Template       |
| --------------- | ------------------ |
| **Treatment**   | `treatment:{id}`   |
| **Appointment** | `appointment:{id}` |
| **Patient**     | `patient:{id}`     |
| **Doctor**      | `doctor:{id}`      |
| **Bill**        | `bill:{id}`        |

![10-context-retriever-entities](/images/site-mirror/d2544f0c7ec10d78df9eec75f79d310566e5b944-2038x1136.webp)

#### Configure fields

In this step, you define the fields of each entity and the relationships between them. You have two options:

- **Auto-detect fields** — scans your database automatically using a model to detect fields. You will need to agree to let the model scan your key names and schemas.
- **Manual configuration** — define each field yourself, marking them as `NUMERIC` or `TEXT` to generate additional `find` and `search` MCP tools.

We'll use a combination of both. We'll first use Auto-detect to define the fields and relationshships then manually configure certain fields to be `NUMERIC` or `TEXT`.

1. Click **Auto-detect fields**, this will scan your database and infer entity fields. This will also automatically map the relationships between your entities based on the entity's field key names.
2. Consent to auto-detect scand and click **Scan Database**.
3. Configure the field indexes. At a minimum, you'll need to configure 3 fields in the `Treatement` entity. Click on the entity's pencil icon then the **Configure** button to configure indexes of the entities:

- `Treatment` entity:
    - `treatment_type` to be `TEXT`
    - `descritption` to be `TEXT`
    - `cost` to be `NUMERIC`

> **NOTE:** Each field can only be a part of 1 index. You might encounter errors if you try to include fields in both the `TAG` and `TEXT` indexes.

4. Make sure to click the checkmark to confirm the changes.
5. Optionally, go through the other entites and configure the field indexes as `TEXT` or `NUMERIC` as needed.

![11-context-retriever-fields](/images/site-mirror/145867df32827335ef51b5ffd2285f0c57977bec-896x539.webp)

6. After configuring all fields, select **Create** to create the service.

### 3. Configure your environment

You will access your Context Retriever via an agent key. To create a Context Retriever agent key, go to the Redis Cloud console and open your Context Retriever service page.

1. Navigate to the **Agent key** tab in your service configuration page and select **New Agent Key**. Name and generate your agent key.

    ![12-context-retriever-agent-key](/images/site-mirror/33e49340162039c9277bdae1ea7d227ba0df1c62-1062x1100.webp)

2. Copy and save the agent key

3. This notebook runs in Google Colab and reads its configuration from Colab secrets.

    Open [Context Retriever Colab notebook](https://colab.research.google.com/github/redis-developer/getting-started-with-redis-iris/blob/main/colab/context_retriever.ipynb).

    In the Colab sidebar, select the **Secrets** tab and add the following secrets, making sure **Notebook access** is enabled for each:

    | Secret name                   | Value                          |
    | ----------------------------- | ------------------------------ |
    | `CONTEXT_RETRIEVER_AGENT_KEY` | The agent key you just copied. |

### 4. Notebook Walkthrough

#### Install dependencies

```python
%pip install redis-context-retriever
```

#### Import libraries

```python
import json

from context_surfaces import UnifiedClient
from google.colab import userdata
```

#### Load secrets

```python
agent_key = userdata.get("CONTEXT_RETRIEVER_AGENT_KEY")
```

#### Initialize the client and list available tools

Context Retriever automatically generates MCP tools from your entity definitions. List them to see what's available:

```python
context_retriever = UnifiedClient()

tools = await context_retriever.list_tools(agent_key)

print(f"Total tools: {len(tools)}")
for t in tools:
    try:
        name = t.get("name")
        desc = t.get("description")
        inputSchema = t.get("inputSchema", {"type": "object", "properties": {}})

        print(f"Name: {name}")
    except Exception as e:
        print(e)
```

#### Call the tools

Use `query_tool` to call any of the generated MCP tools directly:

```python
# Filter all appointments by patient_id
filter_response = await context_retriever.query_tool(
    agent_key=agent_key,
    tool_name="filter_appointment_by_patient_id",
    arguments={"value": "P002", "limit": 10}
)

# Process filter response
print("Filter results:")
filter_results = json.loads(filter_response["content"][0]["text"])["results"]
for a in filter_results:
    print(a)
```

```python
# Get a doctor by doctor_id
get_response = await context_retriever.query_tool(
    agent_key=agent_key,
    tool_name="get_doctor_by_id",
    arguments={"id": "D010"}
)

# Process get data
print("Get result:")
get_result = json.loads(get_response["content"][0]["text"])
print(get_result)
```

```python
# Search treatments by text query with the "MRI" keyword
search_response = await context_retriever.query_tool(
    agent_key=agent_key,
    tool_name="search_treatment_by_text",
    arguments={"query": "MRI", "limit": 10}
)

# Process search data
print("Search results:")
search_results = json.loads(search_response["content"][0]["text"])["results"]
for t in search_results:
    print(t)
```

```python
# Find treatments by cost ranging from 100 to 1000
find_response = await context_retriever.query_tool(
    agent_key=agent_key,
    tool_name="find_treatment_by_cost_range",
    arguments={"min_value": 100, "max_value": 1000, "limit": 10}
)

# Process range data
print("Cost range results:")
find_results = json.loads(find_response["content"][0]["text"])["results"]
for c in find_results:
    print(c)
```

#### Context Retriever tool names

The tool names (e.g. `filter_appointment_by_patient_id`, `get_doctor_by_id`, etc.) reflect the entities defined in a sample healthcare dataset. Your tool names will match the entities you defined in your own Context Retriever service.

| **Index** | MCP tool generated               |
| --------- | -------------------------------- |
| `PK`      | `get_<entity>_by_id`             |
| `TAG`     | `filter_<entity>_by_<field>`     |
| `TEXT`    | `search_<entity>_by_text`        |
| `NUMERIC` | `find_<entity>_by_<field>_range` |

### 5. Clean up

Go to the Context Retriever configuration page in the Redis Cloud console. Scroll down to Actions, next to Delete service click Delete.

## Next Steps

For more in-depth guidance, explore the following:

### Tutorials

1. [Semantic caching with Redis LangCache](https://redis.io/tutorials/semantic-caching-with-redis-langcache/)
2. [Redis Agent Memory and LangGraph](https://redis.io/tutorials/redis-agent-memory-with-langgraph/)
3. [Real-time AI agent with Redis Iris](https://redis.io/tutorials/redis-iris-call-agent/)

### References

- [Redis Iris Docs](https://redis.io/docs/latest/develop/ai/context-engine/)
- [Blog post: Context Is All You Need](https://redis.io/blog/context-is-all-you-need/)
- [GitHub: Getting started with Redis Iris](https://github.com/redis-developer/getting-started-with-redis-iris/)
