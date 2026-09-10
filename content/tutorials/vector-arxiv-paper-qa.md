---
title: "Build an academic RAG app for arXiv paper Q&A with Redis and LangChain"
linkTitle: "Build an academic RAG app for arXiv paper Q&A with Redis and LangChain"
url: "/tutorials/vector-arxiv-paper-qa/"
description: "In this tutorial you will build a paper Q&A app for intermediate Python devs. Along the way you will learn how to:"
group: "For AI"
date: 2026-03-18
lastmod: 2026-03-18
hidden: true
---

*Published 18 March 2026*

> **TL;DR:**
>
> Build an academic RAG app that pulls papers from arXiv, chunks and embeds them,
> stores those vectors in Redis, and answers questions against a topic-scoped paper
> index. Redis fits this workload because it gives you fast vector search,
> low-latency retrieval, and simple index introspection in one place.

> **Note:** This tutorial uses the code from the following git repository:
>
> `https://github.com/redis-developer/ArXivChatGuru.git`

## What you'll learn

In this tutorial you will build a paper Q&A app for intermediate Python devs.
Along the way you will learn how to:

- Fetch papers from arXiv based on a topic query
- Split paper content into chunks and embed those chunks with OpenAI
- Store paper chunks in Redis for fast vector search
- Build topic-scoped Redis indexes so each paper set stays isolated
- Ask grounded questions about the active topic corpus in a Streamlit app
- Inspect Redis index stats to understand what the app stored

## Key terms

**RAG** (retrieval-augmented generation) is an AI pattern that grounds a large language model's answers in real data. Instead of relying on training knowledge alone, a RAG system retrieves relevant documents at query time and passes them to the model as context, reducing hallucinations and keeping answers current.

[**arXiv**](https://arxiv.org/) is an open-access repository of research papers covering physics, math, computer science, and related fields. Researchers upload preprints to arXiv before or alongside peer review, making it one of the largest freely available sources of academic content.

**Vector search** lets you find documents by semantic meaning rather than exact keywords. Each document is converted into a numeric vector (an embedding), and queries are matched against those vectors using distance metrics like cosine similarity. Redis supports vector search natively through its [Query Engine](https://redis.io/docs/latest/develop/interact/search-and-query/).

[**LangChain**](https://python.langchain.com/) is a Python framework for building language-model apps. It provides modular components for text splitting, vector stores, prompt templates, and retrieval chains that you can assemble into a pipeline.

## What you'll build

You will build a lightweight academic RAG app called ArXiv ChatGuru. The app lets
you enter a topic like `graph neural networks` or `diffusion models`, pulls recent
papers from arXiv, loads those papers into Redis, and answers questions using the
retrieved paper context.

The app has two screens:

1. A Streamlit chat screen where you load a topic into Redis and ask questions
2. A stats screen where you inspect the active Redis index

This is a good Redis use case because the app needs fast retrieval over a
changing, topic-specific document set. Redis gives you vector search for the
retrieval step and a simple way to inspect the active paper index after loading.

If you want a more general intro to vector search first, start with
[Perform vector search using Redis](/tutorials/howtos/solutions/vector/getting-started-vector/).
If you want a generic product-data RAG example, see
[Build a RAG GenAI chatbot with Redis](/tutorials/howtos/solutions/vector/gen-ai-chatbot/).

## How does the academic RAG flow work?

At a high level, the app follows this sequence:

1. The user enters a research topic and a paper count
2. The app loads matching papers from arXiv
3. LangChain splits those papers into smaller text chunks
4. OpenAI embeddings convert those chunks into vectors
5. Redis stores the chunks and embeddings in a topic-scoped index
6. Each user question is matched against the active Redis index with vector search
7. The retrieved context is sent to the chat model to generate the answer

## Why does Redis fit paper Q&A well?

Redis is a strong fit for this app because it handles the retrieval layer with very
little moving infrastructure. For a topic-scoped academic RAG workflow you want to:

- Load a small to medium paper corpus quickly
- Search that corpus by semantic meaning, not exact keywords
- Rebuild the active corpus when the topic changes
- Inspect the current index to see what you loaded

Redis handles all of that in one product. You do not need one system for the
vector store and another to inspect the active dataset. That makes the app easier
to explain, easier to run locally, and easier to extend.

## Prerequisites

- [Python 3.13](https://www.python.org/downloads/) for local development
- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- An [OpenAI API key](https://platform.openai.com/signup)
- `make` available in your shell

You also need the source code. Clone the ArXiv ChatGuru repo:

> **GITHUB CODE**
>
> `git clone https://github.com/redis-developer/ArXivChatGuru.git`

## How do you configure the app?

Create a local `.env` file from the template:

```bash
cp .env.template .env
```

Set at least your OpenAI key:

```bash
OPENAI_API_KEY=your_key_here
```

The default config uses these values:

```bash
OPENAI_CHAT_MODEL=gpt-5.4-mini
OPENAI_EMBEDDING_MODEL=text-embedding-3-small
REDIS_INDEX_BASENAME=arxiv
REDIS_URL=redis://arxivchatguru-redis:6379
```

The `REDIS_INDEX_BASENAME` value is important because the app derives a
topic-scoped index name from it. If you load `graph neural networks`, the app
creates a Redis index name that starts with `arxiv-` and ends with a stable hash
for that topic.

## How do you run Redis and the app?

The app uses a Docker-first local setup with `redis:alpine`.

Start the app and Redis together:

```bash
make docker-up
```

Then open:

```text
http://localhost:8501
```

If you prefer local Python execution, install dependencies and run Streamlit:

```bash
python3 -m poetry env use python3.13
make install
make dev
```

## How do you load papers into Redis?

Once the app is running:

1. Enter a topic in the **Topic Area** field
2. Choose how many papers to load
3. Click **Load papers into Redis**

The app pulls papers from arXiv, splits them into chunks, and writes those chunks
to Redis with a topic-scoped index name. When the topic changes, the app clears
the previous active index and rebuilds the paper set for the new topic.

Topic-scoped indexing is important here because the paper set changes every time
the user switches topics. You are not indexing one fixed knowledge base. Each
topic gets its own Redis index, so the retrieval step always targets the right
paper set.

## What code creates the topic-scoped Redis index?

The app builds the Redis config directly in Python so it can control the index
name, key prefix, metadata fields, and embedding dimensions for each topic:

```python
METADATA_SCHEMA = [
    {"name": "title", "type": "text"},
    {"name": "authors", "type": "tag"},
    {"name": "category", "type": "tag"},
    {"name": "links", "type": "tag"},
]

def get_index_config(topic: str) -> RedisConfig:
    return RedisConfig(
        index_name=get_index_name(topic),
        key_prefix=get_index_prefix(topic),
        redis_url=REDIS_URL,
        storage_type="hash",
        content_field="text",
        embedding_field="embedding",
        metadata_schema=METADATA_SCHEMA,
        embedding_dimensions=get_embedding_dimensions(),
        legacy_key_format=False,
    )
```

Before the app writes a fresh paper set, it drops the current topic index with
[`FT.DROPINDEX`](https://redis.io/docs/latest/commands/ft.dropindex/) if one
already exists:

```python
def clear_index(topic: str) -> None:
    redis_client = get_redis_client()
    try:
        redis_client.execute_command("FT.DROPINDEX", get_index_name(topic), "DD")
    except ResponseError as exc:
        error_text = str(exc).lower()
        if "no such index" not in error_text and "unknown index name" not in error_text:
            raise
    finally:
        redis_client.close()
```

This gives you predictable reload behavior. Loading a new topic rebuilds the active
paper index instead of mixing old and new papers together.

## How does the app answer questions?

After the topic index is ready, the app creates a RetrievalQA chain with Redis as
the retriever:

```python
chain = make_qna_chain(
    llm,
    arxiv_db,
    prompt=prompt,
    k=st.session_state["num_context_docs"],
    search_type="similarity",
)
```

When a user enters a question, the app runs vector search against the active Redis
index, retrieves the closest chunks, and passes that context to the chat model.
The UI also shows the retrieved context so you can inspect what Redis returned.

## How do you inspect the Redis index?

The app includes a stats page that reads index metadata and Query Engine metrics
for the active topic:

- Index name
- Prefixes
- Indexed fields
- Document counts
- Vector index size

Use this page to verify what Redis stored after a paper load and to connect the
chat experience back to the underlying data structures.

> **Tip:** Download [Redis Insight](https://redis.io/insight/) to visually explore your Redis data or run raw commands in the workbench. It gives you another way to inspect the indexes and documents the app creates.

## How do you test the app?

The repo includes focused automated coverage for the Redis-heavy paths:

```bash
make test
```

The tests cover:

- Prompt rendering
- Metadata normalization
- Topic-scoped Redis config generation
- Missing-index handling during rebuild and reset
- Stats helpers for the active Redis index

## What should you know before using this pattern in production?

The app is intentionally small. A production-grade academic RAG workflow would
likely add:

- Better chunking tuned for long technical papers
- Filtering by year, author, or category before retrieval
- Stronger result caching and document reuse
- Rate limiting and usage controls around the LLM calls
- Persistent chat history if you want multi-turn memory

You should also expect live arXiv results to change over time. The same topic may
return a slightly different paper set next week than it does today.

## Summary

This app shows how Redis handles the retrieval layer in an academic RAG workflow. You used topic-scoped indexes to keep each paper set isolated, vector search to match questions against embedded paper chunks, and the [`FT.DROPINDEX`](https://redis.io/docs/latest/commands/ft.dropindex/) command to rebuild the index when the topic changes. Redis acts as the vector store, the metadata store, and the index-introspection layer in a single product.

## Next steps

- [Perform vector search using Redis](/tutorials/howtos/solutions/vector/getting-started-vector/) if you want the Redis retrieval mechanics first
- [Semantic text search with Redis](/tutorials/howtos/solutions/vector/semantic-text-search/) for a retrieval-only variant
- [Build a RAG GenAI chatbot with Redis](/tutorials/howtos/solutions/vector/gen-ai-chatbot/) for a more general RAG walkthrough
- [What is AI agent memory? Example using LangGraph and Redis](/tutorials/what-is-agent-memory-example-using-langgraph-and-redis/) if you want to add memory to a future version of this app
- [Try Redis Cloud free](https://redis.io/try-free/) on AWS, Azure, or Google Cloud -- the fastest way to deploy Redis for your AI workloads
- Download [Redis Insight](https://redis.io/insight/) to visually explore your Redis data and run commands in the workbench
